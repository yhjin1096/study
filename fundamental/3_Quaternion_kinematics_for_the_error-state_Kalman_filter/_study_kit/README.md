# Notes on Quaternion kinematics 스터디

## 스터디 개요

Gyubeom Edward Im의 강의 노트 *Notes on Quaternion kinematics for the error-state Kalman filter*
(58쪽, Joan Solà의 원논문을 한국어로 옮기고 보강한 것)를 **내용 수정 없이 그대로** HTML로 옮기고,
이해를 돕는 **인터랙티브 위젯 12개**를 절 사이에 끼워 넣은 자료다.
쿼터니언의 정의에서 출발해 회전 표현·규약·섭동과 자코비안·수치적분을 거쳐
IMU 기반 ESKF(지역 각 에러)와 전역 각 에러 ESKF까지, 원문 8개 장 전체를 다룬다.

원본 PDF: `ref/Notes on Quaternion kinematics for the error-state Kalman filter.pdf`
결과물: `notes/notes_on_quaternion_kinematics.html` (단일 파일 3.9MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/build_html.py notes/notes_on_quaternion_kinematics.md
python3 _study_kit/tools/check_refs.py
```

### 이 스터디에서 원래 킷과 달라진 점

- **판형이 A4다** — 앞의 두 스터디는 Letter(612×792)였고 이 문서는 A4(595.28×841.89)다.
  `kit.conf`의 `clip_x`·`header_y`·`body_x`를 실측해서 다시 잡았다.
- **처음으로 캡션이 있는 문서** — `Figure 1: …` 형식이라 `caption_style = flat`,
  `caption_bold = no`로 `extract_figures.py`가 19개를 전부 검출한다. 다만
  **캡션 기반 추출이 그림 위쪽 경계를 잘못 잡는 경우가 있어**(제목·수식까지 딸려 왔다)
  실제 추출은 bbox 기반 `tools/extract_images_bbox.py`로 했다. 이미지 객체 19개 ↔ 그림 19개가
  1:1이라 깔끔하게 떨어진다.
- **`check_refs.py`가 처음으로 검사할 것이 있다** — 본문이 "그림 1은 …", "테이블 18을 보면 …"처럼
  그림을 인용한다.
- **`\boldsymbol`을 전부 `\pmb`로 바꿨다** — 굵은 그리스 문자가 190곳 나오는 문서라
  `3_Pitfalls.md` B6 함정을 정면으로 밟는다. 안 바꾸면 **문서의 수식이 하나도 렌더링되지 않는다**.
  이 스터디에서 그 사실을 최소 예제로 다시 확인했다(아래 "검증" 참조).
- **위젯에 3D가 들어간다** — 회전을 다루는 문서라 정사영 3D 뷰가 필요했다.
  쿼터니언 연산 + 3D 장면 헬퍼를 `window.QK`로 만들어 위젯마다 같은 블록을 넣었다
  (중복 삽입돼도 `if (!window.QK)` 로 한 번만 정의된다).

## 작업 흐름

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <시작> -l <끝> \
    "ref/Notes on Quaternion kinematics for the error-state Kalman filter.pdf" /tmp/ch.txt

# ② 그림 추출 (캡션은 있지만 bbox 방식이 더 정확했다)
python3 _study_kit/tools/extract_images_bbox.py --list
python3 _study_kit/tools/extract_images_bbox.py --out notes/images

# ③ 노트 작성 — notes/notes_on_quaternion_kinematics.md 를 고친다
#    (원문 재현이 목적이라 2_Template_and_Rule.md 의 3단 구조는 적용하지 않았다)

# ④ 위젯 — _study_kit/tools/widgets/*.html, 이 스터디는 12개

# ⑤ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_quaternion_kinematics.md

# ⑥ 검증 — 아래 다섯 가지는 실제로 오류가 나왔던 항목이다
python3 _study_kit/tools/check_refs.py       # 그림·쪽번호·절 참조
#   수식 번호 (1)~(319) 가 빠짐없이·중복 없이·순서대로 있는지 스크립트로 대조
#   절 제목 99개를 PDF 본문에서 문자열로 다시 찾아 확인
#   <mjx-container 개수로 수식이 실제로 렌더링됐는지 확인   ← 3_Pitfalls B6
#   위젯 12개를 헤드리스 브라우저로 열어 버튼·슬라이더까지 조작해 본다
```

### 이번 빌드의 검증 결과

| 항목 | 결과 |
|---|---|
| 수식 번호 | (1)~(319) — 누락 0, 중복 0, 순서 일치 |
| 절 제목 | 99개 전부 PDF 본문/목차에서 확인 (오타 고친 3개 제외) |
| 그림 | 19개 전부 인라인 |
| 렌더링된 수식 | `<mjx-container` **976개**, 그중 display 324개 (`$$` 319 + 환경을 품은 인라인 5) |
| 위젯 | 12개 · 버튼 전부 클릭 + 슬라이더 min/중간/max 스윕 후 `ERRS=0 BLANK=0 NaN=0` |

## 폴더 구조

```
3_Quaternion_kinematics_for_the_error-state_Kalman_filter/   ← 스터디 루트
├── ref/Notes on Quaternion kinematics for the error-state Kalman filter.pdf
├── _study_kit/                    ← 킷 루트
│   ├── kit.conf                   오프셋 0 · A4 판형 · flat 캡션 · 사이드바 머리말
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html
│       ├── extract_figures.py     캡션 기반 추출 (이 문서는 flat 캡션)
│       ├── extract_images_bbox.py bbox 기반 추출 ★ 실제로 쓴 쪽
│       ├── figure_names/quaternion.txt   Figure N → 파일명 매핑
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯 12개
└── notes/
    ├── notes_on_quaternion_kinematics.md    ← 원본. 이것만 손으로 고친다
    ├── notes_on_quaternion_kinematics.html  ← 생성물(3.9MB). 직접 편집하지 않는다
    └── images/fig01…fig19_p<쪽>_<설명>.png  ← PDF에서 뽑은 그림 19개
```

- 그림 파일명은 `fig<번호>_p<쪽>_<설명>.png` — 원문 캡션이 `Figure N: …`으로 장 번호가 없어
  쪽번호를 함께 넣어 식별한다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **원문 재현이 최우선** — 문장·절 구성·수식 번호를 바꾸지 않는다. 고친 것은
  노트 맨 아래 "옮기며 바로잡은 것"에 전부 적는다
- **위젯은 본문 밖** — "원문에 없는 추가 요소"라고 표시된 회색 박스 안에만 둔다
- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **검증 가능한 위젯** — 위젯의 readout에는 공식값과 수치계산값을 나란히 찍어
  스스로 검산이 되게 한다 (예: 실험 4는 로드리게스 행렬과 쿼터니언 회전의 원소별 차이를 보여 준다)
