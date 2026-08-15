# Probabilistic Robotics 스터디

Sebastian Thrun, Wolfram Burgard, Dieter Fox의 *Probabilistic Robotics* (MIT Press, 2006)를
**EKF/UKF + Particle Filter 기반 Localization**까지 학습하기 위한 개인 스터디 자료 저장소.

원본 PDF: `ref/Probabilistic Robotics _Sebastian Thrun et al..pdf`

---

## 문서 안내 (0~3번 문서를 언제 보는가)

| 문서 | 내용 | 언제 참고 / 사용 |
|---|---|---|
| [`0_Contents.md`](0_Contents.md) | 학습 범위 목차 (Part I 1~6장, Part II 7~8장의 전체 하위 절 + 페이지 번호), 추천 학습 순서 | **다음에 뭘 공부할지 정할 때.** 새 챕터 노트를 만들 때 그 챕터의 절 구성을 그대로 가져오는 기준. 폴더/파일 번호도 여기 챕터 번호를 따름 |
| [`1_Tools.md`](1_Tools.md) | 자료 제작 도구 스택(Markdown, MathJax, PDF 이미지 추출, Canvas 위젯)과 **빌드·점검 명령어** | **HTML을 만들거나 다시 빌드할 때, 그리고 참조를 점검할 때.** `python3 _study_kit/tools/build_html.py <경로>`, `python3 _study_kit/tools/check_refs.py` 실행법이 여기 있음 |
| [`2_Template_and_Rule.md`](2_Template_and_Rule.md) | 챕터 노트 작성 템플릿(1.개념 → 2.수식/유도 → 3.예제/실습)과 언어·생략금지·예제 규칙 | **실제로 챕터 내용을 쓰기 직전에 반드시.** 모든 챕터 `.md`는 이 구조와 규칙을 따름 |
| [`3_Pitfalls.md`](3_Pitfalls.md) | 이 자료를 만들며 실제로 겪은 함정 15가지 (PDF 다루기·노트 쓰기·위젯·환경) | 뭔가 이상할 때. 새 스터디를 시작할 때는 시작 전에 한 번 |

### 일반적인 작업 흐름

1. `0_Contents.md`에서 이번에 공부할 챕터/절을 고른다
2. `2_Template_and_Rule.md`의 템플릿과 규칙에 맞춰 해당 챕터 폴더의 `.md`를 작성한다
3. 책 그림이 필요하면 `python3 _study_kit/tools/extract_figures.py --chapter N --pages A-B --out <챕터>/images`
   로 추출해 그 챕터의 `images/`에 넣고 참조한다 (`--pages`는 PDF 페이지 = 책 페이지 + 21)
4. 인터랙티브 시각화가 필요하면 `_study_kit/tools/widgets/NAME.html`을 만들고, `.md` 본문에 `<!--widget:NAME-->` 한 줄을 넣는다
5. `python3 _study_kit/tools/build_html.py <챕터>.md`를 실행해 같은 폴더에 **self-contained HTML 파일**을 만들고, 브라우저로 열어서 본다
6. **검증한다** — 아래 세 가지는 실제로 오류가 나왔던 항목이라 매번 확인할 값어치가 있다
   - `python3 _study_kit/tools/check_refs.py <챕터>` — 그림·표·페이지·절 참조가 원문과 맞는지
   - **본문의 손계산을 코드로 재계산해 대조** — 7장에서 이 방법으로 7곳의 오류를 잡았다
   - **위젯을 헤드리스로 열어 확인** — 7장 위젯의 단위 버그(공분산이 10⁴배)를 이렇게 찾았다
     (명령은 `1_Tools.md`의 "빌드 결과 확인" 참조)

---

## 폴더 구조

```
Probabilistic_Robotics/            ← 스터디 루트. 명령은 여기서 실행한다
├── ref/                       원본 PDF
│
├── _study_kit/                ← 킷 루트. 도구와 메타 문서가 모여 있다
│   ├── README.md              이 문서
│   ├── kit.conf               설정 (PDF·페이지 오프셋·레이아웃·사이드바)
│   ├── 0_Contents.md          학습 범위 목차 + 학습 순서
│   ├── 1_Tools.md             제작 도구 스택
│   ├── 2_Template_and_Rule.md 노트 작성 템플릿 & 규칙
│   ├── 3_Pitfalls.md          실전에서 겪은 함정 15가지
│   └── tools/                 제작 도구
│       ├── build_html.py          md → self-contained html 변환기
│       ├── extract_figures.py     PDF에서 챕터의 Figure/Table 크롭 추출 (PyMuPDF)
│       ├── check_refs.py          노트의 그림·표·페이지·절 참조를 원문과 대조
│       ├── kit_config.py          kit.conf 로더 (스크립트들이 공유)
│       ├── figure_names/chN.txt   챕터별 그림 파일명 매핑 (추출 재현용)
│       ├── vendor/tex-svg.js      MathJax (수식 렌더링, 외부 폰트 불필요)
│       └── widgets/*.html         Canvas 인터랙티브 위젯
│
├── part1_basics/              Part I. Basics (1~6장)
│   ├── 01_introduction/
│   ├── 02_recursive_state_estimation/
│   ├── 03_gaussian_filters/
│   ├── 04_nonparametric_filters/
│   ├── 05_robot_motion/
│   └── 06_robot_perception/
│
└── part2_localization/        Part II. Localization (7~8장)
    ├── 07_localization_markov_gaussian/
    └── 08_localization_grid_montecarlo/
```

각 챕터 폴더는 다음 형태를 가진다:

```
0N_<chapter_name>/
├── 0N_<chapter_name>.md      챕터 노트 원본 (하위 절은 이 파일 안에서 ## / ### 헤더로 구분)
├── 0N_<chapter_name>.html    빌드 결과물 — 브라우저로 열어서 공부하는 파일 (직접 편집하지 않음)
└── images/                   해당 챕터에서 쓰는 책 원본 그림
```

- **도구와 문서는 `_study_kit/` 안에, 원본과 노트는 그 바깥에** 둔다. 새 스터디를 시작할 때는
  `_study_kit/` 폴더를 통째로 복사해 가면 된다. 도구가 킷 루트와 스터디 루트를 알아서 구분하므로
  **모든 명령은 스터디 루트(이 폴더)에서 실행한다**
- 폴더 앞 번호(01~08)는 `0_Contents.md`의 챕터 번호와 그대로 매칭된다
- 챕터당 파일 1개 원칙 — 절이 많아도 파일을 쪼개지 않고 한 파일 안에서 헤더로 탐색한다 (흐름 파악에 유리)
- `images/`를 챕터 폴더 안에 두어 각 챕터가 self-contained하도록 유지한다
- **`.md`가 원본, `.html`은 생성물**이다. 내용을 고칠 땐 항상 `.md`를 고치고 다시 빌드한다
- 완성된 `.html`은 수식 엔진·이미지·위젯이 전부 인라인되어 있어 **인터넷 없이 단독으로 열린다** (다른 PC로 복사해도 그대로 동작)
