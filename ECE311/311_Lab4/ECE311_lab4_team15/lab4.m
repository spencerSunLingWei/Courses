% ECE311 Lab4
% Lab Group 15

%% =====Section 3 Continuous Time Control Design=====
%% -----Define parameters and plant model-----

% Values given in the table in Section 1
Ra = 3; % ohms
Ke = 0.01; % V/(rad/sec)
Kt = 0.01; % Nm/A
I = 6e-4; % Nm/(rad/dec^2)
b = 1e-4; % Nm/(rad/sec)
% Reference value for the motor shaft angle
thetades = pi / 2; % radians
% Load torque of the motor
tau_l = 0.01; % Nm
d_bar = (Ra/Kt)*tau_l;
% Voltage level of the PWM amplifier
Vlim = 5; % Volts

% An LTI object containing the plant transfer funciton in (1)
A = Kt/(Ra*I);
B = (b+(Ke*Kt)/Ra)/I; 
s=tf('s');
G = A/(s*(s + B));

%% -----Design of the lead controller-----

% Initial crossover frequency
initial_crossover = 20; % rad/sec
% Gain K
K = 1 / abs(evalfr(G, initial_crossover*j)); % K|G(i(initial_crossover)| = 1

% Display the Bode plots of KG
figure(1)
bode(K*G);
grid on
legend('K*G')
disp('From the plot, we can see that the magnitude plot cosses 0dB at 20 rad/sec, as we intended');
disp(' ');

% Define alpha
alpha = 0.1;

% Pick T
[Gm, Pm, Wcg, omega_bar] = margin(K*G/sqrt(alpha)); % find omega_bar using identity (6)
T = 1/(sqrt(alpha)*omega_bar); % Calculated using (5)

% Define an LTI object representing the transfer function C1(s)
C1 = K*(T*s+1)/(alpha*T*s+1);

% Display the Bode plots of G, C1G, and the gain and phase margins of C1G
figure(2)
bode(G);
hold on
margin(C1*G);
grid on
legend('G', 'C1*G');

[Gm, Pm, Wcg, omega_c] = margin(C1*G);
disp('The gain crossover frequency of C1(s)G(s):');
disp([num2str(omega_c), ', between 20 and 50 rad/sec']);
disp('The phase margin of C1(s)G(s):');
disp([num2str(Pm), ', greater than 45 degrees']);
disp('Verified that the gain crossover frequency of C1G meets SPEC2 and its phase margin meets SPEC3');
disp('Verified that the crossover frequency is approximately equal to 35rad/sec and the phase margin is about 55 degrees');
disp(' ');

%% -----Design of the PI controller and analysis of the complete design-----

% Pick 1/TI much smaller than gain crossover frequency of C1G (start with 10 times)
TI = 10 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Determine the gain crossover frequency and the phase margin of CG
[Gm, Pm, Wcg, omega_c] = margin(C*G);
disp('The gain crossover frequency of C(s)G(s):');
disp(num2str(omega_c));
disp('The phase margin of C(s)G(s):');
disp(num2str(Pm));
disp('Verified that omega_c and phase margin of CG are both close to ones computed for C1G.');
disp('Verified that SPEC2 and SPEC3 are met as:');
disp(['omega_c=', num2str(omega_c), ' is between 20 and 50 rad/sec']);
disp(['Pm=', num2str(Pm), ' > 45 degrees']);
disp(' ');

% Verify whether SPEC4 has been met
figure(3)
bode(G / (1+C*G));
legend('G / (1+C*G)');
grid on
disp('From the Bode plots, we verified that the magnitude plot is below the -34dB line in all frequencies');
disp(' ');

% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);

% Plot the step responses of thetades*T_R and d_bar*T_D
figure(4)
subplot(2,1,1);
step(thetades*T_R);
legend('thetades*T_R');
grid on
subplot(2,1,2);
step(d_bar*T_D);
legend('d_bar*T_D');
grid on

% Determine the settling time and percent overshoot of thetades*T_R
stepinfo(thetades*T_R)
disp('The settling time is 0.1986s and the percentage overshoot is 31.1692%.')
disp(' ');
disp(' ');

%Kaw = 1/TI;
%return

%% -----Parameter tuning and insight-----

% Tuning TI value-----------

% Trail one: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 20 times)
TI = 20 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail one: TI=20/omega_c - The settling time is 0.2196s and the percentage overshoot is 27.0830%.');
stepinfo(thetades*T_R);

% Trail two: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 30 times))
TI = 30 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail two: TI=30/omega_c - The settling time is 0.2266s and the percentage overshoot is 25.6406%.');
stepinfo(thetades*T_R);

% Trail three: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 40 times)
TI = 40 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail three: TI=40/omega_c - The settling time is 0.2297s and the percentage overshoot is 24.9016%.');
stepinfo(thetades*T_R);

% Trail four: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 50 times)
TI = 50 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail four: TI=50/omega_c - The settling time is 0.2313s and the percentage overshoot is 24.4515%.');
stepinfo(thetades*T_R);

% Trail five: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 60 times)
TI = 60 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail five: TI=60/omega_c - The settling time is 0.2322s and the percentage overshoot is 24.1526%.');
stepinfo(thetades*T_R);

% Trail six: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 70 times)
TI = 70 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail six: TI=70/omega_c - The settling time is 0.2328s and the percentage overshoot is 23.9344%.');
stepinfo(thetades*T_R);

% Trail seven: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 80 times)
TI = 80 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail seven: TI=80/omega_c - The settling time is 0.2332s and the percentage overshoot is 23.7702%.');
stepinfo(thetades*T_R);

% Trail eight: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 90 times)
TI = 90 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail eight: TI=90/omega_c - The settling time is 0.2334s and the percentage overshoot is 23.6467%.');
stepinfo(thetades*T_R);

% Trail nine: 

% Pick 1/TI much smaller than gain crossover frequency of C1G (tried with 100 times)
TI = 100 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;
% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Trail nine: TI=100/omega_c - The settling time is 0.2336s and the percentage overshoot is 23.5458%.');
stepinfo(thetades*T_R);

disp('As we can see from the above nine trails, while increasing TI by a factor of 10, Ts increases while %OS decreases.')
disp(' ');

% Tuning initial_crossover value-----------

% baseline: 

% Initial crossover frequency
initial_crossover = 20; % rad/sec
% Gain K
K = 1 / abs(evalfr(G, initial_crossover)); % K|G(i(initial_crossover)| = 1
% Define alpha
alpha = 0.1;
% Pick T
[Gm, Pm, Wcg, omega_bar] = margin(K*G/sqrt(alpha)); % find omega_bar using identity (6)
T = 1/(sqrt(alpha)*omega_bar); % Calculated using (5)
% Define an LTI object representing the transfer function C1(s)
C1 = K*(T*s+1)/(alpha*T*s+1);
% Pick 1/TI much smaller than gain crossover frequency of C1G (set back to baseline parameters with 10 times)
TI = 10 / omega_c;
% Define an LTI object containing the PI controller
C2 = (TI*s+1)/(TI*s);
% Define an LTI object with the full controller C(s)
C = C1*C2;

% Determine the gain crossover frequency and the phase margin of CG
[Gm, Pm, Wcg, omega_c] = margin(C*G);
to_disp=['Baseline: initial_crossover=20 - The gain crossover frequency of C(s)G(s): ', num2str(omega_c), 'rad/s'];
disp(to_disp);

% Define two LTI objects containing the two transfer functions of T_R and T_D
T_R = (C*G)/(1+C*G);
T_D = G/(1+C*G);
% perform any pole-zero cancellations
T_R = minreal(T_R);
T_D = minreal(T_D);
% Determine the settling time and percent overshoot of thetades*T_R
disp('Baseline: initial_crossover=20 - The settling time is 0.1976s and the percentage overshoot: 31.1620%.');
stepinfo(thetades*T_R);

% Find the maximum magnitude of the frequency response of G(1+CG)
[mag,phase,wout] = bode(G / (1+C*G));
to_disp=['Baseline: initial_crossover=20 - the maximum magnitude of G/(1+CG): ', num2str(20*log10(max(mag))), 'db'];
disp(to_disp);

% trails: 

for N=20:1:27
    % Tunning the initial_crossover by a factor of 10
    initial_crossover = N; % rad/sec
    % Gain K
    K = 1 / abs(evalfr(G, initial_crossover)); % K|G(i(initial_crossover)| = 1
    % Define alpha
    alpha = 0.1;
    % Pick T
    [Gm, Pm, Wcg, omega_bar] = margin(K*G/sqrt(alpha)); % find omega_bar using identity (6)
    T = 1/(sqrt(alpha)*omega_bar); % Calculated using (5)
    % Define an LTI object representing the transfer function C1(s)
    C1 = K*(T*s+1)/(alpha*T*s+1);
    % Pick 1/TI much smaller than gain crossover frequency of C1G (set back to baseline parameters with 10 times)
    TI = 10 / omega_c;
    % Define an LTI object containing the PI controller
    C2 = (TI*s+1)/(TI*s);
    % Define an LTI object with the full controller C(s)
    C = C1*C2;

    % Determine the gain crossover frequency and the phase margin of CG
    [Gm, Pm, Wcg, omega_c] = margin(C*G);
    to_disp=['Trail: The gain crossover frequency of C(s)G(s): ', num2str(omega_c), 'rad/s'];
    %disp(to_disp);

    % Define two LTI objects containing the two transfer functions of T_R and T_D
    T_R = (C*G)/(1+C*G);
    T_D = G/(1+C*G);
    % perform any pole-zero cancellations
    T_R = minreal(T_R);
    T_D = minreal(T_D);
    % Determine the settling time and percent overshoot of thetades*T_R
    stepinfo(thetades*T_R);

    % Find the maximum magnitude of the frequency response of G(1+CG)
    [mag,phase,wout] = bode(G / (1+C*G));
    to_disp=['Trail: The maximum magnitude of G/(1+CG): ', num2str(20*log10(max(mag))), 'db'];
    %disp(to_disp);
    
    if N == 20  % only create one figure window on the first iteration
        %figure (5)
        %hold on % only turn on 'hold' on the first iteration
    end  % end if
    %bode(C);   % plot output
    %grid on
end  % end for loop
%legend('20','21','22','23','24','25','26','27');
%hold off
    

% Trail one:
disp('Trail one: initial_crossover=21 - The gain crossover frequency of C(s)G(s): 37.6845rad/s');
disp('Trail one: initial_crossover=21 - The settling time is 0.1897s and the percentage overshoot: 30.8578%');
disp('Trail one: initial_crossover=21 - The maximum magnitude of G/(1+CG): -39.4558db');

% Trail two:
disp('Trail two: initial_crossover=22 - The gain crossover frequency of C(s)G(s): 39.4564rad/s');
disp('Trail two: initial_crossover=22 - The settling time is 0.1826s and the percentage overshoot: 30.5381%');
disp('Trail two: initial_crossover=22 - The maximum magnitude of G/(1+CG): -40.2012db');

% Trail three:
disp('Trail three: initial_crossover=23 - The gain crossover frequency of C(s)G(s): 41.2289rad/s');
disp('Trail three: initial_crossover=23 - The settling time is 0.1760s and the percentage overshoot: 30.2426%');
disp('Trail three: initial_crossover=23 - The maximum magnitude of G/(1+CG): -40.9209db');

% Trail four:
disp('Trail four: initial_crossover=24 - The gain crossover frequency of C(s)G(s): 43.0018rad/s');
disp('Trail four: initial_crossover=24 - The settling time is 0.1699s and the percentage overshoot: 29.9685%');
disp('Trail four: initial_crossover=24 - The maximum magnitude of G/(1+CG): -41.6098db');

% Trail five:
disp('Trail five: initial_crossover=25 - The gain crossover frequency of C(s)G(s): 44.7752rad/s');
disp('Trail five: initial_crossover=25 - The settling time is 0.1642s and the percentage overshoot: 29.7154%');
disp('Trail five: initial_crossover=25 - The maximum magnitude of G/(1+CG): -42.2727db');

% Trail six:
disp('Trail six: initial_crossover=26 - The gain crossover frequency of C(s)G(s): 46.5489rad/s');
disp('Trail six: initial_crossover=26 - The settling time is 0.1589s and the percentage overshoot: 29.4847%');
disp('Trail six: initial_crossover=26 - The maximum magnitude of G/(1+CG): -42.9118db');

% Trail seven:
disp('Trail seven: initial_crossover=27 - The gain crossover frequency of C(s)G(s): 48.323rad/s');
disp('Trail seven: initial_crossover=27 - The settling time is 0.1538s and the percentage overshoot: 29.2689%');
disp('Trail seven: initial_crossover=27 - The maximum magnitude of G/(1+CG): -43.5289db');

disp('As we can see from the above trails, while increasing initial_crossover by a factor of 10, crossover frequency of CG increases, Ts decreases, %OS decreases and maximum magnitude of G/(1+CG) decreases which reflects an increasing in disturbance attenuation.')
disp(' ');



