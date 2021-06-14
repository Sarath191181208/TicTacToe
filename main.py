import math
import random
board = []
player = 'X'
computer = 'O'
currentPlayer = player.upper()

print(random.choice([6, 4, 5, 4, 2, 6, 7, 8, (8, 9)]))


def createBoard(grid: int) -> list[int]:
    board = []
    for i in range(grid):
        helper = []
        for j in range(grid):
            helper.append(0)
        board.append(helper)
    return board


def checkWinner(board):
    #  checking rows
    for i in range(len(board)):
        if board[i][0] != 0:
            res = all(ele == board[i][0] for ele in board[i])
            if res == True:
                return board[i][0]
    # checking coloums
    for i in range(len(board)):
        if board[0][i] != 0:
            res = all(ele[i] == board[0][i] for ele in board)
            if res == True:
                return board[0][i]
    # checking diagonals
        # principal diagonal
        if board[0][0] != 0:
            res = all(board[i][i] == board[0][0] for i in range(len(board)))
            if res == True:
                return board[0][0]
        # other diagonal
        if board[0][len(board)-1] != 0:
            res = all(board[i][j] == board[0][len(board)-1]
                      for i, j in zip(range(0, len(board), 1), range(len(board)-1, -1, -1)))
            if res == True:
                return board[0][len(board)-1]


def noOfspaces(board) -> int:
    k = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if not board[i][j]:
                k += 1
    return k


def printBoard(board: list[int]) -> None:
    for i in range(len(board)):
        print("-----------------")
        for j in range(len(board[0])):
            txt = board[i][j]
            if txt == 0:
                txt = " "
            print("| "+txt, end=" ")
        print("|")


def available_moves(board):
    spaces = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                spaces.append((i, j))
    return spaces


def miniMax(state, player, computer):
    maxPlayer = computer
    otherPlayer = "O" if player == 'X' else 'X'
    if checkWinner(state) != None:
        spaces = noOfspaces(state)+1
        return {
            'position': None,
            'score': 1 * spaces if otherPlayer == maxPlayer else -1 * spaces,
        }
    if noOfspaces(state) == 0:
        return {
            'position': None,
            'score': 0
        }
    if player == maxPlayer:
        best = {
            'position':  None,
            'score': -math.inf,
        }
    else:
        best = {
            'position': None,
            'score': math.inf,
        }
    for possible_moves in available_moves(state):
        x, y = possible_moves
        state[x][y] = player

        sim_score = miniMax(state, otherPlayer, computer)

        board[x][y] = 0
        sim_score['position'] = (x, y)
        if player == maxPlayer:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best


run = True
board = createBoard(3)
printBoard(board)
# print(checkWinner(
#     [
#         ['X', 0, 0],
#         [0, 'X', 0],
#         [0, 0, 'X']
#     ]
# ))
while run:
    if currentPlayer == player:
        choice = int(input(f"enter the {currentPlayer} poisition : "))
        board[choice//3][choice % 3] = currentPlayer
    if currentPlayer == player:
        currentPlayer = computer
        pos = miniMax(board, currentPlayer, computer)
        pos = pos['position']
        x, y = pos
        print(pos)
        board[x][y] = computer
        currentPlayer = computer
    else:
        currentPlayer = player
    if checkWinner(board) != None:
        print(checkWinner(board))
        run = False
    printBoard(board)
