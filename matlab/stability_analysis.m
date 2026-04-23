% =========================================================
%  Motor Starter Stability Analysis
%  Industrial Logic & Systems Analysis Project
%
%  Author  : Maaz
%  Tool    : MATLAB Control System Toolbox
%  Purpose : Model motor starter transfer function,
%            verify stability, and tune PID controller.
% =========================================================

clc; clear; close all;

%% ── 1. SYSTEM MODEL ─────────────────────────────────────
%
%  Motor starter modeled as 1st-order system:
%
%           K
%  G(s) = ──────
%         τs + 1
%
%  K   = DC gain   (how much output responds to input)
%  τ   = Time const (how fast system reaches steady state)

K   = 2.0;   % System gain
tau = 0.5;   % Time constant (seconds)

num = [K];
den = [tau, 1];

G = tf(num, den);
disp('── Transfer Function ───────────────────────────');
disp(G);


%% ── 2. STABILITY CHECK ──────────────────────────────────
poles_G = pole(G);
fprintf('\nSystem Poles:\n');
disp(poles_G);

if all(real(poles_G) < 0)
    fprintf('✅  System is STABLE (poles in left half-plane)\n\n');
else
    fprintf('❌  System is UNSTABLE\n\n');
end


%% ── 3. OPEN-LOOP STEP RESPONSE ─────────────────────────
figure(1);
step(G);
title('Open-Loop Step Response (Motor Starter)');
xlabel('Time (s)');
ylabel('Output');
grid on;


%% ── 4. BODE PLOT ────────────────────────────────────────
figure(2);
bode(G);
title('Bode Plot — Frequency Domain Stability');
grid on;

% Get gain and phase margins
[Gm, Pm, Wcg, Wcp] = margin(G);
fprintf('── Stability Margins ────────────────────────────\n');
fprintf('  Gain Margin  : %.2f dB  (at %.2f rad/s)\n', 20*log10(Gm), Wcg);
fprintf('  Phase Margin : %.2f deg (at %.2f rad/s)\n', Pm, Wcp);
fprintf('─────────────────────────────────────────────────\n\n');


%% ── 5. PID CONTROLLER DESIGN ────────────────────────────
%
%  Adding a PID controller for closed-loop control.
%  Closed-loop: CL(s) = C(s)G(s) / (1 + C(s)G(s))

Kp = 1.5;
Ki = 0.8;
Kd = 0.1;

C  = pid(Kp, Ki, Kd);
CL = feedback(C * G, 1);

disp('── Closed-Loop Transfer Function (with PID) ────');
disp(CL);

% Check closed-loop stability
poles_CL = pole(CL);
fprintf('\nClosed-Loop Poles:\n');
disp(poles_CL);

if all(real(poles_CL) < 0)
    fprintf('✅  Closed-Loop System is STABLE\n\n');
else
    fprintf('❌  Closed-Loop System is UNSTABLE — Retune PID\n\n');
end

% Performance metrics
info = stepinfo(CL);
fprintf('── Performance Metrics ──────────────────────────\n');
fprintf('  Rise Time    : %.4f s\n',  info.RiseTime);
fprintf('  Settling Time: %.4f s\n',  info.SettlingTime);
fprintf('  Overshoot    : %.2f %%\n', info.Overshoot);
fprintf('─────────────────────────────────────────────────\n');


%% ── 6. CLOSED-LOOP STEP RESPONSE ───────────────────────
figure(3);
step(CL);
title('Closed-Loop Step Response with PID Controller');
xlabel('Time (s)');
ylabel('Motor Output');
grid on;


%% ── 7. POLE-ZERO MAP ────────────────────────────────────
figure(4);
pzmap(CL);
title('Pole-Zero Map — Closed-Loop System');
grid on;

fprintf('\n[✓] MATLAB Analysis Complete — see figures.\n');
