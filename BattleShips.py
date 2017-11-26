#   ____        _   _   _           _     _
#  | __ )  __ _| |_| |_| | ___  ___| |__ (_)_ __  ___
#  |  _ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \/ __|
#  | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) \__ \
#  |____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/|___/
#                                          |_|
#
botName='MiddleBlue-4'

from random import randint, choice
import json
# These are the only additional libraries available to you. Uncomment them
# to use them in your solution.
#
import numpy  # Base N-dimensional array package


# import pandas   # Data structures & analysis

# =============================================================================
# This calculateMove() function is where you need to write your code. When it
# is first loaded, it will play a complete game for you using the Helper
# functions that are defined below. The Helper functions give great example
# code that shows you how to manipulate the data you receive and the move
# that you have to return.
#
def calculateMove(gameState):
    if "handCount" not in persistentData:
        persistentData["handCount"] = 0
    if gameState["Round"] == 0:

        move = spaceDeployRandomly(gameState)
    else:
        persistentData["handCount"] += 1
        scores = calculateScores(gameState)
        move = maxHit(scores)
        # move = chooseRandomValidTarget(gameState)
    print(str(persistentData["handCount"]) + '. MOVE: ' + str(move))
    return move


# =============================================================================
# The code below shows a selection of helper functions designed to make the
# time to understand the environment and to get a game running as short as
# possible. The code also serves as an example of how to manipulate the myBoard
# and oppBoard dictionaries that are in gameState.



# Deploys all the ships randomly on a blank board
def deployRandomly(gamestate):
    move = []  # Initialise move as an emtpy list
    orientation = None
    row = None
    column = None
    for i in range(len(gamestate["Ships"])):  # For every ship that needs to be deployed
        deployed = False
        while not deployed:  # Keep randomly choosing locations until a valid one is chosen
            row = randint(0, len(gamestate["MyBoard"]) - 1)  # Randomly pick a row
            column = randint(0, len(gamestate["MyBoard"][0]) - 1)  # Randomly pick a column
            orientation = choice(["H", "V"])  # Randomly pick an orientation
            if deployShip(row, column, gamestate["MyBoard"], gamestate["Ships"][i], orientation,
                          i):  # If ship can be successfully deployed to that location...
                deployed = True  # ...then the ship has been deployed
        move.append({"Row": chr(row + 65), "Column": (column + 1),
                     "Orientation": orientation})  # Add the valid deployment location to the list of deployment locations in move
    return {"Placement": move}  # Return the move


# Deploys all the ships randomly on a blank board
def spaceDeployRandomly(gamestate):
    move = []  # Initialise move as an emtpy list
    orientation = None
    row = None
    column = None
    for i in range(len(gamestate["Ships"])):  # For every ship that needs to be deployed
        deployed = False
        count = 0
        while not deployed:  # Keep randomly choosing locations until a valid one is chosen
            row = randint(0, len(gamestate["MyBoard"]) - 1)  # Randomly pick a row
            column = randint(0, len(gamestate["MyBoard"][0]) - 1)  # Randomly pick a column
            orientation = choice(["H", "V"])  # Randomly pick an orientation
            if count < 40:
                if deployShipWithSpace(row, column, gamestate["MyBoard"], gamestate["Ships"][i], orientation,
                                       i):  # If ship can be successfully deployed to that location...
                    deployed = True  # ...then the ship has been deployed
            else:
                if deployShip(row, column, gamestate["MyBoard"], gamestate["Ships"][i], orientation,
                              i):  # If ship can be successfully deployed to that location...
                    deployed = True  # ...then the ship has been deployed
            count = count + 1

        move.append({"Row": chr(row + 65), "Column": (column + 1),
                     "Orientation": orientation})  # Add the valid deployment location to the list of deployment locations in move
    return {"Placement": move}  # Return the move


# Returns whether given location can fit given ship onto given board and, if it can, updates the given board with that ships position
def deployShip(i, j, board, length, orientation, ship_num):
    if orientation == "V":  # If we are trying to place ship vertically
        if i + length - 1 >= len(board):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i + l][j] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            board[i + l][j] = str(ship_num)  # Place the ship on the board
    else:  # If we are trying to place ship horizontally
        if j + length - 1 >= len(board[0]):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i][j + l] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            board[i][j + l] = str(ship_num)  # Place the ship on the board
    return True  # Ship deployed


# Returns whether given location can fit given ship onto given board and, if it can, updates the given board with that ships position
def deployShipWithSpace(i, j, board, length, orientation, ship_num):
    if orientation == "V":  # If we are trying to place ship vertically
        if i + length - 1 >= len(board):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i + l][j] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed

        # liangtou
        if (i + l + 1 < len(board)):
            if board[i + l + 1][j] != "" and board[i + l + 1][j] != "L":
                return False

        if (i - 1 >= 0):
            if board[i - 1][j] != "" and board[i - 1][j] != "L":
                return False

        # liangbian
        for l in range(length):  # For every section of the ship
            if (j + 1 < len(board)):
                if board[i + l][j + 1] != "" and board[i + l][j + 1] != "L":
                    return False  # Ship not deployed

        for l in range(length):  # For every section of the ship
            if (j - 1 >= 0):
                if board[i + l][j - 1] != "" and board[i + l][j - 1] != "L":
                    return False  # Ship not deployed

        for l in range(length):  # For every section of the ship
            board[i + l][j] = str(ship_num)  # Place the ship on the board
    else:  # If we are trying to place ship horizontally
        if j + length - 1 >= len(board[0]):  # If ship doesn't fit within board boundaries
            return False  # Ship not deployed
        for l in range(length):  # For every section of the ship
            if board[i][j + l] != "":  # If there is something on the board obstructing the ship
                return False  # Ship not deployed

        # liangtou
        if (j + l + 1 < len(board)):
            if board[i][j + l + 1] != "" and board[i][j + l + 1] != "L":
                return False

        if (j - 1 >= 0):
            if board[i][j - 1] != "" and board[i][j - 1] != "L":
                return False

        # liangbian
        for l in range(length):  # For every section of the ship
            if (i + 1 < len(board)):
                if board[i + 1][j + l] != "" and board[i + 1][j + l] != "L":
                    return False  # Ship not deployed

        for l in range(length):  # For every section of the ship
            if (i - 1 >= 0):
                if board[i - 1][j + l] != "" and board[i - 1][j + l] != "L":
                    return False  # Ship not deployed

        for l in range(length):  # For every section of the ship
            board[i][j + l] = str(ship_num)  # Place the ship on the board

    return True  # Ship deployed


# Randomly guesses a location on the board that hasn't already been hit
def chooseRandomValidTarget(gamestate):
    valid = False
    row = None
    column = None
    while not valid:  # Keep randomly choosing targets until a valid one is chosen
        row = randint(0, len(gamestate["MyBoard"]) - 1)  # Randomly pick a row
        column = randint(0, len(gamestate["MyBoard"][0]) - 1)  # Randomly pick a column
        if gamestate["OppBoard"][row][column] == "":  # If the target is sea that hasn't already been guessed...
            valid = True  # ...then the target is valid
    move = {"Row": chr(row + 65),
            "Column": (column + 1)}  # Set move equal to the valid target (convert the row to a letter 0->A, 1->B etc.)
    return move  # Return the move


# Returns a list of the lengths of your opponent's ships that haven't been sunk
def shipsStillAfloat(gamestate):
    afloat = []
    ships_removed = []

    for k in range(len(gamestate["Ships"])):  # For every ship
        afloat.append(gamestate["Ships"][k])  # Add it to the list of afloat ships
        ships_removed.append(False)  # Set its removed from afloat list to false
    for i in range(len(gamestate["OppBoard"])):
        for j in range(len(gamestate["OppBoard"][0])):  # For every grid on the board
            for k in range(len(gamestate["Ships"])):  # For every ship
                if str(k) in gamestate["OppBoard"][i][j] and not ships_removed[
                    k]:  # If we can see the ship number on our opponent's board and we haven't already removed it from the afloat list
                    afloat.remove(gamestate["Ships"][
                                      k])  # Remove that ship from the afloat list (we can only see an opponent's ship number when the ship has been sunk)
                    ships_removed[
                        k] = True  # Record that we have now removed this ship so we know not to try and remove it again
    return afloat  # Return the list of ships still afloat


# Returns a list of cells adjacent to the input cell that are free to be targeted (not including land)
def selectUntargetedAdjacentCell(row, column, oppBoard):
    adjacent = []  # List of adjacent cells
    if row > 0 and oppBoard[row - 1][column] == "":  # If there is a cell above
        adjacent.append((row - 1, column))  # Add to list of adjacent cells
    if row < len(oppBoard) - 1 and oppBoard[row + 1][column] == "":  # If there is a cell below
        adjacent.append((row + 1, column))  # Add to list of adjacent cells
    if column > 0 and oppBoard[row][column - 1] == "":  # If there is a cell left
        adjacent.append((row, column - 1))  # Add to list of adjacent cells
    if column < len(oppBoard[0]) - 1 and oppBoard[row][column + 1] == "":  # If there is a cell right
        adjacent.append((row, column + 1))  # Add to list of adjacent cells
    return adjacent


# Given a valid coordinate on the board returns it as a correctly formatted move
def translateMove(row, column):
    return {"Row": chr(row + 65), "Column": (column + 1)}


def calculateScores(gamestate):
    scores = numpy.zeros((len(gamestate["OppBoard"]), len(gamestate["OppBoard"][0])))
    remainedShips = shipsStillAfloat(gamestate)
    sortedShips = numpy.sort(remainedShips)
    highScore = len(remainedShips) * 2
    # print(gamestate["OppBoard"])
    for row in range(len(gamestate["OppBoard"])):
        for column in range(len(gamestate["OppBoard"][0])):  # For every grid on the board
            if gamestate["OppBoard"][row][column] == "" or gamestate["OppBoard"][row][column] == "H":
                addedScoresV = calculateVerticalScoreByPossibleBoatNumber(row, column, gamestate["OppBoard"],
                                                                          sortedShips)
                lengthV = len(addedScoresV)
                addedScoresH = calculateHorizentalScoreByPossibleBoatNumber(row, column, gamestate["OppBoard"],
                                                                            sortedShips)
                lengthH = len(addedScoresH)
                # print("added",addedScoresV)
                # print(addedScoresV)
                scores[row:row + lengthV, column] = scores[row:row + lengthV, column] + addedScoresV
                scores[row, column:column + lengthH] = scores[row, column:column + lengthH] + addedScoresH
                # print(numpy.max(scores))
            if gamestate["OppBoard"][row][column] != "":
                scores[row, column] = 0
            if row > 6 and column>6:
                if (numpy.max(scores) == highScore):
                    return scores
                    # print(gamestate["ResponseDeadline"])
    return scores


def calculateVerticalScoreByPossibleBoatNumber(i, j, board, sortedShips):
    score = numpy.zeros((max(sortedShips)))
    returnedScoreLength = 0
    shipNumber = len(sortedShips)
    boardLen = len(board)
    # if orientation == "V":  # If we are trying to place ship vertically
    for length in sortedShips:
        if i + length > boardLen:  # If ship doesn't fit within board boundaries
            returnedScoreLength = 1
            return score[0:returnedScoreLength]  # Ship not possible
        difference = length - returnedScoreLength
        start = i + returnedScoreLength
        increase = 1
        for l in range(difference):  # For every section of the ship
            if board[start + l][j] != "" and board[start + l][
                j] != "H":  # If there is something on the board obstructing the ship
                return score[0:returnedScoreLength]  # Ship not possible
            elif board[start + l][j] == "H":
                if increase>1:
                    score[returnedScoreLength:length] = score[returnedScoreLength:length] + increase
                increase = max(shipNumber,4) + 3
        # print("add")
        returnedScoreLength = length
        score[0:returnedScoreLength] = score[0:returnedScoreLength] + increase
    return score[0:returnedScoreLength]


def calculateHorizentalScoreByPossibleBoatNumber(i, j, board, sortedShips):
    # else:  # If we are trying to place ship horizontally
    score = numpy.zeros((max(sortedShips)))
    returnedScoreLength = 0
    shipNumber = len(sortedShips)
    for length in sortedShips:
        if j + length > len(board[0]):  # If ship doesn't fit within board boundaries
            returnedScoreLength = 1
            return score[0:returnedScoreLength]  # Ship not possible
        difference = length - returnedScoreLength
        start = j + returnedScoreLength
        increase = 1
        for l in range(difference):  # For every section of the ship
            if board[i][start + l] != "" and board[i][
                        start + l] != "H":  # If there is something on the board obstructing the ship
                return score[0:returnedScoreLength]  # Ship not possible
            elif board[i][start + l] == "H":
                if increase>1:
                    score[returnedScoreLength:length] = score[returnedScoreLength:length] + increase
                increase = max(shipNumber,4) + 3
        returnedScoreLength = length
        score[0:returnedScoreLength] = score[0:returnedScoreLength] + increase
    return score[0:returnedScoreLength]


def maxHit(matrix):
    maxV = numpy.max(matrix)
    maxpointset = numpy.where(matrix == maxV)
    r = randint(0, len(maxpointset[0]) - 1)

    result = maxpointset[0][r], maxpointset[1][r]
    # result = result.astype(np.int32)
    move = {"Row": chr(int(result[0]) + 65),
            "Column": (int(result[1]) + 1)}
    return move

