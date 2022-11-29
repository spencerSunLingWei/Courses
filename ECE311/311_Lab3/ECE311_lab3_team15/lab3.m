%--------------------------------lab3 part4 

% parameter decalaration
M = 1000;        % kg
B = 1;           % Ns/m
g = 9.81;        % m/sec^2
a = B/M;

vdes = 14;
theta = -pi/6;
dbar = g*sin(theta);

% define LTI object with the plant transfer function
s=tf('s');
G=1/(s+a);

% define variables p1, p2, containing initial values of the poles of the CLS
p1 = 1.071;
p2 = 1.071;

% define pi control parameters
K = p1 + p2 - a; 	% p1+p2 = a+K
TI = K/(p1*p2);		% p1*p2 = K/TI

% LTI object with with the controller transfer function
C = K*(TI*s + 1)/(TI*s);

% Using C & G to define T
T = (C*G)/(1+C*G);	% T(s) = Y(s)/R(s)

% perform any pole-zero cancellations in T
T = minreal(T);

% extract the poles of T and verify that they coincide with -p1, -p2
[zero, pole, gain] = zpkdata(T);
pole = cell2mat(pole);

%---------------------lab3 output2

disp('output2.1')
disp('The initial p values are p1=1 and p2=1.')
disp('The settling time over the first 15 seconds is measured/estimated to be 5.386 sec.')
disp('The settling time after the disturbance kicks in at t = 15 seconds is measured/estimated to be 19.327 - 15.000 = 4.327 sec.')
disp(' ')

disp('output2.2')
disp('All five SPEC are met. The detailed specification are shown in the report.')
disp('The tuned p values are chosen to be the farlest number they can be in the OLHP and satisfying the inequality p1+p2<15/7+a.')
disp(' ')

disp('output2.3')
disp('The tuned p values are:')
p1
p2
disp('All five SPEC are met. The detailed specification are shown in the report.')
disp('The estimation/measurement of the settling time within the tracking error scope over the first 15 seconds (when D(s) = 0) is 5.030 sec, which is the fastest settling time with best performance that the team tied by tuning p1 and p2 values.')
disp('The settling time after the disturbance kicks in at t = 15 seconds is measured/estimated to be 18.958 - 15.000 = 3.958 sec.')
stepinfo(T)
disp('The settling time that we computed by the “stepinfo” function is 5.0329s. The approximated time we measured from the graph is 5.030s (measured using cursor), which is approximately the same.')
disp(' ')

disp('output2.4')
disp('Since the mass is on an inclined plane, by analyzing the forces existing on the mass, there is a component of the gravity is along the inclined plane pointing downwards. So in order for it to be moving at constant speed after the disturbance signal is enabled, the control signal u(t) has to settle to a nonzero value and work against that disturbance signal.')
disp('The u(t) value is approximately to be 4.919 m/s^2 by measuring using the cursor from the diagram.')
disp(' ')
