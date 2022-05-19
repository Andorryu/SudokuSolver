import math

class Driver():
    def __init__(self):
        self.run = True
        self.board = [[int(i) for i in file.read(9)] for i in range(9)] # of the form:   board[row][col]
        self.invalid = False
        self.squareSize = int(math.sqrt(len(self.board)))

    def Run(self):
        self.CheckViableBoard()
        self.GeneralAnalysis()
        self.FillInTiles()
        self.RemainderAnalysis()
        self.PairAnalysis()
        if self.invalid:
            print("This board is INVALID")
        else:
            print("This board is VALID")

    def CheckViableBoard(self):
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
        pass

    def FillInTiles(self):
        pass

    def RemainderAnalysis(self):
        pass

    def PairAnalysis(self):
        pass


# open txt file
file = open("input.txt")

# seeking start of file (this is technically unnecessary rn)
file.seek(0, 0)

driver = Driver()
driver.Run()

# close txt file
file.close()