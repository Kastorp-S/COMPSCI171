# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from collections import Counter


class Tile():

    def __init__(self, location: tuple = (None, None), hint: int = '.', mine: bool = False, isCovered: bool = True, isFlagged: bool = False):
        self.mine = mine
        self.isCovered = isCovered
        self.isFlagged = isFlagged
        self.hint = hint
        self.location = location
        self.x = location[0]
        self.y = location[1]
        #print([self.x, self.y])


    def getHint(self) -> int:
        return self.hint

    def setHint(self, num: int):
        self.hint = num
    
    def uncoverTile(self):
        self.isCovered = False


class Constrain:
    def __init__(self, suspectTile=list(), hint=0):
        self.suspectTile = suspectTile
        self.hint = hint

    def __eq__(self, other):
        def compare(x, y): return Counter(x) == Counter(y)
        if compare(self.suspectTile, other.suspectTile) and self.hint == other.hint:
            return True

        else:
            return False

    def compare(self, another_constrain):
        
        new_constrain = Constrain()
        isSubset = True
        this_constrain = self
        
        for variable in set(this_constrain.suspectTile):
            if variable not in set(another_constrain.suspectTile):
                isSubset = False
                break
            
        if isSubset:
            new_constrain.suspectTile = list(set(another_constrain.suspectTile) - set(this_constrain.suspectTile))
            new_constrain.hint = another_constrain.hint - this_constrain.hint
            
        return new_constrain

class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        ########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Edited by Y. Song and J. Ling at 2021.07.10

        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY

        self.tiles = list()               # A list contains all tiles
        self.exploredTiles = list()       # Already explored tiles
        self.unexploredTiles = list()     # Not yet explored

        self.safeTiles = list()           # Hint = 0
        self.flaggedTiles = list()        # Suspected Mines

        self.curTile = Tile()             

        self.firstStep = True

        self.whenToLeaveCounter = rowDimension * colDimension - totalMines
        self.numMines = 0

        for row in reversed(range(rowDimension)):
            tileRow = list()
            for col in range(colDimension):
                tileRow.append(Tile(location=(col, row)))
            self.tiles.append(tileRow)

        for row in self.tiles:
            for tile in row:
                self.unexploredTiles.append(tile)
        
        ########################################################################
	    #							YOUR CODE ENDS							   #
	    ########################################################################


    def getAction(self, number: int) -> "Action Object":

        ########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        # Edited by Y. Song and J. Ling at 2021.07.10

        if self.firstStep:
            self.firstStep = False
            
            self.curTile = self.tiles[self.rowDimension - 1 - self.startY][self.startX]
            self.whenToLeaveCounter -= 1
            self.unexploredTiles.remove(self.curTile)
            self.exploredTiles.append(self.curTile)
            return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

        self.curTile.setHint(number)

        if (number == 0):
			#Append uncovered tiles to list
            #self.safeTiles.append(self.curTile)

			# Uncover all tiles around safe tile
            tilesAroundCurrent = self.findNeighbours(self.curTile.x, self.curTile.y)

			# Ensure action in bound
            for tile in tilesAroundCurrent:
                if tile.x >= 0 and tile.x < self.rowDimension and tile.y >= 0 and tile.y < self.colDimension and tile not in self.safeTiles and tile not in self.exploredTiles and tile not in self.flaggedTiles:
                    self.safeTiles.append(tile)
                    '''print("append tile:")
                    print([tile.x + 1, tile.y + 1])'''
                    tile.uncoverTile()
                    self.tiles[self.rowDimension - 1 - tile.y][tile.x] = tile

        # Uncover all the safe tiles
        if self.safeTiles:
            self.curTile = self.safeTiles.pop()
            self.exploredTiles.append(self.curTile)
            self.unexploredTiles.remove(self.curTile)
            self.whenToLeaveCounter -= 1

            return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

        elif self.flaggedTiles:
            self.curTile = self.flaggedTiles.pop()
            self.exploredTiles.append(self.curTile)
            self.unexploredTiles.remove(self.curTile)
            self.curTile.isFlagged = True
            self.numMines += 1

            return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)

        # No more safe tiles
        else:
            for tile in self.exploredTiles:
                if tile.getHint() > 0:
                
                    flag_Tile = []
                    covered_Tile = []
                    tilesAroundCurrent = self.findNeighbours(tile.x, tile.y)
                    for tilex in tilesAroundCurrent:
                        if tilex.getHint() == '.':
                            '''print("Append covered_Tile")
                            print([tilex.x + 1, tilex.y + 1])'''
                            covered_Tile.append(tilex)
                        elif tilex.getHint() == -1:
                            '''print("Append flag_Tile")
                            print([tilex.x + 1, tilex.y + 1])'''
                            flag_Tile.append(tilex)
                            
                    '''if tile.getHint() == len(covered_Tile) + len(flag_Tile) and len(covered_Tile) != 0:
                        for y in covered_Tile:
                            self.flaggedTiles.append(y)
                            
                    elif tile.getHint() == len(flag_Tile) and len(covered_Tile) != 0:
                        for y in covered_Tile:
                            self.safeTiles.append(y)'''

                    if tile.getHint() == len(covered_Tile) + len(flag_Tile) and len(covered_Tile) != 0:

                        self.curTile = covered_Tile.pop()
                        self.exploredTiles.append(self.curTile)
                        self.unexploredTiles.remove(self.curTile)
                        self.curTile.flag = True
                        self.numMines += 1
                        '''print("Flag Tile 195")
                        print([self.curTile.x + 1, self.curTile.y + 1])'''

                        return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)

                    else:

                        if tile.getHint() == len(flag_Tile) and len(covered_Tile) != 0:
                            self.safeTiles.extend(covered_Tile)
                            self.curTile = self.safeTiles.pop()
                            self.exploredTiles.append(self.curTile)
                            self.unexploredTiles.remove(self.curTile)
                            self.whenToLeaveCounter -= 1
                            '''print("Uncover Tile 208")
                            print([self.curTile.x + 1, self.curTile.y + 1])'''

                            return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

        constrains = list()

        for tile in self.exploredTiles:
            frontier = False
            flag_count = 0
            neighbors = self.findNeighbours(tile.x, tile.y)
            suspectTile = list()

            for neighbor in neighbors:
                if neighbor.getHint() == '.':
                    frontier = True
                    suspectTile.append(neighbor)

                if neighbor.getHint() == -1:
                    flag_count += 1

            if frontier and tile.getHint() != -1:
                cs = Constrain(suspectTile, tile.getHint() - flag_count)
                constrains.append(cs)

        constrains = self.solveConstrain(constrains)
        extracted = self.extract(constrains)

        for cs in extracted:
            if cs.hint == 1:
                self.flaggedTiles.extend(cs.suspectTile)

            elif cs.hint == 0:
                self.safeTiles.extend(cs.suspectTile)

        if self.safeTiles:
            self.curTile = self.safeTiles.pop()
            self.exploredTiles.append(self.curTile)
            self.unexploredTiles.remove(self.curTile)
            self.whenToLeaveCounter -= 1

            return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

        if self.numMines == self.totalMines:
            return Action(AI.Action.LEAVE)


        return Action(AI.Action.LEAVE)

        ########################################################################
	    #							YOUR CODE ENDS							   #
	    ########################################################################

    # returns neighbours' locationations
    def findNeighbours(self, x, y) -> list:

        neighbours = []
        for neighbour_x in range (x - 1, x + 2):
            for neighbour_y in range (y - 1, y + 2):
                if 0 <= neighbour_x < self.rowDimension and 0 <= neighbour_y < self.colDimension and not(x == neighbour_x and y == neighbour_y):
                    neighbours.append(self.tiles[self.rowDimension - 1 - neighbour_y][neighbour_x])

        return neighbours
    
    def solveConstrain(self, constrains):

        for cs1 in constrains:
            for cs2 in constrains:

                cs = cs1.compare(cs2)

                if cs not in constrains and cs.suspectTile:
                    constrains.append(cs)

                if len(cs.suspectTile) == cs.hint:
                    for i in range(len(cs.suspectTile)):
                        cs_new = Constrain([cs.suspectTile[i]], 1)
                        if cs_new not in constrains and cs_new.suspectTile:
                            constrains.append(cs_new)

                if len(cs.suspectTile) > 0 and cs.hint == 0:
                    for i in range(len(cs.suspectTile)):
                        cs_new = Constrain([cs.suspectTile[i]], 0)
                        if cs_new not in constrains and cs_new.suspectTile:
                            constrains.append(cs_new)

        return constrains

    def extract(self, constrains):
        extracted = list()
        for cs in constrains:
            if len(cs.suspectTile) == 1:
                extracted.append(cs)

        return extracted