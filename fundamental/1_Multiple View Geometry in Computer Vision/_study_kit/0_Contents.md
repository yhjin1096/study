# 학습 범위 목차 — Notes on Multiple View Geometry in Computer Vision

Gyubeom Edward Im (Orig. by Richard Hartley and Andrew Zisserman), 104쪽 (21차 개정 2026-07-12)
쪽번호는 원문 그대로다 (PDF 쪽 = 인쇄 쪽, 오프셋 0).

노트: [`notes/notes_on_mvg.md`](../notes/notes_on_mvg.md) →
`.html` (단일 파일 9.4MB, 오프라인으로 열림)

**지금까지 열 개 스터디 중 가장 크다** — 104쪽, 식 (1)~(456), 장 15개 + 절 195개, 그림 63개.
직전 최대였던 6번(45쪽·식 204개)의 2.3배다.

---

## 전체 구성

| 장 | 제목 | 쪽 | 식 | 그림 | 위젯 |
|---|---|---|---|---|---|
| 1 | Projective Space | 7 | (1)~(3) | 1 | **실험 1** |
| 2 | Projective Geometry and Transformations in 2D | 7 | (4)~(78) | 13 | **실험 2~5** |
| 3 | Camera Models | 23 | (79)~(139) | 12 | **실험 6~8** |
| 4 | Computation of the Camera Matrix P | 38 | (140)~(170) | 3 | **실험 9** |
| 5 | More Single View Geometry | 44 | (171)~(201) | 12 | **실험 10~11** |
| 6 | Epipolar Geometry and the Fundamental Matrix | 54 | (202)~(275) | 5 | **실험 12~13** |
| 7 | 3D Reconstruction of Cameras and Structure | 68 | (276)~(298) | 2 | **실험 14** |
| 8 | Computation of the Fundamental Matrix F | 72 | (299)~(315) | — | **실험 15** |
| 9 | Structure Computation | 75 | (316)~(341) | 3 | **실험 16** |
| 10 | Scene planes and homographies | 80 | (342)~(384) | 6 | **실험 17** |
| 11 | Affine Epipolar Geometry | 89 | (385)~(400) | 3 | |
| 12 | The Trifocal Tensor | 93 | (401)~(456) | 3 | **실험 18** |
| 13 | Revision log | 103 | — | — | |
| 14 | References | 104 | — | — | |
| 15 | Closure | 104 | — | — | |

식 번호는 (1)~(456) — **누락·중복·순서 어긋남 없음**.

---

## 절 단위 구성 (위젯 위치 표시)

### 1 Projective Space (p7)

식 (1)~(3). 그림 1개. → **실험 1 `projective-space`**

### 2 Projective Geometry and Transformations in 2D (p7~22)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 2.1 | The 2D projective plane | (4)~(13) | **실험 2 `points-lines-duality`** |
| 2.2 | Ideal points and the line at infinity | (14)~(19) | |
| 2.3 | Conics and dual conics | (20)~(33) | **실험 3 `conics-dual`** |
| 2.4 | Projective transformations | — | |
| 2.5 | A hierarchy of transformations | (34)~(38) | **실험 4 `transformation-hierarchy`** |
| 2.6 | Decomposition of a projective transformation | (39) | |
| 2.7 | Recovery of affine and metric properties from images | (40)~(78) | **실험 5 `metric-rectification`** |

### 3 Camera Models (p23~37)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 3.1 | Finite cameras | (79)~(96) | **실험 6 `pinhole-camera-matrix`** |
| 3.2 | The projective camera (camera anatomy) | (97)~(107) | **실험 7 `camera-anatomy`** |
| 3.3 | Action of a projective camera on points | (108)~(116) | |
| 3.4 | Cameras at infinity (affine cameras) | (117)~(139) | **실험 8 `affine-camera-vertigo`** |

### 4 Computation of the Camera Matrix P (p38~43)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 4.1 | Basic equations | (140)~(153) | |
| 4.2 | Geometric error (Algorithm 7.1) | (154)~(156) | **실험 9 `dlt-camera-matrix`** |
| 4.3 | Zhang's method | (157)~(167) | |
| 4.4 | Radial distortion | (168)~(170) | |

### 5 More Single View Geometry (p44~53)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 5.1 | Camera calibration and the image of the absolute conic | (171)~(180) | **실험 10 `image-absolute-conic`** |
| 5.2 | Orthogonality and $\omega$ | (181) | |
| 5.3 | Vanishing points and vanishing lines | (182)~(190) | **실험 11 `vanishing-points`** |
| 5.4 | Affine 3D measurements and reconstruction | (191)~(193) | |
| 5.5 | Determining camera calibration K from a single view | (194)~(196) | |
| 5.6 | The calibrating conic | (197)~(201) | |

### 6 Epipolar Geometry and the Fundamental Matrix (p54~67)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 6.1 | Epipolar geometry | — | |
| 6.2 | The fundamental matrix F | (202)~(213) | **실험 12 `fundamental-matrix`** |
| 6.3 | The epipolar line homography | (214)~(216) | |
| 6.4 | Fundamental matrices arising from special motions | (217)~(218) | |
| 6.5 | Retrieving the camera matrices | (219)~(236) | |
| 6.6 | Canonical cameras given F | (237)~(245) | |
| 6.7 | The essential matrix | (246)~(261) | **실험 13 `essential-matrix`** |
| 6.8 | Extraction of cameras from the essential matrix | (262)~(275) | |

### 7 3D Reconstruction of Cameras and Structure (p68~71)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 7.1 | The projective reconstruction theorem | (276)~(281) | |
| 7.2 | Stratified reconstruction | (282)~(298) | **실험 14 `stratified-reconstruction`** |

### 8 Computation of the Fundamental Matrix F (p72~74)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 8.1 | Basic equations | (299)~(304) | |
| 8.2 | The normalized 8-point algorithm | (305)~(311) | **실험 15 `eight-point-algorithm`** |
| 8.3 | The Gold Standard method | (312)~(315) | |

### 9 Structure Computation (p75~79)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 9.1 | Problem statement | (316)~(320) | |
| 9.2 | Linear triangulation methods | (321)~(326) | **실험 16 `triangulation`** |
| 9.3 | An optimial solution | (327)~(341) | |

### 10 Scene planes and homographies (p80~88)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 10.1 | Homographies given the plane and vice versa | (342)~(361) | **실험 17 `plane-homography`** |
| 10.2 | Plane induced homographies given F and image correspondences | (362)~(379) | |
| 10.3 | Computing F given the homography induced by a plane | (380) | |
| 10.4 | The infinite homography $\mathbf{H}_\infty$ | (381)~(384) | |

### 11 Affine Epipolar Geometry (p89~92)

| 절 | 제목 | 식 |
|---|---|---|
| 11.1 | Affine epipolar geometry | (385)~(389) |
| 11.2 | The affine fundamental matrix | (390)~(397) |
| 11.3 | Estimating $\mathbf{F}_A$ from image point correspondences | (398)~(400) |

### 12 The Trifocal Tensor (p93~102)

| 절 | 제목 | 식 | 위젯 |
|---|---|---|---|
| 12.1 | The geometric basis for the trifocal tensor | (401)~(416) | |
| 12.2 | Epipolar lines / 카메라 행렬 복원 | (417)~(430) | |
| 12.3 | The trifocal tensor and tensor notation | (431)~(439) | **실험 18 `trifocal-tensor`** |
| 12.4 | Transfer | (440)~(452) | |
| 12.5 | The fundamental matrices for three views | (453)~(456) | |

---

## 그림

**그림 캡션이 하나도 없다** — 전문에서 Figure/Fig./Table 이 0회다.
그래서 `tools/extract_figures.py` 대신 `tools/extract_images_bbox.py` 로 뽑았고,
파일 이름은 **바로 앞 제목**에서 자동으로 붙였다.

```
notes/images/fig01_p007_projective_space.png
notes/images/fig41_p054_epipolar_geometry.png
notes/images/fig60_p093_the_trifocal_tensor.png
...
```

63개, 합계 4.1MB. 이미지 객체와 1:1 대응하며 bbox 가 전부 페이지 안쪽이다.

---

## 색

원문이 쓰는 색은 **`#197fb2` 파랑 한 가지**뿐이다 (산문 강조, 191구간 13,413자, 42쪽에 걸침).
수식 안에는 색이 없어 `\color` 를 쓸 일이 없다.

노트에서는 `==강조==` → `<span class="hl">` 로 옮겼다.
페이지 경계에서 둘로 쪼개진 강조 한 쌍(p96/p97 `해당 공식은 세 점 사이(point-point-point)…`)을
하나로 합쳐 **190구간**이 되었고, `tools/dump_colored.py` 출력과 1:1 대조해 전부 확인했다.

---

## 검증 결과

```
식 456개 · 범위 (1)~(456) · 누락 [] · 중복 [] · 순서일치 True
장 15개 · 절 195개 (h2 55 + h3 140) · 그림 63개 · 위젯 18개
PDF 문장 959개 전부 노트에 있음 (미검출 2건은 제목 경계의 정규화 잔재)
색 강조 191구간 → 190구간 전부 재현 (합쳐진 한 쌍 제외하고 1:1)
MathJax merror 0 · data-mjx-error 0 · mjx-container 2,860
위젯 헤드리스 점검: 버튼 전부 클릭 · 슬라이더 전부 min/mid/max 掃引 →
  JS 오류 0 · 빈 캔버스 0 · NaN/undefined/Infinity 0
창 폭 1440/900/700/480/360px 에서 본문 가로 넘침 0
window.MV 항등식 44개 전부 기계정밀도 통과
```
