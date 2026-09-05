#!/usr/bin/env python3
"""0_Contents.md 의 절 번호·쪽번호를 원본 PDF와 대조한다.

목차를 손으로 옮겨 적으면 반드시 오타가 난다. 이 스크립트는 목차의 각 항목에 대해
"그 책 쪽(→ PDF 쪽)에 그 절 제목이 실제로 있는가"를 확인한다.

  python3 _study_kit/tools/check_toc.py            # 전체 검사
  python3 _study_kit/tools/check_toc.py --verbose  # 맞은 항목까지 전부 출력

판정 기준은 kit.conf 에서 읽는다 (`heading_size` · `heading_gap` · `header_y`).
머리글에도 절 제목이 반복 인쇄되는 판형이 많으므로, **글자 크기와 세로 위치**로
본문의 제목만 골라낸다. 새 책에 쓸 때 아무것도 안 맞으면 이 세 값을 먼저 의심하라.
어떤 값을 넣어야 하는지는 아래 한 줄로 조사한다.

    python3 _study_kit/tools/check_toc.py --survey <절이 시작되는 PDF 쪽>

쪽번호는 kit_config.book_to_pdf() 로 환산한다 (오프셋이 구간마다 다를 수 있다).
"""
import argparse
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_config

CFG = kit_config.load()
HEADING_MIN_SIZE = CFG["heading_size"]   # 이보다 작으면 제목이 아니다
HEADING_MIN_Y = CFG["header_y"]          # 머리글 아래부터가 본문 영역
HEADING_GAP = CFG["heading_gap"]         # 이보다 벌어지면 다른 제목 덩어리
HEADING_FONT = CFG["heading_font"]       # 폰트 이름 정규식. 주면 크기 대신 이걸로 판정

CHAP = re.compile(r'^###\s*(\d+)장\.\s*(.+?)\s*\(p\.(\d+)\)\s*$')
APP = re.compile(r'^###\s*부록\s*([A-Z])\.\s*(.+?)\s*\(p\.(\d+)\)\s*$')
# 번호가 없거나 로마 숫자인 장 — 파트 도입부(Prelude)와 맺음말(Epilogue).
#   ### Prelude I (p.3)          제목을 생략하면 'Prelude' 로 본다
#   ### Prelude I. 제목 (p.3)
#   ### Epilogue (p.548)
PRE = re.compile(
    r'^###\s*(Prelude\s*[IVXLC]+|Epilogue)\s*(?:\.\s*(.+?))?\s*\(p\.(\d+)\)\s*$')
# 절 번호는 숫자(6.1) · 부록 글자(A.1) · 로마 숫자(I.1 · III.2) 를 받는다.
SEC = re.compile(r'^-\s*((?:\d+|[A-Z]+)\.\d+(?:\.\d+)?)\s+(.+?)\s*\((\d+)\)\s*$')


def toc_entries(path):
    """(절번호, 제목, 책 쪽번호) 목록. 장/부록은 절번호 자리에 'CHAPTER 6' 식으로 넣는다.

    ``` 로 둘러싼 코드 블록은 건너뛴다. 목차 파일 안에 형식 설명용 예시를 적어 두는
    경우가 있는데, 그것까지 실제 항목으로 세면 있지도 않은 절이 불일치로 잡힌다.
    """
    out = []
    in_fence = False
    for line in open(path, encoding='utf-8'):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for rx, fmt in ((CHAP, 'CHAPTER %s'), (APP, 'APPENDIX %s'),
                        (PRE, '%s'), (SEC, '%s')):
            m = rx.match(line)
            if m:
                # Prelude/Epilogue 는 제목을 생략할 수 있다. 그때는 그 낱말 자체가
                # 책에 제목으로 인쇄돼 있으므로 그것으로 대조한다.
                title = m.group(2) or m.group(1).split()[0]
                out.append((fmt % m.group(1), title, int(m.group(3))))
                break
    return out


def is_heading_span(sp):
    """이 span 이 절 제목의 조판인가.

    두 가지 기준을 쓴다.

      크기 — 제목이 본문보다 큰 판형 (기본. heading_size)
      폰트 — 제목이 본문과 **같은 크기**이고 볼드로만 구분되는 판형 (heading_font)

    후자가 필요한 이유: LaTeX book 클래스는 \\section 을 본문과 같은 10pt 볼드로
    조판한다. SLAM Handbook 이 그렇다 — 절 제목이 CMBX10 10pt 인데 본문도
    CMR10 10pt 라, 크기만 보면 절 제목을 하나도 못 잡는다.

    둘은 **OR** 로 묶는다. 한 책 안에서도 층위마다 조판이 다르기 때문이다.
    같은 책의 장 제목은 CMR17 17.2pt 로 크지만 볼드가 아니라서, 폰트 기준만
    쓰면 이번엔 장 제목을 놓친다.
    """
    if HEADING_FONT and re.search(HEADING_FONT, sp['font']):
        return True
    return sp['size'] >= HEADING_MIN_SIZE


def headings_on(page):
    """이 쪽에서 '제목처럼 조판된' 덩어리들.

    제목이 두 줄로 넘어가는 절이 많아(예: 10.8), 세로로 붙어 있는 제목 줄은
    하나로 이어 붙인다. 장 표제지처럼 번호와 제목이 따로 놓인 경우도
    같은 덩어리로 묶인다.
    """
    lines = []
    for blk in page.get_text('dict')['blocks']:
        if blk.get('type') != 0:
            continue
        for ln in blk['lines']:
            sp = ln['spans'][0]
            if ln['bbox'][1] < HEADING_MIN_Y or not is_heading_span(sp):
                continue
            txt = ''.join(s['text'] for s in ln['spans']).strip()
            if txt:
                lines.append((ln['bbox'][1], ln['bbox'][3], txt))
    lines.sort()
    blocks, cur, prev_bottom = [], [], None
    for top, bottom, txt in lines:
        if prev_bottom is not None and top - prev_bottom > HEADING_GAP:
            blocks.append(' '.join(cur)); cur = []
        cur.append(txt); prev_bottom = bottom
    if cur:
        blocks.append(' '.join(cur))
    return blocks


# 이 PDF 의 텍스트 레이어가 합자(ligature)를 흘리는 방식.
# '\x1b' 는 매핑되지 않은 'ff' 글리프다 ("work-e\x1biciency" = "work-efficiency").
LIGATURES = {'\x1b': 'ff', '\ufb00': 'ff', '\ufb01': 'fi',
             '\ufb02': 'fl', '\ufb03': 'ffi', '\ufb04': 'ffl'}


def norm(s):
    """비교용 정규화 — 대소문자·공백·하이픈·합자 표현 차이를 무시한다.

    이 PDF 의 텍스트 레이어에는 세 가지 잡음이 있다.
      · 하이픈이 사라진다        'Breadth-first' → 'Breadthfirst'
      · 합자가 제각각이다        'traﬃc' · 'work-e\x1biciency'
      · 합자가 중복되기도 한다   'filter' → 'fifilter'
    앞의 둘은 여기서 펴고, 중복은 단어 단위 부분문자열 비교(match_title)로 넘긴다.
    """
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    return re.sub(r'[^a-z0-9]', '', s.lower())


def match_title(title, block):
    """제목의 주요 단어가 모두 그 덩어리 안에 있으면 같은 제목으로 본다.

    부분문자열 비교라 'filter' 가 'fifilter' 안에서도 걸린다.
    """
    hay = norm(block)
    words = [norm(w) for w in re.split(r'[\s\-—/]+', title)]
    words = [w for w in words if len(w) >= 3]
    return bool(words) and all(w in hay for w in words)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--verbose', action='store_true', help='맞은 항목도 전부 출력')
    ap.add_argument('--survey', type=int, metavar='PDFPAGE',
                    help='그 PDF 쪽의 줄을 글자 크기·위치와 함께 출력한다. '
                         'kit.conf 의 heading_size · header_y 를 정할 때 쓴다')
    ap.add_argument('--contents', default=os.path.join(CFG['kit'], '0_Contents.md'))
    args = ap.parse_args()

    if args.survey:
        doc = fitz.open(CFG['pdf'])
        crit = f"heading_size>={HEADING_MIN_SIZE}"
        if HEADING_FONT:
            crit = f"font~/{HEADING_FONT}/ 또는 " + crit
        print(f"PDF p{args.survey} — 현재 기준: {crit} · y>{HEADING_MIN_Y}")
        for blk in doc[args.survey - 1].get_text('dict')['blocks']:
            if blk.get('type') != 0:
                continue
            for ln in blk['lines']:
                sp = ln['spans'][0]
                txt = ''.join(s['text'] for s in ln['spans']).strip()
                if not txt:
                    continue
                mark = '제목' if (ln['bbox'][1] >= HEADING_MIN_Y
                                  and is_heading_span(sp)) else '  · '
                print(f"  {mark} y={ln['bbox'][1]:6.1f} size={sp['size']:5.1f} "
                      f"{sp['font']:24s} {txt[:46]}")
        doc.close()
        return 0

    entries = toc_entries(args.contents)
    if not entries:
        sys.exit('0_Contents.md 에서 목차 항목을 찾지 못했다: %s' % args.contents)

    doc = fitz.open(CFG['pdf'])
    bad = []
    for sec, title, bookp in entries:
        pdfp = kit_config.book_to_pdf(bookp, CFG)
        if pdfp is None:
            bad.append((sec, title, bookp, None, '그 책 쪽이 PDF에 없다'))
            continue
        # 절이 다음 쪽으로 밀려 조판되는 경우가 있어 두 쪽을 본다.
        # Prelude·Epilogue 도 장 표제지다 — 번호("II")와 제목("Prelude")이 따로
        # 조판되므로 절과 달리 번호 접두사를 요구하면 안 된다.
        is_chapter = sec.startswith(('CHAPTER', 'APPENDIX', 'Prelude', 'Epilogue'))
        number = sec.split()[-1]
        found = None
        for probe in (pdfp, pdfp + 1):
            if not (1 <= probe <= doc.page_count):
                continue
            for h in headings_on(doc[probe - 1]):
                # 장 표제지는 번호와 제목이 따로 조판돼 있어 제목만 본다.
                # 절은 번호까지 맞아야 한다 (같은 쪽에 다른 절 제목이 있을 수 있다).
                if not is_chapter and not h.startswith(number):
                    continue
                if match_title(title, h):
                    found = probe
                    break
            if found:
                break
        if found is None:
            bad.append((sec, title, bookp, pdfp, '그 쪽에 제목이 없다'))
        elif args.verbose:
            print(f'  OK  {sec:12s} 책 p{bookp:3d} → PDF p{found}  {title[:44]}')

    print(f'\n목차 항목 {len(entries)}개 검사 · 불일치 {len(bad)}건')
    for sec, title, bookp, pdfp, why in bad:
        loc = f'PDF p{pdfp}' if pdfp else '-'
        print(f'  [불일치] {sec:12s} 책 p{bookp:3d} ({loc})  {title[:44]}  — {why}')
    doc.close()
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
