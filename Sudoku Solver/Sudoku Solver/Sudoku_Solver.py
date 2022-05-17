

class Driver():
    def __init__(self):
        self.run = True
        self.board = [[int(i) for i in file.read(9)] for i in range(9)] # of the form:   board[row][col]
        self.invalid = False

    def Run(self):
        self.CheckViableBoard()
        self.GeneralAnalysis()
        self.FillInTiles()
        self.RemainderAnalysis()
        self.PairAnalysis()
        if self.invalid:
            print("This board is invalid")

    def CheckViableBoard(self):
        # iterate thru every tile
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != 0:
                    # test the row that the tile is in, for every tile
                    for i in range(len(self.board) - (col + 1)): # i ranges from 0 to the number of tiles left in the row
                        testCol = i + col + 1 # testCol ranges from the index of the tile after the testTile to 8
                        if self.board[row][testCol] == self.board[row][col]:
                            self.invalid = True

                    # test the column that the tile is in for every tile
                    for i in range(len(self.board) - (row + 1)): # i ranges from 0 to the number of tiles left in the row
                        testRow = i + row + 1
                        print(self.board[testRow][col], end="")
                        if self.board[testRow][col] == self.board[row][col]:
                            self.invalid = True
                    print("")

                    # test the square that the tile is in, for every tile

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

# read board into board variable
file.seek(0, 0)

driver = Driver()
driver.Run()

# close txt file
file.close()