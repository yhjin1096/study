#!/usr/bin/env python3
"""
캡션이 없는 문서의 그림 추출기.

이 문서는 캡션이 있어 extract_figures.py 도 라벨은 찾지만, 그림이 절 제목 바로 아래에 오는
경우 영역 판정이 위쪽 본문까지 물어 온다(3_Pitfalls A7 계열). 이 문서는 그림 19개와 이미지
객체 19개가 1:1 로 대응하므로 bbox 를 그대로 clip 으로 삼는 이 방식이 더 정확하다. (페이지 전체를 덮는 스캔 이미지가 아니라
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
    (10, 1): "fig01_p10_3d_vector_rotation",
    (13, 1): "fig02_p13_so3_trajectory",
    (15, 1): "fig03_p15_exp_log_map",
    (17, 1): "fig04_p17_unit_quaternion_manifold_S3",
    (18, 1): "fig05_p18_S3_tangent_space",
    (20, 1): "fig06_p20_double_cover",
    (22, 1): "fig07_p22_quaternion_composition",
    (23, 1): "fig08_p23_slerp_linear_interpolation",
    (24, 1): "fig09_p24_slerp_q_perp",
    (25, 1): "fig10_p25_slerp_negative_q1",
    (26, 1): "fig11_p26_rotation_in_R2_R3",
    (26, 2): "fig12_p26_isoclinic_two_planes",
    (27, 1): "fig13_p27_q_x_q_rotation",
    (28, 1): "fig14_p28_q_x_qconj_rotation",
    (34, 1): "fig15_p34_right_jacobian",
    (39, 1): "fig16_p39_zeroth_first_order_integration",
    (39, 2): "fig17_p39_forward_midward_backward_integration",
    (43, 1): "fig18_p43_state_variable_table",
    (57, 1): "fig19_p57_global_error_state_table",
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
