# 학습 범위 목차 — Notes on On-manifold preintegration for real-time visual-inertial odometry

Gyubeom Edward Im, 18쪽 (원논문: C. Forster et al., *IEEE T-RO* 33.1, 2016)
쪽번호는 원문 그대로다 (PDF 쪽 = 인쇄 쪽, 오프셋 0).

노트: [`notes/notes_on_preintegration.md`](../notes/notes_on_preintegration.md) →
`.html` (단일 파일 2.5MB, 오프라인으로 열림)

**원문에 제목만 있고 본문이 없는 절이 셋 있다** — 1장, 6장, A.4. 비운 것이 아니라 원문이 그렇다.

---

## 전체 구성

| 절 | 제목 | 쪽 | 식 | 위젯 |
|---|---|---|---|---|
| 1 | Introduction | 2 | — | |
| 2 | Preliminaries | 2 | | |
| 2.1 | Notions of Riemannian geometry | 2 | | |
| 2.1.1 | Special orthogonal group SO(3) | 2 | (1)~(12) | **실험 1** |
| 2.1.2 | Special euclidean group SE(3) | 3 | (13) | **실험 2** |
| 2.2 | Uncertainty description in SO(3) | 3 | (14)~(18) | **실험 3** |
| 2.3 | Gauss-Newton method on manifold | 4 | (19)~(23) | **실험 4** |
| 3 | Maximum a posteriori visual-inertial state estimation | 5 | | |
| 3.1 | The state | 5 | (24)(25) | |
| 3.2 | The measurements | 5 | (26) | |
| 3.3 | Factor graphs and MAP estimation | 6 | (27)(28) | **실험 5** |
| 4 | IMU model and motion integration | 6 | (29)~(35) | **실험 6** |
| 5 | IMU preintegration on manifold | 8 | (36)~(38) | **실험 7** |
| 5.1 | Preintegrated IMU measurements | 8 | (39)~(42) | |
| 5.2 | Noise propagation | 10 | (43)~(47) | **실험 8** |
| 5.3 | Incorporating bias updates | 11 | (48) | **실험 9** |
| 5.4 | Preintegrated IMU factors | 11 | (49) | **실험 10** |
| 5.5 | Bias model | 11 | (50)~(53) | |
| 6 | Structureless vision factor | 12 | — | |
| A | Appendix | 12 | | |
| A.1 | Iterative noise propagation | 12 | (54)~(58) | |
| A.2 | Bias correction via first-order updates | 13 | (59)~(66) | |
| A.3 | Jacobians of residual errors | 15 | (67) | |
| A.3.1 | Jacobians of $\mathbf{r}_{\Delta\mathbf{p}_{ij}}$ | 15 | (68)~(72) | |
| A.3.2 | Jacobians of $\mathbf{r}_{\Delta\mathbf{v}_{ij}}$ | 16 | (73)~(76) | |
| A.3.3 | Jacobians of $\mathbf{r}_{\Delta\mathbf{R}_{ij}}$ | 17 | (77)~(80) | **실험 11** |
| A.4 | Structureless vision factors: null space projection | 17 | — | |
| A.5 | Rotation rate integration using euler angles | 17 | (81)(82) | **실험 12** |
| B | References | 18 | — | |
| C | Revision log | 18 | — | |

식 번호는 (1)~(82), 절은 30개다.

---

## 위젯 12개

전부 **원문에 없는 추가 요소**라고 표시된 회색 박스 안에 들어 있다.
계산은 모두 `tools/widgets/_pi_helper.js` 의 `window.PI` 가 한다.

| # | 파일 | 붙는 곳 | 무엇을 보여주나 |
|---|---|---|---|
| 1 | `so3-exp-log-jacobian` | 2.1.1 끝 | Exp/Log 왕복, 식 (8)의 오차 기울기가 2 인 것, $\mathbf{J}_r$ 를 빼면 1 로 떨어지는 것 |
| 2 | `adjoint-identity` | 2.1.2 끝 | 식 (12) — 회전을 통과시키면 축이 돈다. (39)(62)(77)에서 계속 쓰는 도구 |
| 3 | `so3-uncertainty` | 2.2 끝 | 식 (14)~(18). 거리가 $\chi^2_3$ 인지, $\beta \approx \alpha$ 근사가 언제 깨지는지 |
| 4 | `manifold-gauss-newton` | 2.3 끝 | 회전 평균 문제로 lift-solve-retract 를 돌린다. 성분 평균은 SO(3) 밖으로 나간다 |
| 5 | `factor-graph` | 3.3 끝 | 식 (27)의 곱 구조. preintegration 이 미지수를 몇 배 줄이나 |
| 6 | `imu-integration` | 4장 끝 | 식 (34)를 굴린다. $\mathbf{b}^g$ 는 위치 오차에 $t^3$, $\mathbf{b}^a$ 는 $t^2$ 로 들어간다 |
| 7 | `preintegration-invariance` | 5장 끝 | ★ $\mathbf{R}_i,\mathbf{v}_i,\mathbf{p}_i$ 를 흔들어도 $\Delta$ 가 안 변한다. (37) 좌변=우변 |
| 8 | `noise-propagation` | 5.2 끝 | ★ 식 (58) 반복 전파 vs 몬테카를로 표본공분산 |
| 9 | `bias-first-order-update` | 5.3 끝 | ★ 식 (48) 1차 보정 vs 재적분. 오차가 $\|\delta\mathbf{b}\|^2$ 인 것 |
| 10 | `imu-residual` | 5.4 끝 | 식 (49). bias 를 흔들어도 residual 이 안 움직이는 이유 |
| 11 | `residual-jacobians` | A.3.3 끝 | ★ 식 (72)(76)(80) 해석 자코비안 vs 수치미분 (9×24 히트맵) |
| 12 | `euler-vs-so3` | A.5 끝 | 식 (81)(82). 짐벌락 근처에서 오일러 적분만 무너진다 |

★ 는 **자기검산형** — 원문 식으로 구한 값과 독립적인 수치실험 값을 나란히 찍는다.

---

## 추천 읽기 순서

원문 순서대로 읽으면 된다. 다만 5장이 핵심이고 나머지는 그 준비물이다.
시간이 없으면 이렇게 건너뛰어도 된다.

1. **2.1.1 + 실험 1·2** — Exp/Log/$\mathbf{J}_r$ 와 식 (12). 이 셋을 모르면 5장 유도를 못 따라간다
2. **4장 + 실험 6** — IMU 모델과 식 (34). 왜 bias 가 문제인지
3. **5장 도입 + 실험 7** — (36)에서 (37)로 넘어가는 이유. **이 노트에서 가장 중요한 대목**
4. **5.1** — 노이즈를 뒤로 미는 (39)~(42). 실험 1의 식 (8)이 여기서 쓰인다
5. **5.2 + A.1 + 실험 8** — 공분산. 5.2는 왜, A.1은 어떻게
6. **5.3 + A.2 + 실험 9** — bias 갱신. 5.3은 왜, A.2는 어떻게
7. **5.4 + A.3 + 실험 10·11** — residual 과 자코비안. 실제 구현에 바로 들어가는 부분
8. 2.2·2.3·3장·5.5·A.5 — 배경과 곁가지

## 진행 상황

| 항목 | 상태 |
|---|---|
| 전사 (1~6장, 부록 A~C) | 완료 · 식 (1)~(82) 누락·중복 없음 |
| 파란 강조 29곳 | 완료 · 원문 개수와 일치 |
| 진홍 수식 강조 57곳 | 완료 · 원문 개수와 일치 |
| 위젯 12개 | 완료 · 헤드리스 조작 시 오류 0 |
| 오타 수정 | 6곳 · 노트 맨 아래 표에 기록 |
