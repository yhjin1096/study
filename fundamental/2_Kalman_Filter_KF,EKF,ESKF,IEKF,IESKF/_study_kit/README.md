# Notes on Kalman Filter 스터디

## 스터디 개요

Gyubeom Edward Im의 강의 노트 *Notes on Kalman Filter (KF, EKF, ESKF, IEKF, IESKF)*(49쪽)를
**내용 수정 없이 그대로** HTML로 옮기고, 이해를 돕는 **인터랙티브 위젯 11개**를 절 사이에 끼워 넣은
자료다. 추정 이론과 recursive bayes filter에서 출발해 다섯 종류의 칼만 필터와 그 유도, 그리고
MAP·Gauss-Newton과의 관계까지 원문 13개 장 전체를 다룬다.

원본 PDF: `ref/Notes on Kalman Filter(KF, EKF, ESKF, IEKF, IESKF).pdf`
결과물: `notes/notes_on_kalman_filter.html` (단일 파일 5.5MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/build_html.py notes/notes_on_kalman_filter.md
python3 _study_kit/tools/check_refs.py
```

### 이 스터디에서 원래 킷과 달라진 점

- **그림 추출** — 이 원문에도 `Figure`/`Table` 캡션이 **한 번도 나오지 않아** 캡션 기반인
  `extract_figures.py`를 쓸 수 없다. 이미지 객체의 bbox를 clip으로 삼는
  `tools/extract_images_bbox.py`로 24개를 뽑았다 (매핑은 스크립트 안 `NAMES`).
- **노트 배치** — 챕터별로 쪼개지 않고 `notes/` 아래 단일 `.md` 하나에 13개 장을 담았다.
  `check_refs.py`가 `part*/` 뿐 아니라 `notes/`도 훑도록 한 줄 넓혀 두었다.
- **함정 두 개 추가** — `3_Pitfalls.md` B5(인용구 안 여러 줄 `$$`), **B6(`\color`·`\boldsymbol`·
  `\cancel` 같은 autoload 매크로가 페이지 전체 수식을 죽이는 문제)**. B6은 이 스터디에서 실제로 밟았다.

## 작업 흐름 (챕터 하나마다 반복)

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <시작> -l <끝> "ref/Notes on Kalman Filter(KF, EKF, ESKF, IEKF, IESKF).pdf" /tmp/ch.txt

# ② 그림 추출 (캡션이 없는 문서라 bbox 방식)
python3 _study_kit/tools/extract_images_bbox.py --list
python3 _study_kit/tools/extract_images_bbox.py --out notes/images

# ③ 노트 작성 — notes/notes_on_kalman_filter.md 를 고친다
#    (원문 재현이 목적이라 2_Template_and_Rule.md 의 3단 구조는 적용하지 않았다)

# ④ 위젯 — _study_kit/tools/widgets/, 이 스터디의 위젯은 kf-*/ekf-*/eskf-*/iekf-*/ieskf 등

# ⑤ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_kalman_filter.md

# ⑥ 검증 — 아래 네 가지는 실제로 오류가 나왔던 항목이다
python3 _study_kit/tools/check_refs.py      # 쪽번호·절 참조 (이 문서엔 그림 캡션이 없다)
#   수식 번호 (1)~(166) 이 빠짐없이·순서대로 있는지 스크립트로 대조
#   수식이 실제로 렌더링됐는지 <mjx-container 개수로 확인   ← 3_Pitfalls B6
#   위젯을 헤드리스 브라우저로 열어 조작까지 해 본다
```

**⑥을 건너뛰지 마라.** 이 검증 절차로 손계산 오류·위젯 단위 버그·추출 스크립트 버그가 실제로
잡혔다. 자세한 명령은 `1_Tools.md`, 사례는 `3_Pitfalls.md`.

## 폴더 구조

```
2_Kalman_Filter_KF,EKF,ESKF,IEKF,IESKF/   ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/Notes on Kalman Filter(KF, EKF, ESKF, IEKF, IESKF).pdf
├── _study_kit/                    ← 킷 루트
│   ├── kit.conf                   오프셋 0 · Letter 판형 · 사이드바 머리말
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html
│       ├── extract_images_bbox.py 캡션 없는 문서용 bbox 추출 ★
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯 11개
└── notes/
    ├── notes_on_kalman_filter.md    ← 원본. 이것만 손으로 고친다
    ├── notes_on_kalman_filter.html  ← 생성물(5.5MB). 직접 편집하지 않는다
    └── images/fig_p*.png            ← PDF에서 뽑은 그림 24개
```

- **킷은 `_study_kit/` 안에 모여 있다.** 스터디 루트에는 원본과 노트만 남으므로,
  내가 쓴 것과 킷이 준 것이 섞이지 않는다. 킷을 새 버전으로 갈아 끼우기도 쉽다
- 킷을 스터디 루트에 펼쳐 놓아도 동작한다. 도구가 두 배치를 모두 인식한다
  (판정 규칙은 `tools/kit_config.py` 맨 위 설명)
- **문서 1개** — 원문이 한 편의 강의 노트라 장별로 쪼개지 않고 사이드바 목차로 탐색한다
- 그림 파일명은 `fig_p<PDF쪽>_<설명>.png` — 원문에 그림 번호가 없어 쪽번호로 식별한다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **원문 대조 필수** — 기억이나 일반 지식으로 쓰지 않는다. 인용은 쪽번호를 남긴다
- **생략 금지** — 유도를 결과만 적지 않고 왜 그 식이 나오는지 매 단계 밝힌다
- **검증 가능한 예제** — 손계산은 코드로 재계산해 대조한다

이 네 가지가 전체를 관통하는 원칙이고, 나머지는 그것을 지키기 위한 도구다.
