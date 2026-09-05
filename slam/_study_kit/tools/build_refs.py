#!/usr/bin/env python3
"""책 뒤의 References 를 `번호 → 서지정보` 표로 뽑는다.

사용법:
    python3 _study_kit/tools/build_refs.py --book-pages 551-644          # 미리보기
    python3 _study_kit/tools/build_refs.py --book-pages 551-644 --write  # refs.json 저장
    python3 _study_kit/tools/build_refs.py --show 568 1212               # 몇 개만 조회

왜 필요한가
-----------
서베이 성격의 장은 **인용 자체가 본문**이다. SLAM Handbook 은 참고문헌이 1,359편이고
본문 인용 표시가 3,265회 나온다. 노트에 `[568]` 이라고만 적어 두면 나중에 그 노트를
다시 읽을 때 아무 의미가 없다.

이 도구가 `refs.json` 을 만들어 두면 `build_html.py` 가 본문의 `[568]` 을 읽어
저자·연도·제목을 붙여 준다. 노트를 쓸 때는 원문 그대로 번호만 적으면 된다.

무엇을 하는가
-------------
References 구간에서 `[N]` 으로 시작하는 항목을 모아 한 줄로 잇고, 아래로 쪼갠다.

    raw     항목 전문 (그대로 보존)
    authors 연도 앞까지
    year    "2023a" 처럼 붙는 글자까지 포함
    title   연도 뒤 첫 문장
    short   "Abate et al. 2023a" — 본문에 인라인으로 붙일 짧은 형태

줄 끝 하이픈은 이어 붙인다 ("Alt-\\nman" → "Altman"). 텍스트 레이어가 흘리는
합자도 편다 (3_Pitfalls.md A13).
"""

import argparse
import json
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
OUT_PATH = os.path.join(CFG["kit"], "refs.json")

ITEM = re.compile(r"^\[(\d{1,4})\]\s*(.*)$")
# 연도 — 항목 안에서 저자와 제목을 가르는 지점. 여기가 어긋나면 저자 자리가
# 항목 전체를 삼켜 카드에 엉뚱한 내용이 뜬다. 실제로 관측된 변형을 모두 받는다.
#   "2023."  "2023a."  "2023b,"
#   "2005b (Aug)."          연도 뒤 월 (54건)
#   "2022 (3)."             호(issue) 번호
#   "2015 (July 13–17,)."   날짜 범위
#   "1856."                 19세기 이전 — 측량학 고전이 인용된다
YEAR = re.compile(r"\b((?:1[89]|20)\d{2}[a-z]?)\s*(?:\([^)]{0,24}\))?\s*[.,]\s+")

LIGATURES = {"\x1b": "ff", "ﬀ": "ff", "ﬁ": "fi",
             "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"}


def unligature(s):
    for bad, good in LIGATURES.items():
        s = s.replace(bad, good)
    return s


def join_wrapped(lines):
    """줄 목록을 한 문단으로 잇는다. 줄 끝 하이픈은 없애고 붙인다."""
    buf = ""
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if buf.endswith("-"):
            buf = buf[:-1] + ln          # 하이픈 분철 복원
        elif buf:
            buf += " " + ln
        else:
            buf = ln
    return re.sub(r"\s+", " ", buf).strip()


def collect(pdf_path, pdf_lo, pdf_hi):
    """References 구간에서 번호 → 줄 목록을 모은다."""
    doc = fitz.open(pdf_path)
    items, cur_num, cur_lines = {}, None, []
    for pno in range(pdf_lo, pdf_hi + 1):
        page = doc[pno - 1]
        rows = []
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                # 머리글("644 References")은 본문에 섞이면 항목 한가운데로 들어간다.
                # 문자열로는 못 거른다 — 세로 위치로 잘라 낸다.
                if ln["bbox"][1] < CFG["header_y"]:
                    continue
                txt = unligature("".join(s["text"] for s in ln["spans"])).strip()
                if txt:
                    rows.append((round(ln["bbox"][1], 1), ln["bbox"][0], txt))
        # 같은 높이에 조각난 span 을 x 순으로 이어 한 줄로 만든다
        merged = {}
        for y, x, txt in rows:
            key = next((k for k in merged if abs(k - y) < 2.0), y)
            merged.setdefault(key, []).append((x, txt))
        for y in sorted(merged):
            line = " ".join(t for _, t in sorted(merged[y]))
            if line.strip() in ("References",) or re.fullmatch(r"\d{1,4}", line.strip()):
                continue                                   # 표제·머리글 쪽번호
            m = ITEM.match(line)
            if m:
                if cur_num is not None:
                    items[cur_num] = cur_lines
                cur_num, cur_lines = int(m.group(1)), [m.group(2)]
            elif cur_num is not None:
                cur_lines.append(line)
    if cur_num is not None:
        items[cur_num] = cur_lines
    doc.close()
    return items


def parse(raw):
    """항목 전문에서 authors / year / title / short 를 뽑는다."""
    m = YEAR.search(raw)
    if not m:
        return {"raw": raw, "authors": "", "year": "", "title": raw, "short": raw[:48]}
    authors = raw[:m.start()].rstrip(" .,")
    year = m.group(1)
    rest = raw[m.end():]
    # 제목 = 연도 뒤 첫 문장. 약어의 마침표에 걸리지 않도록 '. ' + 대문자/끝 으로 자른다.
    tm = re.search(r"\.(?:\s+|$)", rest)
    title = (rest[:tm.start()] if tm else rest).strip().rstrip(".")

    # short — 첫 저자의 성. "A, Zeng" 처럼 뒤집힌 표기도 있어 첫 조각을 그대로 쓴다.
    first = authors.split(",")[0].strip()
    first = re.sub(r"\s+[A-Z]\.$", "", first)          # "Abate M." → "Abate"
    n_auth = authors.count(",") + (1 if authors else 0)
    short = f"{first} et al. {year}" if n_auth > 2 else f"{first} {year}".strip()
    return {"raw": raw, "authors": authors, "year": year,
            "title": title, "short": short}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", default=CFG["pdf"])
    ap.add_argument("--book-pages", help="References 의 책 쪽 범위 (예: 551-644)")
    ap.add_argument("--pages", help="PDF 쪽 범위로 직접 지정")
    ap.add_argument("--write", action="store_true", help="refs.json 으로 저장")
    ap.add_argument("--show", nargs="+", type=int, help="저장된 refs.json 에서 조회")
    args = ap.parse_args()

    if args.show:
        if not os.path.exists(OUT_PATH):
            raise SystemExit(f"{OUT_PATH} 가 없다. 먼저 --write 로 만들어라.")
        data = json.load(open(OUT_PATH, encoding="utf-8"))
        for n in args.show:
            e = data["refs"].get(str(n))
            print(f"[{n}] " + (f"{e['short']}\n      {e['title']}" if e else "없음"))
        return

    if args.book_pages:
        lo, hi = (int(x) for x in args.book_pages.split("-"))
        pdf_lo, pdf_hi = kit_config.book_range_to_pdf(lo, hi, CFG)
        print(f"책 {lo}-{hi} 쪽  →  PDF {pdf_lo}-{pdf_hi} 쪽")
    elif args.pages:
        pdf_lo, pdf_hi = (int(x) for x in args.pages.split("-"))
    else:
        ap.error("--book-pages 나 --pages 중 하나가 필요하다")

    items = collect(args.pdf, pdf_lo, pdf_hi)
    refs = {str(n): parse(join_wrapped(lines)) for n, lines in sorted(items.items())}

    nums = sorted(int(k) for k in refs)
    gaps = [n for n in range(1, max(nums) + 1) if n not in set(nums)] if nums else []
    print(f"항목 {len(refs)}개  (번호 {min(nums)}–{max(nums)})" if nums else "항목 없음")
    if gaps:
        print(f"⚠ 빠진 번호 {len(gaps)}개: {gaps[:20]}{' …' if len(gaps) > 20 else ''}")

    if not args.write:
        for n in nums[:3] + nums[-2:]:
            e = refs[str(n)]
            print(f"\n[{n}] short={e['short']!r}\n     year={e['year']!r}"
                  f"\n     title={e['title'][:78]!r}")
        print("\n실제로 쓰려면 --write 를 붙여라.")
        return

    json.dump({"count": len(refs), "refs": refs},
              open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{OUT_PATH} 저장 — {len(refs)}개")


if __name__ == "__main__":
    main()
