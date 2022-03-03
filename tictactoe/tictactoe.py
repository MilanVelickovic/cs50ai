"""
Tic Tac Toe Player
"""

from cmath import inf
import copy
import math
from random import randint

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves = 0
    for i in range(len(board)):
        moves += board[i].count(X)
        moves -= board[i].count(O)
        
    return X if moves == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                actions.add((row, column))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] == EMPTY and action != None:
        boardCopy = copy.deepcopy(board)
        boardCopy[action[0]][action[1]] = player(board)
        return boardCopy
    else:
        raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking rows
    for row in board:
        if all(value == row[0] for value in row):
            return row[0]
    
    # Cheking columns
    for i in range(3):
        row = []
        for j in range(3):
            row.append(board[j][i])

        if all(value == row[0] for value in row):
            return row[0]

    # Cheking diagonals
    diagonalR = [board[0][0], board[1][1], board[2][2]] # diagonal \
    diagonalL = [board[0][2], board[1][1], board[2][0]] # diagonal /

    if all(value == diagonalR[0] for value in diagonalR):
        return diagonalR[0]

    if all(value == diagonalL[0] for value in diagonalL):
        return diagonalL[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for row in board:
            for value in row:
                if value == EMPTY:
                    return False 

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        winnerIs = winner(board)
        if winnerIs == X:
            return 1
        if winnerIs == O:
            return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if not terminal(board):
        possible_actions = list(actions(board))
        if len(possible_actions) == 9:
            return possible_actions[randint(0, 8)]
        else:
            turn = player(board)
            alpha = -math.inf # max
            beta = math.inf # min
            if turn == X:
                best_move, value = maximize(board, alpha, beta)
                return best_move
            else:
                best_move, value = minimize(board, alpha, beta)
                return best_move
    
    return None    


def maximize(board, alpha, beta):
    if terminal(board):
        return (None, utility(board))
    else:
        current_best_move = None
        current_best_value = -math.inf
        for action in actions(board):
            move, value = minimize(result(board, action), alpha, beta)
            alpha = max(alpha, value)
            if value > current_best_value:
                current_best_value = value
                current_best_move = action

            if alpha >= beta:
                break

        return (current_best_move, current_best_value)


def minimize(board, alpha, beta):
    if terminal(board):
        return (None, utility(board))
    else:
        current_best_move = None
        current_best_value = math.inf
        for action in actions(board):
            move, value = maximize(result(board, action), alpha, beta)
            beta = min(beta, value)
            if value < current_best_value:
                current_best_value = value
                current_best_move = action
                
            if alpha >= beta:
                break

        return (current_best_move, current_best_value)