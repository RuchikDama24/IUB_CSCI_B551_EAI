#
# pikachu.py : Play the game of Pikachu
#
# Ruchik Dama(rdama). Shashank kumar(sk128),sumanth gopalkrishna(sgopalk)
#
# Based on skeleton code by D. Crandall, March 2021

import sys
import copy
sys.setrecursionlimit(10**6)
from datetime import datetime
startTime = datetime.now()
def successors(player,board2d,evalw,evalb):
    succ=[]
    for i in range(len(board2d)-1):
        for j in range(len(board2d)):
            if board2d[i][j] == player:
                if player in "wb":
                    oppn="b" if player=="w" else "w"
                    if player=="w":
                        if board2d[i + 1][j] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            if i + 1 == len(board2d) - 1:
                                tempboard[i + 1][j] = player.upper()
                            else:
                                tempboard[i + 1][j] = player
                            succ.append(tempboard)
                        if i < len(board2d) - 2 and board2d[i + 1][j] in "bB" and board2d[i + 2][j] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            tempboard[i + 1][j] = "."
                            if i + 2 == len(board2d) - 1:
                                tempboard[i + 2][j] = player.upper()
                            else:
                                tempboard[i + 2][j] = player
                            succ.append(tempboard)
                    else:
                        if board2d[i - 1][j] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            if i - 1 == 0:
                                tempboard[i - 1][j] = player.upper()
                            else:
                                tempboard[i - 1][j] = player
                            succ.append(tempboard)
                        elif i > 1 and board2d[i - 1][j] in "wW" and board2d[i - 2][j] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            tempboard[i - 1][j] = "."
                            if i - 2 == 0:
                                tempboard[i - 2][j] = player.upper()
                            else:
                                tempboard[i - 2][j] = player
                            succ.append(tempboard)
                    #Horizontal Moves
                    if board2d[i][j - 1] == "." and j!=0:
                        tempboard = copy.deepcopy(board2d)
                        tempboard[i][j] = "."
                        tempboard[i][j - 1] = player
                        succ.append(tempboard)
                    if (board2d[i][j - 1] ==oppn or board2d[i][j - 1] ==oppn.upper()) and j!=0:
                        if j==1:
                            continue
                        if board2d[i][j - 2] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            tempboard[i][j - 1] = "."
                            tempboard[i][j - 2] = "w"
                            succ.append(tempboard)
                    if j!=len(board2d)-1 and board2d[i][j + 1] == "." :
                        tempboard = copy.deepcopy(board2d)
                        tempboard[i][j] = "."
                        tempboard[i][j + 1] = player
                        succ.append(tempboard)
                    if j<len(board2d)-2 and (board2d[i][j + 1] ==oppn or board2d[i][j + 1] ==oppn.upper()) and board2d[i][j + 2] == ".":
                        if j == len(board2d) - 2:
                            continue
                        if board2d[i][j + 2] == ".":
                            tempboard = copy.deepcopy(board2d)
                            tempboard[i][j] = "."
                            tempboard[i][j + 1] = "."
                            tempboard[i][j + 2] = "b"
                            succ.append(tempboard)

    #Pikachu
    for i in range(len(board2d)):
        for j in range(len(board2d)):
            if board2d[i][j] == player:
                if player in "WB":
                    oppn = "B" if player == "W" else "W"
                    l1, l3 = 0, 0
                    l2, l4 = len(board2d), len(board2d)
                    b1 = -1  # Initialisinig b1 & b2 (if b or B found then b1 and b2 would be replaced with the position
                    b2 = -1
                    for k in range(i - 1, -1, -1):
                        if (board2d[k][j] ==player or board2d[k][j] ==player.lower()):
                            l1 = k
                            break
                    for k in range(i + 1, len(board2d)):
                        if (board2d[k][j] ==player or board2d[k][j] ==player.lower()):
                            l2 = k
                            break
                    for k in range(j - 1, -1, -1):
                        if (board2d[i][k] ==player or board2d[i][k] ==player.lower()):
                            l3 = k
                            break
                    for k in range(j + 1, len(board2d)):
                        if (board2d[i][k] ==player or board2d[i][k] ==player.lower()):
                            l4 = k
                            break
                    a = []
                    for k in range(l1, i):
                        if (board2d[k][j] ==oppn or board2d[k][j] ==oppn.lower()):
                            a.append(k)
                    if a != []:
                        b1 = a[-1]
                        b2 = j
                        if len(a) == 1:
                            l1 = 0
                        else:
                            l1 = a[-2]
                    for k in range(l1,i):
                        tempboard = copy.deepcopy(board2d)
                        if b1 == 0 or b1==len(board2d)-1:
                            continue
                        if k>b1:
                                if tempboard[k][j] == ".":
                                    tempboard[i][j] = "."
                                    tempboard[k][j] = player
                        else:
                            if k == b1: #position of "b"
                                continue
                            elif tempboard[k][j] == ".":
                                tempboard[i][j] = "."
                                tempboard[k][j] = player
                                if b1 != -1:
                                    tempboard[b1][b2]="."
                                if b1 ==len(board2d)-1:
                                    tempboard[b1][b2] = player
                        succ.append(tempboard)
                    b1, b2 = -1, -1
                    for k in range(i + 1, l2):
                        if (board2d[k][j] ==oppn or board2d[k][j] ==oppn.lower()):
                            if b1 != -1:
                                l2 = k
                                break
                            b1, b2 = k, j
                    for k in range(i + 1, l2):
                        tempboard = copy.deepcopy(board2d)
                        if b1 == 0 or b1 == len(board2d) - 1:
                            continue
                        if k < b1:
                            if tempboard[k][j] == ".":
                                tempboard[i][j] = "."
                                tempboard[k][j] = player
                        else:
                            if k == b1:
                                continue
                            elif tempboard[k][j] == ".":
                                tempboard[i][j] = "."
                                tempboard[k][j] = player
                                if b1 != -1:
                                    tempboard[b1][b2] = "."
                                if b1 == len(board2d) - 1:
                                    tempboard[b1][b2] = player
                        succ.append(tempboard)
                    b1, b2 = -1, -1
                    a = []
                    for k in range(l3, j):
                        if (board2d[i][k] ==oppn or board2d[i][k] ==oppn.lower()):
                            a.append(k)
                    if a != []:
                        b1 = i
                        b2 = a[-1]
                        if len(a) == 1:
                            l3 = 0
                        else:
                            l3 = a[-2]
                    # print(b1)
                    for k in range(l3, j):
                        tempboard = copy.deepcopy(board2d)
                        if b2 == 0 or b2 == len(board2d) - 1:
                            continue
                        tempboard[i][j] = "."
                        if k > b2:
                            if tempboard[i][k] == ".":
                                tempboard[i][k] = player
                        else:
                            if k == b2:  # position of "b"
                                continue
                            elif tempboard[i][k] == ".":
                                tempboard[i][k] = player
                                if b1 != -1:
                                    tempboard[b1][b2] = "."
                                if b1 == len(board2d) - 1:
                                    tempboard[b1][b2] = player
                        succ.append(tempboard)
                    b1,b2=-1,-1
                    for k in range(j + 1, l4):
                        if (board2d[i][k] ==oppn or board2d[i][k] ==oppn.lower()):
                            if b1 != -1:
                                l4 = k
                                break
                            b1, b2 = i, k
                    for k in range(j + 1, l4):
                        tempboard = copy.deepcopy(board2d)
                        if b2==0 or b2==len(board2d)-1:
                            continue
                        if k < b2:
                            if tempboard[i][k] == ".":
                                tempboard[i][j] = "."
                                tempboard[i][k] = player
                        else:
                            if k == b2:
                                continue
                            elif tempboard[i][k] == ".":
                                tempboard[i][j] = "."
                                tempboard[i][k] = player
                                if b1 != -1:
                                    tempboard[b1][b2] = "."
                                if b1 == len(board2d) - 1:
                                    tempboard[b1][b2] = player
                        succ.append(tempboard)
    if board2d in succ:
        succ.remove(board2d)
    return succ

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def oneDtotwoD(board,N):
    j = 0
    s = []
    for row in range(N):
        inner_list = []
        for col in range(N):
            inner_list.append(board[j])
            j += 1
            #print(j)
        s.append(inner_list)
        #print(j)
    return s
def twoDtooneD(board2d):
    board=""
    for row in range(len(board2d)):
        for col in range(len(board2d)):
            board+=board2d[row][col]
    return board

def is_goal(board2d):
    w=0
    b=0
    for i in range(len(board2d)):
        for j in range(len(board2d)):
            if board2d[i][j] in "wW":
                w+=1
            if board2d[i][j] in "bB":
                b+=1
    if w==0 or b==0:
        return True
    else:
        return False
def list_add(list1,list2):
    list3 = []
    for i in list1:
        list3.append(i)
    for j in list2:
        list3.append(j)
    return list3

def evaluation_function(board2d):
    costw=0
    costb=0
    for i in range(len(board2d)):
        for j in range(len(board2d)):
            if board2d[i][j]=="w":
                costw+=10
            if board2d[i][j]=="W":
                costw+=40
            if board2d[i][j]=="B":
                costb+=40
            if board2d[i][j]=="b":
                costb+=10
    return costw-costb

#For Minimax and aplha-beta pruning algorithm we refered https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm
def minimax(board2d,depth,targetdepth,maxplayer):
    if depth==targetdepth:
        return (evaluation_function(board2d),board2d)
    val_board=copy.deepcopy(board2d)
    if maxplayer:
        value=-9999
        for elem in list_add(successors("w", board2d, 0, 0), successors("W", board2d, 0, 0)):
            val=minimax(elem,depth+1,targetdepth,False)
            value=max(value,val[0])
            #value=max(value,maxi)
            if value==val[0]:
                val_board=copy.deepcopy(val[1])
        return (value,val_board)
    else:
        value=9999
        for elem in list_add(successors("b", board2d, 0, 0), successors("B", board2d, 0, 0)):
            val = minimax(elem, depth + 1, targetdepth, True)
            value = min(value, val[0])
            #value = min(value, mini)
            if value == val[0]:
                val_board = copy.deepcopy(val[1])
        return (value, val_board)

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    board2d=copy.deepcopy(oneDtotwoD(board,N))
    print(len(list_add(successors("w",board2d,0,0),successors("W",board2d,0,0))))
    if player in "wW":
        maxplayer=True
        value=-99999
    else:
        maxplayer=False
        value = 99999
    output_board=copy.deepcopy(board2d)
    depth=0
    cur_board=copy.deepcopy(board2d)
    while not is_goal(cur_board):
        depth+=1
        for elem in successors(player,board2d,0,0):
            cur_value, cur_board = minimax(elem, 0, depth, maxplayer)
            if player in "wW":
                if cur_value > value:
                    value = cur_value
                    output_board = copy.deepcopy(elem)
            else:
                if cur_value < value:
                    value = cur_value
                    output_board = copy.deepcopy(elem)
        print(depth)
        print("Time taken to run the script in sec =" + str(datetime.now() - startTime))
        yield twoDtooneD(output_board)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)