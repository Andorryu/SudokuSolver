import math
import copy
import time

class Driver():
    def __init__(self):
        self.run = True
        self.previousBoard = []
        self.board = [[int(j) for j in file.read(9)] for i in range(9)] # of the form:   board[row][col]
        self.impossibleNotes = [[[] for j in range(9)] for i in range(9)]
        self.possibleNotes = [[[] for j in range(9)] for i in range(9)]
        self.invalid = False
        self.squareSize = int(math.sqrt(len(self.board)))

    def Run(self):
        # check the board
        self.CheckViableBoard()
        # print its validity and stop program if invalid
        print("")
        if self.invalid:
            print("This board is INVALID")
            return
        else:
            print("This board is VALID")
        # perform initial general analysis
        # run the analysis techniques until the board is finished
        while self.run:
            self.DisplayBoard()
            self.GeneralAnalysis()
            self.RemainderAnalysis()
            self.PairAnalysis()
            self.FillInTiles()
            self.CheckSolved()

    def CheckViableBoard(self):
        #print("Checking Viability of the board by checking if there are repeats in the rows, columns, or 3x3 squares")
        #print("")
        # iterate thru every tile
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != 0: # for every tile that is not blank
                    
                    #print("Testing", self.board[row][col], "at (", row, ",", col, ")...")
                    #print("...for repeats in its row at...")
                    # test the row that the tile is in, for every tile
                    for i in range(len(self.board) - (col + 1)): # i ranges from 0 to the number of tiles left in the row
                        testCol = i + col + 1 # testCol ranges from the index of the tile after the testTile to 8
                        #print("...(", row, ",", testCol, ")")
                        if self.board[row][testCol] == self.board[row][col]: # if there is a repeat in the row
                            self.invalid = True
                            #print("THERE ARE TWO NUMBERS IN THE SAME ROW!!!")
                            #print("THE NUMBERS AT (", row, ",", col, ") AND (", row, ",", testCol, ") ARE BOTH ", self.board[row][col], "!!!")
                            
                    #print("...for repeats in its column at...")
                    # test the column that the tile is in for every tile
                    for i in range(len(self.board) - (row + 1)): # i ranges from 0 to the number of tiles left in the column
                        testRow = i + row + 1 # testRow ranges from index of the tile after the testTile to 8
                        #print("...(", testRow, ",", col, ")")
                        if self.board[testRow][col] == self.board[row][col]:
                            self.invalid = True
                            #print("THERE ARE TWO NUMBERS IN THE SAME COLUMN!!!")
                            #print("THE NUMBERS AT (", row, ",", col, ") AND (", testRow, ",", col, ") ARE BOTH ", self.board[row][col], "!!!")
                            
                    #print("...for repeats in its 3x3 square at...")
                    # test the square that the tile is in, for every tile

                    # squareRow and squareCol tell us which 3x3 square the tile is in,
                    # their range can be either 0, 1, or 2, each 3x3 square gets its own coord
                    # e.g., square coords of row: 0, col: 2 would mean the tile is in one of the first 3 rows and one of the last 3 columns
                    squareRow = math.floor(row/self.squareSize)
                    squareCol = math.floor(col/self.squareSize)
                    for i in range(self.squareSize): #  i ranges from 0 to 3
                        for j in range(self.squareSize): # j ranges from 0 to 3
                            testRow = i + (squareRow * self.squareSize) # testRow and testCol cover every coord in the square that the testTile is in
                            testCol = j + (squareCol * self.squareSize)
                             # dont test in the same row or column, this saves time, since row and column repeats have already been tested for
                            if testRow != row and testCol != col:
                                #print("...(", testRow, ",", testCol, ")")
                                if self.board[testRow][testCol] == self.board[row][col]:
                                    self.invalid = True
                                    #print("THERE ARE TWO NUMBERS IN THE SAME 3x3 SQUARE!!!")
                                    #print("THE NUMBERS AT (", row, ",", col, ") AND (", testRow, ",", testCol, ") ARE BOTH ", self.board[row][col], "!!!")


    def GeneralAnalysis(self):
        #print("")
        #print("")
        #print("Noting which values are impossible for a given tile")
        # iterate thru every tile
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0: # only work on the empty tiles

                    #print("")
                    #print("Testing the row of (", row, ",", col, ")")
                    # populate impossibleNotes with impossible values based on the filled-in tiles in the row
                    for testCol in range(len(self.board)):
                        if self.board[row][testCol] != 0:
                            if not self.ItemExistsInList(self.board[row][testCol], self.impossibleNotes[row][col]):
                                self.impossibleNotes[row][col].append(self.board[row][testCol])
                                #print("Appended ", self.board[row][testCol], " to board notes")
                            #else:
                                #print("Skipping ", self.board[row][testCol], "...")
                        # trace debug
                        #if testCol == 8:
                            #print("Board Notes:")
                            #print(self.impossibleNotes[row][col])

                    #print("Testing with columns now...")
                    # populate impossibleNotes with impossible values based on the filled-in tiles in the column
                    for testRow in range(len(self.board)):
                        if self.board[testRow][col] != 0:
                            if not self.ItemExistsInList(self.board[testRow][col], self.impossibleNotes[row][col]):
                                self.impossibleNotes[row][col].append(self.board[testRow][col])
                                #print("Appended ", self.board[testRow][col], " to board notes")
                            #else:
                                #print("Skipping ", self.board[testRow][col], "...")
                        # trace debug
                        #if testRow == 8:
                            #print("Board Notes:")
                            #print(self.impossibleNotes[row][col])
                            
                    #print("Testing with 3x3 squares now...")
                    # populate impossibleNotes with impossible values based on the filled-in tiles in the 3x3 square
                    # get coords of each 3x3 square
                    squareRow = math.floor(row/self.squareSize)
                    squareCol = math.floor(col/self.squareSize)
                    for i in range(self.squareSize):
                        for j in range(self.squareSize):
                            testRow = i + (squareRow * self.squareSize) # testRow and testCol cover every coord in the square that the testTile is in
                            testCol = j + (squareCol * self.squareSize)
                            if testRow != row and testCol != col: # dont test in the same row or column
                                if self.board[testRow][testCol] != 0: # dont test it if it is blank
                                    if not self.ItemExistsInList(self.board[testRow][testCol], self.impossibleNotes[row][col]):
                                        self.impossibleNotes[row][col].append(self.board[testRow][testCol])
                                        #print("Appended ", self.board[testRow][testCol], " to board notes")
                                    #else:
                                        #print("Skipping ", self.board[testRow][testCol], "...")
                            # trace debug
                            #if i == 2 and j == 2:
                                #print("Board Notes:")
                                #print(self.impossibleNotes[row][col])
                    
                    # subtract the list of impossible values from the list of every value from 1 to 9 to get all the possible values for that tile
                    self.possibleNotes[row][col] = self.ListSubtraction([i+1 for i in range(9)], self.impossibleNotes[row][col])

        # maybe the ratio of deduced possible values to deduced impossible values at this step determines the difficulty level of the puzzle?
        # maybe the difficulty is determined by how many changes in the board are made?
        #print("")
        #print("The following lists the impossible values for each blank tile, read from left tile to right tile, and from top row to bottom row.")
        #print(self.impossibleNotes)
        #print("")
        #print("The following lists the possible values.")
        #print(self.possibleNotes)


    def FillInTiles(self):
        #print("")
        #print("Now filling in tiles...")


        # lists numbers that repeat for each row, column, or 3x3 square
        rowRepeatList = [[] for i in range(len(self.board))]
        colRepeatList = [[] for i in range(len(self.board))]
        squareRepeatList = [[[] for i in range(self.squareSize)] for j in range(self.squareSize)]
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0: # if the testTile is blank
                    
                    # fill in the blank if there is only one possible number for that blank
                    # i.e., that's the only number for that place
                    if len(self.possibleNotes[row][col]) == 1:
                        print("")
                        print(self.possibleNotes[row][col][0], " is the only possible number for the tile at (", row, ",", col, ")")
                        self.board[row][col] = self.possibleNotes[row][col][0]
                        print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")

                    # fill in the blank if there is a number that is the only one in its row, column or 3x3 square
                    # i.e., that's the only place for that number (within its row, column, or 3x3 square)
                    # search the row
                    for note in self.possibleNotes[row][col]: # for every possible number for that tile
                        for i in range(len(self.board) - (col + 1)): # i ranges from 0 to the number of tiles left in the row
                            testCol = i + col + 1 # testCol ranges from the index of the tile after the testTile to 8
                            if len(self.possibleNotes[row][testCol]) > 0: # if the test notes are not empty (i.e., its a blank tile)
                                # if the test note has not already been determined to repeat in the row, test it
                                if not self.ItemExistsInList(note, rowRepeatList[row]):
                                    # if the note exists anywhere else in the row, add it to the repeat list
                                    if self.ItemExistsInList(note, self.possibleNotes[row][testCol]):
                                        rowRepeatList[row].append(note)
                        # if the note doesn't exist in the repeat list at this point, it must fill the blank
                        if not self.ItemExistsInList(note, rowRepeatList[row]):
                            print("")
                            print(note, " only exists in the possible list at (", row, ",", col, ") in the row ", row)
                            self.board[row][col] = note
                            print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")

                    # search the column
                    for note in self.possibleNotes[row][col]:
                        for i in range(len(self.board) - (row + 1)): # i ranges from 0 to the number of tiles left in the column
                            testRow = i + row + 1 # testRow ranges from index of the tile after the testTile to 8
                            if len(self.possibleNotes[testRow][col]) > 0: # if the test notes are not empty (i.e., its a blank tile)
                                # if the test note has not already been determined to repeat in the column, test it
                                if not self.ItemExistsInList(note, colRepeatList[col]):
                                    # if the note exists anywhere else in the column, add it to the repeat list
                                    if self.ItemExistsInList(note, self.possibleNotes[testRow][col]):
                                        colRepeatList[col].append(note)
                        # if the note doesn't exist in the repeat list at this point, it must fill the blank
                        if not self.ItemExistsInList(note, colRepeatList[col]):
                            print("")
                            print(note, " only exists in the possible list at (", row, ",", col, ") in the col ", col)
                            self.board[row][col] = note
                            print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")

                    # search the 3x3 square
                    squareRow = math.floor(row/self.squareSize)
                    squareCol = math.floor(col/self.squareSize)
                    for note in self.possibleNotes[row][col]:
                        for i in range(self.squareSize):
                            for j in range(self.squareSize):
                                testRow = i + (squareRow * self.squareSize)
                                testCol = j + (squareCol * self.squareSize)
                                if len(self.possibleNotes[testRow][testCol]) > 0:
                                    if row != testRow or col != testCol:
                                        if not self.ItemExistsInList(note, squareRepeatList[squareRow][squareCol]):
                                            if self.ItemExistsInList(note, self.possibleNotes[testRow][testCol]):
                                                squareRepeatList[squareRow][squareCol].append(note)
                        if not self.ItemExistsInList(note, squareRepeatList[squareRow][squareCol]):
                            print("")
                            print(note, " only exists in the possible list at (", row, ",", col, ") at the square coordinates: (", squareRow, ",", squareCol, ")")
                            self.board[row][col] = note
                            print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")
        # clear the notes
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                self.possibleNotes[row][col] = []
                self.impossibleNotes[row][col] = []


    def RemainderAnalysis(self):
        pass

    def PairAnalysis(self):
        pass

    def CheckSolved(self):
        self.run = self.previousBoard != self.board
        self.previousBoard = copy.deepcopy(self.board)
        if not self.run:
            print("Time taken:", time.time() - startTime)
        #self.run = False
        #for row in range(len(self.board)):
        #    for col in range(len(self.board)):
        #        if self.board[row][col] == 0:
        #            self.run = True
        

    def DisplayBoard(self):
        print("")
        print("Sudoku board:")
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                print(self.board[row][col], end=" ")
            print("")

    def ItemExistsInList(self, item, list):
        for i in list:
            if i == item:
                return True
        return False

    def ListSubtraction(self, subtractor, subtractee): # assume that every value in subtractee is also in subtractor
        subtraction = []
        for i in subtractor:
            if not self.ItemExistsInList(i, subtractee):
                subtraction.append(i)
        return subtraction

    def FindOverlap(self, list1, list2):
        resultList = []
        for item1 in list1:
            for item2 in list2:
                if item1 == item2:
                    resultList.append(item1)
        return resultList



# open txt file
file = open("input.txt")

# seeking start of file (this is technically unnecessary rn)
file.seek(0, 0)

startTime = time.time()
driver = Driver()
driver.Run()

# close txt file
file.close()