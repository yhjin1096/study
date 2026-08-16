#!/usr/bin/env python3
"""
캡션이 없는 문서의 그림 추출기.

이 스터디의 원본(Notes on Probability Theory)에는 Figure/Table 캡션이 하나도 없어
캡션 기반인 extract_figures.py 를 쓸 수 없다. 대신 페이지에 박혀 있는 이미지 객체의
bbox 를 그대로 clip 으로 삼아 렌더링한다. (페이지 전체를 덮는 스캔 이미지가 아니라
그림 영역과 정확히 일치하는 것을 확인한 뒤 이 방식을 택했다 — 3_Pitfalls.md A5 참조)

사용법:
    python3 _study_kit/tools/extract_images_bbox.py --list
    python3 _study_kit/tools/extract_images_bbox.py --out notes/images
"""
import argparse, sys
from pathlib import Path
import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit_config

# (PDF 쪽, 그 쪽에서의 순번) -> 파일명. 순번은 get_image_info() 반환 순서(위→아래).
NAMES = {
    (5, 1):  "fig_p05_function_mapping",
    (5, 2):  "fig_p05_surjective_injective",
    (8, 1):  "fig_p08_probability_space",
    (10, 1): "fig_p10_joint_probability_venn",
    (11, 1): "fig_p11_random_variable",
    (12, 1): "fig_p12_random_variable_preimage",
    (24, 1): "fig_p24_covariance_scatter",
    (25, 1): "fig_p25_central_limit_theorem",
    (30, 1): "fig_p30_scalar_vector_infinite_rv",
    (31, 1): "fig_p31_infinite_dimension_function",
    (31, 2): "fig_p31_random_process_sample_paths",
    (33, 1): "fig_p33_fixed_t_vs_fixed_w",
}

PAD = 2.0   # bbox 가 글자를 아슬아슬하게 자르는 것을 막는 여유 (pt)
DPI = 200


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="추출하지 않고 목록만 출력")
    ap.add_argument("--out", default="notes/images")
    args = ap.parse_args()

    cfg = kit_config.load()
    doc = fitz.open(cfg["pdf"])
    out = Path(cfg["root"]) / args.out
    if not args.list:
        out.mkdir(parents=True, exist_ok=True)

    n = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for idx, info in enumerate(page.get_image_info(), start=1):
            key = (pno + 1, idx)
            name = NAMES.get(key, f"fig_p{pno+1:02d}_{idx}")
            b = fitz.Rect(info["bbox"]) + (-PAD, -PAD, PAD, PAD)
            if args.list:
                print(f"p{pno+1:>2} #{idx}  {b.width:6.1f}x{b.height:6.1f}pt  {name}")
            else:
                pix = page.get_pixmap(clip=b, dpi=DPI)
                pix.save(out / f"{name}.png")
                print(f"저장 {name}.png  ({pix.width}x{pix.height}px)")
            n += 1
    print(f"\n총 {n}개")


if __name__ == "__main__":
    main()
