# SLAM Handbook — 학습 목차

> **From Localization and Mapping to Spatial Intelligence**
> Carlone · Kim · Barfoot · Cremers · Dellaert 편, 저자 70명, Cambridge University Press
> 원본: `ref/SLAM_Handbook.pdf` (669쪽 / 책 쪽번호 1–647)

학습 목표: SLAM 을 **처음 보는 상태에서 시작해**, 팩터그래프 기반 back-end 의 추정 이론부터
센서별 front-end 실무, 그리고 Spatial AI 까지 책 전체를 빠짐없이 따라간다.
선수 지식은 따로 떼지 않고 **필요한 자리에서 aside 카드로** 그때그때 채운다.

## 이 책의 성격 — 파트마다 다르다

한 가지 방식으로 읽으면 절반이 헛돈다. 챕터별 수식 개수를 실측해 세 유형으로 나눴고,
노트 템플릿도 유형별로 다르게 쓴다 (`2_Template_and_Rule.md`).

| 유형 | 장 | 노트 방식 |
|---|---|---|
| **A. 유도형** | 1(66) · 2(104) · 3(104) · 4(70) · **6(146)** · 11(136) · 12(75) · 16(72) | 3단 구조 — 개념 → 유도 → 예제 |
| **B. 서베이형** | 5(18) · 7(15) · 8(5) · 9(16) · 10(4) · 13(32) · 14(8) · 15(4) · 17(12) · 18 | 5단 구조 — 대표 방법을 골라 직접 유도 |
| **C. 지도형** | Prelude I · II · III · Epilogue | 파트 전체 조망 |
| **D. 참조형** | Notation | 상시 참조, 챕터마다 갱신 |

괄호 안은 번호매김 수식 개수다. Part II·III 는 수식이 아니라 **인용이 본문**이다
(참고문헌 1,359편 · 본문 인용 3,265회). 그래서 서베이형은 `build_refs.py` 로
인용을 펼쳐 읽는다.

## 진행 상황

| 장 | 유형 | 노트 | 그림 | 위젯 |
|---|---|---|---|---|
| [Notation](../part0_prep/00_notation/00_notation.md) | D | ✅ | — | — |
| [Prelude I](../part1_foundations/00_prelude_1/00_prelude_1.md) | C | ✅ | 7 | — |
| [1장 Factor Graphs for SLAM](../part1_foundations/01_factor_graphs/01_factor_graphs.md) | A | ✅ | 15 | — |
| 2장 Advanced State Variable Representations | A | ⬜ | 7 | — |
| 3장 Robustness to Incorrect Data Association and Outliers | A | ⬜ | 10 | — |
| 4장 Differentiable Optimization | A | ⬜ | 1 | — |
| 5장 Dense Map Representations | B | ⬜ | 12 | — |
| 6장 Certifiably Optimal Solvers | A | ⬜ | 4 | — |
| Prelude II | C | ⬜ | 1 | — |
| 7장 Visual SLAM | B | ⬜ | 16 | — |
| 8장 LiDAR SLAM | B | ⬜ | 12 | — |
| 9장 Radar SLAM | B | ⬜ | 12 | — |
| 10장 Event-based SLAM | B | ⬜ | 8 | — |
| 11장 Inertial Odometry for SLAM | A | ⬜ | 6 | — |
| 12장 Leg Odometry for SLAM | A | ⬜ | 9 | — |
| Prelude III | C | ⬜ | 0 | — |
| 13장 Boosting SLAM with Deep Learning | B | ⬜ | 17 | — |
| 14장 Map Representations with Differentiable Volume Rendering | B | ⬜ | 22 | — |
| 15장 Dynamic and Deformable SLAM | B | ⬜ | 16 | — |
| 16장 Metric-Semantic SLAM | A | ⬜ | 18 | — |
| 17장 Towards Open-World Spatial AI | B | ⬜ | 8 | — |
| 18장 The Computational Structure of Spatial AI Systems | B | ⬜ | 4 | — |
| Epilogue | C | ⬜ | — | — |

그림 개수는 `extract_figures.py --list` 로 확인한 실제 값이다 (총 205개).

---

<!-- AUTO-TOC:START -->
## Part I. Foundations of SLAM

### Prelude I (p.3)
- I.1 What is SLAM? (3)
- I.2 Anatomy of a Modern SLAM System (5)
- I.3 The Role of SLAM in the Autonomy Architecture (9)
- I.4 Past, Present, and Future of SLAM, and Scope of this Handbook (13)
- I.5 Handbook Structure (17)

### 1장. Factor Graphs for SLAM (p.19)
- 1.1 Visualizing SLAM With Factor Graphs (20)
- 1.2 From MAP Inference to Least Squares (25)
- 1.3 Solving Linear Least Squares (29)
- 1.4 Nonlinear Optimization (33)
- 1.5 Factor Graphs and Sparsity (35)
- 1.6 Elimination (40)
- 1.7 Incremental SLAM (46)
- 1.8 Further Readings & Recent Trends (51)

### 2장. Advanced State Variable Representations (p.53)
- 2.1 Optimization on Manifolds (53)
- 2.2 Continuous-Time Trajectories (62)
- 2.3 Further Readings & Recent Trends (74)

### 3장. Robustness to Incorrect Data Association and Outliers (p.75)
- 3.1 What Causes Outliers and Why Are They a Problem? (75)
- 3.2 Detecting and Rejecting Outliers in the SLAM Front-end (78)
- 3.3 Increasing Robustness to Outliers in the SLAM Back-end (85)
- 3.4 Further Readings & Recent Trends (98)

### 4장. Differentiable Optimization (p.101)
- 4.1 Recap on Nonlinear Least Squares (102)
- 4.2 Differentiation Through Nonlinear Least Squares (103)
- 4.3 Differentiation on Manifold (109)
- 4.4 Numerical Challenges of Automatic Differentiation and Modern Libraries (113)
- 4.5 Further Readings & Recent Trends (118)

### 5장. Dense Map Representations (p.119)
- 5.1 Range Sensing Preliminaries (119)
- 5.2 Foundations of Dense Mapping (122)
- 5.3 Map Representations (126)
- 5.4 Constructing Maps: Methods and Practices (135)
- 5.5 Usage Considerations (145)

### 6장. Certifiably Optimal Solvers and Theoretical Properties of SLAM (p.149)
- 6.1 Certifiably Optimal Solvers for SLAM (150)
- 6.2 How Accurate is the Optimal Solution of a SLAM Problem? (173)
- 6.3 Further Readings & Recent Trends (178)

## Part II. SLAM in Practice

### Prelude II (p.185)
- II.1 Key Modules in the SLAM Front-End (185)
- II.2 Sensors and Factor Graphs (187)
- II.3 Evaluation (191)
- II.4 How to Read Part II? (192)

### 7장. Visual SLAM (p.193)
- 7.1 Historical Background and Terminology (193)
- 7.2 The Processing Pipeline of a Visual SLAM System (196)
- 7.3 Visual SLAM Fundamentals (197)
- 7.4 Further Considerations about Image Alignment and BA (207)
- 7.5 Examples of Full Visual SLAM Systems (215)
- 7.6 Real-time Dense Reconstruction (216)
- 7.7 SLAM with Depth-sensing Cameras (217)
- 7.8 Combining Vision with Other Modalities (219)
- 7.9 Further Readings & Recent Trends (222)

### 8장. LiDAR SLAM (p.224)
- 8.1 LiDAR Sensing Preliminaries and Categorization (225)
- 8.2 LiDAR Odometry (227)
- 8.3 LiDAR Place Recognition (236)
- 8.4 LiDAR SLAM (240)
- 8.5 Further Readings & Recent Trends (248)

### 9장. Radar SLAM (p.250)
- 9.1 Introduction to Radar (250)
- 9.2 Radar Odometry (261)
- 9.3 Radar Place Recognition (269)
- 9.4 Radar SLAM (273)
- 9.5 Radar Datasets (279)
- 9.6 Further Readings & Recent Trends (280)

### 10장. Event-based SLAM (p.282)
- 10.1 Sensor Description (282)
- 10.2 Challenges and Applications (286)
- 10.3 Overview and Taxonomy of Event-based SLAM Methods (287)
- 10.4 Front-end of an Event-based SLAM System (289)
- 10.5 Back-end of an Event-based SLAM System (293)
- 10.6 State-of-the-Art Systems (294)
- 10.7 Datasets, Simulators, and Benchmarks (294)
- 10.8 Further Readings & Recent Trends (302)

### 11장. Inertial Odometry for SLAM (p.304)
- 11.1 Basics of Inertial Sensing and Navigation (304)
- 11.2 IMU Preintegration and Factor Graphs (308)
- 11.3 Observability of Aided Inertial Navigation (319)
- 11.4 Visual-Inertial Odometry and Practical Considerations (326)
- 11.5 Further Readings & Recent Trends (330)

### 12장. Leg Odometry for SLAM (p.333)
- 12.1 Historical Background and Preliminaries (333)
- 12.2 Motion Estimation (342)
- 12.3 Contact Estimation (345)
- 12.4 Using Leg Odometry for State Estimation (348)
- 12.5 Open Challenges (353)
- 12.6 Further Readings & Recent Trends (355)

## Part III. From SLAM to Spatial AI

### Prelude III (p.361)
- III.1 Spatial Artificial Intelligence (361)
- III.2 Spatial AI Applications (362)
- III.3 How to Read Part III? (365)

### 13장. Boosting SLAM with Deep Learning (p.366)
- 13.1 Deep Learning for Depth and Camera Pose (368)
- 13.2 Deep Learning for Feature Matching and Optical Flow (374)
- 13.3 Differentiable Bundle Adjustment and DROID-SLAM (379)
- 13.4 DuSt3R (386)
- 13.5 MASt3R (392)
- 13.6 Extending MASt3R to SFM and SLAM (393)
- 13.7 Further Readings & Recent Trends (395)

### 14장. Map Representations with Differentiable Volume Rendering (p.397)
- 14.1 3D Scene Representation and Differentiable Rendering (398)
- 14.2 Neural Radiance Fields (NeRF) (401)
- 14.3 3D Gaussian Splatting (409)
- 14.4 Further Readings & Recent Trends (414)

### 15장. Dynamic and Deformable SLAM (p.417)
- 15.1 Characterizing the Dynamic SLAM Problem (418)
- 15.2 Short-term Dynamics and Dynamic SLAM (423)
- 15.3 Long-term Dynamic and Lifelong SLAM (432)
- 15.4 Deformable SLAM (446)
- 15.5 Further Readings & Recent Trends (451)

### 16장. Metric-Semantic SLAM (p.454)
- 16.1 From Traditional SLAM to Metric-Semantic SLAM (455)
- 16.2 Sparse Metric-Semantic Representations (456)
- 16.3 Dense Metric-Semantic Representations (471)
- 16.4 Hierarchical Metric-Semantic Representations and 3D Scene Graphs (482)
- 16.5 Further Readings & Recent Trends (487)

### 17장. Towards Open-World Spatial AI (p.490)
- 17.1 Background and Terminology (491)
- 17.2 Foundation Models for Spatial AI (495)
- 17.3 Open-World Mapping (499)
- 17.4 Further Readings & Recent Trends (514)

### 18장. The Computational Structure of Spatial AI Systems (p.521)
- 18.1 From SLAM to Spatial AI (521)
- 18.2 Overall Computational Structure (525)
- 18.3 State Estimation and Machine Learning in Spatial AI (526)
- 18.4 The Future Landscape of Processor and Sensor Hardware (528)
- 18.5 Mapping Spatial AI Graphs to Hardware (532)
- 18.6 Convergent Distributed Computation with Gaussian Belief Propagation (540)
- 18.7 Continual Learning within Factor Graphs (542)
- 18.8 Performance Metrics (545)
- 18.9 Further Readings & Recent Trends (547)

### Epilogue (p.548)
<!-- AUTO-TOC:END -->

---

## 추천 학습 순서

**책 순서를 그대로 따른다.** 편집자들이 서문에서 "chapters build on one another"라고
밝혔고, 처음 보는 사람에게는 의존성이 깔끔한 편이 낫다.

다만 책은 **어느 장이 어느 장을 전제하는지 알려주지 않는다.** 그래서 각 챕터 노트
상단에 의존성 블록을 둔다 (`2_Template_and_Rule.md` 의 "챕터 머리 블록").

| 단계 | 범위 | 왜 여기서 |
|---|---|---|
| 0 | Notation | 저자가 70명이라 표기가 흔들린다. 먼저 기준을 잡고 시작한다 |
| 1 | Prelude I + 1~6장 | **전체의 무게중심.** 뒤의 12장이 전부 여기 기댄다 |
| 2 | Prelude II + 7~12장 | 센서별 front-end. 1·2·11장의 팩터가 실제로 어떻게 만들어지는지 |
| 3 | Prelude III + 13~18장 + Epilogue | Spatial AI. 4장(미분가능 최적화)이 13장에서 회수된다 |

> 6장(Certifiably Optimal Solvers)이 Part I 에서 가장 어렵다. 1~4장을 끝낸 뒤에도
> 벽이면 5장으로 넘어갔다가 돌아와도 된다 — 7장 이후가 6장을 전제하지는 않는다.

---

## 목차 검증

목차는 **PDF 북마크에서 자동 생성**한다. 손으로 옮기지 않는다.

```bash
python3 _study_kit/tools/init_contents.py            # 화면에서 먼저 확인
python3 _study_kit/tools/init_contents.py --write    # AUTO-TOC 구간을 갱신
python3 _study_kit/tools/check_toc.py                # 원문과 대조 (불일치만 출력)
python3 _study_kit/tools/check_toc.py --verbose      # 맞은 항목까지 전부
```

`AUTO-TOC:START` ~ `END` 사이는 생성물이므로 **직접 고치지 않는다.** 그 바깥은 자유롭게 쓴다.

각 항목의 책 쪽번호를 `page_offset`(=16)으로 PDF 쪽으로 환산한 뒤, 그 쪽이나 다음 쪽에
그 절 제목이 **제목으로 조판돼 있는지** 확인한다. 전부 불일치로 나온다면 쪽번호가 아니라
판정 기준이 안 맞는 것이다 — `kit.conf` 의 `heading_size` · `header_y` 를 고친다.

```bash
python3 _study_kit/tools/check_toc.py --survey <PDF쪽>
```
