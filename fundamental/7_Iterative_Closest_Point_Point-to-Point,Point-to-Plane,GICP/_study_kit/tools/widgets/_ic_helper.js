// ============================================================================
//  window.IC — Notes on Iterative Closest Point 스터디 위젯 공용 헬퍼
//
//  헬퍼 계보:  LG(Lie Theory) → PI(Preintegration) → VM(VINS-Mono)
//              → EJ(Errors and Jacobians) → IC(여기)
//
//  위쪽 대부분은 물려받은 것이다. 이 스터디에서 더한 것은 파일 맨 아래
//  "Iterative Closest Point 스터디에서 더한 것" 구획에 모여 있다:
//    · 실수 대칭행렬 고유분해(Jacobi) 와 그 위에 세운 SVD
//    · 원문 2·3장의 예제 점군 데이터 (그대로 옮긴 것)
//    · 최근접 탐색 / centroid / 공분산 C = p'_t p'^T_{t+1}
//    · SVD 닫힌 해 (식 26·27), point-to-point GN 2D/3D (식 32·43)
//    · 법선 추정 (2D 식 52 아래 / 3D PCA), point-to-plane GN (식 55·66)
//    · GICP 공분산 (식 88·89), 마할라노비스 GN (식 98)
// ============================================================================

window.IC = (function () {
    // ---- 일반 행렬 ------------------------------------------------------
    function zeros(r, c) { var M = []; for (var i = 0; i < r; i++) M.push(new Array(c).fill(0)); return M; }
    function eye(n) { var M = zeros(n, n); for (var i = 0; i < n; i++) M[i][i] = 1; return M; }
    function mm(A, B) {
      var r = A.length, c = B[0].length, k2 = B.length, C = zeros(r, c);
      for (var i = 0; i < r; i++) for (var j = 0; j < c; j++) {
        var s = 0; for (var k = 0; k < k2; k++) s += A[i][k]*B[k][j]; C[i][j] = s;
      }
      return C;
    }
    function mT(A) { var C = zeros(A[0].length, A.length);
      for (var i = 0; i < A.length; i++) for (var j = 0; j < A[0].length; j++) C[j][i] = A[i][j];
      return C; }
    function madd(A, B) { return A.map(function (r, i) { return r.map(function (v, j) { return v + B[i][j]; }); }); }
    function msub(A, B) { return A.map(function (r, i) { return r.map(function (v, j) { return v - B[i][j]; }); }); }
    function mscale(A, k) { return A.map(function (r) { return r.map(function (v) { return v*k; }); }); }
    function mv(A, v) { return A.map(function (r) { var s = 0; for (var j = 0; j < v.length; j++) s += r[j]*v[j]; return s; }); }
    function minv(A) {                                    // 가우스-조던
      var n = A.length, M = A.map(function (r, i) { return r.concat(eye(n)[i]); });
      for (var c = 0; c < n; c++) {
        var p = c;
        for (var r2 = c + 1; r2 < n; r2++) if (Math.abs(M[r2][c]) > Math.abs(M[p][c])) p = r2;
        if (Math.abs(M[p][c]) < 1e-14) return eye(n);
        var tmp = M[c]; M[c] = M[p]; M[p] = tmp;
        var d = M[c][c];
        for (var j = 0; j < 2*n; j++) M[c][j] /= d;
        for (var r3 = 0; r3 < n; r3++) if (r3 !== c) {
          var f = M[r3][c];
          if (f) for (var j2 = 0; j2 < 2*n; j2++) M[r3][j2] -= f*M[c][j2];
        }
      }
      return M.map(function (r) { return r.slice(n); });
    }
    function mmaxabs(A) { var m = 0; A.forEach(function (r) { r.forEach(function (v) { m = Math.max(m, Math.abs(v)); }); }); return m; }
    function blk(TL, TR, BL, BR) {                        // 3×3 넷 → 6×6
      var M = zeros(6, 6);
      for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
        M[i][j] = TL[i][j]; M[i][j+3] = TR[i][j]; M[i+3][j] = BL[i][j]; M[i+3][j+3] = BR[i][j];
      }
      return M;
    }

    // ---- 벡터 -----------------------------------------------------------
    function nrm(v) { var s = 0; for (var i = 0; i < v.length; i++) s += v[i]*v[i]; return Math.sqrt(s); }
    function unit(v) { var n = nrm(v) || 1; return v.map(function (x) { return x/n; }); }
    function add(a, b) { return a.map(function (v, i) { return v + b[i]; }); }
    function sub(a, b) { return a.map(function (v, i) { return v - b[i]; }); }
    function sc(a, k) { return a.map(function (v) { return v*k; }); }
    function dot(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]*b[i]; return s; }
    function cross(a, b) { return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]; }
    function axis(azDeg, elDeg) {
      var a = azDeg*Math.PI/180, e = elDeg*Math.PI/180;
      return [Math.cos(e)*Math.cos(a), Math.cos(e)*Math.sin(a), Math.sin(e)];
    }

    // ---- so(3) / SO(3) --------------------------------------------------
    function hat(w) { return [[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]]; }   // 식 (17)(32)
    function vee(W) { return [W[2][1], W[0][2], W[1][0]]; }
    function expSO3(w) {                                  // 식 (27) 로드리게스
      var t = nrm(w), W = hat(w);
      if (t < 1e-10) return madd(eye(3), madd(W, mscale(mm(W, W), 0.5)));
      return madd(eye(3), madd(mscale(W, Math.sin(t)/t), mscale(mm(W, W), (1 - Math.cos(t))/(t*t))));
    }
    function logSO3(R) {                                  // 식 (28)
      var tr = (R[0][0] + R[1][1] + R[2][2] - 1)/2;
      var t = Math.acos(Math.max(-1, Math.min(1, tr)));
      if (t < 1e-8) return sc(vee(msub(R, mT(R))), 0.5);
      if (Math.PI - t < 1e-6) {                           // θ≈π — 대칭 성분에서 축을 뽑는다
        var S = mscale(madd(R, eye(3)), 0.5), best = 0, bi = 0;
        for (var i = 0; i < 3; i++) if (S[i][i] > best) { best = S[i][i]; bi = i; }
        var u = unit([S[0][bi], S[1][bi], S[2][bi]]);
        var dsym = vee(msub(R, mT(R)));                   // 부호는 반대칭 성분으로 가린다
        if (dot(dsym, u) < 0) u = sc(u, -1);
        return sc(u, t);
      }
      return sc(vee(msub(R, mT(R))), t/(2*Math.sin(t)));
    }
    function JrSO3(w) {                                   // 식 (48) 오른쪽 자코비안
      var t = nrm(w), W = hat(w);
      if (t < 1e-8) return msub(eye(3), mscale(W, 0.5));
      return madd(msub(eye(3), mscale(W, (1 - Math.cos(t))/(t*t))),
                  mscale(mm(W, W), (t - Math.sin(t))/(t*t*t)));
    }
    function JlSO3(w) { return mT(JrSO3(w)); }            // 식 (50)
    function JinvCoef(t) {                                // 1/θ² − (1+cosθ)/(2θ sinθ)
      if (t < 1e-4) return 1/12 + t*t/720;
      return 1/(t*t) - (1 + Math.cos(t))/(2*t*Math.sin(t));
    }
    function JlInvSO3(w) {                                // 식 (65)
      var t = nrm(w), W = hat(w);
      return madd(msub(eye(3), mscale(W, 0.5)), mscale(mm(W, W), JinvCoef(t)));
    }
    function JrInvSO3(w) {                                // 식 (48) 주석
      var t = nrm(w), W = hat(w);
      return madd(madd(eye(3), mscale(W, 0.5)), mscale(mm(W, W), JinvCoef(t)));
    }
    function AdSO3(R) { return R; }                       // 식 (46)

    // ---- se(3) / SE(3) --------------------------------------------------
    // ξ = [ω; v] (회전 먼저) — 원문 식 (55) 의 순서
    function T(R, t) {
      return [[R[0][0], R[0][1], R[0][2], t[0]],
              [R[1][0], R[1][1], R[1][2], t[1]],
              [R[2][0], R[2][1], R[2][2], t[2]],
              [0, 0, 0, 1]];
    }
    function TR(M) { return [[M[0][0], M[0][1], M[0][2]], [M[1][0], M[1][1], M[1][2]], [M[2][0], M[2][1], M[2][2]]]; }
    function Tt(M) { return [M[0][3], M[1][3], M[2][3]]; }
    function Tinv(M) {                                    // 식 (52)
      var R = TR(M), Rt = mT(R);
      return T(Rt, sc(mv(Rt, Tt(M)), -1));
    }
    function expSE3(xi) {                                 // 식 (64)
      var w = [xi[0], xi[1], xi[2]], v = [xi[3], xi[4], xi[5]];
      return T(expSO3(w), mv(JlSO3(w), v));
    }
    function logSE3(M) {                                  // 식 (67)
      var w = logSO3(TR(M)), v = mv(JlInvSO3(w), Tt(M));
      return [w[0], w[1], w[2], v[0], v[1], v[2]];
    }
    function AdSE3(M) {                                   // 식 (73)
      var R = TR(M), t = Tt(M);
      return blk(R, zeros(3, 3), mm(hat(t), R), R);
    }
    function QlSE3(xi) {                                  // 식 (78)
      var w = [xi[0], xi[1], xi[2]], v = [xi[3], xi[4], xi[5]];
      var t = nrm(w), W = hat(w), V = hat(v), W2 = mm(W, W);
      var c1, c2, c3;
      if (t < 1e-4) { c1 = 1/6; c2 = -1/24; c3 = -1/120; }
      else {
        c1 = (t - Math.sin(t))/(t*t*t);
        c2 = (t*t + 2*Math.cos(t) - 2)/(2*t*t*t*t);
        c3 = (2*t - 3*Math.sin(t) + t*Math.cos(t))/(2*Math.pow(t, 5));
      }
      var A = madd(madd(mm(W, V), mm(V, W)), mm(mm(W, V), W));
      var B = msub(madd(mm(W2, V), mm(V, W2)), mscale(mm(mm(W, V), W), 3));
      var C = madd(mm(mm(W, V), W2), mm(mm(W2, V), W));
      return madd(mscale(V, 0.5), madd(mscale(A, c1), madd(mscale(B, c2), mscale(C, c3))));
    }
    function QrSE3(xi) { return QlSE3(xi.map(function (v) { return -v; })); }   // 식 (79)
    // ξ = [ω; v] (회전 먼저) 순서에서는 Q 블록이 왼쪽 아래에 온다.
    // 원문 (75)·(77) 의 [[J, Q], [0, J]] 배치는 ξ = [v; ω] (이동 먼저) 순서를 전제한 것이다.
    // 수치 미분으로 확인했다 — 노트의 "원문 그대로 둔 것" 참조.
    function JlSE3(xi) {
      var w = [xi[0], xi[1], xi[2]], J = JlSO3(w);
      return blk(J, zeros(3, 3), QlSE3(xi), J);
    }
    function JrSE3(xi) { return JlSE3(xi.map(function (v) { return -v; })); }   // 식 (79)

    // ---- ⊕ / ⊖ ----------------------------------------------------------
    function plusSO3(R, w) { return mm(R, expSO3(w)); }                          // 식 (40)
    function minusSO3(R2, R1) { return logSO3(mm(mT(R1), R2)); }                 // 식 (42)
    function plusSE3(M, xi) { return mm(M, expSE3(xi)); }                        // 식 (68)
    function minusSE3(M2, M1) { return logSE3(mm(Tinv(M1), M2)); }               // 식 (69)

    // ---- 정사영 3D 장면 ---------------------------------------------------
    function scene(ctx, cx, cy, s, yaw, pitch) {
      var cyw = Math.cos(yaw), syw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
      function P(p) {
        var X = p[0]*cyw - p[1]*syw, Y = p[0]*syw + p[1]*cyw;
        return [cx + X*s, cy - (p[2]*cp - Y*sp)*s];
      }
      function head(A, B, col) {
        var ang = Math.atan2(B[1]-A[1], B[0]-A[0]), h = 8;
        ctx.save(); ctx.fillStyle = col; ctx.beginPath();
        ctx.moveTo(B[0], B[1]);
        ctx.lineTo(B[0] - h*Math.cos(ang-0.36), B[1] - h*Math.sin(ang-0.36));
        ctx.lineTo(B[0] - h*Math.cos(ang+0.36), B[1] - h*Math.sin(ang+0.36));
        ctx.closePath(); ctx.fill(); ctx.restore();
      }
      return {
        P: P,
        line: function (a, b, col, w, dash) {
          var A = P(a), B = P(b);
          ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w || 1.4;
          if (dash) ctx.setLineDash(dash);
          ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke(); ctx.restore();
        },
        arrow: function (a, b, col, w, dash) {
          var A = P(a), B = P(b);
          ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w || 2;
          if (dash) ctx.setLineDash(dash);
          ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke(); ctx.restore();
          head(A, B, col);
        },
        poly: function (pts, col, w, dash) {
          ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w || 1.2;
          if (dash) ctx.setLineDash(dash);
          ctx.beginPath();
          for (var i = 0; i < pts.length; i++) { var A = P(pts[i]); i ? ctx.lineTo(A[0], A[1]) : ctx.moveTo(A[0], A[1]); }
          ctx.stroke(); ctx.restore();
        },
        fillPoly: function (pts, col, alpha) {
          ctx.save(); ctx.fillStyle = col; ctx.globalAlpha = alpha === undefined ? 0.16 : alpha;
          ctx.beginPath();
          for (var i = 0; i < pts.length; i++) { var A = P(pts[i]); i ? ctx.lineTo(A[0], A[1]) : ctx.moveTo(A[0], A[1]); }
          ctx.closePath(); ctx.fill(); ctx.restore();
        },
        dot: function (p, col, r) {
          var A = P(p); ctx.save(); ctx.fillStyle = col;
          ctx.beginPath(); ctx.arc(A[0], A[1], r || 3, 0, 6.2832); ctx.fill(); ctx.restore();
        },
        label: function (p, txt, col, dx, dy) {
          var A = P(p); ctx.save(); ctx.fillStyle = col;
          ctx.font = '12px system-ui, sans-serif'; ctx.textAlign = 'left';
          ctx.fillText(txt, A[0] + (dx === undefined ? 7 : dx), A[1] + (dy === undefined ? -6 : dy));
          ctx.restore();
        }
      };
    }
    function circle3(n, r, N) {
      var a = Math.abs(n[0]) < 0.9 ? [1,0,0] : [0,1,0];
      var e1 = unit(cross(n, a)), e2 = cross(n, e1), pts = [];
      for (var i = 0; i <= (N || 64); i++) {
        var t = i/(N || 64)*2*Math.PI, c = Math.cos(t)*r, s2 = Math.sin(t)*r;
        pts.push([e1[0]*c + e2[0]*s2, e1[1]*c + e2[1]*s2, e1[2]*c + e2[2]*s2]);
      }
      return pts;
    }
    function frame(S, R, origin, len, cols, tag) {        // 좌표축 세 개
      var o = origin || [0,0,0];
      for (var i = 0; i < 3; i++) {
        var e = add(o, [R[0][i]*len, R[1][i]*len, R[2][i]*len]);
        S.arrow(o, e, cols[i], 2);
        if (tag && tag[i]) S.label(e, tag[i], cols[i]);
      }
    }
    
    // ══ 여기부터 이 스터디에서 더한 것 ══════════════════════════════════
    // 위쪽은 Lie Theory 스터디의 window.LG 를 그대로 가져온 것이고,
    // 아래는 preintegration 노트에 필요한 것만 새로 쓴 것이다.

    // ---- 난수 ------------------------------------------------------------
    // 위젯이 "다시 굴려도 같은 그림"이 되게 하려면 시드가 필요하다.
    // mulberry32 — 짧고 품질이 충분하다.
    function rng(seed) {
      var s = seed >>> 0;
      return function () {
        s |= 0; s = (s + 0x6D2B79F5) | 0;
        var t = Math.imul(s ^ (s >>> 15), 1 | s);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    }
    function randn(rnd) {                                   // Box–Muller
      var u = 1 - rnd(), v = rnd();
      return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);
    }
    function randnVec(n, rnd) { var v = []; for (var i = 0; i < n; i++) v.push(randn(rnd)); return v; }

    // ---- 대칭행렬 도구 ----------------------------------------------------
    function chol(A) {                                      // A = L Lᵀ (PD 아니면 null)
      var n = A.length, L = zeros(n, n);
      for (var i = 0; i < n; i++) for (var j = 0; j <= i; j++) {
        var s = A[i][j];
        for (var k = 0; k < j; k++) s -= L[i][k]*L[j][k];
        if (i === j) { if (s <= 1e-300) return null; L[i][j] = Math.sqrt(s); }
        else L[i][j] = s/L[j][j];
      }
      return L;
    }
    function symmetrize(A) { return mscale(madd(A, mT(A)), 0.5); }
    function fro(A) { var s = 0; A.forEach(function (r) { r.forEach(function (v) { s += v*v; }); }); return Math.sqrt(s); }

    // ---- 수치 미분 --------------------------------------------------------
    // f: R^n → R^m 을 중심차분으로 미분한다. 해석적 자코비안 검산 전용.
    function numJac(f, x, h) {
      h = h || 1e-6;
      var n = x.length, f0 = f(x), m = f0.length, J = zeros(m, n);
      for (var j = 0; j < n; j++) {
        var xp = x.slice(), xm = x.slice();
        xp[j] += h; xm[j] -= h;
        var a = f(xp), b = f(xm);
        for (var i = 0; i < m; i++) J[i][j] = (a[i] - b[i])/(2*h);
      }
      return J;
    }

    // ---- IMU 시뮬레이터 ---------------------------------------------------
    // 참 궤적을 해석적으로 정의하고 그것을 미분해 참 ω, a 를 만든다.
    // 이렇게 해야 "적분 오차"와 "모델 오차"를 섞지 않고 볼 수 있다.
    //   p(t) = [Rx cos(ωp t), Ry sin(ωp t), Az sin(ωz t)]
    //   R(t) = Exp([0,0,ψ t]) · Exp([φ sin(ωr t), 0, 0])
    var G = [0, 0, -9.81];                                  // 월드 중력
    function truth(t, o) {
      o = o || {};
      var Rx = o.Rx === undefined ? 2 : o.Rx, Ry = o.Ry === undefined ? 1.2 : o.Ry,
          wp = o.wp === undefined ? 1.1 : o.wp, Az = o.Az === undefined ? 0.4 : o.Az,
          wz = o.wz === undefined ? 2.3 : o.wz, psi = o.psi === undefined ? 0.7 : o.psi,
          phi = o.phi === undefined ? 0.5 : o.phi, wr = o.wr === undefined ? 1.7 : o.wr;
      var p = [Rx*Math.cos(wp*t), Ry*Math.sin(wp*t), Az*Math.sin(wz*t)];
      var v = [-Rx*wp*Math.sin(wp*t), Ry*wp*Math.cos(wp*t), Az*wz*Math.cos(wz*t)];
      var a = [-Rx*wp*wp*Math.cos(wp*t), -Ry*wp*wp*Math.sin(wp*t), -Az*wz*wz*Math.sin(wz*t)];
      var R = mm(expSO3([0, 0, psi*t]), expSO3([phi*Math.sin(wr*t), 0, 0]));
      return { p: p, v: v, a: a, R: R };
    }
    // 참 각속도는 Ṙ = R ω^ 에서 수치미분으로 얻는다 (합성회전이라 닫힌형이 지저분하다)
    function trueOmega(t, o, h) {
      h = h || 1e-6;
      var R = truth(t, o).R, R2 = truth(t + h, o).R, R1 = truth(t - h, o).R;
      var Rd = mscale(msub(R2, R1), 1/(2*h));
      return vee(mm(mT(R), Rd));                            // ω = (Rᵀ Ṙ)ᵨ
    }

    // 측정값 만들기 — 식 (29). bias·노이즈는 body 좌표계에서 더한다.
    //   ω̃ = ω + b^g + η^g,  ã = Rᵀ(a − g) + b^a + η^a
    function makeMeas(n, dt, bg, ba, sg, sa, seed, o) {
      var rnd = rng(seed === undefined ? 7 : seed), M = [];
      for (var k = 0; k < n; k++) {
        var t = k*dt, T = truth(t, o), w = trueOmega(t, o);
        var aB = mv(mT(T.R), sub(T.a, G));
        M.push({
          t: t,
          w: [w[0] + bg[0] + sg*randn(rnd), w[1] + bg[1] + sg*randn(rnd), w[2] + bg[2] + sg*randn(rnd)],
          a: [aB[0] + ba[0] + sa*randn(rnd), aB[1] + ba[1] + sa*randn(rnd), aB[2] + ba[2] + sa*randn(rnd)]
        });
      }
      return M;
    }

    // ---- 식 (34) 전방 적분 ------------------------------------------------
    // 절대 상태를 그대로 굴린다. R_i, v_i, p_i 가 바뀌면 전부 다시 계산해야 한다.
    function integrate(R0, v0, p0, M, dt, bg, ba) {
      var R = R0, v = v0.slice(), p = p0.slice(), traj = [{ R: R, v: v, p: p }];
      for (var k = 0; k < M.length; k++) {
        var w = sub(M[k].w, bg), a = sub(M[k].a, ba), Ra = mv(R, a);
        var pn = add(add(p, sc(v, dt)), sc(add(Ra, G), 0.5*dt*dt));
        var vn = add(v, sc(add(Ra, G), dt));
        R = mm(R, expSO3(sc(w, dt))); v = vn; p = pn;
        traj.push({ R: R, v: v, p: p });
      }
      return traj;
    }

    // ---- 식 (37)(58)(66) preintegration ------------------------------------
    // 측정값과 bias 만으로 ΔR, Δv, Δp 를 만든다. R_i, v_i, p_i 는 쓰지 않는다.
    // 같이 굴리는 것:
    //   Sig  9×9 공분산  — 식 (58) 반복식, [δφ, δv, δp] 순
    //   dRg, dvg, dva, dpg, dpa  — 식 (66) bias 자코비안
    function preint(M, dt, bg, ba, Seta) {
      var dR = eye(3), dv = [0,0,0], dp = [0,0,0], Sig = zeros(9, 9);
      var dRg = zeros(3,3), dvg = zeros(3,3), dva = zeros(3,3), dpg = zeros(3,3), dpa = zeros(3,3);
      var Z = zeros(3,3), I = eye(3);
      for (var k = 0; k < M.length; k++) {
        var w = sub(M[k].w, bg), a = sub(M[k].a, ba);
        var dRk = expSO3(sc(w, dt)), Jr = JrSO3(sc(w, dt));
        var Rda = mm(dR, hat(a));                           // ΔR_ik (ã−b^a)^

        if (Seta) {                                          // 식 (57)(58)
          var A = zeros(9,9), B = zeros(9,6), dRkT = mT(dRk);
          function put(Mt, r, c, X, s) {
            for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) Mt[r+i][c+j] = X[i][j]*(s===undefined?1:s);
          }
          put(A, 0, 0, dRkT);
          put(A, 3, 0, Rda, -dt);      put(A, 3, 3, I);
          put(A, 6, 0, Rda, -0.5*dt*dt); put(A, 6, 3, I, dt); put(A, 6, 6, I);
          put(B, 0, 0, Jr, dt);
          put(B, 3, 3, dR, dt);
          put(B, 6, 3, dR, 0.5*dt*dt);
          Sig = madd(mm(mm(A, Sig), mT(A)), mm(mm(B, Seta), mT(B)));
        }

        // 식 (66) — 누적형. 갱신 순서가 중요하다(dRg 는 마지막에 갱신).
        dpa = madd(msub(dpa, mscale(dR, 0.5*dt*dt)), mscale(dva, dt));
        dpg = madd(msub(dpg, mscale(mm(Rda, dRg), 0.5*dt*dt)), mscale(dvg, dt));
        dva = msub(dva, mscale(dR, dt));
        dvg = msub(dvg, mscale(mm(Rda, dRg), dt));
        dRg = msub(mm(mT(dRk), dRg), mscale(JrSO3(sc(w, dt)), dt));

        // 식 (37) 본체 — 갱신 순서: p → v → R
        dp = add(add(dp, sc(dv, dt)), sc(mv(dR, a), 0.5*dt*dt));
        dv = add(dv, sc(mv(dR, a), dt));
        dR = mm(dR, dRk);
      }
      return { dR: dR, dv: dv, dp: dp, dtij: M.length*dt, Sig: Sig,
               dRg: dRg, dvg: dvg, dva: dva, dpg: dpg, dpa: dpa };
    }

    // 식 (48) — 재적분 없이 bias 를 1차로 고쳐 쓴다
    function biasUpdate(P, dbg, dba) {
      return {
        dR: mm(P.dR, expSO3(mv(P.dRg, dbg))),
        dv: add(P.dv, add(mv(P.dvg, dbg), mv(P.dva, dba))),
        dp: add(P.dp, add(mv(P.dpg, dbg), mv(P.dpa, dba))),
        dtij: P.dtij
      };
    }

    // 식 (37) 좌변 — 두 키프레임 상태에서 상대량을 만든다
    function relFromStates(Ri, vi, pi, Rj, vj, pj, dtij) {
      var RiT = mT(Ri);
      return {
        dR: mm(RiT, Rj),
        dv: mv(RiT, sub(sub(vj, vi), sc(G, dtij))),
        dp: mv(RiT, sub(sub(sub(pj, pi), sc(vi, dtij)), sc(G, 0.5*dtij*dtij)))
      };
    }

    // 식 (49) residual — bias 보정항까지 포함한다
    function residual(P, Ri, vi, pi, Rj, vj, pj, dbg, dba) {
      var U = biasUpdate(P, dbg, dba), rel = relFromStates(Ri, vi, pi, Rj, vj, pj, P.dtij);
      return {
        rR: logSO3(mm(mT(U.dR), rel.dR)),
        rv: sub(rel.dv, U.dv),
        rp: sub(rel.dp, U.dp)
      };
    }

    // ---- 2D 플롯 ----------------------------------------------------------
    // 축·눈금·격자만 그려 주고 좌표 변환 함수를 돌려준다.
    function plot(ctx, box, xr, yr, opt) {
      opt = opt || {};
      var L = box[0], T = box[1], W = box[2], H = box[3];
      function X(x) { return L + (x - xr[0])/(xr[1] - xr[0])*W; }
      function Y(y) { return T + H - (y - yr[0])/(yr[1] - yr[0])*H; }
      ctx.save();
      ctx.strokeStyle = opt.rule || '#888'; ctx.lineWidth = 1; ctx.globalAlpha = 0.35;
      var nx = opt.nx || 5, ny = opt.ny || 4, i;
      for (i = 0; i <= nx; i++) { var x = xr[0] + (xr[1]-xr[0])*i/nx;
        ctx.beginPath(); ctx.moveTo(X(x), T); ctx.lineTo(X(x), T+H); ctx.stroke(); }
      for (i = 0; i <= ny; i++) { var y = yr[0] + (yr[1]-yr[0])*i/ny;
        ctx.beginPath(); ctx.moveTo(L, Y(y)); ctx.lineTo(L+W, Y(y)); ctx.stroke(); }
      ctx.restore();
      return {
        X: X, Y: Y,
        curve: function (pts, col, w, dash) {
          ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w || 2;
          if (dash) ctx.setLineDash(dash);
          ctx.beginPath();
          for (var i = 0; i < pts.length; i++) {
            var px = X(pts[i][0]), py = Y(pts[i][1]);
            i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
          }
          ctx.stroke(); ctx.restore();
        },
        dot: function (p, col, r) {
          ctx.save(); ctx.fillStyle = col; ctx.beginPath();
          ctx.arc(X(p[0]), Y(p[1]), r || 3, 0, 6.2832); ctx.fill(); ctx.restore();
        },
        bar: function (x0, x1, y, col, alpha) {
          ctx.save(); ctx.fillStyle = col; ctx.globalAlpha = alpha === undefined ? 0.8 : alpha;
          ctx.fillRect(X(x0), Y(y), X(x1)-X(x0), Y(yr[0])-Y(y)); ctx.restore();
        },
        text: function (s, x, y, col, align, font) {
          ctx.save(); ctx.fillStyle = col; ctx.textAlign = align || 'center';
          ctx.font = font || '11px ui-sans-serif, system-ui, sans-serif';
          ctx.fillText(s, X(x), Y(y)); ctx.restore();
        }
      };
    }

    // ---- 표시용 --------------------------------------------------------
    function fmt(x, d) {
      if (!isFinite(x)) return String(x);
      var a = Math.abs(x);
      if (a !== 0 && (a < 1e-3 || a >= 1e5)) return x.toExponential(d === undefined ? 2 : d);
      return x.toFixed(d === undefined ? 3 : d);
    }


    // ══ 여기부터 VINS-Mono 스터디에서 더한 것 ═══════════════════════════
    // 위쪽은 4_On-manifold preintegration 스터디의 window.PI 를 그대로 가져온 것이다
    // (SO(3) 지수·로그, 3D 씬, 난수, 수치미분, 2D 플롯).
    // 이 문서는 쿼터니언 기반이므로 아래를 새로 썼다 —
    //   쿼터니언 대수와 Ω_L/Ω_R, mid-point preintegration(α,β,γ), F·G·J·P 전파,
    //   초기화 선형시스템, Schur complement.
    //
    // 규약: 쿼터니언은 [w, x, y, z] 순서의 길이 4 배열이다 (원문 NOMENCLATURE 와 같다).

    // ---- 쿼터니언 -------------------------------------------------------
    function qmul(a, b) {                                   // a ⊗ b
      return [a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
              a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
              a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
              a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]];
    }
    function qconj(q) { return [q[0], -q[1], -q[2], -q[3]]; }
    function qinv(q) {                                      // 단위 쿼터니언이면 켤레와 같다
      var n = q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3];
      return qconj(q).map(function (v) { return v/n; });
    }
    function qnorm(q) { return Math.sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3]); }
    function qunit(q) { var n = qnorm(q) || 1; return q.map(function (v) { return v/n; }); }
    function qxyz(q) { return [q[1], q[2], q[3]]; }         // [·]_xyz — 식 (60)

    // 식 NOMENCLATURE — 좌·우 곱셈 연산자. Ω_L(w)q = w ⊗ q,  Ω_R(w)q = q ⊗ w
    // 인자는 3차원 벡터 ω 이며 순수 쿼터니언 [0, ω] 로 본다.
    function OmegaL(w) {
      return [[0, -w[0], -w[1], -w[2]],
              [w[0],  0,  -w[2],  w[1]],
              [w[1],  w[2],  0,  -w[0]],
              [w[2], -w[1],  w[0],  0]];
    }
    function OmegaR(w) {
      return [[0, -w[0], -w[1], -w[2]],
              [w[0],  0,   w[2], -w[1]],
              [w[1], -w[2],  0,   w[0]],
              [w[2],  w[1], -w[0],  0]];
    }
    // 전체 쿼터니언의 좌·우 곱 행렬 [q]_L, [q]_R  (식 178~180 에서 쓴다)
    function qLmat(q) {
      var w=q[0],x=q[1],y=q[2],z=q[3];
      return [[w,-x,-y,-z],[x,w,-z,y],[y,z,w,-x],[z,-y,x,w]];
    }
    function qRmat(q) {
      var w=q[0],x=q[1],y=q[2],z=q[3];
      return [[w,-x,-y,-z],[x,w,z,-y],[y,-z,w,x],[z,y,-x,w]];
    }
    function br3(M) {                                       // 오른쪽 아래 3×3 블록
      return [[M[1][1],M[1][2],M[1][3]],[M[2][1],M[2][2],M[2][3]],[M[3][1],M[3][2],M[3][3]]];
    }
    function q2R(q) {                                       // R{q} — 식 NOMENCLATURE
      var w = q[0], x = q[1], y = q[2], z = q[3];
      return [[1-2*(y*y+z*z), 2*(x*y-w*z),   2*(x*z+w*y)],
              [2*(x*y+w*z),   1-2*(x*x+z*z), 2*(y*z-w*x)],
              [2*(x*z-w*y),   2*(y*z+w*x),   1-2*(x*x+y*y)]];
    }
    function R2q(R) {
      var tr = R[0][0] + R[1][1] + R[2][2], s, q;
      if (tr > 0) { s = Math.sqrt(tr + 1)*2; q = [0.25*s, (R[2][1]-R[1][2])/s, (R[0][2]-R[2][0])/s, (R[1][0]-R[0][1])/s]; }
      else if (R[0][0] > R[1][1] && R[0][0] > R[2][2]) {
        s = Math.sqrt(1 + R[0][0] - R[1][1] - R[2][2])*2;
        q = [(R[2][1]-R[1][2])/s, 0.25*s, (R[0][1]+R[1][0])/s, (R[0][2]+R[2][0])/s];
      } else if (R[1][1] > R[2][2]) {
        s = Math.sqrt(1 + R[1][1] - R[0][0] - R[2][2])*2;
        q = [(R[0][2]-R[2][0])/s, (R[0][1]+R[1][0])/s, 0.25*s, (R[1][2]+R[2][1])/s];
      } else {
        s = Math.sqrt(1 + R[2][2] - R[0][0] - R[1][1])*2;
        q = [(R[1][0]-R[0][1])/s, (R[0][2]+R[2][0])/s, (R[1][2]+R[2][1])/s, 0.25*s];
      }
      return q[0] < 0 ? q.map(function (v) { return -v; }) : q;
    }
    function qexp(v) {                                      // 회전벡터 → 단위 쿼터니언
      var t = nrm(v);
      if (t < 1e-9) return qunit([1, v[0]/2, v[1]/2, v[2]/2]);
      var s = Math.sin(t/2)/t;
      return [Math.cos(t/2), v[0]*s, v[1]*s, v[2]*s];
    }
    function qlog(q) {                                      // 단위 쿼터니언 → 회전벡터
      q = q[0] < 0 ? q.map(function (v) { return -v; }) : q;
      var v = qxyz(q), s = nrm(v);
      if (s < 1e-12) return sc(v, 2);
      return sc(v, 2*Math.atan2(s, q[0])/s);
    }
    // 원문이 자주 쓰는 작은 회전 근사 δq ≈ [1, ½δθ]  (식 (6) 아래 주석)
    function qsmall(dth) { return [1, dth[0]/2, dth[1]/2, dth[2]/2]; }

    // ---- IMU 시뮬레이터 (월드 좌표계 기준) ------------------------------
    // 원문 (2) 를 그대로 따른다:  â = a + b_a + R^t_w g^w + n_a ,  ω̂ = ω + b_g + n_g
    // 여기서 g^w = [0,0,+9.8] 이다 (원문 NOMENCLATURE. 부호에 주의).
    var GW = [0, 0, 9.8];
    function truthVI(t, o) {
      o = o || {};
      var Rx = o.Rx === undefined ? 2 : o.Rx, Ry = o.Ry === undefined ? 1.2 : o.Ry,
          wp = o.wp === undefined ? 1.1 : o.wp, Az = o.Az === undefined ? 0.4 : o.Az,
          wz = o.wz === undefined ? 2.3 : o.wz, psi = o.psi === undefined ? 0.7 : o.psi,
          phi = o.phi === undefined ? 0.5 : o.phi, wr = o.wr === undefined ? 1.7 : o.wr;
      return {
        p: [Rx*Math.cos(wp*t), Ry*Math.sin(wp*t), Az*Math.sin(wz*t)],
        v: [-Rx*wp*Math.sin(wp*t), Ry*wp*Math.cos(wp*t), Az*wz*Math.cos(wz*t)],
        a: [-Rx*wp*wp*Math.cos(wp*t), -Ry*wp*wp*Math.sin(wp*t), -Az*wz*wz*Math.sin(wz*t)],
        q: qmul(qexp([0, 0, psi*t]), qexp([phi*Math.sin(wr*t), 0, 0]))
      };
    }
    function trueOmegaVI(t, o, h) {
      h = h || 1e-6;
      var q = truthVI(t, o).q, q2 = truthVI(t + h, o).q, q1 = truthVI(t - h, o).q;
      var qd = [(q2[0]-q1[0])/(2*h), (q2[1]-q1[1])/(2*h), (q2[2]-q1[2])/(2*h), (q2[3]-q1[3])/(2*h)];
      return sc(qxyz(qmul(qconj(q), qd)), 2);               // ω = 2 (q* ⊗ q̇)_xyz
    }
    function makeMeasVI(n, dt, bg, ba, sg, sa, seed, o) {
      var rnd = rng(seed === undefined ? 7 : seed), M = [];
      for (var k = 0; k <= n; k++) {
        var t = k*dt, T = truthVI(t, o), w = trueOmegaVI(t, o);
        var Rwt = mT(q2R(T.q));                             // R^t_w
        var aB = mv(Rwt, add(T.a, GW));                     // â = R^t_w(a + g) …  (2) 를 옮긴 것
        M.push({ t: t,
          w: [w[0] + bg[0] + sg*randn(rnd), w[1] + bg[1] + sg*randn(rnd), w[2] + bg[2] + sg*randn(rnd)],
          a: [aB[0] + ba[0] + sa*randn(rnd), aB[1] + ba[1] + sa*randn(rnd), aB[2] + ba[2] + sa*randn(rnd)] });
      }
      return M;
    }

    // ---- 절대 적분 (식 4·5) ---------------------------------------------
    // ★ preintVI 와 **같은 수치 해법**을 써야 한다. 식 (7)의 좌변=우변을 확인할 때
    //   한쪽만 오일러로 굴리면 O(δt²) 만큼 어긋나서 (실측 5.6e-3) 마치 식이 틀린 것처럼 보인다.
    //   그래서 여기도 식 (9) mid-point 로 맞췄다.
    function integrateVI(q0, v0, p0, M, dt, bg, ba, method) {
      var euler = (method === 'euler');
      var q = q0.slice(), v = v0.slice(), p = p0.slice(), tr = [{ q: q, v: v, p: p }];
      for (var k = 0; k + 1 < M.length; k++) {
        var w0 = sub(M[k].w, bg), w1 = sub(M[k+1].w, bg);
        var wm = sc(add(w0, w1), 0.5);
        var qN = qunit(qmul(q, qsmall(sc(euler ? w0 : wm, dt))));
        var f0 = sub(mv(q2R(q), sub(M[k].a, ba)), GW);      // (3): a = R(â − b) − g
        var f1 = sub(mv(q2R(qN), sub(M[k+1].a, ba)), GW);
        var fm = euler ? f0 : sc(add(f0, f1), 0.5);
        p = add(add(p, sc(v, dt)), sc(fm, 0.5*dt*dt));
        v = add(v, sc(fm, dt));
        q = qN;
        tr.push({ q: q, v: v, p: p });
      }
      return tr;
    }

    // ---- preintegration (식 9 mid-point / 식 10 euler) -------------------
    // 같이 굴리는 것:  P 9×9? 아니다 — 이 문서의 에러 상태는 15차원이다
    //   δx = [δα, δθ, δβ, δb_a, δb_g]  (식 37 의 순서)
    //   F 15×15, G 15×18, J 15×15, P 15×15
    function preintVI(M, dt, bg, ba, Q, method) {
      var euler = (method === 'euler');
      var al = [0,0,0], be = [0,0,0], ga = [1,0,0,0];
      var J = eye(15), P = zeros(15, 15);
      var I3 = eye(3), Z3 = zeros(3,3);
      function put(A, r, c, X, s) {
        for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) A[r+i][c+j] = X[i][j]*(s === undefined ? 1 : s);
      }
      for (var k = 0; k + 1 < M.length; k++) {
        var a0 = sub(M[k].a, ba), a1 = sub(M[k+1].a, ba);
        var w0 = sub(M[k].w, bg), w1 = sub(M[k+1].w, bg);
        var wm = sc(add(w0, w1), 0.5);                      // mid-point 각속도
        var Rk = q2R(ga);
        var gaN = euler ? qunit(qmul(ga, qsmall(sc(w0, dt))))
                        : qunit(qmul(ga, qsmall(sc(wm, dt))));
        var Rk1 = q2R(gaN);
        var f0 = mv(Rk, a0), f1 = mv(Rk1, a1);
        if (euler) {                                        // 식 (10)
          al = add(add(al, sc(be, dt)), sc(f0, 0.5*dt*dt));
          be = add(be, sc(f0, dt));
        } else {                                            // 식 (9)
          var fm = sc(add(f0, f1), 0.5);
          al = add(add(al, sc(be, dt)), sc(fm, 0.5*dt*dt));
          be = add(be, sc(fm, dt));
        }

        if (Q) {                                            // 식 (37)(38) → (27)(28)
          var F = eye(15), G = zeros(15, 18);
          var A0 = mm(Rk, hat(a0)), A1 = mm(Rk1, hat(a1));
          var W = msub(I3, mscale(hat(wm), dt));            // F11
          put(F, 0, 3, madd(mscale(A0, -dt*dt/4), mscale(mm(A1, W), -dt*dt/4)));   // F01
          put(F, 0, 6, I3, dt);
          put(F, 0, 9, madd(Rk, Rk1), -dt*dt/4);                                   // F03
          put(F, 0, 12, A1, dt*dt*dt/4);                                           // F04
          put(F, 3, 3, W);                                                         // F11
          put(F, 3, 12, I3, -dt);
          put(F, 6, 3, madd(mscale(A0, -dt/2), mscale(mm(A1, W), -dt/2)));         // F21
          put(F, 6, 9, madd(Rk, Rk1), -dt/2);                                      // F23
          put(F, 6, 12, A1, dt*dt/2);                                              // F24
          put(G, 0, 0, Rk, -dt*dt/4);                                              // G00
          put(G, 0, 3, A1, dt*dt*dt/8);                                            // G01
          put(G, 0, 6, Rk1, -dt*dt/4);                                             // G02
          put(G, 0, 9, A1, dt*dt*dt/8);                                            // G03
          put(G, 3, 3, I3, -dt/2);
          put(G, 3, 9, I3, -dt/2);
          put(G, 6, 0, Rk, -dt/2);
          put(G, 6, 3, A1, dt*dt/4);                                               // G21
          put(G, 6, 6, Rk1, -dt/2);
          put(G, 6, 9, A1, dt*dt/4);                                               // G23
          put(G, 9, 12, I3, dt);
          put(G, 12, 15, I3, dt);
          P = madd(mm(mm(F, P), mT(F)), mm(mm(G, Q), mT(G)));   // 식 (27)
          J = mm(F, J);                                          // 식 (28)
        }
        ga = gaN;
      }
      return { al: al, be: be, ga: ga, dt: (M.length - 1)*dt, J: J, P: P };
    }

    // 식 (29) — 재적분 없이 bias 를 1차로 고쳐 쓴다
    function biasUpdateVI(PR, dbg, dba) {
      function blk(r, c) {
        var B = zeros(3,3);
        for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) B[i][j] = PR.J[r+i][c+j];
        return B;
      }
      var Jaa = blk(0, 9), Jag = blk(0, 12), Jba = blk(6, 9), Jbg = blk(6, 12), Jgg = blk(3, 12);
      return {
        al: add(PR.al, add(mv(Jaa, dba), mv(Jag, dbg))),
        be: add(PR.be, add(mv(Jba, dba), mv(Jbg, dbg))),
        ga: qunit(qmul(PR.ga, qsmall(mv(Jgg, dbg)))),
        dt: PR.dt
      };
    }

    // 식 (7) 좌변 — 두 키프레임 상태에서 상대량을 만든다
    function relFromStatesVI(qi, vi, pi, qj, vj, pj, dtij) {
      var Rwi = mT(q2R(qi));                                // R^{b_k}_w
      return {
        al: mv(Rwi, sub(sub(sub(pj, pi), sc(vi, dtij)), sc(GW, -0.5*dtij*dtij))),
        be: mv(Rwi, sub(sub(vj, vi), sc(GW, -dtij))),
        ga: qmul(qinv(qi), qj)
      };
    }

    // 식 (60) IMU residual
    function residualVI(PR, qi, vi, pi, qj, vj, pj, dbg, dba) {
      var U = biasUpdateVI(PR, dbg, dba), rel = relFromStatesVI(qi, vi, pi, qj, vj, pj, PR.dt);
      return {
        ra: sub(rel.al, U.al),
        rth: sc(qxyz(qmul(qinv(U.ga), rel.ga)), 2),
        rb: sub(rel.be, U.be)
      };
    }

    // ---- 선형대수 (초기화·marginalization 용) ----------------------------
    function solveLS(A, b) {                                // 정규방정식 + 가우스-조던
      var At = mT(A);
      return mv(minv(mm(At, A)), mv(At, b));
    }
    function schur(H, b, m) {                               // 앞 m개를 marginalize
      var n = H.length, r = n - m;
      function sub2(R0, C0, R1, C1) {
        var M2 = zeros(R1-R0, C1-C0);
        for (var i = R0; i < R1; i++) for (var j = C0; j < C1; j++) M2[i-R0][j-C0] = H[i][j];
        return M2;
      }
      var Hmm = sub2(0,0,m,m), Hmr = sub2(0,m,m,n), Hrm = sub2(m,0,n,m), Hrr = sub2(m,m,n,n);
      var bm = b.slice(0,m), br = b.slice(m);
      var Hmi = minv(Hmm), K = mm(Hrm, Hmi);
      return { Hp: msub(Hrr, mm(K, Hmr)), bp: sub(br, mv(K, bm)),
               Hmm: Hmm, Hmr: Hmr, Hrm: Hrm, Hrr: Hrr };
    }
    // 접평면 basis — 식 (47)(70) 이 쓰는 두 직교 basis
    function tangentBasis(g) {
      var a = Math.abs(g[0]) < 0.9 ? [1,0,0] : [0,1,0];
      var b1 = unit(cross(unit(g), a)), b2 = cross(unit(g), b1);
      return [b1, b2];
    }


    // ══ 여기부터 Errors and Jacobian Derivations 스터디에서 더한 것 ═════
    // 위쪽은 5_VINS-Mono 스터디의 window.VM 을 그대로 가져온 것이다
    // (SO(3)/SE(3), 쿼터니언, 3D 씬, 난수, 수치미분, 2D 플롯, Schur).
    // 아래는 이 문서 전용 —
    //   핀홀 투영 π_h·π_k 와 렌즈 왜곡, 이미지 패치와 쌍선형 보간,
    //   Plücker 직선과 orthonormal (U,W) 표현, GN/LM 한 스텝.

    // ---- 핀홀 카메라 -----------------------------------------------------
    // 원문 NOMENCLATURE 그대로:  π_h 는 non-homogeneous 화, π_k 는 K 를 곱하는 것
    function piH(Xp) { return [Xp[0]/Xp[2], Xp[1]/Xp[2], 1]; }          // 식 (49) 위
    function piK(pt, K) { return [K.fx*pt[0] + K.cx, K.fy*pt[1] + K.cy]; }
    function project(Xp, K) { return piK(piH(Xp), K); }
    function backProject(p, Z, K) {                                     // π⁻¹ = Z K⁻¹ p
      return [Z*(p[0] - K.cx)/K.fx, Z*(p[1] - K.cy)/K.fy, Z];
    }
    // radial-tangential 왜곡 — 원문은 자코비안에서 무시한다고 했지만
    // "무시했을 때 얼마나 틀리는가" 를 보이려면 정방향 모델이 필요하다.
    function distort(pt, D) {
      var x = pt[0], y = pt[1], r2 = x*x + y*y;
      var rad = 1 + D.k1*r2 + D.k2*r2*r2;
      return [x*rad + 2*D.p1*x*y + D.p2*(r2 + 2*x*x),
              y*rad + D.p1*(r2 + 2*y*y) + 2*D.p2*x*y, 1];
    }
    function projectD(Xp, K, D) { return piK(distort(piH(Xp), D), K); }

    // 식 (48)(49) — ∂p̂/∂p̃ · ∂p̃/∂X′ 를 합친 2×3 (마지막 열이 0 이라 3열만 쓴다)
    function dpdX(Xp, K) {
      var Z = Xp[2], Z2 = Z*Z;
      return [[K.fx/Z, 0, -K.fx*Xp[0]/Z2],
              [0, K.fy/Z, -K.fy*Xp[1]/Z2]];
    }

    // ---- 이미지 (photometric) --------------------------------------------
    // 합성 이미지: 가우시안 블롭 몇 개를 겹쳐 만든다. 해석적 그래디언트가 있어
    // "이미지 그래디언트 ∇I" 를 정확히 알 수 있다 — 식 (83) 검산에 쓴다.
    // 합성 이미지 — 여러 스케일의 가우시안 블롭 합.
    // blur(σ_b) 는 각 블롭의 σ 에 제곱합으로 더한다 (가우시안⊛가우시안 = 가우시안).
    // 그래서 블러를 걸어도 ∇I 가 여전히 해석적으로 정확하다 — 수치미분 검산에 쓸 수 있다.
    function makeImage(seed, blur) {
      var rnd = rng(seed === undefined ? 1 : seed), blobs = [];
      var sb2 = (blur === undefined ? 0 : blur*blur);
      // 굵은 구조 + 잔 텍스처를 섞는다. 잔 텍스처가 있어야 광도 오차의
      // 국소 극소값이 실제로 생긴다.
      [[10, 18, 40, 0.9], [45, 5, 11, 0.55], [130, 1.8, 4.0, 0.34]].forEach(function (g) {
        for (var i = 0; i < g[0]; i++)
          blobs.push({ x: 40 + 560*rnd(), y: 40 + 400*rnd(),
                       a: g[3]*(2*rnd() - 1), s0: g[1] + (g[2] - g[1])*rnd() });
      });
      blobs.forEach(function (b) { b.s = Math.sqrt(b.s0*b.s0 + sb2);
                                   b.aa = b.a*b.s0*b.s0/(b.s*b.s); });   // 블러 시 진폭 보존
      return {
        blobs: blobs, blur: blur === undefined ? 0 : blur,
        at: function (u, v) {
          var s = 0.5;
          for (var i = 0; i < blobs.length; i++) {
            var b = blobs[i], dx = u - b.x, dy = v - b.y;
            s += b.aa*Math.exp(-(dx*dx + dy*dy)/(2*b.s*b.s));
          }
          return s;
        },
        grad: function (u, v) {                                 // 해석적 ∇I
          var gu = 0, gv = 0;
          for (var i = 0; i < blobs.length; i++) {
            var b = blobs[i], dx = u - b.x, dy = v - b.y;
            var e = b.aa*Math.exp(-(dx*dx + dy*dy)/(2*b.s*b.s))/(b.s*b.s);
            gu -= dx*e; gv -= dy*e;
          }
          return [gu, gv];
        }
      };
    }

    // ---- Plücker 직선 ----------------------------------------------------
    // 원문 (130) 순서를 따른다:  L = [m ; d]
    function lineFromPoints(P, Q) {
      var d = sub(Q, P), m = cross(P, Q);
      return { m: m, d: d };
    }
    function lineTransform(L, R, t) {                            // 식 (131)
      return { m: add(mv(R, L.m), cross(t, mv(R, L.d))), d: mv(R, L.d) };
    }
    function KLmat(K) {                                          // 식 (133)
      return [[K.fy, 0, 0], [0, K.fx, 0], [-K.fy*K.cx, -K.fx*K.cy, K.fx*K.fy]];
    }
    function lineProject(Lc, K) { return mv(KLmat(K), Lc.m); }   // 식 (132)
    // 식 (134) — 점-직선 거리 두 개
    function lineError(lc, xs, xe) {
      var n = Math.sqrt(lc[0]*lc[0] + lc[1]*lc[1]);
      return [dot(xs, lc)/n, dot(xe, lc)/n];
    }
    // 식 (136)(137) — Plücker → orthonormal (U, W)
    function toOrthonormal(L) {
      var nm = nrm(L.m), nd = nrm(L.d);
      var u1 = sc(L.m, 1/nm), u2 = sc(L.d, 1/nd);
      var c = cross(L.m, L.d), u3 = sc(c, 1/nrm(c));
      var U = [[u1[0], u2[0], u3[0]], [u1[1], u2[1], u3[1]], [u1[2], u2[2], u3[2]]];
      var s = Math.sqrt(nm*nm + nd*nd);
      return { U: U, W: [[nm/s, -nd/s], [nd/s, nm/s]], w1: nm/s, w2: nd/s, scale: s };
    }
    // 식 (138) — orthonormal → Plücker (스케일은 up-to-scale 이라 임의다)
    function fromOrthonormal(O) {
      return { m: sc([O.U[0][0], O.U[1][0], O.U[2][0]], O.w1),
               d: sc([O.U[0][1], O.U[1][1], O.U[2][1]], O.w2) };
    }
    // 식 (137) 아래 — U ← U R(θ), W ← W R(θ)
    function orthoUpdate(O, dth, dtheta) {
      var U2 = mm(O.U, expSO3(dth));
      var c = Math.cos(dtheta), s2 = Math.sin(dtheta);
      var W2 = mm(O.W, [[c, -s2], [s2, c]]);
      return { U: U2, W: W2, w1: W2[0][0], w2: W2[1][0], scale: O.scale };
    }

    // ---- GN / LM 한 스텝 (식 31·33) ---------------------------------------
    function gnStep(H, b, lam) {
      var n = H.length, A = H.map(function (r) { return r.slice(); });
      for (var i = 0; i < n; i++) A[i][i] += (lam || 0);
      return sc(mv(minv(A), b), -1);
    }

    // ══ 여기부터 Iterative Closest Point 스터디에서 더한 것 ═════════════

    // ---- 실수 대칭행렬 고유분해 (순환 Jacobi) ---------------------------
    // A = V diag(w) Vᵀ,  w 는 내림차순.  n×n 어떤 크기든 된다.
    function eigSym(Ain) {
      var n = Ain.length, i, j, k, p, q;
      var A = Ain.map(function (r) { return r.slice(); });
      var V = eye(n);
      for (var sweep = 0; sweep < 100; sweep++) {
        var off = 0;
        for (i = 0; i < n; i++) for (j = i + 1; j < n; j++) off += A[i][j]*A[i][j];
        if (off < 1e-30) break;
        for (p = 0; p < n; p++) for (q = p + 1; q < n; q++) {
          if (Math.abs(A[p][q]) < 1e-300) continue;
          var theta = (A[q][q] - A[p][p])/(2*A[p][q]);
          var t = Math.sign(theta || 1)/(Math.abs(theta) + Math.sqrt(theta*theta + 1));
          var c = 1/Math.sqrt(t*t + 1), s = t*c;
          for (k = 0; k < n; k++) {
            var akp = A[k][p], akq = A[k][q];
            A[k][p] = c*akp - s*akq; A[k][q] = s*akp + c*akq;
          }
          for (k = 0; k < n; k++) {
            var apk = A[p][k], aqk = A[q][k];
            A[p][k] = c*apk - s*aqk; A[q][k] = s*apk + c*aqk;
          }
          for (k = 0; k < n; k++) {
            var vkp = V[k][p], vkq = V[k][q];
            V[k][p] = c*vkp - s*vkq; V[k][q] = s*vkp + c*vkq;
          }
        }
      }
      var idx = [];
      for (i = 0; i < n; i++) idx.push(i);
      idx.sort(function (a, b) { return A[b][b] - A[a][a]; });          // 내림차순
      var w = idx.map(function (a) { return A[a][a]; });
      var Vs = zeros(n, n);
      for (i = 0; i < n; i++) for (j = 0; j < n; j++) Vs[i][j] = V[i][idx[j]];
      return { w: w, V: Vs };
    }

    // ---- SVD:  A = U D Vᵀ  (정사각 실행렬) -------------------------------
    // AᵀA 를 고유분해해 V·특이값을 얻고 U = A V D⁻¹ 로 만든다.
    // 특이값이 0 에 가까운 방향은 그람-슈미트로 채워 U 를 직교로 유지한다.
    function svd(A) {
      var n = A.length, i, j, k, m;
      var e = eigSym(mm(mT(A), A));
      var D = e.w.map(function (x) { return Math.sqrt(Math.max(0, x)); });
      var V = e.V;
      var AV = mm(A, V), U = zeros(n, n);
      // 열을 하나씩 세우되, 항상 앞선 열들과 직교화한다.
      // 특이값이 0 에 가까운 열은 AV 열이 잡음뿐이므로 직교여공간에서 채운다.
      var TOL = 1e-7*Math.max(1e-300, D[0]);
      for (j = 0; j < n; j++) {
        var col = [];
        for (i = 0; i < n; i++) col.push(AV[i][j]);
        if (D[j] > TOL) { for (i = 0; i < n; i++) col[i] /= D[j]; }
        else { for (i = 0; i < n; i++) col[i] = 0; }
        // 그람-슈미트
        for (m = 0; m < j; m++) {
          var d2 = 0;
          for (i = 0; i < n; i++) d2 += U[i][m]*col[i];
          for (i = 0; i < n; i++) col[i] -= d2*U[i][m];
        }
        var len = nrm(col);
        if (len < 1e-8) {
          // 앞선 열들과 직교하는 축을 찾아 채운다
          var best = null, bn = -1;
          for (k = 0; k < n; k++) {
            var c2 = new Array(n).fill(0); c2[k] = 1;
            for (m = 0; m < j; m++) {
              var d3 = 0;
              for (i = 0; i < n; i++) d3 += U[i][m]*c2[i];
              for (i = 0; i < n; i++) c2[i] -= d3*U[i][m];
            }
            var nn = nrm(c2);
            if (nn > bn) { bn = nn; best = c2; }
          }
          col = best; len = bn;
        }
        for (i = 0; i < n; i++) U[i][j] = col[i]/Math.max(1e-300, len);
      }
      return { U: U, D: D, V: V };
    }
    function det3(M) {
      if (M.length === 2) return M[0][0]*M[1][1] - M[0][1]*M[1][0];
      return M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1])
           - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0])
           + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]);
    }

    // ---- 원문 2·3장의 예제 점군 (그대로) ---------------------------------
    var SRC2D = [[-19,-15],[-18,-10],[-15,-9],[-14,-7],[-11,-6],[-9,-5],[-7,-6],[-4,-8],[-1,-11],[0,-14],
                 [1,-17],[5,-20],[9,-24],[10,-25],[13,-24],[14,-25],[17,-25],[19,-22],[22,-18],[23,-16]];
    var TGT2D = [[-12,-8],[-12,-2],[-10,1],[-10,4],[-9,6],[-6,7],[-3,8],[-1,8],[3,6],[6,5],
                 [10,3],[14,1],[17,1],[19,0],[22,1],[24,2],[27,4],[26,7],[27,11],[27,15]];
    var SRC3D = [[-19,-15,7],[-18,-10,6],[-15,-9,5],[-14,-7,4],[-11,-6,8],[-9,-5,5],[-7,-6,7],[-4,-8,6],
                 [-1,-11,4],[0,-14,6],[1,-17,8],[5,-20,7],[9,-24,5],[10,-25,6],[13,-24,8],[14,-25,5],
                 [17,-25,7],[19,-22,6],[22,-18,8],[23,-16,7]];
    var TGT3D = [[-12,-8,9],[-12,-2,11],[-10,1,10],[-10,4,12],[-9,6,9],[-6,7,10],[-3,8,8],[-1,8,12],
                 [3,6,11],[6,5,9],[10,3,8],[14,1,12],[17,1,11],[19,0,10],[22,1,8],[24,2,9],[27,4,11],
                 [26,7,12],[27,11,9],[27,15,10]];
    function ex2D() { return { src: SRC2D.map(function (p) { return p.slice(); }),
                               tgt: TGT2D.map(function (p) { return p.slice(); }) }; }
    function ex3D() { return { src: SRC3D.map(function (p) { return p.slice(); }),
                               tgt: TGT3D.map(function (p) { return p.slice(); }) }; }

    // ---- 점군 기본 연산 ---------------------------------------------------
    function centroid(P) {                                   // 식 (3)
      var d = P[0].length, c = new Array(d).fill(0);
      for (var i = 0; i < P.length; i++) for (var j = 0; j < d; j++) c[j] += P[i][j];
      return c.map(function (v) { return v/P.length; });
    }
    function demean(P, c) {                                  // 식 (4)
      c = c || centroid(P);
      return P.map(function (p) { return sub(p, c); });
    }
    // 식 (9)(12):  C = p'_t p'^⊺_{t+1}   (source 를 앞에 두는 원문 순서 그대로)
    function covXY(Ps, Pt) {
      var d = Ps[0].length, C = zeros(d, d);
      for (var k = 0; k < Ps.length; k++)
        for (var i = 0; i < d; i++) for (var j = 0; j < d; j++) C[i][j] += Ps[k][i]*Pt[k][j];
      return C;
    }
    function transform(P, R, t) {
      return P.map(function (p) { return add(mv(R, p), t); });
    }
    // 무차별 최근접 탐색 (예제 규모에서는 KD-tree 가 필요 없다)
    function nearest(P, Q, maxDist) {
      var out = [];
      for (var i = 0; i < P.length; i++) {
        var bi = -1, bd = Infinity;
        for (var j = 0; j < Q.length; j++) {
          var d2 = 0;
          for (var k = 0; k < P[i].length; k++) { var dd = P[i][k] - Q[j][k]; d2 += dd*dd; }
          if (d2 < bd) { bd = d2; bi = j; }
        }
        if (maxDist === undefined || Math.sqrt(bd) <= maxDist) out.push({ i: i, j: bi, d: Math.sqrt(bd) });
      }
      return out;
    }
    function rmse(P, Q, corr) {
      if (!corr || !corr.length) return NaN;
      var s = 0;
      for (var k = 0; k < corr.length; k++) { var d = sub(P[corr[k].i], Q[corr[k].j]); s += dot(d, d); }
      return Math.sqrt(s/corr.length);
    }
    function R2d(th) { return [[Math.cos(th), -Math.sin(th)], [Math.sin(th), Math.cos(th)]]; }

    // ---- 식 (26)(27): SVD 닫힌 해 -----------------------------------------
    // fixDet 를 켜면 (27) 처럼 det(VUᵀ) 를 끼워 넣어 reflection 을 막는다.
    function svdSolve(Ps, Pt, fixDet) {
      var cs = centroid(Ps), ct = centroid(Pt);
      var C = covXY(demean(Ps, cs), demean(Pt, ct));
      var s = svd(C);
      var R = mm(s.V, mT(s.U));                              // R = V Uᵀ
      if (fixDet !== false) {
        var n = R.length, S = eye(n);
        S[n-1][n-1] = det3(mm(s.V, mT(s.U))) < 0 ? -1 : 1;
        R = mm(s.V, mm(S, mT(s.U)));
      }
      return { R: R, t: sub(ct, mv(R, cs)), C: C, U: s.U, D: s.D, V: s.V, cs: cs, ct: ct };
    }

    // ---- 법선 추정 ---------------------------------------------------------
    function normal2D(p) { return unit([-p[1], p[0]]); }     // 5.1절 — n = [−y, x]ᵀ
    // 이웃 k개의 공분산을 PCA 해서 가장 작은 고유값의 고유벡터를 쓴다 (5.2·6.3절)
    function normalsPCA(P, k) {
      k = k || 8;
      var d = P[0].length;
      return P.map(function (p, i) {
        var ds = P.map(function (q, j) { return { j: j, d: nrm(sub(q, p)) }; });
        ds.sort(function (a, b) { return a.d - b.d; });
        var nb = ds.slice(0, Math.min(k, P.length)).map(function (o) { return P[o.j]; });
        var c = centroid(nb), M = zeros(d, d);
        nb.forEach(function (q) {
          var v = sub(q, c);
          for (var a = 0; a < d; a++) for (var b = 0; b < d; b++) M[a][b] += v[a]*v[b];
        });
        var e = eigSym(M);
        var n = [];
        for (var a2 = 0; a2 < d; a2++) n.push(e.V[a2][d-1]);  // 가장 작은 고유값
        return { n: unit(n), w: e.w, V: e.V, c: c };
      });
    }

    // ---- point-to-point GN --------------------------------------------------
    // 식 (29)~(33): 2D.  x = [tx, ty, θ]ᵀ,  e = R(θ)p_t + t − p_{t+1}
    function jacP2P2D(p, th) {
      return [[1, 0, -Math.sin(th)*p[0] - Math.cos(th)*p[1]],
              [0, 1,  Math.cos(th)*p[0] - Math.sin(th)*p[1]]];
    }
    // 식 (40)~(45): 3D.  좌섭동 so(3),  e = R p_t + t − p_{t+1}
    //   ∂e/∂[t, Δw] = [ I   −[R p_t + t]× ]
    function jacP2P3D(pw) {                                   // pw = R p_t + t
      var J = zeros(3, 6);
      J[0][0] = 1; J[1][1] = 1; J[2][2] = 1;
      var S = mscale(hat(pw), -1);
      for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) J[i][3+j] = S[i][j];
      return J;
    }
    // 식 (55)(56): point-to-plane 2D — n 을 왼쪽에 곱한 1×3
    function jacP2L2D(p, th, n) {
      var J2 = jacP2P2D(p, th);
      return [[n[0]*J2[0][0] + n[1]*J2[1][0],
               n[0]*J2[0][1] + n[1]*J2[1][1],
               n[0]*J2[0][2] + n[1]*J2[1][2]]];
    }
    // 식 (66)~(68): point-to-plane 3D — nᵀ · (3×6)
    function jacP2L3D(pw, n) {
      var J3 = jacP2P3D(pw), row = new Array(6).fill(0);
      for (var j = 0; j < 6; j++) for (var i = 0; i < 3; i++) row[j] += n[i]*J3[i][j];
      return [row];
    }

    // 한 번의 GN 스텝.  mode: 'p2p' | 'p2l' | 'gicp'
    //   S: source 점군(현재 자세로 이미 변환된 것이 아니라 원본), (R, t): 현재 추정
    //   opts.normals: target 법선 (p2l), opts.M: 점별 정보행렬 (gicp)
    function gnStepICP(S, T, corr, R, t, mode, opts) {
      opts = opts || {};
      var d = S[0].length, dof = (d === 2 ? 3 : 6);
      var H = zeros(dof, dof), b = new Array(dof).fill(0), chi = 0;
      var th = (d === 2) ? Math.atan2(R[1][0], R[0][0]) : 0;
      for (var c = 0; c < corr.length; c++) {
        var i = corr[c].i, j = corr[c].j;
        var pw = add(mv(R, S[i]), t);
        var ev = sub(pw, T[j]);                                // 식 (29): 예측 − 관측
        var J, e;
        if (mode === 'p2l') {
          var n = opts.normals[j];
          e = [dot(n, ev)];
          J = (d === 2) ? jacP2L2D(S[i], th, n) : jacP2L3D(pw, n);
        } else {
          e = ev;
          J = (d === 2) ? jacP2P2D(S[i], th) : jacP2P3D(pw);
        }
        var M = (mode === 'gicp') ? opts.M[c] : null;          // 식 (98): Jᵀ M J
        var JtM = mT(J);
        if (M) JtM = mm(mT(J), M);
        var Hi = mm(JtM, J), bi = mv(JtM, e);
        H = madd(H, Hi);
        for (var a = 0; a < dof; a++) b[a] += bi[a];
        chi += M ? dot(e, mv(M, e)) : dot(e, e);
      }
      for (var q = 0; q < dof; q++) H[q][q] += (opts.lam || 1e-9);
      var dx = sc(mv(minv(H), b), -1);                          // 식 (37): Δx* = −H⁻¹b
      return { dx: dx, H: H, b: b, chi: chi };
    }
    // Δx 를 (R, t) 에 적용.  2D 는 θ 를 더하고, 3D 는 좌섭동으로 곱한다.
    function applyDx(R, t, dx) {
      if (dx.length === 3 && R.length === 2) {
        var th = Math.atan2(R[1][0], R[0][0]) + dx[2];
        return { R: R2d(th), t: [t[0] + dx[0], t[1] + dx[1]] };
      }
      var dR = expSO3(dx.slice(3, 6));
      return { R: mm(dR, R), t: add(mv(dR, t), dx.slice(0, 3)) };
    }

    // 전체 ICP 루프.  method: 'svd' | 'p2p' | 'p2l' | 'gicp'
    function runICP(S, T, opts) {
      opts = opts || {};
      var d = S[0].length;
      var R = opts.R0 || eye(d), t = opts.t0 || new Array(d).fill(0);
      var iters = opts.iters === undefined ? 30 : opts.iters;
      var method = opts.method || 'svd';
      var normals = null, covT = null, covS = null;
      if (method === 'p2l') normals = normalsPCA(T, opts.k || 8).map(function (o) { return o.n; });
      if (method === 'gicp') { covT = gicpCovs(T, opts.k || 8, opts.eps);
                               covS = gicpCovs(S, opts.k || 8, opts.eps); }
      var hist = [];
      for (var it = 0; it < iters; it++) {
        var Sw = transform(S, R, t);
        var corr = nearest(Sw, T, opts.maxDist);
        if (!corr.length) break;
        hist.push({ R: R, t: t, rmse: rmse(Sw, T, corr), n: corr.length });
        if (method === 'svd') {
          var Ps = corr.map(function (c) { return Sw[c.i]; });
          var Pt = corr.map(function (c) { return T[c.j]; });
          var so = svdSolve(Ps, Pt, true);
          R = mm(so.R, R); t = add(mv(so.R, t), so.t);
        } else {
          var o2 = { lam: opts.lam };
          if (method === 'p2l') o2.normals = normals;
          if (method === 'gicp') {
            o2.M = corr.map(function (c) {
              var Cs = mm(R, mm(covS[c.i], mT(R)));            // 식 (93)
              return minv(madd(covT[c.j], Cs));                 // M = (C_{t+1} + R C_t Rᵀ)⁻¹
            });
          }
          var st = gnStepICP(S, T, corr, R, t, method, o2);
          if (!isFinite(st.dx[0])) break;
          var u = applyDx(R, t, st.dx);
          R = u.R; t = u.t;
        }
      }
      var Sf = transform(S, R, t), cf = nearest(Sf, T, opts.maxDist);
      hist.push({ R: R, t: t, rmse: rmse(Sf, T, cf), n: cf.length });
      return { R: R, t: t, hist: hist, normals: normals };
    }

    // ---- GICP 공분산 (식 88·89) --------------------------------------------
    // 법선 방향으로만 ε, 나머지는 1 인 이방성 공분산.  R_ν diag(ε,1,1) R_νᵀ.
    function gicpCovs(P, k, eps) {
      eps = (eps === undefined) ? 1e-3 : eps;
      var d = P[0].length;
      return normalsPCA(P, k || 8).map(function (o) {
        // 고유벡터 행렬의 마지막 열이 법선. 그 축만 ε 로 눌러 준다.
        var D = eye(d); D[d-1][d-1] = eps;                     // eigSym 은 내림차순 → 마지막이 법선
        var swap = zeros(d, d);
        for (var i = 0; i < d; i++) for (var j = 0; j < d; j++) swap[i][j] = o.V[i][j];
        // C = V diag(1,…,1,ε) Vᵀ  — 원문 (89) 의 R_ν diag(ε,1,1) R_νᵀ 와 축 순서만 다르다
        return mm(swap, mm(D, mT(swap)));
      });
    }
    // 식 (84)(87): 법선 방향 투영 행렬 P = n nᵀ
    function projMat(n) {
      var d = n.length, P = zeros(d, d);
      for (var i = 0; i < d; i++) for (var j = 0; j < d; j++) P[i][j] = n[i]*n[j];
      return P;
    }

return { zeros: zeros, eye: eye, mm: mm, mT: mT, madd: madd, msub: msub, mscale: mscale,
             mv: mv, minv: minv, mmaxabs: mmaxabs, blk: blk,
             nrm: nrm, unit: unit, add: add, sub: sub, sc: sc, dot: dot, cross: cross, axis: axis,
             hat: hat, vee: vee, expSO3: expSO3, logSO3: logSO3,
             JrSO3: JrSO3, JlSO3: JlSO3, JrInvSO3: JrInvSO3, JlInvSO3: JlInvSO3, AdSO3: AdSO3,
             T: T, TR: TR, Tt: Tt, Tinv: Tinv, expSE3: expSE3, logSE3: logSE3, AdSE3: AdSE3,
             QlSE3: QlSE3, QrSE3: QrSE3, JlSE3: JlSE3, JrSE3: JrSE3,
             plusSO3: plusSO3, minusSO3: minusSO3, plusSE3: plusSE3, minusSE3: minusSE3,
             scene: scene, circle3: circle3, frame: frame,
             // ── 이 스터디에서 더한 것 ──
             rng: rng, randn: randn, randnVec: randnVec, chol: chol,
             symmetrize: symmetrize, fro: fro, numJac: numJac,
             G: G, truth: truth, trueOmega: trueOmega, makeMeas: makeMeas,
             integrate: integrate, preint: preint, biasUpdate: biasUpdate,
             relFromStates: relFromStates, residual: residual,
             plot: plot, fmt: fmt,
             // ── VINS-Mono 스터디에서 더한 것 ──
             qmul: qmul, qconj: qconj, qinv: qinv, qnorm: qnorm, qunit: qunit, qxyz: qxyz,
             OmegaL: OmegaL, OmegaR: OmegaR, qLmat: qLmat, qRmat: qRmat, br3: br3, q2R: q2R, R2q: R2q,
             qexp: qexp, qlog: qlog, qsmall: qsmall,
             GW: GW, truthVI: truthVI, trueOmegaVI: trueOmegaVI, makeMeasVI: makeMeasVI,
             integrateVI: integrateVI, preintVI: preintVI, biasUpdateVI: biasUpdateVI,
             relFromStatesVI: relFromStatesVI, residualVI: residualVI,
             solveLS: solveLS, schur: schur, tangentBasis: tangentBasis,
             // ── Errors and Jacobians 스터디에서 더한 것 ──
             piH: piH, piK: piK, project: project, backProject: backProject,
             distort: distort, projectD: projectD, dpdX: dpdX, makeImage: makeImage,
             lineFromPoints: lineFromPoints, lineTransform: lineTransform,
             KLmat: KLmat, lineProject: lineProject, lineError: lineError,
             toOrthonormal: toOrthonormal, fromOrthonormal: fromOrthonormal,
             orthoUpdate: orthoUpdate, gnStep: gnStep,
             // ── Iterative Closest Point 스터디에서 더한 것 ──
             eigSym: eigSym, svd: svd, det3: det3,
             ex2D: ex2D, ex3D: ex3D, centroid: centroid, demean: demean, covXY: covXY,
             transform: transform, nearest: nearest, rmse: rmse, R2d: R2d,
             svdSolve: svdSolve, normal2D: normal2D, normalsPCA: normalsPCA,
             jacP2P2D: jacP2P2D, jacP2P3D: jacP2P3D, jacP2L2D: jacP2L2D, jacP2L3D: jacP2L3D,
             gnStepICP: gnStepICP, applyDx: applyDx, runICP: runICP,
             gicpCovs: gicpCovs, projMat: projMat };
  })();