# 스터디 자료 작성 템플릿 & 규칙

모든 챕터 노트(`partX_.../0N_.../0N_*.md`)는 아래 구조와 규칙을 따른다.

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

### 절마다 유연하게 적용한다

- 수식이 없는 절(개괄·요약·문헌)은 **1과 3만** 있어도 된다
- 알고리즘이 중심인 절은 2를 "### 2. 알고리즘"으로 바꿔도 된다
- **다만 내용이 있는 절에는 예외 없이 연습문제 1개 이상**을 둔다 (아래 예제/실습 규칙)

### 책의 절 순서를 바꿔도 된다 — 대신 밝힌다

이해 순서가 책 순서와 다르면 재배치한다. 단 **헤더에 책의 원래 절 번호와 쪽번호를 함께 적고**,
노트 상단에 재배치 사실을 명시한다.

> 예: 어떤 장에서 책은 "밀도 계산 → 표집" 순이었지만, 표집이 훨씬 직관적이라
> "유도 → 표집 → 밀도 계산" 순으로 배치하고 그 이유를 상단에 적었다.

---

## 언어 규칙

- **섹션 1 (개념적 이해)**: 한국어 설명 + 원본 영단어 병기. 예: "사전 확률(prior)", "가능도(likelihood)".
  한글 번역이 어색하거나 못 알아볼 수 있는 용어는 병기를 통해 원문을 같이 남긴다.
- **섹션 2, 3 (수식/유도, 예제/실습)**: 수학적·전문 용어는 한국어로 억지로 번역하지 않고 영어를
  그대로 사용한다. **문장 자체는 한국어로 서술하되 용어는 영어.**

### 용어표를 운영한다

**이 문서 아래쪽에 "절대 번역하지 않는 용어" 표를 만들고, 새 용어가 나올 때마다 갱신한다.**

| 쓸 것 | 쓰지 말 것 |
|---|---|
| (영어 용어) | (어색한 한국어 번역어) |

**판단 기준**: 한국어 교재에서 그 번역어가 **실제로 통용되는가?** 아니라면 영어를 쓴다.

- 통용되는 것의 예: 공분산, 조건부확률, 정규분포, 기댓값, 편미분, 정규화 상수
- 통용되지 않는 것의 예: (분야마다 다르다 — 처음 몇 챕터를 쓰며 직접 판단해 채운다)

**품사를 구분하라.** 명사는 영어로 쓰더라도 동사·형용사형은 한국어가 자연스러운 경우가 많다.
경계가 모호하면 표에 명시한다.

| 원문 | 노트에 쓸 것 | 쓰지 말 것 |
|---|---|---|
| 명사 `projection` | **projection** | 사영 |
| 동사 `project` | **투영하다** | 사영하다 |

> **판단에 멈칫했다면 그건 규칙이 모호하다는 증거다.** 본문을 고치기 전에 규칙에 경계를 명시하라.

### 챕터를 끝낼 때마다 훑는다

```bash
for t in <금지어1> <금지어2> <금지어3>; do
  echo "$t: $(grep -o "$t" part*/*/*.md | wc -l)건"
done
```

여러 세션에 걸쳐 쓰면 표기가 반드시 흔들린다. 이 검사로 한 번에 **31건**이 나온 적도 있다.

---

## 수식/유도 규칙 (생략 금지)

1. 해당 개념/알고리즘과 관련된 유도 전체를 번호를 매겨(`(1)`, `(2)`, ...)
   **설명 없이 먼저 통으로 보여준다.**
2. 그 다음, 번호별로 하나씩 짚어가며 설명한다. 이때:
   - 결과 수식만 제시하지 않고, **왜 그 수식이 나오는지**(정의 적용, 이전 단계 대입, 항등식 변형 등)를
     항상 명시한다.
   - 유도 중 **처음 등장하는 수학적 도구/개념**(예: marginalization, chain rule, Taylor expansion,
     회전행렬 등)이 있으면, 그 개념을 곧바로 수식으로 넘어가지 않고
     **개념 설명 → 수식** 순서로 별도 문단(인용구 `>` 등으로 구분)을 만들어 짚어준다.
   - 정의(definition)와 유도된 결과(derived result)를 구분해서 명시한다
     (예: "이건 정리가 아니라 definition이다").
3. 알고리즘 의사코드는 **원문 표의 이미지와 코드 블록을 함께** 싣고, 라인별로 무엇을 하는지 짚는다.

---

## 원문 참고 규칙 (기억에 의존 금지)

- 스터디 자료를 작성할 때는 **항상 `ref/`의 원본 PDF를 직접 열어 확인한 내용을 근거로 작성한다.**
  기억이나 일반 지식에 의존해서 쓰지 않는다. 수식, 알고리즘 의사코드, 변수 표기, 절 번호, 예제 수치는
  반드시 원문과 대조한다.
- 원문에서 인용/참고한 위치는 **절 번호와 책 쪽번호로 명시**한다 (예: "책 2.4.3절, p.31").
  `tools/check_refs.py`가 이 표기를 읽어 검사한다.

### 시작 전에 반드시 확인할 두 가지

```bash
pdfinfo "ref/책.pdf" | grep Pages                  # ① 총 쪽수
pdftotext -f 60 -l 60 "ref/책.pdf" - | head -3     # ② 페이지 오프셋
```

**둘 다 추측하지 마라.** 앞·중간·뒤 세 곳에서 오프셋을 검증하고 `kit.conf`에 적는다.
이유와 사고 사례는 [`3_Pitfalls.md`](3_Pitfalls.md) A1·A2.

### 원문이 없는 범위를 써야 할 경우

1. 먼저 사용자에게 해당 범위의 원문 확보를 요청한다.
2. 원문 없이 진행해야 한다면, 그 사실을 노트 상단에 명시하고 원문 대조가 필요한 부분을 표시한다.

---

## 예제/실습 규칙

- 가능하면 **책에 나온 예제를 우선 재사용**한다.
- 계산은 중간 단계를 생략하지 않고 전부 보여준다.
- **내용이 있는 절마다 연습문제 1개 이상**, 또는 검증용 짧은 코드 스니펫을 포함한다.

### 손계산은 반드시 코드로 검산한다

**예제를 쓴 뒤 같은 계산을 코드로 다시 해서 대조한다. 예외 없이.**

한 챕터의 예제에서 **7곳이 틀린 적이 있다.** `atan2` 값 하나가 어긋나면서 그 뒤 행렬 곱이
연쇄로 전부 잘못됐다. 손으로 쓴 중간값을 반올림해 다음 계산에 넣으면 오차가 누적된다.

```python
# 노트에 쓴 값과 나란히 출력해 눈으로 대조한다
print(f"  Sigma_bar = {Sigma_bar}   (노트: [[0.198, ...]])")
```

부수 효과 — 이 검산 코드가 그대로 노트의 "검증용 스니펫"이 된다.

---

## 포맷/파일 규칙

- 수식은 LaTeX 문법(`$...$`, `$$...$$`)으로 작성 (MathJax 렌더링 기준).
- 폴더 구조는 `0_Contents.md` 장 번호를 그대로 따른다 (`partX_.../0N_챕터명/0N_챕터명.md`).
- 책 원본 이미지는 해당 챕터 폴더의 `images/`에서 참조한다.
  파일명은 `fig<장>_<번호>_<설명>.png`, `table<장>_<번호>_<설명>.png` 형식으로 통일한다.
- 이미지 바로 아래에 **캡션을 한국어로 옮기고 쪽번호를 붙인다.**

  ```markdown
  ![Figure 6.3 range finder 센서 모델의 네 성분](images/fig6_3_four_components.png)

  *Figure 6.3 — Range finder 센서 모델의 성분들. (책 p.154)*
  ```

- 인터랙티브 시각화는 `tools/widgets/NAME.html`을 만들고 본문에 `<!--widget:NAME-->` 한 줄을 넣는다
  (작성법은 `tools/widgets/_GUIDE.md`).
- **`.md`가 원본, `.html`은 생성물이다.** 내용을 고칠 땐 항상 `.md`를 고치고 다시 빌드한다.

---

## 절대 번역하지 않는 용어

> 이 스터디(GPU·병렬 컴퓨팅)의 표다. 챕터를 쓰면서 마주치는 용어를 계속 추가한다.
> **판단 기준은 "한국어 교재에서 그 번역어가 실제로 통용되는가"** 이지, 번역이 가능한가가 아니다.
> 이 분야는 실무 문헌이 거의 영어라, 음차(스레드·코어·캐시)조차 원어를 쓰는 편이 검색과
> 원문 대조에 유리하다.

| 쓸 것 | 쓰지 말 것 |
|---|---|
| thread | 스레드, 쓰레드, 실행 흐름 |
| core | 코어 |
| kernel | 커널 |
| cache | 캐시 |
| latency | 지연시간, 레이턴시 |
| throughput | 처리량, 스루풋 |
| memory bandwidth | 메모리 대역폭 |
| synchronization / barrier | 동기화 / 장벽 |
| atomic operation | 원자적 연산 |
| sequential / parallel (수식어) | 순차적/병렬적 — **단, 명사구 "병렬 프로그래밍·병렬 실행"은 한국어가 통용되므로 허용** |
| speedup | 속도 향상, 가속비 |
| work efficiency | 작업 효율 |
| coalescing | 병합, 유착 |
| occupancy | 점유율 |
| control divergence | 제어 분기, 분기 발산 |
| tiling | 타일링 |
| privatization | 사유화 |
| scan / prefix sum | 스캔 / 접두사 합 |
| embarrassingly parallel | 창피할 정도로 병렬적인 |
| memory-bound / compute-bound | 메모리 바운드 / 연산 바운드 |
| host / device | 호스트 / 디바이스 |

**반면 아래는 한국어가 표준이므로 그대로 쓴다**: 병렬 프로그래밍, 병렬 실행, 명령어,
정밀도, 면적, 전력, 발열, 반도체, 클러스터(노드 집합), 자료구조, 지역성, 정규화.

**품사 구분** — 명사는 영어로 쓰되 동사·형용사형은 한국어가 자연스럽다.

| 원문 | 노트에 쓸 것 | 쓰지 말 것 |
|---|---|---|
| 명사 `parallelization` | **병렬화** (통용됨) | 패러렐라이제이션 |
| 동사 `parallelize` | **병렬화하다** | 패러렐라이즈하다 |
| 명사 `synchronization` | **synchronization** | 동기화 |
| 동사 `synchronize` | **동기화하다** | 싱크로나이즈하다 |

> `synchronization` 은 명사일 때 영어, 동사형일 때 한국어라는 뜻이다.
> 경계가 헷갈리면 여기 한 줄을 더 적어 규칙을 굳힌다.

### 1장에서 추가된 용어

1장은 개괄이라 새 용어가 대량으로 들어왔다. 위 표의 항목 대부분이 1장에서 처음 나온 것이고,
그중 1장에서만 쓰인 것은 아래와 같다.

| 쓸 것 | 쓰지 말 것 |
|---|---|
| multi-core / many-thread | 멀티코어 / 매니스레드 |
| latency-oriented / throughput-oriented design | 지연 지향 / 처리량 지향 설계 |
| installed base | 설치 기반, 보급률 |
| form factor | 폼팩터 |
| concurrency revolution | 동시성 혁명 |
| computational thinking | 계산적 사고 |
| domain decomposition | 영역 분할 |
| performance portability | 성능 이식성 |
| program counter / instruction pointer | 프로그램 카운터 / 명령 포인터 |
| digital twin | 디지털 트윈 |

**1장에서 추가로 한국어를 쓰는 것**: Amdahl's Law 는 고유명사라 영어 그대로 두되,
"Amdahl's Law 의 상한"처럼 뒤에 붙는 말은 한국어로 쓴다.
배수 표기의 경계 (1장을 쓰며 실제로 흔들려서 규칙으로 굳혔다):

| 무엇인가 | 표기 | 예 |
|---|---|---|
| **성능 비교** — A가 B의 몇 배 빠른가/많은가 | **`×`** | `20×` speedup, FP16 이 FP64 의 `58.2×`, CPU 대비 `10×` memory bandwidth |
| **자원량·배수 변화** — 무엇을 몇 배로 늘리는가 | **`배`** | 면적 2배, 전력 4배, 전류 2배, 연산 유닛 2배 |

`20x`·`20배`(성능 비교일 때)는 쓰지 않는다. 헷갈리면 **"두 대상을 비교하는가,
한 대상을 키우는가"** 를 묻는다. 검사는 `grep -E '[0-9](\.[0-9]+)?배'` 로 훑고
남은 것이 전부 자원·변화인지 눈으로 확인한다.


### 2장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| grid / block / thread block | 격자 / 블록 / 스레드 블록 |
| host / device | 호스트 / 디바이스, 주인 / 장치 |
| device global memory (global memory) | 디바이스 전역 메모리 |
| SPMD (Single-Program Multiple-Data) | 단일 프로그램 다중 데이터 |
| execution configuration parameter | 실행 구성 매개변수 |
| built-in variable | 내장 변수 |
| loop parallelism | 루프 병렬성 |
| data parallelism / task parallelism | 데이터 병렬성 / 작업 병렬성 |
| task decomposition | 작업 분해 |
| scalability | 확장성 |
| kernel / device function / host function | 커널 / 디바이스 함수 / 호스트 함수 |
| qualifier keyword | 한정자 키워드 |
| PTX / NVCC | (약어이므로 그대로) |
| ceiling division | 올림 나눗셈 |

**2장에서 추가로 한국어를 쓰는 것**: **포인터**·**역참조**는 한국어 C/C++ 교재에서
완전히 통용되므로 한국어를 쓴다 (`pointer`·`dereference` 로 쓰지 않는다).
`allocate`/`free` 도 **할당**/**해제**로 쓴다. `launch` 는 명사·동사 모두 **launch** 로 두되
("grid 를 launch 한다") 조사만 붙인다 — "발사·시작"은 뜻이 흐려진다.

**코드 식별자는 절대 번역하거나 띄어쓰지 않는다.** `blockIdx.x`, `threadIdx.x`, `blockDim.x`,
`cudaMalloc`, `cudaMemcpyHostToDevice`, `__global__` 은 백틱으로 감싸 원문 그대로 쓴다.


### 3장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| row-major / column-major | 행 우선 / 열 우선 |
| linearize / flatten | 선형화 / 평탄화 — **단, 동사·서술로 풀어 쓸 때는 한국어 허용** (아래 참조) |
| memory space | 메모리 공간 |
| inner product / dot product | 내적 — 단 수식 설명에서는 병기 가능 |
| tile / tiling | 타일 / 타일링 |
| patch | 패치 |
| radius (patch 의) | 반지름 — patch 문맥에서는 radius |
| stride | 보폭, 간격 |
| BLAS / Level-1·2·3 | (약어이므로 그대로) |

**3장에서 추가로 한국어를 쓰는 것**: **선형대수**, **행렬**, **벡터**, **분해**(LU 분해),
**전치**(transpose 의 명사형은 transpose 를 쓰되 "전치하다"는 한국어)는 한국어 수학 교재에서
표준이므로 한국어를 쓴다. `linearize`·`flatten` 도 **명사로는 영어**(`linearization`)보다
**"선형화"·"평탄화"가 통용**되므로 한국어를 쓰되, 처음 등장할 때 `선형화(linearize)` 로 병기한다.

**차원 순서는 반드시 명시한다.** 이 책은 `dim3(x, y, z)`(코드)와 `(z, y, x)`(그림·데이터)의
순서가 반대다. 노트에서 크기를 적을 때는 **"세로 n × 가로 m"** 처럼 축을 말로 붙여
어느 순서인지 읽는 사람이 헷갈리지 않게 한다.


### 4장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| SM (Streaming Multiprocessor) / streaming processor | 스트리밍 멀티프로세서 / CUDA 코어 |
| GPC (GPU Processing Cluster) | (약어 그대로) |
| warp / warp-level primitive | 워프 |
| processing block | 처리 블록 |
| SIMD / SIMT / SISD / MISD / MIMD | (약어 그대로) |
| control divergence / divergent warp | 제어 분기, 분기 발산 |
| barrier synchronization | 배리어 동기화 |
| transparent scalability | 투명한 확장성 |
| wave / tail effect | 웨이브 / 꼬리 효과 |
| occupancy | 점유율 |
| latency tolerance / latency hiding | 지연 감내 / 지연 은닉 |
| fine-grained multithreading | 세밀 멀티스레딩 |
| zero-overhead thread scheduling | 무오버헤드 스케줄링 |
| context switching | 문맥 전환 |
| intrinsic function (intrinsic) | 내장 함수 |
| register spilling | 레지스터 스필링 |
| performance cliff | 성능 절벽 |
| compute capability | 연산 능력 |
| thread block cluster / distributed shared memory | 스레드 블록 클러스터 / 분산 공유 메모리 |
| oversubscription | 초과 구독 |
| branch prediction | 분기 예측 |
| bandwidth | 대역폭 |

**4장에서 정한 경계 — `barrier synchronization` 과 "동기화"**

`barrier synchronization` 은 **고유한 기법 이름**이므로 영어로 쓴다.
반면 일반 명사·동사로서의 **"동기화"·"동기화하다"는 한국어**를 쓴다 — 한국어 CS 문헌에서
완전히 통용되고, "synchronization 제약"보다 "동기화 제약"이 훨씬 읽기 좋다.

| 쓸 것 | 예 |
|---|---|
| `barrier synchronization` | "block 전체 barrier synchronization" |
| 동기화 (일반 명사) | "block 간 동기화 제약", "동기화 함수" |
| 동기화하다 (동사) | "block 끼리 동기화하지 않는다" |

같은 원리로 `__syncthreads()`·`__syncwarp()` 같은 **코드 식별자는 백틱으로 원문 그대로** 쓴다.

**개수 비교도 `×` 다.** 1장에서 "성능 비교는 `×`, 자원·배수 변화는 `배`"로 정했는데,
**"A 가 B 의 몇 배 많은가"라는 개수 비교도 성능 비교 쪽**이다
(예: "thread 2048개는 streaming processor 128개의 `16×`"). "2배로 늘린다"처럼
한 대상을 키우는 것만 `배` 다.


### 5장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| compute-to-global-memory-access ratio | 연산 대 메모리 접근 비 |
| arithmetic intensity / computational intensity | 산술 강도 / 연산 강도 |
| roofline (model) | 지붕선 모델 |
| speed-of-light 분석 | 광속 분석 |
| shared memory / distributed shared memory | 공유 메모리 / 분산 공유 메모리 |
| constant memory / local memory | 상수 메모리 / 지역 메모리 |
| register file | 레지스터 파일 |
| scratchpad memory | 스크래치패드 메모리 |
| scope / lifetime | 유효 범위 / 수명 |
| tile / tiling / register tiling | 타일 / 타일링 |
| strip-mining | 스트립 마이닝 |
| locality | 지역성 |
| read-after-write / write-after-read | 쓰기 후 읽기 / 읽기 후 쓰기 |
| true dependence / false dependence | 참 의존 / 거짓 의존 |

**5장에서 정한 경계 — `bandwidth` · `cache` · `throughput` 은 영어**

`대역폭`·`캐시`·`처리량`도 한국어에서 통용되기는 한다. 그러나 이 책에서는 거의 언제나
**복합 기술용어의 일부**로 나타나고(`peak memory bandwidth`, `on-chip cache`,
`computational throughput`), 1~4장에서 이미 영어로 일관돼 있다. **그 관례를 따른다.**

| 쓸 것 | 쓰지 말 것 |
|---|---|
| bandwidth / memory bandwidth | 대역폭 / 메모리 대역폭 |
| cache (동사형은 "cache 된다") | 캐시 / 캐시된다 |
| throughput | 처리량 |

**단, 비유 속의 일상어는 한국어를 쓴다.** 5.3절의 "큰 벽을 작은 **타일**로 덮는다"는
물리적 타일을 가리키는 비유이므로 한국어가 맞다. 기술 개념으로서의 `tile`·`tiling` 과
구분되도록 문맥으로 드러낸다.

**이 스터디의 세 갈래를 정리하면**

| 갈래 | 예 | 근거 |
|---|---|---|
| **영어를 쓴다** | thread, block, warp, kernel, tile, occupancy, bandwidth, cache, throughput | 복합 기술용어의 일부로 쓰이고 한국어 번역이 흔들린다 |
| **한국어를 쓴다** | 포인터, 역참조, 동기화(일반), 선형대수, 행렬, 할당, 해제 | 한국어 교재에서 완전히 표준이다 |
| **고유 이름은 영어** | `barrier synchronization`, Amdahl's Law, `__syncthreads()` | 기법·정리·식별자의 이름 |


### 6장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| coalescing / coalesced / uncoalesced | 병합 / 유착 |
| corner turning | 코너 터닝 |
| DRAM burst / cache line (cache block) | 버스트 / 캐시 라인 |
| bank / channel / bank conflict | 뱅크 / 채널 / 뱅크 충돌 |
| interleaved data distribution | 인터리브 분배 |
| DDR (double data rate) / HBM | (약어 그대로) |
| sense amplifier / bit line | 감지 증폭기 / 비트 선 |
| vector load / vector store | 벡터 로드 / 벡터 저장 |
| padding | 패딩 |
| stride | 보폭, 간격 |
| thread coarsening / coarsening factor / coarsening loop | 스레드 조립화 |
| loop unrolling / unrolling factor | 루프 펼치기 |
| instruction scheduling | 명령 스케줄링 |
| double buffering | 이중 버퍼링 |
| privatization | 사유화 |
| bottleneck | 병목 (단, "병목" 은 일상어로 통용되므로 서술문에서는 허용) |
| packing | 패킹 |
| AoS / SoA (array of structures / structure of arrays) | (약어 그대로) |

**6장에서 추가로 한국어를 쓰는 것**: **정렬**(alignment), **혼잡**(congestion),
**직렬화**(serialize)는 한국어가 자연스럽다. `alignment` 는 처음 등장할 때
`정렬(alignment)` 로 병기한다.

**`배` / `×` 경계의 추가 사례.** 6장에는 셋이 다 나온다.
- `16 GB/s 채널이 0.76 GB/s` → 비교가 아니라 값이므로 그대로
- `이용률이 잠재적으로 두 배` · `shared memory 사용량이 2배` → **한 대상을 키우는 것 → `배`**
- `thread 2048개는 SP 128개의 16×` (4장) → **두 대상의 개수 비교 → `×`**


### 7장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| convolution | 합성곱, 컨볼루션 |
| convolution filter | 필터, 합성곱 커널 (**아래 이름 충돌 주의**) |
| filter radius / filter dimension | 필터 반지름 / 필터 차원 |
| halo cell / ghost cell | 헤일로 셀 / 고스트 셀 |
| input tile / output tile | 입력 타일 / 출력 타일 |
| constant memory / constant cache | 상수 메모리 / 상수 캐시 |
| arithmetic intensity | 산술 강도 |
| inner product | 내적 (수식 설명에서는 병기 가능) |
| edge clamp / circular (ghost 처리 방식) | (그대로) |

**7장에서 정한 경계 — `convolution kernel` 은 쓰지 않는다**

책이 명시적으로 경고하는 이름 충돌이다 (책 p.160). 가중치 배열을 흔히
**convolution kernel** 이라 부르는데 **CUDA 의 kernel 함수와 겹친다.**
책은 이를 피해 **`convolution filter`** 로만 부르고, 이 스터디도 그 규약을 따른다.

| 쓸 것 | 쓰지 말 것 |
|---|---|
| convolution filter, filter 배열 | convolution kernel |
| kernel (= CUDA `__global__` 함수) | (다른 뜻으로 쓰지 않는다) |

**첫 등장 병기는 그대로 허용한다.** `radius(반지름)` 처럼 영어 용어에 한국어 뜻을 괄호로
한 번 붙이는 것은 `2_Template_and_Rule.md` 의 섹션 1 규칙대로 계속 쓴다.
두 번째부터는 영어만 쓴다.

**`배` / `×` 경계 — "몇 배 차이"도 비교다.** "이상적 값과 25× 차이", "장난감 예의 4×"
처럼 **두 값을 견주는 것은 `×`** 다. "shared memory 사용량이 2배" 처럼
**한 대상을 키우는 것만 `배`** 다 (4·6장에서 정한 것과 같다).


### 8장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| stencil / stencil sweep | 스텐실 / 스텐실 스윕 |
| order (stencil 의) | 차수 — **단, "도함수의 차수"는 한국어** (아래 참조) |
| grid point | 격자점 (**격자 = grid 와 겹쳐 혼동된다**) |
| structured / unstructured grid | 정형 / 비정형 격자 |
| regular grid | 규칙 격자 |
| finite difference (method) | 유한차분(법) — **단, "finite difference 근사"처럼 수식어로는 영어** |
| finite-element / finite-volume method | 유한요소법 / 유한체적법 |
| boundary condition | 경계 조건 (**단, 일반 서술의 "경계"·"경계 cell" 은 한국어 허용**) |
| input tile / output tile / active part | 입력 타일 / 출력 타일 / 활성부 |
| register tiling | 레지스터 타일링 |
| coarsening factor | 조립화 인자 |
| plane (입력 tile 의 x-y 평면) | **평면은 한국어를 쓴다** — 수학 일반 명사다 |
| fidelity | **충실도(fidelity)** 로 첫 등장 병기 후 한국어 |

**8장에서 정한 경계 — `grid` 가 두 뜻으로 쓰인다**

이 장에서 `grid` 는 **CUDA 의 thread grid** 와 **수치해석의 계산 격자** 두 가지를 가리킨다.
책도 둘 다 `grid` 로 쓴다. 노트에서는 **둘 다 `grid` 로 두되, 수식어로 구별한다.**

| 쓸 것 | 뜻 |
|---|---|
| `grid` / `thread grid` (2장 문맥) | CUDA 의 block 집합 |
| `grid point` · "입력 grid" · "출력 grid" | 수치해석의 계산 격자 |

**"격자"라는 한국어는 쓰지 않는다** — 어느 쪽인지 더 흐려지기 때문이다.
`structured grid`·`regular grid` 같은 복합어도 영어로 둔다.

**8장에서 추가로 한국어를 쓰는 것**: **미분방정식**·**편미분방정식**·**도함수**·**이산화**·
**수치해석**·**근사**·**오차**·**정밀도**·**평면**·**정육면체**는 한국어 수학·수치해석 교재에서
표준이므로 한국어를 쓴다. `discretization` 은 처음 등장할 때 `이산 표현(discrete
representation)` 으로 병기한다.

**`sparse` 는 "성긴"으로 쓴다.** 이 장에서 `sparse` 는 자료구조 용어(sparse matrix)가 아니라
"stencil 패턴에 점이 듬성듬성하다"는 형용사다. 첫 등장에 `성긴(sparse)` 로 병기하고
그 뒤로는 한국어만 쓴다. **자료구조로서의 `sparse matrix` 는 영어로 둔다** (14장에서 다시 나온다).

**`배` / `×` 경계 — 8장에서 나온 사례.**
- "double 은 memory 를 **두 배**로 먹는다", "shared memory 소요가 **2배**" → **한 대상을 키움 → `배`**
- "(b)보다 **2.37×** 많다", "기본 kernel 의 0.41 보다 **2.4×** 낫다",
  "3D order 3 에서는 **18.5×** 차이" → **두 대상 비교 → `×`**


### 9장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| histogram | 히스토그램, 도수분포 |
| bin | 빈, 구간통 (**단, "값 구간"은 한국어 허용**) |
| atomic operation | 원자적 연산, 원자 연산 |
| `atomic_ref` / `fetch_add` / `thread_scope` | (코드 식별자 — 백틱으로 원문 그대로) |
| memory order / `memory_order_relaxed` | 메모리 순서 |
| race condition | 경쟁 상태, 경합 상태 |
| read-modify-write | 읽기-수정-쓰기 |
| owner-computes rule | 소유자 계산 규칙 |
| output interference | 출력 간섭 |
| privatization | 사유화, 개인화 |
| private copy / public copy | 개인 사본 / 공용 사본 — **단 "사본"은 한국어 허용** |
| contention | 경쟁 (**"경쟁"은 한국어가 자연스러워 허용**, 아래 참조) |
| contiguous / interleaved partitioning | 연속 분할 / 교차 분할 |
| feature (데이터의) | 특징 — **단, "feature extraction"은 통째로 영어** |
| last-level cache | 최종 단계 캐시 |
| lost update | 갱신 손실 |

**9장에서 정한 경계 — `contention` 은 "경쟁"으로 쓴다**

`bandwidth`·`cache`·`throughput` 은 영어로 두기로 했는데(5장) `contention` 은 왜 다른가.
이 낱말은 **복합 기술용어의 일부로 쓰이지 않고** 언제나 서술문 안에서
"경쟁이 심하다"·"경쟁을 줄인다"처럼 **평범한 동사·형용사와 함께** 나오기 때문이다.
"contention 이 심하다"보다 **"경쟁이 심하다"가 훨씬 읽힌다.**

| 쓸 것 | 예 |
|---|---|
| 경쟁 / 경쟁이 심하다 / 경쟁을 줄인다 | "가장 붐비는 bin 의 경쟁", "경쟁을 block 안으로 한정한다" |
| `output interference` | 이 장이 도입한 **고유한 개념 이름**이므로 영어 |
| `race condition` | 마찬가지로 고유한 개념 이름 |

같은 원리로 **`atomic operation` 은 영어**다 — 기법의 이름이고
`atomicAdd`·`cuda::atomic_ref` 같은 식별자와 직결된다.

**9장에서 추가로 한국어를 쓰는 것**: **사본**, **복제**, **병합**, **초기화**, **직렬화**,
**빈도**, **분포**, **편향**, **경계 검사**는 한국어가 표준이다.
`merge` 는 이 장에서 **병합**으로 쓰되, **13장의 패턴 이름 `merge` 는 영어**로 둔다
(같은 낱말이 일반 동작과 패턴 이름 두 뜻으로 쓰인다 — 8장의 `grid` 와 같은 구도다).

**`배` / `×` 경계 — 9장에서 나온 사례.**
- "bin 을 4개로 줄이면 같은 bin 을 노리는 thread 가 **64×** 로 늘어난다",
  "2.5 M 의 딱 **2×**", "**6×** 이득", "peak 대비 **12,800×** 낮다" → **두 설정·두 값의 비교 → `×`**
- "throughput 이 **4배**가 되는가" → **같은 양이 몇 곱절이 되는가 → `배`**


### 10장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| reduction / reduction tree | 축소 / 리덕션 / 감축 트리 |
| **work** / **span** | 작업량 / 스팬 · 폭 |
| work efficiency | 작업 효율 |
| identity value | 항등원 (**수학 문맥의 "항등원"은 허용**, 아래 참조) |
| binary operator | 이항 연산자 (**한국어 표준이므로 한국어**, 아래 참조) |
| owner-computes (rule) | 소유자 계산 규칙 |
| stride | 보폭, 간격 |
| memory access divergence | 메모리 접근 발산 |
| memory consistency model | 메모리 일관성 모델 |
| memory fence | 메모리 펜스, 메모리 장벽 |
| warp-level primitive | 워프 수준 프리미티브 |
| warp shuffle / `__shfl_down_sync` / `__syncwarp()` | (코드 식별자 — 백틱 그대로) |
| lane index / `laneIdx()` / `warpIdx()` | 레인 인덱스 |
| warp voting / warp match / warp reduce 함수 | 워프 투표 / 매치 함수 |
| segment (입력 구획) | **구획**으로 쓴다 (아래 참조) |
| Thrust / CUB | (라이브러리 이름 그대로) |

**10장에서 정한 경계 — 수학 용어는 한국어, 계산 모델 용어는 영어**

이 장은 **수학 쪽 용어**와 **병렬 계산 모델 쪽 용어**가 섞여 나온다. 갈라 둔다.

| 갈래 | 쓸 것 | 근거 |
|---|---|---|
| **수학** | 결합법칙 · 교환법칙 · 결합적 · 교환적 · 이항 연산자 · 항등원 · 기하급수 | 한국어 수학 교재에서 완전히 표준이다 |
| **계산 모델** | `work` · `span` · `work efficiency` | 한국어 번역이 흔들리고(작업량/일량, 스팬/폭/깊이) 11장에서 `work-efficient` 라는 복합어로 계속 쓰인다 |

`associative`·`commutative` 는 **수식·정의를 적을 때는 영어**로 병기하고
(`(a Θ b) Θ c = a Θ (b Θ c)  (associative — 결합법칙)`),
**서술문에서는 한국어**를 쓴다 ("덧셈은 결합적이다").
`identity value` 는 **첫 등장에 영어로 정의**한 뒤 그대로 영어를 쓴다 —
`0.0`·`-INFINITY` 같은 구체적 코드 값과 함께 나오는 일이 많아서다.

**`segment` 는 "구획"으로 쓴다.** 이 장에서 `segment` 는 **입력 배열을 block 에 나눠 주는
덩어리**를 가리키는 평범한 명사이고, `tile`(공간적 부분 배열)과 구별해야 한다.
코드 식별자 `segment` 는 물론 백틱으로 원문 그대로 쓴다.

**10장에서 추가로 한국어를 쓰는 것**: **부분합**, **누적**, **직렬화**, **반복**(iteration),
**단계**(step 을 풀어 쓸 때), **경계 검사**, **재현성**은 한국어가 표준이다.
단 **`step` 이 work/span 분석의 정의어로 쓰일 때는 영어**로 둔다
("span 은 step 수다"). 그림 라벨의 "Step 0" 도 영어 그대로 인용한다.

**`배` / `×` 경계 — 10장에서 나온 사례.**
- "coalesced 대비 **2×** 의 transaction", "효율 **2.25×** 개선", "요청 **3.9×** 감소",
  "**$2048\times$** 차이" → **두 대상·두 설정의 비교 → `×`**
- 10장 본문에는 `배` 를 쓸 자리가 없었다 — 이 장의 숫자는 전부 **비교**다.


### 11장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| scan / inclusive scan / exclusive scan | 스캔 / 포함 스캔 / 배타 스캔 |
| prefix sum | 접두사 합, 누적합 |
| Kogge-Stone / Brent-Kung | (고유명사 — 그대로) |
| adder (design) | 덧셈기 — **회로 문맥에서는 "덧셈기" 허용** (아래 참조) |
| work complexity / work efficiency / work-efficient | 작업 복잡도 / 작업 효율 |
| span | 스팬, 폭, 깊이 |
| scan-scan-add / reduce-scan-scan (분해) | (그대로) |
| double-buffering | 이중 버퍼링 |
| unidirectional synchronization | 단방향 동기화 — **한국어를 쓴다** (아래 참조) |
| single lookback / multiple lookback / decoupled lookback | 단일 되돌아보기 / 분리 되돌아보기 |
| memory order / acquire · release semantics | 메모리 순서 / 획득·해제 의미 |
| block counter / dynamic block index assignment | (풀어서 서술) |
| segment / subsegment | **구획 / 부분구획** (10장 규약 그대로) |
| warp shuffle up (`__shfl_up_sync`) | (코드 식별자 — 백틱 그대로) |
| lane index | 레인 인덱스 |
| register tile / `#pragma unroll` | (코드 식별자 — 백틱 그대로) |

**11장에서 정한 경계 — `unidirectional synchronization` 은 "단방향 동기화"**

4장에서 **`barrier synchronization` 은 고유한 기법 이름이라 영어**로 정했다.
그런데 `unidirectional synchronization` 은 다르다 —
**`barrier` 처럼 굳어진 이름이 아니라 "방향이 한쪽뿐인 동기화"라는 서술적 표현**이고,
이 책이 그 자리에서 정의해 쓰는 말이다.
**서술적 표현은 한국어가 읽힌다.**

| 쓸 것 | 근거 |
|---|---|
| `barrier synchronization` (영어) | 굳어진 기법 이름. `__syncthreads()` 와 직결 |
| **단방향 동기화** (한국어) | 서술적 표현. "동기화"는 4장에서 이미 한국어로 정했다 |
| `grid 전체 barrier` | 위 둘의 조합 — `barrier` 만 영어 |

**`acquire`·`release` 는 영어**로 둔다. `cuda::memory_order_acquire` 라는
**코드 식별자와 직결**되고, "획득 의미·해제 의미" 는 통용되지 않는다.
서술할 때는 **"acquire 의미"·"release-acquire 짝"** 처럼 영어 낱말에 조사를 붙인다.

**11장에서 추가로 한국어를 쓰는 것**: **절단점**, **부분합**, **점화식**, **덧셈기**,
**되돌아보기**(설명할 때), **국면**(phase), **배포**(distribute), **음영**(shade) 은 한국어다.
`phase` 는 **"국면"** 으로 쓴다 — reduction 국면 / reverse 국면.
(`stage` 는 **"단계"** 로 쓴다. 둘을 구분해 두면 11.4·11.9절의 3-stage 분해와
11.10절의 2-phase 알고리즘이 헷갈리지 않는다.)

**`stride` 는 계속 영어다** (3·6·10장). 11.7절의 bank conflict 논의에서
"보폭" 이라 쓰고 싶어지지만 규칙대로 `stride` 를 쓴다.

**`배` / `×` 경계 — 11장에서 나온 사례.**
- "순차의 **8~9×**", "**56.9×** 감소", "**$3.2\times$ 에서 $15.1\times$ 로**",
  "scan 은 그보다도 **13×** 낮다" → **두 값의 비교 → `×`**
- 11장 본문에도 `배` 를 쓸 자리가 없었다 — 10장과 마찬가지로 전부 **비교**다.


### 12장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| filter / stable filter / unstable filter | 필터 / 안정 필터 / 불안정 필터 |
| in-place / out-of-place | 제자리 / 제자리 아닌 — **단, 첫 등장에 `제자리(in place)` 병기는 허용** |
| key (filter 되는 목록의 항목) | 키 — **책이 명시적으로 정한 이름이다** (책 p.290) |
| warp voting (함수) | 워프 투표 |
| `__activemask()` / `__ffs()` / `__popc()` / `__all_sync()` / `__any_sync()` / `__ballot_sync()` | (코드 식별자 — 백틱 그대로) |
| active mask / active thread | 활성 마스크 — **단, 형용사 "활성"은 한국어 허용** (아래 참조) |
| leader thread | 대표 thread, 리더 스레드 |
| coalesced atomic operation | 병합 atomic, 합쳐진 원자 연산 |
| cooperative groups / coalesced group | 협력 그룹 / 병합 그룹 |
| `thread_rank()` / `coalesced_threads()` | (코드 식별자 — 백틱 그대로) |
| binary prefix sum | 이진 접두사 합 |
| `thread_scope_block` / `thread_scope_device` | (코드 식별자 — 백틱 그대로) |
| garbage collection / heap | 쓰레기 수집 / 힙 |
| selectivity → **선택률** | (아래 참조 — 이 노트가 만든 말이다) |

**12장에서 정한 경계 — `active` 는 명사면 영어, 형용사면 한국어**

`active mask`·`active thread` 는 **`__activemask()` 라는 식별자와 직결된 복합어**이므로 영어로 둔다.
그러나 서술문의 **"활성 lane", "활성이다", "비활성 thread"** 는 한국어를 쓴다 —
4장에서 `barrier synchronization`(영어)과 "동기화"(한국어)를 갈랐던 것과 같은 구도다.

| 쓸 것 | 예 |
|---|---|
| `active mask` (영어) | "`__activemask()` 가 돌려주는 active mask" |
| 활성 / 비활성 (한국어) | "활성 lane 이 여덟 개", "비활성 thread 는 기다린다" |

**`selectivity` 는 "선택률"로 쓰되, 책에 없는 말임을 밝힌다.**
`cond()` 를 통과하는 key 의 비율을 가리키는데 **책에는 이름이 없다.**
12장의 성능이 거의 전부 이 값의 함수라 이름이 필요해 붙였고,
**노트 본문에서 "이 노트의 표기다 — 책에는 없다"고 명시**했다.
원문에 없는 용어를 도입할 때는 이렇게 출처를 밝힌다.

**12장에서 추가로 한국어를 쓰는 것**: **압축**(compaction — 첫 등장에 `압축(compaction)` 병기),
**중복 제거**, **전치**, **덮어쓰기**, **비트 연산**, **교집합**, **닫힌 식**, **추이적**은
한국어가 표준이다. `broadcast` 는 **"broadcast 한다"** 로 영어에 조사를 붙인다
(2장의 `launch` 와 같은 처리).

**`배` / `×` 경계 — 12장에서 나온 사례.**
- "atomic 이 **16×** 감소", "**$128\times$**", "왕복이 **$4\times$** 이상 줄어든다",
  "효율 **$1.41\times$** 개선", "atomic 을 **$32s\times$** 줄인다",
  "**$50{,}000\times$** 가까이 느리다", "latency 가 **$100\times$** 짧다"
  → **두 구현·두 값의 비교 → `×`**
- "메모리를 **두 배** 쓴다", "block 이 **$C$ 배**의 key 를 맡는다",
  "출력 덩어리가 **$C$ 배** 길어진다" → **한 대상을 키우는 것 → `배`**
- **12장은 `배` 와 `×` 가 한 장에 모두 나온 드문 경우다.** 판별은 늘 같다 —
  **"두 대상을 견주는가(`×`), 한 대상을 키우는가(`배`)"**.
  "$n$ 배 줄인다/개선한다"는 **줄어든 뒤와 전을 견주는 것**이므로 `×` 다.


### 13장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| merge / ordered merge | 병합 — **아래 경계 참조** |
| merge sort | 병합 정렬 |
| **rank / co-rank** | 순위 / 공동 순위 |
| stability / stable / unstable | 안정성 / 안정 정렬 (**아래 참조**) |
| binary search | 이진 탐색 (**아래 참조**) |
| circular buffer | 원형 버퍼 |
| prefix subarray / subarray | 접두 부분배열 — **단, "부분배열"은 한국어 허용** |
| marker variable | 표식 변수 |
| divide-and-conquer | 분할 정복 (**첫 등장 병기는 허용**) |
| map-reduce / Hadoop | (고유명사 그대로) |
| virtual index (Figure 13.20 주석) | 가상 인덱스 |
| `co_rank_circular` / `merge_sequential_circular` / `A_S_start` / `tile_size` | (코드 식별자 — 백틱 그대로) |

**13장에서 정한 경계 — `merge` 는 패턴 이름일 때만 영어**

9장에서 이미 예고해 둔 갈림이다 (`merge` 는 9장에서 **병합**, 13장의 패턴 이름은 영어).
그 규약을 그대로 지킨다.

| 쓸 것 | 언제 |
|---|---|
| `merge` (영어) | **패턴·연산·함수의 이름** — "merge 연산", "`merge_sequential`", "merge sort" |
| 병합 (한국어) | **일반 동작** — 9장의 "private 사본을 public 과 병합한다" |

**`stability` 는 영어다.** "안정 정렬"이 한국어 알고리즘 교재에서 통용되기는 하지만,
12장에서 **`stable filter`/`unstable filter` 를 영어로 정했고** 13·14장이 같은 개념을
이어받는다. **한 개념을 장마다 다른 언어로 쓰지 않는다**는 것이 더 중요하다.
`stable`·`unstable`·`stability` 모두 영어로 쓰고, 서술은 "stable 하다"로 조사만 붙인다.

**`binary search` 도 영어다.** "이진 탐색"이 통용되지만 이 장에서는
`co_rank` 함수의 구현 방식을 가리키는 **고정된 이름**으로 반복해서 나오고,
`higher radix search` 같은 변형과 나란히 쓰인다. **탐색**이라는 낱말 자체는 한국어를 쓴다
("탐색 범위", "탐색이 끝난다").

**13장에서 추가로 한국어를 쓰는 것**: **불변식**(invariant — 첫 등장에 `불변식(invariant)` 병기),
**되감기**(wrap around), **분할상환**(amortize), **덮어쓰기**, **부분배열**, **경계**,
**올림 나눗셈**은 한국어가 표준이다.

**`배` / `×` 경계 — 13장에서 나온 사례.**
- "탐색이 merge 보다 **$40\times$** 비싸다", "merge 의 **$5\times$**",
  "**$1024\times$** 감소", "latency 가 **$100\times$** 짧다" → **두 값의 비교 → `×`**
- "적재량 **2배**", "thread 수가 **2배**", "전자를 **2배**로 늘리는 대신" →
  **한 대상을 키우는 것 → `배`**
- **주의**: `두 배열`·`배정`·`배포` 가 grep 에 걸린다. 기계 점검 뒤 눈으로 걸러야 한다.


### 14장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| sorting / sort | 정렬 — **아래 경계 참조** |
| odd-even (transposition) sort / bubble sort | 홀짝 정렬 / 거품 정렬 |
| merge sort / radix sort / sample sort / bitonic sort | 병합 정렬 / 기수 정렬 / 표본 정렬 |
| sorting network | 정렬망 / 정렬 네트워크 |
| bucket | 버킷 (**단, "bucket 에 담는다"처럼 조사만 붙인다**) |
| radix | 기수 |
| digit (radix 의 자리) | **자리**는 한국어 허용 — "최하위 자리" |
| comparison-based / non-comparison-based | 비교 기반 / 비교 비기반 |
| stable partition | 안정 분할 |
| LSD / MSD (least/most-significant digit) | (약어 그대로) |
| idempotence | **멱등성** — 한국어가 표준 (아래 참조) |
| benign race | 양성 race |
| permutation | **순열** — 한국어가 표준 |
| Thrust / CUB / OneSweep / Hadoop | (고유명사 그대로) |

**14장에서 정한 경계 — `sort` 는 알고리즘 이름일 때 영어, 일반 동작은 한국어**

13장의 `merge` 규약과 같은 구도다.

| 쓸 것 | 언제 |
|---|---|
| `radix sort`·`merge sort`·`odd-even sort` (영어) | **알고리즘의 이름** |
| 정렬 / 정렬한다 / 지역 정렬 (한국어) | **일반 동작** — "구획을 정렬한다", "block 안에서 지역 정렬" |
| `sorting network` (영어) | 알고리즘 **범주**의 고유 이름 |

**`stability` 는 12·13장에서 정한 대로 계속 영어**다. 14장에서 "안정 정렬"이라는
한국어가 특히 통용되지만, **한 개념을 장마다 다른 언어로 쓰지 않는다**는 원칙을 지킨다.

**`멱등성`·`순열`·`정보이론적 하한` 은 한국어를 쓴다** — 수학·CS 교재에서 완전히 표준이다.
`idempotence` 는 첫 등장에 `멱등성(idempotence)` 으로 병기한다.

**표기 충돌 주의 — 책이 $N$ 을 두 뜻으로 쓴다.**
14.7절에서 책은 **key 의 비트 수**를 $N$ 이라 쓰는데, 같은 장의 다른 곳에서 $N$ 은
**입력 원소 수**다. 노트에서는 **비트 수를 $b$, radix 비트 수를 $r$, 원소 수를 $N$** 으로
갈라 쓰고 그 사실을 본문에 명시했다.
**원문이 기호를 겹쳐 쓰면 노트에서 갈라 쓰고 반드시 밝힌다.**

**`배` / `×` 경계 — 14장에서 나온 사례.**
- "$10^5\times$ 더 많은 일", "$4\times$ 감소", "$4\times$ 증가" → **두 값의 비교 → `×`**
- "구획 크기를 **두 배**씩 키우며" → **한 대상을 키우는 것 → `배`**


### 15장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| GEMM (General Matrix Multiply) | (약어 그대로) |
| leading dimension (`lda`·`ldb`·`ldc`) | 선행 차원 |
| block-level / warp-level / thread-level tile | 블록 수준 타일 |
| strip (register tile 의) | 스트립 — **"strip 쌍", "입력 strip" 으로 영어에 조사** |
| software pipelining / warp specialization | 소프트웨어 파이프라이닝 / 워프 특화 |
| double buffering | 이중 버퍼링 (6장 규약 그대로) |
| tensor core / tensor memory (TMEM) | 텐서 코어 |
| WMMA / WGMMA / LDGSTS / TMA | (약어 그대로) |
| cuBLAS / cuDNN / CUTLASS / cuTile | (고유명사 그대로) |
| prologue / steady state / epilogue | 도입부 / 정상 구간 / 마무리 |
| `float4` / `__forceinline__` / `#pragma unroll` | (코드 식별자 — 백틱 그대로) |

**15장에서 다시 확인한 것 — `arithmetic intensity` 는 영어다**

5·7·8장이 모두 `arithmetic intensity` 로 써 왔다 (5장 규칙표의 "쓰지 말 것"에
**산술 강도**가 명시돼 있다). 15장 초고에서 **29곳을 "산술 강도"로 쓴 것을 전량 되돌렸다.**

> **교훈**: 장이 바뀌면 앞 장의 표기를 잊는다.
> 새 장을 끝낼 때 **그 장의 핵심 용어가 앞 장에서 어떻게 쓰였는지 grep 으로 대조**하라.
> ```bash
> for f in part*/*/*.md; do printf "%-28s %s\n" "$(basename $f)" \
>   "$(grep -o 'arithmetic intensity' $f | wc -l)"; done
> ```

**15장에서 추가로 한국어를 쓰는 것**: **외적**(outer product), **내적**, **정렬**(alignment),
**임계값**(roofline 의 ridge point), **선형 결합**, **순열**, **사분면**(quadrant),
**정보이론적 하한**은 한국어 수학 교재에서 표준이다.
`swizzle` 은 **XOR swizzle** 로 영어를 쓴다 (고유한 기법 이름).

**`배` / `×` 경계 — 15장에서 나온 사례.**
- "연산이 **$34\times$** 오래 걸린다", "**$8\times$** 감소", "정사각이 **25%** 낫다" →
  **두 값의 비교 → `×`** 또는 백분율
- "shared memory **두 배**", "반복 **두 배**", "loop 를 **2배** unroll" →
  **한 대상을 키우는 것 → `배`**


---

## Part 3 (16장~) 의 용어

### 16장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| dynamic programming | 동적 계획법 |
| **wavefront** | 파면 / 물결 |
| memoization / tabulation | 메모이제이션 / 표작성 |
| top-down / bottom-up | 하향식 / 상향식 |
| optimal substructure / overlapping sub-problems | 최적 부분구조 / 겹치는 부분문제 |
| Floyd-Warshall / Smith-Waterman / Needleman-Wunsch | (고유명사 그대로) |
| **anti-diagonal** | 반대각선 / 역대각선 |
| **hypertile** / hyperplane partitioning | 하이퍼타일 / 초평면 분할 |
| **shear transformation** / shear factor | 전단 변환 |
| affine transformation | 아핀 변환 (**첫 등장 병기 허용**) |
| scoring matrix / homology score | 점수 행렬 / 상동성 점수 |
| genome / sequence alignment / read / base pair (bp) | 게놈 / 서열 정렬 / 리드 / 염기쌍 (**아래 참조**) |
| traceback | 역추적 (**첫 등장 병기 허용**) |
| persistent thread block | 상주 블록 |
| cooperative groups / `grid.sync()` | 협력 그룹 |
| DPX / `__vimax3_s32_relu()` | (약어·식별자 그대로) |
| time skewing / temporal blocking | 시간 기울이기 |

**16장에서 정한 경계 — 생물학 용어는 한국어를 쓴다**

`genome`·`sequence alignment`·`base pair` 는 **생물학·생명정보학 한국어 문헌에서
게놈·서열 정렬·염기쌍이 완전히 표준**이다. 이 스터디의 판단 기준("한국어 교재에서
그 번역어가 실제로 통용되는가")을 그대로 적용하면 **한국어**다.

| 쓸 것 | 예 |
|---|---|
| **염기쌍**, **게놈**, **서열**, **정렬**(생물학 문맥) | "인간 게놈은 32억 염기쌍" |
| `read`, `sequencing` | **영어** — "short read", "sequencing 기계" (음차가 흔들린다) |
| `Smith-Waterman`, `homology score` | **영어** — 알고리즘·지표의 고유 이름 |

**`정점`·`간선` 은 한국어를 쓴다** (graph 의 vertex·edge). 한국어 알고리즘 교재의 표준이고
**18장에서도 계속 쓴다**. 다만 `graph` 자체는 영어다 (8장에서 `grid` 를 영어로 둔 것과 같은
이유 — "그래프"는 차트와 헷갈린다).

**`대각선`·`평면`·`사분면` 은 한국어**다 (기하 일반명사, 8·15장 규약 그대로).
그러나 **`anti-diagonal` 은 영어** — 이 장이 정의해 반복해서 쓰는 **고유한 개념 이름**이고,
"반대각선"이 통용되지 않는다.

**16장에서 추가로 한국어를 쓰는 것**: **점화식**(11장 규약), **재귀**, **부분문제**,
**최단 경로**, **경계 조건**, **기울임**, **불완전 tile**, **삽입**·**삭제**(insertion·deletion 을
생물학 문맥에서 풀어 쓸 때)는 한국어가 표준이다.

**`배` / `×` 경계 — 16장에서 나온 사례.**
- "**$32\times$** 감소", "**$2\times$** 효율적", "**$1.5\times$** 로 는다",
  "사각 tile 의 **$2\times$** 개수" → **두 값의 비교 → `×`**
- 16장 본문에는 순수한 `배` 를 쓸 자리가 없었다 — 전부 **비교**다.
  ("두 배 효율적"처럼 한국어로 읽고 싶어지는 자리가 많으니 특히 주의한다.)


### 17장에서 추가된 용어

| 쓸 것 | 쓰지 말 것 |
|---|---|
| sparse matrix / dense | 희소 행렬 / 밀집 행렬 (**단, "dense vector"의 서술은 아래 참조**) |
| **SpMV** / SpMSpV / GEMM | (약어 그대로) |
| **COO / CSR / ELL / JDS / CSC** | 좌표 형식 / 압축 행 저장 … (**전부 약어 그대로**) |
| non-zero | 비영 원소 — **"non-zero" 로 쓰고 조사만 붙인다** |
| compaction / regularization | 압축 / 규칙화 (**첫 등장 병기 허용**, 아래 참조) |
| padding | 패딩 (6장 규약 그대로) |
| hybrid (method) | 혼합 방식 |
| `rowPtrs` · `colIdx` · `iterPtr` · `nnzPerRow` | (코드 식별자 — 백틱 그대로) |
| Conjugate Gradient / fill-in | 켤레기울기법 / 채움 |
| cuSPARSE / ELLPACK | (고유명사 그대로) |
| positive-definite | 양의 정부호 (**첫 등장 병기 허용**) |

**17장에서 정한 경계 — `compaction`·`regularization` 은 한국어로 쓴다**

이 장이 **두 낱말을 대비시켜 반복**해서 쓰는데
("압축과 규칙화 사이의 균형"), **한국어 쪽이 훨씬 읽힌다.**
첫 등장에 `압축(compaction)`·`규칙화(regularization)` 로 병기하고 그 뒤로는 한국어.
9장에서 `contention` 을 "경쟁"으로 정한 것과 같은 판단이다 —
**복합 기술용어의 일부가 아니라 서술문 안에서 평범하게 쓰이는 낱말**이다.

**`sparse matrix` 는 영어, 형용사 `sparse`·`dense` 도 영어**다.
"희소 행렬"이 한국어 수치해석 교재에서 통용되기는 하지만,
**8장에서 `sparse` 를 "성긴"으로 쓰기로 한 것은 stencil 문맥의 형용사**였고
(8장 규칙표: "자료구조로서의 sparse matrix 는 영어로 둔다 — 14장에서 다시 나온다"),
그 예고대로 여기서는 영어다. `dense vector`·`dense matrix` 도 짝을 맞춰 영어.

**17장에서 추가로 한국어를 쓰는 것**: **행**·**열**·**전치**·**정렬**·**분할**·
**연립일차방정식**·**계수**·**역행렬**·**수치 안정성**·**반복법**·**분할상환**은
한국어 수학·CS 교재에서 표준이다.
`matrix-vector 곱셈` 처럼 **영어 명사 + 한국어 서술**의 조합을 쓴다 (15장 GEMM 규약과 동일).

**`배` / `×` 경계 — 17장에서 나온 사례.**
- "CSR 의 **$20\times$**", "한 행 때문에 전체가 **$20\times$**", "**$10\times$** 절약",
  "**$200\times$** 차이" → **두 값의 비교 → `×`**
- 17장 본문에도 순수한 `배` 는 없었다. **`두 배열`·`배정`이 grep 에 걸리니 눈으로 거른다.**
