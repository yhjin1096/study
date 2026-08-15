# Notes on Kalman Filter (KF, EKF, ESKF, IEKF, IESKF) — 학습 목차

원문: Gyubeom Edward Im, *Notes on Kalman Filter (KF, EKF, ESKF, IEKF, IESKF)* (49쪽)
`ref/Notes on Kalman Filter(KF, EKF, ESKF, IEKF, IESKF).pdf` · 페이지 오프셋 0

학습 목표: 추정 이론과 recursive bayes filter에서 출발해 KF → EKF → ESKF → IEKF → IESKF로 이어지는
다섯 필터의 식을 유도까지 따라가고, MAP·Gauss-Newton과의 관계로 전체를 하나로 묶는다.

> **결과물은 챕터별 노트가 아니라 원문 전체를 그대로 옮긴 단일 문서다.**
> `notes/notes_on_kalman_filter.md` 하나에 13개 장이 모두 들어 있고, 빌드하면 같은 폴더에
> `notes_on_kalman_filter.html`이 나온다. 위젯 11개가 절 사이에 삽입되어 있다.

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1 Preliminaries | ✅ | 6 (p.3~6) | — |
| 2 Recursive bayes filter | ✅ | 1 (p.7) | 1 (bayes filter) |
| 3 Kalman filter (KF) | ✅ | 3 (p.10, p.13×2) | 3 (1D KF, 칼만 게인, 2D 추적) |
| 4 Extended kalman filter (EKF) | ✅ | 1 (p.15) | 1 (선형화 오차) |
| 5 Error-state kalman filter (ESKF) | ✅ | 1 (p.18) | 1 (nominal+error·reset) |
| 6 Iterated extended kalman filter (IEKF) | ✅ | 1 (p.23) | 1 (반복 보정) |
| 7 Iterated error-state kalman filter (IESKF) | ✅ | 1 (p.26) | 1 (IESKF vs IEKF) |
| 8 Derivation of Kalman filter | ✅ | 2 (p.32, p.38) | 1 (두 가우시안의 곱) |
| 9 MAP, GN, and EKF relationship | ✅ | — | 1 (MAP→GN→EKF) |
| 10 Derivation of IESKF update step | ✅ | 2 (p.45) | — |
| 11 Wrap-up | ✅ | 5 (p.46~48) | 1 (다섯 필터 비교) |
| 12 Reference | ✅ | — | — |
| 13 Revision log | ✅ | — | — |

---

## 1장. Preliminaries (p.3)
- 1.1 Estimation theory (3)
- 1.2 Bayesian philosophy (3)
- 1.3 Estimation problem (4)
- 1.4 Dynamic system (5)

## 2장. Recursive bayes filter (p.6)
- 2.1 Derivation of recursive bayes filter (7)
- 2.2 Gaussian belief case (9)

## 3장. Kalman filter (KF) (p.10)
- 3.1 Prediction step (11)
- 3.2 Correction step (11)
- 3.3 1D Kalman filter (12)
- 3.4 Discussion (13)
  - 3.4.1 Discussion about KF and posterior pdf (13)
  - 3.4.2 Discussion about Kalman gain (14)
- 3.5 Summary (15)

## 4장. Extended kalman filter (EKF) (p.15)
- 4.1 Prediction step (17)
- 4.2 Correction step (17)
- 4.3 Summary (18)

## 5장. Error-state kalman filter (ESKF) (p.18)
- 5.1 Prediction step (21)
- 5.2 Correction step (22)
  - 5.2.1 Reset (22)
- 5.3 Summary (22)

## 6장. Iterated extended kalman filter (IEKF) (p.23)
- 6.1 Compare to EKF (23)
  - 6.1.1 Commonality 1 (23)
  - 6.1.2 Commonality 2 (24)
  - 6.1.3 Commonality 3 (24)
  - 6.1.4 Difference 1 (24)
  - 6.1.5 Difference 2 (24)
- 6.2 Prediction step (25)
- 6.3 Correction step (25)
- 6.4 Summary (25)

## 7장. Iterated error-state kalman filter (IESKF) (p.26)
- 7.1 Compare to ESKF (27)
  - 7.1.1 Commonality 1 (27)
  - 7.1.2 Commonality 2 (27)
  - 7.1.3 Commonality 3 (27)
  - 7.1.4 Difference (MAP-based derivation) (28)
- 7.2 Prediction step (29)
- 7.3 Correction step (29)
- 7.4 Summary (30)

## 8장. Derivation of Kalman filter (p.31)
- 8.1 Derivation of KF prediction step (31)
- 8.2 Derivation of KF update step (ver. 1) (36)
- 8.3 Derivation of KF update step (ver. 2) (38)

## 9장. MAP, GN, and EKF relationship (p.38)
- 9.1 Traditional EKF derivation (38)
- 9.2 MAP-based EKF derivation (39)
  - 9.2.1 Start from MAP estimator (39)
  - 9.2.2 MLE of new observation function (40)
  - 9.2.3 Gauss-Newton Optimization (41)

## 10장. Derivation of IESKF update step (p.43)

## 11장. Wrap-up (p.45)
- 11.1 Kalman Filter (KF) (46)
- 11.2 Extended Kalman Filter (EKF) (46)
- 11.3 Error-state Kalman Filter (ESKF) (47)
- 11.4 Iterated Extended Kalman Filter (IEKF) (47)
- 11.5 Iterated Error-state Kalman Filter (IESKF) (48)

## 12장. Reference (p.48)

## 13장. Revision log (p.49)

---

## 추천 학습 순서

원문 순서 그대로. 1 → 11로 곧게 흐르되, 유도(8~10장)는 뒤로 미뤄도 된다.

1. **1~3장** — 추정 이론 → bayes filter → KF. 여기서 3.3의 1D 버전과 3.4의 두 Discussion이 직관의 핵심
2. **4~7장** — EKF → ESKF → IEKF → IESKF. 네 장이 같은 골격(Compare / Prediction / Correction /
   Summary)이라 **무엇이 달라지는지**만 따라가면 된다
3. **8장** — KF 식이 어디서 나오는지. ver.1(직접 전개)과 ver.2(조건부 가우시안) 두 길이 있는데
   ver.2가 훨씬 짧다
4. **9장** — MAP → GN → EKF. "EKF는 GN 1회"라는 결론이 4~7장 전체를 하나로 묶는다
5. **10~11장** — IESKF 업데이트 유도와 한 장짜리 요약

## 참고 — 이 문서의 특이사항

- **그림 캡션이 하나도 없다.** `Figure`/`Table`이 전문에 0회. `extract_figures.py` 대신
  `tools/extract_images_bbox.py`(이미지 bbox 기반)로 24개를 뽑는다
- 번호 붙은 수식이 (1)~(166)까지 있다. 노트가 이를 그대로 유지하므로 원문 PDF와 나란히 볼 수 있다
- 8장은 3장과 $\mathbf{Q}_t$·$\mathbf{R}_t$의 역할이 서로 바뀌어 있다(8장 안에서는 일관됨).
  노트 맨 아래 "원문 그대로 둔 것" 참조
- 식 (71)의 반복 갱신이 (94)·(158)과 다르다. 위젯(실험 7·8)이 세 식을 나란히 돌려 보여준다
