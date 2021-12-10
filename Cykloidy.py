import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(1)
ax1 = fig.add_subplot()

xpoczatek = -20
xkoniec = 20

ax1.set_xlim(5 * xpoczatek, 5 * xkoniec)
ax1.set_ylim(-10, 120)
ax1.set_aspect("equal")

styczna, = plt.plot([], [])
parabola, = plt.plot([], [])
trajektoria, = plt.plot([], [])

trajektoria_xdata = []
trajektoria_ydata = []
difference = 0.03
x = np.arange(xpoczatek, xkoniec, difference)
print("Function sliding: x*x + 1")
y = x**2 + 1


def updateplot1(frame):
    xA = frame - difference
    xB = frame
    yA = (frame - difference)**2 + 1
    yB = frame**2 + 1

    tmp = (yB - yA) / (xB - xA)
    ystyczne = tmp * x + yB - (tmp * xB)
    alfa = np.arctan2(yB - yA, xB - xA)

    xnew = np.cos(alfa) * x + np.sin(alfa) * ystyczne
    ynew = -np.sin(alfa) * x + np.cos(alfa) * ystyczne

    xparabola = np.cos(alfa) * x + np.sin(alfa) * y
    yparabola = -np.sin(alfa) * x + np.cos(alfa) * y - ynew[0]

    trajektoria_xdata.append(xparabola[240])
    trajektoria_ydata.append(yparabola[240])

    parabola.set_data(xparabola, yparabola)
    styczna.set_data(xnew, ynew - ynew[0])
    trajektoria.set_data(trajektoria_xdata, trajektoria_ydata)
    return styczna, parabola, trajektoria,


plot2 = plt.figure(2)
ax2 = plot2.add_subplot()

dowolna, = plt.plot([], [])
linia1, = plt.plot([], [])
linia2, = plt.plot([], [])
kolo, = plt.plot([], [])
kolotrajektoria, = plt.plot([], [])

kolotrajektoria_xdata = []
kolotrajektoria_ydata = []

isup = input("Type g if You want the circle to be above function:")
r = float(input("Input r = "))
input_function = input("Input function, where x is the argument of y = ")
#Example of input_function = "x ** 2 - 10 * x - 8"
input_function_values = eval(input_function)
reformed_input1 = input_function.replace("x", "(frame)")
reformed_input2 = input_function.replace("x", "(frame - difference)")

ax2.set_xlim(2 * xpoczatek, 2 * xkoniec)
ax2.set_ylim(-70, 70)
ax2.set_aspect("equal")


def updateplot2(frame):
    xA = frame - difference
    xB = frame
    yA = eval(reformed_input2)
    yB = eval(reformed_input1)

    if isup == "g":
        alfa = np.pi - np.arctan2(yA - yB, xA - xB)
    else:
        alfa = np.pi - np.arctan2(yB - yA, xB - xA)

    circle1 = plt.Circle((xB + r * np.sin(alfa), yB + r * np.cos(alfa)), r, color='black', fill=False, clip_on=False)
    ax2.add_patch(circle1)

    tmpx = xB + r * np.sin(alfa) + r * np.sin(frame)
    tmpy = yB + r * np.cos(alfa) + r * np.cos(frame)
    kolotrajektoria_xdata.append(tmpx)
    kolotrajektoria_ydata.append(tmpy)
    kolotrajektoria.set_data(kolotrajektoria_xdata, kolotrajektoria_ydata)

    dowolna.set_data(x, input_function_values)
    return dowolna, kolotrajektoria, circle1 #linia1, linia2,


def updateALL(frame):
    a = updateplot1(frame)
    b = updateplot2(frame)
    return a + b


ani = FuncAnimation(fig, updateALL, frames=x, interval=5, blit=True, repeat=False)

plt.show()