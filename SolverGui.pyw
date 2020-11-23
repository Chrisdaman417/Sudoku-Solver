import tkinter as tk
import Sudoku_Solver as Solve
import tkinter.filedialog as fd
import os

class inputCell():
    def __init__(self):
        self.cell = tk.Entry(width = 1)
        self.cell.config(font=("Calibri 24"),justify="center")

class SolverGUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg = "black")
        self.game = Solve.board()
        self.buttonFrame = tk.Frame(self.window)
        self.buttonFrame.grid(row = 0, column = 9, rowspan = 9, sticky = tk.N+tk.S)
        self.logBlock = tk.Frame(self.window)        
        self.logBlock.grid(row = 9, column = 0, columnspan = 10, sticky = tk.E+tk.W)
        self.log = tk.Label(self.logBlock, font=("Calibri 10"), text = "Welcome to Sudoku")
        self.log.pack(side = tk.LEFT)
        self.CurBoard = [[inputCell() for i in range(self.game.size)] for i in range(self.game.size)]

        # Button Block
        self.Button_loadFile = tk.Button(self.buttonFrame, text = "Load File", font=("Calibri 14"),justify="center", command = self.loadFile)
        self.Button_loadFile.grid(column = 0, row = 0, padx = 5, pady = (5,0), sticky = tk.E+tk.W)
        self.Button_clearBoard = tk.Button(self.buttonFrame, text = "Clear Board", font=("Calibri 14"),justify="center", command = self.clearBoard)
        self.Button_clearBoard.grid(column = 0, row = 1, padx = 5, sticky = tk.E+tk.W)
        self.Button_solveBoard = tk.Button(self.buttonFrame, text = "Solve Board", font=("Calibri 14"),justify="center", command = self.sendSolveStr)
        self.Button_solveBoard.grid(column = 0, row = 2, padx = 5, sticky = tk.E+tk.W)
        self.Button_saveBoard = tk.Button(self.buttonFrame, text = "Save Board", font=("Calibri 14"),justify="center", command = self.sendFile)
        self.Button_saveBoard.grid(column = 0, row = 3, padx = 5, sticky = tk.E+tk.W)

        # Sets Input Board
        for i in range(9):
            for j in range(9):
                self.CurBoard[i][j].cell
                self.CurBoard[i][j].cell.grid(column = j,row = i, ipadx = 9)
                if j == 3 or j == 6:
                    self.CurBoard[i][j].cell.grid_configure(padx = (5,0))
                if i == 3 or i == 6:
                    self.CurBoard[i][j].cell.grid_configure(pady = (5,0))
    
    # Clears Gui Board
    def clearBoard(self):
        for i in range(9):
            for j in range(9):
                self.CurBoard[i][j].cell.config(state="normal")
                self.CurBoard[i][j].cell.delete(0,tk.END)
        self.log.config(text = "Board Cleared")

    # loads Board from selected File
    def loadFile(self):
        currdir = os.getcwd()
        currdir = os.chdir('../')
        string = fd.askopenfilename(initialdir=currdir, title='Please select a file')
        if len(string) <= 0:
            self.log.config(text = "No file Selected")
            return
        self.clearBoard()
        index = 0
        self.game.file = open(string,"r")
        self.game.boardStr = self.game.file.read()
        self.game.file.close()
        sendStr = "%s"%self.game.boardStr
        self.game.copyString(sendStr)
        self.game.validSet()
        if self.game.valid == True:
            self.gameStr = "%s" %self.game.boardStr
            for i in range(9):
                for j in range(9):
                    self.CurBoard[i][j].cell.insert(0, self.game.boardStr[index])
                    if  self.CurBoard[i][j].cell.get() == "0":
                         self.CurBoard[i][j].cell.delete(0)
                    else:
                        self.CurBoard[i][j].cell.config(state = "readonly")
                    index += 1
            self.log.config(text = "Board Loaded!")
        else:
            self.clearBoard()
            self.log.config(text = "Board invalid")

    # Loads board from specific string
    def loadString(self, string):
        self.clearBoard()
        index = 0
        self.game.boardStr = "%s" %string
        self.game.validSet()
        if self.game.valid == True:
            self.gameStr = "%s" %self.game.boardStr
        
            for i in range(9):
                for j in range(9):
                    self.CurBoard[j][i].cell.insert(0, self.game.boardStr[index])
                    if  self.CurBoard[j][i].cell.get() == "0":
                         self.CurBoard[j][i].cell.delete(0)
                    else:
                        self.CurBoard[j][i].cell.config(state = "readonly")
                    index += 1
            self.log.config(text = "Board loaded from string")
        else:
            self.clearBoard()
            self.log.config(text = "Board invalid")
        
    # Sends board to Sudoku_Solver as a string
    # Returns soltuion if available
    def sendSolveStr(self):
        sendStr = ""
        for i in range(9):
            for j in range(9):
                if len(self.CurBoard[i][j].cell.get()) == 0:
                    sendStr += "0."[:-1]
                elif int(self.CurBoard[i][j].cell.get()) <= 9 or int(self.CurBoard[i][j].cell.get()) > 0:
                    sendStr += (self.CurBoard[i][j].cell.get())
        self.game.copyString(sendStr)
        self.game.checkBoard()
        if self.game.win == True:
            self.loadString(self.game.winStr)
            self.log.config(text = "Board Solved")
        else:
            self.log.config(text = "Board Unsolvable! :( ")

    # Saves current board as a specific file
    def sendFile(self):
        file = fd.asksaveasfile(mode='w', defaultextension=".txt")
        if file == None:
            self.log.config(text = "Save Cancelled")
            return
        sendStr = ""
        for i in range(9):
            for j in range(9):
                if len(self.CurBoard[i][j].cell.get()) == 0:
                    sendStr += "0."[:-1]
                elif int(self.CurBoard[i][j].cell.get()) <= 9 or int(self.CurBoard[i][j].cell.get()) > 0:
                    sendStr += (self.CurBoard[i][j].cell.get())
        file.write(sendStr)
        file.close()
        self.log.config(text = "Board saved")

if __name__ == "__main__":
    Main = SolverGUI()
    Main.window.mainloop()