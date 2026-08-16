# 학습 범위 목차 — Formula Derivation and Analysis of the VINS-Mono

Edward Gyubeom Im, 22쪽 (원문: Yibin Wu, arXiv:1912.11986)
쪽번호는 원문 그대로다 (PDF 쪽 = 인쇄 쪽, 오프셋 0).

노트: [`notes/notes_on_vins_mono.md`](../notes/notes_on_vins_mono.md) →
`.html` (단일 파일 3.4MB, 오프라인으로 열림)

---

## 전체 구성

| 절 | 제목 | 쪽 | 식 | 그림 | 위젯 |
|---|---|---|---|---|---|
| 1 | Introduction | 1 | — | 1 | **실험 1** |
| 2 | Imu Preintegration | 2 | | | |
| 2.1 | IMU Preintegration in Continuous Time | 2 | (1)~(8) | 6 | **실험 2** |
| 2.2 | IMU Preintegration in Discrete Time | 7 | (9)(10) | 1 | **실험 3** |
| 2.3 | Error-state Kinematics in Continuous Time | 8 | (11)~(29) | 1 | **실험 4** |
| 2.4 | Error-state Kinematics in Discrete Time | 11 | (30)~(38) | | **실험 5** |
| 3 | Initialization | 13 | | 1 | |
| 3.1 | Vision-Only SfM in Sliding Window | 13 | — | | |
| 3.2 | Visual-Inertial Alignment | 13 | (39)~(47) | | **실험 6·7·8** |
| 4 | Tightly-Coupled Nonlinear Optimization | 15 | | | |
| 4.1 | Basic of the State Estimation | 15 | (48)~(57) | | **실험 9** |
| 4.2 | Cost Function | 16 | (58)(59) | | |
| 4.3 | IMU Model | 17 | (60)~(65) | | **실험 10** |
| 4.4 | Vision Model | 18 | (66)~(78) | | **실험 11** |
| 5 | Marginalization | 20 | (79)~(83) | | **실험 12** |
| 6 | Global Optimization in the VINS-Fusion | 21 | (84)~(88) | | |
| 7 | References | 22 | — | | |
| 8 | Revision log | 22 | — | | |

식 번호는 (1)~(88), 절은 18개, 그림은 10개다.

**3.2절은 소절 번호 대신 파란 강조로 네 단계를 나눈다** — 1) Gyroscope Bias Calibration,
2) Velocity, Gravity Vector, and Metric Scale Initialization, 3) Gravity Refinement,
4) Completing Initialization. 노트도 그대로 옮겼다.

---

## 위젯 12개

전부 **원문에 없는 추가 요소**라고 표시된 회색 박스 안에 들어 있다.
계산은 모두 `tools/widgets/_vm_helper.js` 의 `window.VM` 이 한다.

| # | 파일 | 붙는 곳 | 무엇을 보여주나 |
|---|---|---|---|
| 1 | `frames-and-notation` | 1장 끝 | 위/아래 첨자 규약과 $\Omega_L, \Omega_R$ 검산 |
| 2 | `alpha-beta-gamma` | 2.1 끝 | ★ $t_k$ 상태를 흔들어도 $\alpha,\beta,\gamma$ 가 안 변한다. (7) 좌변=우변 |
| 3 | `midpoint-vs-euler` | 2.2 끝 | ★ 식 (9)는 2차, (10)은 1차 — 기울기로 확인 |
| 4 | `error-state-continuous` | 2.3 끝 | ★ (23)의 $\mathbf{F}$ 를 (12)(13) 정의에서 수치미분과 대조 |
| 5 | `jacobian-covariance-propagation` | 2.4 끝 | ★ (27) $\mathbf{P}$ vs 몬테카를로 · (29)의 오차가 왜 $O(\delta\mathbf{b}\cdot\delta t)$ 인가 |
| 6 | `gyro-bias-calibration` | 3.2 1) 끝 | (39)(40)으로 $\mathbf{b}_g$ 를 실제로 찾는다 |
| 7 | `velocity-gravity-scale` | 3.2 2) 끝 | ★ (44) $\mathbf{Ax}=\mathbf{b}$ 를 세워 풀고 스케일 복원을 확인 |
| 8 | `gravity-refinement` | 3.2 3) 끝 | (47) 크기 고정 + 접평면 2자유도 |
| 9 | `quaternion-error-parameterization` | 4.1 끝 | ★ 4-파라미터로 풀면 $\|\mathbf{q}\|\to 0$ 으로 무너진다 |
| 10 | `imu-residual-vins` | 4.3 끝 | ★ (62)~(65) 자코비안 vs 수치미분 (15×30 히트맵) |
| 11 | `vision-residual-tangent` | 4.4 끝 | (69) 이미지 평면 vs (70) 접평면 — 광축에서 멀어질 때 |
| 12 | `marginalization-schur` | 5장 끝 | ★ Schur 는 같은 해, 그냥 버리면 틀어진다 + fill-in |

★ 는 **자기검산형** — 원문 식으로 구한 값과 독립적인 수치실험 값을 나란히 찍는다.

---

## 추천 읽기 순서

원문 순서대로 읽으면 되지만, 2장이 전체 분량의 절반이고 가장 빽빽하다.

1. **1장 NOMENCLATURE + 실험 1** — 첨자 규약과 $\Omega_L/\Omega_R$. 이걸 모르면 2장을 못 읽는다
2. **2.1 + 실험 2** — (5)에서 (7)로 넘어가는 이유. **이 노트에서 가장 중요한 대목**
3. **2.2 + 실험 3** — mid-point 를 쓰는 이유
4. **2.3 + 실험 4** — 에러 상태 방정식. (15)(17)의 유도를 손으로 따라가 볼 것
5. **2.4 + 실험 5** — (37)(38)은 외울 게 아니라 코드(`midPointIntegration()`)와 대조할 표다
6. **3장 + 실험 6·7·8** — 초기화. 순서(자이로 bias → 속도·중력·스케일 → 중력 정제)가 곧 알고리즘이다
7. **4.1 + 실험 9** — 왜 3자유도로 리프팅하는가. ceres LocalParameterization 의 근거
8. **4.3·4.4 + 실험 10·11** — 실제 구현에 바로 들어가는 residual 과 자코비안
9. **5장 + 실험 12** — marginalization. 6장은 VINS-Fusion 소개라 가볍게

## 진행 상황

| 항목 | 상태 |
|---|---|
| 전사 (1~8장) | 완료 · 식 (1)~(88) 누락·중복 없음 |
| 그림 10개 | 완료 · bbox 추출, 원문 자리에 배치 |
| 파란 강조 | 완료 · 원문 23구간(논리적으로 24개) |
| 수식 내 색 강조 | 완료 · 빨강 4 · 파랑 4 |
| 위젯 12개 | 완료 · 헤드리스 조작 시 오류 0 |
| 오타 수정 | 8곳 · 노트 맨 아래 표에 기록 |
