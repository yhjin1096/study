#!/usr/bin/env python3
"""책 PDF에서 챕터의 Figure/Table 영역을 찾아 PNG로 크롭 추출한다.

사용법
------
  # 그 챕터에 어떤 그림/표가 있는지 먼저 훑어보기
  python3 tools/extract_figures.py --chapter 6 --pages 170-207 --list

  # 실제 추출 (기본 이름: fig6_1.png, table6_2.png ...)
  python3 tools/extract_figures.py --chapter 6 --pages 170-207 --out <챕터>/images

  # 설명이 붙은 파일명으로 추출 (권장)
  python3 tools/extract_figures.py --chapter 6 --pages 170-207 \
      --out <챕터>/images --names tools/figure_names/ch6.txt

  # 한 개만 다시 뽑기
  python3 tools/extract_figures.py --chapter 6 --pages 170-207 \
      --out <챕터>/images --only "Figure 6.9"

설정
----
PDF 경로와 레이아웃 상수는 스터디 루트의 `kit.conf` 에서 읽는다 (없으면 ref/ 자동 탐색).
자세한 항목은 tools/kit_config.py 의 docstring 참조.

페이지 번호
-----------
`--pages` 는 **PDF 페이지 번호**다. 책에 인쇄된 쪽번호와 다르므로 반드시 오프셋을 확인하라.
  PDF 페이지 = 책 페이지 + page_offset      (kit.conf 에 기록)

--names 파일 형식
-----------------
  Figure 6.1 = fig6_1_sonar_scan
  Table 6.2  = table6_2_learn_parameters
빈 줄과 '#' 주석은 무시한다. 목록에 없는 캡션은 기본 이름을 쓴다.

동작 방식
---------
PDF에 따라 **일부 페이지가 통짜 스캔 이미지**일 수 있어, 페이지 안 객체 bbox
(get_image_info / get_drawings)를 그림 영역으로 신뢰할 수 없다. 그래서:

  1. 캡션("Figure N.M" / "Table N.M")의 y 좌표를 찾아 **아래 경계**로 삼고,
  2. 그 위쪽에서 머리글 / 앞선 캡션 / 본문 문단의 끝을 찾아 **위 경계**로 삼은 뒤,
  3. 그 구간을 넉넉히 렌더링하고 **픽셀 단위로 흰 여백을 트림**해 실제 경계를 얻는다.

캡션과 본문은 여러 줄에 걸치고 마지막 줄이 짧아 폭 판정에 걸리지 않으므로,
시작 줄을 찾으면 줄 간격이 이어지는 동안 블록 끝까지 확장한다.
"""
import argparse
import os
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF가 필요하다:  sudo apt install -y python3-fitz")

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_config

CFG = kit_config.load()
DEFAULT_PDF = CFG["pdf"]

ZOOM = 3.0                        # 216 dpi
# 아래 네 값은 책 판형에 따라 다르다. 맞추는 법은 3_Pitfalls.md "레이아웃 상수 맞추기" 참조.
HEADER_Y = CFG["header_y"]        # 페이지 머리글 아래 (pt)
CLIP_X0, CLIP_X1 = CFG["clip_x"]  # 본문 컬럼의 좌우 경계 (pt)
BODY_X0, BODY_X1 = CFG["body_x"]  # 이 폭을 모두 덮는 줄은 본문 문단으로 판정 (pt)
CAPTION_STYLE = CFG["caption_style"]   # "chapter"(Figure 6.3) | "flat"(Figure 3)
CAPTION_BOLD = CFG["caption_bold"]     # 캡션 라벨이 볼드체인가
BLOCK_GAP = 6.0                   # 이 이하로 붙어 있으면 같은 텍스트 블록
MIN_REGION_H = 20.0               # 이보다 얇으면 영역 판정 실패로 본다
PSEUDOCODE_RE = re.compile(r"^\d+:")   # 알고리즘 표의 라인 번호 ("1: Algorithm …")
WHITE = 246                       # 이 값 이상의 밝기는 여백
PAD_PX = 8                        # 트림 후 남길 여백(픽셀)


def text_lines(page):
    """페이지의 텍스트 줄을 (bbox, text) 목록으로."""
    out = []
    for blk in page.get_text("dict")["blocks"]:
        if blk.get("type") != 0:
            continue
        for line in blk["lines"]:
            txt = "".join(s["text"] for s in line["spans"]).strip()
            if txt:
                out.append((line["bbox"], txt))
    return out


def caption_regex(chapter):
    """캡션 라벨 정규식. kit.conf 의 caption_style 에 따라 두 형식을 지원한다.

      chapter 스타일 : "Figure 6.3"  (장 번호 + 일련번호)   — 단행본에 흔하다
      flat    스타일 : "Figure 3:"   (문서 전체 연속 번호)  — LaTeX article 에 흔하다
    """
    if CAPTION_STYLE == "flat":
        return re.compile(r"^(Figure|Table)\s*(\d+)\s*[:.]?$", re.I)
    part = re.escape(str(chapter)) if chapter else r"\d+|[A-Z]"
    return re.compile(r"^(Figure|Table)\s*(%s)\.(\d+)$" % part, re.I)


def find_captions(page, chapter):
    """이 페이지의 캡션을 (라벨, y0) 목록으로.

    본문 중 언급("Figure 6.2 shows a typical example")과 구분해야 한다.
    캡션 라벨이 볼드로 조판되는 책이 많아 기본은 볼드만 본다(caption_bold = yes).
    LaTeX article 처럼 볼드가 아닌 책은 kit.conf 에서 caption_bold = no 로 두면
    "라벨 뒤에 콜론이나 설명이 이어지는가"로 대신 판정한다.

    라벨이 조각나는 경우가 두 가지 있다:
      ① 한 줄 안의 여러 span   ② 같은 높이인데 별도 line
    그래서 같은 y 에 놓인 조각을 x 순으로 이어붙여 라벨을 복원한다.
    """
    label_re = caption_regex(chapter)
    hits = {}

    if CAPTION_BOLD:
        frags = []
        for blk in page.get_text("dict")["blocks"]:
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
        for y in sorted(set(f[0] for f in frags)):
            row = sorted((f for f in frags if abs(f[0] - y) < 2.0), key=lambda f: f[1])
            for cand in (" ".join(t for _, _, t in row),
                         " ".join(t for _, _, t in row[:2])):
                m = label_re.match(cand.strip())
                if m:
                    hits.setdefault(_label_of(m), y)
                    break
        return sorted(hits.items(), key=lambda kv: kv[1])

    # 볼드가 아닌 책 — 줄 전체를 보고 "라벨 + 구분자 + 설명" 형태인지로 판정한다
    line_re = re.compile(r"^(Figure|Table)\s*(\d+)(?:\.(\d+))?\s*[:.]\s+\S", re.I)
    for (x0, y0, x1, y1), txt in text_lines(page):
        m = line_re.match(txt)
        if not m:
            continue
        if CAPTION_STYLE == "chapter":
            if not m.group(3) or (chapter and m.group(2) != str(chapter)):
                continue
            label = "%s %s.%s" % (_kind(m), m.group(2), m.group(3))
        else:
            if m.group(3):                      # flat 인데 점 번호면 다른 규약이다
                continue
            label = "%s %s" % (_kind(m), m.group(2))
        hits.setdefault(label, y0)
    return sorted(hits.items(), key=lambda kv: kv[1])


def _kind(m):
    """책의 조판 표기(FIGURE/Figure/figure)에 상관없이 'Figure'/'Table' 로 통일한다.

    이 책(PMPP 5e)은 캡션을 'FIGURE 6.6' 처럼 전부 대문자로 조판한다.
    파일명과 노트의 참조 표기가 흔들리지 않도록 여기서 한 번에 정규화한다.
    """
    return m.group(1).capitalize()


def _label_of(m):
    if CAPTION_STYLE == "flat":
        return "%s %s" % (_kind(m), m.group(2))
    return "%s %s.%s" % (_kind(m), m.group(2), m.group(3))


def region_floor(lines, label, cap_y0, caption_re):
    """그림 영역의 위쪽 경계: 머리글 / 앞선 캡션 / 본문 문단 중 가장 아래."""
    above = sorted((l for l in lines if l[0][3] <= cap_y0 - 1.0), key=lambda l: l[0][1])
    floor = HEADER_Y
    for i, ((x0, y0, x1, y1), txt) in enumerate(above):
        if PSEUDOCODE_RE.match(txt):
            continue            # 알고리즘 의사코드 줄("1: Algorithm …")은 본문이 아니라 표의 일부다
        is_prev_caption = caption_re.match(txt) and not txt.upper().startswith(label.upper())
        is_body_line = x0 <= BODY_X0 and x1 >= BODY_X1
        if not (is_prev_caption or is_body_line):
            continue
        end = y1
        for (nx0, ny0, nx1, ny1), _ in above[i + 1:]:   # 블록 끝까지 확장
            if ny0 - end > BLOCK_GAP:
                break
            end = max(end, ny1)
        floor = max(floor, end)
    return floor


def trim(img):
    """흰 여백을 제외한 bbox(px). 내용이 없으면 None."""
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    rows = [y for y in range(h) if any(px[x, y] < WHITE for x in range(0, w, 2))]
    cols = [x for x in range(w) if any(px[x, y] < WHITE for y in range(0, h, 2))]
    if not rows or not cols:
        return None
    return (max(cols[0] - PAD_PX, 0), max(rows[0] - PAD_PX, 0),
            min(cols[-1] + PAD_PX, w), min(rows[-1] + PAD_PX, h))


def default_name(label):
    """'Figure 6.1' -> 'fig6_1',  'Table 6.2' -> 'table6_2',  'Figure 3' -> 'fig3'"""
    kind, num = label.split()
    return ("fig" if kind == "Figure" else "table") + num.replace(".", "_")


def load_names(path):
    names = {}
    if not path:
        return names
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            names[k.strip()] = v.strip()
    return names


def extract(page, label, cap_y0, chapter, out_path):
    # "앞선 캡션"을 알아보기 위한 느슨한 정규식 (스타일 무관)
    caption_re = re.compile(r"^(Figure|Table)\s*\d+", re.I)
    lines = text_lines(page)
    floor = region_floor(lines, label, cap_y0, caption_re)

    clip = fitz.Rect(CLIP_X0, floor + 1.0, CLIP_X1, cap_y0 - 2.0)
    if clip.height < MIN_REGION_H:
        # 위 경계 판정이 실패했다 — 머리글 아래 전체를 잡고 픽셀 트림에 맡긴다
        clip = fitz.Rect(CLIP_X0, HEADER_Y, CLIP_X1, cap_y0 - 2.0)
        if clip.height < MIN_REGION_H:
            return None, "영역이 너무 얇음 (h=%.1f)" % clip.height

    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    box = trim(img)
    if box is None:
        return None, "내용 없음"
    img = img.crop(box)
    img.save(out_path)
    return img, None


def main():
    ap = argparse.ArgumentParser(
        description="책 PDF에서 챕터의 Figure/Table을 크롭 추출한다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("--chapter",
                    help="챕터 번호 (예: 6). 부록은 글자로 준다 (예: A). "
                         "caption_style=chapter 일 때 필수, "
                         "flat 이면 생략한다 (그림 번호에 장 번호가 없으므로)")
    ap.add_argument("--pages",
                    help="PDF 페이지 범위 (예: 170-207). 책 쪽번호가 아니다 — kit.conf 의 page_offset 참조")
    ap.add_argument("--book-pages",
                    help="책에 인쇄된 쪽 범위 (예: 123-155). kit.conf 의 page_offset 으로 "
                         "PDF 쪽으로 환산한다. 오프셋이 구간마다 다른 책에서 특히 안전하다")
    ap.add_argument("--out", help="출력 디렉터리 (--list 가 아니면 필수)")
    ap.add_argument("--pdf", default=DEFAULT_PDF, help="원본 PDF 경로")
    ap.add_argument("--names", help="'Figure 6.1 = fig6_1_설명' 형식의 이름 매핑 파일")
    ap.add_argument("--only", action="append",
                    help="이 라벨만 처리 (예: --only 'Figure 6.9'). 여러 번 지정 가능")
    ap.add_argument("--list", action="store_true", help="추출하지 않고 발견된 캡션만 나열")
    ap.add_argument("--clip", metavar="X0,Y0,X1,Y1",
                    help="캡션 자동 탐지를 건너뛰고 이 영역을 직접 잘라낸다 (pt). "
                         "캡션이 없는 그림이나, 캡션이 그림 '위'에 오는 표에 쓴다. "
                         "--page 와 --name 이 함께 필요하다")
    ap.add_argument("--page", type=int, help="--clip 과 함께 쓰는 PDF 쪽번호")
    ap.add_argument("--name", help="--clip 과 함께 쓰는 출력 파일명 (확장자 없이)")
    args = ap.parse_args()

    if args.clip:
        if not (args.page and args.name and args.out):
            ap.error("--clip 에는 --page · --name · --out 이 모두 필요하다")
        try:
            x0, y0, x1, y1 = (float(v) for v in args.clip.split(","))
        except ValueError:
            ap.error("--clip 형식은 'X0,Y0,X1,Y1' 이어야 한다 (예: 163,132,342,268)")
        doc = fitz.open(args.pdf)
        os.makedirs(args.out, exist_ok=True)
        out_path = os.path.join(args.out, args.name + ".png")
        pix = doc[args.page - 1].get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM),
                                            clip=fitz.Rect(x0, y0, x1, y1))
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        box = trim(img)
        if box is None:
            sys.exit("그 영역에 내용이 없다: %s" % args.clip)
        img = img.crop(box)
        img.save(out_path)
        print("  PDF p%d  %s  %dx%dpx  -> %s"
              % (args.page, args.clip, img.size[0], img.size[1], args.name + ".png"))
        return 0

    if bool(args.pages) == bool(args.book_pages):
        ap.error("--pages 와 --book-pages 중 정확히 하나를 쓰라")
    if args.book_pages:
        m = re.match(r"^(\d+)-(\d+)$", args.book_pages)
        if not m:
            ap.error("--book-pages 형식은 'A-B' 여야 한다 (예: 123-155)")
        a, b = kit_config.book_range_to_pdf(int(m.group(1)), int(m.group(2)), CFG)
        print("책 %s-%s 쪽  →  PDF %d-%d 쪽" % (m.group(1), m.group(2), a, b))
        args.pages = "%d-%d" % (a, b)
    if not args.list and not args.out:
        ap.error("--out 이 필요하다 (또는 --list 를 쓰라)")
    if CAPTION_STYLE == "chapter" and args.chapter is None:
        ap.error("caption_style=chapter 이므로 --chapter 가 필요하다 "
                 "(장 번호 없는 'Figure 3' 형식이면 kit.conf 에서 caption_style = flat)")

    if args.chapter and not re.fullmatch(r"\d+|[A-Za-z]", args.chapter):
        ap.error("--chapter 는 숫자(6) 또는 부록 글자(A) 여야 한다: %r" % args.chapter)
    if args.chapter:
        args.chapter = args.chapter.upper() if args.chapter.isalpha() else args.chapter
    m = re.match(r"^(\d+)-(\d+)$", args.pages)
    if not m:
        ap.error("--pages 형식은 'A-B' 여야 한다 (예: 170-207)")
    first, last = int(m.group(1)), int(m.group(2))

    if not os.path.exists(args.pdf):
        sys.exit("PDF를 찾을 수 없다: %s" % args.pdf)

    names = load_names(args.names)
    doc = fitz.open(args.pdf)
    if last > doc.page_count:
        sys.exit("PDF는 %d페이지뿐이다 (--pages %d-%d 요청)" % (doc.page_count, first, last))

    if args.out:
        os.makedirs(args.out, exist_ok=True)

    found = failed = 0
    for pno in range(first, last + 1):
        page = doc[pno - 1]
        for label, cap_y0 in find_captions(page, args.chapter):
            if args.only and label not in args.only:
                continue
            found += 1
            name = names.get(label, default_name(label))
            if args.list:
                print("  %-12s p%-4d -> %s.png" % (label, pno, name))
                continue
            img, err = extract(page, label, cap_y0, args.chapter,
                               os.path.join(args.out, name + ".png"))
            if err:
                failed += 1
                print("  !! %-12s p%-4d  %s" % (label, pno, err))
            else:
                print("  %-12s p%-4d  %dx%dpx  -> %s.png"
                      % (label, pno, img.width, img.height, name))
    doc.close()

    if found == 0:
        print("캡션을 찾지 못했다. --pages 범위와 kit.conf 의 caption_style"
              f"(현재 {CAPTION_STYLE}) · caption_bold(현재 "
              f"{'yes' if CAPTION_BOLD else 'no'})를 확인하라. "
              "캡션 형식 조사법은 3_Pitfalls.md A8 참조.\n"
              "  · 'Figure 3: 설명' 처럼 장 번호가 없으면  caption_style = flat\n"
              "  · 캡션이 볼드가 아니면(LaTeX article 등)  caption_bold  = no\n"
              "(--pages 는 책 쪽번호가 아니라 PDF 페이지 번호다. "
              "kit.conf 의 page_offset 으로 환산하거나 --book-pages 를 쓰라.\n"
              " 현재 오프셋: %s)" % ", ".join(
                  "PDF %d-%d 은 +%d" % (lo, hi, off) for lo, hi, off in CFG["offsets"]))
    elif not args.list:
        print("총 %d개 중 %d개 추출%s" % (found, found - failed,
                                          (", %d개 실패" % failed) if failed else ""))
        print("※ 캡션이 없는 그림(예: 연습문제 삽화)은 이 스크립트로 잡히지 않는다 — 직접 clip 지정 필요")


if __name__ == "__main__":
    main()
