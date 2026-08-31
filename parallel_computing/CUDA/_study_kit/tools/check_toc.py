#!/usr/bin/env python3
"""0_Contents.md 의 절 번호·쪽번호를 원본 PDF와 대조한다.

목차를 손으로 옮겨 적으면 반드시 오타가 난다. 이 스크립트는 목차의 각 항목에 대해
"그 책 쪽(→ PDF 쪽)에 그 절 제목이 실제로 있는가"를 확인한다.

  python3 _study_kit/tools/check_toc.py            # 전체 검사
  python3 _study_kit/tools/check_toc.py --verbose  # 맞은 항목까지 전부 출력

이 책의 조판 (다른 책에 쓸 때는 HEADING_* 를 다시 재야 한다):
  · 절 제목  TradeGothic-Bold      13.4pt   본문 영역 (y > 60)
  · 머리글   TradeGothic-BoldTwo   11.0pt   y ≈ 29        ← 제목이 아니다. 걸러낸다
  · 쪽번호가 구간마다 다르게 어긋나므로 kit_config.book_to_pdf() 로 환산한다
"""
import argparse
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_config

CFG = kit_config.load()
HEADING_MIN_SIZE = 11.5     # 이보다 작으면 제목이 아니다 (본문 9.5 · 머리글 11.0)
HEADING_MIN_Y = 60.0        # 머리글 아래부터가 본문 영역
HEADING_GAP = 8.0           # 이보다 벌어지면 다른 제목 덩어리로 본다

CHAP = re.compile(r'^###\s*(\d+)장\.\s*(.+?)\s*\(p\.(\d+)\)\s*$')
APP = re.compile(r'^###\s*부록\s*([A-Z])\.\s*(.+?)\s*\(p\.(\d+)\)\s*$')
SEC = re.compile(r'^-\s*((?:\d+|[A-Z])\.\d+(?:\.\d+)?)\s+(.+?)\s*\((\d+)\)\s*$')


def toc_entries(path):
    """(절번호, 제목, 책 쪽번호) 목록. 장/부록은 절번호 자리에 'CHAPTER 6' 식으로 넣는다."""
    out = []
    for line in open(path, encoding='utf-8'):
        for rx, fmt in ((CHAP, 'CHAPTER %s'), (APP, 'APPENDIX %s'), (SEC, '%s')):
            m = rx.match(line)
            if m:
                out.append((fmt % m.group(1), m.group(2), int(m.group(3))))
                break
    return out


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
            if ln['bbox'][1] < HEADING_MIN_Y or sp['size'] < HEADING_MIN_SIZE:
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
    ap.add_argument('--contents', default=os.path.join(CFG['kit'], '0_Contents.md'))
    args = ap.parse_args()

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
        # 절이 다음 쪽으로 밀려 조판되는 경우가 있어 두 쪽을 본다
        is_chapter = sec.startswith(('CHAPTER', 'APPENDIX'))
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
