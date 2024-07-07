"""
Tic Tac Toe Player
"""

import math

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
    lessRepeated = X;
    for row in board:
        xTimes = row.count(X)
        yTimes = row.count(O)

        if xTimes < yTimes or xTimes is yTimes:
            lessRepeated = X
        else:
            lessRepeated = O

    return lessRepeated
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = {}
    for rowIdx, row in enumerate(board):
       for colIdx, val in enumerate(row):
           actions.add((rowIdx, colIdx))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        if board[action[0]][action[1]] is not EMPTY:
            raise NameError("Action not valid")
        
        board[action[0]][action[1]] = player(board);
    except:
        raise NameError("Action not valid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    players = [X, O]

    winner = None

    for player in players:
        if checkHorizontaly(board, player) or checkVerticaly(board, player) or checkDiagonally(board, player)
            winner = player
    
    return winner

def checkHorizontaly(board, player):
    for row in board:
        if row.count(player) is 3:
            return True;
    
def checkVerticaly(board, player):
    for col in range(3):
        if board[0][col] is not player:
            return False
        
    return True

def checkDiagonally(board, player):
    colIndex = 0
    for row in board:
        if row[colIndex] is not player:
            return False
        colIndex += 1 

    for row in board:
        if row[colIndex] is not player:
            return False
        colIndex -= 1 
    
    return True

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
