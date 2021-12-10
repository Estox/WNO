import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(1)
ax1 = fig.add_subplot()
ax1.set_xlim(-20, 20)
ax1.set_ylim(-20, 20)
ax1.set_aspect("equal")

x = np.linspace(0, 100, 1)

r = 1

class Tygrys():
    def __init__(self):
        self.x = np.random.sample() * 20 - 10
        self.y = np.random.sample() * 20 - 10


liczba_tygrysow = 20
tygrysy, = plt.plot([], [])
linie, = plt.plot([], [])
liczba_punktow = 5
alfa = np.linspace(0, np.pi, liczba_punktow)
liczba_punktow = liczba_punktow * liczba_tygrysow


def bettercross(point1, point2, point3):
    y1 = point1[1] - point2[1]
    y2 = point1[1] - point3[1]
    x1 = point1[0] - point2[0]
    x2 = point1[0] - point3[0]
    return y2*x1 - y1*x2


def distance(point1, point2, point3):
    y1 = point1[1] - point2[1]
    y2 = point1[1] - point3[1]
    x1 = point1[0] - point2[0]
    x2 = point1[0] - point3[0]

    it1 = y1**2 + x1**2
    it2 = y2**2 + x2**2

    if it1 == it2:
        return 0
    elif it1 < it2:
        return -1
    return 1


lista_tygrysow = []

for i in range(liczba_tygrysow):
    tygrys = Tygrys()
    lista_tygrysow.append(tygrys)


def update(frame):
    xdata, ydata, resultx, resulty = [], [], [], []
    collinearPoints, tygrysy = [], []
    olddatax, olddatay = [], []

    for tygrysek in lista_tygrysow:
        tygrysek.x = tygrysek.x + np.random.sample() - 0.5
        tygrysek.y = tygrysek.y + np.random.sample() - 0.5
        olddatax.append(tygrysek.x)
        olddatay.append(tygrysek.y)

    for i in range(len(olddatax)):
        tmpx = olddatax[i] + r * np.cos(alfa)
        tmpy = olddatay[i] + r * np.sin(alfa)
        xdata.extend(tmpx)
        ydata.extend(tmpy)

    leftindex = xdata.index(min(xdata))
    current = [xdata[leftindex], ydata[leftindex]]
    start = current
    resultx.append(xdata[leftindex])
    resulty.append(ydata[leftindex])
    while True:
        nextTarget = [xdata[0], ydata[0]]
        for i in range(1, liczba_punktow):
            pointi = [xdata[i], ydata[i]]
            if [pointi] == current:
                continue

            val = bettercross(current, nextTarget, pointi)

            if val > 0:
                nextTarget = pointi
                collinearPoints = []
            elif val == 0:
                if distance(current, nextTarget, pointi) < 0:
                    collinearPoints.append(nextTarget)
                    nextTarget = pointi
                else:
                    collinearPoints.append(pointi)

        for k in collinearPoints:
            resultx.append(k[0])
            resulty.append(k[1])

        if nextTarget == start:
            break
        resultx.append(nextTarget[0])
        resulty.append(nextTarget[1])
        current = nextTarget

    resultx.append(resultx[0])
    resulty.append(resulty[0])

    linie, = plt.plot(resultx, resulty)
    tygrysy, = plt.plot(xdata, ydata, '.')
    return tygrysy, linie,


ani = FuncAnimation(fig, update, frames=x, interval=300, blit=True)

plt.show()