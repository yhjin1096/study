# 위젯 작성 가이드

위젯은 **알고리즘을 눈으로 확인하게 해 주는 인터랙티브 조각**이다.
슬라이더로 파라미터를 바꾸면 그림과 숫자가 즉시 따라 움직인다.

## 어떻게 붙는가

1. `tools/widgets/NAME.html` 파일을 만든다 (HTML 조각 + `<script>`, **전체 문서가 아님**)
2. 노트 본문에 한 줄을 넣는다

   ```markdown
   <!--widget:NAME-->
   ```

3. `build_html.py`가 그 자리에 파일 내용을 그대로 삽입한다

같은 위젯을 여러 챕터에서 재사용해도 된다 (챕터마다 독립 HTML이라 충돌하지 않는다).

## 뼈대

`example-widget.html`을 복사해 시작하는 것이 가장 빠르다. 구조는 이렇다.

```html
<div class="lab" id="w-이름">          <!-- id 는 위젯마다 고유하게 -->
  <div class="lab-head">
    <span class="lab-tag">실험 1</span>
    <span class="lab-title">제목</span>
    <span class="lab-note">Figure 3.2 를 재현</span>
  </div>
  <div class="lab-body">
    <p>이 위젯이 무엇을 보여주는지 2~3문장. 어느 식·표에 대응하는지 밝힌다.</p>

    <div class="sliders"> … </div>      <!-- 슬라이더들 -->
    <div class="btnrow"> … </div>       <!-- 버튼들 -->
    <canvas id="…-canvas" width="880" height="330"></canvas>
    <div class="legend"> … </div>       <!-- 색 범례 -->
    <div class="readout" id="…-readout"></div>   <!-- 숫자 출력 -->
  </div>
</div>

<script>
(function () { … })();                  <!-- 즉시실행함수로 전역 오염 방지 -->
</script>
```

## 쓸 수 있는 CSS 자산

`build_html.py`가 아래를 제공한다. **직접 색을 지정하지 말고 변수를 쓰라** —
라이트/다크 테마가 자동으로 따라간다.

### 색 변수

| 변수 | 용도 |
|---|---|
| `--ink` / `--ink-soft` / `--ink-faint` | 본문 / 보조 / 흐린 텍스트, 주요 곡선 |
| `--rule` / `--rule-soft` | 축·테두리 / 격자선 |
| `--accent` / `--accent-soft` | 강조 (추정값, 현재 상태) |
| `--predict` | 예측 단계, 두 번째 계열 |
| `--correct` | 보정 단계, 참값·표본 |
| `--ground` / `--panel` / `--panel-2` | 배경 |

```js
function css(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
ctx.strokeStyle = css('--accent');
```

### 클래스

| 클래스 | 용도 |
|---|---|
| `.lab` `.lab-head` `.lab-tag` `.lab-title` `.lab-note` `.lab-body` | 위젯 껍데기 |
| `.sliders` `.slider` | 슬라이더 그리드 (자동 반응형) |
| `.btnrow` + `<button>` | 버튼 줄. `button.ghost`(약하게) `button.correct` `button.predict` |
| `.legend` + `.swatch` | 색 범례 |
| `.readout` | 숫자 출력. 안에서 `<b>`를 쓰면 강조된다 |
| `.log` | 스텝 로그 (스크롤됨) |

## 캔버스 기본 패턴

고해상도 화면에서 흐려지지 않도록 devicePixelRatio를 처리한다.

```js
var dpr = window.devicePixelRatio || 1, W = cv.clientWidth, H = 330;
if (cv.width !== W * dpr) { cv.width = W * dpr; cv.height = H * dpr; }
ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
ctx.clearRect(0, 0, W, H);
```

좌표 변환 함수를 만들어 두면 그리기 코드가 깔끔해진다.

```js
function PX(x) { return offX + (x - minX) * sc; }
function PY(y) { return H - (offY + (y - minY) * sc); }   // y축을 위로
```

`window.addEventListener('resize', draw)`를 잊지 말 것.

---

## 반드시 지킬 것 세 가지

이전 스터디에서 **실제로 버그가 났던** 지점들이다. 자세한 내용은 `3_Pitfalls.md` C장.

### ① 단위를 모델 식과 맞춘다

위젯이 cm를 쓰는데 모델 계수가 m를 전제하면 **$v^2$ 항이 10⁴배**가 되어 조용히 망가진다.
슬라이더를 움직여도 결과가 안 변하면 그 항이 다른 항에 압도당하고 있다는 신호다.
각 항의 크기를 실제로 찍어 보라.

### ② 화면 범위 계산에 그릴 것을 전부 넣는다

표본점만으로 범위를 정하면 타원이 화면 밖으로 나가 직선처럼 보인다.
타원 반경(2σ), 궤적, 랜드마크를 모두 포함시킨다.

### ③ 조작까지 해 보고 나서 "동작한다"고 말한다

초기 렌더링만 보면 부족하다. 버튼 전부 클릭 + 슬라이더 극단값까지 돌려
JS 오류·빈 캔버스·NaN을 확인한다. 명령은 `1_Tools.md`의 "위젯 점검"에 있다.

---

## 좋은 위젯의 조건

- **노트의 어느 식·표에 대응하는지 밝힌다** — 코드 주석에 `// Table 5.3 라인 2` 처럼
- **책 그림을 재현하는 프리셋 버튼**을 둔다 — "Figure 3.2 설정" 같은
- **readout에 숫자를 찍는다** — 노트의 예제 수치와 대조할 수 있으면 검산 도구가 된다
- 슬라이더는 6개 이하. 그 이상이면 위젯을 나눈다
