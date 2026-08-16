# Notes on Quaternion kinematics for the error-state Kalman filter — 학습 목차

원문: Gyubeom Edward Im, *Notes on Quaternion kinematics for the error-state Kalman filter* (58쪽)
(Orig. by Joan Solà) · `ref/Notes on Quaternion kinematics for the error-state Kalman filter.pdf`
페이지 오프셋 0 · A4 판형

학습 목표: 쿼터니언의 대수적 정의에서 출발해 회전군 SO(3)와의 관계, 표기 규약, 섭동·자코비안·
수치적분을 거쳐 IMU 기반 ESKF를 지역 각 에러와 전역 각 에러 두 방식으로 끝까지 유도한다.

> **결과물은 챕터별 노트가 아니라 원문 전체를 그대로 옮긴 단일 문서다.**
> `notes/notes_on_quaternion_kinematics.md` 하나에 8개 장이 모두 들어 있고, 빌드하면 같은 폴더에
> `notes_on_quaternion_kinematics.html`이 나온다. 위젯 12개가 절 사이에 삽입되어 있다.

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 Quaternion Definition and properties | ✅ | — | 2 (해밀턴 곱, exp/log) |
| 2 Rotations and cross-relations | ✅ | 14 (p.10~28) | 5 (벡터 회전, 로드리게스, 이중 덮개, SLERP, 등각) |
| 3 Quaternion conventions. My choice | ✅ | — | — |
| 4 Perturbations, derivatives and integrals | ✅ | 3 (p.34, p.39×2) | 3 (오른쪽 자코비안, 지역/전역 섭동, 회전 적분) |
| 5 Error-state kinematics for IMU-driven systems | ✅ | 1 (p.43 테이블) | 1 (세 가지 상태) |
| 6 Fusing IMU with complementary sensory data | ✅ | — | — |
| 7 The ESKF using global angular errors | ✅ | 1 (p.57 테이블) | 1 (지역 vs 전역 ESKF) |
| 8 Revision log | ✅ | — | — |

**검증** — 수식 번호 (1)~(319) 누락·중복 없음 / 절 제목 99개 PDF 대조 완료 /
그림 19개 인라인 / 렌더링된 수식 `<mjx-container` 976개 / 위젯 12개 조작 테스트 `ERRS=0 BLANK=0 NaN=0`

---

## 1장. Quaternion Definition and properties (p.4)
- 1.1 Definition of quaternion (4)
  - 1.1.1 Alternative representations of the quaternion (4)
- 1.2 Main quaternion properties (5)
  - 1.2.1 Sum (5)
  - 1.2.2 Product (5)  ← **실험 1 해밀턴 곱**
  - 1.2.3 Identity (6)
  - 1.2.4 Conjugate (6)
  - 1.2.5 Norm (7)
  - 1.2.6 Inverse (7)
  - 1.2.7 Unit or normalized quaternion (7)
- 1.3 Additional quaternion properties (7)
  - 1.3.1 Quaternion commutator (7)
  - 1.3.2 Product of pure quaternions (7)
  - 1.3.3 Natural powers of pure quaternions (8)
  - 1.3.4 Exponential of pure quaternions (8)
  - 1.3.5 Exponential of general quaternions (9)
  - 1.3.6 Logarithm of unit quaternions (9)
  - 1.3.7 Logarithm of general quaternions (9)
  - 1.3.8 Exponential forms of the type qt (9)  ← **실험 2 exp/log**

## 2장. Rotations and cross-relations (p.10)
- 2.1 The 3D vector rotation formula (10)  ← **실험 3 벡터 회전 (3D)**
- 2.2 The rotation group SO(3) (11)
- 2.3 The rotation group and the rotation matrix (11)
  - 2.3.1 The exponential map (12)
  - 2.3.2 The capitalized exponential map (14)
  - 2.3.3 Rotation matrix and rotation vector: the Rodrigues rotation formula (14)  ← **실험 4 로드리게스 (3D)**
  - 2.3.4 The logarithm maps (15)
  - 2.3.5 The rotation action (15)
- 2.4 The rotation group and the quaternion (16)
  - 2.4.1 The exponential map (17)
  - 2.4.2 The capitalized exponential map (18)
  - 2.4.3 Quaternion and rotation vector (19)
  - 2.4.4 The logarithmic maps (19)
  - 2.4.5 The rotation action (19)
  - 2.4.6 The double cover of the manifold of SO(3) (20)  ← **실험 5 이중 덮개 (3D)**
- 2.5 Rotation matrix and quaternion (21)
- 2.6 Rotation composition (21)
- 2.7 Spherical linear interpolation (SLERP) (22)  ← **실험 6 SLERP (3D)**
- 2.8 Quaternion and isoclinic rotations: explaining the magic (25)  ← **실험 7 등각 회전**

## 3장. Quaternion conventions. My choice (p.28)
- 3.1 Quaternion flavors (28)
  - 3.1.1 Order of the quaternion components (29)
  - 3.1.2 Specification of the quaternion algebra (29)
  - 3.1.3 Function of the rotating operator (29)
  - 3.1.4 Direction of the rotation operator (30)

## 4장. Perturbations, derivatives and integrals (p.31)
- 4.1 The additive and subtractive operators in SO(3) (31)
- 4.2 The four possible derivative definitions (31)
  - 4.2.1 Functions from vector space to vector space (31)
  - 4.2.2 Functions from SO(3) to SO(3) (32)
  - 4.2.3 Functions from vector space to SO(3) (32)
  - 4.2.4 Functions from SO(3) to vector space (32)
- 4.3 Useful, and very useful, Jacobians of the rotation (32)
  - 4.3.1 Jacobian with respect to the vector (32)
  - 4.3.2 Jacobian with respect to the quaternion (33)
  - 4.3.3 Right Jacobian of SO(3) (33)  ← **실험 8 오른쪽 자코비안**
  - 4.3.4 Jacobian with respect to the rotation vector (35)
  - 4.3.5 Jacobians of the rotation composition (35)
- 4.4 Perturbations, uncertainties, noise (36)
  - 4.4.1 Local perturbations (36)
  - 4.4.2 Global perturbations (36)  ← **실험 9 지역/전역 섭동 (3D)**
- 4.5 Time derivatives (36)
  - 4.5.1 Global-to-local relations (37)
  - 4.5.2 Time-derivative of the quaternion product (38)
  - 4.5.3 Other useful expressions with the derivatives (38)
- 4.6 Time-integration of rotation rates (38)
  - 4.6.1 Zeroth order integration (39)
  - 4.6.2 First order integration (40)  ← **실험 10 회전 적분**

## 5장. Error-state kinematics for IMU-driven systems (p.41)
- 5.1 Motivation (41)
- 5.2 The error-state Kalman filter explained (42)
- 5.3 System kinematics in continuous time (42)
  - 5.3.1 The true-state kinematics (43)
  - 5.3.2 The nominal-state kinematics (44)
  - 5.3.3 The error-state kinematics (45)  ← **실험 11 세 가지 상태**
- 5.4 System kinematics in discrete time (47)
  - 5.4.1 The nominal state kinematics (47)
  - 5.4.2 The error-state kinematics (47)
  - 5.4.3 The error-state Jacobian and perturbation matrices (48)

## 6장. Fusing IMU with complementary sensory data (p.49)
- 6.1 Observation of the error state via filter correction (49)
  - 6.1.1 Jacobian computation for the filter correction (50)
- 6.2 Injection of the observed error into the nominal state (51)
- 6.3 ESKF reset (51)
  - 6.3.1 Jacobian of the reset operation with respect to the orientation error (52)

## 7장. The ESKF using global angular errors (p.53)
- 7.1 System kinematics in continuous time (53)
  - 7.1.1 The true- and nominal-state kinematics (53)
  - 7.1.2 The error-state kinematics (53)
- 7.2 System kinematics in discrete time (55)
  - 7.2.1 The nominal state (55)
  - 7.2.2 The error state (55)
  - 7.2.3 The error state Jacobian and perturbation matrices (55)
- 7.3 Fusing with complementary sensory data (56)
  - 7.3.1 Error state observation (56)
  - 7.3.2 Injection of the observed error into the nominal state (56)
  - 7.3.3 ESKF reset (57)  ← **실험 12 지역 vs 전역 ESKF**

## 8장. Revision log (p.58)
---

## 추천 학습 순서

원문 순서 그대로 읽되, 목적에 따라 건너뛸 수 있다.

1. **1~2장** — 쿼터니언 대수 → 회전. 이 문서의 8할이 여기 들어 있다.
   2.4(exp/log)와 2.8(등각 회전)이 "왜 반각인가", "왜 q ⊗ x ⊗ q\* 인가"에 답한다
2. **3장** — 규약. 짧지만 **가장 실용적인 장**이다. Hamilton vs JPL, 능동 vs 수동을
   여기서 정리해 두지 않으면 남의 코드와 부호가 안 맞는다
3. **4장** — 섭동과 자코비안. 4.3.3(오른쪽 자코비안)과 4.4(지역/전역 섭동)가 5~7장의 전제다
4. **5~6장** — IMU ESKF. 상태 정의(테이블 18) → 연속 시간 → 이산 시간 → 융합·주입·리셋
5. **7장** — 같은 필터를 전역 각 에러로. 바뀌는 곳이 테이블 19에 정리되어 있다

ESKF만 급하다면 **2.4 → 3장 → 4.4 → 5장 → 6장** 순으로 읽어도 된다.

## 참고 — 이 문서의 특이사항

- **번호 붙은 수식이 (1)~(319)까지** 있다. 노트가 이를 그대로 유지하므로 원문 PDF와 나란히 볼 수 있다
- **그림 19개 중 2개(Figure 18·19)는 실제로는 표**다. 원문 캡션이 그냥 `Table`이라 그대로 두었다
- 원문의 **오타 14곳과 수식 오기 3곳**을 고쳤다. 목록은 노트 맨 아래 "옮기며 바로잡은 것"에 있다
- **(305)가 (304)→(306) 사이에서 이어지지 않는다**(지역 좌표계 유도의 식이 남아 있다).
  판단할 수 없어 원문 그대로 두고 "원문 그대로 둔 것"에 적어 두었다
- 굵은 그리스 문자는 `\boldsymbol`이 아니라 **`\pmb`**로 조판했다 — 오프라인 MathJax 번들에
  `boldsymbol` 패키지가 없어 쓰면 문서 전체 수식이 죽는다 (`3_Pitfalls.md` B6)
