#!/usr/bin/env python3
"""원문의 색 강조 구간을 쪽 단위로 뽑는다.

이 스터디(VINS-Mono)의 원문은 색을 세 가지로 쓴다.

  #197fb2 (파랑)  산문 강조 — 고딕/산세리프 볼드 폰트. ==강조== 로 옮긴다
  #ff0000 (빨강)  수식 내부 강조 — CM 계열 수학 폰트. \\color{#ff0000}{...} 로 옮긴다
  #0000ff (파랑)  수식 내부 강조 — 위와 짝을 이룬다. \\color{#0000ff}{...}

색 구간을 눈으로 찾으면 반드시 샌다. 전사할 때 이 스크립트의 출력을
수식 옆에 놓고 하나씩 대조한다. 색 목록은 파일 위쪽 NAME 에 모아 두었으므로
다른 문서를 다룰 때는 거기만 고치면 된다.

사용법
  python3 _study_kit/tools/dump_colored.py                 # 전체
  python3 _study_kit/tools/dump_colored.py -p 7-9          # 쪽 지정
  python3 _study_kit/tools/dump_colored.py -p 7 -c math    # prose|math|blue|m-red|m-blue|all
  python3 _study_kit/tools/dump_colored.py --count         # 개수만 (검증용)

--count 의 숫자는 노트를 다 쓴 뒤 ==강조== 개수 · \\color 개수와 맞춰 본다.
"""
import argparse
import re
import sys

import fitz

import kit_config

# 스터디마다 원문이 쓰는 색이 다르다. 여기에만 적어 두면 나머지는 따라간다.
#   VINS-Mono 는 세 가지를 쓴다 — 산문 강조 하나, 수식 안 강조 둘.
BLUE = 0x197FB2      # 산문 강조 (nanum/SFBX 폰트)
MRED = 0xFF0000      # 수식 안 강조 (CM 계열 수학 폰트)
MBLUE = 0x0000FF     # 수식 안 강조
NAME = {BLUE: "blue", MRED: "m-red", MBLUE: "m-blue"}
ALL = tuple(NAME)
GROUP = {"prose": (BLUE,), "math": (MRED, MBLUE)}


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in out if 1 <= p <= n]


def runs(page, wanted):
    """연속한 같은 색 span 을 한 구간으로 묶는다.

    줄이 바뀌어도 색이 이어지면 같은 구간으로 본다. 원문에서 강조가
    줄바꿈을 넘어가는 경우가 흔하기 때문이다. 다만 줄이 바뀐 자리는
    ` / ` 로 표시해 두어 전사할 때 알아볼 수 있게 한다.
    """
    out = []
    cur = None
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            first = True
            for s in line["spans"]:
                c = s["color"]
                if c in wanted:
                    if cur and cur["color"] == c:
                        # 줄이 바뀐 자리에만 ` / ` 를 넣는다. 같은 줄 안의 span 경계는
                        # 한글 글리프마다 쪼개져 있어 표시하면 읽을 수가 없다.
                        cur["text"] += (" / " if first else "") + s["text"]
                        cur["fonts"].add(s["font"].split("+")[-1])
                        cur["y1"] = s["bbox"][3]
                    else:
                        if cur:
                            out.append(cur)
                        cur = {
                            "color": c,
                            "text": s["text"],
                            "fonts": {s["font"].split("+")[-1]},
                            "y0": s["bbox"][1],
                            "y1": s["bbox"][3],
                        }
                    first = False
                else:
                    if cur:
                        out.append(cur)
                        cur = None
    if cur:
        out.append(cur)
    return out


def eq_marks(page):
    """그 쪽에 있는 수식 번호와 y 좌표. 색 구간이 몇 번 식 근처인지 알려 준다."""
    marks = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            t = "".join(s["text"] for s in line["spans"]).strip()
            m = re.fullmatch(r"\((\d{1,3})\)", t)
            if m:
                marks.append((line["bbox"][1], int(m.group(1))))
    return sorted(marks)


def nearest_eq(marks, y):
    """y 위치보다 아래에 처음 나오는 수식 번호 — 그 식에 속한 색일 가능성이 높다."""
    for my, n in marks:
        if my >= y - 6:
            return n
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pages", help="예: 7 · 7-9 · 7,10,15")
    ap.add_argument("-c", "--color", default="all",
                    choices=["all", "prose", "math", "blue", "m-red", "m-blue"])
    ap.add_argument("--count", action="store_true", help="개수만 출력")
    ap.add_argument("--min-chars", type=int, default=0, help="이 글자수 미만 구간은 숨김")
    args = ap.parse_args()

    cfg = kit_config.load()
    doc = fitz.open(cfg["pdf"])
    if args.color == "all":
        wanted = set(ALL)
    elif args.color in GROUP:
        wanted = set(GROUP[args.color])
    else:
        wanted = {c for c, n in NAME.items() if n == args.color}
    pages = parse_pages(args.pages, doc.page_count)

    total = {c: 0 for c in ALL}
    chars = {c: 0 for c in ALL}
    for pno in pages:
        page = doc[pno - 1]
        marks = eq_marks(page)
        rs = [r for r in runs(page, wanted) if r["text"].strip()]
        shown = [r for r in rs if len(r["text"].strip()) >= args.min_chars]
        for r in rs:
            total[r["color"]] += 1
            chars[r["color"]] += len(r["text"].strip())
        if args.count or not shown:
            continue
        print(f"\n══ p{pno} ══ ({len(shown)}구간)")
        for i, r in enumerate(shown, 1):
            eq = nearest_eq(marks, r["y0"])
            tag = f"({eq})" if eq else "  — "
            print(f"  {i:3d}. [{NAME[r['color']]:6s}] {tag:>6s}  {r['text'].strip()}")

    print("\n── 합계 ──")
    for c in ALL:
        if c in wanted:
            print(f"  {NAME[c]:6s} #{c:06x}  {total[c]:4d}구간  {chars[c]:5d}자")
    return 0


if __name__ == "__main__":
    sys.exit(main())
