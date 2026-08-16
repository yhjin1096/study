# Notes on On-manifold preintegration for real-time visual-inertial odometry

> **원문** — Gyubeom Edward Im, *Notes on On-manifold preintegration for real-time
> visual-inertial odometry* (18쪽, 원논문 C. Forster 외) ·
> blog: [alida.tistory.com](https://alida.tistory.com) · email: criterion.im@gmail.com
> 파일: `ref/Notes on On-manifold preintegration for real-time visual-inertial odometry.pdf`
>
> **이 문서에 대하여** — 원문을 **내용 수정 없이 그대로** 옮긴 것이다. 절 구성·문장·수식 번호
> (1)~(82)가 모두 원문과 같고 순서도 바꾸지 않았다. 원문에는 그림이 하나도 없다.
> **1장 · 6장 · A.4는 원문에 제목만 있고 본문이 없다.** 비워 둔 것이 아니라 원문이 그렇다.
>
> 원문에 없는 것은 **인터랙티브 위젯 12개**뿐이며, 전부 **원문에 없는 추가 요소**라고 표시된
> 회색 박스 안에 들어 있어 본문과 섞이지 않는다.
>
> 명백한 오타는 바로잡았고, 무엇을 고쳤는지는 맨 아래
> [옮기며 바로잡은 것](#옮기며-바로잡은-것)에 전부 적어 두었다.
> 원문이 쓰는 **두 가지 색 강조를 모두 재현**했다 —
> 산문의 <span class="hl">파란 강조</span> 29곳과, 수식 안의 $\color{#a50000}{진홍\ 강조}$ 57곳이다.

| 장 | 원문 쪽 | 식 | 장 | 원문 쪽 | 식 |
|---|---|---|---|---|---|
| 1 Introduction | 2 | — | 6 Structureless vision factor | 12 | — |
| 2 Preliminaries | 2 | (1)~(23) | A Appendix | 12 | (54)~(82) |
| 3 Maximum a posteriori visual-inertial state estimation | 5 | (24)~(28) | B References | 18 | — |
| 4 IMU model and motion integration | 6 | (29)~(35) | C Revision log | 18 | — |
| 5 IMU preintegration on manifold | 8 | (36)~(53) | | | |

# 1 Introduction

# 2 Preliminaries

본 논문에서는 VIO 관련 수식을 최적화하기 위해 MAP 추정을 사용한다. IMU 상태 변수에는 회전, 포즈와 같은
비선형(smooth manifold like SO(3), SE(3)) 항들이 존재하기 때문에 MAP 추정 방법은 결국 비선형 최소제곱법
(non-linear least squares like GN, LM)을 수행하여 풀게 된다. 본격적으로 설명하기에 앞서 자주 사용하는 기하학
지식들을 먼저 설명한다.

## 2.1 Notions of Riemannian geometry

### 2.1.1 Special orthogonal group SO(3)

==SO(3)군은 3차원 회전 행렬들의 제약조건을 담고 있는 군==을 말한다(자세한 내용은 링크 참조).

$$SO(3) \doteq \{\mathbf{R} \in \mathbb{R}^{3\times 3} : \mathbf{R}^\intercal\mathbf{R} = \mathbf{I},\ \det(\mathbf{R}) = 1\} \tag{1}$$

SO(3)군 사이의 연산은 행렬 곱으로 수행하며 역(inverse)는 행렬을 전치(transpose)함으로써 구할 수 있다.
==SO(3)는 smooth manifold 상에 존재하며 접평면(tangent space at identity) 상의 원소는 lie algebra
so(3)라고 부른다.== lie algebra so(3)는 3x3 크기의 반대칭 행렬로 구성되어 있다.

$$\boldsymbol{\omega}^\wedge =
\begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix}^\wedge =
\begin{bmatrix} 0 & -\omega_3 & \omega_2 \\ \omega_3 & 0 & -\omega_1 \\ -\omega_2 & \omega_1 & 0 \end{bmatrix}
\in so(3) \tag{2}$$

- $(\cdot)^\wedge$ : 3차원 벡터 $\boldsymbol{\omega}$를 3x3 반대칭 행렬 so(3)로 만드는 연산
- $(\cdot)^\vee$ : 3x3 반대칭 행렬 so(3)를 3차원 벡터 $\boldsymbol{\omega}$로 만드는 연산

반대칭 행렬의 유용한 성질은 다음과 같다

$$\mathbf{a}^\wedge\mathbf{b} = -\mathbf{b}^\wedge\mathbf{a}, \quad \forall\mathbf{a},\mathbf{b} \in \mathbb{R}^3 \tag{3}$$

==지수 매핑(exponential mapping at identity)== $\exp : so(3) \mapsto SO(3)$는 lie algebra so(3)를 lie group SO(3)
로 변환해주는 연산이며 둘 사이의 관계를 표현한 Rodrigues' formula가 유명하다

$$\exp(\boldsymbol{\phi}^\wedge) = \mathbf{I} + \frac{\sin(\|\boldsymbol{\phi}\|)}{\|\boldsymbol{\phi}\|}\boldsymbol{\phi}^\wedge + \frac{1-\cos(\|\boldsymbol{\phi}\|)}{\|\boldsymbol{\phi}\|^2}(\boldsymbol{\phi}^\wedge)^2 \tag{4}$$

지수 매핑의 1차 근사는 작은 회전량을 근사할 때 유용하게 사용된다.

$$\exp(\boldsymbol{\phi}^\wedge) \approx \mathbf{I} + \boldsymbol{\phi}^\wedge \tag{5}$$

==로그 매핑(logarithm mapping at identity)==은 $\mathbf{R} \neq \mathbf{I}$인 SO(3)를 lie algebra so(3)로 변환해주는 매핑이다

$$\log(\mathbf{R}) = \frac{\varphi\cdot(\mathbf{R}-\mathbf{R}^\intercal)}{2\sin(\varphi)} \quad \text{with } \varphi = \cos^{-1}\left(\frac{\mathrm{tr}(\mathbf{R}-1)}{2}\right) \tag{6}$$

- $\log(\mathbf{R})^\vee = \mathbf{a}\varphi$ : $\mathbf{a}$는 회전축 벡터, $\varphi$는 회전 각도
- $\mathbf{R} = \mathbf{I}$이면 $\varphi = 0$이 되어 $\mathbf{a}$의 해가 무수히 많아진다

만약 지수 매핑의 정의역을 $\|\boldsymbol{\phi}\| < \pi$로 제한한다면 지수 매핑은 일대일 대응(bijective) 함수가 되며 그 역함수는
로그 매핑이 된다. 하지만 정의역을 제한하지 않으면 지수 매핑은 전사(surjective) 함수가 된다. 왜냐하면 임의의
회전 행렬 $\mathbf{R}$에 대한 angle-axis 표현을 $(\mathbf{a},\theta)$라고 할 때, $\boldsymbol{\phi} = (\theta + 2k\pi)\mathbf{a}$, $k \in \mathbb{Z}$가 $2\pi$마다 같은 각도를 의미하기
때문이다.

표기의 편의를 위해 일반적으로 $\exp(), \log()$ 대신 벡터화된 지수 매핑과 로그 매핑 $\mathrm{Exp}(), \mathrm{Log}()$을 자주 사용한다

$$\begin{aligned}
\mathrm{Exp} &: \quad \mathbb{R}^3 \to SO(3) \quad ; \quad \boldsymbol{\phi} \mapsto \exp(\boldsymbol{\phi}^\wedge) \\
\mathrm{Log} &: \quad SO(3) \to \mathbb{R}^3 \quad ; \quad \mathbf{R} \mapsto \log(\mathbf{R})^\vee
\end{aligned} \tag{7}$$

수식을 유도하다 보면 다음과 같은 지수 매핑의 1차 근사를 사용할 것이다.

$$\mathrm{Exp}(\boldsymbol{\phi} + \delta\boldsymbol{\phi}) \approx \mathrm{Exp}(\boldsymbol{\phi})\mathrm{Exp}(\mathbf{J}_r(\boldsymbol{\phi})\delta\boldsymbol{\phi}) \tag{8}$$

- $\mathbf{J}_r$ : ==SO(3)군의 오른쪽 자코비안(right jacobian)==. 기존 SO(3)군의 오른쪽에 섭동량(increments)를 곱할 때
유도되는 자코비안 행렬

$$\mathbf{J}_r(\boldsymbol{\phi}) = \mathbf{I} - \left(\frac{1-\cos(\|\boldsymbol{\phi}\|)}{\|\boldsymbol{\phi}\|^2}\right)\boldsymbol{\phi}^\wedge + \left(\frac{\|\boldsymbol{\phi}\|-\sin(\|\boldsymbol{\phi}\|)}{\|\boldsymbol{\phi}\|^3}\right)(\boldsymbol{\phi}^\wedge)^2 \tag{9}$$

로그 매핑에도 유사한 1차 근사가 존재한다

$$\mathrm{Log}(\mathrm{Exp}(\boldsymbol{\phi})\mathrm{Exp}(\delta\boldsymbol{\phi})) \approx \boldsymbol{\phi} + \mathbf{J}_r^{-1}(\boldsymbol{\phi})\delta\boldsymbol{\phi} \tag{10}$$

오른쪽 자코비안의 역행렬은 다음과 같다

$$\mathbf{J}_r^{-1}(\boldsymbol{\phi}) = \mathbf{I} + \frac{1}{2}\boldsymbol{\phi}^\wedge + \left(\frac{1}{\|\boldsymbol{\phi}\|^2} - \frac{1+\cos(\|\boldsymbol{\phi}\|)}{2\|\boldsymbol{\phi}\|\sin(\|\boldsymbol{\phi}\|)}\right)(\boldsymbol{\phi}^\wedge)^2 \tag{11}$$

오른쪽 자코비안과 그 역행렬 $\mathbf{J}_r, \mathbf{J}_r^{-1}$은 $\|\boldsymbol{\phi}\| = 0$일 때 항등 행렬 $\mathbf{I}$가 된다.
지수 매핑의 또다른 유용한 성질은 다음과 같다

$$\begin{aligned}
\mathbf{R}\mathrm{Exp}(\boldsymbol{\phi})\mathbf{R}^\intercal &= \exp(\mathbf{R}\boldsymbol{\phi}^\wedge\mathbf{R}^\intercal) = \mathrm{Exp}(\mathbf{R}\boldsymbol{\phi}) \\
\Leftrightarrow \mathrm{Exp}(\boldsymbol{\phi})\mathbf{R} &= \mathbf{R}\mathrm{Exp}(\mathbf{R}^\intercal\boldsymbol{\phi})
\end{aligned} \tag{12}$$

<!--widget:so3-exp-log-jacobian-->

### 2.1.2 Special euclidean group SE(3)

SE(3)군은 3차원 강체(rigid body)의 변환 행렬과 관련된 제약조건을 담고 있는 군을 말한다. (자세한 내용은 링크
참조).

$$SE(3) \doteq \{(\mathbf{R},\mathbf{p}) : \mathbf{R} \in SO(3), \mathbf{p} \in \mathbb{R}^3\} \tag{13}$$

두 개의 SE(3)군에 속한 변환 행렬 $\mathbf{T}_1, \mathbf{T}_2$가 주어졌을 때, 군의 연산은 행렬곱으로 표현되며 $\mathbf{T_1T_2} = (\mathbf{R}_1\mathbf{R}_2, \mathbf{p}_1 +
\mathbf{R}_1\mathbf{p}_2)$와 같다. 그리고 역(inverse)는 변환 행렬의 역행렬 $\mathbf{T}_1^{-1} = (\mathbf{R}_1^\intercal, -\mathbf{R}_1^\intercal\mathbf{p}_1)$으로 표현된다. SE(3)군 역시 지수
매핑과 로그 매핑이 존재하지만 이는 본 논문에서 사용되지 않으므로 자세한 설명은 생략한다.

<!--widget:adjoint-identity-->

## 2.2 Uncertainty description in SO(3)

SO(3)에서 불확실성을 정의하는 자연스러운 방법은 먼저 접평면(tangent space)에서 분포를 정한 뒤 이를 (7)의
지수 매핑을 통해 SO(3) 군으로 보내는 것이다.

$$\tilde{\mathbf{R}} = \mathbf{R}\mathrm{Exp}(\epsilon), \qquad \epsilon \sim (0,\Sigma) \tag{14}$$

- $\mathbf{R}$: 노이즈가 없는 회전 (→ 평균)
- $\epsilon$: 평균이 0, 분산이 $\Sigma$인 정규분포를 따르는 확률 변수

$\tilde{\mathbf{R}}$의 분포를 명시적으로 얻기 위해 $\mathbb{R}^3$의 적분에서 시작해보자.

$$\int_{\mathbb{R}^3} p(\epsilon)d\epsilon = \int_{\mathbb{R}^3} \alpha e^{-\frac{1}{2}\|\epsilon\|_\Sigma^2}d\epsilon = 1 \tag{15}$$

- $\alpha = 1/\sqrt{(2\pi)^3\det(\Sigma)}$
- $\|\epsilon\|_\Sigma^2 \doteq \epsilon^\intercal\Sigma^{-1}\epsilon$ : 마할라노비스 거리의 제곱

위 식에 $\epsilon = \mathrm{Log}(\mathbf{R}^{-1}\mathbf{R})$을 대입해보자. 이는 $\|\epsilon\| < \pi$일 때 (14)의 역연산이다.

$$\int_{SO(3)} \beta(\tilde{\mathbf{R}})e^{-\frac{1}{2}\|\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}})\|_\Sigma^2}d\tilde{\mathbf{R}} = 1 \tag{16}$$

- $\beta(\tilde{\mathbf{R}})$ : 정규화 인자(normalization factor). 함수의 적분 면적을 1로 만들어주는 계수

정규화 인자를 자세히 보면 $\beta(\tilde{\mathbf{R}}) = \alpha/|\det(\mathcal{J}(\tilde{\mathbf{R}}))|$과 같다. 이 때, $\mathcal{J}(\tilde{\mathbf{R}}) \doteq \mathbf{J}_r(\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}}))$이다. $\mathbf{J}_r(\cdot)$은 앞서
(9)에서 설명한 SO(3)군의 오른쪽 자코비안이다.
(16)의 형태에서 바로 SO(3)의 가우시안 분포를 얻을 수 있다.

$$p(\tilde{\mathbf{R}}) = \beta(\tilde{\mathbf{R}})e^{-\frac{1}{2}\|\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}})\|_\Sigma^2} \tag{17}$$

공분산이 작을 때는 $\tilde{\mathbf{R}} \approx \mathbf{R}$이므로 $\mathbf{J}_r(\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}})) \approx \mathbf{I}$이고 $\beta(\tilde{\mathbf{R}}) \approx \alpha$로 근사할 수 있다. (16)는 이미 $\|\epsilon\| < \pi$와
같이 범위가 정해져 있기 때문에 평균에서 멀리 있는($\pi$를 넘어가는) 각도는 고려하지 않으므로 작은 공분산이라는
가정이 더욱 타당해진다.
만약 $\beta$를 상수로 가정하면, $\tilde{\mathbf{R}}$이 (17)처럼 분포할 때 회전 $\mathbf{R}$의 negative log-likelihood는 다음과 같다

$$\mathcal{L}(\mathbf{R}) = \frac{1}{2}\|\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}})\|_\Sigma^2 + \mathrm{const} = \frac{1}{2}\|\mathrm{Log}(\tilde{\mathbf{R}}^{-1}\mathbf{R})\|_\Sigma^2 + \mathrm{const} \tag{18}$$

이는 기하학적으로 봤을 때 $\tilde{\mathbf{R}}$과 $\mathbf{R}$ 사이의 회전각(SO(3) geodesic 거리)을 의미한다. 그리고 거기에 $\Sigma^{-1}$ 가중
치를 곱한 후 제곱한 거리로 해석할 수 있다.

<!--widget:so3-uncertainty-->

## 2.3 Gauss-Newton method on manifold

유클리드 공간에서 일반적인 Gauss-Newton(GN) 방법은 (일반적으로 non-convex)인 목적 함수를 2차 근사(quadratic
approximation)로 반복적으로 최적화한다. 2차 근사는 선형 방정식(정규 방정식)을 푸는 문제로 귀결되고 그 해로
현재 추정값을 갱신한다. ==이번 섹션에서는 이러한 GN을 변수들이 특정 manifold $\mathcal{M}$ 위에 사는 (제약 없는)
최적화 문제로 확장하는 법에 대해 설명한다.==
다음 문제를 생각해보자

$$\min_{x \in \mathcal{M}} f(x) \tag{19}$$

- $x$는 manifold $\mathcal{M}$ 위에 존재하는 변수
- 편의 상 위 식은 단일 변수로 나타내었지만 다변수로 쉽게 일반화할 수 있다.

유클리드 경우와 달리 위 식은 $x$에 대해 바로 2차 근사를 만들 수 없다. 주된 이유는 두 가지이다.

1. 첫째로 $x$ 자체로 최적화를 수행하는 경우 over-parameterized 문제가 발생할 수 있다. 예를 들어 회전 행렬은
   3자유도이지만 9개의 파라미터를 갖고 있다. 이 때문에 정규 방정식이 under-determined되어 무수한 해를
   가질 수 있다.

2. 둘째는 그렇게 얻은 근사 해가 일반적으로 $\mathcal{M}$ 위에 있지 않다.

==manifold 최적화의 일반적인 접근 방법은 리트랙션(retraction) $\mathcal{R}_x$를 도입하는 것이다.== $\mathcal{R}_x$는 점 $x$의 접평면
공간의 원소 $\delta x$와 $x$ 주변의 $\mathcal{M}$ 상의 한 이웃 사이를 연결하는 일대일 대응 매핑 연산자를 의미한다. 리트랙션을
사용하면 문제를 아래와 같이 변경할 수 있다.

$$\min_{x \in \mathcal{M}} f(x) \qquad \Rightarrow \qquad \min_{\delta x \in \mathbb{R}^n} f(\mathcal{R}_x(\delta x)) \tag{20}$$

==위 식과 같이 기존 파라미터를 변경(re-parameterized)하는 것을 흔히 리프팅(lifting)이라고 부른다.== 간단
히 말하면 현재 상태에서 정의되는 접평면(여기는 국소적으로 유클리드 공간처럼 작동)에서 작업을 수행하기 위해
파라미터를 바꾸는 것이다(SO(3)인 경우 $\delta x \in \mathbb{R}^3$).
리프팅이 되었으면 (20) 문제에 일반적인 최적화 기법을 적용한다. GN 프레임워크에서는 현재 상태 주변에서
비용 함수를 제곱한 다음 2차 근사 방법을 통해 접평면 공간에서 $\delta x^*$를 구한다. 최종적으로 현재 상태를 다음과
같이 갱신한다.

$$\hat{x} \leftarrow \mathcal{R}_x(\delta x^*) \tag{21}$$

==위와 같은 방법론을 흔히 "lift-solve-retraction"이라고 부르며 어떤 trust-region 방법에도 사용할 수 있다.==
또한 이 방법은 항공 역학 필터링 문헌의 에러 상태 모델(error-state model)을 단일 이론으로 묶어주며 로보틱스
최적화에도 널리 쓰인다.
마지막으로 $\mathcal{R}_x$의 구체적인 방법에 대해 얘기해보자. 지수 매핑(exponential mapping)은 사용 가능한 리트랙션
방법 중 하나이다. 본 논문에서는 다음과 같은 리트랙션을 사용한다.

$$\mathcal{R}_{\mathbf{R}}(\boldsymbol{\phi}) = \mathbf{R}\mathrm{Exp}(\delta\boldsymbol{\phi}), \qquad \delta\boldsymbol{\phi} \in \mathbb{R}^3 \tag{22}$$

SE(3)군의 경우 $\mathbf{T} \doteq (\mathbf{R},\mathbf{p})$라고 하면 다음과 같이 리트랙션을 정의한다.

$$\mathcal{R}_{\mathbf{T}}(\delta\boldsymbol{\phi},\delta\mathbf{p}) = (\mathbf{R}\mathrm{Exp}(\delta\boldsymbol{\phi}),\ \mathbf{p} + \mathbf{R}\delta\mathbf{p}), \qquad [\delta\boldsymbol{\phi},\delta\mathbf{p}] \in \mathbb{R}^6 \tag{23}$$

<!--widget:manifold-gauss-newton-->

# 3 Maximum a posteriori visual-inertial state estimation

본 논문에서는 IMU와 단안 카메라가 달린 시스템(모바일 로봇, 드론, 핸드헬드 장치 등)의 상태를 추정하는 VIO
문제를 다룬다. ==IMU 좌표계 $B$가 우리가 추적하는 본체의 좌표계와 일치한다고 가정하고 카메라-IMU 변환은
미리 캘리브레이션하여 고정되어 있다고 본다.== Front-end에서는 3D 랜드마크에 대한 이미지 측정 값을 제공하며
여러 영상 중 일부를 키프레임으로 고정한다. 우리는 이 키프레임들의 포즈를 추정한다.

## 3.1 The state

시간 $i$에서 시스템의 상태는 IMU 기준의 방향, 위치, 속도, bias로 표현된다.

$$\mathbf{x}_i \doteq [\mathbf{R}_i, \mathbf{p}_i, \mathbf{v}_i, \mathbf{b}_i] \tag{24}$$

- $(\mathbf{R}_i, \mathbf{p}_i)$ : SE(3)군에 속하는 포즈
- $\mathbf{v}_i \in \mathbb{R}^3$ : 속도
- $\mathbf{b}_i = [\mathbf{b}_i^g, \mathbf{b}_i^a] \in \mathbb{R}^6$ : IMU bias

시간 $k$까지의 모든 키프레임들의 집합을 $\mathcal{K}_k$라고 할 때 우리가 추정하는 상태들의 집합 $\mathcal{X}_k$는 다음과 같이 표기할
수 있다.

$$\mathcal{X}_k \doteq \{\mathbf{x}_i\}_{i \in \mathcal{K}_k} \tag{25}$$

==본 논문의 실제 구현에서는 structureless 기법을 사용하기 때문에 3D 랜드마크는 상태 변수에 포함하지
않는다.== 필요하다면 위 방법을 랜드마크 및 카메라 내,외부 파라미터 추정으로도 쉽게 일반화 할 수 있다.

## 3.2 The measurements

입력 측정값은 IMU와 카메라 센서로부터 들어온다. 키프레임 $i$의 이미지 집합을 $\mathcal{C}_i$로 표기한다. 시간 $i$에 카메라는
여러 랜드마크 $l$을 볼 수 있으므로 $\mathcal{C}_i$에는 여러 측정값 $\mathbf{z}_{il}$이 포함된다. 편의 상 $l \in \mathcal{C}_i$라고 표기하면 $i$에서 $l$을
관측했다는 뜻으로 해석한다.
연속 키프레임 $i$와 $j$ 사이에서 수집된 IMU 측정값들의 집합은 $\mathcal{I}_{ij}$로 쓴다. IMU 업데이트 속도와 키프레임 빈도
에 따라 $\mathcal{I}_{ij}$의 수는 수 개에서 수 백개의 측정값이 들어갈 수 있다. 시간 $k$까지 모인 전체 IMU+이미지 관측값들의
집합 $\mathcal{Z}_k$는 다음과 같다.

$$\mathcal{Z}_k \doteq \{\mathcal{C}_i, \mathcal{I}_{ij}\}_{(i,j) \in \mathcal{K}_k} \tag{26}$$

## 3.3 Factor graphs and MAP estimation

관측값 $\mathcal{Z}_k$와 상태에 대한 사전 정보 $p(\mathcal{X}_0)$가 주어졌을 때 상태 변수 $\mathcal{X}_k$의 사후 분포(posteriori)는 다음과 같다

$$\begin{aligned}
p(\mathcal{X}_k|\mathcal{Z}_k) &\propto p(\mathcal{X}_0)p(\mathcal{Z}_k|\mathcal{X}_k) =^{(a)} p(\mathcal{X}_0) \prod_{(i,j) \in \mathcal{K}_k} p(\mathcal{C}_i, \mathcal{I}_{ij}|\mathcal{X}_k) \\
&=^{(b)} p(\mathcal{X}_0) \prod_{(i,j) \in \mathcal{K}_k} p(\mathcal{I}_{ij}|\mathbf{x}_j, \mathbf{x}_i) \prod_{i \in \mathcal{K}_k} \prod_{l \in \mathcal{C}_i} p(\mathbf{z}_{il}|\mathbf{x}_i)
\end{aligned} \tag{27}$$

- (a) : 관측값들 간의 독립이라고 가정했을 때 분해
- (b) : 마르코프 성질을 사용한 분해

==$\mathcal{Z}_k$는 이미 관측된 값이므로 더 이상 우리가 추정할 변수가 아니다. 따라서 사후분포는 상태 변수 $\mathcal{X}_k$들만을
인수(factor) 로 갖는 likelihood들의 곱으로 정리된다. 이 곱 구조를 그대로 그림으로 나타낸 것이 factor graph
이다.== 그래프에는 상태(미지수)들을 담는 변수 노드와, 해당 상태들에 의존하는 likelihood(또는 제약)를 나타내는
factor 노드가 있고, 각 factor 노드는 자신이 참조하는 변수 노드들과 연결된다.
MAP 추정으로 구하고자 하는 상태 $\mathcal{X}^*$는 (27)를 최대로 하는 값, 즉 negative log-posterior의 최소값이다.
노이즈가 평균이 0인 가우시안 분포라고 가정하면 이는 residual 제곱들의 합으로 표현할 수 있다.

$$\begin{aligned}
\mathcal{X}_k^* &\doteq \arg\min_{\mathcal{X}_k}\ -\log_e p(\mathcal{X}_k|\mathcal{Z}_k) \\
&= \arg\min_{\mathcal{X}_k} \|\mathbf{r}_0\|_{\boldsymbol{\Sigma}_0^2}^2 + \sum_{(i,j) \in \mathcal{K}_k} \|\mathbf{r}_{\mathcal{I}_{ij}}\|_{\boldsymbol{\Sigma}_{ij}^2}^2 + \sum_{i \in \mathcal{K}_k}\sum_{l \in \mathcal{C}_i} \|\mathbf{r}_{\mathcal{C}_{il}}\|_{\boldsymbol{\Sigma}_C}^2
\end{aligned} \tag{28}$$

- $\mathbf{r}_0$ : 사전 항의 residual
- $\mathbf{r}_{\mathcal{I}_{ij}}$ : preintegrated IMU의 residual
- $\mathbf{r}_{\mathcal{C}_{il}}$ : 랜드마크의 reprojection residual
- $\boldsymbol{\Sigma}_0, \boldsymbol{\Sigma}_{ij}, \boldsymbol{\Sigma}_c$ : 각 residual들의 공분산

간단하게 말해서 residual은 측정값과 예측값의 차이를 수치화한 함수이고 우리는 그 제곱합(+공분산으로 가중
된)을 최소화해 상태 $\mathcal{X}_k$를 추정한다.

<!--widget:factor-graph-->

# 4 IMU model and motion integration

일반적으로 IMU 센서로부터 얻을 수 있는 정보에는 3축의 가속도와 3축의 각속도 정보가 포함된다. 가속도와
각속도의 측정값(measurement)에는 bias와 노이즈 성분이 포함되어 있기 때문에 다음과 같이 나타낼 수 있다.

$$\begin{aligned}
{}_{B}\tilde{\boldsymbol{\omega}}_{WB}(t) &= {}_{B}\boldsymbol{\omega}_{WB}(t) + \mathbf{b}^g(t) + \boldsymbol{\eta}^g(t) \\
{}_{B}\tilde{\mathbf{a}}(t) &= \mathbf{R}_{WB}^\intercal(t)({}_{W}\mathbf{a}(t) - {}_{W}\mathbf{g}) + \mathbf{b}^a(t) + \boldsymbol{\eta}^a(t)
\end{aligned} \tag{29}$$

- ${}_{B}\tilde{\boldsymbol{\omega}}_{WB}(t)$: 관측된(measured) 각속도
- ${}_{B}\tilde{\mathbf{a}}(t)$: 관측된(measured) 가속도
- ${}_{B}\boldsymbol{\omega}_{WB}(t)$: 실제(true) 각속도
- ${}_{W}\mathbf{a}(t)$: 실제(true) 가속도
- $\mathbf{b}^g(t), \mathbf{b}^a(t)$: 각속도와 가속도의 bias 값
- $\boldsymbol{\eta}^g(t), \boldsymbol{\eta}^a(t)$: 각속도와 가속도의 노이즈 값

기호 앞에 위치하는 B는 =="B(=IMU) 좌표계에서 바라본"== 것을 의미한다. IMU의 포즈는 $\{\mathbf{R}_{WB},\ {}_{W}\mathbf{p}\}$에 의해 B
에서 W로 변환되어 월드 좌표계 기준으로 표현된다. ${}_{B}\boldsymbol{\omega}_{WB} \in \mathbb{R}^3$는 B 좌표계에서 표현된 "W에서 본 B의" 순간적인
각속도(instantaneous angular velocity)를 의미한다. ${}_{W}\mathbf{a} \in \mathbb{R}^3$는 월드 좌표계에서 본 센서의 가속도를 의미하며 ${}_{W}\mathbf{g}$
는 월드 좌표계에서 본 중력 벡터를 의미한다.
IMU 측정값으로 부터 아래와 같은 ==IMU Kinematic Model==을 사용하면 IMU의 모션을 추정할 수 있다.

$$\begin{aligned}
\dot{\mathbf{R}}_{WB} &= \mathbf{R}_{WB}\ {}_{B}\boldsymbol{\omega}_{WB}^\wedge \\
{}_{W}\dot{\mathbf{v}} &= {}_{W}\mathbf{a} \\
{}_{W}\dot{\mathbf{p}} &= {}_{W}\mathbf{v}
\end{aligned} \tag{30}$$

위 모델을 사용하면 시간에 따른 IMU의 포즈와 속도의 변화를 수식으로 나타낼 수 있다. $t + \Delta t$ 시간에 IMU
포즈와 속도는 다음과 같이 (30)를 적분하여 나타낼 수 있다.

$$\begin{aligned}
\mathbf{R}_{WB}(t + \Delta t) &= \mathbf{R}_{WB}(t) \cdot \mathrm{Exp}\left(\color{#a50000}{\int_t^{t+\Delta t} {}_{B}\boldsymbol{\omega}_{WB}(\tau)d\tau}\right) \\
{}_{W}\mathbf{v}(t + \Delta t) &= {}_{W}\mathbf{v}(t) + \color{#a50000}{\int_t^{t+\Delta t} {}_{W}\mathbf{a}(\tau)d\tau} \\
{}_{W}\mathbf{p}(t + \Delta t) &= {}_{W}\mathbf{p}(t) + \int_t^{t+\Delta t} {}_{W}\mathbf{v}(\tau)d\tau + \color{#a50000}{\int\int_t^{t+\Delta t} {}_{W}\mathbf{a}(\tau)d\tau^2}
\end{aligned} \tag{31}$$

만약 가속도 ${}_{W}\mathbf{a}$와 각속도 ${}_{B}\boldsymbol{\omega}_{WB}$가 시간 $[t, t+\Delta t]$ 동안 일정(constant)하다고 가정하면 위 식은 다음과 같이
조금 더 간결하게 쓸 수 있다.

$$\begin{aligned}
\mathbf{R}_{WB}(t + \Delta t) &= \mathbf{R}_{WB}(t) \cdot \mathrm{Exp}(\color{#a50000}{{}_{B}\boldsymbol{\omega}_{WB}}\Delta t) \\
{}_{W}\mathbf{v}(t + \Delta t) &= {}_{W}\mathbf{v}(t) + \color{#a50000}{{}_{W}\mathbf{a}}\Delta t \\
{}_{W}\mathbf{p}(t + \Delta t) &= {}_{W}\mathbf{p}(t) + {}_{W}\mathbf{v}\Delta t + \color{#a50000}{{}_{W}\mathbf{a}}\Delta t^2
\end{aligned} \tag{32}$$

(29)에서 보다시피 실제 IMU 가속도와 각속도 ${}_{W}\mathbf{a}, {}_{B}\boldsymbol{\omega}_{WB}$는 IMU 측정값 ${}_{W}\tilde{\mathbf{a}}, {}_{B}\tilde{\boldsymbol{\omega}}_{WB}$에 대한 함수이므로 위 식을
다시 고쳐쓰면 다음과 같다.

$$\begin{aligned}
\mathbf{R}_{WB}(t + \Delta t) &= \mathbf{R}_{WB}(t) \cdot \mathrm{Exp}((\color{#a50000}{{}_{B}\tilde{\boldsymbol{\omega}}_{WB}(t) - {}_{B}\mathbf{b}^g(t) - {}_{B}\boldsymbol{\eta}^{gd}(t)})\Delta t) \\
{}_{W}\mathbf{v}(t + \Delta t) &= {}_{W}\mathbf{v}(t) + \color{#a50000}{{}_{W}\mathbf{g}}\Delta t + \color{#a50000}{\mathbf{R}_{WB}(t)({}_{W}\tilde{\mathbf{a}}(t) - {}_{B}\mathbf{b}^a(t) - {}_{B}\boldsymbol{\eta}^{ad}(t))}\Delta t \\
{}_{W}\mathbf{p}(t + \Delta t) &= {}_{W}\mathbf{p}(t) + {}_{W}\mathbf{v}(t)\Delta t + \color{#a50000}{\frac{1}{2}{}_{W}\mathbf{g}}\Delta t^2 + \color{#a50000}{\frac{1}{2}\mathbf{R}_{WB}(t)({}_{W}\tilde{\mathbf{a}}(t) - {}_{B}\mathbf{b}^a(t) - {}_{B}\boldsymbol{\eta}^{ad}(t))}\Delta t^2
\end{aligned} \tag{33}$$

아래 첨자로 붙은 좌표계는 자명하기 때문에 가독성을 위하여 이를 생략하여 나타낸다.

$$\boxed{\begin{aligned}
\mathbf{R}(t + \Delta t) &= \mathbf{R}(t) \cdot \mathrm{Exp}((\color{#a50000}{\tilde{\boldsymbol{\omega}}(t) - \mathbf{b}^g(t) - \boldsymbol{\eta}^{gd}(t)})\Delta t) \\
\mathbf{v}(t + \Delta t) &= \mathbf{v}(t) + \color{#a50000}{\mathbf{g}}\Delta t + \color{#a50000}{\mathbf{R}(t)(\tilde{\mathbf{a}}(t) - \mathbf{b}^a(t) - \boldsymbol{\eta}^{ad}(t))}\Delta t \\
\mathbf{p}(t + \Delta t) &= \mathbf{p}(t) + \mathbf{v}(t)\Delta t + \color{#a50000}{\frac{1}{2}\mathbf{g}}\Delta t^2 + \color{#a50000}{\frac{1}{2}\mathbf{R}(t)(\tilde{\mathbf{a}}(t) - \mathbf{b}^a(t) - \boldsymbol{\eta}^{ad}(t))}\Delta t^2
\end{aligned}} \tag{34}$$

- $\boldsymbol{\eta}^{gd}, \boldsymbol{\eta}^{ad}$ : 이산화 시간(discrete-time) 버전 각속도, 가속도 노이즈

이산화 시간(discrete-time) 버전 노이즈 $\boldsymbol{\eta}^{gd}, \boldsymbol{\eta}^{ad}$의 공분산은 연속 시간 노이즈 $\boldsymbol{\eta}^g, \boldsymbol{\eta}^a$와 샘플링 주기 $\Delta t$와
관련있기 때문에 이에 대한 함수로 나타낼 수 있다.

$$\begin{aligned}
\mathrm{Cov}(\boldsymbol{\eta}^{gd}(t)) &= \frac{1}{\Delta t}\mathrm{Cov}(\boldsymbol{\eta}^g(t)) \\
\mathrm{Cov}(\boldsymbol{\eta}^{ad}(t)) &= \frac{1}{\Delta t}\mathrm{Cov}(\boldsymbol{\eta}^a(t))
\end{aligned} \tag{35}$$

<!--widget:imu-integration-->

# 5 IMU preintegration on manifold

(34)을 자세히 보면 $t$ 시간과 $t + \Delta t$ 시간의 사이의 상태 변수에 대한 관계식인 것을 알 수 있다. 따라서 (34)를
사용하면 매 IMU 측정값(measurement)가 들어올 때마다 다음 스텝의 상태 변수를 추정(estimation)할 수 있다.
두 키프레임 $i, j$가 주어졌을 때 두 키프레임 사이에 존재하는 모든 IMU 측정값들을 누적하면 하나의 측정값으로
합칠 수 있으며 이를 ==preintegrated IMU 측정값(measurement)==이라고 정의한다. IMU는 카메라와 시간적으로
동기화되어 있다고 가정하고 임의의 이산 시간 $k$에 대한 측정값을 매 순간 얻는다고 할 때 (34)을 $k = i$부터 $k = j$
까지 누적한 preintegration IMU 측정값은 다음과 같다.

$$\begin{aligned}
\mathbf{R}_j &= \mathbf{R}_i \prod_{k=i}^{j-1} \mathrm{Exp}\left(\left(\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_k^g - \boldsymbol{\eta}_k^{gd}\right)\Delta t\right) \\
\mathbf{v}_j &= \mathbf{v}_i + \mathbf{g}\color{#a50000}{\Delta t_{ij}} + \sum_{k=i}^{j-1}\mathbf{R}_k\left(\tilde{\mathbf{a}}_k - \mathbf{b}_k^a - \boldsymbol{\eta}_k^{ad}\right)\Delta t \\
\mathbf{p}_j &= \mathbf{p}_i + \sum_{k=i}^{j-1}\left[\mathbf{v}_k\Delta t + \frac{1}{2}\mathbf{g}\Delta t^2 + \frac{1}{2}\mathbf{R}_k\left(\tilde{\mathbf{a}}_k - \mathbf{b}_k^a - \boldsymbol{\eta}_k^{ad}\right)\Delta t^2\right]
\end{aligned} \tag{36}$$

- $\Delta t_{ij} \doteq \sum_{k=i}^{j-1}\Delta t$: 키프레임 $i$ 부터 $j-1$까지 모든 $\Delta t$를 더한 값
- 가독성을 위해 $(\cdot)(t_i)$를 $(\cdot)_i$로 표기하였다

(36)를 사용하면 두 키프레임 $i$와 $j$ 사이의 IMU 측정값들을 누적하여 둘 사이의 상대적인 모션을 추정할 수 있다.
하지만 최적화 과정에서 비선형 상태 변수 $\mathbf{R}_i$가 업데이트 될 때마다 $[i,j)$ 구간의 모든 비선형 상태 변수를 선형화
(linearization)하는 과정에서 반복적인 연산을 수행해야 한다. 예를 들어 $\mathbf{R}_i$가 변하면 이에 따른 $\mathbf{R}_k, k = i,\cdots,j-1$
또한 모두 다시 계산해야 한다.
이러한 비효율적인 계산을 피하기 위해 (36)을 바로 사용하는 것이 아닌 아래와 같은 ==두 키프레임 $i$와 $j$의 상
대적인 모션 증가량(relative motion increments)를 정의하여 $t_i$ 시간의 포즈와 속도에 대해 독립적이 되도록
만든다.==

$$\boxed{\begin{aligned}
\Delta\mathbf{R}_{ij} &\doteq \mathbf{R}_i^\intercal\mathbf{R}_j & &= \prod_{k=i}^{j-1}\mathrm{Exp}\left(\left(\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_k^g - \boldsymbol{\eta}_k^{gd}\right)\Delta t\right) \\
\Delta\mathbf{v}_{ij} &\doteq \mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) & &= \sum_{k=i}^{j-1}\Delta\mathbf{R}_{ik}\left(\tilde{\mathbf{a}}_k - \mathbf{b}_k^a - \boldsymbol{\eta}_k^{ad}\right)\Delta t \\
\Delta\mathbf{p}_{ij} &\doteq \mathbf{R}_i^\intercal(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_k\Delta t_{ij} - \frac{1}{2}\sum_{k=i}^{j-1}\mathbf{g}\Delta t^2) & &= \sum_{k=i}^{j-1}\left[\Delta\mathbf{v}_{ik}\Delta t + \frac{1}{2}\Delta\mathbf{R}_{ik}\left(\tilde{\mathbf{a}}_k - \mathbf{b}_k^a - \boldsymbol{\eta}_k^{ad}\right)\Delta t^2\right]
\end{aligned}} \tag{37}$$

위 식에서 주목해야할 부분은 ==$\Delta\mathbf{v}_{ij}$와 $\Delta\mathbf{p}_{ij}$는 실제 속도와 실제 위치의 물리적 변화를 의미하지 않는다는
사실이다.== 두 물리량은 (37) 식의 맨 오른쪽 부분을 $t_i$ 시간의 상태 변수로부터 독립으로 만들기 위해 임의로 정의한
값이다. 식을 자세히 보면 맨 오른쪽 식은 중력 효과 또한 없는 것을 알 수 있다. (37)을 사용하면 $t_i$에 상관없이
IMU의 측정값으로부터 바로 두 키프레임 사이의 preintegration IMU 측정값을 구할 수 있다.
엄밀하게 말하면 (37) 에서 IMU의 bias 값은 매 순간마다 변화해야 하지만 계산의 편의를 위해 두 키프레임 $i, j$
사이의 시간은 충분히 짧은 시간이기 때문에 bias 값을 상수로 가정한다.

$$\begin{aligned}
\mathbf{b}_i^g &= \mathbf{b}_{i+1}^g = \cdots = \mathbf{b}_{j-1}^g \\
\mathbf{b}_i^a &= \mathbf{b}_{i+1}^a = \cdots = \mathbf{b}_{j-1}^a
\end{aligned} \tag{38}$$

<!--widget:preintegration-invariance-->

## 5.1 Preintegrated IMU measurements

(37)은 키프레임 $i$, $j$의 상태 변수를 나타낸 좌측 항과 이들의 측정값을 나타낸 우측 항으로 이루어져 있기 때문에
이미 하나의 측정 모델(measurement model)이라고 볼 수 있다. 하지만 ==(37)는 수식 안에 측정 노이즈($\eta$)들이
복잡하게 섞여 있기 때문에 하나의 깔끔한 MAP 추정 문제로 수식화하기 어려운 단점이 있다.== MAP 추정을
하려면 각 상태변수들을 깔끔한 negative log-likelihood 형태로 변환할 수 있어야 하기 때문에 노이즈항들을 분리할
필요가 있다. 따라서 노이즈항을 분리하기 위한 여러 수학적 테크닉들을 사용할 것이다. 그리고 $t_i$ 시간에서 bias
값은 이미 알고 있다고 가정하고 수식을 유도한다.
우선 $\Delta\mathbf{R}_{ij}$부터 노이즈항을 분리해보자. Preliminaries 섹션에서 설명한 (8)을 사용하여 노이즈항을 맨 뒤로
옮길 수 있다.

$$\begin{aligned}
\Delta\mathbf{R}_{ij} &= \prod_{k=i}^{j-1}\left[\mathrm{Exp}((\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_i^g)\Delta t) \cdot \color{#a50000}{\mathrm{Exp}\left(-\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t\right)}\right] \\
&= \Delta\tilde{\mathbf{R}}_{ij} \cdot \color{#a50000}{\prod_{k=i}^{j-1}\mathrm{Exp}\left(-\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t\right)} \\
&\doteq \Delta\tilde{\mathbf{R}}_{ij} \cdot \color{#a50000}{\mathrm{Exp}(-\delta\boldsymbol{\phi}_{ij})}
\end{aligned} \tag{39}$$

- $\mathbf{J}_r^k \doteq \mathbf{J}_r^k((\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_i^g)\Delta t)$를 단순화하여 표기
- $\Delta\tilde{\mathbf{R}}_{ij} \doteq \prod_{k=i}^{j-1}\mathrm{Exp}((\tilde{\boldsymbol{\omega}}_k - \mathbf{b}_i^g)\Delta t)$ : preintegrated된 상대 회전량
- $\delta\boldsymbol{\phi}_{ij}$ : preintegrated된 상대 회전량의 노이즈

다음으로 (39)를 (37)의 $\Delta\mathbf{v}_{ij}$에 대입한 후 작은 회전량에 대해 $\mathrm{Exp}(\delta\boldsymbol{\phi}_{ij}) \approx \mathbf{I} + \delta\boldsymbol{\phi}_{ij}^\wedge$ 근사를 적용하면 아래
식과 같다.

$$\begin{aligned}
\Delta\mathbf{v}_{ij} &= \sum_{k=i}^{j-1}\Delta\tilde{\mathbf{R}}_{ik}(\mathbf{I} - \color{#a50000}{\delta\boldsymbol{\phi}_{ij}}\!)(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)\Delta t - \color{#a50000}{\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t} \\
&= \Delta\tilde{\mathbf{v}}_{ij} + \color{#a50000}{\sum_{k=i}^{j-1}\left[\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ij}\Delta t - \Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t\right]} \\
&\doteq \Delta\tilde{\mathbf{v}}_{ij} - \color{#a50000}{\delta\mathbf{v}_{ij}}
\end{aligned} \tag{40}$$

- $\delta\tilde{\mathbf{v}}_{ij} \doteq \Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)\Delta t$ : preintegrated된 상대 속도
- $\delta\mathbf{v}_{ij}$ : preintegrated된 상대 속도의 노이즈

유사하게 (39)와 (40)을 (37)의 $\Delta\mathbf{p}_{ij}$에 대입한 후 작은 회전량의 근사식을 적용하면 다음과 같다.

$$\begin{aligned}
\Delta\mathbf{p}_{ij} &= \sum_{k=i}^{j-1}\left[(\Delta\tilde{\mathbf{v}}_{ik} - \color{#a50000}{\delta\mathbf{v}_{ik}}\!)\Delta t + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}(\mathbf{I} - \color{#a50000}{\delta\boldsymbol{\phi}_{ik}^\wedge}\!)(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)\Delta t^2 - \color{#a50000}{\frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t^2}\right] \\
&= \Delta\tilde{\mathbf{p}}_{ij} + \color{#a50000}{\sum_{k=i}^{j-1}\left[-\delta\mathbf{v}_{ik}\Delta t + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)\Delta t^2 - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t^2\right]} \\
&\doteq \Delta\tilde{\mathbf{p}}_{ij} - \color{#a50000}{\delta\mathbf{p}_{ij}}
\end{aligned} \tag{41}$$

- $\delta\tilde{\mathbf{p}}_{ij}$ : preintegrated된 상대 위치
- $\delta\mathbf{p}_{ij}$ : preintegrated된 상대 위치의 노이즈

지금까지 유도한 (39), (40), (41)을 원래 식 (37)에 대입하면 다음과 같은 preintegrated 측정 모델이 나온다.

$$\boxed{\begin{aligned}
\Delta\tilde{\mathbf{R}}_{ij} &= \mathbf{R}_i^\intercal\mathbf{R}_j\mathrm{Exp}(\color{#a50000}{\delta\boldsymbol{\phi}_{ij}}\!) \\
\Delta\tilde{\mathbf{v}}_{ij} &= \mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) + \color{#a50000}{\delta\mathbf{v}_{ij}} \\
\Delta\tilde{\mathbf{p}}_{ij} &= \mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) + \color{#a50000}{\delta\mathbf{p}_{ij}}
\end{aligned}} \tag{42}$$

- $\mathrm{Exp}(-\delta\boldsymbol{\phi}_{ij})^\intercal = \mathrm{Exp}(\delta\boldsymbol{\phi}_{ij})$가 적용되었다
- $[\delta\boldsymbol{\phi}_{ij}^\intercal, \delta\mathbf{v}_{ij}^\intercal, \delta\mathbf{p}_{ij}^\intercal]^\intercal$ : 랜덤 노이즈 벡터

이전 식 (37)은 상태와 노이즈항이 복잡하게 섞여 있었던 반면에 (42)은 상태와 랜덤 노이즈항이 서로 깔끔하게
분리된 것을 볼 수 있다.
==랜덤 노이즈가 평균이 0인 가우시안 분포를 따른다고 가정하면 (측정=상태+가우시안 노이즈) 형태로 분리된
꼴이므로 MAP 추정에서 결론적으로 풀고자하는 negative log-likelihood의 수식이 2차식 $\mathbf{r}^\intercal\Sigma^{-1}\mathbf{r}$ 형태로 깔
끔하게 계산되기 때문에 이를 활용한 최적화 구현이 비교적 단순해진다.== 그리고 회전, 속도, 위치에 대한 노이즈를
하나의 9차원 벡터와 공분산으로 다룰 수 있어 코드, 이론, 디버깅 또한 매우 통일성 있게 정돈된다.

## 5.2 Noise propagation

이번 섹션에서는 앞서 구한 랜덤 노이즈 벡터 $[\delta\boldsymbol{\phi}_{ij}^\intercal, \delta\mathbf{v}_{ij}^\intercal, \delta\mathbf{p}_{ij}^\intercal]^\intercal$의 특성에 대해 살펴본다. ==앞서 이 노이즈 벡터를
평균이 0인 가우시안 노이즈로 가정하면 다루기 편리하다고 하였지만 공분산을 정확히 모델링하는 것은 매우
중요하다.== 공분산의 역행렬은 MAP 최적화에서 각 항의 가중치로 직접 들어가기 때문이다. 그래서 해당 섹션에서는
preintegrated된 측정값의 공분산 $\boldsymbol{\Sigma}_{ij}$을 유도하는 과정에 대해 자세히 설명한다.

$$\boldsymbol{\eta}_{ij}^\Delta \doteq [\delta\boldsymbol{\phi}_{ij}^\intercal, \delta\mathbf{v}_{ij}^\intercal, \delta\mathbf{p}_{ij}^\intercal]^\intercal \sim \mathcal{N}(\mathbf{0}_{9\times 1}, \boldsymbol{\Sigma}_{ij}) \tag{43}$$

먼저 $\delta\boldsymbol{\phi}_{ij}$를 고려해보자. (39)를 보면 다음과 같이 정의되어 있다.

$$\mathrm{Exp}(-\delta\boldsymbol{\phi}_{ij}) \doteq \prod_{k=i}^{j-1}\mathrm{Exp}\left(-\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t\right) \tag{44}$$

양변에 logarithm mapping $\mathrm{Log}(\cdot)$을 취하면 다음과 같다.

$$\delta\boldsymbol{\phi}_{ij} = -\mathrm{Log}\left(\prod_{k=i}^{j-1}\mathrm{Exp}\left(-\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t\right)\right) \tag{45}$$

우측항에 logarithm mapping의 1차 근사를 적용하면 다음과 같다. 이 때, $\boldsymbol{\eta}_k^{gd}$와 $\delta\boldsymbol{\phi}_{ij}$는 충분히 작은 값이기
때문에 오른쪽 자코비안(right jacobian) $\mathbf{J}_r$은 $\mathbf{I}$에 수렴한다.

$$\delta\boldsymbol{\phi}_{ij} \simeq \sum_{k=i}^{j-1}\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t \tag{46}$$

- $\mathrm{Log}\left(\mathrm{Exp}(\boldsymbol{\phi})\mathrm{Exp}(\delta\boldsymbol{\phi})\right) \approx \boldsymbol{\phi} + \mathbf{J}_r^{-1}(\boldsymbol{\phi})\delta\boldsymbol{\phi}$ 근사를 적용하였다

1차 근사항까지만 고려하면 상대 회전량에 대한 노이즈 $\delta\boldsymbol{\phi}_{ij}$는 평균이 0인 가우시안 노이즈 $\boldsymbol{\eta}_k^{gd}$의 선형 결합
(linear combination)이므로 역시 평균이 0인 가우시안 분포를 지닌다. 이러한 성질이 좋은 이유는 회전에 대한
측정값 (42)이 정확히 (상태+노이즈) 꼴이 되기 때문이다. ($\tilde{\mathbf{R}} = \mathbf{R}\mathrm{Exp}(\epsilon)$)
상대 회전량에 대한 노이즈를 위와 같이 정리하면 속도, 위치에 대한 노이즈 $\delta\mathbf{v}_{ij}, \delta\mathbf{p}_{ij}$는 이해하기 수월해진다.
$\delta\mathbf{v}_{ij}, \delta\mathbf{p}_{ij}$ 식을 보면 $\boldsymbol{\eta}_k^{ad}$와 $\delta\boldsymbol{\phi}_{ij}$의 선형 결합으로 구성되어 있기 때문에 역시 평균이 0인 가우시안 분포가 된다.

$$\begin{aligned}
\delta\mathbf{v}_{ij} &\simeq \sum_{k=i}^{j-1}\left[-\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ik}\Delta t + \Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t\right] \\
\delta\mathbf{p}_{ij} &\simeq \sum_{k=i}^{j-1}\left[\delta\mathbf{v}_{ik}\Delta t - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ik}\Delta t^2 + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t^2\right]
\end{aligned} \tag{47}$$

- 이러한 근사는 고차항을 제외한 1차 근사까지만 유효하다

(46), (47) 식을 보면 ==preintegration 노이즈 $\boldsymbol{\eta}_{ij}^\Delta$는 IMU 측정 노이즈 $\boldsymbol{\eta}_k^d \doteq [\boldsymbol{\eta}_k^{ad}, \boldsymbol{\eta}_k^{gd}],\ k = 1,\cdots,j-1$의
선형 함수(linear function)으로 이루어져 있다고 볼 수 있다.== 이는 IMU 데이터시트로부터 얻은 $\boldsymbol{\eta}_k^d$의 공분산
값을 사용하여 선형 전파(linear propagation)을 통해 $\boldsymbol{\eta}_{ij}^\Delta$를 구할 수 있다는 것을 의미한다. 이러한 preintegrated
공분산을 $\boldsymbol{\Sigma}_{ij}$라고 부른다. Appendix IX-A를 보면 $\boldsymbol{\Sigma}_{ij}$를 계산하는 방법에 대해 자세히 설명한다. 이런 방법을 통해
새로운 IMU 측정값이 들어올 때마다 $\boldsymbol{\Sigma}_{ij}$를 매 번 새로 계산할 필요없이 이전 상태로부터 반복적(iterative)으로
상태를 업데이트할 수 있다.

<!--widget:noise-propagation-->

## 5.3 Incorporating bias updates

이전 섹션에서 preintegration을 수행하는 동안의 bias $\{\bar{\mathbf{b}}_i^a, \bar{\mathbf{b}}_i^g\}$는 값을 이미 알고 있으며 변하지 않는다고 설명하
였다. ==하지만 대부분의 경우 최적화를 하는 동안 bias 추정값은 작게 나마 $\delta\mathbf{b}$만큼 변한다.== 한가지 방법은 bias가
바뀔 때마다 preintegration 결과를 처음부터 다시 적분하는 것이다. 그러나 이는 계산 비용이 크므로 비효율적이다.
대신, bias를 $\mathbf{b} \leftarrow \bar{\mathbf{b}} + \delta\mathbf{b}$로 업데이트한다고 하면 다음과 같이 1차 선형 전개로 preintegration 측정값을 빠르게
갱신할 수 있다.

$$\begin{aligned}
\Delta\tilde{\mathbf{R}}_{ij}(\mathbf{b}_i^g) &\simeq \Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)\color{#a50000}{\mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}^g\right)} \\
\Delta\tilde{\mathbf{v}}_{ij}(\mathbf{b}_i^g, \mathbf{b}_i^a) &\simeq \Delta\tilde{\mathbf{v}}_{ij}(\bar{\mathbf{b}}_i^g, \bar{\mathbf{b}}_i^a) + \color{#a50000}{\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}_i^a} \\
\Delta\tilde{\mathbf{p}}_{ij}(\mathbf{b}_i^g, \mathbf{b}_i^a) &\simeq \Delta\tilde{\mathbf{p}}_{ij}(\bar{\mathbf{b}}_i^g, \bar{\mathbf{b}}_i^a) + \color{#a50000}{\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}_i^a}
\end{aligned} \tag{48}$$

위 갱신 과정은 SO(3)에서 바로 동작한다(회전식에 $\mathrm{Exp}(\cdot)$가 있는 이유). 자코비안 행렬 $\{\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}, \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g},\cdots\}$은
preintegration 시점의 bias $\bar{\mathbf{b}}$에서 계산한 값이며 bias 값이 변함에 따라 측정값이 얼마나 변하는지를 설명한다. 이
자코비안 행렬들은 상수로 간주되며 preintegration 중 미리 계산해둘 수 있다. 이 자코비안들의 유도는 [5.1] 섹션의
(큰 값+작은 섭동) 전개와 거의 동일하며 Appendix IX-B에 자세히 설명되어 있다.

<!--widget:bias-first-order-update-->

## 5.4 Preintegrated IMU factors

(42)의 preintegration 측정 모델과 1차 근사에서 측정 노이즈가 평균이 0이고 공분산이 $\boldsymbol{\Sigma}_{ij}$인 가우시안 분포를
따른다는 점을 사용하면 residual $\mathbf{r}_{\mathcal{I}_{ij}} \doteq [\mathbf{r}_{\Delta\mathbf{R}_{ij}}^\intercal, \mathbf{r}_{\Delta\mathbf{v}_{ij}}^\intercal, \mathbf{r}_{\Delta\mathbf{p}_{ij}}^\intercal]^\intercal \in \mathbb{R}^9$를 다음과 같이 쉽게 나타낼 수 있다.

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{R}_{ij}} &\doteq \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)\mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}^g\right)\right)^\intercal\mathbf{R}_i^\intercal\mathbf{R}_j\right) \\
\mathbf{r}_{\Delta\mathbf{v}_{ij}} &\doteq \mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) - \left[\Delta\tilde{\mathbf{v}}_{ij}(\bar{\mathbf{b}}_i^g, \bar{\mathbf{b}}_i^a) + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}^g + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}^a\right] \\
\mathbf{r}_{\Delta\mathbf{p}_{ij}} &\doteq \mathbf{R}_i^\intercal(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2) - \left[\Delta\tilde{\mathbf{p}}_{ij}(\bar{\mathbf{b}}_i^g, \bar{\mathbf{b}}_i^a) + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}^g + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}^a\right]
\end{aligned} \tag{49}$$

- 위 식에는 (48)에서 설명한 bias 갱신도 포함되어 있다

==[2.3] 섹션에서 설명한 "lift-solve-retract" 방법론에 따르면 매 가우스-뉴턴 반복마다 (49)의 파라미터를
변경(re-parameterized)해야 한다. 여기서 re-parameterization이란 기존의 비선형 절대 변수 대신 선형의
국소 증분량으로 문제를 다시 쓰는 것을 말한다.== 예를 들어, 회전 $\mathbf{R} \in SO(3)$은 비선형 공간에 존재하므로 $\mathbf{R} \to \boldsymbol{\theta}$
와 같이 선형 공간의 변수로 바꾸는 작업을 말한다 ($\mathbf{R} \approx \mathbf{R}_k\mathrm{Exp}(\delta\boldsymbol{\theta})$). 나머지 변수도 마찬가지로 국소 증분량으로
변경한다 ($\mathbf{v} \approx \mathbf{v}_k + \delta\mathbf{v},\ \mathbf{p} \approx \mathbf{p}_k + \delta\mathbf{p},\ \mathbf{b} \approx \mathbf{b}_k + \delta\mathbf{b}$).
==그 다음 "solve" 단계에서는 현재 추정값 주변에서 이 비용 함수를 선형화(linearize)해야 한다.== 선형화를
수월하게 하려면 위 residual들에 대한 자코비안의 해석적 표현을 미리 구해두는 것이 편리하며, 이는 Appendix
IX-C에서 유도하였다.

<!--widget:imu-residual-->

## 5.5 Bias model

IMU 모델 식 (29)를 소개할 때 bias는 시간에 따라 천천히 변하는 값이라고 설명하였다. 따라서 우리는 bias를
브라운 운동(brownian motion)으로 모델링할 수 있다.

$$\begin{aligned}
\dot{\mathbf{b}}^g(t) &= \boldsymbol{\eta}^{bg}, \\
\dot{\mathbf{b}}^a(t) &= \boldsymbol{\eta}^{ba}
\end{aligned} \tag{50}$$

연속된 두 키프레임 $i$와 $j$ 사이의 구간 $[t_i, t_j]$에서 (50)을 적분하면 다음과 같다.

$$\begin{aligned}
\mathbf{b}_j^g &= \mathbf{b}_i^g + \boldsymbol{\eta}^{bgd} \\
\mathbf{b}_j^a &= \mathbf{b}_i^a + \boldsymbol{\eta}^{bad}
\end{aligned} \tag{51}$$

- $\mathbf{b}_i^g \doteq \mathbf{b}^g(t_i),\ \mathbf{b}_i^a \doteq \mathbf{b}^a(t_i)$로 단순화

$\boldsymbol{\eta}^{bgd}, \boldsymbol{\eta}^{bad}$는 bias 노이즈의 이산화(discrete) 버전으로써 평균이 0이고 공분산이 각각 $\boldsymbol{\Sigma}^{bgd} \doteq \Delta t_{ij}\mathrm{Cov}(\boldsymbol{\eta}^{bg})$, $\boldsymbol{\Sigma}^{bad} \doteq$
$\Delta t_{ij}\mathrm{Cov}(\boldsymbol{\eta}^{ba})$이다.

$$\begin{aligned}
\boldsymbol{\eta}^{bgd} &\sim \mathcal{N}(0, \boldsymbol{\Sigma}^{bgd}) \\
\boldsymbol{\eta}^{bad} &\sim \mathcal{N}(0, \boldsymbol{\Sigma}^{bad})
\end{aligned} \tag{52}$$

모델 (51)은 팩터 그래프(factor graph)에 쉽게 포함될 수 있다. 모든 연속 키프레임 쌍에 대해 논문 식(26)에
추가되는 가산항으로 넣으면 된다.

$$\|\mathbf{r}^{b_{ij}}\|^2 \doteq \|\mathbf{b}_j^g - \mathbf{b}_i^g\|_{\boldsymbol{\Sigma}^{bgd}}^2 + \|\mathbf{b}_j^a - \mathbf{b}_i^a\|_{\boldsymbol{\Sigma}^{bad}}^2 \tag{53}$$

# 6 Structureless vision factor

# A Appendix

## A.1 Iterative noise propagation

이번 섹션에서는 앞서 [5.2] 섹션에서 논의되었던 preintegrated 노이즈의 공분산을 계산하는 과정에 대해 설명한
다. 식을 유도해보면 결국 노이즈의 공분산은 반복식 형태(iterative form)로 구할 수 있고 식 자체가 직관적이고
간결하므로 수식 해석이 용이하며 실시간 구현에 훨씬 유리하다.
상대 회전량에 대한 노이즈 (46)부터 살펴보자. $\delta\boldsymbol{\phi}_{ij}$를 반복식 형태로 만들기 위해 마지막 샘플 $k = j-1$ 항을
떼어내보자.

$$\begin{aligned}
\delta\boldsymbol{\phi}_{ij} &\simeq \sum_{k=i}^{j-1}\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t \\
&= \sum_{k=i}^{j-2}\Delta\tilde{\mathbf{R}}_{k+1j}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t + \overbrace{\Delta\tilde{\mathbf{R}}_{jj}^\intercal}^{\mathbf{I}_{3\times 3}}\mathbf{J}_r^{j-1}\boldsymbol{\eta}_{j-1}^{gd}\Delta t \\
&= \sum_{k=i}^{j-2}\overbrace{(\Delta\tilde{\mathbf{R}}_{k+1j-1}\Delta\tilde{\mathbf{R}}_{j-1j})}^{=\Delta\tilde{\mathbf{R}}_{k+1j}}{}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t + \mathbf{J}_r^{j-1}\boldsymbol{\eta}_{j-1}^{gd}\Delta t \\
&= \Delta\tilde{\mathbf{R}}_{j-1j}^\intercal\color{#a50000}{\sum_{k=i}^{j-2}\Delta\tilde{\mathbf{R}}_{k+1j-1}^\intercal\mathbf{J}_r^k\boldsymbol{\eta}_k^{gd}\Delta t} + \mathbf{J}_r^{j-1}\boldsymbol{\eta}_{j-1}^{gd}\Delta t \\
&= \Delta\tilde{\mathbf{R}}_{j-1j}^\intercal\color{#a50000}{\delta\boldsymbol{\phi}_{ij-1}} + \mathbf{J}_r^{j-1}\boldsymbol{\eta}_{j-1}^{gd}\Delta t
\end{aligned} \tag{54}$$

동일한 과정을 (47)에 대해서도 수행해보자

$$\begin{aligned}
\delta\mathbf{v}_{ij} &= \sum_{k=i}^{j-1}\left[-\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ik}\Delta t + \Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t\right] \\
&= \color{#a50000}{\sum_{k=i}^{j-2}\left[-\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ik}\Delta t + \Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t\right]} \\
&\qquad - \Delta\tilde{\mathbf{R}}_{ij-1}(\tilde{\mathbf{a}}_{j-1} - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ij-1}\Delta t + \Delta\tilde{\mathbf{R}}_{ij-1}\boldsymbol{\eta}_{j-1}^{ad}\Delta t \\
&= \color{#a50000}{\delta\mathbf{v}_{ij-1}} - \Delta\tilde{\mathbf{R}}_{ij-1}(\tilde{\mathbf{a}}_{j-1} - \mathbf{b}_i^a)^\wedge\delta\boldsymbol{\phi}_{ij-1}\Delta t + \Delta\tilde{\mathbf{R}}_{ij-1}\boldsymbol{\eta}_{j-1}^{ad}\Delta t
\end{aligned} \tag{55}$$

$$\begin{aligned}
\delta\mathbf{p}_{ij} &= \sum_{k=i}^{j-1}\left[\delta\mathbf{v}_{ik}\Delta t - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\boldsymbol{\phi}_{ik}\Delta t^2 + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t^2\right] \\
&= \color{#a50000}{\sum_{k=i}^{j-2}\left[\delta\mathbf{v}_{ik}\Delta t - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \mathbf{b}_i^a)^\wedge\boldsymbol{\phi}_{ik}\Delta t^2 + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ik}\boldsymbol{\eta}_k^{ad}\Delta t^2\right]} \\
&\qquad + \delta\mathbf{v}_{ij-1}\Delta t - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ij-1}(\tilde{\mathbf{a}}_{j-1} - \mathbf{b}_i^a)^\wedge\boldsymbol{\phi}_{ij-1}\Delta t^2 + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ij-1}\boldsymbol{\eta}_{j-1}^{ad}\Delta t^2 \\
&= \color{#a50000}{\delta\mathbf{p}_{ij-1}} + \delta\mathbf{v}_{ij-1}\Delta t - \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ij-1}(\tilde{\mathbf{a}}_{j-1} - \mathbf{b}_i^a)^\wedge\boldsymbol{\phi}_{ij-1}\Delta t^2 + \frac{1}{2}\Delta\tilde{\mathbf{R}}_{ij-1}\boldsymbol{\eta}_{j-1}^{ad}\Delta t^2
\end{aligned} \tag{56}$$

Preintegrated 노이즈와 IMU 측정 노이즈는 각각 $\boldsymbol{\eta}_{ik}^\Delta \doteq [\delta\boldsymbol{\phi}_{ik}, \delta\mathbf{v}_{ik}, \delta\mathbf{p}_{ik}]$, 그리고 $\boldsymbol{\eta}_k^d \doteq [\boldsymbol{\eta}_k^{ad}, \boldsymbol{\eta}_k^{gd}]$이다. 표기
의 편의를 위해 transpose를 생략하였으나 모두 열벡터이다. 이를 사용하여 위 식을 다시 작성하면 다음과 같은
컴팩트한 형태가 된다

$$\boldsymbol{\eta}_{ij}^\Delta = \mathbf{A}_{j-1}\boldsymbol{\eta}_{ij-1}^\Delta + \mathbf{B}_{j-1}\boldsymbol{\eta}_{j-1}^d \tag{57}$$

선형 모델 (57)과 IMU 측정 노이즈 $\boldsymbol{\eta}_k^d$의 공분산 $\boldsymbol{\Sigma}_\eta \in \mathbb{R}^{6\times 6}$를 사용하여 preintegrated 측정값의 공분산을
반복적(iterative)으로 쓸 수 있다.

$$\boldsymbol{\Sigma}_{ij} = \mathbf{A}_{j-1}\boldsymbol{\Sigma}_{ij-1}\mathbf{A}_{j-1}^\intercal + \mathbf{B}_{j-1}\boldsymbol{\Sigma}_\eta\mathbf{B}_{j-1}^\intercal \tag{58}$$

- 초기값: $\boldsymbol{\Sigma}_{ij} = \mathbf{0}_{9\times 9}$

## A.2 Bias correction via first-order updates

이번 섹션에서는 [5.3] 섹션에서 설명한 1차 근사 bias 보정식의 유도 과정에 대해 설명한다. 우선, 시간 $i$에서 bias
추정값 $\bar{\mathbf{b}}_i \doteq [\bar{\mathbf{b}}_i^g, \bar{\mathbf{b}}_i^a]$가 주어졌다고 하자. 이 때 계산해둔 preintegration 값들은 다음과 같이 나타낸다.

$$\begin{aligned}
\Delta\bar{\mathbf{R}}_{ij} &\doteq \Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i) \\
\Delta\bar{\mathbf{v}}_{ij} &\doteq \Delta\tilde{\mathbf{v}}_{ij}(\bar{\mathbf{b}}_i) \\
\Delta\bar{\mathbf{p}}_{ij} &\doteq \Delta\tilde{\mathbf{p}}_{ij}(\bar{\mathbf{b}}_i)
\end{aligned} \tag{59}$$

==이번 섹션의 목표는 bias 추정값이 바뀌었을 때 이 세 값을 다시 적분하지 않고 업데이트하는 공식을 만드는
것이다.== 새 bias 값이 $\hat{\mathbf{b}}_i \leftarrow \bar{\mathbf{b}}_i + \delta\mathbf{b}_i$와 같이 주어졌다고 하자. 여기서 $\delta\mathbf{b}_i$는 이전 값 $\bar{\mathbf{b}}_i$에 비해 작은 업데이트
값이다.
회전에 대해 bias 보정을 먼저 진행해보자. 핵심 아이디어는 $\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i)$를 =="이전 bias에서 preintegration 결과
$\Delta\bar{\mathbf{R}}_{ij}$ + 1차 보정"== 꼴로 쓰는 것이다. (39) 식을 활용해 $\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i)$를 전개하면 다음과 같다

$$\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i) = \prod_{k=i}^{j-1}\mathrm{Exp}\left(\left(\tilde{\boldsymbol{\omega}}_k - \hat{\mathbf{b}}_i^g\right)\Delta t\right) \tag{60}$$

여기에 $\hat{\mathbf{b}}_i = \bar{\mathbf{b}}_i + \delta\mathbf{b}_i$를 넣고 각 항에 1차 근사 (5)를 적용하면 아래와 같은 식이 나온다

$$\begin{aligned}
\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i) &= \prod_{k=i}^{j-1}\mathrm{Exp}((\tilde{\boldsymbol{\omega}}_k - (\bar{\mathbf{b}}_i^g + \delta\mathbf{b}_i^g))\Delta t) \\
&\simeq \prod_{k=i}^{j-1}\mathrm{Exp}((\tilde{\boldsymbol{\omega}}_k - \bar{\mathbf{b}}_i^g)\Delta t)\mathrm{Exp}\left(-\mathbf{J}_r^k\delta\mathbf{b}_i^g\Delta t\right)
\end{aligned} \tag{61}$$

그 다음으로 관계식 (12)을 사용하여 $\delta\mathbf{b}_i^g$가 들어간 항들을 끝으로 이동시키면 다음과 같다

$$\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i) = \Delta\bar{\mathbf{R}}_{ij}\prod_{k=i}^{j-1}\mathrm{Exp}\left(-\Delta\tilde{\mathbf{R}}_{k+1j}(\bar{\mathbf{b}}_i)^\intercal\mathbf{J}_r^k\delta\mathbf{b}_i^g\Delta t\right) \tag{62}$$

- $\Delta\bar{\mathbf{R}}_{ij} = \prod_{k=i}^{j-1}\mathrm{Exp}((\tilde{\boldsymbol{\omega}}_k - \bar{\mathbf{b}}_i^g)\Delta t)$

위 식에 1차 근사식 (8)을 반복적으로 적용하면 다음과 같은 결과를 얻는다

$$\begin{aligned}
\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i) &\simeq \Delta\bar{\mathbf{R}}_{ij}\color{#a50000}{\mathrm{Exp}\left(\sum_{k=i}^{j-1}-\Delta\tilde{\mathbf{R}}_{k+1j}(\bar{\mathbf{b}}_i)^\intercal\mathbf{J}_r^k\delta\mathbf{b}_i^g\Delta t\right)} \\
&= \Delta\bar{\mathbf{R}}_{ij}\color{#a50000}{\mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g\right)}
\end{aligned} \tag{63}$$

위 식을 보면 회전 preintegration $\Delta\tilde{\mathbf{R}}_{ij}(\hat{\mathbf{b}}_i)$은 "이전 값 $\Delta\tilde{\mathbf{R}}_{ij}$ x 작은 회전 보정" 형태로 갱신할 수 있으며 다시
적분할 필요가 없다는 것을 알 수 있다.
이제 속도항에 대해 같은 작업을 해보자.

$$\begin{aligned}
\Delta\tilde{\mathbf{v}}(\hat{\mathbf{b}}_i) &= \sum_{k=i}^{j-1}\Delta\tilde{\mathbf{R}}_{ik}(\hat{\mathbf{b}}_i)(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a - \delta\mathbf{b}_i^a)\Delta t \\
&= \sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}\mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ik}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g\right)(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a - \delta\mathbf{b}_i^a)\Delta t \\
&= \sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}\left(\mathbf{I} + \left(\frac{\partial\Delta\bar{\mathbf{R}}_{ik}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g\right)^\wedge\right)(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a - \delta\mathbf{b}_i^a)\Delta t \\
&= \Delta\bar{\mathbf{v}}_{ij}\color{#a50000}{-\sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}\Delta t\delta\mathbf{b}_i^a + \sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ik}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g\right)^\wedge(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a)\Delta t} \\
&= \Delta\bar{\mathbf{v}}_{ij}\color{#a50000}{-\sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}\Delta t\delta\mathbf{b}_i^a - \sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a)^\wedge\frac{\partial\Delta\bar{\mathbf{R}}_{ik}}{\partial\mathbf{b}^g}\Delta t\delta\mathbf{b}_i^g} \\
&= \Delta\bar{\mathbf{v}}_{ij}\color{#a50000}{+\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}_i^a + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g}
\end{aligned} \tag{64}$$

- $\Delta\bar{\mathbf{v}}_{ij} = \sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a)\Delta t$

결과를 보면 속도에 대한 선형 보정식으로 정리된다. 위치항에 대해서도 동일한 방식으로 유도하면 다음과 같다.

$$\Delta\tilde{\mathbf{p}}(\hat{\mathbf{b}}_i) = \Delta\bar{\mathbf{p}}_{ij}\color{#a50000}{+\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^a}\delta\mathbf{b}_i^a + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g} \tag{65}$$

정리하자면 (48)에 쓰이는 자코비안들은 다음과 같다

$$\boxed{\begin{aligned}
\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g} &= -\sum_{k=i}^{j-1}[\Delta\tilde{\mathbf{R}}_{k+1j}(\bar{\mathbf{b}}_i)^\intercal\mathbf{J}_r^k\Delta t] \\
\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^a} &= -\sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}\Delta t \\
\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g} &= -\sum_{k=i}^{j-1}\Delta\bar{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a)^\wedge\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\Delta t \\
\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^a} &= \sum_{k=i}^{j-1}\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^a}\Delta t - \frac{1}{2}\Delta\bar{\mathbf{R}}_{ik}\Delta t^2 \\
\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}^g} &= \sum_{k=i}^{j-1}\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}^g}\Delta t - \frac{1}{2}\Delta\bar{\mathbf{R}}_{ik}(\tilde{\mathbf{a}}_k - \bar{\mathbf{b}}_i^a)^\wedge\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\Delta t^2
\end{aligned}} \tag{66}$$

이 자코비안들은 ==새 IMU 측정값이 들어올 때마다 누적으로 계산해둘 수 있어서 최적화 중 bias가 바뀌면 1
차 보정만으로도 빠르게 $\Delta\tilde{\mathbf{R}}_{ij}, \Delta\tilde{\mathbf{v}}_{ij}, \Delta\tilde{\mathbf{p}}_{ij}$를 업데이트할 수 있다.== 단 bias 가 너무 크면 1차 근사 정확도가 떨어질
수 있으므로 해당 구간을 다시 적분하는 것이 안전하다.

## A.3 Jacobians of residual errors

이번 섹션에서는 (49) 식에 나오는 residual들의 자코비안 행렬들을 해석적으로 유도한다. 이 자코비안들은 GN
같은 반복 최적화를 할 때 필수적으로 사용된다(비용 함수 (28)을 최적화할 때 사용함).
최적화는 [2.3] 섹션에서 설명한 리프팅(lifting)을 써서 residual을 증분 함수로 만든 뒤 미분한다. 즉, 다음과
같이 리트랙션을 대입한다.

$$\boxed{\begin{aligned}
\mathbf{R}_i &\leftarrow \mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i), & \qquad \mathbf{R}_j &\leftarrow \mathbf{R}_j\mathrm{Exp}(\delta\boldsymbol{\phi}_j) \\
\mathbf{p}_i &\leftarrow \mathbf{p}_i + \mathbf{R}_i\delta\mathbf{p}_i, & \qquad \mathbf{p}_j &\leftarrow \mathbf{p}_j + \mathbf{R}_j\delta\mathbf{p}_j \\
\mathbf{v}_i &\leftarrow \mathbf{v}_i + \delta\mathbf{v}_i, & \qquad \mathbf{v}_j &\leftarrow \mathbf{v}_j + \delta\mathbf{v}_j \\
\delta\mathbf{b}_i^g &\leftarrow \delta\mathbf{b}_i^g + \delta\tilde{\mathbf{b}}_i^g, & \qquad \delta\mathbf{b}_i^a &\leftarrow \delta\mathbf{b}_i^a + \delta\tilde{\mathbf{b}}_i^a
\end{aligned}} \tag{67}$$

==이렇게 하면 residual이 벡터 공간의 함수가 되므로 자코비안을 쉽게 계산할 수 있다. 이제부터는 residual
을 $[\delta\boldsymbol{\phi}_i, \delta\mathbf{p}_i, \delta\mathbf{v}_i, \delta\boldsymbol{\phi}_j, \delta\mathbf{p}_j, \delta\mathbf{v}_j, \delta\tilde{\mathbf{b}}_i^g, \delta\tilde{\mathbf{b}}_i^a]$에 대해 미분한다.==

### A.3.1 Jacobians of $\mathbf{r}_{\Delta\mathbf{p}_{ij}}$

$\mathbf{r}_{\Delta\mathbf{p}_{ij}}$은 $\delta\tilde{\mathbf{b}}_i^g$와 $\delta\tilde{\mathbf{b}}_i^a$에 선형이므로 이들에 대한 자코비안은 (48)에서 쓴 bias 보정항이 그대로 된다. $\delta\boldsymbol{\phi}_j, \mathbf{v}_j$는 residual
에 등장하지 않으므로 모두 0이다. 다른 자코비안들에 대해 살펴보자

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{p}_i + \mathbf{R}_i\delta\mathbf{p}_i) &= \mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{R}_i\delta\mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) - C \\
&= \mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{p}_i) + \color{#a50000}{(-\mathbf{I}_{3\times 1})\delta\mathbf{p}_i}
\end{aligned} \tag{68}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{p}_j + \mathbf{R}_j\delta\mathbf{p}_j) &= \mathbf{R}_i^\intercal\left(\mathbf{p}_j + \mathbf{R}_j\delta\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) - C \\
&= \mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{p}_j) + \color{#a50000}{(\mathbf{R}_i^\intercal\mathbf{R}_j)\delta\mathbf{p}_j}
\end{aligned} \tag{69}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{v}_i + \delta\mathbf{v}_i) &= \mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \delta\mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) - C \\
&= \mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{v}_i) + \color{#a50000}{(-\mathbf{R}_i^\intercal\Delta t_{ij})\delta\mathbf{v}_i}
\end{aligned} \tag{70}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i)) &= (\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i))^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) - C \\
&= (\mathbf{I} - \delta\boldsymbol{\phi}_i^\wedge)\mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right) - C \\
&= \mathbf{r}_{\Delta\mathbf{p}_{ij}}(\mathbf{R}_i) + \color{#a50000}{\left(\mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right)\right)^\wedge\delta\boldsymbol{\phi}_i}
\end{aligned} \tag{71}$$

- $C \doteq \Delta\tilde{\mathbf{p}}_{ij} + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}_i^g}\delta\mathbf{b}_i^g + \frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}_i^a}\delta\mathbf{b}_i^a$

지금까지 구한 자코비안들을 한 번에 정리하면 다음과 같다.

$$\boxed{\begin{aligned}
\frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\boldsymbol{\phi}_i} &= \left(\mathbf{R}_i^\intercal\left(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_i\Delta t_{ij} - \frac{1}{2}\mathbf{g}\Delta t_{ij}^2\right)\right)^\wedge & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\boldsymbol{\phi}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\mathbf{p}_i} &= -\mathbf{I}_{3\times 1} & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\mathbf{p}_j} &= \mathbf{R}_i^\intercal\mathbf{R}_j \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\mathbf{v}_i} &= -\mathbf{R}_i^\intercal\Delta t_{ij} & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\mathbf{v}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^a} &= -\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}_i^a} & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{p}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^g} &= -\frac{\partial\Delta\bar{\mathbf{p}}_{ij}}{\partial\mathbf{b}_i^g}
\end{aligned}} \tag{72}$$

### A.3.2 Jacobians of $\mathbf{r}_{\Delta\mathbf{v}_{ij}}$

$\mathbf{r}_{\Delta\mathbf{v}_{ij}}$도 $\delta\tilde{\mathbf{b}}_i^g$와 $\delta\tilde{\mathbf{b}}_i^a$에 선형이므로 이들에 대한 자코비안은 (48)에서 쓴 bias 보정항이 그대로 된다. $\delta\boldsymbol{\phi}_j, \mathbf{p}_i, \mathbf{p}_j$는
residual에 등장하지 않으므로 모두 0이다. 다른 자코비안들에 대해 살펴보자

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{v}_{ij}}(\mathbf{v}_i + \delta\mathbf{v}_i) &= \mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \delta\mathbf{v}_i - \mathbf{g}\Delta t_{ij}) - D \\
&= \mathbf{r}_{\Delta\mathbf{v}}(\mathbf{v}_j)\color{#a50000}{-\mathbf{R}_i^\intercal\delta\mathbf{v}_i}
\end{aligned} \tag{73}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{v}_{ij}}(\mathbf{v}_j + \delta\mathbf{v}_j) &= \mathbf{R}_i^\intercal(\mathbf{v}_j + \delta\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) - D \\
&= \mathbf{r}_{\Delta\mathbf{v}}(\mathbf{v}_j) + \color{#a50000}{\mathbf{R}_i^\intercal\delta\mathbf{v}_j}
\end{aligned} \tag{74}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{v}_{ij}}(\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i)) &= (\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i))^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) - D \\
&= (\mathbf{I} - \delta\boldsymbol{\phi}_i^\wedge)\mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij}) - D \\
&= \mathbf{r}_{\Delta\mathbf{v}}(\mathbf{R}_i) + \color{#a50000}{\left(\mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij})\right)^\wedge\delta\boldsymbol{\phi}_i}
\end{aligned} \tag{75}$$

- $D \doteq \left[\Delta\tilde{\mathbf{v}}_{ij} + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}_i^g}\delta\mathbf{b}_i^g + \frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}_i^a}\delta\mathbf{b}_i^a\right]$

지금까지 구한 자코비안들을 한 번에 정리하면 다음과 같다.

$$\boxed{\begin{aligned}
\frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\boldsymbol{\phi}_i} &= \left(\mathbf{R}_i^\intercal(\mathbf{v}_j - \mathbf{v}_i - \mathbf{g}\Delta t_{ij})\right)^\wedge & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\boldsymbol{\phi}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\mathbf{p}_i} &= 0 & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\mathbf{p}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\mathbf{v}_i} &= -\mathbf{R}_i^\intercal & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\mathbf{v}_j} &= \mathbf{R}_i^\intercal \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^a} &= -\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}_i^a} & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{v}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^g} &= -\frac{\partial\Delta\bar{\mathbf{v}}_{ij}}{\partial\mathbf{b}_i^g}
\end{aligned}} \tag{76}$$

### A.3.3 Jacobians of $\mathbf{r}_{\Delta\mathbf{R}_{ij}}$

$\mathbf{p}_i, \mathbf{p}_j, \mathbf{v}_i, \mathbf{v}_j, \delta\mathbf{b}_i^a$는 residual에 등장하지 않으므로 모두 0이다. 나머지에 대한 편미분을 전개하면 다음과 같다

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i)) &= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)E\right)^\intercal(\mathbf{R}_i\mathrm{Exp}(\delta\boldsymbol{\phi}_i))^\intercal\mathbf{R}_j\right) \\
&= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)E\right)^\intercal\mathrm{Exp}(-\delta\boldsymbol{\phi}_i)\mathbf{R}_i^\intercal\mathbf{R}_j\right) \\
&= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)E\right)^\intercal\mathbf{R}_i^\intercal\mathbf{R}_j\mathrm{Exp}(-\mathbf{R}_j^\intercal\mathbf{R}_i\delta\boldsymbol{\phi}_i)\right) \\
&= \mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_i)\color{#a50000}{-\mathbf{J}_r^{-1}(\mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_i))\mathbf{R}_j^\intercal\mathbf{R}_i\delta\boldsymbol{\phi}_i}
\end{aligned} \tag{77}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\mathbf{R}_j\mathrm{Exp}(\delta\boldsymbol{\phi}_j)) &= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)E\right)^\intercal\mathbf{R}_i^\intercal(\mathbf{R}_j\mathrm{Exp}(\delta\boldsymbol{\phi}_j))\right) \\
&= \mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_j)\color{#a50000}{+\mathbf{J}_r^{-1}(\mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_j))\delta\boldsymbol{\phi}_j}
\end{aligned} \tag{78}$$

$$\begin{aligned}
\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g + \delta\tilde{\mathbf{b}}_i^g) &= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)\mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}(\delta\mathbf{b}_i^g + \delta\tilde{\mathbf{b}}_i^g)\right)\right)^\intercal\mathbf{R}_i^\intercal\mathbf{R}_j\right) \\
&= \mathrm{Log}\left(\left(\Delta\tilde{\mathbf{R}}_{ij}(\bar{\mathbf{b}}_i^g)\ E\ \mathrm{Exp}\left(\mathbf{J}_r^b\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\tilde{\mathbf{b}}_i^g\right)\right)^\intercal\mathbf{R}_i^\intercal\mathbf{R}_j\right) \\
&= \mathrm{Log}\left(\mathrm{Exp}\left(-\mathbf{J}_r^b\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\tilde{\mathbf{b}}_i^g\right)(\Delta\tilde{\mathbf{R}}(\bar{\mathbf{b}}_i^g)E)^\intercal\mathbf{R}_i^\intercal\mathbf{R}_j\right) \\
&= \mathrm{Log}\left(\mathrm{Exp}\left(-\mathbf{J}_r^b\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\tilde{\mathbf{b}}_i^g\right)\mathrm{Exp}\left(\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g)\right)\right) \\
&= \mathrm{Log}\left(\mathrm{Exp}(\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g)) \cdot \mathrm{Exp}\left(-\mathrm{Exp}(\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g))^\intercal\mathbf{J}_r^b\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\tilde{\mathbf{b}}_i^g\right)\right) \\
&= \mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g)\color{#a50000}{-\mathbf{J}_r^{-1}(\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g))\mathrm{Exp}(\mathbf{r}_{\Delta\mathbf{R}_{ij}}(\delta\mathbf{b}_i^g))^\intercal\mathbf{J}_r^b\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\tilde{\mathbf{b}}_i^g}
\end{aligned} \tag{79}$$

- $E \doteq \mathrm{Exp}\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}^g\right)$
- $\mathbf{J}_r^b = \mathbf{J}_r\left(\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}\delta\mathbf{b}_i^g\right)$

지금까지 구한 자코비안들을 한 번에 정리하면 다음과 같다.

$$\boxed{\begin{aligned}
\frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\boldsymbol{\phi}_i} &= -\mathbf{J}_r^{-1}(\mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_i))\mathbf{R}_j^\intercal\mathbf{R}_i & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\boldsymbol{\phi}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\mathbf{p}_i} &= 0 & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\mathbf{p}_j} &= \mathbf{J}_r^{-1}(\mathbf{r}_{\Delta\mathbf{R}}(\mathbf{R}_j)) \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\mathbf{v}_i} &= 0 & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\mathbf{v}_j} &= 0 \\
\frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^a} &= 0 & \qquad \frac{\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}}{\partial\delta\tilde{\mathbf{b}}_i^g} &= -\mathbf{J}_r^{-1}\left(\mathbf{r}_{\Delta\mathbf{R}}(\delta\mathbf{b}_i^g)\right)\mathrm{Exp}\left(\mathbf{r}_{\Delta\mathbf{R}}(\delta\mathbf{b}_i^g)\right)^\intercal\mathbf{J}_r^b\frac{\partial\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}
\end{aligned}} \tag{80}$$

<!--widget:residual-jacobians-->

## A.4 Structureless vision factors: null space projection

## A.5 Rotation rate integration using euler angles

이번 섹션에서는 오일러 각 파라미터화로 인해 IMU 각속도 측정값을 적분하는 방법에 대해 설명한다. 시간 $k$의
각속도 측정값을 $\tilde{\boldsymbol{\omega}}_k$, 그에 대응하는 노이즈를 $\boldsymbol{\eta}_k^g$라고 하자. 또한 시간 $k$의 오일러 각 벡터를 $\boldsymbol{\theta}_k \in \mathbb{R}^3$라고 하면 $\tilde{\boldsymbol{\omega}}_k$
를 적분하여 다음 스텝의 오일러 각 $\boldsymbol{\theta}_{k+1}$을 다음과 같이 얻을 수 있다.

$$\boldsymbol{\theta}_{k+1} = \boldsymbol{\theta}_k + [E'(\boldsymbol{\theta}_k)]^{-1}(\tilde{\boldsymbol{\omega}}_k - \boldsymbol{\eta}_k^g)\Delta t \tag{81}$$

- $E'(\boldsymbol{\theta}_k)$ : =="conjugate 오일러 각속도 행렬"==이라고 부르며 오일러 각속도와 몸체(body)의 각속도를 연결하는
행렬이다

$E'(\boldsymbol{\theta}_k)$는 몸체 각속도 → 오일러 각속도로 변환하는 행렬이므로 그 역행렬로 각속도를 적분하여 오일러 각을
업데이트한다. $\boldsymbol{\theta}_{k+1}$의 공분산은 1차 선형화로 다음과 같이 계산할 수 있다.

$$\boldsymbol{\Sigma}_{k+1}^{\mathrm{Euler}} = \mathbf{A}_k\boldsymbol{\Sigma}_k^{\mathrm{Euler}}\mathbf{A}_k^\intercal + \mathbf{B}_k\boldsymbol{\Sigma}_\eta\mathbf{B}_k^\intercal \tag{82}$$

- $\mathbf{A}_k \doteq \mathbf{I}_{3\times 3} + \frac{\partial[E'(\boldsymbol{\theta}_k)]^{-1}}{\partial\boldsymbol{\theta}_k}\Delta t$
- $\mathbf{B}_k \doteq -[E'(\boldsymbol{\theta}_k)]^{-1}\Delta t$
- $\boldsymbol{\Sigma}_\eta$ : 관측 노이즈 $\boldsymbol{\eta}_k^{gd}$의 공분산

일반적인 공분산의 전파 공식을 사용하면 위와 같은 식이 나온다. 단, 오일러 각은 짐벌락이 있을 수 있으니 큰
회전에는 SO(3) 기반 적분을 쓰는 것이 보통 더 안정적이다

<!--widget:euler-vs-so3-->

# B References

[1] Forster, Christian, et al. "On-manifold preintegration for real-time visual-inertial odometry." IEEE Transactions on Robotics 33.1 (2016): 1-21.

# C Revision log

- 1st: 2024-11-27
- 2nd: 2024-11-30
- 3rd: 2025-07-25 : Preintegrated IMU measurements 섹션 작성
- 4th: 2025-07-26 : Bias model 섹션까지 작성
- 5th: 2025-07-27 : Preliminaries 섹션 작성
- 6th: 2025-07-28 : Appendix 작성

# 옮기며 바로잡은 것

원문에서 명백한 오타로 보이는 것만 고쳤다. 아래가 전부이며, 그 밖의 표현·기호·문장 순서는
원문 그대로 두었다.

## 고친 것

| # | 원문 쪽 · 위치 | 원문 | 고친 것 |
|---|---|---|---|
| 1 | p2 · 2장 첫 문단 | 회전, 포즈**과** 같은 | 포즈**와** 같은 |
| 2 | p2 · 2.1.1 | 전치(**tranpose**)함으로써 | 전치(**transpose**)함으로써 |
| 3 | p2 · 2.1.1 (6) 위 | lie **albegra** so(3) | lie **algebra** so(3) |
| 4 | p11 · 5.3 첫 문장 | **preintegrationd**을 수행하는 | **preintegration**을 수행하는 |
| 5 | p11 · 5.3 끝 | 계산해둘 수 있다**.이** 자코비안들의 | 계산해둘 수 있다**. 이** 자코비안들의 |
| 6 | p17 · 식 (80) 좌하 | $\partial\mathbf{r}_{\Delta\mathbf{R}\mathbf{v}_{ij}}/\partial\delta\tilde{\mathbf{b}}_i^a = 0$ | $\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}/\partial\delta\tilde{\mathbf{b}}_i^a = 0$ |

## 원문 그대로 둔 것

고칠지 망설였지만 손대면 원문의 유도 과정을 바꾸게 되므로 그대로 옮긴 것들이다. 읽을 때
참고하라고 적어 둔다.

| # | 원문 쪽 · 위치 | 내용 |
|---|---|---|
| 1 | p2 · 식 (6) | $\varphi = \cos^{-1}\left(\frac{\mathrm{tr}(\mathbf{R}-1)}{2}\right)$ — 관례상 $\frac{\mathrm{tr}(\mathbf{R})-1}{2}$ 이다 |
| 2 | p3 · 식 (14) | $\epsilon \sim (0,\Sigma)$ — 바로 아래 설명은 "정규분포"라고 하므로 $\mathcal{N}(0,\Sigma)$ 를 뜻한다 |
| 3 | p4 · (15) 아래 문장 | $\epsilon = \mathrm{Log}(\mathbf{R}^{-1}\mathbf{R})$ — (16)부터는 $\mathrm{Log}(\mathbf{R}^{-1}\tilde{\mathbf{R}})$ 로 쓴다 |
| 4 | p6 · 식 (28) | $\|\mathbf{r}_0\|_{\boldsymbol{\Sigma}_0^2}^2$ 처럼 $\boldsymbol{\Sigma}$ 에도 제곱이 붙어 있다. $\boldsymbol{\Sigma}_C$ 항만 제곱이 없다 |
| 5 | p6 · (28) 설명 | 본문은 $\boldsymbol{\Sigma}_c$(소문자), 식은 $\boldsymbol{\Sigma}_C$(대문자) |
| 6 | p7 · 식 (32) 3행 | ${}_{W}\mathbf{a}\Delta t^2$ — (31)의 이중적분을 상수 가속도로 풀면 $\frac{1}{2}{}_{W}\mathbf{a}\Delta t^2$ 이고, 실제로 (33)부터는 $\frac{1}{2}$ 이 붙는다 |
| 7 | p8 · 식 (37) 3행 | $\Delta\mathbf{p}_{ij} \doteq \mathbf{R}_i^\intercal(\mathbf{p}_j - \mathbf{p}_i - \mathbf{v}_k\Delta t_{ij} - \cdots)$ — 문맥상 $\mathbf{v}_i$ 이며 (42)에서는 $\mathbf{v}_i$ 로 쓴다 |
| 8 | p9 · 식 (40) 1행 | $(\mathbf{I} - \delta\boldsymbol{\phi}_{ij})$ — $\wedge$ 가 빠져 있다. (41)에서는 $(\mathbf{I} - \delta\boldsymbol{\phi}_{ik}^\wedge)$ 로 쓴다 |
| 9 | p9 · 식 (40)(41) | 첨자가 $\delta\boldsymbol{\phi}_{ij}$ 인데 합 안의 항은 $k$ 에 대한 것이라 (47)에서는 $\delta\boldsymbol{\phi}_{ik}$ 로 바뀐다 |
| 10 | p12 · 식 (56) | $\boldsymbol{\phi}_{ik}$ — (47)과 맞추면 $\delta\boldsymbol{\phi}_{ik}$ 이다 |
| 11 | p14 · 식 (64) 3행 | $\Delta\bar{\mathbf{R}}$ — 다른 행과 맞추면 $\Delta\bar{\mathbf{R}}_{ik}$ 이다 |
| 12 | p15 · 식 (66) 3·5행 | $\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}$ — 합 안이므로 $\frac{\partial\Delta\bar{\mathbf{R}}_{ik}}{\partial\mathbf{b}^g}$ 이 맞다 ((64) 유도가 그렇다) |
| 13 | p15 · 식 (68)(72) | $-\mathbf{I}_{3\times 1}$ — 3×3 항등행렬이므로 $\mathbf{I}_{3\times 3}$ 이다 |
| 14 | p16 · 식 (73) | 좌변은 $\mathbf{r}_{\Delta\mathbf{v}_{ij}}(\mathbf{v}_i + \delta\mathbf{v}_i)$ 인데 우변 상수항이 $\mathbf{r}_{\Delta\mathbf{v}}(\mathbf{v}_j)$ 로 적혀 있다 |
| 15 | p17 · 식 (80) 우2행 | $\partial\mathbf{r}_{\Delta\mathbf{R}_{ij}}/\partial\delta\mathbf{p}_j = \mathbf{J}_r^{-1}(\cdots)$ — (78)의 유도로 보면 $\partial\delta\boldsymbol{\phi}_j$ 에 대한 값이다 |
| 16 | p17 · 식 (80) 우4행 | $\frac{\partial\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}$ — 다른 곳은 모두 $\frac{\partial\Delta\bar{\mathbf{R}}_{ij}}{\partial\mathbf{b}^g}$ 이다 |
| 17 | 전체 | 전치 기호로 $\intercal$ 를 쓰는데, 굵은 글씨 안팎에서 모양이 조금씩 다르다 |
