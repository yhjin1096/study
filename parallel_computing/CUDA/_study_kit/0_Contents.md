# Programming Massively Parallel Processors (5th Edition) — 학습 목차

Wen-mei W. Hwu, David B. Kirk, Izzat El Hajj · Elsevier, 5판 (2027)
원본 PDF: `ref/Programming_Massively_Parallel_Processors.pdf` (673쪽 · 책 쪽번호 1~649)

학습 목표: CUDA C++ 로 GPU 커널을 처음부터 작성하는 것에서 시작해, GPU 아키텍처가
성능을 결정하는 방식(coalescing · occupancy · control divergence · bank conflict)을
이해하고, 그 위에서 reduction · scan · merge · sort 같은 병렬 패턴을 직접 구현한 뒤,
sparse matrix · graph · CNN · LLM attention 같은 실제 응용과 multi-GPU 프로그래밍까지 간다.

전 범위(1~24장 + 부록 A~C, 총 231개 절)를 대상으로 한다.

> 이 목차는 책에 인쇄된 Contents(PDF p.7~14)를 파싱해 만들었고,
> `_study_kit/tools/check_toc.py` 로 전 항목의 쪽번호를 원본과 대조해 확인했다.
> **쪽번호는 모두 책에 인쇄된 번호다** (PDF 쪽 아님 — 변환은 `kit.conf` 의 `page_offset` 참조).

## 진행 상황

| 장 | 노트 | 그림 | 위젯 |
|---|---|---|---|
| 1장 Introduction | ✅ | ✅ 2개 + Figure P.1 | ✅ amdahl |
| 2장 Heterogeneous data-parallel computing | ✅ | ✅ 15개 | ✅ thread-index |
| 3장 Multidimensional grids and data | ✅ | ✅ 13개 | ✅ grid-2d |
| 4장 Compute architecture and scheduling | ✅ | ✅ 10개 | ✅ occupancy |
| 5장 Memory architecture and data locality | ✅ | ✅ 14개 | ✅ roofline |
| 6장 Performance considerations | ✅ | ✅ 13개 | ✅ bank-conflict |
| 7장 Convolution | ✅ | ✅ 15개 | ✅ conv-tile |
| 8장 Stencil computation | ✅ | ✅ 12개 | ✅ stencil-ai |
| 9장 Histogram | ✅ | ✅ 15개 | ✅ atomic-contention |
| 10장 Reduction | ✅ | ✅ 21개 + 연습 삽화 1개 | ✅ reduction-efficiency |
| 11장 Scan | ✅ | ✅ 20개 | ✅ scan-work-span |
| 12장 Filter | ✅ | ✅ 11개 | ✅ warp-vote |
| 13장 Merge | ✅ | ✅ 20개 | ✅ co-rank |
| 14장 Sorting | ✅ | ✅ 13개 | ✅ radix-sort |
| 15장 Advanced optimizations for matrix multiplication | ⬜ | — | — |
| 16장 Dynamic programming and wavefront parallelism | ⬜ | — | — |
| 17장 Sparse matrix computation | ⬜ | — | — |
| 18장 Graph traversal | ⬜ | — | — |
| 19장 Convolutional neural networks | ⬜ | — | — |
| 20장 Large language models | ⬜ | — | — |
| 21장 Electrostatic potential map | ⬜ | — | — |
| 22장 Algorithm selection, problem decomposition, and problem formulation | ⬜ | — | — |
| 23장 Multi-GPU programming | ⬜ | — | — |
| 24장 Conclusion and future outlook | ⬜ | — | — |
| 부록 A. Numerical considerations | ⬜ | — | — |
| 부록 B. Deep learning basics | ⬜ | — | — |
| 부록 C. CUDA memories, address spaces, and pointers | ⬜ | — | — |

### 1장. Introduction (p.1)

- 1.1 Heterogeneous parallel computing (3)
- 1.2 Why more speed or parallelism? (7)
- 1.3 Speeding up real applications (9)
- 1.4 Challenges in parallel programming (11)
- 1.5 Related parallel programming interfaces (12)
- 1.6 Overarching goals (14)
- 1.7 Organization of the book (15)

---

## Part 1. Fundamental concepts


### 2장. Heterogeneous data-parallel computing (p.21)

- 2.1 Data parallelism (21)
- 2.2 CUDA C++ program structure (24)
- 2.3 A vector addition example (26)
- 2.4 Device global memory and data transfer (28)
- 2.5 Kernel functions and threading (32)
- 2.6 Calling kernel functions (37)
- 2.7 Compilation (39)
- 2.8 Summary (40)
- 2.9 Exercises (41)

### 3장. Multidimensional grids and data (p.45)

- 3.1 Multidimensional grid organization (45)
- 3.2 Mapping threads to MultiDimensional data (48)
- 3.3 Image blur -- a more complex kernel (55)
- 3.4 Matrix multiplication (59)
- 3.5 Summary (64)

### 4장. Compute architecture and scheduling (p.67)

- 4.1 Architecture of a modern GPU (68)
- 4.2 Thread block scheduling (69)
- 4.3 Synchronization and transparent scalability (70)
- 4.4 Warps and SIMD hardware (74)
- 4.5 Control divergence (79)
- 4.6 Warp scheduling and latency tolerance (82)
- 4.7 Resource partitioning and occupancy (85)
- 4.8 Querying device properties (87)
- 4.9 Summary (89)
- 4.10 Exercises (90)

### 5장. Memory architecture and data locality (p.93)

- 5.1 Memory bandwidth as a performance limiter (93)
- 5.2 CUDA memory types (98)
- 5.3 Tiling for reduced memory traffic (104)
- 5.4 A tiled matrix multiplication kernel (108)
- 5.5 Boundary checks (112)
- 5.6 Impact of memory usage on occupancy (115)
- 5.7 Summary (118)
- 5.8 Exercises (119)

### 6장. Performance considerations (p.123)

- 6.1 Global memory access coalescing (124)
- 6.2 Hiding memory latency (132)
- 6.3 Vector loads and stores (138)
- 6.4 Shared memory bank conflicts (139)
- 6.5 Thread coarsening (141)
- 6.6 Loop unrolling (144)
- 6.7 Double buffering (146)
- 6.8 A checklist of optimizations (147)
- 6.9 Optimization strategy (153)
- 6.10 Summary (154)
- 6.11 Exercises (154)

---

## Part 2. Parallel patterns


### 7장. Convolution (p.159)

- 7.1 Background (159)
- 7.2 Parallel convolution -- a basic kernel (164)
- 7.3 Memory bandwidth considerations (167)
- 7.4 Constant memory and caching (168)
- 7.5 Tiled convolution with halo cells (172)
- 7.6 Tiled convolution using caches for halo cells (178)
- 7.7 Summary (179)
- 7.8 Exercises (180)

### 8장. Stencil computation (p.183)

- 8.1 Background (184)
- 8.2 Parallel stencil -- a basic kernel (187)
- 8.3 Memory bandwidth considerations (189)
- 8.4 Shared-memory tiling for stencil sweep (189)
- 8.5 Thread coarsening (193)
- 8.6 Register tiling (196)
- 8.7 Summary (198)
- 8.8 Exercises (198)

### 9장. Histogram (p.201)

- 9.1 Background (202)
- 9.2 Atomic operations and a basic histogram kernel (203)
- 9.3 Latency and throughput of atomic operations (209)
- 9.4 Privatization (211)
- 9.5 Thread coarsening (214)
- 9.6 Thread-level privatization (217)
- 9.7 Summary (219)
- 9.8 Exercises (220)

### 10장. Reduction (p.221)

- 10.1 Background (221)
- 10.2 Reduction trees (223)
- 10.3 A simple reduction kernel (227)
- 10.4 Reducing control divergence (230)
- 10.5 Reducing memory access divergence (234)
- 10.6 Reducing global memory accesses (236)
- 10.7 Reducing synchronization overhead with warp-level primitives (237)
- 10.8 Further reducing synchronization overhead with two-stage warp-wide reduction (241)
- 10.9 Reduction for arbitrary length inputs (244)
- 10.10 Thread coarsening to reduce overhead (246)
- 10.11 Summary (249)
- 10.12 Exercises (249)

### 11장. Scan (p.251)

- 11.1 Background (252)
- 11.2 Parallel scan with the Kogge-Stone algorithm (254)
- 11.3 Double-buffering to reduce synchronization (258)
- 11.4 Warp-level primitives to reduce synchronization (261)
- 11.5 Work efficiency considerations (265)
- 11.6 Coarsening to improve work-efficiency (267)
- 11.7 Register tiling to avoid shared memory access latency (270)
- 11.8 Memory bandwidth considerations (272)
- 11.9 Consolidating block segments for a global scan (273)
- 11.10 Parallel scan with the Brent-Kung algorithm (282)
- 11.11 Summary (285)
- 11.12 Exercises (286)

### 12장. Filter (p.289)

- 12.1 Background (289)
- 12.2 A simple parallel unstable filter (290)
- 12.3 Coalescing atomic operations with warp-level primitives (291)
- 12.4 Privatization (295)
- 12.5 A simple parallel stable filter (297)
- 12.6 Improving memory coalescing with shared memory and thread coarsening (298)
- 12.7 In-place stable filter (300)
- 12.8 Related patterns (301)
- 12.9 Summary (302)
- 12.10 Exercises (302)

### 13장. Merge (p.303)

- 13.1 Background (303)
- 13.2 A sequential merge algorithm (305)
- 13.3 A parallelization approach (306)
- 13.4 Co-rank function implementation (308)
- 13.5 A basic parallel merge kernel (313)
- 13.6 A tiled merge kernel to improve coalescing (314)
- 13.7 A circular-buffer merge kernel (321)
- 13.8 Thread coarsening for merge (327)
- 13.9 Summary (327)
- 13.10 Exercises (327)

### 14장. Sorting (p.329)

- 14.1 Background (330)
- 14.2 Parallel odd-even sort (331)
- 14.3 Parallel merge sort (333)
- 14.4 Radix sort (334)
- 14.5 Parallel radix sort (336)
- 14.6 Optimizing for memory coalescing (339)
- 14.7 Choice of radix value (342)
- 14.8 Thread coarsening to improve coalescing (344)
- 14.9 Other parallel sort methods (345)
- 14.10 Summary (346)
- 14.11 Exercises (347)

### 15장. Advanced optimizations for matrix multiplication (p.349)

- 15.1 Background (349)
- 15.2 Data reuse analysis (350)
- 15.3 Using larger tiles with thread coarsening (352)
- 15.4 Register tiling of the input tiles (357)
- 15.5 Coalesced storing of the output tile (360)
- 15.6 Eliminating bank conflicts (361)
- 15.7 Occupancy considerations (363)
- 15.8 Software pipelining (364)
- 15.9 Specialized software and hardware support (368)
- 15.10 Summary (370)
- 15.11 Exercises (370)

---

## Part 3. Advanced patterns and applications


### 16장. Dynamic programming and wavefront parallelism (p.373)

- 16.1 Dynamic programming (373)
- 16.2 Implementation approaches (374)
- 16.3 Wavefront patterns (376)
- 16.4 Floyd-Warshall algorithm (377)
- 16.5 Genome sequence alignment and Smith-Waterman algorithm (382)
- 16.6 Wavefront parallelization: block-level tiling (384)
- 16.7 Hyperplane transformation (389)
- 16.8 More optimizations (397)
- 16.9 Summary (399)
- 16.10 Exercises (399)

### 17장. Sparse matrix computation (p.401)

- 17.1 Background (402)
- 17.2 A simple SpMV kernel with the COO format (404)
- 17.3 Grouping row non-zeros with the CSR format (407)
- 17.4 Improving memory coalescing with the ELL format (410)
- 17.5 Regulating padding with the hybrid ELL-COO format (414)
- 17.6 Reducing control divergence with the JDS format (416)
- 17.7 Column-wise accessibility with the CSC format (418)
- 17.8 Summary (421)
- 17.9 Exercises (422)

### 18장. Graph traversal (p.425)

- 18.1 Background (425)
- 18.2 Breadth-first search (429)
- 18.3 Vertex-centric parallelization of BFS (431)
- 18.4 Edge-centric parallelization of BFS (436)
- 18.5 Improving work efficiency with frontiers (438)
- 18.6 Reducing contention with privatization (442)
- 18.7 Reducing launch overhead with cooperative groups (445)
- 18.8 Other optimizations (448)
- 18.9 Summary (449)
- 18.10 Exercises (449)

### 19장. Convolutional neural networks (p.453)

- 19.1 Convolutional neural networks (454)
- 19.2 A CUDA convolutional layer kernel (460)
- 19.3 Formulating convolutional layer as GEMM (463)
- 19.4 CUDNN library (472)
- 19.5 Summary (474)
- 19.6 Exercises (474)

### 20장. Large language models (p.477)

- 20.1 Transformer architecture (478)
- 20.2 Multi-head attention (482)
- 20.3 Implementing attention in CUDA (486)
- 20.4 KV caching (488)
- 20.5 Flash attention (492)
- 20.6 KV cache arithmetic intensity and memory requirement (504)
- 20.7 Alleviating the memory requirements of the attention mechanism (508)
- 20.8 Summary (510)
- 20.9 Exercises (511)

### 21장. Electrostatic potential map (p.513)

- 21.1 Background (513)
- 21.2 Scatter vs. gather in kernel design (515)
- 21.3 Thread coarsening (519)
- 21.4 Memory coalescing (521)
- 21.5 Cutoff binning for data size scalability (523)
- 21.6 Summary (527)
- 21.7 Exercises (528)

### 22장. Algorithm selection, problem decomposition, and problem formulation (p.529)

- 22.1 Algorithm selection (530)
- 22.2 Problem decomposition (532)
- 22.3 Application level considerations -- Amdahl’s law (537)
- 22.4 Problem formulation (538)
- 22.5 Batching: latency vs. throughput (539)
- 22.6 Summary (540)

### 23장. Multi-GPU programming (p.541)

- 23.1 Stencil as a running example (542)
- 23.2 Multi-GPU stencil with MPI (545)
- 23.3 Overlapping computation and communication (553)
- 23.4 Multi-GPU stencil with NCCL (563)
- 23.5 Multi-GPU stencil with NVSHMEM (568)
- 23.6 Summary (574)
- 23.7 Exercises (576)

### 24장. Conclusion and future outlook (p.577)

- 24.1 Goals revisited (577)
- 24.2 Future outlook (578)

---

## Part 4. Appendices


### 부록 A. Numerical considerations (p.583)

- A.1 Floating-point data representation (583)
- A.2 Representable numbers (586)
- A.3 Precision and special bit patterns in IEEE format (590)
- A.4 Arithmetic accuracy and rounding (591)
- A.5 Lower-precision formats (592)
- A.6 Algorithm considerations (593)
- A.7 Linear solvers and numerical stability (594)
- A.8 Summary (599)
- A.9 Exercises (599)

### 부록 B. Deep learning basics (p.601)

- B.1 Classifiers (602)
- B.2 Fully connected and convolutional layers (605)
- B.2.1 Training models (606)
- B.3 Convolutional neural networks (612)
- B.4 CNN inference and training: sequential implementation (613)
- B.4.1 CNN training (616)
- B.5 Summary (621)

### 부록 C. CUDA memories, address spaces, and pointers (p.623)

- C.1 Unified device memory address space (624)
- C.2 Zero-copy access to host memory (624)
- C.3 Unified virtual address space (625)
- C.4 Large virtual and physical GPU address spaces (625)
- C.5 Unified physical address space (626)
- C.6 Unified memory (626)
- C.7 Access to full host virtual address space (627)
- C.8 Page fault handling (628)
- C.9 Virtual address space control (629)

---

## 추천 학습 순서

기본은 **책 순서를 그대로 따른다.** 이 책은 앞 장의 기법을 뒤 장에서 계속 다시 쓰는
누적 구조라 의존성이 깔끔하고, 건너뛰면 뒤에서 반드시 되돌아오게 된다.

1. **1장 Introduction** — 책 전체 지도. 왜 GPU인가, 무엇을 배우게 되는가
2. **2장 Heterogeneous data-parallel computing** — 첫 CUDA 커널. host/device 분리와 메모리 전송
3. **3장 Multidimensional grids and data** — grid/block을 다차원 데이터에 대응시키는 법
4. **4장 Compute architecture and scheduling** — warp·SM·occupancy — 하드웨어가 스레드를 어떻게 굴리는가
5. **5장 Memory architecture and data locality** — tiling과 shared memory. 이 책의 핵심 기법이 처음 나온다
6. **6장 Performance considerations** — coalescing·bank conflict·coarsening. 최적화 도구상자
7. **7장 Convolution** — constant memory와 halo. tiling의 첫 응용
8. **8장 Stencil computation** — stencil. register tiling이 추가된다
9. **9장 Histogram** — atomic과 privatization — 경쟁을 다루는 법
10. **10장 Reduction** — reduction tree와 divergence 제거. warp-level primitive 등장
11. **11장 Scan** — scan. work efficiency라는 개념이 본격적으로 나온다
12. **12장 Filter** — filter. warp voting과 atomic coalescing
13. **13장 Merge** — merge. co-rank라는 독특한 병렬화 아이디어
14. **14장 Sorting** — radix sort. coalescing 최적화의 종합
15. **15장 Advanced optimizations for matrix multiplication** — matmul 재방문. 5·6장의 기법을 전부 동원한다
16. **16장 Dynamic programming and wavefront parallelism** — dynamic programming의 wavefront 병렬화
17. **17장 Sparse matrix computation** — sparse matrix. 자료구조 선택이 성능을 지배하는 사례
18. **18장 Graph traversal** — graph BFS. frontier와 cooperative groups
19. **19장 Convolutional neural networks** — CNN을 GEMM으로 바꾸는 정식화
20. **20장 Large language models** — LLM attention·KV cache·Flash Attention (5·6·15장 선행 필요)
21. **21장 Electrostatic potential map** — scatter vs gather. 커널 설계 관점의 사례 연구
22. **22장 Algorithm selection, problem decomposition, and problem formulation** — 알고리즘 선택과 문제 분해 — 코드가 아닌 설계 이야기
23. **23장 Multi-GPU programming** — MPI/NCCL/NVSHMEM으로 GPU 여러 장 쓰기
24. **24장 Conclusion and future outlook** — 마무리와 전망
25. **부록 A. Numerical considerations** — floating-point와 수치 안정성
26. **부록 B. Deep learning basics** — 딥러닝 기초 (19·20장 배경지식)
27. **부록 C. CUDA memories, address spaces, and pointers** — unified memory와 주소 공간

### 저자가 제시한 의존 관계 (Figure P.1, 책 p.xxiii)

저자가 머리말에 장 사이 의존 관계를 그림으로 그려 두었다. 아래는 그 그림을 옮긴 것이다.

```
Part I   1 → 2 → { 3, 4 } → 5 → 6            (여기까지는 사실상 일직선)

Part II  6 ─┬→ 7 ─┬→ 8
            │     └────────────────→ 19      (Part III)
            ├→ 9 ─┬⇢ 10                      (⇢ 는 점선 = 약한 의존)
            │     ├→ 11
            │     └────────────────→ 16      (Part III)
            ├→ 10 → 11 → 12 → 14
            ├→ 13 ──────────→ 14
            └→ 15                            (여기서 끝. 나가는 화살표 없음)
                    8 ──────────────→ 23      (Part III)
                   14 ─┬──────────→ 17
                       └──────────→ 21

Part III 17 → 18 ─┐
         16 ──────┼→ 22
         21 ──────┘
         19 → 20
         24 (마지막)
```

읽는 법: **6장이 Part II 전체의 관문이다.** 7·9·10·13·15장이 모두 6장에서 갈라져 나온다.
그리고 Part III 의 각 응용 장은 Part II 의 특정 패턴 하나에 붙어 있다 —
19장(CNN)은 7장(convolution)에, 23장(multi-GPU)은 8장(stencil)에,
16장(DP)은 9장에, 17·21장은 14장(sort)에.

> **주의**: 이 그림은 5판에서 일부 갱신이 안 된 것으로 보인다. 상자의 제목이
> 인쇄된 목차와 다른 곳이 있다 (12장 "Filtering" → 실제 "Filter", 22장
> "Problem Decomposition" → 실제 "Algorithm selection, problem decomposition,
> and problem formulation", 23장 "Programming a Heterogeneous Cluster" → 실제
> "Multi-GPU programming"). 의존 관계 자체는 유효하지만 제목은 목차를 따른다.

### 그래서 어떻게 읽을 것인가

- **1~6장은 순서대로 반드시.** 여기가 나머지 전부의 토대다. 특히 5장(tiling)과
  6장(coalescing · coarsening)의 기법이 7장 이후 거의 모든 장에서 반복된다.
  3장과 4장은 서로 독립이라 순서를 바꿔도 되지만, 굳이 그럴 이유는 없다.
- **7~15장(패턴 장)은 6장만 끝냈으면 어느 것부터 시작해도 된다.** 다만 위 그림의
  사슬은 지킨다 — `9 → 10 → 11 → 12 → 14` 와 `13 → 14`, `7 → 8`.
  15장(matmul 재방문)은 어디에도 걸리지 않으니 6장 직후에 읽어도 좋다.
  5장의 tiled matmul 이 아직 머리에 있을 때 읽으면 오히려 낫다.
- **Part III 는 짝지어 읽는다.** 응용 장 하나를 그 뿌리가 되는 패턴 장 바로 뒤에
  붙이면 "이 패턴이 실제로 어디 쓰이나"가 바로 이어진다.
  예: `7 → 8 → 23` 또는 `7 → 19 → 20`.
- **20장(LLM)은 5 · 6 · 15장을 먼저 본 뒤에.** Flash Attention 이 tiling 과
  software pipelining 위에 서 있어서, 그 전에 읽으면 결론만 외우게 된다.
  딥러닝 배경이 얕다면 부록 B 를 19장 앞에 끼워 넣는다.
- **부록은 필요할 때 꺼내 본다.** A(수치)는 언제든, B(딥러닝)는 19장 전에,
  C(주소 공간)는 23장 전에 보면 좋다.

---

## 목차 검증

이 파일의 쪽번호가 실제 PDF 와 맞는지 대조한다.

```bash
python3 _study_kit/tools/check_toc.py           # 불일치만 출력
python3 _study_kit/tools/check_toc.py --verbose # 맞은 항목까지 전부
```

각 항목의 책 쪽번호를 PDF 쪽으로 환산한 뒤, 그 쪽(또는 다음 쪽)에 그 절 제목이
실제로 조판돼 있는지 확인한다. **이 책은 `page_offset` 이 구간마다 다르므로**
(28 → 24) 손으로 환산하지 말고 스크립트나 `--book-pages` 옵션을 쓴다.
