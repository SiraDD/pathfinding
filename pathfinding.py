import pygame
import time
import random
import numpy
from pygame.locals import *

# set up pygame window
width = 440
height = 440
fps = 30

# define colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
dark_green = (0, 150, 0)

# variables
x = 0
y = 0
w = 20  # width
grid = []
position = []
obstacle = [[0 for i in range(20)] for i in range(20)]
cellDetails = [[[99999.0 for i in range(3)] for i in range(20)] for i in range(20)]
closedList = [[0 for i in range(20)] for i in range(20)]
openList = []
found = False

# initialise pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()


def build_grid(x, y, w):
    for i in range(20):
        x = 20
        y += 20
        grid_horizontal = []
        for j in range(20):
            pygame.draw.line(screen, white, [x, y], [x + w, y])  # top
            pygame.draw.line(screen, white, [x, y + w], [x + w, y + w])  # bottom
            pygame.draw.line(screen, white, [x, y], [x, y + w])  # left
            pygame.draw.line(screen, white, [x + w, y], [x + w, y + w])
            grid_horizontal.append((x, y))
            x += 20
        grid.append(grid_horizontal)
    pygame.display.update()


def isValid(x, y):
    return True if x > 19 and x < 420 and y > 19 and y < 420 else False


def isValidIndex(x_index, y_index):
    if x_index > -1 and x_index < 20 and y_index > -1 and y_index < 20:
        return True
    else:
        return False


def isUnblocked(x_index, y_index):
    return True if obstacle[y_index][x_index] == 0 else False


def isDestination(x_index, y_index, end):
    end_index = coordToIndex(end[0], end[1])
    return True if x_index == end_index[0] and y_index == end_index[1] else False


def coordToIndex(x, y):
    return (int((x / 20) - 1), int((y / 20) - 1))


def indexToCoord(x_index, y_index):
    return ((x_index + 1) * 20, (y_index + 1) * 20)


def calcHValue(x_index, y_index, end_index):
    return max((abs(end_index[0] - x_index), abs(end_index[1] - y_index)))


def draw(x, y, colour):
    pygame.draw.rect(screen, colour, (x, y, 20, 20))
    pygame.display.update()


def round_down(num):
    return num - (num % 20)


def draw_obstacle(): # not used currently
    while event.type == MOUSEBUTTONDOWN:
        pos_raw = pygame.mouse.get_pos()
        pos_new = (round_down(pos_raw[0]), round_down(pos_raw[1]))
        position.append(pos_new)  #
        print(position)  #
        draw(pos_new[0], pos_new[1], red)


def dijkstra(start, end):
    (x_start, y_start) = start
    x_start = (x_start / 20) - 1
    y_start = (y_start / 20) - 1
    start_up = (x_start, y_start + 1)
    start_down = (x_start, y_start - 1)
    start_left = (x_start - 1, y_start)
    start_right = (x_start + 1, y_start)
    for i in obstacle:
        used = 0
        if obstacle[start_up[1]][start_up[0]] == 1:
            used = 1
        else:
            values[start_up[1]][start_up[0]] += 1


def searchPath(src_index, end_index):
    i, j = end_index
    path = []
    pathUsed = [[0 for i in range(20)] for i in range(20)]
    # N, E, S, W, NE, SE, NW, SW
    pos = [(i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j - 1),
           (i - 1, j + 1)]
    while True:
        (i_optimal, j_optimal) = (99999, 99999)
        for e in pos:
            i_current, j_current = e
            if isValidIndex(e[0], e[1]):
                if (closedList[j_current][i_current] == 1) and (pathUsed[j_current][i_current] == 0):
                    if i_optimal == 99999:
                        (i_optimal, j_optimal) = e
                    if cellDetails[j_current][i_current][1] < cellDetails[j_optimal][i_optimal][1]:
                        (i_optimal, j_optimal) = (i_current, j_current)
                    if src_index == (i_optimal, j_optimal):
                        return

        x, y = indexToCoord(i_optimal, j_optimal)
        draw(x, y, purple)
        i, j = (i_optimal, j_optimal)
        pos = [(i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j - 1),
               (i - 1, j + 1)]
        path.append((i, j))
        pathUsed[j][i] = 1
        clock.tick(60)


def aStarSearch(src, end):
    src_index = coordToIndex(src[0], src[1])
    end_index = coordToIndex(end[0], end[1])
    (i, j) = src_index
    i = int(i)
    j = int(j)
    # 0 = f, 1 = g, 2 = h
    cellDetails[j][i] = [0.0, 0.0, 0.0]

    if not isValid(src[0], src[1]):
        print("Source is invalid")
        return

    if not isUnblocked(i, j):
        print("Source is blocked")
        return

    openList.append([0, 0, (i, j)])

    while len(openList) > 0:

        smallest_f = openList[0][0]
        smallest_h = openList[0][1]
        e_final = 0
        (i, j) = openList[0][2]
        i = int(i)
        j = int(j)
        for e in range(len(openList)):
            if (openList[e][0] < smallest_f) or (openList[e][0] == smallest_f and openList[e][1] < smallest_h):
                smallest_f = openList[e][0]
                smallest_h = openList[e][1]
                (i, j) = openList[e][2]
                i = int(i)
                j = int(j)
                e_final = e

        # remove from openList
        openList.pop(e_final)

        # add to closedList
        closedList[j][i] = 1

        if len(openList) > 0:
            x, y = indexToCoord(i, j)
            draw(x, y, dark_green)

        # North
        if isValidIndex(i, j - 1):
            if isDestination(i, j - 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i, j - 1) and closedList[j - 1][i] == 0:
                gNew = cellDetails[j][i][1] + 1.0
                hNew = calcHValue(i, j - 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j - 1][i][0] > fNew:
                    openList.append([fNew, hNew, (i, j - 1)])
                    cellDetails[j - 1][i] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i, j - 1)
                    draw(x, y, green)

        # East
        if isValidIndex(i + 1, j):
            if isDestination(i + 1, j, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i + 1, j) and closedList[j][i + 1] == 0:
                gNew = cellDetails[j][i][1] + 1.0
                hNew = calcHValue(i + 1, j, end_index)
                fNew = gNew + hNew
                if cellDetails[j][i + 1][0] > fNew:
                    openList.append([fNew, hNew, (i + 1, j)])
                    cellDetails[j][i + 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i + 1, j)
                    draw(x, y, green)

        # South
        if isValidIndex(i, j + 1):
            if isDestination(i, j + 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i, j + 1) and closedList[j + 1][i] == 0:
                gNew = cellDetails[j][i][1] + 1.0
                hNew = calcHValue(i, j + 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j + 1][i][0] > fNew:
                    openList.append([fNew, hNew, (i, j + 1)])
                    cellDetails[j + 1][i] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i, j + 1)
                    draw(x, y, green)

        # West
        if isValidIndex(i - 1, j):
            if isDestination(i - 1, j, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
                # add more
            elif isUnblocked(i - 1, j) and closedList[j][i - 1] == 0:
                gNew = cellDetails[j][i][1] + 1.0
                hNew = calcHValue(i - 1, j, end_index)
                fNew = gNew + hNew
                if cellDetails[j][i - 1][0] > fNew:
                    openList.append([fNew, hNew, (i - 1, j)])
                    cellDetails[j][i - 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i - 1, j)
                    draw(x, y, green)

        # North East
        if isValidIndex(i + 1, j - 1):
            if isDestination(i + 1, j - 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i + 1, j - 1) and closedList[j - 1][i + 1] == 0:
                gNew = cellDetails[j][i][1] + 1.41
                hNew = calcHValue(i + 1, j - 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j - 1][i + 1][0] > fNew:
                    openList.append([fNew, hNew, (i + 1, j - 1)])
                    cellDetails[j - 1][i + 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i + 1, j - 1)
                    draw(x, y, green)

        # South East
        if isValidIndex(i + 1, j + 1):
            if isDestination(i + 1, j + 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i + 1, j + 1) and closedList[j + 1][i + 1] == 0:
                gNew = cellDetails[j][i][1] + 1.41
                hNew = calcHValue(i + 1, j + 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j + 1][i + 1][0] > fNew:
                    openList.append([fNew, hNew, (i + 1, j + 1)])
                    cellDetails[j + 1][i + 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i + 1, j + 1)
                    draw(x, y, green)

        # North West
        if isValidIndex(i - 1, j - 1):
            if isDestination(i - 1, j - 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
            elif isUnblocked(i - 1, j - 1) and closedList[j - 1][i - 1] == 0:
                gNew = cellDetails[j][i][1] + 1.41
                hNew = calcHValue(i - 1, j - 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j - 1][i - 1][0] > fNew:
                    openList.append([fNew, hNew, (i - 1, j - 1)])
                    cellDetails[j - 1][i - 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i - 1, j - 1)
                    draw(x, y, green)

        # South West
        if isValidIndex(i - 1, j + 1):
            if isDestination(i - 1, j + 1, end):
                print("The destination cell is found")
                searchPath(src_index, end_index)
                return
                # add more
            elif isUnblocked(i - 1, j + 1) and closedList[j + 1][i - 1] == 0:
                gNew = cellDetails[j][i][1] + 1.41
                hNew = calcHValue(i - 1, j + 1, end_index)
                fNew = gNew + hNew
                if cellDetails[j + 1][i - 1][0] > fNew:
                    openList.append([fNew, hNew, (i - 1, j + 1)])
                    cellDetails[j + 1][i - 1] = [fNew, gNew, hNew]
                    x, y = indexToCoord(i - 1, j + 1)
                    draw(x, y, green)

        clock.tick(60)
    print("Unable to find end node")
    return

def main():
    build_grid(0, 0, 20)
    print("Select starting and ending position")
    while len(position) < 2:
        ev = pygame.event.get()
        for event in ev:
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                pos_raw = pygame.mouse.get_pos()
                pos_new = (round_down(pos_raw[0]), round_down(pos_raw[1]))
                if isValid(pos_new[0], pos_new[1]):
                    position.append(pos_new)
                    draw(pos_new[0], pos_new[1], blue)
        clock.tick(60)
    # creating obstacles
    start = position[0]
    end = position[1]
    while pygame.mouse.get_pressed()[2] == 0:
        ev = pygame.event.get()
        for event in ev:
            if event.type == QUIT:
                pygame.quit()
                return
            if pygame.mouse.get_pressed()[0]:
                try:
                    pos_raw = pygame.mouse.get_pos()
                    pos_new = (round_down(pos_raw[0]), round_down(pos_raw[1]))
                    (pos_x, pos_y) = pos_new
                    pos_x = int((pos_x / 20) - 1)
                    pos_y = int((pos_y / 20) - 1)
                    indicator = 0
                    if pos_x < 20 and pos_y < 20:
                        if obstacle[pos_y][pos_x] == 1 or pos_new == position[0] or pos_new == position[1]:
                            indicator = 1
                        elif indicator == 0:
                            if pos_x > -1 and pos_y > -1:
                                obstacle[pos_y][pos_x] = 1
                                draw(pos_new[0], pos_new[1], red)
                except AttributeError:
                    pass
        clock.tick(60)
    src = start
    aStarSearch(src, end)
    while True:
        ev = pygame.event.get()
        for event in ev:
            if event.type == QUIT:
                pygame.quit()
                return
        #aStarSearch(src, end)
        clock.tick(600)


# Execute game:
main()
