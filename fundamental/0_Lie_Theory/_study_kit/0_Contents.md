# Notes on Lie Theory — 학습 목차

원문: Gyubeom Edward Im, *Notes on Lie Theory* (26쪽)
`ref/Notes on Lie Theory.pdf` · 페이지 오프셋 0 · A4 판형

학습 목표: 군의 정의에서 출발해 Lie Group / Lie Algebra / 접평면의 관계를 잡고,
SO(3)와 SE(3)의 Exp·Log·Adjoint·좌우 자코비안을 유도까지 따라간 뒤,
그것으로 on-manifold EKF와 Pose Graph SLAM을 세우는 데까지 간다.

> **결과물은 챕터별 노트가 아니라 원문 전체를 그대로 옮긴 단일 문서다.**
> `notes/notes_on_lie_theory.md` 하나에 8개 장이 모두 들어 있고, 빌드하면 같은 폴더에
> `notes_on_lie_theory.html`이 나온다. 위젯 11개가 절 사이에 삽입되어 있다.

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 Introduction | ✅ | — | — |
| 2 Group Theory | ✅ | 13 (p.3~9) | 4 (접평면, ⊕/⊖, 자코비안, 공분산) |
| 3 SO(3) Group | ✅ | 6 (p.9~15) | 3 (Exp/Log, Adjoint, Jl·Jr) |
| 4 SE(3) Group | ✅ | 5 (p.16~20) | 2 (나사 운동, Ad와 𝒥) |
| 5 Applications for estimation | ✅ | 4 (p.23~25) | 1 (on-manifold EKF) |
| 6 Lie theory-based optimization on SLAM | ✅ | 1 (p.25) | 1 (Pose Graph GN) |
| 7 Reference / 8 Revision log | ✅ | — | — |

**검증** — 수식 번호 (1)~(91) 누락·중복 없음 · 순서 일치 / 절 제목 36개 PDF 대조 완료 /
그림 29개 인라인 / 렌더링된 수식 `<mjx-container` 376개 /
위젯 11개 조작 테스트 `ERRS=0 BLANK=0 NaN=0` / 파란 강조 12곳 · Tip 박스 1개 재현

---

## 1장. Introduction (p.3)

## 2장. Group Theory (p.3)
- 2.1 Lie Group (3)
- 2.2 Manifold (4)
- 2.3 Group Action (4)
- 2.4 Topology of Lie Theory (5)  ← **실험 1 매니폴드와 접평면 (3D)**
- 2.5 Plus and Minus Operators of Lie Group (5)  ← **실험 2 ⊕ / ⊖ (3D)**
- 2.6 Tangent Space and Lie Algebra (7)
- 2.7 Calculus on Lie Group (7)
- 2.8 Jacobians on Lie Group (8)  ← **실험 3 Lie Group 자코비안**
- 2.9 Perturbations on Lie Group (8)  ← **실험 4 섭동과 공분산 (3D)**

## 3장. SO(3) Group (p.9)
- 3.1 Lie Group SO(3) (9)
  - 3.1.1 SO(3) group properties (9)
- 3.2 Lie Algebra so(3) (10)
- 3.3 Exponential Mapping and Logarithm Mapping (10)  ← **실험 5 Exp / Log**
- 3.4 Derivation of Exponential Mapping (12)
- 3.5 Plus and Minus Operator of SO(3) (14)
- 3.6 Adjoint Matrix of SO(3) (15)  ← **실험 6 Adjoint (3D)**
- 3.7 Left and Right Jacobian of SO(3) (15)  ← **실험 7 Jl 과 Jr**

## 4장. SE(3) Group (p.16)
- 4.1 Lie Group SE(3) (16)
  - 4.1.1 SE(3) group properties (17)
- 4.2 Lie Algebra se(3) (17)
- 4.3 Exponential Mapping and Logarithm Mapping (18)  ← **실험 8 SE(3) 나사 운동 (3D)**
- 4.4 Plus and Minus Operator of SE(3) (20)
- 4.5 Adjoint Matrix of SE(3) (20)
- 4.6 Left and Right Jacobian of SE(3) (21)  ← **실험 9 Ad 와 𝒥**

## 5장. Applications for estimation (p.22)
- 5.1 EKF map-based localization (23)  ← **실험 10 on-manifold EKF**
  - 5.1.1 Prediction Step (23)
  - 5.1.2 Correction Step (24)
- 5.2 Pose Graph SLAM (24)

## 6장. Lie theory-based optimization on SLAM (p.25)  ← **실험 11 Pose Graph GN**

## 7장. Reference (p.26)

## 8장. Revision log (p.26)
---

## 추천 학습 순서

원문 순서 그대로 읽으면 된다. 26쪽이라 한 번에 통독할 수 있는 분량이다.

1. **2장** — 이 문서의 뼈대다. 2.4(접평면)에서 그림 한 장으로 전체 구도를 잡고,
   2.5(⊕/⊖) → 2.8(자코비안) → 2.9(공분산)로 **"매니폴드 위에서 미분하고 확률을 다루는 법"**을 익힌다
2. **3장** — 2장의 추상적인 이야기를 SO(3)에서 구체화한다. 3.4는 지수 매핑이 어디서 나오는지의
   유도이므로 급하면 건너뛰어도 3.5~3.7로 이어진다
3. **4장** — 같은 것을 SE(3)로. **4.3의 `t = J_l·v`** 하나만 확실히 잡으면 나머지는 SO(3)와 같은 골격이다
4. **5~6장** — 앞의 도구로 EKF와 Pose Graph를 세운다. 6장의 결론(**제약조건 없는 최적화**)이
   문서 전체의 목적지다

SLAM 최적화만 급하다면 **2.5 → 2.8 → 4.3 → 6장** 순으로 읽어도 된다.

## 참고 — 이 문서의 특이사항

- **26쪽에 그림이 29개다.** 개념을 그림으로 설명하는 성격의 문서다
- **캡션이 하나도 없다** (`Figure`/`Table`이 전문에 0회). `extract_figures.py` 대신
  `tools/extract_images_bbox.py`(이미지 bbox 기반)로 29개를 뽑는다 — `3_Pitfalls.md` A10
- 번호 붙은 수식이 (1)~(91)까지 있다. 노트가 이를 그대로 유지하므로 원문 PDF와 나란히 볼 수 있다
- **원문의 파란 강조(#197fb2)를 재현했다** — 앞의 세 스터디와 달리 색이 수식이 아니라 산문에
  쓰였기 때문이다. 마크다운에서 `==강조==`로 쓰면 `<span class="hl">`이 된다.
  MathJax SVG는 `currentColor`를 상속하므로 강조 구간 안의 인라인 수식도 함께 물든다
- **식 (75)·(77)의 블록 배치가 식 (55)의 성분 순서와 어긋난다.** 실험 9가 두 배치를 나란히 돌려
  수치로 보여 준다. 노트 맨 아래 "원문 그대로 둔 것" 참조
- 원문의 **오타 4곳**을 고쳤다. 목록은 노트 맨 아래 "옮기며 바로잡은 것"에 있다
