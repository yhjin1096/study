# 그림 파일명 매핑

챕터별로 `chN.txt` 를 만들어 `Figure/Table` 번호 ↔ 파일명 대응을 적는다.
`extract_figures.py --names tools/figure_names/chN.txt` 로 쓰며, **추출을 언제든 재현**할 수 있게 한다.

```
# 6장 — Figure/Table 파일명 매핑
# 사용: python3 tools/extract_figures.py --chapter 6 --pages 170-207 \
#         --out part1_xxx/06_chapter/images --names tools/figure_names/ch6.txt

Figure 6.1  = fig6_1_짧은_설명
Table 6.2   = table6_2_알고리즘_이름

# 캡션이 없어 스크립트로 잡히지 않는 그림은 직접 지정한 clip 좌표를 여기 주석으로 남긴다:
#   fig6_ex1_marker   PDF p.206, clip=(280, 200, 410, 275)   연습문제 1의 마커
```

파일명 규칙: `fig<장>_<번호>_<설명>.png`, `table<장>_<번호>_<설명>.png`
