# Notes on Iterative Closest Point 스터디

Gyubeom Edward Im의 강의 노트 *Notes on Iterative Closest Point
(Point-to-Point, Point-to-Plane, GICP)* (24쪽)를 **내용 수정 없이 그대로** HTML로 옮기고,
이해를 돕는 **인터랙티브 위젯 12개**를 절 사이에 끼워 넣은 자료다.
SVD 닫힌 해 → Vanila ICP → least squares ICP(2D/3D) → point-to-plane → GICP 까지
원문 8개 장 20개 절 전체를 다룬다.

원본 PDF: `ref/Notes on Iterative Closest Point(Point-to-Point, Point-to-Plane, GICP).pdf`
결과물: `notes/notes_on_icp.html` (단일 파일 3.8MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/inject_helper.py             # 위젯에 window.IC 주입
python3 _study_kit/tools/build_html.py notes/notes_on_icp.md
python3 _study_kit/tools/check_refs.py
```

## 이 스터디에서 원래 킷과 달라진 점

### ① 색이 네 가지다 — 지금까지 최다

| 색 | 어디에 | 개수 | 어떻게 옮겼나 |
|---|---|---|---|
| `#197fb2` 파랑 | 산문 강조 | 40구간 (논리 39) | `==강조==` → `<span class="hl">` |
| `#a50000` 진홍 | 수식 (p4·p5·p19) + 산문 (p12·p17·p19·p23) | 15 | 수식은 `\color`, 산문은 `{{c\|…}}` |
| `#ff0000` 빨강 | "빨간색" 범례 · `sourcePoints` · 수식의 source 항 | 7 | 수식은 `\color`, 산문은 `{{r\|…}}` |
| `#00ffff` 하늘 | "파란색" 범례 · `targetPoints` · 수식의 target 항 | 7 | 수식은 `\color`, 산문은 `{{t\|…}}` |

빨강/하늘은 **그림의 점 색을 가리키는 범례**다. 원문이 "빨간색 점 = sourcePoints,
파란색 점 = targetPoints" 라고 쓰고 이후 식 (1)(2) 에서도 같은 색으로 항을 구분한다.
의미가 있으므로 그대로 재현했다. (`#00ffff` 는 흰 배경에서 흐리지만 원문 값 그대로 두고
다크 모드 대비만 CSS로 보정했다.)

이를 위해 **`build_html.py` 에 색 마커 세 개를 추가**했다:

```
{{c|…}} → <span class="hl-crimson">     {{r|…}} → <span class="hl-src">
{{t|…}} → <span class="hl-tgt">
```

CSS 변수 `--hl-crimson / --hl-src / --hl-tgt` 로 라이트·다크 값을 따로 준다.
수식 안의 색은 `\color{#a50000}{…}` 처럼 직접 찍고, SVG 속성으로 박히는 값은
다크 모드에서 `[fill="#ff0000"] { fill:#ff6b6b }` 규칙으로 밝힌다 (3_Pitfalls B6).

### ② 그림에 캡션이 하나도 없다

전문에서 `Figure`/`Fig.`/`Table` 이 **0회**다. `extract_images_bbox.py` 로 이미지 객체 9개를
그대로 뽑고 파일명은 내용을 보고 지었다.

```
fig01_p02_example_pointcloud_2d      fig06_p09_icp_steps_4_to_6
fig02_p03_known_data_associations    fig07_p13_point_to_plane_geometry
fig03_p04_centroid_alignment         fig08_p20_projection_matrix_equivalence
fig04_p08_unknown_data_associations  fig09_p21_projection_matrix
fig05_p08_icp_steps_1_to_3
```

fig05·fig06 은 4.2절 알고리즘의 1~3 단계와 4~6 단계로 이어지는 한 쌍이다.

### ③ `window.IC` — 헬퍼 5대째

```
LG(Lie Theory) → PI(Preintegration) → VM(VINS-Mono) → EJ(Errors and Jacobians) → IC(여기)
```

`IC` 는 `EJ` 를 그대로 물려받고 (SO(3)/SE(3), 쿼터니언, 수치미분, 선형대수, 플롯) 아래를 더했다.

| 갈래 | 함수 |
|---|---|
| 고유분해·SVD | `eigSym` (순환 Jacobi) · `svd` (AᵀA 고유분해 + 그람-슈미트) · `det3` |
| 예제 데이터 | `ex2D` `ex3D` — **원문 2·3장의 점군을 그대로** |
| 점군 기본 | `centroid`(3) `demean`(4) `covXY`(9) `transform` `nearest` `rmse` `R2d` |
| 닫힌 해 | `svdSolve(Ps, Pt, fixDet)` — 식 (26)(27) |
| 법선 | `normal2D` (5.1절) · `normalsPCA(P, k)` (5.2·6.3절) |
| 자코비안 | `jacP2P2D`(32) `jacP2P3D`(43) `jacP2L2D`(55) `jacP2L3D`(66) |
| GN 루프 | `gnStepICP` (p2p/p2l/gicp 공용, 식 98) · `applyDx` · `runICP` |
| GICP | `gicpCovs`(88·89) · `projMat`(84·87) |

SVD 는 `AᵀA` 를 고유분해하는 방식이라 **rank-deficient 입력에서 재구성 오차가
$\sqrt{\varepsilon}$ 수준(≈1e-8)** 이다. 대신 `UᵀU = I` 는 1e-16 로 유지되도록
영공간 열을 그람-슈미트로 채운다 — ICP 에서는 $\mathbf{R}=\mathbf{V}\mathbf{U}^\intercal$ 의
직교성이 재구성 정밀도보다 중요하기 때문이다.

**검산표** (헤드리스 Chrome, `window.IC` 항등식):

```
eigSym  V diag(w) Vᵀ = A        1.2e-14     식 (32) J 2×3 vs 수치미분      3.3e-9
eigSym  VᵀV = I                 1.4e-15     식 (43) J 3×6 (좌섭동)         6.1e-9
svd  U D Vᵀ = A                 1.3e-15     식 (55) J 1×3                  5.3e-9
svd  UᵀU = I (rank-2 포함)      1.1e-15     식 (66) J 1×6                  4.5e-9
식 (26) R 복원 (3D)             7.1e-15     normalsPCA 평면 법선           7.5e-16
식 (26) t 복원 (3D)             5.2e-14     식 (85) P = P²                 1.2e-16
식 (26) θ 복원 (2D)             1.1e-16     식 (85) P = Pᵀ                 0
식 (27) reflection  det         −1 → +1     식 (89) C 고유값               1, 1, ε
runICP  svd / p2p / p2l / gicp  RMSE 4.7 → 1e-14 이하 (전부)
```

### ④ 위젯이 "원문 데이터로 실제로 돌리는" 형식이다

앞 스터디들이 자코비안 검산 위주였다면, 여기서는 **원문 2·3장의 점군을 그대로 넣고
ICP 를 끝까지 수렴시켜** 보여 준다. 그 덕에 원문에 없는 사실 두 가지가 드러났다 —
point-to-plane 의 초기값 취약성(실험 6), `n = [−y, x]` 를 위치벡터에 쓸 때의 실패(실험 7).

## 원문에서 찾은 어긋남 네 곳

전사 원칙상 **원문 식은 그대로 두었다.** 노트 맨 아래 「원문 그대로 둔 것」 표와
해당 위젯의 「고쳐서」 버튼에서 확인할 수 있다.

| 식 | 원문 | 실제 값 | 위젯 |
|---|---|---|---|
| (22) | $\mathbf{t} = \mathbf{R}\bar{\mathbf{p}}_t - \bar{\mathbf{p}}_{t+1}$ | 부호 반대. (6)·(26) 과 같아야 한다 | 실험 2 |
| (56) 끝줄 | $- n^y(\cdots)$ | $+ n^y(\cdots)$. **앞 (55) 는 맞다** | 실험 8 |
| (66)(68) 회전 3열 | 성분마다 자기 $n$ 만 곱함 | $\mathbf{n}^\intercal[\cdot]_\times$ 로 세 성분이 섞여야 함 | 실험 8 |
| (86) 둘째 줄 | $\|d^\intercal\mathbf{P}d\|^2$ | $d^\intercal\mathbf{P}d$ (한 번 더 제곱됨) | 실험 10 |

읽는 법의 문제 셋도 부록에 적었다 — (55) 의 2행 레이아웃, `n = [−y, x]` 의 해석, `Vanila` 철자.

## 검증

```
식 (1)~(101)          101개 · 누락 0 · 중복 0 · 순서 일치
PDF 문장 265개        전부 노트에 있음 (불릿 36개도 확인)
색 4종 양방향 대조    원문 구간 ↔ 노트 구간 불일치 0
mjx-container         558 · display 수식 101 · MathJax 오류 0
hl 39 · callout 11 · 인라인 이미지 9 · 위젯 12
위젯 헤드리스 조작    버튼 전부 클릭 + 슬라이더 min/mid/max → 오류 0, 빈 캔버스 0, NaN 0
수식 가로 넘침        폭 820~1920px 전 구간에서 0, 페이지 본문 가로 스크롤 0
```

빌더의 수식 자동 축소를 **반복형으로 고쳤다** (3_Pitfalls C7).
기존 한 번 계산 방식은 판정 대상을 잘못 잡아 **모든 수식을 불필요하게 줄이면서도**
특정 창 폭에서 몇 픽셀씩 넘쳤다. 지금은 축소되는 수식이 창 폭에 따라 1~5개뿐이고
넘침은 0이다.
