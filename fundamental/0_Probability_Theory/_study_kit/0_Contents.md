# Notes on Probability Theory — 학습 목차

원문: Gyubeom Edward Im, *Notes on Probability Theory* (45쪽) — `ref/Notes on Probability Theory.pdf`
페이지 오프셋 0 (PDF 쪽 = 인쇄 쪽번호). 아래 쪽번호는 원문에 인쇄된 번호다.

학습 목표: 측도론 기반의 확률 정의에서 출발해 확률변수·분포·모멘트를 정리하고, 가우시안 분포의
조건부/주변 성질을 거쳐 랜덤프로세스와 Gaussian Process Regression까지 간다.

> **이 스터디의 결과물은 챕터별 노트가 아니라 원문 전체를 그대로 옮긴 단일 문서다.**
> `notes/notes_on_probability_theory.md` 하나에 13개 장이 모두 들어 있고, 빌드하면 같은 폴더에
> `notes_on_probability_theory.html`이 나온다. 위젯 11개가 절 사이에 삽입되어 있다.

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 Introduction | ✅ | — | — |
| 2 Set theory | ✅ | 2 (p.5) | — |
| 3 Measure theory | ✅ | — | — |
| 4 Probability | ✅ | 2 (p.8, p.10) | 2 (독립vs배반, Bayes) |
| 5 Random variables | ✅ | 2 (p.11, p.12) | — |
| 6 Probability distribution | ✅ | — | 3 (이산·연속·joint/marginal/conditional) |
| 7 Moment | ✅ | 1 (p.24) | 1 (공분산·상관계수) |
| 8 More on Gaussian distribution | ✅ | 1 (p.25) | 2 (CLT, 조건부 가우시안) |
| 9 Random Process | ✅ | 4 (p.30, p.31×2, p.33) | 1 (Wiener process) |
| 10 Gaussian Process | ✅ | — | 1 (GP 표집) |
| 11 Gaussian Process Regression | ✅ | — | 1 (GPR) |
| 12 References | ✅ | — | — |
| 13 Revision log | ✅ | — | — |

---

## 1장. Introduction (p.3)

## 2장. Set theory (p.4)
- 2.1 Cardinality (4)
- 2.2 Function (5)

## 3장. Measure theory (p.6)
- 3.1 σ-field (6)
  - 3.1.1 Properties of σ-field (6)
- 3.2 Measurable space (7)

## 4장. Probability (p.7)
- 4.1 Random experiment (7)
- 4.2 Probability axioms (8)
- 4.3 Probability allocation function (8)
  - 4.3.1 Discrete sample space Ω: (9)
  - 4.3.2 Continuous sample space Ω: (9)
- 4.4 Independence ≠ disjoint (9)
- 4.5 Joint probability (10)
- 4.6 Marginal probability (10)
- 4.7 Conditional probability (10)
- 4.8 Bayesian rule (11)

## 5장. Random variables (p.11)
- 5.1 Discrete random variable (12)
- 5.2 Continuous random variable (12)

## 6장. Probability distribution (p.12)
- 6.1 Discrete probability distribution (13)
  - 6.1.1 Bernoulli distribution (13)
  - 6.1.2 Binomial distribution (13)
  - 6.1.3 Geometric distribution (14)
  - 6.1.4 Negative binomial distribution (14)
  - 6.1.5 Poisson distribution (15)
- 6.2 Continuous probability distribution (16)
  - 6.2.1 Uniform distribution (16)
  - 6.2.2 Gaussian distribution (16)
  - 6.2.3 Chi-square distribution (17)
  - 6.2.4 Exponential distribution (18)
  - 6.2.5 Gamma distribution (18)
  - 6.2.6 Beta distribution (19)
- 6.3 Joint probability distribution (20)
- 6.4 Marginal probability distribution (20)
- 6.5 Conditional probability distribution (20)
- 6.6 Bayesian rule (21)

## 7장. Moment (p.21)
- 7.1 Expectation (22)
  - 7.1.1 Properties of expectation (22)
  - 7.1.2 Conditional expectation (22)
  - 7.1.3 Law of total expectation (22)
- 7.2 Variance and standard deviation (23)
- 7.3 Covariance and correlation (23)
  - 7.3.1 Correlation coefficient (24)
- 7.4 Orthogonal (24)

## 8장. More on Gaussian distribution (p.25)
- 8.1 Central limit theorem (25)
- 8.2 Multivariate gaussian distribution (25)
- 8.3 Joint gaussian distribution (26)
- 8.4 Conditional gaussian distribution (26)
  - 8.4.1 Derivation of conditional gaussian distribution (26)
- 8.5 Linear transformation of gaussian random variable (28)
- 8.6 Marginalization and conditioning is also gaussian (29)

## 9장. Random Process (p.30)
- 9.1 Definition of random process (32)
  - 9.1.1 Kolmogorov existence theorem (33)
- 9.2 Types of random process (33)
- 9.3 Wiener process (a.k.a Brownian motion) (34)
- 9.4 Moment (34)
  - 9.4.1 Mean function (34)
  - 9.4.2 Auto-correlation function (ACF) (34)
  - 9.4.3 Auto-covariance function (ACVF) (34)
  - 9.4.4 Cross-covariance function (CCVF) (35)
  - 9.4.5 Momentum on gaussian process (35)
- 9.5 Stationary (35)
  - 9.5.1 Strict-sense stationary (SSS) (35)
  - 9.5.2 Wide-sense stationary (WSS) (35)

## 10장. Gaussian Process (p.36)
- 10.1 Toy example of gaussian process (37)

## 11장. Gaussian Process Regression (p.38)
- 11.1 Weight-space view (38)
  - 11.1.1 Linear regression (MLE) (38)
  - 11.1.2 Bayesian linear regression (MAP) (39)
  - 11.1.3 Gaussian process regression (40)
  - 11.1.4 Predictive distribution (40)
  - 11.1.5 Kernel trick (40)
- 11.2 Function-space view (42)
- 11.3 Pros and cons of GPR (44)
  - 11.3.1 Pros (44)
  - 11.3.2 Cons (44)

## 12장. References (p.44)

## 13장. Revision log (p.45)

---

## 추천 학습 순서

원문 순서 그대로 읽으면 된다. 의존 관계가 1 → 13으로 곧게 흐른다.

1. 1~5장 — 측도론에서 확률변수까지. 3장은 뒤 내용의 전제가 아니므로 가볍게 지나가도 된다
2. 6~7장 — 분포 카탈로그와 모멘트. 위젯 3·4로 분포를 직접 흔들어 보는 것이 빠르다
3. 8장 — 조건부 가우시안 유도(8.4.1)가 이 문서의 첫 번째 고비. 11장 GPR의 뼈대가 된다
4. 9~10장 — 확률변수를 무한차원으로 확장해 랜덤프로세스와 GP로
5. 11장 — GPR. weight-space view(11.1)와 function-space view(11.2)가 같은 식 (151)=(162)에
   도달하는 것을 확인하는 것이 목표

## 참고 — 이 문서의 특이사항

- **그림 캡션이 하나도 없다.** `Figure`/`Table`이 전문에 0회 등장한다. 따라서 `extract_figures.py`
  대신 `tools/extract_images_bbox.py`(이 스터디에서 추가)가 이미지 객체 bbox로 12개를 뽑는다
- 번호 붙은 수식이 (1)~(162)까지 있다. 노트가 이를 그대로 유지하므로 원문 PDF와 나란히 놓고 볼 수 있다
- 원문 오타를 바로잡은 목록은 노트 맨 아래 "옮기며 바로잡은 것"에 있다
