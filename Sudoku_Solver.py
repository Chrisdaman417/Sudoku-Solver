import copy

# Board of 81 cells in a 9x9 Grid
class board:
    def __init__(self):
        self.size = 9
        self.board = [[cell() for i in range(self.size)] for i in range(self.size)]
        self.boardStr = ""
        self.winStr = ""
        self.current = 0
        self.valid = True
        self.change = True
        self.win = False

    # Sets board to blank
    def clearBoard(self):
        self.change = True
        self.win = False
        self.winStr = ""
        for j in range(self.size):
                for i in range(self.size):
                    self.board[j][i].resetCell()

    # Copies board from specific file (txt)
    def copyFile(self, string):
        self.file = open(string,"r")
        self.boardStr = self.file.read()
        self.file.close()
        self.validSet()
        self.clearBoard()
        if self.valid == False:
            return
        else:
            self.index = 0
            for j in range(self.size):
                for i in range(self.size):
                    if int(self.boardStr[self.index]) != 0:
                        self.board[j][i].setCell(int(self.boardStr[self.index]))
                    self.index += 1
        self.validBoard()

    # Copies board from passed string
    def copyString(self,string):
        self.clearBoard()
        self.boardStr = string
        self.validSet()
        if self.valid == False:
            return
        else:
            self.index = 0
            for j in range(self.size):
                for i in range(self.size):
                    if int(self.boardStr[self.index]) != 0:
                        self.board[j][i].setCell(int(self.boardStr[self.index]))
                    self.index += 1
        self.validBoard()

    # Reads current board state
    def output(self):
        if self.valid == True:
            for j in range(self.size):
                for i in range(self.size):
                    print(self.board[j][i].result,end = " ")
                print("")
        else:
            print("No valid board to print")
        print("")

    # Determines if board is valid
    def validBoard(self):
        self.valid = True
        # Row valid Check
        for i in range(self.size):
            for j in range(self.size):
                self.current = self.board[i][j].result
                if self.current == 0:
                    continue
                for k in range(self.size):
                    if k == j:
                        continue
                    if self.current == self.board[i][k].result:
                        self.valid = False
                        return

        # Col valid Check
        for i in range(self.size):
            for j in range(self.size):
                self.current = self.board[j][i].result
                if self.current == 0:
                    continue
                for k in range(self.size):
                    if k == j:
                        continue
                    if self.current == self.board[k][i].result:
                        self.valid = False
                        return

        # Box valid Check
        for x in range(3):
                for y in range(3):
                    for i in range(3):
                        for j in range(3):
                            if self.board[i+(y*3)][j+(x*3)].result == 0:
                                continue
                            self.current = self.board[i+(y*3)][j+(x*3)].result
                            if self.board[i+(y*3)][j+(x*3)].result == 0:
                                for k in range(3):
                                    for l in range(3):
                                        if k == i and l == j:
                                            continue
                                        if self.current == self.board[k+(y*3)][l+(x*3)].result:
                                            self.valid = False

    # Determines if input is valid
    def validSet(self):
        self.valid = True
        if len(self.boardStr) < (self.size*self.size):
            self.valid = False
            return
        for i in range(81):
            if int(self.boardStr[i]) < 0 or int(self.boardStr[i]) > 9:
                self.valid = False

    # Trims options from cells in specific row
    def checkRow(self,row):
        for i in range(self.size):
            if self.board[row][i].result == 0:
                for j in range(self.size):
                    if self.board[row][j].result != 0:
                        if self.board[row][j].result in self.board[row][i].options:
                            self.board[row][i].options.remove(self.board[row][j].result)
                            self.board[row][i].setResult()
                            self.change = True

    # Trims options from cells in specific column          
    def checkCol(self,col):
        for i in range(self.size):
            if self.board[i][col].result == 0:
                for j in range(self.size):
                    if self.board[j][col].result != 0:
                         if self.board[j][col].result in self.board[i][col].options:
                            self.board[i][col].options.remove(self.board[j][col].result)
                            self.board[i][col].setResult()
                            self.change = True

    # Trims options from cells in specific box
    def checkBox(self,x,y):
        for i in range(3):
            for j in range(3):
                if self.board[i+(y*3)][j+(x*3)].result == 0:
                    for k in range(3):
                        for l in range(3):
                            if self.board[k+(y*3)][l+(x*3)].result != 0:
                                if self.board[k+(y*3)][l+(x*3)].result in self.board[i+(y*3)][j+(x*3)].options:
                                    self.board[i+(y*3)][j+(x*3)].options.remove(self.board[k+(y*3)][l+(x*3)].result)
                                    self.board[i+(y*3)][j+(x*3)].setResult()
                                    self.change = True                      

    # Sets only options in specific row
    def compRow(self,row):
        for i in range(self.size):
            if self.board[row][i].result == 0:
                for checki in range(len(self.board[row][i].options)):
                    matchFound = False
                    for j in range(self.size):
                        if j == i:
                            pass
                        if self.board[row][j].result == 0:
                            if self.board[row][i].options[checki] in self.board[row][j].options:
                                matchFound = True
                                break
                    if matchFound == False:
                        self.board[row][i].setCell(self.board[row][i].options[checki])
                        self.change = True
                        return

    # Sets only options in specific column
    def compCol(self,col):
        for i in range(self.size):
            if self.board[i][col].result == 0:
                for checki in range(len(self.board[i][col].options)):
                    matchFound = False
                    for j in range(self.size):
                        if j == i:
                            pass
                        if self.board[j][col].result == 0:
                            if self.board[i][col].options[checki] in self.board[j][col].options:
                                matchFound = True
                                break
                    if matchFound == False:
                        self.board[i][col].setCell(self.board[i][col].options[checki])
                        self.change = True
                        return

    # Sets only options in specific box
    def compBox(self,x,y):
        for i in range(3):
            for j in range(3):
                if self.board[i+(y*3)][j+(x*3)].result == 0:
                    for checki in range(len(self.board[i+(y*3)][j+(x*3)].options)):
                        matchFound = False
                        for k in range(3):
                            for l in range(3):
                                if k == i and l == j:
                                    continue
                                elif self.board[k+(y*3)][l+(x*3)].result == 0:
                                    if self.board[i+(y*3)][j+(x*3)].options[checki] in self.board[k+(y*3)][l+(x*3)].options:
                                        matchFound = True
                                        break
                            if matchFound == True:
                                break
                        if matchFound == False:
                            self.board[i+(y*3)][j+(x*3)].setCell(self.board[i+(y*3)][j+(x*3)].options[checki])
                            self.change = True
                            return

    # Check for win State
    def checkWin(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].result == 0:
                    return
        self.win = True

    # Fine next blank cell
    def findCheat(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col].result == 0:
                    return row, col
        return None, None

    # valid Check
    def cheatValid(self, guess, row, col):
        # Sets row, col, and box for validity check
        row_numbers = [self.board[row][i].result for i in range(9)]
        col_numbers = [self.board[i][col].result for i in range(9)]
        
        # Divides then rounds to nearest whole number
        row_start = (row//3)*3 
        col_start = (col//3)*3

        # Checks to see if guess is in cell[row][col]
        if guess not in self.board[row][col].options:
            return False

        # Checks to see if guess is already in row
        if guess in row_numbers:
            return False

        # Checks to see if guess is already in col
        if guess in col_numbers:
            return False

        # Checks to see if guess is already in box
        for r in range(row_start, row_start+3):
            for c in range(col_start, col_start+3):
                if self.board[r][c].result == guess:
                    return False

        # Passed all checks. Valid Guess!
        return True

    # Backtracing Algorithm
    def cheatCode(self):
        # Find Cell to guess
        row, col = self.findCheat()
        
        # End of board
        if row == None:
            return True

        # Guess from 1 - 9
        for random in range(1, 10):

            # Is cheat valid?
            # Yes --> Set board and rerun
            if self.cheatValid(random, row, col):

                # Set Board
                self.board[row][col].guessCell(random)

                # Rerun
                if self.cheatCode():
                    return True

            # No --> next Guess
            self.board[row][col].guessCell(0)

        # Unsolvable
        return False

    # Check Entire Board
    def checkBoard(self):
        while not self.win:
            self.change = False
            for i in range(self.size):
                self.checkRow(i)
                self.checkCol(i)
            for i in range(3):
                for j in range(3):
                    self.checkBox(j,i)
            self.checkWin()
            if self.change == False:
                for i in range(self.size):
                    self.compRow(i)
                    self.compCol(i)
                for i in range(3):
                    for j in range(3):
                        self.compBox(j,i)
                self.checkWin()
                if self.change == False:
                    if self.cheatCode():
                        self.win = True
        for i in range(9):
            for j in range(9):
                self.winStr += str(self.board[j][i].result)

# Contains result or options for result
class cell:
    def __init__(self):
        self.options = [1,2,3,4,5,6,7,8,9]
        self.result = 0

    def guessCell(self, guess):
        self.result = guess

    # Sets the cell to a specific input value
    def setCell(self, input):
        self.result = input
        self.options.clear()

    # Sets the result to last option if able
    def setResult(self):
        if len(self.options) > 1:
            return
        elif len(self.options) == 1:
            self.setCell(int(self.options[0]))

    # Outputs the options for a cell
    def readOptions(self):
        if self.result == 0:
            for i in range(len(self.options)):
                if self.options[i] == None:
                    return
                print(self.options[i], end =" ")
        else:
            print(self.result, end = " ")

    # Resets the cell to starting state
    def resetCell(self):
        self.options = [1,2,3,4,5,6,7,8,9]
        self.result = 0

# Main Function
class Solver:
    def __init__(self):
        self.gameBoard = board()

    def run(self):
        self.gameBoard.copyFile("")
        if self.gameBoard.valid == True:
            self.gameBoard.checkBoard()
        

if __name__ == "__main__":
    Main = Solver()
    Main.run()