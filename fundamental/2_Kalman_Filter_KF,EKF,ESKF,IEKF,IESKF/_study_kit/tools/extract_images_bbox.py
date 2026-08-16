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
    (3, 1):  "fig_p03_weight_measurement_noise",
    (4, 1):  "fig_p04_estimation_problem",
    (5, 1):  "fig_p05_filtering_smoothing_prediction_interpolation",
    (6, 1):  "fig_p06_dynamic_system_block",
    (6, 2):  "fig_p06_dynamic_system_graph",
    (6, 3):  "fig_p06_prediction_step_graph",
    (6, 4):  "fig_p06_update_step_graph",
    (7, 1):  "fig_p07_belief_graph",
    (10, 1): "fig_p10_kf_pipeline",
    (13, 1): "fig_p13_nd_vs_1d_kalman_filter",
    (13, 2): "fig_p13_predict_correct_pdf",
    (15, 1): "fig_p15_ekf_pipeline",
    (18, 1): "fig_p18_eskf_pipeline",
    (23, 1): "fig_p23_iekf_pipeline",
    (26, 1): "fig_p26_ieskf_pipeline",
    (32, 1): "fig_p32_Lt_quadratic_curvature",
    (38, 1): "fig_p38_kf_update_recap",
    (45, 1): "fig_p45_ieskf_update_derivation_1",
    (45, 2): "fig_p45_ieskf_update_derivation_2",
    (46, 1): "fig_p46_wrapup_kf",
    (46, 2): "fig_p46_wrapup_ekf",
    (47, 1): "fig_p47_wrapup_eskf",
    (47, 2): "fig_p47_wrapup_iekf",
    (48, 1): "fig_p48_wrapup_ieskf",
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
