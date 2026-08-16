# On-manifold IMU Preintegration 스터디

Gyubeom Edward Im의 강의 노트 *Notes on On-manifold preintegration for real-time
visual-inertial odometry*(18쪽, 원논문은 C. Forster 외)를 **내용 수정 없이 그대로** HTML로
옮기고, 이해를 돕는 **인터랙티브 위젯 12개**를 절 사이에 끼워 넣은 자료다.
SO(3) 기초 → MAP/factor graph → IMU 모델 → preintegration → residual·자코비안까지,
원문 30개 절 전체를 다룬다.

원본 PDF: `ref/Notes on On-manifold preintegration for real-time visual-inertial odometry.pdf`
결과물: `notes/notes_on_preintegration.html` (단일 파일 2.5MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/inject_helper.py             # 위젯에 window.PI 주입
python3 _study_kit/tools/build_html.py notes/notes_on_preintegration.md
python3 _study_kit/tools/check_refs.py
```

## 이 스터디에서 원래 킷과 달라진 점

### ① 함정 B6 을 **피하지 않고 해결했다**

이 문서는 색을 **두 가지** 쓴다.

| 색 | 어디에 | 폰트 | 개수 | 어떻게 옮겼나 |
|---|---|---|---|---|
| `#197fb2` 파랑 | 산문 강조 | nanum·SFBX (고딕/산세리프) | 29구간 | `==강조==` → `<span class="hl">` |
| `#a50000` 진홍 | **수식 내부** | CMMI·CMSY·CMEX·CMMIB (수학) | 57구간 | `\color{#a50000}{...}` |

진홍은 CSS 로 못 만든다. 그런데 `\color` 는 MathJax 의 autoload 대상이라 그냥 쓰면
오프라인에서 네트워크 요청이 실패하고 **페이지의 모든 수식이 조용히 사라진다**
(`3_Pitfalls.md` B6). 앞선 다섯 스터디는 이 매크로를 안 쓰는 쪽으로 피해 다녔다.

해결책은 **컴포넌트를 번들에 이어 붙이는 것**이다.

```bash
# mathjax@3.2.2 es5/input/tex/extensions/{color,boldsymbol}.js
cat tex-svg.js color.js boldsymbol.js > _study_kit/tools/vendor/tex-svg.js
```

그리고 `build_html.py` 의 tex 설정에 한 줄:

```js
packages: {'[+]': ['color', 'boldsymbol']}
```

**`loader: {load: ['[tex]/color']}` 로 부르면 안 된다** — 그러면 다시 네트워크를 타서 B6 에 걸린다.
같은 방법으로 `cancel.js` 는 동작하지 않았다(이 문서에는 필요 없다).

`\boldsymbol` 이 같이 살아난 것이 그냥 덤이 아니다. 이 문서는 볼드 그리스 문자
($\boldsymbol{\omega}, \boldsymbol{\eta}, \boldsymbol{\phi}, \boldsymbol{\Sigma}$)가 본문 전반에 깔려 있어
쿼터니언 스터디처럼 `\pmb` 로 치환하면 원문과 모양이 달라진다.

**어두운 배경 보정** — `\color` 값은 SVG 에 `fill`/`stroke` **속성**으로 박힌다. CSS 프로퍼티가
속성을 이기므로 `[fill="#a50000"] { fill:#f2736b }` 규칙 하나로 다크 테마에서만 밝게 띄웠다.
원문 값을 바꾸는 것이 아니라 표시만 보정하는 것이다.

### ② 그림이 하나도 없다

이미지 객체 0개, 전문에서 `Figure`/`Table` 0회, 30pt 넘는 벡터 드로잉 0개다
(p15~17 의 드로잉 20~37개는 전부 분수선·행렬 괘선·overbrace 다).
`extract_figures.py` 와 `extract_images_bbox.py` 를 **이 스터디에서는 쓰지 않는다.**

### ③ 색 위치 추출 도구를 새로 만들었다

`tools/dump_colored.py` — 쪽 단위로 `(색, 텍스트, 가장 가까운 식 번호)` 를 뽑는다.
진홍 57구간을 눈으로 찾으면 반드시 샌다. 전사할 때 이 출력을 옆에 놓고 대조했다.

```bash
python3 _study_kit/tools/dump_colored.py --count      # 개수만 (검증용)
python3 _study_kit/tools/dump_colored.py -p 9 -c red  # 9쪽의 진홍 구간
```

### ④ 헬퍼를 파일 하나로 두고 주입한다

위젯 12개 중 11개가 같은 계산 라이브러리를 쓴다. 완성 HTML 은 단일 파일이어야 하니
헬퍼를 위젯마다 인라인해야 하는데, 12벌을 손으로 복사해 두면 한 곳을 고칠 때 어긋난다.
그래서 원본은 `widgets/_pi_helper.js` 한 벌만 두고 위젯에는 `//%PI%` 표시만 남긴 뒤
`tools/inject_helper.py` 로 채운다. 다시 돌려도 되고 `--check` 로 어긋난 파일만 볼 수도 있다.

### ⑤ 수식 축소 하한을 70% → 62% 로 낮췄다

(33)(79) 처럼 한 줄에 좌표계 첨자·물결·bias·노이즈가 다 붙은 수식이 있어
70% 로는 폭을 넘긴다. `build_html.py` 의 `MIN` 값이다.

## window.PI — 위젯이 공유하는 계산 라이브러리

앞부분은 `0_Lie_Theory` 스터디의 `window.LG`(SO(3)/SE(3) 지수·로그, 오른쪽 자코비안, 3D 씬)를
그대로 가져왔고, 뒷부분이 이 스터디에서 새로 쓴 것이다.

| 갈래 | 함수 |
|---|---|
| 난수 | `rng`(mulberry32 시드) `randn` `randnVec` |
| 대칭행렬 | `chol` `symmetrize` `fro` |
| 미분 | `numJac` (중심차분) |
| IMU 시뮬 | `truth` `trueOmega` `makeMeas` (식 29) |
| 적분 | `integrate` (식 34) |
| preintegration | `preint` (식 37·58·66 을 한 번에 누적) `biasUpdate` (식 48) `relFromStates` (식 37 좌변) `residual` (식 49) |
| 그리기 | `plot` (2D 축·격자·곡선·막대) `fmt` |

`preint` 하나가 $\Delta\mathbf{R},\Delta\mathbf{v},\Delta\mathbf{p}$ 와 9×9 공분산 $\boldsymbol{\Sigma}_{ij}$,
그리고 식 (66)의 bias 자코비안 다섯 개를 **같은 루프에서 누적**한다. 실제 구현이 그렇게 한다.

### 헬퍼를 믿기 전에 검산한 것

위젯 11개가 전부 여기에 기대므로, 쓰기 전에 헤드리스 브라우저에서 항등식으로 먼저 검산했다.

| 검산 | 결과 |
|---|---|
| 식 (6)(7) `Log(Exp(w)) = w` | 2.2e-16 |
| `RᵀR = I` | 2.9e-16 |
| **식 (12)** `R Exp(φ) Rᵀ = Exp(Rφ)` | 3.2e-16 |
| **식 (8)(9)** `Jr` 를 수치미분과 대조 | 1.6e-10 |
| 식 (11) `Jr Jr⁻¹ = I` | 1.8e-16 |
| **식 (37) 불변성** — `R_i,v_i,p_i` 세 가지에서 좌변=우변 | 5.3e-15 |
| **식 (48)** 1차 보정 오차 (δb=1e-2 / 5e-3) | 2.1e-4 / 5.2e-5 → **수렴차수 2.00** |
| **식 (58)** Σ vs 몬테카를로 4000회 — 전체 / 대각 최대 | 3.4% / 4.8% (표본오차 ±2.2%) |
| Σ 의 대칭성 · 양정치 | 8.6e-21 · Cholesky OK |
| **식 (72)(76)(80)** 해석 자코비안 vs 수치미분 (9×24) | 7.1e-10 (‖J‖=8.3) |
| 오일러 적분 vs SO(3) 적분 (pitch 40°) | 6.9e-4 rad — 실제 모델 차이 |

이 표가 있기 때문에 위젯 readout 에 찍히는 `1e-15` 들을 **결과의 정확성 근거**로 쓸 수 있다.

**검산 중에 테스트 쪽 실수를 두 번 잡았다.** ⓐ `Jr` 검산에서 `Log(Exp(w)Exp(x−w))` 를 미분하면
$\mathbf{J}_r^{-1}$ 이 나온다 — $\mathbf{J}_r$ 를 보려면 `Log(Exp(w)ᵀExp(x))` 를 미분해야 한다.
ⓑ 공분산 검산에서 몬테카를로는 **이산** 노이즈를 뿌리는데 $\boldsymbol{\Sigma}_\eta$ 에는
식 (35)대로 $\sigma^2/\Delta t$ 를 넣어 두어 정확히 $1/\Delta t = 200$ 배가 어긋났다
(상대오차가 99.5% = 1 − 1/200 로 나온 것이 단서였다).

## 작업 흐름

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 기호를 정확히 보려면 layout 모드가 낫다 (물결·바가 살아 있다)
pdftotext -layout -f <시작> -l <끝> "ref/Notes on ... .pdf" /tmp/ch.txt
#    구조와 색은 쪽 이미지를 직접 봐야 한다

# ② 색 위치를 먼저 뽑아 놓고 시작한다 — 이 문서는 색이 두 가지다
python3 _study_kit/tools/dump_colored.py -c blue
python3 _study_kit/tools/dump_colored.py -c red

# ③ 노트 작성 — notes/notes_on_preintegration.md
#    파란 강조는 ==이렇게==, 수식 안의 진홍은 \color{#a50000}{...}
#    \color 는 두 인자를 받으므로 \color{black} 으로 되돌릴 필요가 없다

# ④ 위젯 — _study_kit/tools/widgets/*.html (12개)
python3 _study_kit/tools/inject_helper.py

# ⑤ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_preintegration.md

# ⑥ 검증
python3 _study_kit/tools/check_refs.py
#   식 번호 (1)~(82) 가 빠짐없이·중복 없이·순서대로 있는지
#   절 제목 30개를 PDF 목차·본문에서 문자열로 다시 찾아 확인
#   ==강조== 29 · \color 57 을 dump_colored.py --count 와 대조   ← 안 맞으면 빠뜨린 것이다
#   <mjx-container 개수로 수식이 실제로 렌더링됐는지 확인        ← 3_Pitfalls B6
#   data-mjx-error 가 0 인지 — ★ <script> 를 먼저 지우고 세라.
#     MathJax 번들 소스 자체에 'merror' 와 '"data-mjx-error"' 문자열이 들어 있어
#     그냥 세면 각각 3건씩 잡힌다 (실제 오류가 아니다)
#   위젯 12개를 헤드리스로 열어 버튼·슬라이더까지 조작해 본다
```

### 이번 빌드의 검증 결과

| 항목 | 결과 |
|---|---|
| 수식 번호 | (1)~(82) — 누락 0, 중복 0, 순서 일치 |
| 절 | 30개 (본문 없는 1장·6장·A.4 포함) |
| 그림 | 0개 (원문에 없음) |
| 렌더링된 수식 | `<mjx-container` **575개**, display 82개 · 실제 `data-mjx-error` **0** |
| 색 강조 | `.hl` **29곳** · `\color{#a50000}` **57곳** — 둘 다 `dump_colored.py --count` 와 일치 |
| 위젯 | 12개 · 버튼 전부 클릭 + 슬라이더 min/중간/max 스윕 후 `ERRS=0 BLANK=0 BAD=0` |
| `check_refs.py` | 문제 0건 |

## 폴더 구조

```
4_On-manifold_preintegration_.../   ← 스터디 루트 (여기서 명령을 실행한다)
├── ref/Notes on On-manifold preintegration ... .pdf
├── _study_kit/                     ← 킷 루트
│   ├── kit.conf                    오프셋 0 · A4 · 그림 없음 · 색 두 가지
│   ├── README.md                   이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py           md → self-contained html (==강조==, \color, [!TIP])
│       ├── dump_colored.py         ★ 원문의 색 강조 구간을 쪽 단위로 추출
│       ├── inject_helper.py        ★ 위젯의 //%PI% 자리에 헬퍼를 채운다
│       ├── check_refs.py           노트의 참조를 원문과 대조
│       ├── kit_config.py           kit.conf 로더
│       ├── extract_figures.py      (이 문서엔 그림이 없어 쓰지 않는다)
│       ├── extract_images_bbox.py  (같음)
│       ├── vendor/tex-svg.js       MathJax + color + boldsymbol ★ 이 스터디에서 다시 만든 것
│       └── widgets/
│           ├── _pi_helper.js       ★ window.PI 원본 (여기만 고친다)
│           └── *.html              Canvas 인터랙티브 위젯 12개
└── notes/
    ├── notes_on_preintegration.md    ← 원본. 이것만 손으로 고친다
    └── notes_on_preintegration.html  ← 생성물(2.5MB). 직접 편집하지 않는다
```

## 이 자료가 지키는 원칙

- **원문 재현이 최우선** — 문장·절 구성·수식 번호를 바꾸지 않는다. 본문이 없는 절도
  비어 있는 채로 둔다. 고친 것은 노트 맨 아래 "옮기며 바로잡은 것"에 전부 적는다
- **위젯은 본문 밖** — "원문에 없는 추가 요소"라고 표시된 회색 박스 안에만 둔다
- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **검증 가능한 위젯** — readout 에 원문 식의 값과 독립적인 수치실험 값을 나란히 찍는다
  (실험 7은 (37) 좌변과 우변, 실험 8은 (58)과 몬테카를로, 실험 9는 (48)과 재적분,
  실험 11은 (72)(76)(80)과 수치미분)
