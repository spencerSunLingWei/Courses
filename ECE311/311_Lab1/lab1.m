%lab1 part3-----------------------------------------------------

% Motor parameter declaration
La = 0.02;      % H
Ra = 3;         % ohms
Ke = 0.01;      % V/(rad/sec)
Kt = 0.01;      % Nm/A
I = 6*10^-4;    % Nm/(rad/sec^2)
b = 10^-4;      % Nm/(rad/sec)

% write the state-space form matrix for motor model
A = [0 1 0; 0 -b/I Kt/I; 0 -Ke/La -Ra/La];
B = [0; 0; 1/La];
C = [0 1 0];
D = 0;

% write the simplified motor model form matrix
A1 = [0 1; 0 -(b+(Ke*Kt/Ra))/I];
B1 = [0; Kt/(Ra*I)];
C1 = [0 1];
D1 = 0;

% define the state-space model of the motor
motor = ss(A,B,C,D);
motor_simplified = ss(A1, B1, C1, D1);

% convert to transfer function
G_motor = tf(motor);
G_motor_simplified = tf(motor_simplified);

% convert the object motor to ZPK form
zpk_motor = zpk(motor);

% extract the list of poles of the transfer function
[zero, pole, gain] = zpkdata(G_motor);
pole = cell2mat(pole); 

% extract numerator and denominator arrays of the transfer function
[num, den] = tfdata(G_motor);
num = cell2mat(num);
den = cell2mat(den);
% extract the arrays from the simplied version
[num1, den1] = tfdata(G_motor_simplified);
num1 = cell2mat(num1);
den1 = cell2mat(den1); 

% print desire output
disp('Lab1 part3 Output1')

disp(' ')
disp('1.1 Printed output for the transfer function G_motor')
G_motor
disp('1.2 Printed output for the simplified version of the transfer function G_motor_simplified')
G_motor_simplified

disp('2. Printed output for the ZPK form of the transfer function')
zpk_motor

disp('3.1 Printed output for the poles of the transfer function G_motor')
pole
disp('3.2 Comments on the location of the poles and expected motor behavior')
disp('As we observed from the printed output for the poles of the transfer function G_motor, we find out that the location of the two poles are on the negative real axis and are separated apart. One pole has the magnitude of 0.2223 which is much smaller than the other pole’s magnitude, which is 149.9444.')
disp('')
disp('The expected behaviour based on the location of the poles when the input voltage is a unit step is the two negative integer poles contribute exponential terms that decay with time. So, when the input voltage is a unit step, the output time response can be found as exponential functions before it reaches the steady state.')

disp(' ')
disp('4.1 Numerator array of the transfer function G_motor')
num
disp('4.2 Denominator array of the transfer function G_motor')
den
disp('4.3 Numerator array of the transfer function G_motor_simplified')
num1
disp('4.4 Denominator array of the transfer function G_motor_simplieid')
den1

%lab1 part4------------------------------------------------------

%create a figure with three subplots
figure(1);
T = linspace(0, 30, 1000);
subplot(3, 1, 1);

%plot the step response of the state space model motor
Y1 = step(motor, T);
plot(T, Y1);
xlabel('Time (s)');
ylabel('Step response of motor (rad/s)');
title('Step response of state space model motor VS Time');

%plot the step response of the simplified state space model motor_simplified
subplot(3, 1, 2);
Y2 = step(motor_simplified, T);
plot(T, Y2);
xlabel('Time (s)');
ylabel('Step response of motor_simplified (rad/s)');
title('Step response of simplied state space model motor VS Time');

%plot the difference of step responce between motor and motor_simplified
subplot(3, 1, 3);
plot(T, Y1-Y2);
maximum_error = max(abs(Y1 - Y2));
xlabel('Time (s)');
ylabel('Difference of step response (rad/s)');
title('Difference of step response between full model and simplied model VS Time');

%find the theoretical asymptotic value of the motor
% time approach infinity, s approach 0
approximate_asymptotic = Y1(end); %approximate asymptotic value using Y1 graph
syms s;
theoretical_asymptotic = limit(833.3 / (s^2 + 150.2*s + 33.33), s, 0); %theoretical asymptotic value calculated using G_motor

%plot the armature current of the full motor model vs time
figure(2);
C_armature_current = [0 0 1];
motor_armature_current = ss(A, B, C_armature_current, D);
Y3 = step(motor_armature_current, T);
plot(T, Y3);
xlabel('Time (s)');
ylabel('Amrature current (A)');
title('Armature current of the full motor model VS Time');

%plot the output response of state space model with input signal sin(T)
figure(3);
X0=[0;-1;.5];
lsim(motor, sin(T), T, X0);
Y4=lsim(motor, sin(T), T, X0);
xlabel('Time');
ylabel('Output response of motor (rad/s)');
title('Output response of state space model with input signal sin(T) VS Time');

% estimate amplitude of the oscillation when s=i
approximated_amplitude = (max(Y4(800:1000)) - min(Y4(800:1000)))/2;
s = i;
theoretical_amplitude = abs(evalfr(G_motor, s)); %theratical amplitude of absolute value of G(i) 

% print desire output
disp('Lab1 part4 Output2')

disp(' ')
disp('1. Figure 1, 2 and 3 have been plotted, along with the labels of the titles and axes.')

disp(' ')
disp('2.1 Compare the step responses of the motor model and its simplified version. How close are they to each other?')
disp('The simplified version and the actual full motor model has a very close output. The difference between the waveforms is very little. ')
disp(' ')
disp('2.2 What is the maximum error between the two?')
maximum_error

disp('3. Printed output for the approximate asymptotic value of the motor speed in response to a unit step')
approximate_asymptotic

disp('4.1 Printed output for the theoretical asymptotic value of the motor speed in response to a unit step')
theoretical_asymptotic
disp('4.2 Verify that the approximate value above is indeed very close to the theoretical value')
disp('The result is 83330 / 3333  = 25.0015, which is very close to the approximate asymptotic value.')

disp(' ')
disp('5. Printed output for the approximate amplitude of oscillation of the motor speed in response to a sinusoidal input')
approximated_amplitude
disp('6.1 Print the theoretical amplitude of oscillation of the motor speed in response to a sinusoidal input')
theoretical_amplitude
disp('6.2 compare it to the approximate value above')
disp('The magnitude of the theoretical amplitude is sqrt(1.1419^2 + 5.3035^2) = 5.4250, which is very close to the approximate amplitude value.')




