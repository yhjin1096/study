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
"""
import glob
import os
import re

DEFAULTS = {
    "pdf": None,            # None 이면 ref/ 에서 자동 탐색
    "caption_style": "chapter",   # "chapter" = Figure 6.3 / "flat" = Figure 3
    "caption_bold": True,         # 캡션 라벨이 볼드체인가
    "page_offset": 0,
    "last_chapter": 99,
    "book_pages": (1, 9999),
    "clip_x": (155.0, 522.0),
    "header_y": 52.0,
    "body_x": (186.0, 488.0),
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
            if k in ("page_offset", "last_chapter"):
                cfg[k] = int(v)
            elif k in ("header_y",):
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
