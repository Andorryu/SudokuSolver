import math

class Driver():
    def __init__(self):
        self.run = True
        self.board = [[int(i) for i in file.read(9)] for i in range(9)] # of the form:   board[row][col]
        self.impossibleNotes = [[[] for i in range(9)] for i in range(9)]
        self.possibleNotes = [[[] for i in range(9)] for i in range(9)]
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
        self.GeneralAnalysis()
        # run the analysis techniques until the board is finished
        while self.run:
            self.FillInTiles()
            self.GeneralAnalysis()
            self.RemainderAnalysis()
            self.PairAnalysis()
            print("")
            print("Sudoku board:")
            self.DisplayBoard()
            self.CheckSolved()
            #self.run = False

    def CheckViableBoard(self):
        print("Checking Viability of the board by checking if there are repeats in the rows, columns, or 3x3 squares")
        print("")
        # iterate thru every tile
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != 0:
                    
                    print("Testing", self.board[row][col], "at (", row, ",", col, ")...")
                    print("...for repeats in its row at...")
                    # test the row that the tile is in, for every tile
                    for i in range(len(self.board) - (col + 1)): # i ranges from 0 to the number of tiles left in the row
                        testCol = i + col + 1 # testCol ranges from the index of the tile after the testTile to 8
                        print("...(", row, ",", testCol, ")")
                        if self.board[row][testCol] == self.board[row][col]:
                            self.invalid = True
                            print("THERE ARE TWO NUMBERS IN THE SAME COLUMN!!!")
                            print("THE NUMBERS AT (", row, ",", col, ") AND (", testRow, ",", testCol, ") ARE BOTH ", self.board[row][col], "!!!")
                            
                    print("...for repeats in its column at...")
                    # test the column that the tile is in for every tile
                    for i in range(len(self.board) - (row + 1)): # i ranges from 0 to the number of tiles left in the column
                        testRow = i + row + 1 # testRow ranges from index of the tile after the testTile to 8
                        print("...(", testRow, ",", col, ")")
                        if self.board[testRow][col] == self.board[row][col]:
                            self.invalid = True
                            print("THERE ARE TWO NUMBERS IN THE SAME COLUMN!!!")
                            print("THE NUMBERS AT (", row, ",", col, ") AND (", testRow, ",", testCol, ") ARE BOTH ", self.board[row][col], "!!!")
                            
                    print("...for repeats in its 3x3 square at...")
                    # test the square that the tile is in, for every tile
                    # get coords of each 3x3 square
                    squareRow = math.floor(row/self.squareSize)
                    squareCol = math.floor(col/self.squareSize)
                    for i in range(self.squareSize):
                        for j in range(self.squareSize):
                            testRow = i + (squareRow * self.squareSize) # testRow and testCol cover every coord in the square that the testTile is in
                            testCol = j + (squareCol * self.squareSize)
                            if testRow != row and testCol != col: # dont test in the same row or column
                                print("...(", testRow, ",", testCol, ")")
                                if self.board[testRow][testCol] == self.board[row][col]:
                                    self.invalid = True
                                    print("THERE ARE TWO NUMBERS IN THE SAME 3x3 SQUARE!!!")
                                    print("THE NUMBERS AT (", row, ",", col, ") AND (", testRow, ",", testCol, ") ARE BOTH ", self.board[row][col], "!!!")



    def GeneralAnalysis(self):
        print("")
        print("")
        print("Noting which values are impossible for a given tile")
        # iterate thru every tile
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0: # only work on the empty tiles

                    print("")
                    print("Testing the row of (", row, ",", col, ")")
                    # populate impossibleNotes with impossible values based on the filled-in tiles in the row
                    for testCol in range(len(self.board)):
                        if self.board[row][testCol] != 0:
                            if not self.ItemExistsInList(self.board[row][testCol], self.impossibleNotes[row][col]):
                                self.impossibleNotes[row][col].append(self.board[row][testCol])
                                print("Appended ", self.board[row][testCol], " to board notes")
                            else:
                                print("Skipping ", self.board[row][testCol], "...")
                        # trace debug
                        if testCol == 8:
                            print("Board Notes:")
                            print(self.impossibleNotes[row][col])

                    print("Testing with columns now...")
                    # populate impossibleNotes with impossible values based on the filled-in tiles in the column
                    for testRow in range(len(self.board)):
                        if self.board[testRow][col] != 0:
                            if not self.ItemExistsInList(self.board[testRow][col], self.impossibleNotes[row][col]):
                                self.impossibleNotes[row][col].append(self.board[testRow][col])
                                print("Appended ", self.board[testRow][col], " to board notes")
                            else:
                                print("Skipping ", self.board[testRow][col], "...")
                        # trace debug
                        if testRow == 8:
                            print("Board Notes:")
                            print(self.impossibleNotes[row][col])
                            
                    print("Testing with 3x3 squares now...")
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
                                        print("Appended ", self.board[testRow][testCol], " to board notes")
                                    else:
                                        print("Skipping ", self.board[testRow][testCol], "...")
                            # trace debug
                            if i == 2 and j == 2:
                                print("Board Notes:")
                                print(self.impossibleNotes[row][col])
                    
                    # subtract the list of impossible values from the list of every value from 1 to 9 to get all the possible values for that tile
                    self.possibleNotes[row][col] = self.ListSubtraction([i+1 for i in range(9)], self.impossibleNotes[row][col])




        # maybe the ratio of deduced possible values to deduced impossible values at this step determines the difficulty level of the puzzle?
        print("")
        print("The following lists the impossible values for each blank tile, read from left tile to right tile, and from top row to bottom row.")
        print(self.impossibleNotes)
        print("")
        print("The following lists the possible values.")
        print(self.possibleNotes)

    def FillInTiles(self):
        print("")
        print("Now filling in tiles...")
        rowRepeatList = [[] for i in range(len(self.board))]
        colRepeatList = [[] for i in range(len(self.board))]
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0:

                    # fill in the blank if there is a number that is the only one in its row, column or 3x3 square
                    # search the row
                    for note in self.possibleNotes[row][col]:
                        for i in range(len(self.board) - (col + 1)): # i ranges from 0 to the number of tiles left in the row
                            testCol = i + col + 1 # testCol ranges from the index of the tile after the testTile to 8
                            if len(self.possibleNotes[row][testCol]) > 0: # if the test notes are not empty
                                if not self.ItemExistsInList(note, rowRepeatList[row]):
                                    if self.ItemExistsInList(note, self.possibleNotes[row][testCol]):
                                        rowRepeatList[row].append(note)
                        if not self.ItemExistsInList(note, rowRepeatList[row]):
                            print("")
                            print(note, " only exists in the possible list at (", row, ",", col, ") in the row ", row)
                            self.board[row][col] = note
                            print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")
                    # search the column
                    for note in self.possibleNotes[row][col]:
                        for i in range(len(self.board) - (row + 1)): # i ranges from 0 to the number of tiles left in the column
                            testRow = i + row + 1 # testRow ranges from index of the tile after the testTile to 8
                            if len(self.possibleNotes[testRow][col]) > 0: # if the test notes are not empty
                                if not self.ItemExistsInList(note, colRepeatList[col]):
                                    if self.ItemExistsInList(note, self.possibleNotes[testRow][col]):
                                        colRepeatList[col].append(note)
                        if not self.ItemExistsInList(note, colRepeatList[col]):
                            print("")
                            print(note, " only exists in the possible list at (", row, ",", col, ") in the col ", col)
                            self.board[row][col] = note
                            print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")
                    # search the 3x3 square


                    # fill in the blank if there is only one possible number for that blank
                    if len(self.possibleNotes[row][col]) == 1:
                        print("")
                        print(self.possibleNotes[row][col][0], " is the only possible number for the tile at (", row, ",", col, ")")
                        self.board[row][col] = self.possibleNotes[row][col][0]
                        print("Inserted ", self.board[row][col], " at (", row, ",", col, ")")

        # update the notes of filled-in tiles
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != 0:
                    self.impossibleNotes[row][col] = []
                    self.possibleNotes[row][col] = []


    def RemainderAnalysis(self):
        pass

    def PairAnalysis(self):
        pass

    def CheckSolved(self):
        self.run = False
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0:
                    self.run = True # run until the board is solved


    def DisplayBoard(self):
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

driver = Driver()
driver.Run()

# close txt file
file.close()