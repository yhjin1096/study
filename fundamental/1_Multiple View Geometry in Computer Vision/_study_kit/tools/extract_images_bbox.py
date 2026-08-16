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
    # 캡션이 하나도 없다. 파일명은 그림 바로 앞의 소제목에서 따 왔다.
    (  7, 1): "fig01_p007_projective_space",
    (  8, 1): "fig02_p008_homogeneous_representation_of_line",
    (  9, 1): "fig03_p009_homogeneous_representation_of_points",
    (  9, 2): "fig04_p009_intersection_of_lines",
    ( 10, 1): "fig05_p010_ideal_points_and_the_line_at_infinity",
    ( 12, 1): "fig06_p012_a_model_for_the_projective_plane",
    ( 12, 2): "fig07_p012_conics_and_dual_conics",
    ( 15, 1): "fig08_p015_a_hierarchy_of_transformations",
    ( 17, 1): "fig09_p017_recovery_of_affine_and_metric_properties_from",
    ( 18, 1): "fig10_p018_recovery_of_affine_properties_from_images",
    ( 20, 1): "fig11_p020_recovery_of_metric_properties_from_images",
    ( 22, 1): "fig12_p022_recovery_of_metric_properties_from_images",
    ( 23, 1): "fig13_p023_the_basic_pinhole_model",
    ( 24, 1): "fig14_p024_the_basic_pinhole_model",
    ( 25, 1): "fig15_p025_principal_point_offset",
    ( 26, 1): "fig16_p026_camera_rotation_and_translation",
    ( 28, 1): "fig17_p028_column_vectors",
    ( 29, 1): "fig18_p029_the_principal_plane",
    ( 31, 1): "fig19_p031_back_projection_of_points_to_rays",
    ( 32, 1): "fig20_p032_result_6_1",
    ( 33, 1): "fig21_p033_cameras_at_infinity",
    ( 33, 2): "fig22_p033_definition_6_3",
    ( 34, 1): "fig23_p034_affine_cameras",
    ( 36, 1): "fig24_p036_error_in_employing_and_affine_camera",
    ( 40, 1): "fig25_p040_geometric_error",
    ( 41, 1): "fig26_p041_zhang_s_method",
    ( 43, 1): "fig27_p043_radial_distortion",
    ( 44, 1): "fig28_p044_radial_distortion",
    ( 44, 2): "fig29_p044_result_8_15",
    ( 45, 1): "fig30_p045_result_8_15",
    ( 45, 2): "fig31_p045_result_8_16",
    ( 47, 1): "fig32_p047_result_8_17",
    ( 47, 2): "fig33_p047_vanishing_points_and_vanishing_lines",
    ( 48, 1): "fig34_p048_vanishing_lines",
    ( 49, 1): "fig35_p049_orthogonality_relationships_amongst_vanishing",
    ( 50, 1): "fig36_p050_affine_3d_measurements_and_reconstruction",
    ( 51, 1): "fig37_p051_calibration_from_three_orthogonal_vanishing_po",
    ( 52, 1): "fig38_p052_vanishing_line",
    ( 52, 2): "fig39_p052_the_calibrating_conic",
    ( 53, 1): "fig40_p053_the_calibrating_conic",
    ( 54, 1): "fig41_p054_epipolar_geometry",
    ( 55, 1): "fig42_p055_geometric_derivation",
    ( 56, 1): "fig43_p056_algebraic_derivation",
    ( 58, 1): "fig44_p058_pure_translation",
    ( 68, 1): "fig45_p068_geometrical_interpretation_of_the_four_solutio",
    ( 68, 2): "fig46_p068_3d_reconstruction_of_cameras_and_structure",
    ( 70, 1): "fig47_p070_the_step_to_affine_reconstruction",
    ( 75, 1): "fig48_p075_structure_computation",
    ( 75, 2): "fig49_p075_problem_statement",
    ( 78, 1): "fig50_p078_reformulation_of_the_minimization_problem",
    ( 80, 1): "fig51_p080_homographies_given_the_plane_and_vice_versa",
    ( 82, 1): "fig52_p082_homographies_compatible_with_epipolar_geometry",
    ( 84, 1): "fig53_p084_three_points",
    ( 86, 1): "fig54_p086_a_point_and_line",
    ( 87, 1): "fig55_p087_result_13_8",
    ( 88, 1): "fig56_p088_result_13_8",
    ( 89, 1): "fig57_p089_affine_epipolar_geometry",
    ( 90, 1): "fig58_p090_affine_epipolar_geometry",
    ( 92, 1): "fig59_p092_epipolar_lines",
    ( 93, 1): "fig60_p093_the_trifocal_tensor",
    ( 96, 1): "fig61_p096_point_and_line_incidence_relations",
    (101, 1): "fig62_p101_point_transfer_using_the_trifocal_tensor",
    (102, 1): "fig63_p102_the_fundamental_matrices_for_three_views",
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
