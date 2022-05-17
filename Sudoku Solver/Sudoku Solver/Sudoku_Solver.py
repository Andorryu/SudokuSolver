

class Driver():
    def __init__(self):
        self.run = True
        self.board = [[i for i in file.read(9)] for i in range(9)] # of the form:   board[row][col]

    def Run(self):
        self.CheckViableBoard()
        self.GeneralAnalysis()
        while self.run:
            self.FillInTiles()
            self.RemainderAnalysis()
            self.PairAnalysis()

    def CheckViableBoard(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                print(self.board[row][col])

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



