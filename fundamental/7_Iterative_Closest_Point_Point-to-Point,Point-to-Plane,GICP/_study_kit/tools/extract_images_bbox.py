#!/usr/bin/env python3
"""
캡션이 없는 문서의 그림 추출기.

이 문서에는 그림 캡션이 하나도 없다 — 전문에서 Figure/Fig./Table 이 모두 0회다.
그래서 캡션 기반인 extract_figures.py 를 쓸 수 없다.
그림 9개와 이미지 객체 9개가 1:1 로 대응하므로 bbox 를 그대로 clip 으로 삼는다. (페이지 전체를 덮는 스캔 이미지가 아니라
그림 영역과 정확히 일치하는 것을 확인한 뒤 이 방식을 택했다 — 3_Pitfalls.md A5·A10 참조)

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
    # 캡션이 하나도 없어 파일명은 그림 내용을 보고 지었다.
    ( 2, 1): "fig01_p02_example_pointcloud_2d",
    ( 3, 1): "fig02_p03_known_data_associations",
    ( 4, 1): "fig03_p04_centroid_alignment",
    ( 8, 1): "fig04_p08_unknown_data_associations",
    ( 8, 2): "fig05_p08_icp_steps_1_to_3",
    ( 9, 1): "fig06_p09_icp_steps_4_to_6",
    (13, 1): "fig07_p13_point_to_plane_geometry",
    (20, 1): "fig08_p20_projection_matrix_equivalence",
    (21, 1): "fig09_p21_projection_matrix",
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
