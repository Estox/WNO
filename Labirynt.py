import numpy as np
from numpy.random import randint as rand
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as patches


def draw_maze(cells):
    for k, column in enumerate(cells):
        for i, cell in enumerate(column):
            if i % 2 == 0 and k % 2 == 0 or i % 2 == 1 and k % 2 == 1:
                # South wall
                if cell[3] == 1:
                    line = Line2D([cell[0] - 1, cell[0] + 1], [cell[1] - 1, cell[1] - 1])
                    ax.add_line(line)
                # East wall
                if cell[4] == 1:
                    line = Line2D([cell[0] + 1, cell[0]], [cell[1] - 1, cell[1] + 1])
                    ax.add_line(line)
                # West wall
                if cell[5] == 1:
                    line = Line2D([cell[0] - 1, cell[0]], [cell[1] - 1, cell[1] + 1])
                    ax.add_line(line)
            else:
                # North wall
                if cell[2] == 1:
                    line = Line2D([cell[0] - 1, cell[0] + 1], [cell[1] + 1, cell[1] + 1])
                    ax.add_line(line)
                # East wall
                if cell[4] == 1:
                    line = Line2D([cell[0] + 1, cell[0]], [cell[1] + 1, cell[1] - 1])
                    ax.add_line(line)
                # West wall
                if cell[5] == 1:
                    line = Line2D([cell[0] - 1, cell[0]], [cell[1] + 1, cell[1] - 1])
                    ax.add_line(line)


def init_cells():
    cells = np.ones((width, height, 7))
    for i in range(height):
        cells[:, i, 0] = np.linspace(1, width, width)
    for i in range(width):
        cells[i, :, 1] = np.linspace(1, height * 2 - 1, height)
    cells[:, :, 6] = 0  # if visited
    # print(cells)
    return cells


def DFS(cells):
    x, y = 0, 0
    triangular = np.array([[cells[x, y, 0]-1, cells[x, y, 1]-1], [cells[x, y, 0]+1, cells[x, y, 1]-1],
                           [cells[x, y, 0], cells[x, y, 1]+1]])
    t1 = plt.Polygon(triangular, color='gray')
    ax.add_patch(t1)

    # bottom left corner cell visited flag setting (starting point):
    cells[x, y, 6] = 1
    stack = []
    stack.append([x, y])
    nr_of_non_visited = np.where(cells[:, :, 6] == 0)
    while len(nr_of_non_visited[0]):
        # non visited neighbours:
        non_vis_nbrs = []
        if x > 0 and cells[x-1, y, 6] == 0:  # West = 5
            non_vis_nbrs.append([x-1, y, 5])
        if y > 0 and cells[x, y-1, 6] == 0 and not(x % 2 == 1 and y % 2 == 0) and not(x % 2 == 0 and y % 2 == 1):  # South = 3
            non_vis_nbrs.append([x, y-1, 3])
        if x < width-1 and cells[x+1, y, 6] == 0:  # East = 4
            non_vis_nbrs.append([x+1, y, 4])
        if y < height-1 and cells[x, y+1, 6] == 0 and not(x % 2 == 0 and y % 2 == 0) and not(x % 2 == 1 and y % 2 == 1):  # North = 2
            non_vis_nbrs.append([x, y+1, 2])
        if len(non_vis_nbrs) > 1:
            #print("non vis")
            which = rand(0, len(non_vis_nbrs))
            #print(which)
            x_, y_, side = non_vis_nbrs[which]
        elif len(non_vis_nbrs) == 1:
            x_, y_, side = non_vis_nbrs[0]
        if x_ != x or y_ != y:
            stack.append([x_, y_])
            cells[x_, y_, 6] = 1
            cells[x, y, side] = 0
            if side == 2 or side == 4:
                side += 1
            else:
                side -= 1
            cells[x_, y_, side] = 0
            x, y = x_, y_
        else:
            stack.pop()
            x, y = stack[-1]
            x_, y_ = x, y
        nr_of_non_visited = np.where(cells[:, :, 6] == 0)
        #print(non_vis_nbrs)
    if width % 2 == 1:
        triangular = np.array([[cells[-1, -1, 0] - 1, cells[-1, -1, 1] + 1], [cells[-1, -1, 0] + 1, cells[-1, -1, 1] + 1],
                               [cells[-1, -1, 0], cells[-1, -1, 1] - 1]])
    else:
        triangular = np.array([[cells[-1, -1, 0] - 1, cells[-1, -1, 1] - 1], [cells[-1, -1, 0] + 1, cells[-1, -1, 1] - 1],
             [cells[-1, -1, 0], cells[-1, -1, 1] + 1]])
    t1 = plt.Polygon(triangular, color='gray')
    ax.add_patch(t1)
    rand(0, 3)  # 0 - North, 1 - South, 2 - East, 3 - West

    return cells


def solver(cells):
    new_cells = cells
    new_cells[:, :, 6] = 0
    our_map = {}
    matrix = np.zeros([height, width])
    matrix[height - 1][0] = 1
    cell = 0
    column = 0
    move = 2
    p = str([column, cell])
    our_map[p] = 1
    nr_of_non_visited = np.where(matrix[:, :] == 0)
    while len(nr_of_non_visited[0]):
        if matrix[0][width - 1] != 0:
            break
        keys = [k for k, v in our_map.items() if float(v) == move - 1]

        while keys:
            i0 = list(keys[0])
            i0.remove("[")
            i0.remove("]")
            i0.remove(",")
            column, cell = int(''.join(i0[0:i0.index(" ")])), int(''.join(i0[i0.index(" ")+1:]))
            if new_cells[column, cell, 6] == 0:
                if new_cells[column][cell][2] == 0 and matrix[height - cell - 2][column] == 0:
                    matrix[height - cell - 2][column] = move
                    p = str([column, cell + 1])
                    our_map[p] = move
                if new_cells[column][cell][3] == 0 and matrix[height - cell][column] == 0:
                    matrix[height - cell][column] = move
                    p = str([column, cell - 1])
                    our_map[p] = move
                if new_cells[column][cell][4] == 0 and matrix[height - 1 - cell][column + 1] == 0:
                    matrix[height - 1 - cell][column + 1] = move
                    p = str([column + 1, cell])
                    our_map[p] = move
                if new_cells[column][cell][5] == 0 and matrix[height - 1 - cell][column - 1] == 0:
                    matrix[height - 1 - cell][column - 1] = move
                    p = str([column - 1, cell])
                    our_map[p] = move
                new_cells[column, cell, 6] = 1
            keys.pop(0)
        move += 1
        nr_of_non_visited = np.where(matrix[:, :] == 0)
    return matrix


def pathseeker(matrix, cells):
    column = width - 1
    row = 0
    value = matrix[row][column]
    path = []
    while value > 1:
        if row > 0 and cells[column][height - 1 - row][2] == 0 and matrix[row - 1][column] == value - 1:
            path.append(2)
        if row < height - 1 and cells[column][height - 1 - row][3] == 0 and matrix[row + 1][column] == value - 1:
            path.append(3)
        if column < width - 1 and cells[column][height - 1 - row][4] == 0 and matrix[row][column + 1] == value - 1:
            path.append(4)
        if column > 0 and cells[column][height - 1 - row][5] == 0 and matrix[row][column - 1] == value - 1:
            path.append(5)
        if path[-1] == 2:
            row -= 1
        elif path[-1] == 3:
            row += 1
        elif path[-1] == 4:
            column += 1
        elif path[-1] == 5:
            column -= 1
        value -= 1
    return path


def draw_path(path):
    x = width

    if width % 2 == 0:
        isit = 1
        y = 2 * height - 4 / 3
    else:
        isit = 0
        y = 2 * height - 2 / 3

    for index, line in enumerate(path):
        if index % 2 == isit:
            if line == 5:
                line = Line2D([x, x - 1], [y, y - 2/3], color='red')
                ax.add_line(line)
                x -= 1
                y -= 2/3
            if line == 4:
                line = Line2D([x, x + 1], [y, y - 2/3], color='red')
                ax.add_line(line)
                x += 1
                y -= 2/3
            if line == 2:
                line = Line2D([x, x], [y, y + 4/3], color='red')
                ax.add_line(line)
                y += 4/3
        else:
            if line == 5:
                line = Line2D([x, x - 1], [y, y + 2/3], color='red')
                ax.add_line(line)
                x -= 1
                y += 2/3
            if line == 4:
                line = Line2D([x, x + 1], [y, y + 2/3], color='red')
                ax.add_line(line)
                x += 1
                y += 2/3
            if line == 3:
                line = Line2D([x, x], [y, y - 4/3], color='red')
                ax.add_line(line)
                y -= 4/3


height = 10
width = 15

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
ax.set_xlim(-2, width+3)
ax.set_ylim(-2, height*2+2)
ax.set_aspect("equal")

cells = init_cells()
cells = DFS(cells)
draw_maze(cells)
matrix = solver(cells)
path = pathseeker(matrix, cells)
draw_path(path)
plt.show()
