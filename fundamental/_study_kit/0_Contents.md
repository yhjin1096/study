# <책 제목> — 학습 목차

> **이 파일은 템플릿이다.** `<...>` 부분을 채우고 이 안내 블록은 지운다.
>
> 이 파일이 이후 모든 작업의 기준이 된다:
> - 폴더/파일 번호가 여기 장 번호를 따른다
> - 챕터 노트의 절 구성을 여기서 그대로 가져온다
> - `tools/check_refs.py`가 여기 절 목록으로 참조를 검사한다
>
> **쪽번호는 책에 인쇄된 번호를 적는다** (PDF 페이지 아님). 목차를 다 적은 뒤
> 아래 "목차 검증" 스니펫으로 한 번에 대조하면 오타를 잡을 수 있다.

학습 목표: <무엇에서 시작해 무엇까지 갈 것인가. 한두 문장으로.>

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 <제목> | ⬜ | — | — |
| 2 <제목> | ⬜ | — | — |

---

## Part I. <파트 제목>

### 1장. <제목> (p.<쪽>)
- 1.1 <절 제목> (<쪽>)
- 1.2 <절 제목> (<쪽>)
  - 1.2.1 <하위 절> (<쪽>)
  - 1.2.2 <하위 절> (<쪽>)
- 1.3 Summary (<쪽>)
- 1.4 Bibliographical Remarks (<쪽>)
- 1.5 Exercises (<쪽>)

### 2장. <제목> (p.<쪽>)
- 2.1 <절 제목> (<쪽>)

---

## Part II. <파트 제목>

### N장. <제목> (p.<쪽>)
- N.1 <절 제목> (<쪽>)

---

## 추천 학습 순서

1. 1장 (<한 줄 메모>)
2. 2장 (<한 줄 메모>)

> 책 순서를 그대로 따를지, 저자가 권하는 다른 순서를 따를지 여기서 정한다.
> 저자가 서문이나 "이 책을 가르치는 법" 절에서 순서를 제안하는 경우가 있으니 확인해 보라.
> 책 순서는 **의존성이 깔끔**하고, 저자 제안 순서는 **동기 부여가 빠른** 편이다.

---

## 목차 검증

목차를 다 적은 뒤 아래를 돌려 쪽번호가 실제와 맞는지 확인한다.
(`kit.conf`의 `page_offset`이 먼저 정확해야 한다.)

```python
import fitz, re, sys
sys.path.insert(0, 'tools'); import kit_config
cfg = kit_config.load(); doc = fitz.open(cfg['pdf']); off = cfg['page_offset']

toc = []
for line in open('0_Contents.md', encoding='utf-8'):
    m = re.match(r'\s*-\s*(\d+\.\d+(?:\.\d+)?)\s+(.+?)\s*\((\d+)\)\s*$', line)
    if m: toc.append((m.group(1), m.group(2), int(m.group(3))))
    m2 = re.match(r'###\s*(\d+)장\.\s*(.+?)\s*\(p\.(\d+)\)', line)
    if m2: toc.append((m2.group(1), m2.group(2), int(m2.group(3))))

bad = 0
for sec, title, bookp in toc:
    ok = False
    for probe in (bookp + off, bookp + off + 1):        # 절이 다음 쪽으로 밀리는 경우 허용
        if not (1 <= probe <= doc.page_count): continue
        for blk in doc[probe-1].get_text("dict")["blocks"]:
            if blk.get("type") != 0: continue
            for ln in blk["lines"]:
                f = ln["spans"][0]
                s = "".join(x["text"] for x in ln["spans"]).strip()
                if "Bold" in f["font"] and f["size"] > 10.5 and s.startswith(sec):
                    ok = True
        if ok: break
    if not ok:
        print(f"  [불일치] {sec} {title[:40]} — 책 p{bookp}"); bad += 1
print(f"\n불일치 {bad}건 / {len(toc)}건")
```
