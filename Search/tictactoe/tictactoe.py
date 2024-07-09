"""
Tic Tac Toe Player
"""

import math
import copy

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
    xTimes = 0
    oTimes = 0
    for row in board:
        xTimes += row.count(X)
        oTimes += row.count(O)

    if xTimes < oTimes or xTimes is oTimes:
        return X
    else:
        return O
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for rowIdx, row in enumerate(board):
       for colIdx, cell in enumerate(row):
           if cell is EMPTY: actions.add((rowIdx, colIdx))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        copyBoard = copy.deepcopy(board)
        
        if copyBoard[action[0]][action[1]] is not EMPTY:
            raise NameError("Action not valid")
        if action[0] > len(copyBoard) or action[1] > len(copyBoard[0]) or action[0] < 0 or action[1] < 0:
            raise NameError("Action not valid")
        
        copyBoard[action[0]][action[1]] = player(copyBoard);
        
        return copyBoard
    except:
        raise NameError("Action not valid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    players = [X, O]

    winner = None

    for player in players:
        if checkHorizontaly(board, player) or checkVerticaly(board, player) or checkDiagonally(board, player):
            winner = player
    
    return winner

def checkHorizontaly(board, player):
    for row in board:
        if row.count(player) == 3:
            return True;
    
def checkVerticaly(board, player):
    for col in range(3):      
        count = 0;   
        for row in range(3):
            if board[row][col] is player:
                count += 1            
            if count == 3: return True
        
    return False

def checkDiagonally(board, player):
    colIndex = 0
    count = 0
    for row in board:
        if row[colIndex] is player:
            count += 1
        if count == 3:
            return True        
        colIndex += 1 

    colIndex = len(board) - 1;
    count = 0

    for row in board:
        if row[colIndex] is player:
            count += 1
        if count == 3:
            return True        
        colIndex -= 1 
    
    return False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) is None and hasEmptySpaces(board)):
        return False
    
    return True

def hasEmptySpaces(board):
    for row in board:
        for player in row:
            if player is EMPTY:
                return True
    
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gameWinner = winner(board)

    if gameWinner is X:
        return 1
    if gameWinner is O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return None
    
    if player(board) is X:
        return maxVal(board)["action"]
    else:
        return minVal(board)["action"]
        
def maxVal(board):
    if terminal(board):
        return { "value": utility(board) }
    
    currVal = -(math.inf)
    
    bestMove = None
    for action in actions(board):
        minValue = minVal(result(board, action))
        '''
            Not using "max" because we need to store the best action when
            the new value is bigger than the currently stored (Better move)
        '''
        if minValue["value"] > currVal:
            currVal = minValue["value"]
            bestMove = action
            # If the new value is the max score, return directly so its faster
            if currVal == 1:
                return { "value": currVal, "action": action }
    
    # If it hasnt returned anything, return the current better move
    return { "value": currVal, "action": bestMove }

def minVal(board):
    if terminal(board):
        return { "value": utility(board) }
    
    currVal = math.inf
    
    bestMove = None
    for action in actions(board):
        maxValue = maxVal(result(board, action))
        '''
            Not using "min" because we need to store the best action when
            the new value is lower than the currently stored (Better move)
        '''
        if maxValue["value"] < currVal:
            currVal = maxValue["value"]
            bestMove = action
            # If the new value is the min score, return directly so its faster
            if currVal == -1:
                return { "value": currVal, "action": action }
    
    # If it hasnt returned anything, return the current better move
    return { "value": currVal, "action": bestMove }