# VINS-Mono Formula Derivation 스터디

Edward Gyubeom Im의 강의 노트 *Formula Derivation and Analysis of the VINS-Mono*
(22쪽, 원문은 Yibin Wu)를 **내용 수정 없이 그대로** HTML로 옮기고, 이해를 돕는
**인터랙티브 위젯 12개**를 절 사이에 끼워 넣은 자료다.
IMU preintegration → 에러 상태 방정식 → 초기화 → tightly-coupled 최적화 → marginalization까지,
원문 8개 장 18개 절 전체를 다룬다.

원본 PDF: `ref/Formula Derivation and Analysis of the VINS-Mono.pdf`
결과물: `notes/notes_on_vins_mono.html` (단일 파일 3.4MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/inject_helper.py             # 위젯에 window.VM 주입
python3 _study_kit/tools/build_html.py notes/notes_on_vins_mono.md
python3 _study_kit/tools/check_refs.py
```

## 이 스터디에서 원래 킷과 달라진 점

### ① 색이 세 가지다

| 색 | 어디에 | 폰트 | 개수 | 어떻게 옮겼나 |
|---|---|---|---|---|
| `#197fb2` 파랑 | 산문 강조 | nanum·SFBX | 23구간 | `==강조==` → `<span class="hl">` |
| `#ff0000` 빨강 | **수식 안** | CM 계열 | 4구간 | `\color{#ff0000}{...}` |
| `#0000ff` 파랑 | **수식 안** | CM 계열 | 4구간 | `\color{#0000ff}{...}` |

수식 안의 두 색은 <b>짝</b>으로 쓰인다 — p14 (41)의 $\mathbf{p}_c^b$(빨강)/$\mathbf{q}_c^b$(파랑),
p18 (66)의 $\mathbf{P}_w^{b_j}$/$\mathbf{P}_b^c$ 가 (68)의 성질로 부호가 뒤집히는 것을 보여 준다.
`\color` 는 4번 스터디에서 만든 color·boldsymbol 번들이 그대로 처리한다 (`3_Pitfalls.md` B6).

`tools/dump_colored.py` 의 색 목록을 세 개로 늘리고 `-c prose|math` 무리 지정을 더했다.
다른 문서를 다룰 때는 파일 위쪽 `NAME` 만 고치면 된다.

```bash
python3 _study_kit/tools/dump_colored.py --count      # 개수만 (검증용)
python3 _study_kit/tools/dump_colored.py -c math      # 수식 안의 색만
```

**"23구간"과 노트의 `==강조==` 24개가 다른 이유** — p11 에서 문단 끝 문장과
바로 이어지는 소제목 "Midpoint numerical integration method:" 사이에 검은 글자가 없어서
추출기가 <b>한 덩어리</b>로 센다. 논리적으로는 둘이므로 노트에서는 24개로 나눴다.
(선형대수 스터디의 114 vs 113 과 같은 종류의 차이다.)

### ② 그림 10개 · 캡션은 딱 하나

전문에서 `Figure` 가 1회 — p13 의 "Figure 1: Initialization procedure" 뿐이고
나머지 9개는 캡션이 없다. 그래서 캡션 기반 `extract_figures.py` 를 못 쓰고
`extract_images_bbox.py` 를 썼다. 이미지 객체 10개와 그림 10개가 1:1 이라 깨끗하게 떨어진다
(`3_Pitfalls.md` A10).

### ③ 헬퍼가 `window.VM` 이다 — 쿼터니언 기반

이 문서는 SO(3)가 아니라 **쿼터니언**으로 쓰여 있다 (`⊗`, `Ω_L`/`Ω_R`, `α/β/γ`).
그래서 4번 스터디의 `window.PI` 를 바탕으로 쿼터니언 대수를 새로 얹었다.
쿼터니언은 `[w, x, y, z]` 순서이고, 중력은 원문 NOMENCLATURE 대로 $\mathbf{g}^w = [0,0,+9.8]$ 이다
(부호에 주의 — 실제 중력가속도는 $-\mathbf{g}^w$).

| 갈래 | 함수 |
|---|---|
| 쿼터니언 | `qmul qconj qinv qnorm qunit qxyz qexp qlog qsmall q2R R2q` |
| 곱셈 연산자 | `OmegaL OmegaR` (NOMENCLATURE) |
| IMU 시뮬 | `truthVI trueOmegaVI makeMeasVI` (식 2) · `integrateVI` (식 4·5) |
| preintegration | `preintVI` (식 9·10 + 27·28 + 37·38 을 한 루프에서) · `biasUpdateVI` (식 29) |
| residual | `relFromStatesVI` (식 7 좌변) · `residualVI` (식 60) |
| 선형대수 | `solveLS` · `schur` (식 79~82) · `tangentBasis` (식 47·70) |
| 상속분 | `PI` 의 SO(3)·3D 씬·난수·`numJac`·2D 플롯 전부 |

`preintVI(M, dt, bg, ba, Q, method)` 하나가 $\alpha,\beta,\gamma$ 와 15×15 $\mathbf{P}$, 15×15 $\mathbf{J}$ 를
같은 루프에서 누적한다. `method: 'euler'` 를 주면 식 (10)으로 바뀐다.
상태 순서는 식 (37) 그대로 $[\delta\alpha, \delta\boldsymbol{\theta}, \delta\beta, \delta\mathbf{b}_a, \delta\mathbf{b}_g]$ 다.

### 헬퍼를 믿기 전에 검산한 것

| 검산 | 결과 |
|---|---|
| $\mathbf{q}\otimes\mathbf{q}^{-1}=1$ · $\|\mathbf{q}\|-1$ | 2.2e-16 · 1.1e-16 |
| $\mathbf{R}\{\mathbf{q}_1\otimes\mathbf{q}_2\} = \mathbf{R}\{\mathbf{q}_1\}\mathbf{R}\{\mathbf{q}_2\}$ | 2.7e-16 |
| `R2q(q2R(q))` 왕복 · `qlog(qexp(v))` 왕복 | 0.0 · 5.6e-17 |
| `q2R(qexp(v))` = `expSO3(v)` (PI 와의 정합) | 4.6e-16 |
| **NOMENCLATURE** $\Omega_L(\boldsymbol{\omega})\mathbf{q}=\boldsymbol{\omega}\otimes\mathbf{q}$ · $\Omega_R(\boldsymbol{\omega})\mathbf{q}=\mathbf{q}\otimes\boldsymbol{\omega}$ | 1.1e-16 · 0.0 |
| **식 (6)** $\dot{\mathbf{q}}=\frac{1}{2}\Omega_R(\boldsymbol{\omega})\mathbf{q}$ — 수치미분 대조 | 2.4e-11 |
| **식 (7) 불변성** — $\mathbf{q}_i,\mathbf{v}_i,\mathbf{p}_i$ 세 가지에서 좌변=우변 | 8.2e-15 |
| **식 (9)** mid-point $\alpha$ 오차 (δt 0.02/0.01/0.005) | 9.9e-5 / 2.5e-5 / 6.2e-6 → **차수 2.00** |
| **식 (10)** euler $\alpha$ 오차 | 1.3e-2 / 6.6e-3 / 3.3e-3 → **차수 1.00** |
| **식 (27)** $\mathbf{P}$ 대칭성 · 양정치 | 1.2e-21 · Cholesky OK |
| **식 (60)** residual (정답 상태에서) | 2.7e-15 |
| **식 (82)** Schur 해 = 전체 해 · $\mathbf{H}_p$ 대칭성 | 4.4e-15 · 1.6e-15 |
| **식 (47)** basis 직교성 $\mathbf{b}_1\cdot\mathbf{b}_2$, $\mathbf{b}_i\cdot\mathbf{g}$ | 0.0 · 1.4e-17 |

**검산 중에 잡은 것 세 가지.**

ⓐ `integrateVI` 를 오일러로, `preintVI` 를 mid-point 로 두었더니 식 (7)의 좌변=우변이
**5.6e-3** 으로 나왔다. 식이 틀린 게 아니라 **양쪽 수치 해법이 달라서** 생긴 $O(\delta t^2)$ 차이였다.
같은 mid-point 로 맞추니 8.2e-15 가 됐다. → 헬퍼에 주석으로 못 박아 두었다.

ⓑ **식 (29)의 bias 1차 보정 오차는 $\|\delta\mathbf{b}\|^2$ 이 아니라 $O(\delta\mathbf{b}\cdot\delta t)$ 다.**
1차 보정이니 2차 수렴을 기대했는데 기울기가 계속 1.00 이었다. 원인을 추적하니
(38)의 $\mathbf{F}_{11} = \mathbf{I}-[\cdot]_\times\delta t$ 와 $-\delta t\mathbf{I}$ 가 **그 자체로 $\delta t$ 에 대한 1차 근사**여서
(엄밀한 값은 $\mathbf{R}^\intercal$ 와 $\mathbf{J}_r\delta t$) $\mathbf{J}$ 가 $O(\delta t)$ 만큼 어긋나기 때문이었다.
$\delta t$ 를 절반으로 줄이면 오차 계수도 정확히 절반이 되는 것으로 확인했다
(1.03e-3 → 5.16e-4 → 2.58e-4 → 1.28e-4). 실험 5가 이것을 보여 준다.

ⓒ 실험 9의 첫 판은 "①의 가장 작은 고유값이 정규화 항 λ 그 자체다"라고 적었는데
**화면의 숫자는 4.1e-1 이었다.** 측정값이 여러 개면 $\mathbf{m}_k$ 마다 못 보는 방향이 달라
$\mathbf{H}$ 가 수치적으로 랭크 4 가 되기 때문이다. 랭크 결손은 측정값이 **1개일 때만** 그대로 드러난다.
그래서 위젯을 고유값 비교에서 **가우스-뉴턴을 실제로 돌려 $\|\mathbf{q}\|$ 가 0 으로 무너지는 것을
보여 주는** 쪽으로 다시 만들었다 (잔차가 $\mathbf{q}$ 에 선형이라 무제약 최소해가 $\mathbf{q}=\mathbf{0}$ 이다).

### ④ 수식 축소 하한을 55% 로 낮췄다

식 (37)이 15×15 $\mathbf{F}$ 와 15×18 $\mathbf{G}$ 를 한 줄에 늘어놓은 거대한 행렬이라
62% 로도 좁은 창에서 넘쳤다. 900~1900px 전 구간에서 넘침 0 을 확인했다.

## 작업 흐름

**모든 명령은 스터디 루트에서 실행한다** (`_study_kit/` 안이 아니라 그 상위).

```bash
# ① 원문 정독 — 기호는 layout 모드로, 구조와 색은 쪽 이미지로
pdftotext -layout -f <시작> -l <끝> "ref/Formula ... .pdf" /tmp/ch.txt

# ② 색 위치를 먼저 뽑아 놓는다 — 이 문서는 색이 세 가지다
python3 _study_kit/tools/dump_colored.py -c prose
python3 _study_kit/tools/dump_colored.py -c math

# ③ 그림 추출 (캡션이 없으므로 bbox 방식)
python3 _study_kit/tools/extract_images_bbox.py --list
python3 _study_kit/tools/extract_images_bbox.py --out notes/images

# ④ 노트 작성 — notes/notes_on_vins_mono.md
#    파란 강조는 ==이렇게==, 수식 안은 \color{#ff0000}{...} / \color{#0000ff}{...}
#    ★ 목록 항목이 여러 줄이면 이어지는 줄을 반드시 들여쓴다 — 3_Pitfalls B9

# ⑤ 위젯 — _study_kit/tools/widgets/*.html (12개)
python3 _study_kit/tools/inject_helper.py

# ⑥ 빌드
python3 _study_kit/tools/build_html.py notes/notes_on_vins_mono.md

# ⑦ 검증
python3 _study_kit/tools/check_refs.py
#   식 번호 (1)~(88) 이 빠짐없이·중복 없이·순서대로 있는지
#   절 제목 18개를 PDF 목차·본문에서 문자열로 다시 찾아 확인
#   ==강조== 와 \color 개수를 dump_colored.py --count 와 대조
#   <mjx-container 개수 · data-mjx-error 0 (★ <script> 를 먼저 지우고 셀 것 — B6)
#   위젯 12개를 헤드리스로 열어 버튼·슬라이더까지 조작
#   .mathblock 의 scrollWidth > clientWidth 로 넘치는 수식이 없는지 (여러 창 폭에서)
```

### 이번 빌드의 검증 결과

| 항목 | 결과 |
|---|---|
| 수식 번호 | (1)~(88) — 누락 0, 중복 0, 순서 일치 |
| 절 | 18개 (8개 장 + 하위 10개) |
| 그림 | 10개 전부 인라인 |
| 렌더링된 수식 | `<mjx-container` **625개**, display 88개 · 실제 `data-mjx-error` **0** |
| 색 강조 | `.hl` **24곳** · `\color{#ff0000}` 4 · `\color{#0000ff}` 4 |
| 위젯 | 12개 · 버튼 전부 클릭 + 슬라이더 min/중간/max 스윕 후 `ERRS=0 BLANK=0 BAD=0` |
| 수식 넘침 | 창 900·1000·1200·1500·1900px 에서 모두 0건 |
| `check_refs.py` | 문제 0건 |

## 폴더 구조

```
5_Formula_Derivation_and_Analysis_of_the_VINS-Mono/   ← 스터디 루트
├── ref/Formula Derivation and Analysis of the VINS-Mono.pdf
├── _study_kit/
│   ├── kit.conf                    오프셋 0 · A4 · 캡션 1개뿐 · 색 세 가지
│   ├── README.md                   이 문서
│   ├── 0_Contents.md  1_Tools.md  2_Template_and_Rule.md  3_Pitfalls.md
│   └── tools/
│       ├── build_html.py           md → self-contained html
│       ├── dump_colored.py         색 강조 구간 추출 (색 목록을 세 개로 확장)
│       ├── inject_helper.py        위젯의 //%VM% 자리에 헬퍼를 채운다
│       ├── extract_images_bbox.py  ★ 이 문서에서 쓰는 쪽 (캡션 없음)
│       ├── extract_figures.py      캡션 기반 (쓰지 않는다)
│       ├── check_refs.py  kit_config.py
│       ├── vendor/tex-svg.js       MathJax + color + boldsymbol
│       └── widgets/
│           ├── _vm_helper.js       ★ window.VM 원본 (여기만 고친다)
│           └── *.html              Canvas 인터랙티브 위젯 12개
└── notes/
    ├── notes_on_vins_mono.md       ← 원본. 이것만 손으로 고친다
    ├── notes_on_vins_mono.html     ← 생성물(3.4MB)
    └── images/fig01…fig10_p<쪽>_<설명>.png
```

- 원문에 그림 번호가 거의 없으므로 파일명의 `figNN`은 **등장 순서**로 이 스터디가 붙인 번호다
  (p13 만 원문에 "Figure 1" 이 있고 노트도 그 캡션을 그대로 쓴다)

## 이 자료가 지키는 원칙

- **원문 재현이 최우선** — 문장·절 구성·수식 번호를 바꾸지 않는다. 고친 것은 노트 맨 아래
  "옮기며 바로잡은 것"에 전부 적는다
- **위젯은 본문 밖** — "원문에 없는 추가 요소"라고 표시된 회색 박스 안에만 둔다
- **한국어 노트, 영어 전문용어** — 언어 규칙은 `2_Template_and_Rule.md`
- **검증 가능한 위젯** — readout 에 원문 식의 값과 독립적인 수치실험 값을 나란히 찍는다
  (실험 2는 (7) 좌변과 우변, 실험 5는 (27)과 몬테카를로, 실험 10은 (62)~(65)와 수치미분,
  실험 12는 Schur 해와 전체 해)
- **화면의 숫자와 설명이 어긋나면 설명이 아니라 위젯을 고친다** — 실험 9가 그 사례다
