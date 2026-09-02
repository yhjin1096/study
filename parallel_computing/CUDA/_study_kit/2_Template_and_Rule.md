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
