import math
import time
import pygame
import random

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption("N Queen")
FPS = 20

# colours
BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
RED = (230, 20, 40)
BLUE = (20, 80, 220)

OClr = BLUE
XClr = RED
txtClr = BLACK
boardClr = WHITE

playerScorePos = (30, 560)
compScorePos = (300, 560)


def PYtxt(txt: str, fontSize: int = 28, fontColour: tuple = BLACK, font: str = 'freesansbold.ttf'):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


class tic_tac_toe():

    def __init__(self, grid, width, height, currentPlayer) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.player = 'X'
        self.computer = 'O'
        self.board = self.create_board(self.grid)
        self.cubes = [
            [Cube(self.board[i][j], i, j, width, height, self.grid)
             for j in range(self.grid)]
            for i in range(self.grid)
        ]
        self.available_moves = self.moves()
        self.currentPlayer = currentPlayer
        self.winner = None
        self.playerWins = 0
        self.compWins = 0

    def create_board(self, grid):
        board = []
        for i in range(grid):
            helper = []
            for j in range(grid):
                helper.append(0)
            board.append(helper)
        self.grid = len(board)
        return board

    def drawGrid(self):
        WIN.fill(boardClr)
        rowGap = self.height / self.grid
        colGap = self.width / self.grid
        # Draw Cubes
        for i in range(self.grid):
            for j in range(self.grid):
                self.cubes[i][j].draw(WIN)

        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.grid+1):
            pygame.draw.line(WIN, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)

        for i in range(self.grid):
            pygame.draw.line(WIN, BLACK, (i*colGap, 0), (colGap*i, self.width))
        WIN.blit(PYtxt(f"playerScore : {self.playerWins}"), playerScorePos)
        WIN.blit(PYtxt(f"computer : {self.compWins}"), compScorePos)
        pygame.display.update()

    def print_board(self):
        for i in range(len(self.board)):
            print("-----------------")
            for j in range(len(self.board[0])):
                txt = self.board[i][j]
                if txt == 0:
                    txt = " "
                print("| "+txt, end=" ")
            print("|")

    def moves(self):
        spaces = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    spaces.append((i, j))
        return spaces

    def checkWinner(self, pos):
        i, j = pos
        # checking row
        if self.board[i][0] != 0:
            res = all(ele == self.board[i][0] for ele in self.board[i])
            if res == True:
                return self.board[i][0]
        # checking in a col
        if self.board[0][j]:
            res = all(ele[j] == self.board[0][j] for ele in self.board)
            if res == True:
                return self.board[0][j]
        # checking principal diagonal
        if i == j or i == len(self.board)-1-j:
            if self.board[0][0] != 0:
                res = all(self.board[i][i] == self.board[0][0]
                          for i in range(len(self.board)))
                if res == True:
                    return self.board[0][0]
            if self.board[0][len(self.board)-1] != 0:
                res = all(self.board[i][j] == self.board[0][len(
                    self.board)-1]for i, j in zip(range(0, len(self.board), 1), range(len(self.board)-1, -1, -1)))
                if res == True:
                    return self.board[0][len(self.board)-1]

    def place_ai(self, pos, player):
        x, y = pos
        self.board[x][y] = player
        self.winner = self.checkWinner(pos)

    def place_board(self, pos, player):
        x, y = pos
        if self.board[x][y] == 0:
            self.board[x][y] = player
            self.cubes[x][y].value = player
            self.winner = self.checkWinner(pos)
            if self.winner == self.computer:
                self.compWins += 1
            elif self.winner != None:
                self.playerWins += 1
            return True
        else:
            print("Illegal move")
            return False


class Cube():
    def __init__(self, value, row, col, width, height, grid):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.grid = grid
        self.centerFactor = 10

    def draw(self, win):
        # fnt = pygame.font.SysFont("comicsans", 40)
        textCorrectionFactor = 64
        rowGap = self.height / self.grid
        # colGap = self.width / self.grid
        x = self.col * rowGap
        y = self.row * rowGap

        if self.value != 0:
            # fnt = pygame.font.SysFont("comicsans", 40)
            # text = fnt.render(self.value, 1, txtClr)
            if self.value == 'X':
                text = PYtxt(self.value, int(rowGap)-textCorrectionFactor, RED)
            else:
                text = PYtxt(self.value, int(rowGap) -
                             textCorrectionFactor, BLUE)
            win.blit(text, (x + (rowGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))


# def moves(board):
#     spaces = []
#     for i in range(len(board)):
#         for j in range(len(board)):
#             if board[i][j] == 0:
#                 spaces.append((i, j))
#     return spaces


def miniMax(board, player):
    moves = len(board.moves())
    if moves == len(board.board)**2:
        return {
            'position': random.choice([(0, 0), (1, 1), (2, 2), (2, 0)]),
        }

    maxPlayer = board.computer
    otherPlayer = board.player if player == board.computer else board.computer
    if board.winner != None:
        spaces = len(board.available_moves) + 1
        return {
            'position': None,
            'score': 1 * spaces if otherPlayer == maxPlayer else -1 * spaces,
        }
    if moves == 0:
        return {
            'position': None,
            'score': 0
        }
    if player == maxPlayer:
        best = {
            'position': None,
            'score': -math.inf
        }
    else:
        best = {
            'position': None,
            'score': math.inf,
        }
    for possible_moves in board.moves():
        x, y = possible_moves
        board.place_ai((x, y), player)
        sim_score = miniMax(board, otherPlayer)
        board.place_ai((x, y), 0)
        sim_score['position'] = (x, y)
        if player == maxPlayer:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best


def main():
    board = tic_tac_toe(3, 540, 540, 'X')
    # board.print_board()
    run = True
    board.drawGrid()
    itr = 0
    # game Loop
    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        if board.currentPlayer == board.player:
            # choice = int(
            #     input(f"enter the {board.currentPlayer} poisition : "))
            # board.place_board((choice//3, choice % 3), board.player)
            # board.currentPlayer = board.computer
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if board.place_board((y//(540//3), x//(540//3)), board.player):
                    board.currentPlayer = board.computer
                    board.drawGrid()
        else:
            # choice = int(
            #     input(f"enter the {board.currentPlayer} poisition : "))
            # board.place_board((choice//3, choice % 3), board.computer)
            if pygame.mouse.get_pressed()[0]:
                pos = miniMax(board, board.computer)
                pos = pos['position']
                # for slowing the ai
                if itr:
                    time.sleep(0.5)
                if not pos == None:
                    board.place_board(pos, board.computer)
                itr += 1
            # board.print_board()
            # if pygame.mouse.get_pressed()[0]:
            #     x, y = pygame.mouse.get_pos()
            #     board.place_board((y//(540//3), x//(540//3)), board.computer)
            #     board.currentPlayer = board.player
            board.drawGrid()
            board.currentPlayer = board.player
            # this is needed to dont skip the check of the above block and exec the whole programm again
            time.sleep(1)
        if board.winner != None or len(board.moves()) == 0:
            print(board.winner)
            board.board = board.create_board(board.grid)
            for i in range(board.grid):
                for j in range(board.grid):
                    board.cubes[i][j].value = 0
            board.drawGrid()
            board.winner = None
            itr = 0

    pygame.quit()


if __name__ == '__main__':
    main()
