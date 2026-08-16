#!/usr/bin/env python3
"""
캡션이 없는 문서의 그림 추출기.

이 문서(Notes on Linear Algebra)에는 캡션이 하나도 없다 — 전문에서 Figure/Table/Fig. 가 0회다.
그래서 캡션 기반인 extract_figures.py 를 쓸 수 없다. 그림 19개와 이미지 객체 19개가 1:1 로
대응하므로 bbox 를 그대로 clip 으로 삼는다. (페이지 전체를 덮는 스캔 이미지가 아니라
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
    ( 6, 1): "fig01_p06_overdetermined_system",
    ( 6, 2): "fig02_p06_underdetermined_system",
    ( 7, 1): "fig03_p07_span_in_R2_and_R3",
    ( 8, 1): "fig04_p08_linear_independence_vs_dependence",
    (10, 1): "fig05_p10_standard_basis_vectors",
    (11, 1): "fig06_p11_column_space",
    (13, 1): "fig07_p13_domain_codomain_range",
    (14, 1): "fig08_p14_surjective_injective",
    (16, 1): "fig09_p16_orthogonal_vectors",
    (16, 2): "fig10_p16_least_square_projection",
    (19, 1): "fig11_p19_orthogonal_vs_orthonormal_set",
    (20, 1): "fig12_p20_projection_onto_line",
    (20, 2): "fig13_p20_projection_onto_plane",
    (21, 1): "fig14_p21_gram_schmidt",
    (22, 1): "fig15_p22_eigenvector",
    (23, 1): "fig16_p23_four_subspaces_orthogonality",
    (26, 1): "fig17_p26_svd_matrix_shapes",
    (37, 1): "fig18_p37_leading_principal_minors",
    (42, 1): "fig19_p42_svd_matrix_shapes",
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
