# 학습 범위 목차 — Errors and Jacobian Derivations for SLAM

Gyubeom Edward Im, 45쪽 (10차 개정 2024-05-25)
쪽번호는 원문 그대로다 (PDF 쪽 = 인쇄 쪽, 오프셋 0).

노트: [`notes/notes_on_errors_and_jacobians.md`](../notes/notes_on_errors_and_jacobians.md) →
`.html` (단일 파일 4.2MB, 오프라인으로 열림)

---

## 전체 구성

| 절 | 제목 | 쪽 | 식 | 그림 | 위젯 |
|---|---|---|---|---|---|
| 1 | Introduction | 2 | (1)~(15) | | |
| 2 | Optimization formulation | 3 | | | |
| 2.1 | Error derivation | 3 | (16) | | |
| 2.2 | Error function derivation | 3 | (17)~(23) | | |
| 2.3 | Non-linear least squares | 4 | (24)~(33) | | **실험 1** |
| 3 | Reprojection error | 6 | | | |
| 3.1 | Jacobian of the reprojection error | 7 | (34)~(51) | 2 | **실험 2** |
| 3.1.1 | Jacobian of camera pose | 7 | (52)~(62) | | **실험 3·4** |
| 3.1.2 | Lie theory-based SO(3) optimization | 9 | | | |
| 3.2 | Jacobian of Map Point | 12 | (63)~(67) | | **실험 5** |
| 3.3 | Code implementations | 13 | — | | |
| 4 | Photometric error | 14 | | 2 | |
| 4.1 | Jacobian of the photometric error | 15 | (68)~(99) | | **실험 6·7** |
| 4.1.1 | Lie theory-based SE(3) optimization | 17 | | | |
| 4.2 | Code implementations | 21 | — | | |
| 5 | Relative pose error | 22 | | 1 | |
| 5.1 | Jacobian of relative pose error | 23 | (100)~(128) | | **실험 8** |
| 5.1.1 | Lie theory-based SE(3) optimization | 24 | | | |
| 5.2 | Code implementations | 26 | — | | |
| 6 | Line reprojection error | 27 | | 2 | |
| 6.1 | Line Transformation and projection | 27 | (129)~(133) | | |
| 6.2 | Line reprojection error | 28 | (134) | | |
| 6.3 | Orthonormal representation | 29 | (135)~(138) | | **실험 9** |
| 6.4 | Error function formulation | 30 | (139)~(145) | | |
| 6.4.1 | The analytical jacobian of 3d line | 30 | (146)~(152) | | **실험 10** |
| 6.5 | Code implementations | 31 | — | | |
| 7 | IMU measurement error | 31 | | 2 | |
| 7.1 | Error function formulation | 32 | (153)~(171) | | |
| 7.2 | Jacobian of IMU measurement error | 36 | (172)~(184) | | **실험 11** |
| 7.2.1 | Lie theory-based SO(3) optimization | 37 | | | |
| 7.3 | Code implementations | 38 | — | | |
| 8 | Other jacobians | 39 | | | |
| 8.1 | Jacobian of unit quaternion | 39 | (185)~(190) | | |
| 8.2 | Jacobian of camera intrinsics | 40 | (191)~(199) | | |
| 8.3 | Jacobian of inverse depth | 43 | (200)~(204) | | **실험 12** |
| 9 | References | 45 | — | | |
| 10 | Revision log | 45 | — | | |

식 번호는 (1)~(204), 절은 42개, 그림은 9개다. **지금까지 일곱 스터디 중 가장 크다.**

**그림에 캡션이 하나도 없다** — 전문에서 Figure/Fig./Table 이 0회다.
그래서 `tools/extract_figures.py` 대신 `tools/extract_images_bbox.py` 로 뽑았다.

**"Code implementations" 절 8개** (3.3 · 4.2 · 5.2 · 6.5 · 7.3 · 8.1.1 · 8.2.1 · 8.3.3)는
전부 g2o/DSO/VINS-Mono 소스 **링크 목록**이다. 코드 리스팅이 박혀 있지 않다
(문서 전체에 고정폭 폰트가 0회 쓰였다).

---

## 위젯 12개

전부 **원문에 없는 추가 요소**라고 표시된 회색 박스 안에 들어 있다.
계산은 모두 `tools/widgets/_ej_helper.js` 의 `window.EJ` 가 한다.

이 문서는 **자코비안 문서**이므로 위젯도 대부분 **수치미분 대조형**으로 만들었다 —
원문 식으로 계산한 행렬과, 그 식을 전혀 쓰지 않고 유한차분으로 구한 행렬을 나란히 찍는다.

| # | 파일 | 붙는 곳 | 무엇을 보여주나 |
|---|---|---|---|
| 1 | `gauss-newton-vs-lm` | 2.3 끝 | (33) 의 $\lambda$ 하나가 GN 의 발산을 막는다 |
| 2 | `projection-pipeline` | 3.1 끝 | (34)~(47) 파이프라인 한 단계씩 + 왜곡 격자 |
| 3 | `so3-perturbation` | 3.1.1 중간 | ★ 좌·우 섭동이 **다른** 자코비안을 준다. 1차 근사 오차 기울기 2 |
| 4 | `camera-pose-jacobian` | 3.1.1 끝 | ★ (62) $\mathbf{J}_c$ vs 수치미분 · **섭동 규약 3종 비교** |
| 5 | `map-point-jacobian` | 3.2 끝 | ★ (67) vs 수치미분 + 베이스라인과 $\mathrm{cond}(\mathbf{H}_p)$ |
| 6 | `photometric-convergence` | 4장 도입 끝 | 광도 오차의 GN 성공률 (시드 6개 평균) — 블러가 곧 피라미드 |
| 7 | `se3-photometric-jacobian` | 4.1.1 끝 | ★ (99) 세 조각 사슬 vs 수치미분 · $\nabla I\!\to\!0$ 이면 전부 죽는다 |
| 8 | `relative-pose-error` | 5.1.1 끝 | ★ (128) 좌·우 섭동 비교 + pose graph 루프 클로저 |
| 9 | `plucker-orthonormal` | 6.3 끝 | ★ Plücker 직접 갱신은 Klein quadric 을 깬다, orthonormal 은 안 깬다 |
| 10 | `line-jacobian` | 6.4.1 끝 | ★ (148)(149)(150)(151)(152) **조각별로** + 곱까지 7개 전부 대조 |
| 11 | `imu-error-jacobian` | 7.2.1 끝 | ★ (178)~(181) 18개 블록 대조 — **(178) 두 곳이 원문과 어긋난다** |
| 12 | `other-jacobians` | 8.3.2 끝 | ★ (190)(199)(204) — **(199) 의 (2,4) 성분이 원문과 어긋난다** |

★ 는 **자기검산형** — 원문 식으로 구한 값과 독립적인 수치미분 값을 나란히 찍는다.
실험 4·8·11·12 는 「원문 그대로 / 고쳐서」 버튼으로 두 결과를 직접 비교할 수 있다.

---

## 추천 읽기 순서

45쪽이지만 구조는 단순하다 — **에러 종류마다 같은 절차를 반복**한다.
(에러 정의 → 최소제곱 → 자코비안 사슬 → 리 군 섭동 → 코드 링크)
2장에서 그 절차를 한 번 익히면 3~8장은 "무엇을 무엇으로 미분하나"만 바뀐다.

1. **2장 + 실험 1** — GN/LM. 이후 모든 장이 이 틀 위에 있다
2. **3.1.1 + 실험 3·4** — $\partial\hat{\mathbf{p}}/\partial\mathbf{X}'$ 와 $[-(\mathbf{X}')^\wedge\ \ \mathbf{I}]$.
   **이 노트에서 가장 많이 재사용되는 두 블록**이다. 섭동 규약을 여기서 확실히 해 둘 것
3. **3.2 + 실험 5** — 맵포인트. 3.1.1 의 결과를 재활용한다
4. **4.1.1 + 실험 7** — 광도 오차. 기하 부분은 3장과 **완전히 같고** 앞에 $\nabla I$ 만 붙는다
5. **실험 6** — 왜 direct method 가 피라미드를 쓰는가. 식보다 그림이 설명한다
6. **5.1.1 + 실험 8** — 상대 포즈. $\mathrm{Ad}$ 와 $\mathcal{J}_r^{-1}\approx\mathbf{I}$ 근사
7. **6장 + 실험 9·10** — 직선. 6.3 의 orthonormal 이 핵심이고 나머지는 사슬 계산
8. **7장 + 실험 11** — IMU. 5_VINS-Mono 스터디를 먼저 읽으면 훨씬 빠르다
9. **8장 + 실험 12** — 독립적인 세 자코비안. 필요할 때 찾아 보면 된다

## 진행 상황

| 항목 | 상태 |
|---|---|
| 전사 (1~10장) | 완료 · 식 (1)~(204) 누락·중복 없음 · 순서 일치 |
| 원문 대조 | 완료 · PDF 문장 430개 전부 노트에 있음 · 불릿 158개 확인 |
| 그림 9개 | 완료 · bbox 추출 (캡션이 없어 파일명은 내용으로 지었다) |
| 파란 강조 | 완료 · 40구간 (#197fb2). **수식 안에는 색이 없다** |
| 식 상호참조 | 완료 · 본문 참조 77곳 전부 실재하는 식 번호 |
| 위젯 12개 | 완료 · 헤드리스 조작(버튼 전부 클릭 + 슬라이더 min/mid/max) 시 오류 0 |
| 오타 수정 | 2곳 + 조판 대체 1곳 · 노트 맨 아래 표에 기록 |
| 원문 어긋남 | 3곳 발견 · **원문 그대로 두고** 수치 근거와 함께 부록에 기록 |
