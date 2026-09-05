# Notation — 표기 기준

> **원문 범위**: 책 p.xiv~xv (Notation). 유형 D (참조형).
> **먼저 필요한 것**: 없다. 이 노트가 출발점이다.
> **나중에 쓰이는 곳**: 전 챕터.
> **성격**: 한 번 읽고 끝내는 노트가 아니다. **챕터를 진행하며 계속 덧붙인다.**

## 왜 이 노트를 먼저 만드는가

이 책은 **저자가 70명**이다. 편집자들이 서문에서 "하나로 이어지는 문서를 만들려
했고 70명이 동시에 쓰는 일은 꽤 어려웠다"고 밝혔다 (책 p.xii). 실제로 표기가
장마다 흔들리는 곳이 있다.

책 앞머리의 Notation 표는 **편집자가 정한 기준선**이다. 이것을 먼저 붙잡아 두면,
어떤 장에서 다른 표기가 나왔을 때 "내가 잘못 읽었나"가 아니라 "여기는 기준과
다르구나"로 판단할 수 있다.

그래서 이 노트는 두 부분이다.

1. **기준** — 책 p.xiv~xv 를 그대로 옮긴 것. 고치지 않는다
2. **관측 기록** — 챕터를 읽으며 마주친 실제 표기. 기준과 어긋나면 여기 적는다

---

## 1. General Notation (책 p.xiv)

### 1.1 글꼴로 종류를 구분한다

이 책에서 **글꼴 자체가 정보**다. 같은 글자 `a` 라도 굵기와 서체로 종류가 갈린다.

| 표기 | 뜻 | LaTeX |
|---|---|---|
| $a$ | 실수 스칼라 (real scalar) | `a` |
| $\boldsymbol{a}$ | 실수 열벡터 (column vector) — 굵은 소문자 | `\boldsymbol{a}` |
| $\boldsymbol{A}$ | 실수 행렬 (matrix) — 굵은 대문자 | `\boldsymbol{A}` |
| $\mathsf{A}$ | 집합 (set) — sans-serif 대문자 | `\mathsf{A}` |

> **읽을 때 주의.** 행렬 $\boldsymbol{A}$ 와 집합 $\mathsf{A}$ 는 인쇄물에서 구분이
> 미묘하다. 문맥이 애매하면 그 기호가 어디서 정의됐는지로 판단한다.
> 이 노트에서는 집합을 `\mathsf{}` 로 일관되게 쓴다.

### 1.2 기본 기호

| 표기 | 뜻 |
|---|---|
| $\boldsymbol{I}$ | 항등행렬 (identity matrix) |
| $\boldsymbol{0}$ | 영행렬 (zero matrix) |
| $\boldsymbol{A}^\mathsf{T}$ | 행렬 $\boldsymbol{A}$ 의 transpose |
| $\mathbb{R}^{M \times N}$ | 실수 $M \times N$ 행렬들의 벡터공간 |

### 1.3 확률

| 표기 | 뜻 |
|---|---|
| $p(\boldsymbol{a})$ | $\boldsymbol{a}$ 의 확률밀도 |
| $p(\boldsymbol{a} \mid \boldsymbol{b})$ | $\boldsymbol{b}$ 가 주어졌을 때 $\boldsymbol{a}$ 의 확률밀도 |
| $p(\boldsymbol{a}; \boldsymbol{b})$ | $\boldsymbol{b}$ 로 **parametrize 된** $\boldsymbol{a}$ 의 확률밀도 |
| $\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ | 평균 $\boldsymbol{\mu}$, 공분산 $\boldsymbol{\Sigma}$ 인 Gaussian 확률밀도 |
| $\mathcal{GP}(\boldsymbol{\mu}(t), \mathcal{K}(t,t'))$ | 평균함수 $\boldsymbol{\mu}(t)$, 공분산함수 $\mathcal{K}(t,t')$ 인 Gaussian process |

> **세미콜론과 세로줄의 차이는 사소하지 않다.** $p(\boldsymbol{a} \mid \boldsymbol{b})$ 는
> $\boldsymbol{b}$ 도 **확률변수**이고 그 값이 관측됐다는 뜻이다. 반면
> $p(\boldsymbol{a}; \boldsymbol{b})$ 의 $\boldsymbol{b}$ 는 확률변수가 아니라
> **고정된 파라미터**다. 분포 자체가 $\boldsymbol{b}$ 에 따라 달라지지만
> $\boldsymbol{b}$ 에 대한 확률은 논하지 않는다.
>
> 이 구분은 나중에 실제로 걸린다 — MAP 은 prior $p(\boldsymbol{X})$ 를 두므로 상태가
> 확률변수지만, MLE 는 상태를 파라미터로 본다. 자세한 것은 [[map-estimation]].
>
> $\mathcal{GP}$ 는 2장(연속시간 궤적)에서 본격적으로 쓰인다.

### 1.4 추정량 위의 장식 — hat 과 check

| 표기 | 뜻 | 읽는 법 |
|---|---|---|
| $\hat{(\cdot)}$ | **posterior** (추정된) 값 | hat |
| $\check{(\cdot)}$ | **prior** 값 | check |

> **이 책 특유의 표기다.** 많은 문헌이 prior 를 위첨자 마이너스($\hat{x}^-$)나
> 아래첨자 $k|k-1$ 로 쓰는데, 이 책은 **check** 를 쓴다.
> Barfoot 의 *State Estimation for Robotics* 계열 표기다.
>
> 짝으로 외우면 헷갈리지 않는다 — **check 로 시작해서 측정을 반영하면 hat 이 된다.**
>
> ```
> ǎ  (prior, 측정 전)   →   â  (posterior, 측정 후)
> ```

### 1.5 시간 첨자

| 표기 | 뜻 |
|---|---|
| $(\cdot)_k$ | timestep $k$ 에서의 값 |
| $(\cdot)_{k_1 : k_2}$ | timestep $k_1$ 부터 $k_2$ 까지의 값 **전체 집합** (양 끝 포함) |

$(\cdot)_{k_1:k_2}$ 가 값 하나가 아니라 **집합**이라는 점이 중요하다. SLAM 은 궤적
전체를 한꺼번에 추정하므로(smoothing) 이 표기가 자주 나온다. 예를 들어
$\boldsymbol{x}_{0:K}$ 는 처음부터 끝까지의 pose 전부다.

### 1.6 노름

| 표기 | 정의 |
|---|---|
| $\|\boldsymbol{x}\|_1$ | $\sum_i \lvert x_i \rvert$ |
| $\|\boldsymbol{x}\|_2$ | $\sqrt{\sum_i x_i^2}$ |

> 책의 Notation 표에는 없지만 본문에서 **Mahalanobis 노름** $\|\boldsymbol{e}\|_{\boldsymbol{\Sigma}}^2 = \boldsymbol{e}^\mathsf{T} \boldsymbol{\Sigma}^{-1} \boldsymbol{e}$ 가
> 아래첨자로 공분산을 달고 곧바로 등장한다 (1장 식 (1.17)·(1.18), 책 p.29). 그때 다시 짚는다.

---

## 2. 3D Geometry Notation (책 p.xv)

여기가 **이 책에서 가장 많이 틀리는 곳**이다. 첨자의 위·아래가 각각 다른 뜻을 갖는데,
한 번 뒤집어 읽으면 그 뒤 유도가 전부 어긋난다.

### 2.1 기준 규칙 — 위는 "어느 좌표계에서 본 것인가"

| 표기 | 뜻 |
|---|---|
| $\mathcal{F}^a$ | 3차원 **reference frame** (좌표계) |
| $\boldsymbol{v}^a$ | 벡터를 $\mathcal{F}^a$ **에서 본** 좌표 |

**위첨자 = 그 값을 표현하는 좌표계.** 벡터 $\boldsymbol{v}$ 자체는 하나지만
어느 frame 에서 보느냐에 따라 숫자가 달라진다 — 그 "어디서"가 위첨자다.

### 2.2 회전과 이동

| 표기 | 뜻 |
|---|---|
| $\boldsymbol{R}_a^b$ | $3\times3$ **rotation matrix** ($SO(3)$ 의 원소). $\mathcal{F}^a$ 에서 표현된 점을 (순수 회전된) $\mathcal{F}^b$ 표현으로 바꾼다 |
| $\boldsymbol{t}_a^b$ | $\mathcal{F}^a$ **원점의 3차원 위치**를 $\mathcal{F}^b$ 에서 표현한 것 |

$$\boldsymbol{v}^b = \boldsymbol{R}_a^b\, \boldsymbol{v}^a$$

> **첨자 읽는 법.** $\boldsymbol{R}_a^b$ 는 "**아래 $a$ 에서 위 $b$ 로**"다.
> 식에서 확인할 수 있다 — 오른쪽에 붙는 것이 $\boldsymbol{v}^a$ (아래첨자와 일치)이고,
> 결과가 $\boldsymbol{v}^b$ (위첨자와 일치)다.
>
> **아래첨자가 입력, 위첨자가 출력.** 곱할 때 안쪽 첨자가 맞물려 지워진다고 보면 된다.
>
> $$\boldsymbol{R}_a^c = \boldsymbol{R}_b^c\, \boldsymbol{R}_a^b$$
>
> $b$ 가 가운데서 만나 사라진다. 순서를 반대로 쓰면 틀린다.
>
> ⚠️ **$\boldsymbol{t}_a^b$ 만 결이 다르다.** 이건 변환이 아니라 **위치**다.
> "$\mathcal{F}^a$ 의 원점이 $\mathcal{F}^b$ 에서 어디에 있나"이므로,
> 아래첨자가 *무엇의* 위치인지를, 위첨자가 *어느 좌표계에서 본* 것인지를 말한다.

### 2.3 동차좌표와 SE(3)

| 표기 | 정의 |
|---|---|
| $\tilde{\boldsymbol{v}}^a$ | $4\times1$ **homogeneous point**, $\tilde{\boldsymbol{v}}^a = \begin{bmatrix} \boldsymbol{v}^a \\ 1\end{bmatrix}$ |
| $\boldsymbol{T}_a^b$ | $4\times4$ **transformation matrix** ($SE(3)$ 의 원소) |

$$\boldsymbol{T}_a^b = \begin{bmatrix} \boldsymbol{R}_a^b & \boldsymbol{t}_a^b \\ \boldsymbol{0} & 1 \end{bmatrix},
\qquad \tilde{\boldsymbol{v}}^b = \boldsymbol{T}_a^b\, \tilde{\boldsymbol{v}}^a$$

> **왜 4차원으로 늘리는가.** 회전은 행렬 곱으로 되지만 이동은 덧셈이라
> ($\boldsymbol{v}^b = \boldsymbol{R}_a^b \boldsymbol{v}^a + \boldsymbol{t}_a^b$)
> 둘을 한 번에 다룰 수 없다. 좌표 끝에 1 을 붙이면 **덧셈이 행렬 곱 안으로 들어온다.**
> 마지막 행 $\begin{bmatrix}\boldsymbol{0} & 1\end{bmatrix}$ 이 그 1 을 그대로 통과시켜
> 다음 변환에서도 같은 수법을 쓸 수 있게 한다.
>
> 직접 곱해서 확인해 보라 — 아래 3.1 의 연습문제다.

### 2.4 Lie group

| 표기 | 뜻 |
|---|---|
| $SO(3)$ | **special orthogonal group** — 3D 회전을 표현하는 matrix Lie group |
| $\mathfrak{so}(3)$ | $SO(3)$ 에 대응하는 **Lie algebra** |
| $SE(3)$ | **special Euclidean group** — 3D pose 를 표현하는 matrix Lie group |
| $\mathfrak{se}(3)$ | $SE(3)$ 에 대응하는 Lie algebra |

**대문자는 group, 소문자(fraktur)는 algebra** 라는 것만 지금 기억하면 된다.
왜 이런 것이 필요한지는 **2장 Optimization on Manifolds** 가 통째로 다룬다.
지금 단계에서는 "회전을 그냥 벡터처럼 더할 수 없어서 별도 장치가 필요하다"
정도로 충분하다.

### 2.5 hat 과 vee 연산자

| 표기 | 뜻 |
|---|---|
| $(\cdot)^\wedge$ | $\mathbb{R}^3$ (또는 $\mathbb{R}^6$) 의 벡터 → 3D 회전(또는 pose)의 Lie algebra 원소 |
| $(\cdot)^\vee$ | 그 반대 방향 |

$\wedge$ 는 3차원에서 **외적을 구현한다.** 두 벡터 $\boldsymbol{u}, \boldsymbol{v} \in \mathbb{R}^3$ 에 대해

$$\boldsymbol{u}^\wedge \boldsymbol{v} = \boldsymbol{u} \times \boldsymbol{v}$$

> **구체적으로 무슨 행렬인가.** 책은 여기서 형태를 주지 않지만, 위 등식이 성립하려면
> 답은 하나뿐이다 — skew-symmetric 행렬이다.
>
> $$\boldsymbol{u}^\wedge = \begin{bmatrix} 0 & -u_3 & u_2 \\ u_3 & 0 & -u_1 \\ -u_2 & u_1 & 0 \end{bmatrix}$$
>
> $\vee$ 는 이 행렬에서 $(u_1, u_2, u_3)$ 를 도로 꺼낸다. 확인은 3.2 의 연습문제.
>
> ⚠️ **표기 충돌 주의.** 위에서 본 $\hat{(\cdot)}$ (posterior) 와 이 $(\cdot)^\wedge$ 는
> **둘 다 "hat" 이라 부르지만 완전히 다른 것**이다. 앞은 글자 **위**에 얹히고,
> 뒤는 **위첨자 자리**에 온다. $\hat{\boldsymbol{x}}$ 와 $\boldsymbol{x}^\wedge$ 를
> 눈으로 구분하는 습관을 지금 들여 두는 편이 낫다.

---

## 3. 예제/실습

### 3.1 동차변환이 정말 회전 + 이동인가

$\boldsymbol{T}_a^b \tilde{\boldsymbol{v}}^a$ 를 블록 곱으로 직접 전개해서,
$\boldsymbol{v}^b = \boldsymbol{R}_a^b \boldsymbol{v}^a + \boldsymbol{t}_a^b$ 가 나오는지 확인하라.

**풀이.** 블록 행렬 곱을 그대로 쓴다.

$$\boldsymbol{T}_a^b \tilde{\boldsymbol{v}}^a
= \begin{bmatrix} \boldsymbol{R}_a^b & \boldsymbol{t}_a^b \\ \boldsymbol{0}^\mathsf{T} & 1 \end{bmatrix}
  \begin{bmatrix} \boldsymbol{v}^a \\ 1 \end{bmatrix}
= \begin{bmatrix} \boldsymbol{R}_a^b \boldsymbol{v}^a + \boldsymbol{t}_a^b \cdot 1 \\
                  \boldsymbol{0}^\mathsf{T} \boldsymbol{v}^a + 1 \cdot 1 \end{bmatrix}
= \begin{bmatrix} \boldsymbol{R}_a^b \boldsymbol{v}^a + \boldsymbol{t}_a^b \\ 1 \end{bmatrix}$$

위쪽 3개 성분이 정확히 원하던 식이고, 마지막 성분이 **다시 1** 이 되어
$\tilde{\boldsymbol{v}}^b$ 도 동차좌표 형태를 유지한다. 그래서 변환을 연달아 곱할 수 있다.

$$\tilde{\boldsymbol{v}}^c = \boldsymbol{T}_b^c \boldsymbol{T}_a^b \tilde{\boldsymbol{v}}^a
= \boldsymbol{T}_a^c \tilde{\boldsymbol{v}}^a$$

### 3.2 $\boldsymbol{u}^\wedge \boldsymbol{v} = \boldsymbol{u} \times \boldsymbol{v}$ 검산

위에서 제시한 skew-symmetric 행렬이 실제로 외적을 주는지 수치로 확인한다.
$\boldsymbol{u} = (1, 2, 3)$, $\boldsymbol{v} = (4, 5, 6)$ 으로 손계산하면

$$\boldsymbol{u}^\wedge \boldsymbol{v}
= \begin{bmatrix} 0 & -3 & 2 \\ 3 & 0 & -1 \\ -2 & 1 & 0 \end{bmatrix}
  \begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}
= \begin{bmatrix} 0\cdot4 - 3\cdot5 + 2\cdot6 \\ 3\cdot4 + 0\cdot5 - 1\cdot6 \\ -2\cdot4 + 1\cdot5 + 0\cdot6 \end{bmatrix}
= \begin{bmatrix} -3 \\ 6 \\ -3 \end{bmatrix}$$

```python
# 검산 — numpy 가 없으면: sudo apt install -y python3-numpy
import numpy as np

def hat(u):
    """R^3 벡터 → so(3) 원소 (skew-symmetric 행렬)"""
    return np.array([[    0, -u[2],  u[1]],
                     [ u[2],     0, -u[0]],
                     [-u[1],  u[0],     0]])

def vee(U):
    """so(3) 원소 → R^3 벡터. hat 의 역"""
    return np.array([U[2, 1], U[0, 2], U[1, 0]])

u = np.array([1., 2., 3.])
v = np.array([4., 5., 6.])

print("hat(u) @ v =", hat(u) @ v)      # 노트: [-3, 6, -3]
print("np.cross   =", np.cross(u, v))  # 같아야 한다
print("vee(hat(u))=", vee(hat(u)))     # 노트: [1, 2, 3]  ← 왕복해서 제자리

# skew-symmetric 인지: A^T = -A
print("skew 확인   :", np.allclose(hat(u).T, -hat(u)))

# 자기 자신과의 외적은 0 (평행하므로)
print("u^ u = 0    :", np.allclose(hat(u) @ u, 0))
```

실행하면 `[-3. 6. -3.]` 이 두 번 나오고 나머지가 `True` 여야 한다.
손계산과 일치하는 것을 확인했다.

### 3.3 연습문제 — 첨자 뒤집기

$\boldsymbol{R}_a^b$ 의 역이 $\boldsymbol{R}_b^a$ 이고, 회전행렬의 성질상
$\boldsymbol{R}_b^a = (\boldsymbol{R}_a^b)^{-1} = (\boldsymbol{R}_a^b)^\mathsf{T}$ 이다.

그렇다면 $\boldsymbol{T}_b^a$ 는 무엇인가? $(\boldsymbol{T}_a^b)^\mathsf{T}$ 가
**아닌** 이유와 함께 답하라.

> **힌트** — $\boldsymbol{T}_a^b \boldsymbol{T}_b^a = \boldsymbol{I}$ 가 되어야 한다.
> 블록 곱으로 조건을 세우고 이동 성분을 풀면 된다. 답은 2장에서 다시 만난다.

---

## 4. 관측 기록 — 챕터를 읽으며 채운다

기준(위 1·2절)과 **실제 본문의 표기가 어긋난 곳**을 여기에 누적한다.
70명이 쓴 책이라 이런 일이 생기고, 기록해 두지 않으면 매번 다시 헷갈린다.

| 장 | 기준 표기 | 그 장에서 쓴 표기 | 메모 |
|---|---|---|---|
| — | — | — | *(아직 없음. 1장부터 채운다)* |

### 기록 규칙

- **같은 뜻인데 다른 기호**를 쓴 경우 → 위 표에 적고, 노트 본문에서는 기준 표기로 통일하되
  원문 대조가 가능하도록 첫 등장 때 "(책은 $\cdots$ 로 쓴다, p.NNN)" 를 붙인다
- **같은 기호인데 다른 뜻**인 경우 → 훨씬 위험하다. 표에 적고 **그 장 노트의 머리 블록에도** 경고를 남긴다
- 판단이 애매하면 원문을 이미지로 렌더링해 확인한다 (`3_Pitfalls.md` A13)

---

## 5. 이 노트에서 확정한 용어

`2_Template_and_Rule.md` 의 "절대 번역하지 않는 용어" 표에 아래를 추가한다.

| 쓸 것 | 쓰지 말 것 |
|---|---|
| frame (또는 좌표계) | 프레임 |
| pose | 자세, 포즈 |
| homogeneous point / coordinates | 동차점 (단 "동차좌표"는 통용되므로 허용) |
| Lie group / Lie algebra | 리 군 / 리 대수 |
| skew-symmetric | 반대칭 |
| prior / posterior | (첫 등장 시 병기 허용, 이후 영어) |
| Gaussian process | 가우시안 과정 |

**한국어를 쓰는 것**: 공분산, 확률밀도, 항등행렬, 영행렬, 전치, 벡터공간, 외적, 회전행렬, 노름.
