# Probabilistic Robotics — 학습 목차 (EKF/UKF + Particle Filter 기반 Localization)

학습 목표: Bayes Filter 이론 → Gaussian Filters(KF/EKF/UKF/Information Filter) → Nonparametric
Filters(Histogram/Particle Filter) → Motion/Perception 모델 → Part II Localization(Markov/EKF/UKF
Localization, Grid/Monte Carlo Localization) 까지.

## 진행 상황 — **1~8장 전부 완료** (2026-08-15)

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 Introduction | ✅ | 2 | (7장 것 재사용) |
| 2 Recursive State Estimation | ✅ | 4 | bayes-stepper, continuous-belief, param-lab |
| 3 Gaussian Filters | ✅ | 14 | kalman-1d, ekf-linearization, ukf-sigma-points, information-filter |
| 4 Nonparametric Filters | ✅ | 11 | histogram-filter, log-odds, particle-filter |
| 5 Robot Motion | ✅ | 18 | velocity-motion, odometry-motion |
| 6 Robot Perception | ✅ | 20 | beam-model-mixture, likelihood-field, landmark-measurement |
| 7 Localization: Markov·Gaussian | ✅ | 21 | markov-1d-hallway, ekf-localization, ekf-vs-ukf-linearization |
| 8 Localization: Grid·Monte Carlo | ✅ | 28 | grid-vs-mcl-hallway, mcl-global-kidnapping, kld-sampling |

아래 목차의 **페이지 번호 145개는 원문과 대조 검증됨** (`_study_kit/tools/check_refs.py` 및 목차 대조).

> **다음에 갈 수 있는 곳** (이 스터디 범위 밖):
> **10장 EKF SLAM** 이 가장 자연스럽다 — 7.4절 EKF Localization의 상태 벡터에 랜드마크를 추가하면
> 그대로 SLAM이고, 5.2.1절에서 "$3+2N$ 차원"으로 이미 계산해 둔 그 벡터다.
> 그 밖에 9장 Occupancy Grid Mapping, 13장 FastSLAM(8.3절 MCL + 9장), 16·17장 계획·제어.

---

## Part I. Basics

### 1장. Introduction (p.3)
- 1.1 Uncertainty in Robotics (3)
- 1.2 Probabilistic Robotics (4)
- 1.3 Implications (9)
- 1.4 Road Map (10)
- 1.5 Teaching Probabilistic Robotics (11)
- 1.6 Bibliographical Remarks (11)

### 2장. Recursive State Estimation (p.13)
- 2.1 Introduction (13)
- 2.2 Basic Concepts in Probability (14)
- 2.3 Robot Environment Interaction (19)
  - 2.3.1 State (20)
  - 2.3.2 Environment Interaction (22)
  - 2.3.3 Probabilistic Generative Laws (24)
  - 2.3.4 Belief Distributions (25)
- 2.4 Bayes Filters (26)
  - 2.4.1 The Bayes Filter Algorithm (26)
  - 2.4.2 Example (28)
  - 2.4.3 Mathematical Derivation of the Bayes Filter (31)
  - 2.4.4 The Markov Assumption (33)
- 2.5 Representation and Computation (34)
- 2.6 Summary (35)
- 2.7 Bibliographical Remarks (36)
- 2.8 Exercises (36)

### 3장. Gaussian Filters (p.39)
- 3.1 Introduction (39)
- 3.2 The Kalman Filter (40)
  - 3.2.1 Linear Gaussian Systems (40)
  - 3.2.2 The Kalman Filter Algorithm (43)
  - 3.2.3 Illustration (44)
  - 3.2.4 Mathematical Derivation of the KF (45)
- 3.3 The Extended Kalman Filter (54)
  - 3.3.1 Why Linearize? (54)
  - 3.3.2 Linearization Via Taylor Expansion (56)
  - 3.3.3 The EKF Algorithm (59)
  - 3.3.4 Mathematical Derivation of the EKF (59)
  - 3.3.5 Practical Considerations (61)
- 3.4 The Unscented Kalman Filter (65)
  - 3.4.1 Linearization Via the Unscented Transform (65)
  - 3.4.2 The UKF Algorithm (67)
- 3.5 The Information Filter (71)
  - 3.5.1 Canonical Parameterization (71)
  - 3.5.2 The Information Filter Algorithm (73)
  - 3.5.3 Mathematical Derivation of the Information Filter (74)
  - 3.5.4 The Extended Information Filter Algorithm (75)
  - 3.5.5 Mathematical Derivation of the Extended Information Filter (76)
  - 3.5.6 Practical Considerations (77)
- 3.6 Summary (79)
- 3.7 Bibliographical Remarks (81)
- 3.8 Exercises (81)

### 4장. Nonparametric Filters (p.85)
- 4.1 The Histogram Filter (86)
  - 4.1.1 The Discrete Bayes Filter Algorithm (86)
  - 4.1.2 Continuous State (87)
  - 4.1.3 Mathematical Derivation of the Histogram Approximation (89)
  - 4.1.4 Decomposition Techniques (92)
- 4.2 Binary Bayes Filters with Static State (94)
- 4.3 The Particle Filter (96)
  - 4.3.1 Basic Algorithm (96)
  - 4.3.2 Importance Sampling (100)
  - 4.3.3 Mathematical Derivation of the PF (103)
  - 4.3.4 Practical Considerations and Properties of Particle Filters (104)
- 4.4 Summary (113)
- 4.5 Bibliographical Remarks (114)
- 4.6 Exercises (115)

### 5장. Robot Motion (p.117)
- 5.1 Introduction (117)
- 5.2 Preliminaries (118)
  - 5.2.1 Kinematic Configuration (118)
  - 5.2.2 Probabilistic Kinematics (119)
- 5.3 Velocity Motion Model (121)
  - 5.3.1 Closed Form Calculation (121)
  - 5.3.2 Sampling Algorithm (122)
  - 5.3.3 Mathematical Derivation of the Velocity Motion Model (125)
- 5.4 Odometry Motion Model (132)
  - 5.4.1 Closed Form Calculation (133)
  - 5.4.2 Sampling Algorithm (137)
  - 5.4.3 Mathematical Derivation of the Odometry Motion Model (137)
- 5.5 Motion and Maps (140)
- 5.6 Summary (143)
- 5.7 Bibliographical Remarks (145)
- 5.8 Exercises (145)

### 6장. Robot Perception (p.149)
- 6.1 Introduction (149)
- 6.2 Maps (152)
- 6.3 Beam Models of Range Finders (153)
  - 6.3.1 The Basic Measurement Algorithm (153)
  - 6.3.2 Adjusting the Intrinsic Model Parameters (158)
  - 6.3.3 Mathematical Derivation of the Beam Model (162)
  - 6.3.4 Practical Considerations (167)
  - 6.3.5 Limitations of the Beam Model (168)
- 6.4 Likelihood Fields for Range Finders (169)
  - 6.4.1 Basic Algorithm (169)
  - 6.4.2 Extensions (172)
- 6.5 Correlation-Based Measurement Models (174)
- 6.6 Feature-Based Measurement Models (176)
  - 6.6.1 Feature Extraction (176)
  - 6.6.2 Landmark Measurements (177)
  - 6.6.3 Sensor Model with Known Correspondence (178)
  - 6.6.4 Sampling Poses (179)
  - 6.6.5 Further Considerations (180)
- 6.7 Practical Considerations (182)
- 6.8 Summary (183)
- 6.9 Bibliographical Remarks (184)
- 6.10 Exercises (185)

---

## Part II. Localization

### 7장. Mobile Robot Localization: Markov and Gaussian (p.191)
- 7.1 A Taxonomy of Localization Problems (193)
- 7.2 Markov Localization (197)
- 7.3 Illustration of Markov Localization (200)
- 7.4 EKF Localization (201)
  - 7.4.1 Illustration (201)
  - 7.4.2 The EKF Localization Algorithm (203)
  - 7.4.3 Mathematical Derivation of EKF Localization (205)
  - 7.4.4 Physical Implementation (210)
- 7.5 Estimating Correspondences (215)
  - 7.5.1 EKF Localization with Unknown Correspondences (215)
  - 7.5.2 Mathematical Derivation of the ML Data Association (216)
- 7.6 Multi-Hypothesis Tracking (218)
- 7.7 UKF Localization (220)
  - 7.7.1 Mathematical Derivation of UKF Localization (220)
  - 7.7.2 Illustration (223)
- 7.8 Practical Considerations (229)
- 7.9 Summary (232)
- 7.10 Bibliographical Remarks (233)
- 7.11 Exercises (234)

### 8장. Mobile Robot Localization: Grid And Monte Carlo (p.237)
- 8.1 Introduction (237)
- 8.2 Grid Localization (238)
  - 8.2.1 Basic Algorithm (238)
  - 8.2.2 Grid Resolutions (239)
  - 8.2.3 Computational Considerations (243)
  - 8.2.4 Illustration (245)
- 8.3 Monte Carlo Localization (250)
  - 8.3.1 Illustration (250)
  - 8.3.2 The MCL Algorithm (252)
  - 8.3.3 Physical Implementations (253)
  - 8.3.4 Properties of MCL (253)
  - 8.3.5 Random Particle MCL: Recovery from Failures (256)
  - 8.3.6 Modifying the Proposal Distribution (261)
  - 8.3.7 KLD-Sampling: Adapting the Size of Sample Sets (263)
- 8.4 Localization in Dynamic Environments (267)
- 8.5 Practical Considerations (273)
- 8.6 Summary (274)
- 8.7 Bibliographical Remarks (275)
- 8.8 Exercises (276)

---

## 추천 학습 순서

1. 1장 (개괄, 가볍게)
2. 2장 (Bayes Filter 이론적 기반)
3. 3장 (Kalman Filter → EKF → UKF → Information Filter)
4. 4장 (Histogram Filter → Particle Filter)
5. 5장 (Velocity/Odometry Motion Model)
6. 6장 (Beam Model, Likelihood Field, Feature-Based Measurement Model)
7. 7장 (EKF/UKF Localization — Part I 내용의 실제 적용)
8. 8장 (Grid Localization, Monte Carlo Localization — Particle Filter의 실제 적용)
