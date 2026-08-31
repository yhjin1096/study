#!/usr/bin/env python3
"""스터디별 설정을 읽는다.

`kit.conf` 를 읽고, 없으면 합리적인 기본값을 쓴다.
`extract_figures.py` 와 `check_refs.py` 가 공유한다.

두 개의 루트
------------
킷은 스터디 루트에 그대로 펼쳐 놓아도 되고, 하위 폴더에 담아 두어도 된다.
그래서 위치를 두 가지로 나눠 본다.

    킷 루트   `tools/` 의 부모.  kit.conf · 0~3 문서 · tools 가 사는 곳
    스터디 루트   `ref/` 나 `part*/` 가 있는 곳.  원본 PDF와 챕터 노트가 사는 곳

    (가) 펼친 배치            (나) 담은 배치
    MyStudy/                  MyStudy/            ← 스터디 루트
    ├── kit.conf              ├── _study_kit/     ← 킷 루트
    ├── tools/                │   ├── kit.conf
    ├── ref/                  │   └── tools/
    └── part1_x/              ├── ref/
    두 루트가 같다            └── part1_x/

킷 루트에서 한 단계 위까지만 훑는다. 그 안에 `ref/` 나 `part*/` 가 없으면
두 루트를 같다고 본다 (킷만 단독으로 복사해 둔 상태).

kit.conf 형식 (key = value, '#' 이후는 주석):

    pdf          = ref/My Book.pdf   # 생략하면 ref/ 안의 .pdf 를 자동으로 찾는다
    page_offset  = 21                # PDF 페이지 = 책 페이지 + 이 값
    last_chapter = 8                 # 학습 범위의 마지막 장 (이후 참조는 '범위 밖'으로 표시)
    book_pages   = 1-647             # 책 페이지 번호의 유효 범위

    caption_style = chapter          # 캡션 번호 형식: chapter("Figure 6.3") | flat("Figure 3")
    caption_bold  = yes              # 캡션 라벨이 볼드체인가 (LaTeX article 은 보통 no)

    # 아래는 그림 추출 레이아웃 (책마다 다르다. 3_Pitfalls.md 의 "레이아웃 상수 맞추기" 참조)
    clip_x       = 155-522           # 본문 컬럼의 좌우 경계 (pt)
    header_y     = 52                # 페이지 머리글 아래 (pt)
    body_x       = 186-488           # 이 폭을 모두 덮는 줄은 본문 문단으로 판정 (pt)
    heading_size = 11.5              # 절 제목의 최소 글자 크기 (pt) — check_toc.py
    heading_gap  = 8                 # 제목 줄을 잇는 세로 간격 한계 (pt) — check_toc.py
"""
import glob
import os
import re

DEFAULTS = {
    "pdf": None,            # None 이면 ref/ 에서 자동 탐색
    "caption_style": "chapter",   # "chapter" = Figure 6.3 / "flat" = Figure 3
    "caption_bold": True,         # 캡션 라벨이 볼드체인가
    "page_offset": 0,      # 대표 오프셋 (구간이 여러 개면 첫 구간의 값)
    "offsets": None,       # [(pdf_lo, pdf_hi, offset), ...] — load() 가 채운다
    "last_chapter": 99,
    "book_pages": (1, 9999),
    "clip_x": (155.0, 522.0),
    "header_y": 52.0,
    "body_x": (186.0, 488.0),
    "heading_size": 11.5,  # check_toc.py — 이보다 큰 글자만 '절 제목'으로 본다
    "heading_gap": 8.0,    # check_toc.py — 이보다 벌어지면 다른 제목 덩어리
}


def kit_root(start=None):
    """킷 자산(kit.conf · 0~3 문서 · tools)이 있는 폴더 = `tools/` 의 부모."""
    if start:
        return os.path.abspath(start)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _is_study(d):
    return os.path.isdir(os.path.join(d, "ref")) or bool(glob.glob(os.path.join(d, "part*", "")))


def study_root(start=None):
    """원본 PDF와 챕터 노트가 있는 폴더. 킷 루트이거나 그 한 단계 위다."""
    kit = kit_root(start)
    if _is_study(kit):
        return kit
    parent = os.path.dirname(kit)
    if parent != kit and _is_study(parent):
        return parent
    return kit          # 아직 ref/ 도 노트도 없는 갓 복사한 킷


def _pair(value, cast=float):
    m = re.match(r"^\s*(-?[\d.]+)\s*-\s*(-?[\d.]+)\s*$", value)
    if not m:
        raise ValueError(f"'A-B' 형식이어야 한다: {value!r}")
    return (cast(m.group(1)), cast(m.group(2)))


def _offsets(value):
    """page_offset 값을 [(pdf_lo, pdf_hi, offset), ...] 로 파싱한다.

    두 가지 표기를 받는다.

        page_offset = 28                        책 전체가 한 오프셋
        page_offset = 28@29-209, 27@210-314     PDF 쪽 구간마다 다른 오프셋

    두 번째 표기가 필요한 이유: 판본에 따라 빈 쪽(장 사이의 blank verso)이
    PDF 에서 빠져 있으면 뒤로 갈수록 오프셋이 줄어든다. 하나의 스칼라로 적으면
    책 뒷부분의 쪽번호가 통째로 어긋난다. `3_Pitfalls.md` A2 참조.

    구간은 **PDF 쪽번호** 기준으로 적는다 (책 쪽번호가 아니라).
    """
    value = value.strip()
    if re.fullmatch(r"-?\d+", value):
        return [(1, 10 ** 9, int(value))]
    segs = []
    for part in value.split(","):
        m = re.fullmatch(r"\s*(-?\d+)\s*@\s*(\d+)\s*-\s*(\d+)\s*", part)
        if not m:
            raise SystemExit(
                "page_offset 형식이 잘못됐다: %r\n"
                "  스칼라       page_offset = 28\n"
                "  구간별       page_offset = 28@29-209, 27@210-314" % part)
        off, lo, hi = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if lo > hi:
            raise SystemExit(f"page_offset 구간의 시작이 끝보다 크다: {part!r}")
        segs.append((lo, hi, off))
    segs.sort()
    for (lo1, hi1, _), (lo2, _, _) in zip(segs, segs[1:]):
        if lo2 <= hi1:
            raise SystemExit(f"page_offset 구간이 겹친다: PDF {lo1}-{hi1} 와 {lo2}-")
    return segs


def pdf_to_book(pdf_page, cfg=None):
    """PDF 쪽번호 → 책에 인쇄된 쪽번호. 구간 밖이면 None."""
    for lo, hi, off in (cfg or load())["offsets"]:
        if lo <= pdf_page <= hi:
            return pdf_page - off
    return None


def book_to_pdf(book_page, cfg=None):
    """책에 인쇄된 쪽번호 → PDF 쪽번호. 그 쪽이 PDF 에 없으면 None."""
    for lo, hi, off in (cfg or load())["offsets"]:
        if lo - off <= book_page <= hi - off:
            return book_page + off
    return None


def book_range_to_pdf(first, last, cfg=None):
    """책 쪽 구간 → PDF 쪽 구간. 경계의 빈 쪽은 안쪽으로 좁혀 맞춘다."""
    cfg = cfg or load()
    a = next((book_to_pdf(b, cfg) for b in range(first, last + 1)
              if book_to_pdf(b, cfg)), None)
    b = next((book_to_pdf(x, cfg) for x in range(last, first - 1, -1)
              if book_to_pdf(x, cfg)), None)
    if a is None or b is None:
        raise SystemExit(f"책 {first}-{last} 쪽에 대응하는 PDF 쪽이 없다")
    return a, b


def load(root=None):
    """설정 dict 를 돌려준다.

    'root' = 스터디 루트 (ref/ · part*/ 가 있는 곳)
    'kit'  = 킷 루트 (kit.conf · 0~3 문서 · tools/ 가 있는 곳)
    두 배치 모두에서 맞게 잡힌다. 자세한 것은 이 파일 맨 위 docstring 참조.
    """
    kit = kit_root(root)
    root = root or study_root()
    cfg = dict(DEFAULTS)
    cfg["root"] = root
    cfg["kit"] = kit

    # kit.conf 는 킷 루트에 있는 것이 정석이지만, 스터디 루트에 둔 것도 받아 준다.
    path = os.path.join(kit, "kit.conf")
    if not os.path.exists(path):
        path = os.path.join(root, "kit.conf")
    if os.path.exists(path):
        for raw in open(path, encoding="utf-8"):
            line = raw.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            k, v = (s.strip() for s in line.split("=", 1))
            if k == "page_offset":
                cfg["offsets"] = _offsets(v)
                cfg["page_offset"] = cfg["offsets"][0][2]
            elif k == "last_chapter":
                cfg[k] = int(v)
            elif k in ("header_y", "heading_size", "heading_gap"):
                cfg[k] = float(v)
            elif k == "book_pages":
                cfg[k] = _pair(v, int)
            elif k in ("clip_x", "body_x"):
                cfg[k] = _pair(v, float)
            elif k == "caption_style":
                if v not in ("chapter", "flat"):
                    raise SystemExit(f"caption_style 은 chapter 또는 flat: {v!r}")
                cfg[k] = v
            elif k == "caption_bold":
                cfg[k] = v.lower() in ("yes", "true", "1", "y")
            elif k == "pdf":
                cfg[k] = v

    if cfg["offsets"] is None:          # page_offset 을 안 적었으면 스칼라 기본값을 쓴다
        cfg["offsets"] = [(1, 10 ** 9, cfg["page_offset"])]

    # PDF 경로 확정 — 지정이 없으면 ref/ 에서 찾는다
    if cfg["pdf"]:
        cfg["pdf"] = cfg["pdf"] if os.path.isabs(cfg["pdf"]) else os.path.join(root, cfg["pdf"])
    else:
        refdir = os.path.join(root, "ref")
        pdfs = sorted(f for f in os.listdir(refdir) if f.lower().endswith(".pdf")) \
            if os.path.isdir(refdir) else []
        if len(pdfs) == 1:
            cfg["pdf"] = os.path.join(refdir, pdfs[0])
        elif len(pdfs) > 1:
            raise SystemExit(
                "ref/ 에 PDF가 여러 개다. kit.conf 에 pdf = ref/<파일명> 을 지정하라:\n  "
                + "\n  ".join(pdfs))
        else:
            hint = ("\n(킷을 하위 폴더에 담아 두었다면 ref/ 는 그 상위, 즉 스터디 루트에 둔다.)"
                    if cfg["root"] == cfg["kit"] else "")
            raise SystemExit(
                f"PDF를 찾을 수 없다. {refdir} 에 넣거나 kit.conf 에 지정하라.{hint}")
    return cfg


if __name__ == "__main__":
    import json
    c = load()
    print(json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()},
                     indent=2, ensure_ascii=False))
