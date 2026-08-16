# Notes on Lie Theory 스터디

## 스터디 개요

Gyubeom Edward Im의 강의 노트 *Notes on Lie Theory*(26쪽, Joan Solà의
*Lie theory for the roboticist* 영상을 바탕으로 정리한 것)를 **내용 수정 없이 그대로** HTML로 옮기고,
이해를 돕는 **인터랙티브 위젯 11개**를 절 사이에 끼워 넣은 자료다.
군의 정의 → Lie Group / Lie Algebra / 접평면 → SO(3) → SE(3) → on-manifold EKF와
Pose Graph SLAM까지, 원문 8개 장 전체를 다룬다.

원본 PDF: `ref/Notes on Lie Theory.pdf`
결과물: `notes/notes_on_lie_theory.html` (단일 파일 4.0MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/build_html.py notes/notes_on_lie_theory.md
python3 _study_kit/tools/check_refs.py
```

### 이 스터디에서 원래 킷과 달라진 점

- **★ 처음으로 원문의 색 강조를 재현했다.** 앞의 세 스터디(확률론·칼만 필터·쿼터니언)에서는
  "색은 재현하지 않았다"고 적었는데, 그 문서들은 색이 **수식 안**에 있어 `\color` 매크로가
  필요했기 때문이다(오프라인 번들에 color 패키지가 없어 쓰면 문서 전체 수식이 죽는다 — B6).
  이 문서의 파란 강조(#197fb2, 6쪽에 12곳)는 **산문**에 쓰인 것이라 CSS만으로 충분하다.
  그리고 **MathJax SVG 글리프는 `currentColor`를 상속하므로** 색칠한 span 안의 인라인 수식도
  함께 물든다 — TeX 매크로를 전혀 쓰지 않으니 B6 함정과 무관하다.
- **빌더에 두 가지를 더했다** (`tools/build_html.py`)
  - `==강조==` → `<span class="hl">` (색 변수 `--hl`, 라이트 `#197fb2` / 다크 `#57b6e4`)
  - `> [!TIP]` 로 시작하는 인용구 → `.callout` 박스. 원문 p.26의 tcolorbox 하나를 재현한다
- **그림 추출은 bbox 방식** — 이 문서에도 캡션이 하나도 없다(`Figure`/`Table` 전문 0회).
  이미지 객체 29개와 그림 29개가 1:1이라 `tools/extract_images_bbox.py`가 깨끗하게 떨어진다
  (`3_Pitfalls.md` A10).
- **위젯 헬퍼가 `window.LG`로 바뀌었다** — 쿼터니언 스터디의 `QK`(쿼터니언 + 3D 씬)를
  행렬 Lie group으로 다시 썼다. `hat`/`vee`, SO(3)·SE(3)의 `exp`/`log`, 좌·우 자코비안과
  그 역행렬, `Ad`, `Q_l`/`Q_r`, 6×6 일반 역행렬, 그리고 정사영 3D 씬이 들어 있다.
  헬퍼는 위젯마다 같은 블록으로 들어가되 `if (!window.LG)` 로 한 번만 정의된다.

### 헬퍼를 믿기 전에 검산한 것

`LG`는 위젯 11개가 전부 의존하므로 먼저 헤드리스 브라우저에서 항등식으로 검산했다.

| 검산 | 결과 |
|---|---|
| `RRᵀ = I`, `Log(Exp(w)) = w` | 5.6e-17 / 0.0 |
| θ ≈ π 근처 로그 왕복 | 1.3e-9 (부호 판정을 반대칭 성분으로 가린 뒤) |
| 식 (50) `Jl(w) = Jr(−w) = Jrᵀ(w)` | 0.0 |
| 식 (48) BCH — Jr 사용 / 미사용 | 6.7e-10 / 4.1e-5 |
| 식 (44)(71) Adjoint 항등식 | 1.1e-16 / 2.2e-16 |
| 식 (64)(67) SE(3) exp·log 왕복 | 2.5e-16 |
| 식 (79) `Ql(ξ) = Qr(−ξ)` | 0.0 |

이 과정에서 **식 (75)·(77)의 블록 배치가 식 (55)의 성분 순서와 어긋난다**는 것을 발견했다.
수치 미분으로 구한 6×6 자코비안과 대조하니 `ξ = [ω; v]` 순서에서는 `Q`가 **왼쪽 아래**여야
맞는다(오차 1.4e-10). 원문의 `[[J, Q], [0, J]]` 배치는 `ξ = [v; ω]` 순서를 전제한 것이다.
본문은 원문 그대로 두고, **실험 9**가 두 배치를 나란히 돌려 기울기 2 대 1로 보여 준다.

## 작업 흐름

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 반드시 PDF를 직접 열어 확인하며 쓴다 (기억에 의존 금지)
pdftotext -layout -f <시작> -l <끝> "ref/Notes on Lie Theory.pdf" /tmp/ch.txt

# ② 그림 추출 (캡션이 없는 문서라 bbox 방식)
python3 _study_kit/tools/extract_images_bbox.py --list
python3 _study_kit/tools/extract_images_bbox.py --out notes/images

# ③ 노트 작성 — notes/notes_on_lie_theory.md 를 고친다
#    원문의 파란 강조는 ==이렇게== 감싼다

# ④ 위젯 — _study_kit/tools/widgets/*.html (11개). //%LG% 자리에 헬퍼를 넣어 조립한다

# ⑤ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_lie_theory.md

# ⑥ 검증
python3 _study_kit/tools/check_refs.py       # 절·쪽번호 참조
#   수식 번호 (1)~(91) 이 빠짐없이·중복 없이·순서대로 있는지 스크립트로 대조
#   절 제목 36개를 PDF 본문에서 문자열로 다시 찾아 확인
#   <mjx-container 개수로 수식이 실제로 렌더링됐는지 확인   ← 3_Pitfalls B6
#   위젯 11개를 헤드리스로 열어 버튼·슬라이더까지 조작해 본다
```

### 이번 빌드의 검증 결과

| 항목 | 결과 |
|---|---|
| 수식 번호 | (1)~(91) — 누락 0, 중복 0, 순서 일치 |
| 절 제목 | 36개 전부 PDF 본문/목차에서 확인 (오타 고친 1개 제외) |
| 그림 | 29개 전부 인라인 |
| 렌더링된 수식 | `<mjx-container` **376개**, 그중 display 96개 (`$$` 91 + 환경을 품은 인라인 5) |
| 색 강조 | `.hl` 12곳 — 원문 p5·p6·p12·p16·p22·p25 의 파란 span 개수와 일치 |
| Tip 박스 | 1개 (원문 p.26) |
| 위젯 | 11개 · 버튼 전부 클릭 + 슬라이더 min/중간/max 스윕 후 `ERRS=0 BLANK=0 NaN=0` |

## 폴더 구조

```
0_Lie Theory/                      ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/Notes on Lie Theory.pdf
├── _study_kit/                    ← 킷 루트
│   ├── kit.conf                   오프셋 0 · A4 · 캡션 없음 · clip_x 66-530
│   ├── README.md                  이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py          md → self-contained html (==강조==, [!TIP] 지원)
│       ├── extract_images_bbox.py bbox 기반 추출 ★ 이 문서에서 쓰는 쪽
│       ├── extract_figures.py     캡션 기반 (이 문서엔 캡션이 없어 쓰지 않는다)
│       ├── figure_names/lie_theory.txt  파일명 → 무엇을 그린 그림인가
│       ├── check_refs.py          노트의 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더
│       ├── vendor/tex-svg.js      MathJax (외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯 11개
└── notes/
    ├── notes_on_lie_theory.md     ← 원본. 이것만 손으로 고친다
    ├── notes_on_lie_theory.html   ← 생성물(4.0MB). 직접 편집하지 않는다
    └── images/fig01…fig29_p<쪽>_<설명>.png   ← PDF에서 뽑은 그림 29개
```

- 원문에 그림 번호가 없으므로 파일명의 `figNN`은 **등장 순서**로 이 스터디가 붙인 번호다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 **인터넷 없이 단독으로 열린다**

## 이 자료가 지키는 원칙

- **원문 재현이 최우선** — 문장·절 구성·수식 번호를 바꾸지 않는다. 고친 것은
  노트 맨 아래 "옮기며 바로잡은 것"에 전부 적는다
- **위젯은 본문 밖** — "원문에 없는 추가 요소"라고 표시된 회색 박스 안에만 둔다
- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **검증 가능한 위젯** — readout에 공식값과 수치계산값을 나란히 찍어 스스로 검산이 되게 한다
  (예: 실험 3은 식 (8)의 정의를 τ→0 으로 수렴시켜 해석적 자코비안과 대조하고,
  실험 11은 최적화 뒤에도 회전 제약조건이 저절로 지켜지는 것을 1e-16 수준으로 보여 준다)
