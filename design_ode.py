##### IMPORTS ####################
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
##################################

plt.ion() # turn interactive mode on

# Put all your variables here
# This is python, remember that numbers will round down if you're
# dividing 2 integers so make at least one of them a float, for example
#
#    1/5 = 0
#    1.0/5 + 0.2

m = 90.0                # Mass of person
g = 9.81                # Gravity
R = 0.35 #Radius of the wheel
T = 50 #Torque
rho = 1.225 #rho
A = 1.5 # Area for wind resistance
drag_coeff = 1.1 #Coefficient of Drag

# This function is all our d<something>/dt
def f(y, t):
    # y is an array of values from each step (see 311)
    P13i = y[0]
    P32i = y[1]
    Q11i = y[2]
    Q41i = y[3]

    # We added a fifth variable and equation to solve for a theta because
    # this ended up easier to do for us.
    Ti   = y[4]

    # Some geometry shit I added for convenience
    r = Q11i
    omega = P32i/J
    SE12 = m*g*math.sin(Ti)
    SE22 = m*g*math.cos(Ti)


    # the model equations
    # Whenever your equations use a state variable, use the one from the previous that came from
    # the 'y' array
    Qd11 = P13i / I13
    Qd41 = 2*P32i/(L*math.cos(Ti))
    Pd13 = SE12 - Q11i/C11 - m*omega*r*(P32i/J)
    Pd32 = ((1 + ((I23*(r**2))/J))**-1) * (r*SE22 + ((r*m*omega*P13i) / I13) - (Q41i*2 / (L*C41*math.cos(Ti))) )
    T = P32i/J

    # Return the slopes we just solved right above IN THE SAME ORDER AS YOUR 'y' ARRAY
    return [Pd13, Pd32, Qd11, Qd41, T]

# initial conditions
P13z = 0
P32z = 0
Q11z = 0.1
Q41z = 10*0.0254 - (l+0.12)
Tz = 17*math.pi / 180              # Because Radians

y0 = [P13z, P32z, Q11z, Q41z, Tz]  # initial condition vector
t = np.linspace(0, 4, 10000)       # time space. This goes from 0 to 4 seconds in 10000 steps

# solve the DEs!
soln = odeint(f, y0, t)

# The solution to each of our equations is a thing in the solution array
P13 = soln[:, 0]
P32 = soln[:, 1]
Q11 = soln[:, 2]
Q41 = soln[:, 3]
T   = soln[:, 4]

# Each blob below opens a graph for one of our state equation solutions

# plot angle
plt.figure()
plt.plot(t, T, label='Angle of Lever')
plt.xlabel('seconds')
plt.ylabel('Angle (rad)')
plt.title('Angle of Lever')
plt.legend(loc=0)

# plot Q11
plt.figure()
plt.plot(t, Q11, label='Q11')
plt.xlabel('seconds')
plt.ylabel('Q11')
plt.title('Q11 over time')
plt.legend(loc=0)

# plot Q41
plt.figure()
plt.plot(t, Q41, label='Q41')
plt.xlabel('seconds')
plt.ylabel('Q41')
plt.title('Q41 over time')
plt.legend(loc=0)

# plot P13
plt.figure()
plt.plot(t, P13, label='P13')
plt.xlabel('seconds')
plt.ylabel('P13')
plt.title('P13 over time')
plt.legend(loc=0)

# plot P32
plt.figure()
plt.plot(t, P32, label='P32')
plt.xlabel('seconds')
plt.ylabel('P32')
plt.title('P32 over time')
plt.legend(loc=0)


# Wait until all graphs are closed to close application
plt.show(block=True)
