#!/usr/bin/env python3
"""
스터디 노트 빌더: Markdown -> self-contained HTML.

사용법:
    python3 tools/build_html.py part1_basics/02_recursive_state_estimation/02_recursive_state_estimation.md

동작:
  - Markdown을 HTML로 변환 (표준 라이브러리만 사용, 외부 의존성 없음)
  - LaTeX 수식($...$, $$...$$)은 손대지 않고 통과시켜 MathJax가 렌더링
  - MathJax tex-svg 번들(tools/vendor/tex-svg.js)을 <script>로 인라인 (외부 폰트 불필요)
  - 이미지(images/*.png)를 base64 data URI로 인라인
  - <!--widget:NAME--> 마커를 tools/widgets/NAME.html 내용으로 치환
  - h1/h2로 사이드바 목차 자동 생성

출력: 입력 .md와 같은 폴더에 같은 이름의 .html
"""

import base64
import html
import mimetypes
import re
import sys
from pathlib import Path

# 킷 루트 = tools/ 의 부모 (kit.conf · 위젯 · MathJax 가 있는 곳)
# 스터디 루트 = ref/ 나 part*/ 가 있는 곳. 킷 루트이거나 그 한 단계 위다.
# (킷을 스터디 루트에 펼쳐 두든 하위 폴더에 담아 두든 똑같이 동작한다.
#  판정 규칙은 tools/kit_config.py 맨 위 docstring 참조)
KIT = Path(__file__).resolve().parent.parent
ROOT = next((d for d in (KIT, KIT.parent)
             if (d / "ref").is_dir() or any(d.glob("part*/"))), KIT)

# 사이드바 머리말 — kit.conf 에서 읽는다 (없으면 기본값).
#   brand     = My Book
#   booktitle = Author — 스터디 노트
BRAND, BOOKTITLE = "스터디 노트", ""
_conf = KIT / "kit.conf"
if not _conf.exists():
    _conf = ROOT / "kit.conf"
if _conf.exists():
    for _line in _conf.read_text(encoding="utf-8").splitlines():
        _line = _line.split("#", 1)[0].strip()
        if "=" not in _line:
            continue
        _k, _v = (x.strip() for x in _line.split("=", 1))
        if _k == "brand":
            BRAND = _v
        elif _k == "booktitle":
            BOOKTITLE = _v
VENDOR = KIT / "tools" / "vendor"
WIDGETS = KIT / "tools" / "widgets"


# ---------------------------------------------------------------- placeholders

class Vault:
    """마크다운 변환 중 건드리면 안 되는 조각(수식/코드)을 잠시 보관한다."""

    def __init__(self):
        self.items = []

    def stash(self, value):
        token = f"\x00VAULT{len(self.items)}\x00"
        self.items.append(value)
        return token

    def restore(self, text):
        for i, value in enumerate(self.items):
            text = text.replace(f"\x00VAULT{i}\x00", value)
        return text


# ------------------------------------------------------------------- utilities

def slugify(text, used):
    text = re.sub(r"\$[^$]*\$", "", text)          # 수식 제거
    text = re.sub(r"[*`_\[\]()]", "", text)        # 마크다운 기호 제거
    text = text.strip().lower()
    text = re.sub(r"[^\w가-힣\s.-]", "", text)
    slug = re.sub(r"[\s.]+", "-", text).strip("-") or "sec"
    base, n = slug, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    return slug


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


# ------------------------------------------------------------ inline markdown

def inline(text, vault):
    """문단 내부 서식. 수식/코드는 이미 vault에 보관된 상태로 들어온다.
    (vault 복원은 build() 최상위에서 한 번만 수행한다.)"""
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    # ==강조== → 원문의 색 강조를 재현한다. 수식은 이미 vault에 들어가 있으므로
    # 강조 구간 안의 인라인 수식도 함께 감싸진다. MathJax SVG 글리프는
    # currentColor를 상속하므로 \color 매크로 없이 수식까지 같이 물든다 (3_Pitfalls B6 회피).
    text = re.sub(r"==([^=\n]+)==", r'<span class="hl">\1</span>', text)
    return text


# ------------------------------------------------------------- block markdown

def convert(md, vault, base_dir):
    lines = md.split("\n")
    out, toc = [], []
    used_slugs = set()
    i, n = 0, len(lines)

    def close_list(stack):
        while stack:
            out.append(f"</{stack.pop()}>")

    list_stack = []

    while i < n:
        line = lines[i]

        # --- widget marker
        m = re.match(r"\s*<!--\s*widget:([\w-]+)\s*-->\s*$", line)
        if m:
            close_list(list_stack)
            path = WIDGETS / f"{m.group(1)}.html"
            out.append(path.read_text(encoding="utf-8") if path.exists()
                       else f"<!-- missing widget: {m.group(1)} -->")
            i += 1
            continue

        # --- fenced code
        if line.startswith("```"):
            close_list(list_stack)
            lang = line[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(buf), quote=False)
            out.append(f'<div class="codewrap"><pre><code class="lang-{lang}">{code}</code></pre></div>')
            continue

        # --- horizontal rule
        if re.match(r"^\s*---+\s*$", line):
            close_list(list_stack)
            out.append('<hr>')
            i += 1
            continue

        # --- heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list(list_stack)
            level, raw = len(m.group(1)), m.group(2).strip()
            slug = slugify(raw, used_slugs)
            out.append(f'<h{level} id="{slug}">{inline(raw, vault)}</h{level}>')
            if level <= 2:
                toc.append((level, slug, re.sub(r"\$[^$]*\$|[*`]", "", raw).strip()))
            i += 1
            continue

        # --- blockquote (연속 라인 묶음)
        if line.startswith(">"):
            close_list(list_stack)
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            # 첫 줄이 [!TIP] 이면 원문의 tcolorbox 를 재현한 Tip 박스로 낸다
            label = None
            if buf and re.fullmatch(r"\[!(\w+)\]", buf[0].strip()):
                label = re.fullmatch(r"\[!(\w+)\]", buf[0].strip()).group(1).title()
                buf = buf[1:]
            inner, _ = convert("\n".join(buf), vault, base_dir)
            if label:
                out.append(f'<div class="callout"><span class="callout-label">{label}</span>'
                           f'<div class="callout-body">{inner}</div></div>')
            else:
                out.append(f'<blockquote>{inner}</blockquote>')
            continue

        # --- table
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            close_list(list_stack)
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{inline(c, vault)}</th>" for c in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c, vault)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')
            continue

        # --- list item
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            indent = len(m.group(1))
            ordered = m.group(2).endswith(".")
            tag = "ol" if ordered else "ul"
            depth = indent // 2
            while len(list_stack) > depth + 1:
                out.append(f"</{list_stack.pop()}>")
            if len(list_stack) == depth + 1 and list_stack[-1] != tag:
                out.append(f"</{list_stack.pop()}>")
            if len(list_stack) < depth + 1:
                out.append(f"<{tag}>")
                list_stack.append(tag)
            item = [m.group(3)]
            i += 1
            # 이어지는 들여쓰기 연속 줄을 같은 항목으로 흡수
            while i < n and lines[i].strip() and not re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i]) \
                    and not lines[i].startswith(("#", ">", "```", "|")) \
                    and (len(lines[i]) - len(lines[i].lstrip())) > indent:
                item.append(lines[i].strip())
                i += 1
            out.append(f"<li>{inline(' '.join(item), vault)}</li>")
            continue

        # --- blank
        if not line.strip():
            close_list(list_stack)
            i += 1
            continue

        # --- standalone image (자체 문단)
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if m:
            close_list(list_stack)
            alt, src = m.group(1), m.group(2)
            p = (base_dir / src)
            uri = data_uri(p) if p.exists() else src
            out.append(f'<figure><img src="{uri}" alt="{html.escape(alt, quote=True)}"></figure>')
            i += 1
            continue

        # --- paragraph
        close_list(list_stack)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|>|```|\s*[-*]\s|\s*\d+\.\s|\s*---+\s*$|\|)", lines[i]) \
                and not re.match(r"\s*<!--\s*widget:", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{inline(' '.join(buf), vault)}</p>")

    close_list(list_stack)
    return "\n".join(out), toc


# ---------------------------------------------------------------------- shell

def build(md_path):
    md_path = Path(md_path).resolve()
    base_dir = md_path.parent
    md = md_path.read_text(encoding="utf-8")

    vault = Vault()

    # 순서 중요: 코드펜스는 convert()가 직접 처리하므로 건너뛰고,
    # 수식과 인라인 코드만 미리 보관해 마크다운 서식 변환에서 보호한다.
    def protect(pattern, text, wrap=None):
        def repl(m):
            body = m.group(0)
            if wrap:
                body = wrap(m)
            return vault.stash(body)
        return re.sub(pattern, repl, text, flags=re.S)

    # 코드펜스 내부는 보호 대상에서 제외하기 위해 분리 처리
    segments = re.split(r"(```.*?```)", md, flags=re.S)
    for k, seg in enumerate(segments):
        if seg.startswith("```"):
            continue
        seg = protect(r"\$\$.+?\$\$", seg,
                      wrap=lambda m: '<div class="mathblock">' + html.escape(m.group(0), quote=False) + "</div>")
        seg = protect(r"(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)", seg,
                      wrap=lambda m: html.escape(m.group(0), quote=False))
        seg = protect(r"`[^`\n]+`", seg,
                      wrap=lambda m: "<code>" + html.escape(m.group(0)[1:-1], quote=False) + "</code>")
        segments[k] = seg
    md = "".join(segments)

    body, toc = convert(md, vault, base_dir)
    body = vault.restore(body)

    title = re.search(r"^#\s+(.*)$", md_path.read_text(encoding="utf-8"), re.M)
    title = title.group(1).strip() if title else md_path.stem

    toc_html = "\n".join(
        f'<a class="lvl{lvl}" href="#{slug}">{html.escape(text, quote=False)}</a>'
        for lvl, slug, text in toc
    )

    mathjax = (VENDOR / "tex-svg.js").read_text(encoding="utf-8")

    out_path = md_path.with_suffix(".html")
    out_path.write_text(PAGE.format(
        title=html.escape(title, quote=False),
        brand=html.escape(BRAND, quote=False),
        booktitle=html.escape(BOOKTITLE, quote=False),
        toc=toc_html,
        body=body,
        mathjax=mathjax,
    ), encoding="utf-8")
    kb = out_path.stat().st_size / 1024
    try:                                  # 스터디 루트 밖의 .md 도 빌드할 수 있게
        shown = out_path.relative_to(ROOT)
    except ValueError:
        shown = out_path
    print(f"built {shown}  ({kb:.0f} KB, {len(toc)} toc entries)")
    return out_path


PAGE = """<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --ground:#fbfcfd; --panel:#ffffff; --panel-2:#f2f5f8;
  --ink:#18212b; --ink-soft:#4a5866; --ink-faint:#778695;
  --rule:#dbe3ea; --rule-soft:#eaeff4;
  --accent:#1f5f9e; --accent-soft:#e8f0f8;
  --hl:#197fb2;                      /* 원문의 파란 강조색 그대로 */
  --predict:#b4632f; --correct:#25715f;
  --code-bg:#f4f7fa;
  --shadow:0 1px 2px rgba(24,33,43,.05), 0 8px 24px -16px rgba(24,33,43,.28);
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#0e1419; --panel:#141c24; --panel-2:#1a242e;
    --ink:#dce5ed; --ink-soft:#9fb0bf; --ink-faint:#71828f;
    --rule:#25323d; --rule-soft:#1c262f;
    --accent:#69a8dd; --accent-soft:#16293a;
    --hl:#57b6e4;                    /* 어두운 배경에서 읽히도록 밝힌 값 */
    --predict:#dd9560; --correct:#5cb7a0;
    --code-bg:#111a22;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.7);
  }}
}}
:root[data-theme="dark"] {{
  --ground:#0e1419; --panel:#141c24; --panel-2:#1a242e;
  --ink:#dce5ed; --ink-soft:#9fb0bf; --ink-faint:#71828f;
  --rule:#25323d; --rule-soft:#1c262f;
  --accent:#69a8dd; --accent-soft:#16293a;
  --hl:#57b6e4;
  --predict:#dd9560; --correct:#5cb7a0;
  --code-bg:#111a22;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.7);
}}

/* 산문은 70ch로 고정. 산문이 아닌 블록(수식·코드·표·그림·위젯)만
   좌우로 최대 15ch씩 = 총 30ch까지 넓게 쓴다 (산문 70ch + 최대 30ch = 100ch). */
:root {{ --prose:70ch; --bleed:0px; }}
@media (min-width:1150px) {{ :root {{ --bleed:5ch; }} }}
@media (min-width:1320px) {{ :root {{ --bleed:10ch; }} }}
@media (min-width:1500px) {{ :root {{ --bleed:15ch; }} }}

* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"Pretendard Variable",Pretendard,-apple-system,"Apple SD Gothic Neo",
    "Noto Sans KR","Malgun Gothic",system-ui,sans-serif;
  font-size:16.5px; line-height:1.78;
  -webkit-text-size-adjust:100%;
}}
.shell {{ display:grid; grid-template-columns:274px minmax(0,1fr); gap:0; }}

/* ---- sidebar ---- */
.side {{
  position:sticky; top:0; align-self:start; height:100vh; overflow-y:auto;
  border-right:1px solid var(--rule); background:var(--panel-2);
  padding:2.2rem 1.1rem 3rem 1.6rem;
}}
.side .brand {{
  font-size:.72rem; letter-spacing:.13em; text-transform:uppercase;
  color:var(--ink-faint); font-weight:650; margin-bottom:.15rem;
}}
.side .booktitle {{
  font-size:.95rem; font-weight:680; line-height:1.35; color:var(--ink);
  margin-bottom:1.5rem; text-wrap:balance;
}}
.side nav {{ display:flex; flex-direction:column; gap:1px; }}
.side nav a {{
  color:var(--ink-soft); text-decoration:none; font-size:.845rem; line-height:1.45;
  padding:.34rem .55rem; border-radius:5px; border-left:2px solid transparent;
  transition:background .13s, color .13s;
}}
.side nav a.lvl1 {{ font-weight:660; color:var(--ink); margin-top:.85rem; }}
.side nav a.lvl2 {{ padding-left:1.1rem; }}
.side nav a:hover {{ background:var(--accent-soft); color:var(--accent); }}
.side nav a.active {{ background:var(--accent-soft); color:var(--accent); border-left-color:var(--accent); font-weight:640; }}
.side nav a:focus-visible {{ outline:2px solid var(--accent); outline-offset:1px; }}

/* ---- main ---- */
main {{ padding:3.4rem 3.2rem 8rem; min-width:0; }}
.wrap {{ max-width:var(--prose); margin:0 auto; }}

/* 산문 칸 밖으로 확장되는 블록들 */
.mathblock, .codewrap, .tablewrap, figure, .lab {{
  margin-left:calc(-1 * var(--bleed));
  margin-right:calc(-1 * var(--bleed));
}}

h1,h2,h3,h4 {{ text-wrap:balance; line-height:1.32; }}
h1 {{
  font-size:1.92rem; font-weight:720; letter-spacing:-.017em;
  margin:3.6rem 0 1.1rem; padding-bottom:.55rem; border-bottom:2px solid var(--rule);
}}
h1:first-child {{ margin-top:0; }}
h2 {{ font-size:1.36rem; font-weight:690; letter-spacing:-.012em; margin:2.7rem 0 .85rem; color:var(--ink); }}
h3 {{ font-size:1.06rem; font-weight:670; margin:2rem 0 .6rem; color:var(--accent); letter-spacing:-.004em; }}
h4 {{ font-size:.97rem; font-weight:660; margin:1.5rem 0 .45rem; color:var(--ink-soft); }}
p {{ margin:.95rem 0; }}
strong {{ font-weight:670; }}
hr {{ border:0; border-top:1px solid var(--rule-soft); margin:2.6rem 0; }}
a {{ color:var(--accent); }}

ul,ol {{ margin:.9rem 0; padding-left:1.35rem; }}
li {{ margin:.42rem 0; }}
li::marker {{ color:var(--ink-faint); }}

blockquote {{
  margin:1.5rem 0; padding:.95rem 1.25rem; background:var(--panel);
  border:1px solid var(--rule); border-left:3px solid var(--accent);
  border-radius:0 7px 7px 0; box-shadow:var(--shadow);
}}
blockquote > :first-child {{ margin-top:0; }}
blockquote > :last-child {{ margin-bottom:0; }}
blockquote p {{ font-size:.955rem; color:var(--ink-soft); }}
blockquote strong {{ color:var(--ink); }}

/* ---- 원문의 색 강조 (파란 굵은 글씨) ----
   MathJax SVG 는 currentColor 를 상속하므로 이 안의 인라인 수식도 함께 물든다.
   \\color 매크로를 쓰지 않으므로 3_Pitfalls B6 함정에 걸리지 않는다. */
.hl {{ color:var(--hl); font-weight:640; }}
.hl mjx-container {{ color:inherit; }}

/* ---- 원문의 tcolorbox(Tip 박스) ---- */
.callout {{
  position:relative; margin:2.1rem 0 1.6rem; padding:1.15rem 1.25rem .95rem;
  background:var(--panel); border:1px solid var(--rule);
  border-radius:10px; box-shadow:var(--shadow);
}}
.callout-label {{
  position:absolute; top:-.72rem; left:1.15rem; padding:.12rem .6rem;
  background:var(--panel-2); border:1px solid var(--rule); border-radius:6px;
  font-size:.76rem; font-weight:660; letter-spacing:.02em; color:var(--ink-soft);
}}
.callout-body > :first-child {{ margin-top:0; }}
.callout-body > :last-child {{ margin-bottom:0; }}
.callout-body p {{ font-size:.955rem; }}

figure {{ margin-top:1.9rem; margin-bottom:1.9rem; text-align:center; }}
figure img {{
  max-width:100%; height:auto; border:1px solid var(--rule); border-radius:7px;
  background:#fff; padding:.55rem;
}}

.tablewrap {{ overflow-x:auto; margin-top:1.5rem; margin-bottom:1.5rem; }}
table {{ border-collapse:collapse; width:100%; font-size:.9rem; }}
th,td {{ padding:.55rem .8rem; border-bottom:1px solid var(--rule-soft); text-align:left; vertical-align:top; }}
th {{
  font-size:.75rem; text-transform:uppercase; letter-spacing:.07em;
  color:var(--ink-faint); font-weight:660; border-bottom:1px solid var(--rule);
}}
tbody tr:hover {{ background:var(--panel-2); }}

code {{
  font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  font-size:.875em; background:var(--code-bg); padding:.12em .38em;
  border-radius:4px; border:1px solid var(--rule-soft);
}}
.codewrap {{
  overflow-x:auto; margin-top:1.4rem; margin-bottom:1.4rem;
  border:1px solid var(--rule); border-radius:8px; background:var(--code-bg);
}}
.codewrap pre {{ margin:0; padding:1rem 1.15rem; }}
.codewrap code {{ background:none; border:0; padding:0; font-size:.84rem; line-height:1.62; }}

.mathblock {{
  overflow-x:auto; overflow-y:hidden;
  margin-top:1.15rem; margin-bottom:1.15rem;
  padding:.15rem 0;   /* 좌우 패딩을 두면 음수 마진으로 넓힌 폭이 상쇄된다 */
}}
mjx-container[display="true"] {{ margin:0 !important; }}
mjx-container {{ max-width:none; }}

/* ---- widgets ---- */
.lab {{
  margin-top:2.2rem; margin-bottom:2.2rem;
  border:1px solid var(--rule); border-radius:10px;
  background:var(--panel); box-shadow:var(--shadow); overflow:hidden;
}}
.lab-head {{
  display:flex; align-items:baseline; gap:.7rem; flex-wrap:wrap;
  padding:.85rem 1.15rem; border-bottom:1px solid var(--rule-soft); background:var(--panel-2);
}}
.lab-tag {{
  font-size:.66rem; letter-spacing:.13em; text-transform:uppercase;
  font-weight:700; color:var(--accent); background:var(--accent-soft);
  padding:.22rem .5rem; border-radius:4px;
}}
.lab-title {{ font-size:.95rem; font-weight:670; }}
.lab-note {{ font-size:.82rem; color:var(--ink-faint); }}
.lab-body {{ padding:1.15rem; }}
.lab-body > p {{ font-size:.9rem; color:var(--ink-soft); margin:.5rem 0; }}

.btnrow {{ display:flex; gap:.5rem; flex-wrap:wrap; margin:.55rem 0 .9rem; }}
button {{
  font:inherit; font-size:.855rem; font-weight:600;
  padding:.45rem .85rem; border-radius:6px; cursor:pointer;
  border:1px solid var(--rule); background:var(--panel-2); color:var(--ink);
  transition:background .13s, border-color .13s, transform .06s;
}}
button:hover {{ background:var(--accent-soft); border-color:var(--accent); color:var(--accent); }}
button:active {{ transform:translateY(1px); }}
button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
button.ghost {{ background:transparent; color:var(--ink-faint); }}
button.predict {{ border-color:var(--predict); color:var(--predict); }}
button.predict:hover {{ background:color-mix(in srgb, var(--predict) 12%, transparent); }}
button.correct {{ border-color:var(--correct); color:var(--correct); }}
button.correct:hover {{ background:color-mix(in srgb, var(--correct) 12%, transparent); }}

.sliders {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(215px,1fr)); gap:.7rem 1.4rem; margin:.4rem 0 1rem; }}
.slider {{ display:flex; flex-direction:column; gap:.2rem; }}
.slider label {{ font-size:.78rem; color:var(--ink-soft); display:flex; justify-content:space-between; gap:.6rem; }}
.slider label b {{ font-family:ui-monospace,monospace; font-variant-numeric:tabular-nums; color:var(--ink); font-weight:620; }}
input[type=range] {{ width:100%; accent-color:var(--accent); }}
input[type=range]:focus-visible {{ outline:2px solid var(--accent); outline-offset:3px; }}

canvas {{ display:block; width:100%; height:auto; border-radius:7px; background:var(--panel-2); border:1px solid var(--rule-soft); }}
.readout {{
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-variant-numeric:tabular-nums;
  font-size:.8rem; color:var(--ink-soft); margin-top:.7rem; line-height:1.75;
}}
.readout b {{ color:var(--ink); font-weight:620; }}
.log {{ max-height:9.5rem; overflow-y:auto; margin-top:.65rem; border-top:1px solid var(--rule-soft); padding-top:.55rem; }}
.log div {{
  font-family:ui-monospace,monospace; font-variant-numeric:tabular-nums;
  font-size:.755rem; color:var(--ink-faint); padding:.12rem 0;
}}
.log div:first-child {{ color:var(--ink); }}
.legend {{ display:flex; gap:1.1rem; flex-wrap:wrap; font-size:.76rem; color:var(--ink-soft); margin-top:.6rem; }}
.legend span {{ display:inline-flex; align-items:center; gap:.35rem; }}
.swatch {{ width:.72rem; height:.72rem; border-radius:2px; display:inline-block; }}

@media (max-width:940px) {{
  .shell {{ grid-template-columns:1fr; }}
  .side {{
    position:static; height:auto; border-right:0; border-bottom:1px solid var(--rule);
    padding:1.4rem 1.4rem 1.1rem; max-height:16rem;
  }}
  main {{ padding:2rem 1.35rem 5rem; }}
}}
@media (prefers-reduced-motion: reduce) {{
  * {{ transition:none !important; animation:none !important; }}
}}
</style>

<div class="shell">
  <aside class="side">
    <div class="brand">{brand}</div>
    <div class="booktitle">{booktitle}</div>
    <nav id="toc">
{toc}
    </nav>
  </aside>
  <main><div class="wrap">
{body}
  </div></main>
</div>

<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']],
    processEscapes: true,
    tags: 'none'
  }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script>{mathjax}</script>

<script>
// 넘치는 수식만 골라 폰트 크기를 줄여 폭에 맞춘다.
// 하한 70% — 그보다 더 줄여야 하는 수식은 억지로 줄이지 않고 스크롤을 남긴다
// (읽을 수 없을 만큼 작아지는 것을 방지).
(function () {{
  var MIN = 0.70;
  function fit() {{
    document.querySelectorAll('.mathblock').forEach(function (box) {{
      box.style.fontSize = '';
      var eq = box.querySelector('mjx-container');
      if (!eq) return;
      var avail = box.clientWidth - 2;
      var need = eq.getBoundingClientRect().width;
      if (need > avail && need > 0) {{
        var ratio = Math.max(MIN, (avail / need) * 0.99);
        box.style.fontSize = (ratio * 100).toFixed(1) + '%';
        box.dataset.fitted = ratio.toFixed(2);
      }} else {{
        delete box.dataset.fitted;
      }}
    }});
  }}
  var timer;
  function debounced() {{ clearTimeout(timer); timer = setTimeout(fit, 120); }}
  if (window.MathJax && window.MathJax.startup) {{
    window.MathJax.startup.promise.then(fit);
  }} else {{
    window.addEventListener('load', fit);
  }}
  window.addEventListener('resize', debounced);
}})();

// 사이드바 스크롤 스파이
(function () {{
  var links = Array.prototype.slice.call(document.querySelectorAll('#toc a'));
  var targets = links.map(function (a) {{ return document.getElementById(a.hash.slice(1)); }});
  function sync() {{
    var best = 0;
    for (var i = 0; i < targets.length; i++) {{
      if (targets[i] && targets[i].getBoundingClientRect().top <= 96) best = i;
    }}
    links.forEach(function (a, i) {{ a.classList.toggle('active', i === best); }});
  }}
  window.addEventListener('scroll', sync, {{ passive: true }});
  sync();
}})();
</script>
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        build(arg)
