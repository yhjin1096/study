# SLAM Handbook 스터디

**From Localization and Mapping to Spatial Intelligence**
Carlone · Kim · Barfoot · Cremers · Dellaert 편 · 저자 70명 · Cambridge University Press

## 스터디 개요

SLAM 을 **처음 보는 상태에서 시작해** 책 전체(18장 + Prelude 3 + Epilogue)를 빠짐없이
따라간다. 선수 지식은 따로 떼지 않고 **필요한 자리에서 aside 카드로** 그때그때 채운다.

원본 PDF: `ref/SLAM_Handbook.pdf` (669쪽 / 책 쪽번호 1–647)

이 책은 파트마다 성격이 완전히 다르다. 그래서 **장 유형에 따라 노트 템플릿을 바꿔 쓴다.**

| 유형 | 장 | 노트 방식 |
|---|---|---|
| A. 유도형 | 1 · 2 · 3 · 4 · 6 · 11 · 12 · 16 | 3단 — 개념 → 유도 → 예제 |
| B. 서베이형 | 5 · 7 · 8 · 9 · 10 · 13 · 14 · 15 · 17 · 18 | 5단 — 대표 방법을 골라 직접 유도 |
| C. 지도형 | Prelude I · II · III · Epilogue | 파트 조망 |

근거와 상세는 [`0_Contents.md`](0_Contents.md), 템플릿은 [`2_Template_and_Rule.md`](2_Template_and_Rule.md).

## 문서 안내

| 문서 | 내용 | 언제 보는가 |
|---|---|---|
| [`0_Contents.md`](0_Contents.md) | 학습 목차(절 구성 + 쪽번호), 장 유형, 추천 순서, 진행 상황 | **다음에 뭘 공부할지 정할 때.** 목차는 PDF 북마크에서 자동 생성된다 |
| [`1_Tools.md`](1_Tools.md) | 도구 스택과 **빌드·추출·점검 명령어** | HTML 을 만들 때, 그림을 뽑을 때, 참조를 점검할 때 |
| [`2_Template_and_Rule.md`](2_Template_and_Rule.md) | **노트 템플릿과 규칙** — 유형별 구조, 언어 규칙, 생략 금지, aside, 용어표 | **챕터 내용을 쓰기 직전에 반드시** |
| [`3_Pitfalls.md`](3_Pitfalls.md) | **실전에서 겪은 함정 20가지** | 시작 전에 한 번, 그리고 뭔가 이상할 때마다 |
| [`tools/asides/_GUIDE.md`](tools/asides/_GUIDE.md) | aside 카드(포스트잇) 작성법 | 배경 지식을 보충할 때 |

## 이 책의 설정 — 이미 조사해서 `kit.conf` 에 넣었다

전부 실측한 값이다. **다시 추측하지 마라.**

| 항목 | 값 | 비고 |
|---|---|---|
| `page_offset` | **16** (전 구간 일정) | PDF 북마크 146개로 교차검증 완료 |
| 판형 | A4 595×842 pt | 킷 기본값(576×648 단행본)과 다르다 |
| `caption_bold` | **no** | 라벨이 CMR9. `yes` 로 두면 캡션 205개를 전부 놓친다 |
| `caption_sep` | **none** | 콜론 없이 `Figure 5.1 Range sensing…` |
| `caption_size` | 8.0–10.5 | 삽입된 논문 스크린샷 안의 3.9pt 캡션 차단 |
| `heading_font` | **CMBX** | 절 제목이 본문과 같은 10pt 볼드라 크기로는 못 잡는다 |
| 그림·표 | Figure 225 · Table 8 · Algorithm 4 | `--list` 로 확인한 실제 값 |
| 참고문헌 | 1,320편 (`refs.json`) | 본문 인용 표시 3,265회 |

**Prelude 그림은 장 번호가 로마 숫자다** — `--chapter I` 로 준다.

> ⚠️ PyMuPDF 1.23.7 이 이 PDF 를 닫을 때 segfault(종료 코드 139)를 낸다.
> 데이터는 정상이지만 `&&` 로 명령을 이어 붙이면 끊긴다. `;` 를 쓰라 (`3_Pitfalls.md` A17).

## 한 번만 하는 준비 (이미 끝났다)

```bash
sudo apt install -y python3-fitz python3-numpy        # 머신마다 한 번
python3 _study_kit/tools/init_contents.py --write     # 목차 생성  → 0_Contents.md
python3 _study_kit/tools/check_toc.py                 # 135개 항목 · 불일치 0건 확인됨
python3 _study_kit/tools/build_refs.py --book-pages 551-644 --write   # → refs.json
```

## 작업 흐름 (챕터 하나마다 반복)

**모든 명령은 스터디 루트(`slam/SLAM_Handbook/`)에서 실행한다.**

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <PDF 시작> -l <PDF 끝> "ref/SLAM_Handbook.pdf" /tmp/ch.txt

# ② 그림·표 추출 — 책 쪽번호로 지정한다 (PDF 쪽 환산은 도구가 한다)
python3 _study_kit/tools/extract_figures.py --chapter 8 --book-pages 224-249 --list
python3 _study_kit/tools/extract_figures.py --chapter 8 --book-pages 224-249 \
    --out part2_in_practice/08_lidar/images --names _study_kit/tools/figure_names/ch8.txt

# ③ 노트 작성 — 2_Template_and_Rule.md 에서 그 장의 유형(A/B/C)에 맞는 템플릿을 고른다
#    배경 보충은 본문에 풀지 말고 [[aside]] 카드로, 인용은 [568] 원문 그대로

# ④ 위젯 (필요하면) — _study_kit/tools/widgets/_GUIDE.md

# ⑤ 빌드
python3 _study_kit/tools/build_html.py part2_in_practice/08_lidar/08_lidar.md

# ⑥ 검증 — 건너뛰지 마라
python3 _study_kit/tools/check_refs.py 08   # 그림·표·쪽번호·절 참조
python3 _study_kit/tools/check_toc.py       # 목차 쪽번호
#   빌드 출력의 ⚠ (정의 없는 aside · refs.json 에 없는 인용) 을 확인
#   본문의 손계산을 코드로 재계산해 대조   ← 오류가 가장 많이 나오는 곳
#   헤드리스로 렌더링·위젯 조작 확인
```

## 폴더 구조

```
slam/SLAM_Handbook/                 ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/SLAM_Handbook.pdf
├── _study_kit/                     ← 킷 루트
│   ├── kit.conf                    이 책의 설정 (위 표의 값들)
│   ├── refs.json                   참고문헌 1,320편 (build_refs.py 생성물)
│   ├── README.md  0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py           md → self-contained html (+ aside 카드 · 인용 확장)
│       ├── extract_figures.py      PDF에서 Figure/Table 크롭 추출
│       ├── init_contents.py        PDF 북마크 → 0_Contents.md          ← 신규
│       ├── build_refs.py           References → refs.json              ← 신규
│       ├── check_refs.py           노트의 참조를 원문과 대조
│       ├── check_toc.py            0_Contents.md 의 쪽번호를 원문과 대조
│       ├── kit_config.py           kit.conf 로더
│       ├── asides/*.md             aside 카드 (전역)                    ← 신규
│       ├── figure_names/chN.txt    챕터별 그림 파일명 매핑
│       ├── vendor/tex-svg.js       MathJax (외부 폰트 불필요)
│       └── widgets/*.html          Canvas 인터랙티브 위젯
├── part0_prep/00_notation/
├── part1_foundations/              00_prelude_1 · 01_factor_graphs … 06_certifiable
├── part2_in_practice/              00_prelude_2 · 07_visual … 12_leg
└── part3_spatial_ai/               00_prelude_3 · 13_deep_learning … 19_epilogue
```

- **챕터당 파일 1개** — 절이 많아도 쪼개지 않고 헤더로 탐색한다
- `images/` 를 챕터 폴더 안에 두어 각 챕터가 self-contained 하게 유지한다
- 완성된 `.html` 은 수식 엔진·이미지·위젯·카드가 전부 인라인되어 **인터넷 없이 열린다**
- **`.md` 가 원본, `.html` 은 생성물이다.** `.html` 을 직접 편집하지 않는다

## 이 자료가 지키는 원칙

- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **원문 대조 필수** — 기억이나 일반 지식으로 쓰지 않는다. 인용은 쪽번호를 남긴다
- **생략 금지** — 결과만 적지 않고 왜 그 식이 나오는지 매 단계 밝힌다. **카드 안에서도 같다**
- **검증 가능한 예제** — 손계산은 코드로 재계산해 대조한다
- **서베이를 서베이로 옮기지 않는다** — 유형 B 는 대표 방법을 골라 직접 유도한다
