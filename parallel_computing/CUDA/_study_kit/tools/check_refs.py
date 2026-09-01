#!/usr/bin/env python3
"""챕터 노트의 상호참조를 원본 PDF·목차와 대조한다.

사용법
------
  python3 tools/check_refs.py                 # 전체 노트 검사
  python3 tools/check_refs.py 06 07           # 특정 노트만 (파일명 일부로 필터)

검사 항목
---------
  A) Figure/Table 참조  — PDF에 그 캡션이 실제로 존재하는가
  B) 책 페이지 참조     — 책의 페이지 범위 안인가
  C) 절 번호 참조       — 0_Contents.md 에 있는 절인가
                          (9장 이후는 학습 범위 밖이므로 '참고'로만 표시)

캡션 수집이 까다로운 이유
-------------------------
캡션 라벨이 항상 한 덩어리로 있지 않다. PyMuPDF가 텍스트를 쪼개는 방식 때문에
  ① 한 줄 안의 여러 span 으로 나뉘거나
  ② 같은 높이인데 별도 line 으로 나뉜다 (책 Table 3.2 가 이 경우: 'Table' / '3.2')
그래서 같은 y 에 놓인 볼드 조각을 x 순으로 이어붙여 라벨을 복원한다.
extract_figures.py 의 find_captions() 와 같은 방식이다.

주의 — 번호 건너뜀
------------------
책에 따라 **존재하지 않는 그림 번호**가 있다 (저자가 번호를 건너뛴 경우).
[없는 그림/표]로 보고되면 먼저 PDF 전문을 검색해 실제로 없는 번호인지 확인하고,
없는 것이 맞으면 kit.conf 옆에 메모해 두라. 참조하지 않는 한 문제가 아니다.
"""
import argparse
import glob
import os
import re
import sys

try:
    import fitz
except ImportError:
    sys.exit("PyMuPDF가 필요하다:  sudo apt install -y python3-fitz")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_config

CFG = kit_config.load()
ROOT = CFG["root"]                                 # ref/ · part*/ 가 있는 곳
KIT = CFG["kit"]                                   # 0_Contents.md · tools/ 가 있는 곳
PDF = CFG["pdf"]
BOOK_PAGE_MIN, BOOK_PAGE_MAX = CFG["book_pages"]   # 책에 인쇄된 쪽번호의 유효 범위
STUDY_MAX_CH = CFG["last_chapter"]                 # 학습 범위의 마지막 장
CAPTION_STYLE = CFG["caption_style"]               # "chapter"(Figure 6.3) | "flat"(Figure 3)
CAPTION_BOLD = CFG["caption_bold"]


def real_captions():
    """PDF 전체에서 캡션 라벨을 수집. kit.conf 의 caption_style·caption_bold 를 따른다."""
    doc = fitz.open(PDF)
    found = set()

    if CAPTION_BOLD:
        label_re = (re.compile(r"^(Figure|Table)\s*(\d+)\s*[:.]?$", re.I)
                    if CAPTION_STYLE == "flat"
                    else re.compile(r"^(Figure|Table)\s*(\d+|[A-Z])\.(\d+)$", re.I))
        for pno in range(doc.page_count):
            frags = []
            for blk in doc[pno].get_text("dict")["blocks"]:
                if blk.get("type") != 0:
                    continue
                for line in blk["lines"]:
                    head = ""
                    for sp in line["spans"]:
                        # 공백만 있는 span 은 폰트를 따지지 않고 통과시킨다.
                        # 이 책은 "FIGURE" 와 "6.6" 사이의 공백만 Helvetica(비볼드)로
                        # 조판해서, 여기서 끊으면 라벨이 "FIGURE" 로 잘린다.
                        if not sp["text"].strip():
                            head += sp["text"]
                            continue
                        if "Bold" not in sp["font"]:
                            break
                        head += sp["text"]
                    head = head.strip()
                    if head:
                        frags.append((round(line["bbox"][1], 1), line["bbox"][0], head))
            for y in set(f[0] for f in frags):
                row = sorted((f for f in frags if abs(f[0] - y) < 2.0), key=lambda f: f[1])
                for cand in (" ".join(t for _, _, t in row),
                             " ".join(t for _, _, t in row[:2])):
                    m = label_re.match(cand.strip())
                    if m:
                        found.add(_label(m))
                        break
    else:
        # 볼드가 아닌 책 — "라벨 + 구분자 + 설명" 형태의 줄로 판정
        line_re = re.compile(r"^(Figure|Table)\s*(\d+|[A-Z])(?:\.(\d+))?\s*[:.]\s+\S", re.I)
        for pno in range(doc.page_count):
            for blk in doc[pno].get_text("dict")["blocks"]:
                if blk.get("type") != 0:
                    continue
                for line in blk["lines"]:
                    txt = "".join(sp["text"] for sp in line["spans"]).strip()
                    m = line_re.match(txt)
                    if not m:
                        continue
                    if CAPTION_STYLE == "chapter" and m.group(3):
                        found.add("%s %s.%s" % (_kind(m), m.group(2), m.group(3)))
                    elif CAPTION_STYLE == "flat" and not m.group(3):
                        found.add("%s %s" % (_kind(m), m.group(2)))
    doc.close()
    return found


def _kind(m):
    """책의 조판 표기(FIGURE/Figure)에 상관없이 'Figure'/'Table' 로 통일한다.
    노트에는 늘 'Figure 6.6' 표기로 쓰고, 이 함수가 PDF 쪽 표기를 거기에 맞춘다."""
    return m.group(1).capitalize()


def _label(m):
    if CAPTION_STYLE == "flat":
        return "%s %s" % (_kind(m), m.group(2))
    return "%s %s.%s" % (_kind(m), m.group(2), m.group(3))


def toc_sections():
    """0_Contents.md 에서 절 번호를 수집."""
    txt = open(os.path.join(KIT, "0_Contents.md"), encoding="utf-8").read()
    secs = set(re.findall(r"^\s*-?\s*((?:\d+|[A-Z])\.\d+(?:\.\d+)?)\s", txt, re.M))
    secs |= set(re.findall(r"###\s*(\d+)장", txt))
    secs |= set(re.findall(r"###\s*부록\s*([A-Z])", txt))          # 부록은 'A' 로 등록
    return secs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("only", nargs="*", help="검사할 노트 (파일명 일부, 예: 06 07)")
    args = ap.parse_args()

    caps = real_captions()
    secs = toc_sections()
    print(f"PDF 캡션 {len(caps)}개 · 목차 절 {len(secs)}개 수집\n")

    ref_fig = (re.compile(r"\b(Figure|Table)\s+(\d+)(?!\.\d)") if CAPTION_STYLE == "flat"
               else re.compile(r"\b(Figure|Table)\s+((?:\d+|[A-Z])\.\d+)"))
    ref_pg = re.compile(r"책 p\.(\d+)")
    ref_sec = re.compile(r"((?:\d+|[A-Z])\.\d+(?:\.\d+)?)\s*절")

    problems = info = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "part*", "*", "*.md"))):
        name = os.path.basename(path).replace(".md", "")
        if args.only and not any(o in name for o in args.only):
            continue
        txt = open(path, encoding="utf-8").read()
        bad, notes = [], []

        for kind, num in set(ref_fig.findall(txt)):
            label = f"{kind} {num}"
            cnt = len(re.findall(re.escape(label) + r"\b", txt))
            if cnt and label not in caps:
                bad.append(f"[없는 그림/표] {label} ({cnt}회)")

        for pg in sorted(set(int(p) for p in ref_pg.findall(txt))):
            if not (BOOK_PAGE_MIN <= pg <= BOOK_PAGE_MAX):
                bad.append(f"[페이지 범위 밖] 책 p.{pg}")

        # 이미지 참조 — 파일이 실제로 있는가, 그리고 markdown 이 깨지지 않는가
        for line in txt.splitlines():
            if not line.lstrip().startswith("!["):
                continue
            m = re.match(r"!\[(.*?)\]\((\S+?)\)\s*$", line.strip())
            if not m:
                # alt 텍스트에 대괄호가 있으면 markdown 이 이미지로 인식하지 못하고
                # 원문이 그대로 출력된다. 빌드는 성공하므로 조용히 그림 하나가 사라진다.
                bad.append(f"[이미지 문법 깨짐] {line.strip()[:70]}")
                continue
            alt, rel = m.group(1), m.group(2)
            if "[" in alt or "]" in alt:
                bad.append(f"[alt 에 대괄호] {alt[:60]}")
            img = os.path.join(os.path.dirname(path), rel)
            if not os.path.exists(img):
                bad.append(f"[없는 이미지 파일] {rel}")

        for s in sorted(set(ref_sec.findall(txt))):
            if s in secs:
                continue
            head = s.split(".")[0]
            ch = int(head) if head.isdigit() else 0     # 부록은 학습 범위 검사 대상이 아니다
            cnt = len(re.findall(re.escape(s) + r"\s*절", txt))
            if ch > STUDY_MAX_CH:
                notes.append(f"[학습 범위 밖 참조] {s}절 ({cnt}회)")
            else:
                bad.append(f"[목차에 없는 절] {s}절 ({cnt}회)")

        problems += len(bad)
        info += len(notes)
        status = "이상 없음" if not bad else f"문제 {len(bad)}건"
        print(f"=== {name}  {status}")
        for b in bad:
            print(f"    {b}")
        for n in notes:
            print(f"    · {n}")

    print(f"\n문제 {problems}건 · 참고 {info}건")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
