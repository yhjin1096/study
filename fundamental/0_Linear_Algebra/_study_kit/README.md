# Notes on Linear Algebra 스터디

## 스터디 개요

Gyubeom Edward Im의 강의 노트 *Notes on Linear Algebra*(51쪽)를 **내용 수정 없이 그대로** HTML로
옮기고, 이해를 돕는 **인터랙티브 위젯 14개**를 절 사이에 끼워 넣은 자료다.
선형시스템 → 최소제곱 → 고유값분해 → SVD → 다변수 미분 → 행렬 대수 → 행렬 분해·유사역행렬까지,
원문 9개 장 129개 절 전체를 다룬다.

원본 PDF: `ref/Notes on Linear Algebra.pdf`
결과물: `notes/notes_on_linear_algebra.html` (단일 파일 3.6MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/build_html.py notes/notes_on_linear_algebra.md
python3 _study_kit/tools/check_refs.py
```

### 이 스터디에서 원래 킷과 달라진 점

- **파란 강조가 113곳으로 매우 많다.** Lie Theory 스터디에서 만든 `==강조==` →
  `<span class="hl">` 장치가 여기서 제값을 한다. 색이 **수식 안이 아니라 산문**에 쓰였고,
  MathJax SVG 글리프가 `currentColor`를 상속하므로 강조 구간 안의 인라인 수식도 함께 물든다
  (`3_Pitfalls.md` B6). 확인해 둔 사실 — 이 문서의 **display 수식 줄에 붙은 색 span은 0곳**이고
  색이 붙은 수학은 전부 인라인이었다. 그래서 `\color` 는 한 번도 필요하지 않았다.
- **빌더 정규식을 한 번 고쳤다.** 원문에 `트레이스 = 랭크` 처럼 **강조 구간 안에 `=` 가 들어가는**
  곳이 있어 `==([^=\n]+)==` 가 매칭에 실패했다. `==((?:[^=\n]|=(?!=))+)==` 로 바꿔
  단일 `=` 는 허용하고 `==` 만 경계로 본다. Lie Theory 킷에도 같이 반영했다.
- **그림 추출은 bbox 방식** — 캡션이 하나도 없다(`Figure`/`Table` 전문 0회).
  이미지 객체 19개와 그림 19개가 1:1이라 `tools/extract_images_bbox.py` 가 깨끗하게 떨어진다
  (`3_Pitfalls.md` A10).
- **위젯 헬퍼가 `window.LA`다** — 앞 스터디의 `QK`(쿼터니언)·`LG`(Lie group)와 달리
  **수치 선형대수 라이브러리**를 새로 썼다. RREF/rank/nullspace, LU·PLU·LDU, Cholesky·LDLT,
  QR(수정 그람-슈미트), 대칭 고유분해(자코비 회전), SVD, Moore–Penrose 유사역행렬,
  low-rank 근사, leading principal minors, 그리고 2D 플롯·3D 정사영 씬이 들어 있다.
  위젯마다 같은 블록으로 들어가되 `if (!window.LA)` 로 한 번만 정의된다.

### 헬퍼를 믿기 전에 검산한 것

`LA` 는 위젯 14개가 전부 의존하므로 먼저 헤드리스 브라우저에서 항등식으로 검산했다.

| 검산 | 결과 |
|---|---|
| `A·A⁻¹ = I` | 5.6e-17 |
| rank / nullspace — `‖A·n‖`, rank–nullity | 1.0e-16 · OK |
| `PA = LU`, `PA = LDU` | 0.0 · 0.0 |
| `A = LLᵀ` (Cholesky), `A = LDLᵀ` | 0.0 · 0.0 (비PD 입력에는 `null` 반환) |
| `A = QR`, `QᵀQ = I` | 2.2e-16 · 5.4e-16 |
| `S = VDVᵀ` (자코비), 고유값 내림차순 | 2.8e-13 · OK |
| `A = UΣVᵀ` — 3×4 / 3×2(rank1) / 4×3 / 대칭, `UᵀU = VᵀV = I` | ≤ 3.1e-15 |
| **Penrose 4조건 (201)~(204)** — full/rank-deficient/tall/wide 네 경우 | ≤ 3.6e-15 |
| 식 (193)·(199) 닫힌 형태와 `pinv` 일치 | 2.5e-16 · 3.1e-16 |
| Eckart–Young `‖A−Aₖ‖_F = √(Σσᵢ²)` | 0.0 |

이 검산 표가 있기 때문에 위젯 readout에 찍히는 `1e-16` 들을 **결과의 정확성 근거**로 쓸 수 있다.

## 작업 흐름

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <시작> -l <끝> "ref/Notes on Linear Algebra.pdf" /tmp/ch.txt

# ② 파란 강조 위치를 쪽 단위로 뽑아 놓고 시작한다 (114구간을 눈으로 찾으면 반드시 샌다)
#    색 있는 span 을 연속 구간으로 묶어 출력하는 스크립트를 쓰면 전사 중 대조할 수 있다

# ③ 그림 추출 (캡션이 없는 문서라 bbox 방식)
python3 _study_kit/tools/extract_images_bbox.py --list
python3 _study_kit/tools/extract_images_bbox.py --out notes/images

# ④ 노트 작성 — notes/notes_on_linear_algebra.md. 원문의 파란 강조는 ==이렇게== 감싼다

# ⑤ 위젯 — _study_kit/tools/widgets/*.html (14개). //%LA% 자리에 헬퍼를 넣어 조립한다

# ⑥ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_linear_algebra.md

# ⑦ 검증
python3 _study_kit/tools/check_refs.py       # 절·쪽번호 참조
#   수식 번호 (1)~(235) 가 빠짐없이·중복 없이·순서대로 있는지 스크립트로 대조
#   절 제목 129개를 PDF 본문/목차에서 문자열로 다시 찾아 확인
#   ==강조== 개수와 PDF 의 색 구간 개수를 대조   ← 두 개가 안 맞으면 빠뜨린 것이다
#   <mjx-container 개수로 수식이 실제로 렌더링됐는지 확인   ← 3_Pitfalls B6
#   위젯 14개를 헤드리스로 열어 버튼·슬라이더까지 조작해 본다
```

### 이번 빌드의 검증 결과

| 항목 | 결과 |
|---|---|
| 수식 번호 | (1)~(235) — 누락 0, 중복 0, 순서 일치 |
| 절 제목 | 129개 전부 PDF 본문/목차에서 확인 (오타 고친 2개 제외) |
| 그림 | 19개 전부 인라인 |
| 렌더링된 수식 | `<mjx-container` **1,096개**, 그중 display 242개 (`$$` 237 + 환경을 품은 인라인 5) |
| 색 강조 | `.hl` **113곳** — PDF 의 색 구간 수와 일치 |
| 위젯 | 14개 · 버튼 전부 클릭 + 슬라이더 min/중간/max 스윕 후 `ERRS=0 BLANK=0 NaN=0` |
| `check_refs.py` | 문제 0건 |

## 폴더 구조

```
0_Linear_Algebra/                  ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/Notes on Linear Algebra.pdf
├── _study_kit/                    ← 킷 루트
│   ├── kit.conf                   오프셋 0 · A4 · 캡션 없음 · clip_x 66-530
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html (==강조==, [!TIP] 지원)
│       ├── extract_images_bbox.py bbox 기반 추출 ★ 이 문서에서 쓰는 쪽
│       ├── extract_figures.py     캡션 기반 (이 문서엔 캡션이 없어 쓰지 않는다)
│       ├── figure_names/linear_algebra.txt  파일명 → 무엇을 그린 그림인가
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯 14개
└── notes/
    ├── notes_on_linear_algebra.md    ← 원본. 이것만 손으로 고친다
    ├── notes_on_linear_algebra.html  ← 생성물(3.6MB). 직접 편집하지 않는다
    └── images/fig01…fig19_p<쪽>_<설명>.png   ← PDF에서 뽑은 그림 19개
```

- 원문에 그림 번호가 없으므로 파일명의 `figNN`은 **등장 순서**로 이 스터디가 붙인 번호다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **원문 재현이 최우선** — 문장·절 구성·수식 번호를 바꾸지 않는다. 고친 것은
  노트 맨 아래 "옮기며 바로잡은 것"에 전부 적는다
- **위젯은 본문 밖** — "원문에 없는 추가 요소"라고 표시된 회색 박스 안에만 둔다
- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **검증 가능한 위젯** — readout에 공식값과 수치계산값을 나란히 찍어 스스로 검산이 되게 한다
  (예: 실험 4는 식 (51) `Aᵀ(b−Ax̂) = 0` 을 열마다 막대로 찍고, 실험 13은 Penrose 4조건을
  전부 계산하며, 실험 14는 RLS 와 배치 해의 차이가 왜 `1e-8` 인지 조건수로 설명한다)
