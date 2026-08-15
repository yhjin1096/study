# 학습 자료 제작 도구 스택

| 구분 | 도구 | 역할 |
|---|---|---|
| 콘텐츠 포맷 | Markdown → HTML | 원본은 Markdown(.md)으로 작성/관리, 최종 결과물은 HTML 파일로 렌더링 |
| 빌드 | `_study_kit/tools/build_html.py` (순수 Python, 무의존성) | md → html 변환, 수식 통과, 이미지 base64 인라인, 위젯 삽입, 목차 생성 |
| 수식 | MathJax `tex-svg` (`_study_kit/tools/vendor/tex-svg.js`) | LaTeX 문법으로 작성. SVG 출력이라 **외부 폰트 파일이 필요 없어** 단일 HTML에 인라인 가능 |
| 이미지 | `_study_kit/tools/extract_figures.py` (PyMuPDF + PIL) | 원본 PDF에서 챕터의 Figure/Table을 찾아 크롭 → 챕터 `images/`에 저장 후 base64로 인라인 |
| 인터랙티브 시각화 (메인) | Canvas + 순수 JavaScript (`_study_kit/tools/widgets/*.html`) | 공분산 타원, 시그마 포인트, 파티클 클라우드, "로봇+센서+필터" 스텝별 애니메이션/시뮬레이션 |
| 인터랙티브 시각화 (보조) | Plotly.js | 3D 가우시안 표면, likelihood surface 등. 필요해지면 vendor에 인라인해서 사용 |
| 결과물 | **로컬 self-contained HTML 파일** | 챕터 폴더에 `.html` 1개. 수식 엔진·이미지·위젯 전부 인라인되어 오프라인·오프-네트워크로 열림 |

## 파이프라인

```
원본 PDF (ref/)
        │
        ├── python3 _study_kit/tools/extract_figures.py --chapter N --pages A-B --out <챕터>/images
        ▼
챕터 .md (원본, 손으로 작성)
   +  images/*.png (PDF에서 추출)
   +  _study_kit/tools/widgets/*.html (Canvas 위젯)
   +  _study_kit/tools/vendor/tex-svg.js (MathJax)
        │
        ├── python3 _study_kit/tools/build_html.py <챕터>.md
        ▼
챕터 .html (단일 파일, 브라우저로 바로 열기)
```

## 사전 준비 (한 번만)

```bash
sudo apt install -y python3-fitz     # PyMuPDF — 그림 추출에 필요
sudo apt install -y python3-numpy    # 노트 본문의 검증용 코드 스니펫 실행에 필요
```

`build_html.py`는 순수 Python이라 추가 설치가 필요 없다. PIL(Pillow)은 시스템에 이미 있다.
이 환경에는 `pip`이 없으므로 파이썬 패키지는 apt로 설치한다.

> **numpy는 노트를 읽고 빌드하는 데는 필요 없다.** 6·7장 본문에 있는 검증용 코드 스니펫 3개
> (beam model 밀도, EKF localization 한 스텝)를 직접 돌려볼 때만 쓴다. 각 스니펫 첫 줄에도
> 같은 안내를 적어 두었다.

## 두 개의 루트 — 명령은 어디서 실행하는가

```
Probabilistic_Robotics/   ← 스터디 루트. ref/ 와 노트가 있고, 명령을 여기서 실행한다
├── ref/
├── _study_kit/           ← 킷 루트. kit.conf · 0~3 문서 · tools/ 가 있다
├── part1_basics/
└── part2_localization/
```

도구는 자기 위치(`tools/`의 부모)를 킷 루트로 잡고, 거기나 그 한 단계 위에서
`ref/`·`part*/`를 찾아 스터디 루트를 정한다. 그래서 킷을 하위 폴더에 담아 두든
스터디 루트에 펼쳐 두든 똑같이 동작한다. 판정 규칙은 `_study_kit/tools/kit_config.py` 맨 위 설명.

아래 명령은 모두 **스터디 루트 기준**이다.

## 설정 — `kit.conf`

PDF 경로·페이지 오프셋·학습 범위·그림 추출 레이아웃·사이드바 머리말이 킷 루트의
`kit.conf` 한 곳에 모여 있고, `build_html.py`·`extract_figures.py`·`check_refs.py`가 함께 읽는다.

```
page_offset  = 21          # PDF 페이지 = 책 쪽번호 + 21 (검증됨)
last_chapter = 8           # 학습 범위
book_pages   = 1-647       # 책 쪽번호 유효 범위 (PDF 총 668쪽)
clip_x       = 155-522     # 그림 추출 레이아웃 (판형 576×648pt)
brand        = Probabilistic Robotics
booktitle    = Thrun · Burgard · Fox — 스터디 노트
```

```bash
python3 _study_kit/tools/kit_config.py      # 현재 인식된 설정을 JSON으로 출력
```

> 이 저장소의 `_study_kit/tools/`는 `../_study_kit/tools/`와 **동일한 코드**다. 도구를 고쳤다면 양쪽에
> 반영해 갈라지지 않게 한다.

## 그림·표 추출

```bash
# 1) 그 챕터에 어떤 그림/표가 있는지 먼저 훑어본다
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 --list

# 2) 이름 매핑 파일을 만든 뒤 (_study_kit/tools/figure_names/chN.txt) 추출한다
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 \
    --out part1_basics/06_robot_perception/images \
    --names _study_kit/tools/figure_names/ch6.txt

# 하나만 다시 뽑기
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 \
    --out part1_basics/06_robot_perception/images --only "Figure 6.9"
```

- **`--pages`는 PDF 페이지 번호다.** 책 페이지 + 21 (`2_Template_and_Rule.md`의 페이지 오프셋 참조).
  챕터 시작: 4장 106 · 5장 138 · 6장 170 · 7장 212 · 8장 258 · 9장 302.
- `--names`를 생략하면 `fig6_1.png`, `table6_2.png` 같은 기본 이름을 쓴다. 챕터별 매핑 파일은
  `_study_kit/tools/figure_names/`에 남겨 두어 언제든 같은 결과를 다시 만들 수 있게 한다.
- **캡션이 없는 그림**(연습문제 삽화 등)은 이 스크립트로 잡히지 않는다. `fitz`로 clip을 직접 지정해
  뽑고, 그 좌표를 매핑 파일 하단에 주석으로 적어 둔다 (ch6.txt 예시 참조).

> **왜 PyMuPDF인가**: 이 책 PDF는 일부 페이지가 통짜 스캔 이미지라서 페이지 안 객체 bbox를
> 그림 영역으로 신뢰할 수 없다. 그래서 스크립트는 **캡션 위치로 영역을 좁힌 뒤 픽셀 단위로 흰 여백을
> 트림**하는 방식을 쓴다. 캡션 라벨은 볼드체(Palatino-Bold 9pt)라서, 본문 중 언급
> ("Figure 6.2 shows a typical…", Palatino-Roman 10pt)과 폰트로 구분한다.

## 빌드

```bash
# 챕터 하나 빌드 (같은 폴더에 .html 생성)
python3 _study_kit/tools/build_html.py part1_basics/02_recursive_state_estimation/02_recursive_state_estimation.md

# 여러 개 한 번에
python3 _study_kit/tools/build_html.py part1_basics/*/*.md part2_localization/*/*.md
```

- `.md`를 수정하면 위 명령을 다시 실행해 `.html`을 갱신한다. **`.html`은 생성물이므로 직접 편집하지 않는다.**
- 본문에 `<!--widget:NAME-->` 한 줄을 넣으면 `_study_kit/tools/widgets/NAME.html`이 그 자리에 삽입된다.
- 결과 HTML은 외부 네트워크 없이 동작한다 (MathJax·이미지·위젯 모두 파일 안에 포함).

## 상호참조 점검

노트가 인용한 그림·표·페이지·절 번호가 실제 원문과 맞는지 대조한다.

```bash
python3 _study_kit/tools/check_refs.py            # 전체
python3 _study_kit/tools/check_refs.py 06 07      # 특정 노트만
```

- **[없는 그림/표]** — PDF에 그 캡션이 없다. 번호를 잘못 적었거나, 아래 "번호 건너뜀"에 해당한다
- **[목차에 없는 절]** — `0_Contents.md`에 없는 절 번호. 오타이거나 존재하지 않는 절이다
- **· [학습 범위 밖 참조]** — 9장 이후 절 참조. 문제가 아니라 정보다

> **이 책에는 번호 건너뜀이 있다** — **Figure 3.1과 Figure 8.15는 존재하지 않는다.** PDF 전문 검색으로
> 확인한 사실이며, 노트가 이를 참조하지 않는 한 정상이다.
>
> 캡션 라벨은 PyMuPDF가 여러 조각으로 쪼개는 경우가 있어(책 Table 3.2는 `'Table'`과 `'3.2'`가 별도
> line) 같은 높이의 볼드 조각을 이어붙여 복원한다. `extract_figures.py`도 같은 로직을 쓴다.

## 빌드 결과 확인

브라우저로 직접 열어 보는 것이 기본이지만, 헤드리스로 렌더링 오류만 빠르게 확인할 수도 있다.

```bash
google-chrome --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=8000 --window-size=1280,4000 \
    --screenshot=/tmp/shot.png \
    "file://$PWD/part1_basics/06_robot_perception/06_robot_perception.html"
```

위젯만 따로 점검하려면 빌드된 HTML에서 `<style>` 블록을 꺼내 위젯 파일과 합친 테스트 페이지를
만들어 같은 방식으로 캡처한다 (JS 오류가 있으면 canvas가 비어 있게 나온다).
