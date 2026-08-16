#!/usr/bin/env python3
"""위젯 파일의 `//%EJ%` 자리에 공용 헬퍼(window.EJ)를 채워 넣는다.

위젯 12개가 모두 같은 계산 라이브러리를 쓴다. 완성된 HTML 은 오프라인 단일
파일이어야 하므로 헬퍼를 위젯마다 인라인해야 하는데, 그렇다고 12벌을 손으로
복사해 두면 한 곳을 고칠 때 열두 곳이 어긋난다.

그래서 원본은 `widgets/_ej_helper.js` 한 벌만 두고, 위젯에는 표시만 남긴다.

    <script>
    (function () {
      //%EJ%
      var P = window.EJ;
      ...

이 스크립트를 돌리면 그 자리가 아래로 바뀐다.

    // ==EJ-BEGIN== (자동 생성 — 고치지 말 것. tools/widgets/_ej_helper.js 를 고칠 것)
    if (!window.EJ) window.EJ = (function () { ... })();
    // ==EJ-END==

이미 채워진 파일에 다시 돌려도 된다. BEGIN~END 를 통째로 갈아 끼운다.

사용법
  python3 _study_kit/tools/inject_helper.py            # 전체
  python3 _study_kit/tools/inject_helper.py --check    # 어긋난 파일만 알려 주고 끝
"""
import argparse
import re
import sys
from pathlib import Path

BEGIN = "// ==EJ-BEGIN== (자동 생성 — 고치지 말 것. tools/widgets/_ej_helper.js 를 고칠 것)"
END = "// ==EJ-END=="
MARK = "//%EJ%"


def block(helper_text, indent):
    body = "\n".join((indent + ln) if ln.strip() else "" for ln in helper_text.split("\n"))
    return f"{indent}{BEGIN}\n{body}\n{indent}{END}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="쓰지 않고 어긋난 파일만 보고")
    args = ap.parse_args()

    wdir = Path(__file__).resolve().parent / "widgets"
    helper = (wdir / "_ej_helper.js").read_text(encoding="utf-8").rstrip("\n")

    pat = re.compile(
        r"^([ \t]*)" + re.escape(BEGIN) + r"\n.*?^[ \t]*" + re.escape(END),
        re.S | re.M,
    )
    stale, done = [], []
    for f in sorted(wdir.glob("*.html")):
        text = f.read_text(encoding="utf-8")
        if MARK in text:
            new = re.sub(r"^([ \t]*)" + re.escape(MARK) + r"[ \t]*$",
                         lambda m: block(helper, m.group(1)), text, flags=re.M)
        elif pat.search(text):
            new = pat.sub(lambda m: block(helper, m.group(1)), text)
        else:
            continue
        if new != text:
            stale.append(f.name)
            if not args.check:
                f.write_text(new, encoding="utf-8")
        done.append(f.name)

    if args.check:
        print("어긋남: " + (", ".join(stale) if stale else "없음"))
        return 1 if stale else 0
    print(f"헬퍼 주입 {len(stale)}개 갱신 / 대상 {len(done)}개")
    for n in stale:
        print("  " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
