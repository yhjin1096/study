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
ASIDES = KIT / "tools" / "asides"

# ── aside 카드 (포스트잇) ────────────────────────────────────────────────────
# 본문에는 점선 밑줄만 남기고, 클릭하면 우측 패널에서 전문을 보여 준다.
# 책이 설명 없이 전제하는 배경을 흐름을 끊지 않고 채우기 위한 장치다.
# 작성법은 tools/asides/_GUIDE.md.
ASIDE_REF = re.compile(r"\[\[([\w.-]+?)(?:\|([^\]]+?))?\]\]")
ASIDE_DEF = re.compile(r"^<!--\s*aside:([\w.-]+)\s*(.*?)-->\s*$(.*?)^<!--\s*/aside\s*-->\s*$",
                       re.M | re.S)
# 인용 — "[568]" · "[548, 740]". 마크다운 링크 "[1](url)" 와 겹치지 않게 뒤에 '(' 가
# 오면 넘긴다. refs.json 이 없으면 이 기능 전체가 조용히 꺼진다.
CITE_REF = re.compile(r"\[(\d{1,4}(?:\s*,\s*\d{1,4})*)\](?!\()")


def load_refs():
    """build_refs.py 가 만든 refs.json. 없으면 빈 dict (인용 확장이 꺼진다)."""
    path = KIT / "refs.json"
    if not path.exists():
        return {}
    import json
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("refs", {})
    except (ValueError, OSError):
        return {}


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


# ---------------------------------------------------------------- aside cards

class Cards:
    """aside 카드와 인용을 모은다.

    본문을 훑으며 참조된 것만 기록해 두었다가, 마지막에 그것들만 문서에 싣는다.
    전역 카드가 100개여도 그 챕터가 쓴 것만 들어가므로 HTML 이 부풀지 않는다.
    """

    def __init__(self, local_defs, refs):
        self.local = local_defs          # {이름: (제목, 마크다운 본문)} — 챕터 안 정의
        self.refs = refs                 # refs.json 의 {번호: 서지정보}
        self.used = {}                   # {카드 id: (제목, 본문 마크다운, 종류)}
        self.missing_asides = []
        self.missing_cites = []

    # -- 정의 찾기 ----------------------------------------------------------
    def _lookup(self, name):
        """챕터 로컬이 전역보다 우선한다."""
        if name in self.local:
            return self.local[name]
        path = ASIDES / f"{name}.md"
        if not path.exists():
            return None
        raw = path.read_text(encoding="utf-8")
        title = name
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.S)
        if m:
            for line in m.group(1).splitlines():
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
            raw = raw[m.end():]
        return (title, raw.strip())

    # -- 본문에서 호출되는 두 가지 -------------------------------------------
    def aside_button(self, name, label):
        found = self._lookup(name)
        if not found:
            if name not in self.missing_asides:
                self.missing_asides.append(name)
            return (f'<span class="pin pin-missing" title="정의 없음: {html.escape(name)}">'
                    f'{html.escape(label or name)}</span>')
        title, body = found
        cid = f"a-{slug_id(name)}"
        self.used[cid] = (title, body, "aside")
        return (f'<button type="button" class="pin" data-card="{cid}">'
                f'{html.escape(label or title, quote=False)}</button>')

    def cite_button(self, group):
        out = []
        for num in (n.strip() for n in group.split(",")):
            entry = self.refs.get(num)
            if not entry:
                if num not in self.missing_cites:
                    self.missing_cites.append(num)
                out.append(f'<span class="cite cite-missing">{num}</span>')
                continue
            cid = f"r-{num}"
            title = f"[{num}] {entry.get('short', '')}".strip()
            body = "**{}**\n\n{}".format(
                entry.get("title") or "(제목 없음)", entry.get("raw", ""))
            self.used[cid] = (title, body, "cite")
            out.append(f'<button type="button" class="cite" data-card="{cid}">{num}</button>')
        return '<span class="cites">[' + ", ".join(out) + "]</span>"

    # -- 문서 끝에 실을 카드 뭉치 --------------------------------------------
    def render(self, base_dir):
        if not self.used:
            return ""
        parts = []
        for cid, (title, body, kind) in self.used.items():
            v = Vault()
            html_body = protect_math(body, v)
            html_body, _ = convert(html_body, v, base_dir, cards=None)
            html_body = v.restore(html_body)
            parts.append(
                f'<article class="card card-{kind}" id="{cid}" '
                f'data-title="{html.escape(title, quote=True)}">{html_body}</article>')
        return '<div id="cardvault" aria-hidden="true">\n' + "\n".join(parts) + "\n</div>"

    def report(self):
        n_aside = sum(1 for k in self.used if k.startswith("a-"))
        n_cite = sum(1 for k in self.used if k.startswith("r-"))
        return n_aside, n_cite


def slug_id(name):
    return re.sub(r"[^\w-]", "-", name).strip("-").lower() or "x"


def check_math_pairs(md):
    """`$` 짝이 맞지 않는 줄을 찾는다. 빌드를 막지는 않고 경고만 한다.

    이걸 자동으로 잡아야 하는 이유가 있다. 인용구 안에서 `$…$` 를 두 줄에 걸쳐 쓰면
    둘째 줄의 `>` 가 수식 안으로 들어가 **MathJax 가 문서 전체의 typeset 을 포기한다.**
    수식 하나가 깨지는 것이 아니라 **그 문서의 모든 수식이 원문 그대로 남는다.**
    빌드는 성공하고 콘솔에 오류도 없어서, 브라우저로 열어 보기 전에는 알 수 없다.

    코드펜스 안은 세지 않는다 (`$` 를 셸 프롬프트로 쓰는 일이 흔하다).
    """
    bad, in_fence = [], False
    for no, line in enumerate(md.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.count("$") % 2:
            bad.append((no, line.strip()))
    return bad


def protect_math(md, vault):
    """수식과 인라인 코드를 vault 에 보관해 마크다운 서식 변환에서 지킨다.

    코드펜스 안은 convert() 가 직접 처리하므로 건드리지 않는다.
    """
    def protect(pattern, text, wrap=None):
        def repl(m):
            return vault.stash(wrap(m) if wrap else m.group(0))
        return re.sub(pattern, repl, text, flags=re.S)

    segments = re.split(r"(```.*?```)", md, flags=re.S)
    for k, seg in enumerate(segments):
        if seg.startswith("```"):
            continue
        seg = protect(r"\$\$.+?\$\$", seg,
                      wrap=lambda m: '<div class="mathblock">'
                                     + html.escape(m.group(0), quote=False) + "</div>")
        seg = protect(r"(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)", seg,
                      wrap=lambda m: html.escape(m.group(0), quote=False))
        seg = protect(r"`[^`\n]+`", seg,
                      wrap=lambda m: "<code>"
                                     + html.escape(m.group(0)[1:-1], quote=False) + "</code>")
        segments[k] = seg
    return "".join(segments)


def extract_aside_defs(md):
    """챕터 안의 `<!--aside:이름 제목-->…<!--/aside-->` 를 걷어 낸다.

    걷어 낸 자리는 지운다 — 정의는 본문에 그대로 나오면 안 되고,
    참조된 지점에서 카드로만 보여야 한다.
    """
    defs = {}

    def take(m):
        defs[m.group(1)] = (m.group(2).strip() or m.group(1), m.group(3).strip())
        return ""

    return ASIDE_DEF.sub(take, md), defs


# ------------------------------------------------------------ inline markdown

def inline(text, vault, cards=None):
    """문단 내부 서식. 수식/코드는 이미 vault에 보관된 상태로 들어온다.
    (vault 복원은 build() 최상위에서 한 번만 수행한다.)

    cards 가 주어지면 aside 참조 `[[이름]]` 와 인용 `[568]` 을 카드 버튼으로 바꾸고,
    어떤 카드가 쓰였는지 cards 에 기록한다 (build() 가 그것만 문서에 싣는다).
    """
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    if cards is not None:
        text = ASIDE_REF.sub(lambda m: cards.aside_button(m.group(1), m.group(2)), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    if cards is not None:
        text = CITE_REF.sub(lambda m: cards.cite_button(m.group(1)), text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    return text


# ------------------------------------------------------------- block markdown

def convert(md, vault, base_dir, cards=None):
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
            out.append(f'<h{level} id="{slug}">{inline(raw, vault, cards)}</h{level}>')
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
            # cards 를 넘겨야 인용구 안의 [[aside]] · [568] 도 카드가 된다.
            # 보충 설명은 인용구로 감싸 쓰는 일이 많아 여기서 빠지면 크게 샌다.
            inner, _ = convert("\n".join(buf), vault, base_dir, cards=cards)
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
            th = "".join(f"<th>{inline(c, vault, cards)}</th>" for c in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c, vault, cards)}</td>" for c in r) + "</tr>"
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
            out.append(f"<li>{inline(' '.join(item), vault, cards)}</li>")
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
        out.append(f"<p>{inline(' '.join(buf), vault, cards)}</p>")

    close_list(list_stack)
    return "\n".join(out), toc


# ---------------------------------------------------------------------- shell

def build(md_path):
    md_path = Path(md_path).resolve()
    base_dir = md_path.parent
    md = md_path.read_text(encoding="utf-8")

    # aside 정의를 먼저 걷어 낸다 — 본문에 그대로 나오면 안 되고, 참조 지점에서
    # 카드로만 보여야 한다. 수식 보호(protect_math)보다 앞서야 정의 안의 수식도 산다.
    md, local_defs = extract_aside_defs(md)
    cards = Cards(local_defs, load_refs())
    unpaired = check_math_pairs(md)

    vault = Vault()
    md = protect_math(md, vault)

    body, toc = convert(md, vault, base_dir, cards=cards)
    body = vault.restore(body)
    cardvault = cards.render(base_dir)

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
        cardvault=cardvault,
        mathjax=mathjax,
    ), encoding="utf-8")
    kb = out_path.stat().st_size / 1024
    try:                                  # 스터디 루트 밖의 .md 도 빌드할 수 있게
        shown = out_path.relative_to(ROOT)
    except ValueError:
        shown = out_path
    print(f"built {shown}  ({kb:.0f} KB, {len(toc)} toc entries)")

    n_aside, n_cite = cards.report()
    if n_aside or n_cite:
        n_local = sum(1 for k, (_, _, kind) in cards.used.items()
                      if kind == "aside" and k[2:] in
                      {slug_id(x) for x in local_defs})
        print(f"  aside 카드 {n_aside}개 (전역 {n_aside - n_local} · 로컬 {n_local})"
              f" · 인용 {n_cite}개")
    if cards.missing_asides:
        print("  ⚠ 정의 없는 aside 참조: "
              + ", ".join(f"[[{n}]]" for n in cards.missing_asides))
    if cards.missing_cites:
        print("  ⚠ refs.json 에 없는 인용: "
              + ", ".join(f"[{n}]" for n in cards.missing_cites))
    if unpaired:
        print(f"  ⚠ '$' 짝이 안 맞는 줄 {len(unpaired)}개 —"
              " 이 문서의 수식이 **전부** 렌더링되지 않을 수 있다")
        for no, text in unpaired[:6]:
            print(f"      {no}: {text[:76]}")
        print("      → 여러 줄로 나뉜 수식을 한 줄로 합쳐라 (3_Pitfalls.md B1-3)")
    return out_path


PAGE = """<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{
  --ground:#fbfcfd; --panel:#ffffff; --panel-2:#f2f5f8;
  --ink:#18212b; --ink-soft:#4a5866; --ink-faint:#778695;
  --rule:#dbe3ea; --rule-soft:#eaeff4;
  --accent:#1f5f9e; --accent-soft:#e8f0f8;
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

/* ---- aside 카드 (포스트잇) ---- */
/* 본문 표시: 점선 밑줄만. 흐름을 끊지 않는 것이 목적이다. */
.pin {{
  font:inherit; color:var(--accent); background:none; border:0; padding:0 .06em;
  border-bottom:1px dashed var(--accent); cursor:pointer; line-height:inherit;
}}
.pin::after {{ content:"\\2009\\25E6"; font-size:.8em; vertical-align:.15em; opacity:.75; }}
.pin:hover, .pin:focus-visible {{ background:var(--accent-soft); border-bottom-style:solid; }}
.pin-missing {{ color:var(--ink-faint); border-bottom:1px dashed var(--ink-faint); cursor:help; }}

.cites {{ white-space:nowrap; color:var(--ink-faint); }}
.cite {{
  font:inherit; font-size:.92em; color:var(--accent); background:none; border:0;
  padding:0; cursor:pointer; text-decoration:underline dotted;
}}
.cite:hover, .cite:focus-visible {{ text-decoration-style:solid; }}
.cite-missing {{ color:#b4553d; text-decoration:underline wavy; }}

/* 카드 보관소 — 화면 밖이지만 레이아웃은 계산된다.
   display:none 으로 숨기면 MathJax 가 수식 크기를 0 으로 잡는다. */
#cardvault {{
  position:absolute; left:-99999px; top:0;
  width:min(30rem, 92vw); visibility:hidden;
}}

#drawer {{
  position:fixed; top:0; right:0; bottom:0; z-index:60;
  width:min(30rem, 92vw); display:flex; flex-direction:column;
  background:var(--panel); border-left:1px solid var(--rule);
  box-shadow:-12px 0 32px rgba(16,28,40,.14);
  transform:translateX(101%); transition:transform .22s ease;
}}
#drawer.open {{ transform:none; }}
#drawer-head {{
  display:flex; align-items:flex-start; gap:.75rem; flex:none;
  padding:1rem 1.1rem .8rem; border-bottom:1px solid var(--rule);
  background:var(--panel-2);
}}
#drawer-title {{ font-weight:650; font-size:.98rem; line-height:1.4; flex:1; }}
#drawer-close {{
  flex:none; font:inherit; font-size:1.3rem; line-height:1; padding:.1rem .4rem;
  color:var(--ink-soft); background:none; border:0; border-radius:.3rem; cursor:pointer;
}}
#drawer-close:hover {{ background:var(--rule-soft); color:var(--ink); }}
#drawer-body {{ flex:1; overflow-y:auto; padding:1.1rem 1.2rem 2.5rem; }}
#drawer-body .card {{ font-size:.94rem; }}
#drawer-body > .card > :first-child {{ margin-top:0; }}
#drawer-body .card-cite {{ color:var(--ink-soft); }}
/* 패널이 좁아 본문 크기 그대로면 표와 코드가 가로로 넘친다 */
#drawer-body table {{ font-size:.86em; }}
#drawer-body pre {{ font-size:.82em; }}
#drawer-body h1, #drawer-body h2 {{ font-size:1.05rem; }}
#drawer-body h3, #drawer-body h4 {{ font-size:.98rem; }}
/* 인용 카드의 원문 서지 한 줄은 흐리게 — 제목이 먼저 읽혀야 한다 */
#drawer-body .card-cite p:last-child {{ font-size:.9em; color:var(--ink-faint); }}
#drawer-scrim {{
  position:fixed; inset:0; z-index:59; background:rgba(16,28,40,.28);
  opacity:0; pointer-events:none; transition:opacity .22s ease;
}}
#drawer-scrim.open {{ opacity:1; pointer-events:auto; }}

/* 좁은 화면에서는 아래에서 올라오는 시트로 */
@media (max-width: 640px) {{
  #drawer {{
    top:auto; left:0; width:auto; max-height:78vh;
    border-left:0; border-top:1px solid var(--rule);
    border-radius:.9rem .9rem 0 0; transform:translateY(101%);
  }}
  #drawer.open {{ transform:none; }}
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

{cardvault}
<div id="drawer-scrim"></div>
<div id="drawer" role="dialog" aria-modal="false" aria-labelledby="drawer-title">
  <div id="drawer-head">
    <div id="drawer-title"></div>
    <button id="drawer-close" type="button" aria-label="닫기">&times;</button>
  </div>
  <div id="drawer-body"></div>
</div>

<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']],
    processEscapes: true,
    tags: 'none',

    // ── 동적 로드를 끈다 ─────────────────────────────────────────────
    // 이 HTML 은 self-contained 라 네트워크도, 옆에 놓인 확장 파일도 없다.
    // 그런데 기본 설정의 autoload 는 번들에 없는 매크로를 만나면 확장을
    // 받아 오려 하고, 실패하면 **startup.promise 가 reject 되어 문서 전체의
    // typeset 이 중단된다.** 수식 하나가 깨지는 게 아니라 전부 원문 그대로
    // 남는다 — 빌드는 성공하고 콘솔 오류도 없어서 찾기가 매우 어렵다.
    // (실제로 \\boldsymbol 하나 때문에 문서의 수식 252개가 전부 죽었다.)
    //
    // 끄고 나면 없는 매크로는 그 자리만 빨갛게 표시되고 나머지는 정상이다.
    packages: {{ '[-]': ['require', 'autoload'] }},

    macros: {{
      // 번들에 없지만 자주 쓰는 것들은 있는 것으로 치환해 둔다.
      boldsymbol: ['{{\\\\mathbf{{#1}}}}', 1]
    }}
  }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }},
  svg: {{ fontCache: 'global' }},
  startup: {{
    // 그래도 무언가 실패했을 때 조용히 넘어가지 않도록 남긴다.
    pageReady: function () {{
      return window.MathJax.startup.defaultPageReady().catch(function (err) {{
        console.error('MathJax typeset 실패:', err);
      }});
    }}
  }}
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

// aside 카드 — 클릭하면 우측 패널에서 연다.
//
// 카드는 #cardvault 안에 미리 렌더돼 있고(화면 밖·레이아웃은 계산됨), 열 때
// 패널로 **옮긴다**. 복제하지 않는 이유: MathJax 가 이미 그려 놓은 SVG 를 그대로
// 쓰기 위해서다. display:none 으로 숨겼다면 수식 크기가 0 으로 잡혔을 것이다.
(function () {{
  var vault = document.getElementById('cardvault');
  var panel = document.getElementById('drawer');
  var scrim = document.getElementById('drawer-scrim');
  var head = document.getElementById('drawer-title');
  var bodyEl = document.getElementById('drawer-body');
  if (!panel || !vault) return;

  var current = null, lastFocus = null;

  function close() {{
    if (current) {{ vault.appendChild(current); current = null; }}
    panel.classList.remove('open');
    scrim.classList.remove('open');
    if (lastFocus) {{ lastFocus.focus(); lastFocus = null; }}
  }}

  function open(id, trigger) {{
    var card = document.getElementById(id);
    if (!card) return;
    if (current === card) {{ close(); return; }}   // 같은 것을 또 누르면 닫는다
    if (current) vault.appendChild(current);
    lastFocus = trigger || null;
    current = card;
    head.textContent = card.dataset.title || '';
    bodyEl.appendChild(card);
    bodyEl.scrollTop = 0;
    panel.classList.add('open');
    scrim.classList.add('open');
    document.getElementById('drawer-close').focus();
  }}

  document.addEventListener('click', function (e) {{
    var btn = e.target.closest('.pin[data-card], .cite[data-card]');
    if (btn) {{ e.preventDefault(); open(btn.dataset.card, btn); }}
  }});
  document.getElementById('drawer-close').addEventListener('click', close);
  scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {{
    if (e.key === 'Escape' && current) close();
  }});
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
