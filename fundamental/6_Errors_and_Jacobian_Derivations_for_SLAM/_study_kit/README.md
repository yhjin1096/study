# Errors and Jacobian Derivations for SLAM 스터디

Gyubeom Edward Im의 강의 노트 *Errors and Jacobian Derivations for SLAM* (45쪽, 10차 개정)을
**내용 수정 없이 그대로** HTML로 옮기고, 이해를 돕는 **인터랙티브 위젯 12개**를 절 사이에
끼워 넣은 자료다. 재투영·광도·상대포즈·직선·IMU 다섯 가지 에러와 그 자코비안,
그리고 쿼터니언·내부 파라미터·inverse depth 자코비안까지 원문 10개 장 42개 절 전체를 다룬다.

원본 PDF: `ref/Errors and Jacobian Derivations for SLAM.pdf`
결과물: `notes/notes_on_errors_and_jacobians.html` (단일 파일 4.2MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/inject_helper.py             # 위젯에 window.EJ 주입
python3 _study_kit/tools/build_html.py notes/notes_on_errors_and_jacobians.md
python3 _study_kit/tools/check_refs.py
```

## 이 스터디에서 원래 킷과 달라진 점

### ① 색이 한 가지뿐이다

| 색 | 어디에 | 폰트 | 개수 | 어떻게 옮겼나 |
|---|---|---|---|---|
| `#197fb2` 파랑 | 산문 강조 | nanum·SFBX | 40구간 | `==강조==` → `<span class="hl">` |

**수식 안에는 색이 없다.** 4·5번 스터디에서 필요했던 `\color{...}` 를 이 문서에서는
한 번도 쓰지 않는다. `tools/dump_colored.py` 의 색 목록도 하나로 줄여 두었다
(`GROUP = {"prose": (BLUE,), "math": ()}`).

### ② 그림에 캡션이 하나도 없다

전문에서 `Figure` / `Fig.` / `Table` 이 **0회**다. `tools/extract_figures.py`(캡션 기반)를
쓸 수 없어 `tools/extract_images_bbox.py` 로 이미지 객체 9개를 그대로 뽑았다.
bbox 가 전부 페이지 안쪽이라 잘림 없이 나온다.

파일명은 캡션 대신 **내용을 보고 지었다**:

```
fig01_p07_reprojection_error_geometry      fig06_p27_line_transformation
fig02_p07_projection_pipeline              fig07_p28_line_reprojection_error
fig03_p14_photometric_error_geometry       fig08_p31_imu_preintegration_overview
fig04_p14_photometric_projection_pipeline  fig09_p32_preintegration_factor_and_residual
fig05_p22_relative_pose_error_factor
```

p7·p14 의 두 번째 그림은 가로로 긴 **투영 파이프라인 표** 이미지다 (454×55, 454×60).

### ③ 코드 리스팅이 없다

"Code implementations" 절이 8개나 되지만 전부 **소스 링크 목록**이다.
문서 전체에 고정폭 폰트가 0회 쓰였다 — 코드 블록 처리를 신경 쓸 필요가 없었다.

### ④ 위젯이 전부 "수치미분 대조형"이다

자코비안 문서이므로, 위젯의 기본 형식을 **원문 식으로 계산한 행렬 vs 유한차분으로 구한 행렬**
로 잡았다. 두 값을 나란히 찍고 상대오차를 표시한다.
이 형식 덕분에 **원문의 어긋남 세 곳을 찾아냈다** (아래 참조).

### ⑤ `window.EJ` — 헬퍼 4대째

```
LG (3_Lie_Theory)  →  PI (4_Preintegration)  →  VM (5_VINS-Mono)  →  EJ (여기)
```

`EJ` 는 `VM` 을 그대로 물려받고 (SO(3)/SE(3), 쿼터니언, preintegration, 선형대수, 플롯)
아래를 더했다.

| 갈래 | 함수 |
|---|---|
| 핀홀 투영 | `piH` `piK` `project` `backProject` `distort` `projectD` `dpdX`(식 48·49) |
| 합성 이미지 | `makeImage(seed, blur)` — 3중 스케일 가우시안 블롭. **∇I 가 해석적**이라 수치미분 검산에 쓸 수 있다. blur 는 각 블롭 σ 에 제곱합으로 더해진다 |
| Plücker 직선 | `lineFromPoints` `lineTransform`(131) `KLmat`(133) `lineProject`(132) `lineError`(134) `toOrthonormal`(136·137) `fromOrthonormal`(138) `orthoUpdate` |
| 쿼터니언 | `qLmat` `qRmat` `br3` — 식 (178)~(180) 의 $[\cdot]_L,[\cdot]_R,[\cdot]_{3\times3}$ |
| 최적화 | `gnStep(H, b, lam)` — 식 (31)(33) |

**검산표** (헤드리스 Chrome, `window.EJ` 항등식):

```
expSO3/logSO3 왕복                1.1e-16     식 (148) ∂e_l/∂l            5.1e-10
q2R(qexp(v)) = expSO3(v)          2.0e-16     식 (131)(150) T_cw L_w      4.4e-16
project → backProject             0           식 (151) ∂L_w/∂δθ           (실험 10)
식 (48)(49) ∂p̂/∂X′               1.2e-8      식 (152) ∂L_c/∂δξ           (실험 10)
식 (61)(62) J_c (좌섭동)           2.9e-8      식 (178)~(181) 18블록        (실험 11)
식 (67) J_p                        3.4e-8      식 (190) ∂X̃′/∂v            7.7e-11
식 (83) ∇I 해석 vs 수치            1.1e-13     식 (199) ∂p₂/∂c             7.3e-8
식 (99) J (1×6)                    4.6e-11     식 (204) ∂p₂/∂ρ             7.1e-8
식 (117) e_ij (관측=예측)          0           Klein quadric mᵀd           7.2e-16
식 (128) J_ij (좌섭동)             1.5e-10     Plücker ↔ (U,W) 왕복        1.1e-16
```

## 원문에서 찾은 어긋남 세 곳

전사 원칙상 **원문 식은 그대로 두었다.** 노트 맨 아래 「원문 그대로 둔 것」 표와
해당 위젯의 「고쳐서」 버튼에서 확인할 수 있다.

| 식 | 원문 | 실제 미분값 | 위젯 |
|---|---|---|---|
| (178) 2행 | 부호 없음 | **음수** — 뒤집으면 1.2e-10 | 실험 11 |
| (178) 3행 | $\mathbf{p}_{b_{k+1}}-\mathbf{p}_{b_k}$ | $\mathbf{v}_{b_{k+1}}-\mathbf{v}_{b_k}$ — 3.1e-10 | 실험 11 |
| (198) 끝줄 · (199) (2,4) | $\tilde{u}_2,\ r_{12}$ | $\tilde{v}_2,\ r_{22}$ — 7.3e-8 | 실험 12 |

읽는 법의 문제 두 가지도 부록에 적어 두었다 — (52) vs (61) 의 섭동 규약,
(109) vs (119) 의 섭동 방향.

## 검증

```
식 (1)~(204)          204개 · 누락 0 · 중복 0 · 순서 일치
PDF 문장 430개        전부 노트에 있음 (불릿 158개도 확인)
본문 식 참조 77곳     전부 실재하는 번호
mjx-container         990 · display 수식 204 · MathJax 오류 0
hl span 40 · callout 13 · 인라인 이미지 9 · 위젯 12
위젯 헤드리스 조작    버튼 전부 클릭 + 슬라이더 min/mid/max → 오류 0, 빈 캔버스 0, NaN 0
수식 가로 넘침        폭 900~1920px 에서 식 (182)(199) 둘만 자체 스크롤 (의도된 동작),
                      페이지 본문 가로 스크롤 0
```

식 (182)(199) 는 자동 축소 하한(55%)에 걸린다 — 더 줄이면 읽을 수 없어서
`.mathblock { overflow-x:auto }` 로 각자 스크롤하게 두었다.
