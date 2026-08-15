# 스터디 자료 작성 템플릿 & 규칙

모든 챕터(`partX_.../0N_.../0N_*.md`)는 아래 3단 구조와 규칙을 따른다.
기준 예시: Bayes' theorem (2장 Recursive State Estimation) 초안.

---

## 템플릿 구조

```
## 1. 개념적 이해

(한국어 설명. 새로 등장하는 용어는 처음 나올 때 "한국어 설명(English term)" 형태로 병기.
 수식은 최소화하고 비유/직관 위주로 서술.)

## 2. 수식/유도

### 전체 유도 과정 (먼저 한 번에)

(관련된 수식 전체를 (1), (2), (3)... 번호를 매겨 설명 없이 연속으로 먼저 제시)

### 단계별 설명 (생략 없이)

**(1) ...**
(수식 (1)에 대한 설명)

**(2) ...**
(수식 (2)에 대한 설명. 이 유도에서 처음 쓰이는 도구/개념이 있으면
 그 개념을 먼저 설명하고 나서 수식으로 연결 — 아래 "생략 금지 규칙" 참조)

...

## 3. 예제/실습

(구체적 숫자를 사용한 예제. 계산 과정 전 단계 표시.
 가능하면 책에 나온 예제를 우선 사용. 마지막에 연습문제 또는 짧은 코드 스니펫.)
```

---

## 언어 규칙

- **섹션 1 (개념적 이해)**: 한국어 설명 + 원본 영단어 병기. 예: "사전 확률(prior)", "가능도(likelihood)". 한글 번역이 어색하거나 못 알아볼 수 있는 용어는 병기를 통해 원문을 같이 남긴다.
- **섹션 2, 3 (수식/유도, 예제/실습)**: 수학적·전문 용어는 한국어로 억지로 번역하지 않고 영어를 그대로 사용한다 (예: conditional probability, marginalization, joint probability, likelihood, posterior, prior, normalizer). 문장 자체는 한국어로 서술하되 용어는 영어.

### 절대 번역하지 않는 용어 (섹션 1 포함, 전 구간)

아래 용어들은 한국어 번역어가 어색하거나 잘 쓰이지 않으므로 **영어를 그대로 쓴다.** 괄호 병기도 하지 않는다.

| 쓸 것 | 쓰지 말 것 |
|---|---|
| unimodal / multi-modal / bimodal | 단봉 / 다봉 / 이봉 |
| mode | 봉우리 (분포의 최빈값을 뜻할 때) |
| innovation | 혁신 |
| Kalman gain | 칼만 이득 |
| Jacobian | 야코비안 |
| marginalization | 주변화 |
| canonical / moments / natural parameterization | 정준 / 모멘트 / 자연 파라미터화 |
| bijective mapping | 전단사 사상 |
| point mass distribution | 점 질량 분포 |
| perception (명사) | 지각 |
| odometer | 주행거리계 |
| projection (명사) | 사영 |
| prior / posterior / likelihood / belief | (첫 등장 시 "사전 확률(prior)"처럼 병기하는 것은 허용, 이후에는 영어) |
| ray casting | 광선 투사 (첫 등장 시 1회 병기만 허용) |
| likelihood field | 가능도장 / 우도장 |
| beam model / beam | 빔 모델 (모델명은 영어, 일반 명사 "빔"은 허용) |
| correspondence / correspondence variable | 대응 변수 |
| signature | 서명 / 특징값 |
| feature / feature-based / location-based | 특징 / 특징 기반 / 위치 기반 |
| occupancy grid map | 점유 격자 지도 |
| map matching | 지도 정합 |
| free-space | 자유 공간 |
| specular reflection | (첫 등장 시 "정반사(specular reflection)" 병기 허용, 이후 영어) |
| range / bearing | 거리 / 방위각 (측정량 이름일 때는 영어) |
| overconfidence / overconfident | 과신 (첫 등장 시 병기 허용) |
| max-range reading | 최대 거리 읽기 |
| intrinsic parameter | 내재 파라미터 |
| E-step / M-step / EM | (EM은 첫 등장 시 "expectation maximization" 전개만) |
| position tracking | 위치 추적 |
| global localization | 전역 위치추정 |
| kidnapped robot problem | 납치된 로봇 문제 (첫 등장 시 병기 허용) |
| Markov localization | 마르코프 위치추정 |
| localization | 위치추정 (첫 등장 시 병기 허용, 이후 영어) |
| data association | 데이터 연관 (첫 등장 시 병기 허용) |
| mutual exclusion principle | 상호 배제 원리 (첫 등장 시 병기 허용) |
| negative information | 부정 정보 |
| mixture weight / track (MHT) | 혼합 가중치 / 트랙 |
| pruning | 가지치기 (첫 등장 시 병기 허용) |
| state augmentation | 상태 증강 (첫 등장 시 병기 허용) |
| passive / active localization | 수동 / 능동 |
| innovation vector | innovation 벡터 (innovation은 절대 번역하지 않음) |

**7장에서 추가로 한국어를 쓰는 것**: 추측 항법(dead reckoning), 좌표 변환, 회전행렬, 정규분포,
불확실성 타원, 시그마 포인트, 랜드마크.

### 8장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| grid localization | 격자 위치추정 (알고리즘 이름이므로 영어) |
| Monte Carlo localization / MCL | 몬테카를로 위치추정 |
| resampling | 재표집 (첫 등장 시 병기 허용) |
| importance weight / importance factor | 중요도 가중치 (첫 등장 시 병기 허용) |
| topological / metric representation | 위상적 / 미터법 표현 (첫 등장 시 병기 허용) |
| model pre-caching | 모델 사전 캐싱 |
| sensor subsampling | 센서 부분표집 |
| delayed motion updates | 지연 운동 갱신 |
| selective updating | 선택적 갱신 |
| catastrophic failure | 파국적 실패 (첫 등장 시 병기 허용) |
| injection of random particles | 랜덤 particle 주입 (particle은 영어) |
| Mixture MCL / mixture proposal distribution | 혼합 MCL |
| KLD-sampling | KLD 표집 |
| Kullback-Leibler divergence | (첫 등장 시 전개만, 이후 KL divergence) |
| outlier rejection | 이상치 기각 (첫 등장 시 병기 허용) |
| bin (histogram) | 구간 / 통 |
| particle deprivation / depletion | particle 고갈 (particle은 영어) |

**8장에서 추가로 한국어를 쓰는 것**: 분할(partition), 질량중심, 엔트로피, 신뢰수준, 분위수,
지수 이동 평균, 대칭성.

**반면 아래는 한국어가 표준이므로 그대로 쓴다**: 공분산, 결합확률, 조건부확률, 정규분포, 확률변수, 기댓값,
전확률 정리, 충분통계량, 곡률, 귀납법, 정방행렬, 편미분, 항등식, 정규화 상수, 랜드마크, 시그마 포인트.

### 명사만 금지하는 항목 — 동사·형용사형은 한국어를 쓴다

위 표의 **perception**과 **projection**은 **명사일 때만** 금지한다. 원문의 동사·형용사를 옮긴 서술까지
영어로 바꾸면 오히려 읽기 나빠지기 때문이다.

| 원문 | 노트에 쓸 것 | 쓰지 말 것 |
|---|---|---|
| 명사 `perception` | **perception** ("로봇 perception 문제는 state estimation 문제다") | 지각 |
| 동사 `perceive` / 형용사 `perceptual` | **지각하다 / 지각 영역** ("센서는 지각할 수 있는 것이 제한된다") | perceive하다 |
| 명사 `projection` | **projection** | 사영 |
| 동사 `project` | **투영하다** ("측정을 $x$-$y$ 공간으로 투영한다") | 사영하다 |

**"투영"은 허용한다** — `projection`의 표준 번역어이며, 노트 전체가 이미 이 표기로 통일되어 있다.
금지 대상은 어색한 번역어인 **"사영"** 이다.

> 2026-08-15 점검에서 이 경계가 모호해 혼란이 있었다. 당시 `봉우리`(mode) 24건, `사영` 6건,
> `다봉` 1건을 각각 `mode`·`투영`·`multi-modal`로 정정했고, 동사형 `지각하다` 6건은 위 기준에 따라
> 위반이 아닌 것으로 판정해 그대로 두었다.

**판단 기준**: 한국어 로보틱스·통계 교재에서 그 번역어가 실제로 통용되는가? 아니라면 영어를 쓴다.
새로운 용어가 등장할 때마다 이 표를 갱신한다.

## 수식/유도 규칙 (생략 금지)

1. 해당 개념/알고리즘과 관련된 유도 전체를 번호를 매겨(`(1)`, `(2)`, ...) **설명 없이 먼저 통으로 보여준다.**
2. 그 다음, 번호별로 하나씩 짚어가며 설명한다. 이때:
   - 결과 수식만 제시하지 않고, **왜 그 수식이 나오는지**(정의 적용, 이전 단계 대입, 항등식 변형 등)를 항상 명시한다.
   - 유도 중 **처음 등장하는 수학적 도구/개념**(예: marginalization, chain rule, Taylor expansion, linearization 등)이 있으면, 그 개념을 곧바로 수식으로 넘어가지 않고 **개념 설명 → 수식** 순서로 별도 문단(인용구 `>` 등으로 구분)을 만들어 짚어준다.
   - 정의(definition)와 유도된 결과(derived result)를 구분해서 명시한다 (예: "이건 정리가 아니라 definition이다").

## 원문 참고 규칙 (기억에 의존 금지)

- 스터디 자료를 작성할 때는 **항상 `ref/`의 원본 PDF를 직접 열어 확인한 내용을 근거로 작성한다.**
  기억이나 일반 지식에 의존해서 쓰지 않는다. 수식, 알고리즘 의사코드, 변수 표기, 절 번호, 예제 수치는
  반드시 원문과 대조한다.
- 원문에서 인용/참고한 위치는 절 번호와 책 페이지로 명시한다 (예: "책 2.4.3절, p.31").
- **ref PDF 수록 범위**: `ref/Probabilistic Robotics _Sebastian Thrun et al..pdf`는 **총 668페이지로
  책 전체(1~17장 + Bibliography + Index)를 담고 있다.** `pdfinfo`로 확인한 값이다.
- **페이지 오프셋**: PDF 페이지 번호 = 책 페이지 번호 + 21. 문서 전 구간에서 성립한다.
  (검증: 책 p.39=PDF 60, p.85=106, p.117=138, p.149=170, p.487=508, p.569=590, p.647=668)
  주요 챕터 시작 위치: 4장 PDF 106 · 5장 138 · 6장 170 · 7장 212 · 8장 258 · 9장 302.
- **⚠️ 페이지 수를 추정하지 말 것**: 파일이 어디까지 있는지 확인할 때는 반드시
  `pdfinfo "<파일>" | grep Pages` 를 실행한다. 특정 페이지에 내용이 있다는 사실은 그 페이지가
  마지막이라는 근거가 되지 않는다. 세션 시작 시 표시되는 페이지 수도 그대로 믿지 말고 직접 확인한다.
  (2026-08-15에 이 확인을 건너뛰어 "PDF가 98페이지에서 끝난다"고 잘못 판단하고, 그 오류를 이 규칙
  파일과 메모리, 3장 노트에까지 기록한 사고가 있었다.)
- 원문이 실제로 없는 범위를 작성해야 할 경우:
  1. 먼저 사용자에게 해당 범위의 원문 확보를 요청한다.
  2. 원문 없이 진행해야 한다면, 그 사실을 노트 상단에 명시하고 원문 대조가 필요한 부분을 표시한다.

## 예제/실습 규칙

- 가능하면 책에 나온 예제(예: 2.4.2절 도어 상태 추정)를 우선 재사용한다.
- 계산은 중간 단계를 생략하지 않고 전부 보여준다.
- 마지막에 스스로 풀어볼 연습문제 1개 이상, 또는 검증용 짧은 Python 코드 스니펫을 포함한다.

## 포맷/파일 규칙

- 수식은 LaTeX 문법(`$...$`, `$$...$$`)으로 작성 (KaTeX/MathJax 렌더링 기준).
- 폴더 구조는 `0_Contents.md` 챕터 번호를 그대로 따른다 (`partX_.../0N_챕터명/0N_챕터명.md`).
- 책 원본 이미지가 필요하면 해당 챕터 폴더의 `images/`에서 참조한다.
- 인터랙티브 시각화(Canvas/p5.js, Plotly.js 등, `1_Tools.md` 참조)는 필요한 절 아래에 위젯 코드/설명으로 추가한다.
