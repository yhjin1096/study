# Notes on Multiple View Geometry in Computer Vision 스터디

Gyubeom Edward Im의 강의 노트 *Notes on Multiple View Geometry in Computer Vision*
(Hartley & Zisserman 원서 기반, 104쪽)를 **내용 수정 없이 그대로** HTML로 옮기고,
이해를 돕는 **인터랙티브 위젯 18개**를 절 사이에 끼워 넣은 자료다.
사영공간 $\mathbb{P}^n$ → 2D 사영기하 → 카메라 모델 → 단일 시점 → epipolar geometry →
3D 복원 → scene plane → affine epipolar → trifocal tensor 까지 원문 15개 장 195개 절 전체를 다룬다.

원본 PDF: `ref/Notes on Multiple View Geometry in Computer Vision.pdf`
결과물: `notes/notes_on_mvg.html` (단일 파일 9.4MB, 오프라인으로 열림)

```bash
# 다시 빌드할 때
python3 _study_kit/tools/inject_helper.py             # 위젯에 window.MV 주입
python3 _study_kit/tools/build_html.py notes/notes_on_mvg.md
python3 _study_kit/tools/check_refs.py
```

## 이 스터디의 규모

**열 개 스터디 중 가장 크다.** 직전 최대였던 6번(45쪽·식 204개)의 2.3배다.

| | 이 스터디 | 6번 (직전 최대) | 7번 (ICP) |
|---|---|---|---|
| 쪽 | 104 | 45 | 24 |
| 식 | (1)~(456) | (1)~(204) | (1)~(101) |
| 절 | 15장 + 195절 | 10장 + 42절 | 8장 + 12절 |
| 그림 | 63 | 9 | 9 |
| 위젯 | 18 | 12 | 12 |
| HTML | 9.4MB | 4.2MB | 3.8MB |

규모가 커서 전사를 **7회분으로 쪼개** 진행했고 (킷 작업 목록 #80~#86),
매 회 끝에 식 번호 연속성 · 그림 위치 · PDF 문장 대조를 돌렸다.

## 이 스터디에서 원래 킷과 달라진 점

### ① 색이 한 가지뿐이다 — 대신 구간이 191개로 가장 많다

원문이 쓰는 색은 `#197fb2` 파랑 하나다. 수식 안에는 색이 없다.
그래서 7번 스터디가 도입한 `{{c|…}}` `{{r|…}}` `{{t|…}}` 마커는 쓸 일이 없고
`==강조==` 하나로 끝난다. 다만 **구간 수가 191개(13,413자, 42쪽)로 지금까지 최다**라
손으로 옮기면 반드시 샌다.

그래서 **`dump_colored.py` 출력과 노트를 기계적으로 대조하는 검사기**를 만들어 썼다.
PDF 색 구간의 텍스트를 「한글·영문·숫자만 남긴 문자열」로 정규화하고,
노트도 같은 방식으로 정규화하되 **각 글자가 `==` 안인지 밖인지 표시**해 두면,
색 구간이 실제로 강조 안에 들어 있는지 구간마다 % 로 나온다.

정규화할 때 두 군데를 조심해야 한다 (이걸 놓쳐서 두 번 헛짚었다):

- `\begin{pmatrix}` 의 **`pmatrix` 가 낱말로 섞여 들어간다** → `\(begin|end)\{…\}` 를 통째로 지운다
- `\det` 는 지워지는데 PDF 에는 `det` 가 남는다 → 이런 항목은 눈으로 확인

이 검사기로 **191구간 중 149구간이 빠져 있던 것**을 찾아냈고,
154구간을 자동 반영 + 8구간을 손으로 넣고 나머지(중복 매치·짧은 구간)를 개별 처리해
최종적으로 190구간(페이지 경계에서 쪼개진 한 쌍을 합쳐서)을 재현했다.

### ② 그림 63개 — 캡션이 없어 제목에서 이름을 붙였다

전문에 Figure/Fig./Table 이 0회다. `extract_figures.py`(캡션 기반)를 쓸 수 없어
`extract_images_bbox.py` 를 쓰되, **바로 앞 제목으로 파일 이름을 자동 생성**하도록
`NAMES` 맵(63항목)을 미리 만들어 두었다.

```
fig01_p007_projective_space.png
fig41_p054_epipolar_geometry.png
fig60_p093_the_trifocal_tensor.png
```

### ③ `window.MV` — 다섯 세대째 헬퍼

`LG`(Lie) → `PI`(preintegration) → `VM`(VINS) → `EJ`(errors/jacobians) → `IC`(ICP) → **`MV`**.
`MV` 는 `IC` 를 그대로 물려받고 사영기하 전용 함수를 얹는다 (~78KB).

```
hnorm h2e e2h join meet onLine ptLineDist          동차좌표·점·직선
nullvec nullvecLeft rq3 rq2 qr2                    분해
conicFrom5 conicTangent conicFromLines adjugate3   Conic
normalizePts dltH decomposeH
  affineRectifyH metricRectifyH                    Homography·정류
Kmat camP camM camP4 camCenter decomposeP
  principalPlane principalPoint principalAxis
  pinvP backProjectRay depthOf dltP                카메라 행렬
omegaFromK rayAngle vanishingPoint
  omegaFromVPs KfromOmega                          IAC·소실점
fFromP enforceRank2 eightPoint epipoles
  sampsonError eFromF decomposeE chooseByCheirality  F·E
triangulateDLT reprojError                         구조 복원
hFromPlane hFromRtn hInf compatCheck               평면 유도 H
trifocalFromP trifocalLine trifocalSum
  trifocalPointTransfer trifocalLineTransfer       Trifocal
```

44개 항등식을 원문 식 번호와 1:1로 대응시켜 검산했고 전부 기계정밀도로 통과했다
(목록은 노트 부록 「수치로 확인한 것」).

**`decomposeH` 는 QR 이지 RQ 가 아니다.** 식 (39) 의 $\mathbf{A} = s\mathbf{R}\mathbf{K} + \mathbf{t}\mathbf{v}^\intercal$ 는
회전이 왼쪽·상삼각이 오른쪽이므로 QR 이다. 카메라 분해(식 96) 의 $\mathbf{M} = \mathbf{K}\mathbf{R}$ 이
RQ 인 것과 순서가 반대다. 처음에 `rq2` 를 쓰다 $2.7\times10^{-2}$ 어긋나서 `qr2` 를 새로 넣었다.

### ④ 공용 빌더에서 세 가지를 고쳤다 (아홉 킷 전부에 반영)

이 스터디를 검증하다 **다른 스터디에도 있던 버그 셋**을 찾아 공용 `build_html.py` 에 고쳤고,
아홉 킷에 동기화한 뒤 노트 10개를 전부 다시 빌드했다.

| # | 증상 | 원인 | 고침 |
|---|---|---|---|
| 1 | 좁은 창에서 본문이 옆으로 밀림 | **인라인 수식**에는 `.mathblock` 같은 스크롤 상자가 없어 줄바꿈 불가능한 긴 식이 그대로 폭을 밀어냄 | 인라인 `mjx-container` 도 폭에 맞춰 축소. 부모가 `<span class="hl">` 이면 `clientWidth` 가 0 이므로 **블록 조상까지 올라가서** 잰다 |
| 2 | 위를 고쳐도 일부 문서가 여전히 밀림 | `mjx-assistive-mml` 이 `position:absolute; width:auto` 라 `.mathblock` 의 `overflow:auto` 클리핑을 **빠져나간다** | 레이아웃 폭만 `1px` 로 묶음 (화면에는 이미 `clip` 으로 감춰져 있다) |
| 3 | 참고문헌 줄이 원시 마크다운으로 출력 | 링크 정규식 `\[([^\]]+)\]` 이 `[(Blog) [SLAM] 제목](url)` 처럼 **텍스트 안에 대괄호가 든 링크**에서 실패 | 한 겹 중첩까지 허용하도록 수정 |

3번은 2번 스터디(Kalman Filter) 참고문헌 4번 항목이 링크가 아니라 URL 통짜로 나오고 있던 것으로,
검증 과정에서 딸려 나왔다.

고친 뒤 열 개 노트 전부에서 **창 폭 1440/900/480/360px 모두 가로 넘침 0**을 확인했다.

## 실험 18개

전부 **원문에 없는 추가 요소**이며 각 위젯 머리에 그렇게 적어 두었다.
계산은 예외 없이 `window.MV` 가 하고, 화면의 숫자는 실행 결과를 그대로 찍는다.

| # | 이름 | 장 | 무엇을 보이나 |
|---|---|---|---|
| 1 | `projective-space` | 1 | $\mathbb{P}^n$ = 원점을 지나는 직선들의 집합. $k$ 를 바꿔도 같은 점 |
| 2 | `points-lines-duality` | 2.1 | $\mathbf{l} = \mathbf{x}\times\mathbf{x}'$ 와 $\mathbf{x} = \mathbf{l}\times\mathbf{l}'$ 가 같은 식임 |
| 3 | `conics-dual` | 2.3 | 5점이 Conic 을 유일하게 결정 · 접선과 쌍대 Conic |
| 4 | `transformation-hierarchy` | 2.5~2.6 | 등거리→닮음→아핀→사영에서 무엇이 보존되나 · 식 (39) 분해 (QR) |
| 5 | `metric-rectification` | 2.7 | 소실선으로 아핀 정류 → 직교 쌍으로 계량 정류 |
| 6 | `pinhole-camera-matrix` | 3.1 | $\mathbf{P} = \mathbf{K}\mathbf{R}[\mathbf{I}\mid-\tilde{\mathbf{C}}]$ 를 성분별로 |
| 7 | `camera-anatomy` | 3.2 | 중심·주평면·주점·주축·열벡터가 어디를 가리키나 |
| 8 | `affine-camera-vertigo` | 3.4 | Vertigo 효과와 discrepancy 식 (129)~(139) |
| 9 | `dlt-camera-matrix` | 4.2 | DLT 와 **동일평면 퇴화**. 정규화는 여기서는 거의 차이가 없다 |
| 10 | `image-absolute-conic` | 5.1 | $\omega = \mathbf{K}^{-\intercal}\mathbf{K}^{-1}$ 와 각도 측정 |
| 11 | `vanishing-points` | 5.3 | 소실점으로 회전·초점거리·주점 복원 |
| 12 | `fundamental-matrix` | 6.2 | $\mathbf{x}'^\intercal\mathbf{F}\mathbf{x}=0$ · epipolar line 다발 · rank 2 |
| 13 | `essential-matrix` | 6.7 | $\mathbf{E}$ 의 특이값 $(\sigma,\sigma,0)$ · 네 해와 cheirality |
| 14 | `stratified-reconstruction` | 7.2 | 사영 → 아핀 → 계량 단계별 복원 |
| 15 | `eight-point-algorithm` | 8.2 | **정규화 유무로 오차가 $33$배~$10^{14}$배** 벌어짐 |
| 16 | `triangulation` | 9.2 | DLT triangulation 과 사영모호성 |
| 17 | `plane-homography` | 10.1 | 평면이 유도하는 $\mathbf{H}$ 와 $\mathbf{F}$ 의 호환 조건 |
| 18 | `trifocal-tensor` | 12.3 | $\mathcal{T}$ 의 직선 전이 · **trifocal 평면에서 $\mathbf{F}$ 전이가 무너지는 것** |

**9번은 한 번 갈아엎었다.** 처음에는 "카메라 DLT 에서도 Hartley 정규화가 중요하다"를
보이려 했는데, 탐침을 돌려 보니 **어떤 스케일에서도 조건수 비가 1.0 근처**였다.
월드 스케일은 $\mathbf{P}$ 가 흡수하고 이미지 좌표만 키워도 마찬가지였다.
전제가 숫자와 어긋났으므로 주제를 **동일평면 퇴화**로 바꾸고,
정규화 이야기는 실제로 극적인 차이가 나는 15번(8-point)으로 옮겼다.
(→ `3_Pitfalls` C6·C8 계열: 위젯의 주장은 위젯 자신의 숫자로 먼저 확인한다)

## 원문에 대해

**수치로 어긋나는 식을 찾지 못했다.** 앞선 스터디들과 다른 점이다.
철자·오탈자는 여러 곳 있지만 전부 **그대로 두고** 노트 부록에 목록으로 적었다
(`vanisinh`, `윌드`, `likelihook`, `Fundemental`, `Conjuate`, `Degenrate`,
`optimial`, `Levenerg`, `employing and affine camera`, `품으로써`, `Epipoar`).

손을 댄 곳은 딱 하나 — 식 (107) 위의 `det(M)m₃,row`**`e`** 에서 끝에 붙은 글자 `e` 하나다.

## 파일

```
_study_kit/
  README.md            ← 이 파일
  0_Contents.md        학습 범위 목차 (장·절·식·그림·위젯 위치)
  1_Tools.md           도구 사용법
  2_Template_and_Rule.md  전사·위젯 작성 규칙 (아홉 킷 공통)
  3_Pitfalls.md        지금까지 밟은 함정 (아홉 킷 공통, 동기화)
  kit.conf             이 스터디 설정 (PDF 경로·오프셋·색·bbox)
  tools/
    build_html.py            md → 단일 파일 HTML
    extract_images_bbox.py   그림 추출 (캡션 없는 문서용) — NAMES 63항목
    extract_figures.py       그림 추출 (캡션 기반) — 이 문서에서는 미사용
    dump_colored.py          원문 색 구간 덤프 (전사 대조용)
    inject_helper.py         위젯에 window.MV 주입
    check_refs.py            식 번호·목차 절 대조
    kit_config.py            kit.conf 읽기
    widgets/
      _mv_helper.js          window.MV (~78KB)
      *.html                 실험 1~18
    vendor/tex-svg.js        MathJax (color·boldsymbol 포함, 오프라인)
notes/
  notes_on_mvg.md      전사 원본
  notes_on_mvg.html    결과물 (9.4MB, 단일 파일)
  images/              63개 PNG
ref/
  Notes on Multiple View Geometry in Computer Vision.pdf
```
