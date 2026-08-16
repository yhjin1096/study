#!/usr/bin/env python3
"""
캡션이 없는 문서의 그림 추출기.

이 문서(Notes on Lie Theory)에는 캡션이 하나도 없다 — 전문에서 Figure/Table/Fig. 가 0회다.
그래서 캡션 기반인 extract_figures.py 를 쓸 수 없다. 그림 29개와 이미지 객체 29개가 1:1 로
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
    ( 3, 1): "fig01_p03_smooth_vs_nonsmooth_manifold",
    ( 4, 1): "fig02_p04_manifold",
    ( 4, 2): "fig03_p04_unit_quaternion_constraint",
    ( 5, 1): "fig04_p05_lie_group_and_lie_algebra",
    ( 5, 2): "fig05_p05_exponential_logarithm_mapping",
    ( 6, 1): "fig06_p06_plus_operator",
    ( 6, 2): "fig07_p06_tangent_at_identity_and_composition",
    ( 6, 3): "fig08_p06_minus_operator",
    ( 7, 1): "fig09_p07_tangent_space",
    ( 7, 2): "fig10_p07_y_minus_x_on_tangent_space",
    ( 7, 3): "fig11_p07_error_xhat_minus_x",
    ( 8, 1): "fig12_p08_jacobian_between_manifolds",
    ( 9, 1): "fig13_p09_perturbation_and_covariance",
    ( 9, 2): "fig14_p09_so3_manifold_and_tangent",
    (11, 1): "fig15_p11_so3_exp_log_diagram",
    (13, 1): "fig16_p13_so3_derivative_at_identity",
    (14, 1): "fig17_p14_so3_plus_operator",
    (14, 2): "fig18_p14_so3_minus_operator",
    (15, 1): "fig19_p15_so3_adjoint",
    (16, 1): "fig20_p16_se3_manifold_and_tangent",
    (18, 1): "fig21_p18_se3_exp_log_diagram",
    (20, 1): "fig22_p20_se3_plus_operator",
    (20, 2): "fig23_p20_se3_minus_operator",
    (20, 3): "fig24_p20_se3_adjoint",
    (23, 1): "fig25_p23_poses_and_landmarks",
    (23, 2): "fig26_p23_ekf_localization_known_landmarks",
    (24, 1): "fig27_p24_pose_graph_slam_all_unknown",
    (25, 1): "fig28_p25_jacobian_sparsity",
    (25, 2): "fig29_p25_se3_left_update",
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
