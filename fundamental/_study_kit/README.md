# <책 제목> 스터디

<!-- ══════════════════════════════════════════════════════════════════
     킷을 막 복사했다면 — 아래 "초기 설정"을 끝내고 이 주석 블록을 지운다.
     ══════════════════════════════════════════════════════════════════ -->

> ## 초기 설정 (킷 복사 직후 한 번)
>
> ### 0. 도구 설치 (머신마다 한 번)
>
> ```bash
> sudo apt install -y python3-fitz     # PyMuPDF — 그림 추출
> sudo apt install -y python3-numpy    # 노트의 검증용 코드 스니펫 실행 (선택)
> ```
>
> `build_html.py`는 순수 Python이라 추가 설치가 필요 없다. PIL(Pillow)은 대개 이미 있다.
> 이 환경에는 `pip`이 없으므로 파이썬 패키지는 apt로 설치한다.
>
> ### 1. 폴더를 만들고 킷을 **폴더째** 복사한다
>
> ```bash
> cd ~/yhj/study
> mkdir -p "My_Book/ref"
> cp -r _study_kit "My_Book/"            # → My_Book/_study_kit/  (폴더째)
> cp "원본.pdf" "My_Book/ref/"
> ```
>
> `My_Book/`이 **스터디 루트**(원본과 노트), `My_Book/_study_kit/`이 **킷 루트**(도구와 문서)다.
> 도구가 두 위치를 알아서 구분하므로 **모든 명령은 스터디 루트에서 실행한다.**
>
> ### 2. `kit.conf`를 채운다 — **여기서 시간을 아끼려 하지 마라**
>
> ```bash
> cd "My_Book"
> pdfinfo "ref/원본.pdf" | grep Pages                  # 총 쪽수를 눈으로 확인
> pdftotext -f 30 -l 30 "ref/원본.pdf" - | head -3     # 이 PDF 쪽의 인쇄 쪽번호는?
> python3 -c "import fitz; print(fitz.open('ref/원본.pdf')[0].rect)"   # 판형
> python3 _study_kit/tools/kit_config.py               # 채운 값이 이렇게 읽히는지 확인
> ```
>
> **페이지 오프셋을 추측하면 반드시 사고가 난다.** 앞·중간·뒤 세 곳에서 검증하고 적는다.
> 이유는 [`3_Pitfalls.md`](3_Pitfalls.md) A1·A2.
>
> ### 3. 목차를 만든다
>
> [`0_Contents.md`](0_Contents.md)의 틀에 학습 범위의 절 구성과 **책 쪽번호**를 옮겨 적는다.
> 이 파일이 이후 모든 작업의 기준이다 — 폴더 번호, 노트 구조, 참조 검사가 전부 여기를 본다.
> 다 적은 뒤 그 파일 아래쪽 "목차 검증" 스니펫으로 쪽번호를 대조한다.
>
> ### 4. 이 README의 제목과 아래 "스터디 개요"를 채우고, 이 안내 블록을 지운다

---

## 스터디 개요

<이 책으로 무엇을 어디까지 학습하는지 한두 문장.>

원본 PDF: `ref/<파일명>.pdf`

## 문서 안내

| 문서 | 내용 | 언제 보는가 |
|---|---|---|
| [`0_Contents.md`](0_Contents.md) | 학습 범위 목차 (절 구성 + 쪽번호), 추천 학습 순서, 진행 상황 | **다음에 뭘 공부할지 정할 때.** 새 챕터 노트의 절 구성을 여기서 가져온다. 폴더/파일 번호도 여기 장 번호를 따름 |
| [`1_Tools.md`](1_Tools.md) | 도구 스택과 **빌드·추출·점검 명령어** | HTML을 만들거나 다시 빌드할 때, 그림을 추출할 때, 참조를 점검할 때 |
| [`2_Template_and_Rule.md`](2_Template_and_Rule.md) | **노트 작성 템플릿과 규칙** — 3단 구조, 언어 규칙, 생략 금지, 용어표 | **챕터 내용을 쓰기 직전에 반드시.** 모든 챕터 `.md`가 이 구조를 따른다 |
| [`3_Pitfalls.md`](3_Pitfalls.md) | **실전에서 겪은 함정 15가지** | 시작 전에 한 번, 그리고 뭔가 이상할 때마다 |

## 작업 흐름 (챕터 하나마다 반복)

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <시작> -l <끝> "ref/원본.pdf" /tmp/ch.txt

# ② 그림·표 추출
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 --list
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 \
    --out part1_xxx/06_chapter/images --names _study_kit/tools/figure_names/ch6.txt

# ③ 노트 작성 — 2_Template_and_Rule.md 의 구조와 규칙을 따른다

# ④ 위젯 (필요하면) — _study_kit/tools/widgets/_GUIDE.md

# ⑤ 빌드
python3 _study_kit/tools/build_html.py part1_xxx/06_chapter/06_chapter.md

# ⑥ 검증 — 아래 세 가지는 실제로 오류가 나왔던 항목이다
python3 _study_kit/tools/check_refs.py 06   # 그림·표·쪽번호·절 참조
#   본문의 손계산을 코드로 재계산해 대조   ← 오류가 가장 많이 나오는 곳
#   위젯을 헤드리스 브라우저로 열어 확인   ← 조작까지 해 봐야 한다
```

**⑥을 건너뛰지 마라.** 이 검증 절차로 손계산 오류·위젯 단위 버그·추출 스크립트 버그가 실제로
잡혔다. 자세한 명령은 `1_Tools.md`, 사례는 `3_Pitfalls.md`.

## 폴더 구조

```
My_Book/                           ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/원본.pdf
├── _study_kit/                    ← 킷 루트 (복사해 온 폴더 전체)
│   ├── kit.conf                   이 스터디의 설정 (PDF·오프셋·레이아웃·사이드바)
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html
│       ├── extract_figures.py     PDF에서 Figure/Table 크롭 추출
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더 (스크립트들이 공유)
│       ├── figure_names/chN.txt   챕터별 그림 파일명 매핑 (추출 재현용)
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯
└── part1_xxx/
    └── 01_chapter_name/
        ├── 01_chapter_name.md    ← 원본. 이것만 손으로 고친다
        ├── 01_chapter_name.html  ← 생성물. 직접 편집하지 않는다
        └── images/
```

- **킷은 `_study_kit/` 안에 모여 있다.** 스터디 루트에는 원본과 노트만 남으므로,
  내가 쓴 것과 킷이 준 것이 섞이지 않는다. 킷을 새 버전으로 갈아 끼우기도 쉽다
- 킷을 스터디 루트에 펼쳐 놓아도 동작한다. 도구가 두 배치를 모두 인식한다
  (판정 규칙은 `tools/kit_config.py` 맨 위 설명)
- 폴더 앞 번호는 `0_Contents.md`의 장 번호를 그대로 따른다
- **챕터당 파일 1개** — 절이 많아도 쪼개지 않고 헤더로 탐색한다 (흐름 파악에 유리)
- `images/`를 챕터 폴더 안에 두어 각 챕터가 self-contained하게 유지한다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **원문 대조 필수** — 기억이나 일반 지식으로 쓰지 않는다. 인용은 쪽번호를 남긴다
- **생략 금지** — 유도를 결과만 적지 않고 왜 그 식이 나오는지 매 단계 밝힌다
- **검증 가능한 예제** — 손계산은 코드로 재계산해 대조한다

이 네 가지가 전체를 관통하는 원칙이고, 나머지는 그것을 지키기 위한 도구다.
