# 학습 자료 제작 도구 스택

| 구분 | 도구 | 역할 |
|---|---|---|
| 콘텐츠 포맷 | Markdown → HTML | 원본은 Markdown(.md)으로 작성/관리, 최종 결과물은 HTML 파일로 렌더링 |
| 빌드 | `tools/build_html.py` (순수 Python, 무의존성) | md → html 변환, 수식 통과, 이미지 base64 인라인, 위젯 삽입, 목차 생성 |
| 수식 | MathJax `tex-svg` (`tools/vendor/tex-svg.js`) | LaTeX 문법으로 작성. SVG 출력이라 **외부 폰트 파일이 필요 없어** 단일 HTML에 인라인 가능 |
| 이미지 | `tools/extract_figures.py` (PyMuPDF + PIL) | 원본 PDF에서 챕터의 Figure/Table을 찾아 크롭 → 챕터 `images/`에 저장 후 base64로 인라인 |
| 점검 | `tools/check_refs.py` | 노트의 그림·표·쪽번호·절 참조를 원문과 대조 |
| 인터랙티브 시각화 | Canvas + 순수 JavaScript (`tools/widgets/*.html`) | 슬라이더로 파라미터를 바꾸며 알고리즘을 눈으로 확인 |
| 결과물 | **로컬 self-contained HTML 파일** | 챕터 폴더에 `.html` 1개. 수식 엔진·이미지·위젯 전부 인라인되어 오프라인으로 열림 |

## 파이프라인

```
원본 PDF (ref/)
        │
        ├── python3 _study_kit/tools/extract_figures.py --chapter N --pages A-B --out <챕터>/images
        ▼
챕터 .md (원본, 손으로 작성)
   +  images/*.png (PDF에서 추출)
   +  tools/widgets/*.html (Canvas 위젯)
   +  tools/vendor/tex-svg.js (MathJax)
        │
        ├── python3 _study_kit/tools/build_html.py <챕터>.md
        ▼
챕터 .html (단일 파일, 브라우저로 바로 열기)
        │
        └── python3 _study_kit/tools/check_refs.py   +  헤드리스 렌더링 확인
```

## 사전 준비 (한 번만)

```bash
sudo apt install -y python3-fitz     # PyMuPDF — 그림 추출에 필요
sudo apt install -y python3-numpy    # 노트 본문의 검증용 코드 스니펫 실행에 필요 (선택)
```

`build_html.py`는 순수 Python이라 추가 설치가 필요 없다. PIL(Pillow)은 대개 이미 있다.
이 환경에는 `pip`이 없으므로 파이썬 패키지는 apt로 설치한다.

> **numpy는 노트를 읽고 빌드하는 데는 필요 없다.** 본문의 검증용 스니펫을 직접 돌려볼 때만 쓴다.
> 스니펫을 넣을 때 첫 줄에 설치 안내를 주석으로 적어 두면 좋다.

## 두 개의 루트 — 명령은 어디서 실행하는가

```
My_Book/            ← 스터디 루트. ref/ 와 노트가 있고, 명령을 여기서 실행한다
├── ref/
├── _study_kit/     ← 킷 루트. kit.conf · 0~3 문서 · tools/ 가 있다
└── part1_xxx/
```

도구는 자기 위치(`tools/`의 부모)를 킷 루트로 잡고, 거기나 그 한 단계 위에서
`ref/`·`part*/`를 찾아 스터디 루트를 정한다. 그래서 **킷을 하위 폴더에 담아 두든
스터디 루트에 펼쳐 두든 똑같이 동작한다.** 판정 규칙은 `tools/kit_config.py` 맨 위 설명.

이 문서의 명령은 모두 **스터디 루트 기준**이다.

## 설정 — `kit.conf`

킷 루트의 `kit.conf`를 `extract_figures.py`·`check_refs.py`·`build_html.py`가 함께 읽는다.
킷을 복사하면 `kit.conf`가 함께 딸려 오니 **값만 채우면 된다.**

```
page_offset   = 21          # PDF 페이지 = 책 쪽번호 + 이 값  ← 반드시 검증할 것
last_chapter  = 8           # 학습 범위의 마지막 장
book_pages    = 1-647       # 책 쪽번호의 유효 범위
caption_style = chapter     # 캡션 번호 형식: chapter("Figure 6.3") | flat("Figure 3")
caption_bold  = yes         # 캡션 라벨이 볼드체인가 (LaTeX article 은 보통 no)
clip_x        = 155-522     # 그림 추출 레이아웃 (책 판형마다 다름)
header_y      = 52
body_x        = 186-488
brand         = My Book     # 사이드바 머리말
booktitle     = Author — 스터디 노트
```

> **`caption_style`·`caption_bold` 를 먼저 맞춰라.** 이 둘이 틀리면 `--list` 가 아무것도 못 찾는다.
> 조사법은 `3_Pitfalls.md` A8.

설정을 확인하려면:

```bash
python3 _study_kit/tools/kit_config.py      # 현재 인식된 설정을 JSON으로 출력
```

## 그림·표 추출

```bash
# 1) 그 챕터에 어떤 그림/표가 있는지 먼저 훑어본다
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 --list

# 2) 이름 매핑 파일을 만든 뒤 (tools/figure_names/chN.txt) 추출한다
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 \
    --out part1_xxx/06_chapter/images --names _study_kit/tools/figure_names/ch6.txt

# 하나만 다시 뽑기
python3 _study_kit/tools/extract_figures.py --chapter 6 --pages 170-207 \
    --out part1_xxx/06_chapter/images --only "Figure 6.9"
```

- **`--pages`는 PDF 페이지 번호다.** 책 쪽번호가 아니다 (`kit.conf`의 `page_offset` 참조)
- `--names`를 생략하면 `fig6_1.png`, `table6_2.png` 같은 기본 이름을 쓴다.
  챕터별 매핑 파일을 `tools/figure_names/`에 남겨 두면 언제든 같은 결과를 다시 만들 수 있다
- **캡션이 없는 그림**(연습문제 삽화 등)은 이 스크립트로 잡히지 않는다.
  `fitz`로 clip을 직접 지정해 뽑고, 그 좌표를 매핑 파일 하단에 주석으로 적어 둔다

> **왜 PyMuPDF인가** — 일부 페이지가 통짜 스캔 이미지인 PDF가 흔한데, 그러면 페이지 안 객체 bbox를
> 그림 영역으로 신뢰할 수 없다. 그래서 이 스크립트는 **캡션 위치로 영역을 좁힌 뒤 픽셀 단위로
> 흰 여백을 트림**하는 방식을 쓴다. 스캔이든 벡터든 똑같이 동작한다.
> 캡션과 본문 언급은 **폰트로 구분**한다(캡션 라벨은 볼드). 자세한 함정은 `3_Pitfalls.md` A장.

## 빌드

```bash
# 챕터 하나 빌드 (같은 폴더에 .html 생성)
python3 _study_kit/tools/build_html.py part1_xxx/02_chapter/02_chapter.md

# 여러 개 한 번에
python3 _study_kit/tools/build_html.py part1_xxx/*/*.md part2_xxx/*/*.md
```

- `.md`를 수정하면 위 명령을 다시 실행해 `.html`을 갱신한다.
  **`.html`은 생성물이므로 직접 편집하지 않는다.**
- 본문에 `<!--widget:NAME-->` 한 줄을 넣으면 `tools/widgets/NAME.html`이 그 자리에 삽입된다
- 결과 HTML은 외부 네트워크 없이 동작한다 (MathJax·이미지·위젯 모두 파일 안에 포함)

## 상호참조 점검

노트가 인용한 그림·표·쪽번호·절 번호가 실제 원문과 맞는지 대조한다.

```bash
python3 _study_kit/tools/check_refs.py            # 전체
python3 _study_kit/tools/check_refs.py 06 07      # 특정 노트만
```

- **[없는 그림/표]** — PDF에 그 캡션이 없다. 번호를 잘못 적었거나 **저자가 번호를 건너뛴** 경우다.
  후자라면 PDF 전문 검색으로 확정한 뒤 `kit.conf` 메모에 남긴다
- **[목차에 없는 절]** — `0_Contents.md`에 없는 절 번호. 오타이거나 존재하지 않는 절이다
- **· [학습 범위 밖 참조]** — `last_chapter` 이후 장 참조. 문제가 아니라 정보다

## 빌드 결과 확인

브라우저로 직접 열어 보는 것이 기본이지만, 헤드리스로 렌더링 오류를 빠르게 확인할 수도 있다.

```bash
google-chrome --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=8000 --window-size=1280,4000 \
    --screenshot=/tmp/shot.png \
    "file://$PWD/part1_xxx/06_chapter/06_chapter.html"
```

> 스크린샷 경로를 `/dev/null`로 주면 "Unsupported screenshot image file type" 오류가 뜬다.
> 페이지 문제가 아니니 실제 파일 경로를 주라.

### 위젯 점검 — 조작까지 해 봐야 한다

초기 렌더링만 보면 부족하다. **버튼을 전부 누르고 슬라이더를 극단값으로 흔든 뒤**
JS 오류·빈 캔버스·NaN을 확인한다.

```python
# 빌드된 HTML에서 <style>을 꺼내 위젯과 합친 테스트 페이지를 만들고,
# 아래 스크립트를 붙여 --dump-dom 으로 <title>을 읽는다.
"""
window.__errs=[];
window.addEventListener('error', e => window.__errs.push(e.message));
setTimeout(() => {
  document.querySelectorAll('button').forEach(b => { try { b.click(); } catch(e){} });
  document.querySelectorAll('input[type=range]').forEach(s => {
    [s.min, (+s.min + +s.max)/2, s.max].forEach(v => {
      s.value = v; s.dispatchEvent(new Event('input', {bubbles:true}));
    });
  });
  setTimeout(() => {
    let blank = 0;
    document.querySelectorAll('canvas').forEach(c => {
      const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
      let nz = 0; for (let i=3; i<d.length; i+=400) if (d[i]) nz++;
      if (nz < 3) blank++;
    });
    const bad = (document.body.innerText.match(/NaN|Infinity/g) || []).length;
    document.title = `ERRS=${window.__errs.length} BLANK=${blank} NaN=${bad}`;
  }, 700);
}, 900);
"""
```

```bash
google-chrome --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=6000 --dump-dom "file://$PWD/wtest.html" \
    | grep -o '<title>[^<]*</title>'
```
