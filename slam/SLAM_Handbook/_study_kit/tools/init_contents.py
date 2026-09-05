#!/usr/bin/env python3
"""PDF 북마크에서 `0_Contents.md` 의 목차 부분을 만든다.

사용법:
    python3 _study_kit/tools/init_contents.py                 # 화면에 출력
    python3 _study_kit/tools/init_contents.py --write         # 0_Contents.md 갱신
    python3 _study_kit/tools/init_contents.py --dump          # 북마크 원본을 그대로

왜 필요한가
-----------
목차를 손으로 옮겨 적으면 반드시 오타가 난다. `pdftotext` 로 인쇄된 목차 쪽을
파싱하는 방법도 있지만, 텍스트 레이어는 하이픈을 흘리고 합자를 깨뜨린다
(3_Pitfalls.md A13). **PDF 북마크는 조판이 아니라 구조에서 나오므로 그 두 문제가
없다.** 북마크가 있는 책이라면 이쪽이 가장 정확하다.

무엇을 하는가
-------------
북마크의 레벨을 그대로 쓰지 않고 **번호 형태로 판정한다.** 레벨 부여가 책마다
제각각이기 때문이다.

    Part I Foundations of SLAM     → ## Part I. Foundations of SLAM
    1 Factor Graphs for SLAM       → ### 1장. Factor Graphs for SLAM (p.19)
    1.1 Visualizing SLAM With …    → - 1.1 Visualizing SLAM With … (20)
    I Prelude                      → ### Prelude I (p.3)
    I.1 What is SLAM?              → - I.1 What is SLAM? (3)
    Epilogue                       → ### Epilogue (p.548)
    References / Author index …    → (건너뜀 — 학습 대상이 아니다)

쪽번호는 `kit.conf` 의 `page_offset` 으로 PDF 쪽 → 책 쪽으로 환산한다.

만든 뒤에는 반드시 대조한다:
    python3 _study_kit/tools/check_toc.py
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_config

try:
    import fitz
except ImportError:
    raise SystemExit("PyMuPDF 가 필요하다:  sudo apt install -y python3-fitz")

CFG = kit_config.load()

# 북마크 제목의 맨 앞 번호를 뜯어낸다.
#   "1 Factor Graphs"      → ('1',    'Factor Graphs')
#   "1.1 Visualizing …"    → ('1.1',  'Visualizing …')
#   "I Prelude"            → ('I',    'Prelude')
#   "III.2 Spatial AI …"   → ('III.2','Spatial AI …')
NUMBERED = re.compile(r'^((?:\d+|[IVXLC]+)(?:\.\d+)*)\s+(.*)$')
PART = re.compile(r'^Part\s+([IVXLC]+|\d+)\b\s*(.*)$', re.I)

# 학습 대상이 아닌 뒷부분 — 목차에 넣지 않는다.
SKIP = {"references", "author index", "subject index", "index",
        "table of contents", "contents", "list of contributors"}


def clean(title):
    """북마크 제목을 한 줄로 다듬는다.

    원문에서 두 줄로 조판된 제목은 북마크에 공백 여러 개로 이어져 들어온다.
    예: "3 Robustness to Incorrect Data   Association and Outliers"
    """
    return re.sub(r'\s+', ' ', title).strip()


def is_roman(s):
    return bool(re.fullmatch(r'[IVXLC]+', s))


def entries(pdf_path):
    """북마크를 (kind, number, title, book_page) 목록으로.

    kind 는 'part' | 'chapter' | 'prelude' | 'epilogue' | 'section'.
    """
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    if not toc:
        raise SystemExit(
            "이 PDF 에는 북마크가 없다. 인쇄된 목차 쪽을 pdftotext -layout 으로 뽑아\n"
            "손으로 옮긴 뒤 check_toc.py 로 대조하라 (3_Pitfalls.md A13 주의).")

    out = []
    for _lvl, raw, pdf_page in toc:
        title = clean(raw)
        book_page = kit_config.pdf_to_book(pdf_page, CFG)

        m = PART.match(title)
        if m:
            out.append(("part", m.group(1).upper(), clean(m.group(2)), book_page))
            continue

        if title.lower() in SKIP:
            continue
        if title.lower() == "epilogue":
            out.append(("epilogue", "", title, book_page))
            continue

        m = NUMBERED.match(title)
        if not m:
            continue                      # Foreword · Preface · Notation 등 앞머리
        num, rest = m.group(1), clean(m.group(2))

        if "." in num:
            out.append(("section", num, rest, book_page))
        elif is_roman(num):
            out.append(("prelude", num, rest, book_page))
        else:
            out.append(("chapter", num, rest, book_page))
    return out


def render(rows):
    """목차 markdown 을 만든다. 형식은 check_toc.py 가 읽는 그대로다."""
    lines, progress = [], []
    for kind, num, title, page in rows:
        if kind == "part":
            lines += ["", f"## Part {num}. {title}", ""]
        elif kind == "prelude":
            lines.append(f"### Prelude {num} (p.{page})")
            progress.append((f"Prelude {num}", title or "Prelude"))
        elif kind == "epilogue":
            lines += ["", f"### Epilogue (p.{page})"]
            progress.append(("Epilogue", ""))
        elif kind == "chapter":
            lines += ["", f"### {num}장. {title} (p.{page})"]
            progress.append((f"{num}장", title))
        else:
            lines.append(f"- {num} {title} ({page})")
    return "\n".join(lines).strip() + "\n", progress


def render_progress(progress):
    out = ["| 장 | 노트 | 그림 | 위젯 |", "|---|---|---|---|"]
    for label, title in progress:
        name = f"{label} {title}".strip()
        out.append(f"| {name} | ⬜ | — | — |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=CFG["pdf"])
    ap.add_argument("--write", action="store_true",
                    help="0_Contents.md 의 목차 구간을 실제로 갱신한다")
    ap.add_argument("--dump", action="store_true",
                    help="가공 없이 북마크 원본을 출력한다 (구조 확인용)")
    args = ap.parse_args()

    if args.dump:
        doc = fitz.open(args.pdf)
        for lvl, title, pg in doc.get_toc():
            print(f"{'  ' * (lvl - 1)}L{lvl} PDF{pg:4d} "
                  f"책{kit_config.pdf_to_book(pg, CFG):4d}  {clean(title)}")
        doc.close()
        return

    rows = entries(args.pdf)
    body, progress = render(rows)
    n_ch = sum(1 for r in rows if r[0] in ("chapter", "prelude", "epilogue"))
    n_sec = sum(1 for r in rows if r[0] == "section")

    if not args.write:
        print(body)
        print(f"\n<!-- 장 {n_ch}개 · 절 {n_sec}개 -->", file=sys.stderr)
        print("실제로 쓰려면 --write 를 붙이고, 그 뒤 check_toc.py 로 대조하라.",
              file=sys.stderr)
        return

    path = os.path.join(CFG["kit"], "0_Contents.md")
    marker_a = "<!-- AUTO-TOC:START -->"
    marker_b = "<!-- AUTO-TOC:END -->"
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    block = f"{marker_a}\n{body}{marker_b}\n"

    if marker_a in old and marker_b in old:
        new = re.sub(re.escape(marker_a) + r".*?" + re.escape(marker_b),
                     block.rstrip("\n"), old, flags=re.S)
    else:
        new = (old.rstrip("\n") + "\n\n" if old else "") + block
    open(path, "w", encoding="utf-8").write(new)
    print(f"{path} 갱신 — 장 {n_ch}개 · 절 {n_sec}개")
    print("\n[진행 상황 표에 붙여 넣을 것]\n")
    print(render_progress(progress))
    print("이제 반드시 대조하라:  python3 _study_kit/tools/check_toc.py")


if __name__ == "__main__":
    main()
