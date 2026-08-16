# 학습 자료 제작 도구 스택

| 구분 | 도구 | 역할 |
|---|---|---|
| 콘텐츠 포맷 | Markdown → HTML | 원본은 Markdown(.md)으로 작성/관리, 최종 결과물은 HTML 파일로 렌더링 |
| 빌드 | `tools/build_html.py` (순수 Python, 무의존성) | md → html 변환, 수식 통과, 이미지 base64 인라인, 위젯 삽입, 목차 생성 |
| 수식 | MathJax `tex-svg` (`tools/vendor/tex-svg.js`) | LaTeX 문법으로 작성. SVG 출력이라 **외부 폰트 파일이 필요 없어** 단일 HTML에 인라인 가능 |
| 이미지 | `tools/extract_images_bbox.py` (PyMuPDF) | **캡션이 없는 문서**용. 페이지의 이미지 객체 bbox 를 그대로 크롭하고, 바로 앞 제목에서 이름을 붙인다 (63개) |
| 점검 | `tools/check_refs.py` | 노트의 그림·표·쪽번호·절 참조를 원문과 대조 |
| 인터랙티브 시각화 | Canvas + 순수 JavaScript (`tools/widgets/*.html`) | 슬라이더로 파라미터를 바꾸며 알고리즘을 눈으로 확인 |
| 결과물 | **로컬 self-contained HTML 파일** | 챕터 폴더에 `.html` 1개. 수식 엔진·이미지·위젯 전부 인라인되어 오프라인으로 열림 |

## 파이프라인

```
원본 PDF (ref/)
        │
        ├── python3 _study_kit/tools/dump_colored.py          ← 원문의 색 강조 위치를 먼저 뽑는다
        ├── python3 _study_kit/tools/extract_images_bbox.py   ← 그림 63개 (캡션 없음)
        ▼
노트 .md (원본, 손으로 작성)
   +  tools/widgets/*.html (Canvas 위젯 18개)
   +  images/*.png (PDF 에서 뽑은 그림 63개)
   +  tools/widgets/_mv_helper.js → inject_helper.py 로 위젯에 주입
   +  tools/vendor/tex-svg.js (MathJax + color + boldsymbol)
        │
        ├── python3 _study_kit/tools/inject_helper.py
        ├── python3 _study_kit/tools/build_html.py notes/notes_on_mvg.md
        ▼
노트 .html (단일 파일, 브라우저로 바로 열기)
        │
        └── python3 _study_kit/tools/check_refs.py   +  헤드리스 렌더링·위젯 확인
```

> **이 스터디는 그림 63개에 캡션이 하나도 없다** — 전문에서 `Figure`/`Fig.`/`Table` 이 0회다.
> 그래서 `extract_images_bbox.py` 만 쓴다. `extract_figures.py`(캡션 기반)는 쓸 수 없다.
> 63개나 되어 이름을 손으로 짓는 대신 **바로 앞 제목에서 자동 생성**하도록
> `extract_images_bbox.py` 안의 `NAMES` 맵(63항목)을 미리 만들어 두었다.
> 자세한 것은 `kit.conf` 의 캡션 항목과 `README.md` ② 를 볼 것.

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

## 색 강조 추출 — `dump_colored.py`

이 문서는 색을 **한 가지**만 쓴다 — `#197fb2` 파랑, 산문 강조뿐이다 (수식 안에는 색이 없다).
대신 **구간이 191개(13,413자, 42쪽)로 지금까지 최다**다. 전사 전에 뽑아 놓고 옆에 두고 쓴다.

```bash
python3 _study_kit/tools/dump_colored.py --count          # 개수만 — 전사 후 대조용
python3 _study_kit/tools/dump_colored.py -p 54            # 54쪽만
python3 _study_kit/tools/dump_colored.py -p 7-22          # 쪽 범위
python3 _study_kit/tools/dump_colored.py --min-chars 20   # 짧은 구간 숨기기
```

색 목록은 `dump_colored.py` 위쪽 `NAME` 에 모아 두었다. 다른 문서를 다룰 때는 거기만 고친다.

출력에는 각 구간이 **어느 식 번호 근처인지**도 같이 나온다. 줄바꿈은 ` / ` 로 표시된다.

## 위젯 헬퍼 주입 — `inject_helper.py`

위젯 18개가 `window.MV` 를 공유한다. 원본은 `tools/widgets/_mv_helper.js` 한 벌이고,
위젯 파일에는 `//%MV%` 표시만 둔다.

```bash
python3 _study_kit/tools/inject_helper.py           # 표시 자리를 채운다 (여러 번 돌려도 됨)
python3 _study_kit/tools/inject_helper.py --check   # 어긋난 파일만 알려 주고 끝
```

헬퍼를 고쳤으면 **빌드 전에 반드시** 한 번 돌린다. `--check` 를 빌드 전에 걸어 두면 잊지 않는다.

## 그림·표 추출 (이 스터디에서는 쓰지 않음)

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

초기 렌더링만 보면 부족하다. **버튼을 전부 누르고 슬라이더를 min/중간/max 로 흔든 뒤**
JS 오류·빈 캔버스·NaN 을 확인한다. 이 스터디에서는 위젯이 18개라 아래 방식으로 한 번에 돌렸다.

**빌드된 HTML 에는 `</body>` 가 없다** (`3_Pitfalls` D4). `replace('</body>', probe)` 로
탐침을 끼우면 **조용히 실패**한다 — 반드시 **파일 끝에 이어 붙이고**, 붙었는지
`grep -c '__probe'` 로 먼저 확인한다.

```python
probe = r"""
<script>
window.__errs=[];
window.addEventListener('error',function(e){window.__errs.push('ERR '+(e.message||e));});
window.addEventListener('unhandledrejection',function(e){window.__errs.push('REJ '+e.reason);});
setTimeout(function(){
  var log=[];
  function blank(cv){ var g=cv.getContext('2d'),d=g.getImageData(0,0,cv.width,cv.height).data,n=0;
    for(var i=3;i<d.length;i+=4*97){ if(d[i]!==0) n++; } return n<5; }
  document.querySelectorAll('.lab').forEach(function(L){
    var id=L.id||'?';
    L.querySelectorAll('button').forEach(function(b){ try{b.click();}catch(e){log.push('BTN '+id);} });
    L.querySelectorAll('input[type=range]').forEach(function(s){
      var mn=+s.min,mx=+s.max,dv=s.defaultValue;
      [mn,(mn+mx)/2,mx].forEach(function(v){
        s.value=String(v); s.dispatchEvent(new Event('input',{bubbles:true})); });
      s.value=dv; s.dispatchEvent(new Event('input',{bubbles:true})); });
    L.querySelectorAll('canvas').forEach(function(cv){ if(blank(cv)) log.push('BLANK '+id); });
    L.querySelectorAll('.readout').forEach(function(r){
      if(/NaN|undefined|Infinity/.test(r.textContent)) log.push('BAD '+id); });
  });
  var ov=[]; document.querySelectorAll('.mathblock').forEach(function(m,i){
    var o=m.scrollWidth-m.clientWidth; if(o>1) ov.push((i+1)+':'+o); });
  var d=document.createElement('pre'); d.id='__probe';
  d.textContent='LABS='+document.querySelectorAll('.lab').length+
    ' 넘침='+(ov.join(',')||'없음')+
    ' 본문가로='+(document.body.scrollWidth-document.documentElement.clientWidth)+
    '\n'+(window.__errs.concat(log).join('\n')||'오류 0 · 빈 캔버스 0 · NaN 0');
  document.body.appendChild(d);
},9000)</script>"""
open(tmp,'w').write(open(built).read() + probe)     # ← 끝에 이어 붙인다
```

```bash
google-chrome --headless --disable-gpu --no-sandbox \
    --window-size=1440,1000 --virtual-time-budget=900000 \
    --dump-dom "file://$PWD/probe.html" | grep -A20 '__probe'
```

- `--virtual-time-budget` 은 **20만 이상**으로 준다. 9.4MB 문서는 MathJax 조판에만 한참 걸린다
- `data-mjx-error`·`merror` 를 셀 때는 **`<script>` 를 먼저 지운다**.
  MathJax 소스 자체에 그 문자열이 들어 있어 그냥 세면 항상 0 이 아니다

### 창 폭 掃引 — 수식이 본문을 밀어내지 않는가

수식은 넘치면 `.mathblock` 안에서 가로 스크롤되면 되지만, **본문 자체가 밀리면 안 된다**.
빌드 뒤 폭을 여러 개로 바꿔 가며 `document.body.scrollWidth - clientWidth` 를 잰다.

```bash
for w in 1440 900 700 480 360; do
  google-chrome --headless --disable-gpu --no-sandbox \
    --window-size=$w,900 --virtual-time-budget=600000 \
    --dump-dom "file://$PWD/probe.html" | grep -o '본문가로=[0-9-]*'
done
```

전부 `0` 이어야 한다. 0 이 아니면 원인은 대개 셋 중 하나다 (`3_Pitfalls` C9):

1. **줄바꿈 불가능한 인라인 수식** — `.mathblock` 같은 스크롤 상자가 없어 그대로 폭을 민다
2. **`mjx-assistive-mml`** — `position:absolute; width:auto` 라 조상의 `overflow:auto` 를 빠져나간다
3. **링크로 파싱되지 않은 긴 URL** — 원시 마크다운이 그대로 남은 경우

셋 다 `build_html.py` 에서 고쳐 두었지만, 새 문서에서 또 다른 경로가 나올 수 있으니
폭 掃引은 매번 돌린다.

### 색 강조 대조 — 191구간을 눈으로 세지 마라

`dump_colored.py` 의 색 구간이 노트에서 실제로 `==` 안에 들어 있는지 **기계적으로** 확인한다.
PDF 구간과 노트를 각각 「한글·영문·숫자만 남긴 문자열」로 정규화하고,
노트 쪽은 **글자마다 `==` 안인지 밖인지** 표시해 두면 구간별 포함률이 % 로 나온다.

정규화에서 두 가지를 조심한다 (놓치면 멀쩡한 구간이 "본문없음" 으로 뜬다):

- `\begin{pmatrix}` 의 **`pmatrix` 가 낱말로 섞인다** → `\(begin|end)\{…\}` 를 통째로 지운다
- `\det` 는 지워지는데 PDF 에는 `det` 가 남는다 → 이런 항목은 눈으로 확인

이 스터디에서는 이 검사기로 **191구간 중 149구간이 빠져 있던 것**을 찾아냈다.
자동 반영까지 시킬 때는 경계가 **인라인 수식 안으로 들어가지 않도록**
`$…$` 구간을 미리 구해 놓고 밖으로 밀어내야 한다.
