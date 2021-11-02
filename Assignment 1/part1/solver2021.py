#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by:  Ayush Sanghavi sanghavi, Vighnesh Kolhatkar vkolhatk,Ruchik Dama rdama
#
# Based on skeleton code by D. Crandall, January 2021
# Discussed wih Shashank Kumar

import sys
import heapq as hq

ROWS = 4
COLS = 5


def printable_board(board):
    return [('%3d ') * COLS % board[j:(j + COLS)] for j in range(0, ROWS * COLS, COLS)]


import copy

# Referred from the misere tic tac toe python file
def rowLeftShift(state, r):
    state[r] = state[r][1:] + state[r][:1]
    return state

# Referred from the misere tic tac toe python file
def rowRightShift(state, r):
    state[r] = state[r][-1:] + state[r][:-1]
    return state


# Used from the misere tic tac toe python file.
def transpose_board(board):
    return [list(col) for col in zip(*board)]


def oneDtotwoD(state1):
    j = 0
    s = []
    for row in range(ROWS):
        inner_list = []
        for col in range(COLS):
            inner_list.append(state1[j])
            j += 1
            #print(j)
        s.append(inner_list)
        #print(j)
    return s


def heuristic(state):
    end_state = []
    h = 0
    for i in range(ROWS * COLS):
        end_state.append(i + 1)
    end_state = oneDtotwoD(end_state)
    for i in range(ROWS):
        for j in range(COLS):
            if (end_state[i][j] != state[i][j]):
                h += 1

    return h


# return a list of possible successor states
def successors(state):
    succ = []
    for i in range(ROWS):
        # s = state
        if i % 2 == 0:
            a = rowLeftShift(copy.deepcopy(state), i)
            if i==0:
                p="L1"
            if i==2:
                p="L3"
            succ.append([a,p])
        if i % 2 == 1:
            a = rowRightShift(copy.deepcopy(state), i)
            if i==1:
                p="R2"
            if i==2:
                p="R4"
            succ.append([a,p])
        #  print(s,i)
    s = transpose_board(copy.deepcopy(state))
    for i in range(COLS):
        if i % 2 == 0:
            a = rowLeftShift(copy.deepcopy(s), i)
            a = transpose_board(a)
            if i==0:
                p="U1"
            if i==2:
                p="U3"
            if i==4:
                p="U5"
            succ.append([a,p])
        if i % 2 == 1:
            a = rowRightShift(copy.deepcopy(s), i)
            a = transpose_board(a)
            if i==1:
                p="D2"
            if i==3:
                p="D4"
            succ.append([a,p])

    return succ


# check if we've reached the goal
def is_goal(state):
    #return heuristic(state) == 0
    end_state = []
    h = 0
    for i in range(ROWS * COLS):
        end_state.append(i + 1)
    end_state = oneDtotwoD(end_state)
    return end_state==state


def f(s,g):
    return heuristic(s)+g


def solve(initial_board):
    fringe = []
    hq.heapify(fringe)
    initial_state = oneDtotwoD(initial_board)
    cost = 0
    explored = []
    hq.heappush(fringe, (heuristic(initial_state), cost, initial_state, []))
    while len(fringe) > 0:
        (fs, cost, state, path) = hq.heappop(fringe)
        explored.append(state)
        for succ in successors(state):
            if is_goal(succ[0]):
                path += [succ[1]]
                print("Goal State")
                return path
            elif succ[0] in explored:
                continue
            else:
                hq.heappush(fringe, (heuristic(succ[0]) + cost, cost + 1, succ[0], path + [succ[1]]))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
