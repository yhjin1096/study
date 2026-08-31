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

이 스터디의 실제 값 (근거는 `kit.conf` 주석에 자세히 적어 두었다):

```
# PDF 페이지 = 책 쪽번호 + offset. 이 책은 구간마다 다르다 ← 아래 설명 참조
page_offset   = 28@29-209, 27@210-314, 26@315-477, 25@478-500, 24@501-673
last_chapter  = 24          # 학습 범위의 마지막 장 (부록은 별도)
book_pages    = 1-629       # 책 쪽번호의 유효 범위 (본문 끝 629, Index 631~)
caption_style = chapter     # "FIGURE 6.6" — 장 번호 + 일련번호
caption_bold  = yes         # 캡션 라벨이 TradeGothic-Bold 8.7pt
clip_x        = 82-461      # 판형 540x666pt. 홀짝쪽 여백이 뒤집혀 있어 합집합
header_y      = 45          # 머리글이 y=29 한 줄
body_x        = 120-423     # 본문 문단 판정 — 홀짝쪽의 교집합
brand         = PMPP 5e
booktitle     = Programming Massively Parallel Processors — 스터디 노트
```

### `page_offset` 이 구간마다 다른 경우

`page_offset` 은 **스칼라 하나**로도, **구간별 목록**으로도 쓸 수 있다.

```
page_offset = 28                          # 책 전체가 한 오프셋
page_offset = 28@29-209, 27@210-314       # PDF 쪽 구간마다 다른 오프셋
```

구간은 **PDF 쪽번호** 기준이다. 이 책처럼 장 사이의 빈 쪽이 PDF 에서 빠져 있으면
뒤로 갈수록 오프셋이 줄어드는데, 스칼라 하나로 적으면 책 뒷부분이 통째로 어긋난다.

환산은 손으로 하지 말고 도구에 맡긴다.

```bash
python3 -c "import sys; sys.path.insert(0,'_study_kit/tools'); import kit_config as k; \
            print(k.book_to_pdf(513), k.pdf_to_book(537))"
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

- **`--book-pages` 를 쓰라.** 책에 인쇄된 쪽번호로 지정하면 도구가 `page_offset`
  (구간별이어도) 을 적용해 PDF 쪽으로 환산하고, 환산 결과를 출력한다.
  `--pages` 는 PDF 쪽번호를 직접 주는 옛 방식이고, 둘 중 하나만 쓴다
- `--names`를 생략하면 `fig6_1.png`, `table6_2.png` 같은 기본 이름을 쓴다.
  챕터별 매핑 파일을 `tools/figure_names/`에 남겨 두면 언제든 같은 결과를 다시 만들 수 있다
- **캡션이 없는 그림**(연습문제 삽화 등)이나 **캡션이 그림 위에 있는 표**는
  자동 탐지로 잡히지 않는다. `--clip` 으로 직접 영역을 지정하고,
  좌표는 매핑 파일 하단에 주석으로 남겨 다시 만들 수 있게 해 둔다

```bash
# 이 책에서 유일하게 자동 추출이 안 되는 항목 (캡션이 표 위에 있다)
python3 _study_kit/tools/extract_figures.py \
    --clip 163,132,342,268 --page 498 --name table19_1 \
    --out part3_advanced/19_cnn/images
```

- **부록 그림**은 장 번호가 글자다. `--chapter A` 처럼 준다

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

노트에 쓰는 라벨 표기는 **`Figure 6.6` · `Table 19.1` 로 통일한다.** 이 책은 본문에
`FIGURE 6.6` 처럼 전부 대문자로 조판돼 있지만, 도구가 수집할 때 이 표기로 정규화하므로
노트도 같은 표기를 써야 대조가 된다. 부록은 `Figure A.3` 형식이다.

## 목차 점검

`0_Contents.md` 의 절 번호와 쪽번호가 원본과 맞는지 대조한다. 목차를 손으로 옮겨 적으면
반드시 오타가 나므로, 목차를 고칠 때마다 돌린다.

```bash
python3 _study_kit/tools/check_toc.py             # 불일치만 출력
python3 _study_kit/tools/check_toc.py --verbose   # 맞은 항목까지 전부
```

각 항목의 책 쪽번호를 (구간별 오프셋을 적용해) PDF 쪽으로 환산한 뒤, 그 쪽이나 다음 쪽에
그 절 제목이 **제목으로 조판돼 있는지** 확인한다. 머리글에 같은 제목이 반복되므로
글자 크기와 세로 위치로 걸러 낸다. 다른 책에 쓸 때는 스크립트 맨 위의
`HEADING_MIN_SIZE` · `HEADING_MIN_Y` 를 다시 재야 한다.

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
