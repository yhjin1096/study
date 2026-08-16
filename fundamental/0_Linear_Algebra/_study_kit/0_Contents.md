# Notes on Linear Algebra — 학습 목차

원문: Gyubeom Edward Im, *Notes on Linear Algebra* (51쪽)
`ref/Notes on Linear Algebra.pdf` · 페이지 오프셋 0 · A4 판형 (목차 p1~4, 본문 p5~51)

학습 목표: 선형시스템과 Span에서 출발해 최소제곱·고유값분해·SVD를 지나
행렬 분해와 유사역행렬, Woodbury/RLS까지 &mdash; SLAM 최적화에 필요한 선형대수 도구를 한 바퀴 돈다.

> **결과물은 챕터별 노트가 아니라 원문 전체를 그대로 옮긴 단일 문서다.**
> `notes/notes_on_linear_algebra.md` 하나에 9개 장이 모두 들어 있고, 빌드하면 같은 폴더에
> `notes_on_linear_algebra.html`이 나온다. 위젯 14개가 절 사이에 삽입되어 있다.

## 진행 상황

| 장 | 노트 | 식 | 그림 | 위젯 |
|---|---|---|---|---|
| 1 Linear systems | ✅ | (1)~(41) | 8 | 3 (행/열 그림, Span, 네 부분공간) |
| 2 Least squares | ✅ | (42)~(73) | 6 | 3 (정규방정식, 정사영, Gram-Schmidt) |
| 3 Eigenvectors and eigenvalues | ✅ | (74)~(91) | 2 | 1 (A = VDV⁻¹) |
| 4 Singular value decomposition | ✅ | (92)~(105) | 1 | 2 (SVD 기하, rank-k 근사) |
| 5 Derivatives of multivariable functions | ✅ | (106)~(124) | — | 1 (∇f 와 H) |
| 6 Matrix algebra | ✅ | (125)~(158) | 1 | 1 (det 와 PD) |
| 7 Matrix decompositions | ✅ | (159)~(235) | 1 | 3 (분해 비교, A†, RLS) |
| 8 Reference / 9 Revision log | ✅ | — | — | — |

**검증** — 수식 번호 (1)~(235) 누락·중복 없음 · 순서 일치 / 절 제목 129개 PDF 대조 완료 /
그림 19개 인라인 / 렌더링된 수식 `<mjx-container` 1,096개 / 파란 강조 113곳 재현 /
위젯 14개 조작 테스트 `ERRS=0 BLANK=0 NaN=0`

---

## 1장. Linear systems (p.5)
- 1.1 Linear equation (5)
- 1.2 Linear system (5)
- 1.3 Homogeneous equation (5)
- 1.4 Over-determined system (6)
- 1.5 Under-determined system (6)
- 1.6 Solving linear system (7)  ← **실험 1 행 그림·열 그림**
- 1.7 Linear combination (7)
- 1.8 Span (7)
- 1.9 From matrix equation to vector equation (7)
- 1.10 Several perspectives about matrix multiplication (8)
- 1.11 Linear independence (8)
- 1.12 Linear dependence (9)  ← **실험 2 Span 과 선형독립 (3D)**
- 1.13 Vector space and subspace (9)
- 1.14 Span and subspace (10)
- 1.15 Basis of a subspace (10)
- 1.16 Dimension of subspace (11)
- 1.17 Column space of matrix (11)
- 1.18 Four fundamental subspaces of a matrix (11)
- 1.19 Rank of matrix (11)
- 1.20 Dimensions, orthogonality, and solvability (12)  ← **실험 3 네 부분공간 (3D)**
- 1.21 Transformation (13)
- 1.22 Linear transformation (13)
- 1.23 Transformations between vectors (13)
- 1.24 Matrix of linear transformation (13)
- 1.25 Onto and one-to-one (14)

## 2장. Least squares (p.14)
- 2.1 Inner product (14)
- 2.2 Properties of inner product (14)
- 2.3 Vector norm (15)
- 2.4 Unit vector (15)
- 2.5 Distance between vectors in $\mathbb{R}^n$ (15)
- 2.6 Inner product and angle between vectors (15)
- 2.7 Orthogonal vectors (16)
- 2.8 Least square problem (16)
- 2.9 Normal equation (17)
- 2.10 Another derivation of normal equation (17)
- 2.11 What if C = A⊺A is NOT invertible? (17)
- 2.12 Orthogonal projection perspective (17)
- 2.13 Projection matrix P (17)
  - 2.13.1 Projection matrix for under-determined system (18)
  - 2.13.2 Projection matrix and nullspace (18)  ← **실험 4 정규방정식**
- 2.14 Orthogonal and orthonormal sets (19)
- 2.15 Orthogonal and orthonormal basis (19)
- 2.16 Orthogonal projection ŷ of y onto line (20)
- 2.17 Orthogonal projection ŷ of y onto plane (20)
- 2.18 Orthogonal projection when y ∈ W (20)
- 2.19 Transformation: orthogonal projection (21)
- 2.20 Orthogonal projection perspective (21)  ← **실험 5 정사영 (3D)**
- 2.21 Gram-Schmidt orthogonalization (21)  ← **실험 6 Gram-Schmidt (3D)**

## 3장. Eigenvectors and eigenvalues (p.22)
- 3.1 Null space (22)
- 3.2 Orthogonal complement (23)
- 3.3 Characteristic equation (23)
- 3.4 Eigenspace (23)
- 3.5 Diagonalization (23)
- 3.6 Finding V and D (24)
- 3.7 Eigendecomposition (24)
- 3.8 Linear transformation via eigendecomposition (24)
- 3.9 Change of basis (25)
- 3.10 Element-wise scaling (25)
- 3.11 Back to original basis (25)
- 3.12 Linear transformation via $\mathbf{A}^k$ (25)
- 3.13 Geometric multiplicity and algebraic multiplicity (25)  ← **실험 7 A = VDV⁻¹**

## 4장. Singular value decomposition (p.26)
- 4.1 SVD as sum of outer products (26)
- 4.2 Another perspective of SVD (26)
- 4.3 Computing SVD (27)  ← **실험 8 SVD 의 기하**
- 4.4 Diagonalization of symmetric matrices (27)
- 4.5 Spectral theorem of symmetric matrices (27)
- 4.6 Spectral decomposition (27)
- 4.7 Symmetric positive definite matrices (28)
- 4.8 Back to computing SVD (28)
- 4.9 Eigendecomposition in machine learning (28)
- 4.10 Low rank approximation of a matrix (29)
- 4.11 Dimension reducing transformation (29)  ← **실험 9 rank-k 근사**

## 5장. Derivatives of multivariable functions (p.29)
- 5.1 Gradient (29)
- 5.2 Jacobian matrix (29)
  - 5.2.1 Toy example 1 (30)
  - 5.2.2 Toy example 2 (30)
- 5.3 Hessian matrix (31)
- 5.4 Laplacian (31)
- 5.5 Taylor expansion (32)  ← **실험 10 ∇f 와 H**

## 6장. Matrix algebra (p.32)
- 6.1 Identity matrix (32)
- 6.2 Transpose of matrix (32)
- 6.3 Determinant of matrix (32)
  - 6.3.1 Determinant of block triangle matrix (33)
- 6.4 Inverse matrix (33)
- 6.5 Trace of matrix (34)
- 6.6 Diagonal matrix (34)
- 6.7 Idempotent matrix (35)
- 6.8 Skew-symmetric matrix (35)
- 6.9 Positive definite matrix (36)  ← **실험 11 det 와 PD**
- 6.10 Toeplitz matrix (37)

## 7장. Matrix decompositions (p.38)
- 7.1 LU decomposition (38)
  - 7.1.1 PLU decomposition (38)
  - 7.1.2 LDU decomposition (38)
- 7.2 Cholesky decomposition (39)
  - 7.2.1 Detailed explanation (39)
- 7.3 LDLT decomposition (39)
- 7.4 QR decomposition (40)
  - 7.4.1 Detailed explanation (40)
  - 7.4.2 QR decomposition on least squares problem (41)
- 7.5 Eigen decomposition (41)  ← **실험 12 분해 7종 비교**
- 7.6 Singular value decomposition (42)
  - 7.6.1 Computing SVD (42)
  - 7.6.2 Range and nullspace of SVD (42)
  - 7.6.3 SVD on under-determined system (43)
  - 7.6.4 SVD on over-determined system (43)
- 7.7 Pseudo inverse (43)
  - 7.7.1 Pseudo inverse on under-determined system (full row rank) (43)
  - 7.7.2 Pseudo inverse on over-determined system (full column rank) (44)
  - 7.7.3 Moore–Penrose pseudo inverse (44)
  - 7.7.4 Full column rank case (45)
  - 7.7.5 Full row rank case (45)
  - 7.7.6 Rank deficient case (46)
  - 7.7.7 QR decomposition of pseudo inverse when singular case (47)  ← **실험 13 A†**
- 7.8 Woodbury’s identity (47)
  - 7.8.1 Recursive least squares (47)
- 7.9 Matrix inversion lemma (48)
  - 7.9.1 Derivation of matrix inversion lemma (49)
  - 7.9.2 LDU decomposition (49)
  - 7.9.3 UDL decomposition (49)
  - 7.9.4 Back to matrix inversion lemma (50)  ← **실험 14 RLS**

## 8장. Reference (p.50)

## 9장. Revision log (p.50)
---

## 추천 학습 순서

원문 순서 그대로 읽으면 된다. 절이 129개지만 대부분 한두 문단짜리라 흐름이 끊기지 않는다.

1. **1장** — 이 문서의 뼈대다. 1.9~1.12(선형결합·Span·독립)와 **1.18~1.20(네 부분공간)**만
   확실히 잡으면 나머지 장이 전부 그 위에 얹힌다
2. **2장** — 최소제곱. 2.8~2.13이 핵심이고, 2.13.1~2.13.2(사영행렬과 nullspace)는 저자가 최근에
   보강한 부분이라 7.7의 유사역행렬과 바로 이어진다
3. **3~4장** — 고유값분해 → SVD. 4.8의 "**SVD는 언제나 존재한다**"가 두 장을 가르는 결론이다
4. **5장** — 그레디언트·자코비안·헤시안. 짧지만 SLAM 최적화의 표기가 전부 여기서 정해진다
5. **6장** — 행렬 도구 상자. 필요할 때 찾아보는 장이다
6. **7장** — 분해와 유사역행렬. 7.7(A†)과 7.8~7.9(Woodbury / matrix inversion lemma)가
   칼만 필터 유도로 이어진다

최소제곱과 SLAM 최적화만 급하다면 **1.18~1.20 → 2.8~2.13 → 4.1~4.3 → 7.6~7.9** 로도 읽을 수 있다.

## 참고 — 이 문서의 특이사항

- **절이 129개로 네 스터디 중 가장 많다** (확률론 86 · 칼만 63 · 쿼터니언 99 · Lie Theory 36)
- **캡션이 하나도 없다** (`Figure`/`Table`이 전문에 0회). `extract_figures.py` 대신
  `tools/extract_images_bbox.py`(이미지 bbox 기반)로 19개를 뽑는다 — `3_Pitfalls.md` A10
- 번호 붙은 수식이 (1)~(235)까지 있다. 노트가 이를 그대로 유지하므로 원문 PDF와 나란히 볼 수 있다
- **파란 강조가 113곳**으로 매우 많다. 전부 재현했다 — 색이 수식 안이 아니라 산문에 쓰였고,
  MathJax SVG가 `currentColor`를 상속하므로 강조 안의 인라인 수식도 함께 물든다
- 원문의 **오타 10곳**을 고쳤고, 앞뒤와 어긋나 보이지만 손대지 않은 곳 7가지를 따로 적어 두었다.
  목록은 노트 맨 아래 "옮기며 바로잡은 것"에 있다
- 위젯의 수치는 전부 이 스터디에서 새로 만든 `window.LA` 헬퍼가 계산한다. 헬퍼 자체를
  항등식으로 먼저 검산한 표는 `README.md` 에 있다
