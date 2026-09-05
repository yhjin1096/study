# Programming Massively Parallel Processors (5th Edition) 스터디

## 스터디 개요

Wen-mei W. Hwu · David B. Kirk · Izzat El Hajj, *Programming Massively Parallel
Processors: A Hands-on Approach*, 5판 (Elsevier, 2027) 을 정독하며 노트를 만든다.

CUDA C++ 로 GPU 커널을 처음부터 작성하는 것에서 시작해, GPU 아키텍처가 성능을
결정하는 방식(coalescing · occupancy · control divergence · bank conflict)을 이해하고,
그 위에서 reduction · scan · merge · sort 같은 병렬 패턴을 직접 구현한 뒤,
sparse matrix · graph · CNN · LLM attention 같은 응용과 multi-GPU 까지 간다.
**전 범위(1~24장 + 부록 A~C, 231개 절)** 가 대상이다.

원본 PDF: `ref/Programming_Massively_Parallel_Processors.pdf` (673쪽 · 책 쪽번호 1~649)

## 문서 안내

| 문서 | 내용 | 언제 보는가 |
|---|---|---|
| [`0_Contents.md`](0_Contents.md) | 학습 범위 목차 (절 구성 + 쪽번호), 추천 학습 순서, 진행 상황 | **다음에 뭘 공부할지 정할 때.** 새 챕터 노트의 절 구성을 여기서 가져온다. 폴더/파일 번호도 여기 장 번호를 따름 |
| [`1_Tools.md`](1_Tools.md) | 도구 스택과 **빌드·추출·점검 명령어** | HTML을 만들거나 다시 빌드할 때, 그림을 추출할 때, 참조를 점검할 때 |
| [`2_Template_and_Rule.md`](2_Template_and_Rule.md) | **노트 작성 템플릿과 규칙** — 3단 구조, 언어 규칙, 생략 금지, 용어표 | **챕터 내용을 쓰기 직전에 반드시.** 모든 챕터 `.md`가 이 구조를 따른다 |
| [`3_Pitfalls.md`](3_Pitfalls.md) | **실전에서 겪은 함정** | 시작 전에 한 번, 그리고 뭔가 이상할 때마다 |

## 이 책에서 먼저 알아야 할 것 세 가지

초기 설정에서 실제로 문제를 일으켰던 것들이다. 자세한 근거는 `kit.conf` 주석과
`3_Pitfalls.md` A10~A12 에 있다.

1. **`page_offset` 이 하나가 아니다.** 장 사이 빈 쪽 4장이 PDF 에서 빠져 있어
   오프셋이 28 → 24 로 구간마다 줄어든다. **쪽 범위를 손으로 환산하지 마라.**
   `--book-pages` 옵션이나 `kit_config.book_to_pdf()` 를 쓴다.
2. **캡션 표기가 종류마다 다르다.** Figure 는 `FIGURE 6.6` (전부 대문자),
   Table 은 `Table 19.1` (혼합). 도구가 대소문자를 무시하고 잡은 뒤
   `Figure 6.6` / `Table 19.1` 로 정규화한다. **노트에는 정규화된 표기로 쓴다.**
3. **텍스트 레이어가 하이픈과 합자를 흘린다.** `Breadth-first` → `Breadthfirst`,
   `filter` → `fifilter`, `efficiency` → `e<0x1b>iciency`.
   **`pdftotext` 출력의 철자를 그대로 믿지 말고**, 애매하면 해당 영역을
   이미지로 렌더링해 눈으로 확인한다.

## 작업 흐름 (챕터 하나마다 반복)

**모든 명령은 스터디 루트(`CUDA/`)에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
#    책 123-155 쪽 = 6장. --book-pages 로 뽑은 PDF 쪽 범위를 그대로 쓴다
pdftotext -layout -f 151 -l 183 "ref/Programming_Massively_Parallel_Processors.pdf" /tmp/ch6.txt

# ② 그림·표 추출 — 책 쪽번호로 지정한다 (오프셋 환산은 도구가 한다)
python3 _study_kit/tools/extract_figures.py --chapter 6 --book-pages 123-155 --list
python3 _study_kit/tools/extract_figures.py --chapter 6 --book-pages 123-155 \
    --out part1_fundamentals/06_performance/images \
    --names _study_kit/tools/figure_names/ch6.txt

# ③ 노트 작성 — 2_Template_and_Rule.md 의 구조와 규칙을 따른다

# ④ 위젯 (필요하면) — _study_kit/tools/widgets/_GUIDE.md

# ⑤ 빌드
python3 _study_kit/tools/build_html.py part1_fundamentals/06_performance/06_performance.md

# ⑥ 검증 — 아래 네 가지는 실제로 오류가 나왔던 항목이다
python3 _study_kit/tools/check_refs.py 06   # 그림·표·쪽번호·절 참조
python3 _study_kit/tools/check_toc.py       # 목차 쪽번호가 원본과 맞는가
#   본문의 손계산을 코드로 재계산해 대조   ← 오류가 가장 많이 나오는 곳
#   위젯을 헤드리스 브라우저로 열어 확인   ← 조작까지 해 봐야 한다
```

**⑥을 건너뛰지 마라.** 자세한 명령은 `1_Tools.md`, 사례는 `3_Pitfalls.md`.

## 폴더 구조

```
CUDA/                              ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/Programming_Massively_Parallel_Processors.pdf
├── _study_kit/                    ← 킷 루트
│   ├── kit.conf                   이 스터디의 설정 (PDF·오프셋·레이아웃·사이드바)
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html
│       ├── extract_figures.py     PDF에서 Figure/Table 크롭 추출
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── check_toc.py           0_Contents.md 의 쪽번호를 원문과 대조
│       ├── kit_config.py          kit.conf 로더 (구간별 오프셋 환산 포함)
│       ├── figure_names/chN.txt   챕터별 그림 파일명 매핑 (추출 재현용, 부록은 chA/B/C)
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯
├── part1_fundamentals/
│   └── 06_performance/
│       ├── 06_performance.md     ← 원본. 이것만 손으로 고친다
│       ├── 06_performance.html   ← 생성물. 직접 편집하지 않는다
│       └── images/
└── part4_appendices/
    └── C_memories_address_spaces/   ← 부록은 장 번호 대신 글자를 쓴다
```

- 폴더 앞 번호는 `0_Contents.md`의 장 번호를 그대로 따른다
  (부록은 번호가 없으므로 `A_`·`B_`·`C_` 로 시작한다)
- 부 폴더 이름은 책의 Part 를 따른다 — `part4_appendices` 가 책의 **Part 4: Appendices** 다.
  `check_refs.py` 가 `part*/*/*.md` 를 훑으므로 이 접두사를 지켜야 검사에 걸린다
- **챕터당 파일 1개** — 절이 많아도 쪼개지 않고 헤더로 탐색한다 (흐름 파악에 유리)
- `images/`를 챕터 폴더 안에 두어 각 챕터가 self-contained하게 유지한다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **원문 대조 필수** — 기억이나 일반 지식으로 쓰지 않는다. 인용은 쪽번호를 남긴다
- **생략 금지** — 유도를 결과만 적지 않고 왜 그 식이 나오는지 매 단계 밝힌다
- **검증 가능한 예제** — 손계산은 코드로 재계산해 대조한다

이 네 가지가 전체를 관통하는 원칙이고, 나머지는 그것을 지키기 위한 도구다.
