% Lab2 Part4 -----------------------------------------------------------

% Declare variables with numerical values given in the Table
M = 0.1;    % Kg
La = 0.05;  % H
Ra = 3;     % ohms
g = 9.81;   % m/(sec^2)
km = 0.1;   % N(m^2)/(A^2)

% Declar ybar representing the quilibrium value of y
% Declar a vector xbar and a scalar ubar with expressions 
% calculated in Section 3
ybar = 0.1; % m
xbar = [ybar; 0; sqrt((g * M) / km) * ybar];
ubar = Ra * sqrt((g * M) / km) * ybar;

% using the command linmod calling the Simulink model to find A,B,C,D
% of the numerical linearization at xbar, ubar
[A, B, C, D] = linmod('lab2_1', xbar, ubar);

% Declar A1, B1, C1, D1 containing the expressions for the theoretical
% linearization matrices found in Section 3.
A1 = [0 1 0; (2*g)/ybar 0 (-2)*sqrt((g*km)/M)*(1/ybar); 0 0 (-1)*(Ra/La)];
B1 = [0; 0; 1/La];
C1 = [1 0 0];
D1 = [0];

% compute the error between theoretical and numerically derived matrices.
err_A = norm(A - A1);
err_B = norm(B - B1);

% Using A1,B1,C1,D1, find the transfer function of the linearized model
% define the state-space model
ss_model = ss(A1, B1, C1, D1);
% convert to transfer function
G = tf(ss_model);

% Extract the list of poles of the transfer function
[zero, pole, gain] = zpkdata(G);
pole = cell2mat(pole); 

% Compute the eigenvalues of A1
e = eig(A1);

% print desired output
disp('Lab2 part4 Output2')
disp(' ')
% 
disp('2.1.1 Print the numerically derived matrices A,B')
A
B
disp('2.1.2 Print the theoretically derived counterparts A1,B1.')
A1
B1
% 
disp('2.2.1 Print the error for the derived numerically and theoretically matrices.')
err_A
err_B

disp('2.2.2 Comment on the accrucay.')
disp(' ')
disp('The errors between the theoretically derived and the numerically approximated matrices are in the order')
disp('of 1e-06 and 1e-11 respectively, which is so small that the difference between them can be ignored in practice.')
disp('Therefore, the numerical approximation performed by Matlab/Simulink has really high accuracy.')
disp(' ')

disp('2.3.1 Printed eigenvalue of A1 and the poles of G.')
e
pole

disp('2.3.2 Is the linearized model internally stable?')
disp(' ')
disp('The linearized model is internally unstable, as one of the eigenvalues of A1 is 14.0071, which has a real part > 0, resulting in an unstable system.')
disp(' ')

disp('2.3.3 Is the linearized model BIBO stable?')
disp(' ')
disp('The model is also not BIBO stable, since one of the poles of G is 14.0071, which has a real part > 0, resulting in an unstable system.')
disp(' ')

disp('2.3.4 Comment on how your findings about stability conform with physical intuition.')
disp(' ')
disp('The above findings conform with the physical intuition of the problem. There are two forces acting ')
disp('on the steel ball, where one of them is the force imparted by the electromagnet, and the other force') 
disp('is the gravity of the ball itself. The ball can stay still if and only if the ball is initially static,') 
disp('and the electromagnetic force always cancels out with gravity. Otherwise, the ball will move. If the') 
disp('ball moves closer to the electromagnet, then the electromagnetic force will be greater than the gravity') 
disp('and the ball will be attracted by the electromagnet, resulting in a constantly decreasing y. If the ball')
disp('moves away from the electromagnet, the electromagnetic force will become less than the gravity, so the') 
disp('ball will keep falling, resulting in a constantly increasing y. In either case, the value of y will explode')
disp('and result in a system that is neither internally stable nor BIBO stable.')
disp(' ')

% Lab2 Part5 -----------------------------------------------------------

K= 100;
z=10;
p=100;

s = tf('s');
CONTROLLER = K*(s+z)/(s+p);

denominator = 1- CONTROLLER * G;
[zero, pole, gain] = zpkdata(denominator);
cell2mat(zero);

disp('Lab2 par5 Output3')
disp(' ')

disp('3.1 Print the value of K you found above.')
K

disp('3.2 Describe the procedure you followed in finding K, and any observations you made along the way.')
disp(' ')
disp('The following procedures are followed when finding K with observations provided along the way. The team first') 
disp('started from K = 10, increasing K by increments of 10, repeating the following procedures until we found the')
disp('desired K value. ')
disp(' ')
disp('      1. Constructing the controller function based on formula K * (s+z)/(s+p), where K = K, z = 10 and p = 100.')
disp('      2. In order to find the poles of the closed-loop system transfer function, we compute the roots/zeros of the ')
disp('      denominator 1-C(s)G(s) using the zpkdata() function. ')
disp('      3. Printing the roots of the 1-CONTROLLER G(s).')
disp('      4. Plotting the roots using the rlocus() function, with zeros labelled as “о”. ')
disp('      5. Determine whether the output function at the time domain is BIBO stable or not based on THM2. If all roots')
disp('      are on the open left half-plane, the system is BIBO stable.')

disp(' ')
disp('As we increased the K value, we discovered that the fourth root on the right half-plane, initially when K=10,')
disp('is moving towards the left. When K is increased to 100, all roots are landed on the open left half-plane.')
disp(' ')

disp('3.3.1 Print the range of initial condition y(0).')
disp(' ')
disp('Rough upper limits = 18.8m')
disp('Rough lower limits = 0.06m')
disp(' ')

disp('3.3.2 Comment on why your controller does not work for initial conditions that are far from the equilibrium.')
disp(' ')
disp('The controller is designed to stabilize the linearization and then applied to the nonlinear model. As we declared ')
disp('within the code previous part, y =0.1m is the equilibrium value. The system is nonlinear, so we are applying the')
disp('linearization of the model at the equilibrium point. Since the linearization method is taking the gradient of the ')
disp('vector function, it will only be accurate if it is near that equilibrium. So, by initializing y(0) exceeding the ')
disp('range from 0.06 to 18.8, it becomes far from the equilibrium point, so the linearization accuracy will be low, which ')
disp('leads to the instability of the output.')

disp(' ')

rlocus(denominator)

