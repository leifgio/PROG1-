from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random


class Separator(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.configFont = QtGui.QFont()
        self.configFont.setPixelSize(16)
        self.configFont.setBold(True)
        self.setGeometry(10, 10, 500, 40)
        self.setFixedHeight(40)
        self.victoryText = ("you win with " + str(window.trials) + " tries!")
        self.loseText = ("you lose the answer is " + str(window.possibleAnswers[window.answer[0]] + ", " + window.possibleAnswers[window.answer[1]] + ", " + window.possibleAnswers[window.answer[2]] + ", " + window.possibleAnswers[window.answer[3]]))
        window.theBox.widgetList.append(self)
        self.show()

    # print the answer if lose, number of trials if win
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setFont(self.configFont)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        painter.drawRect(20, 5, 490, 30)
        if window.solved:
            painter.drawText(30, 23, self.victoryText)
        else:
            painter.drawText(30, 23, self.loseText)


class GuessRow(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.configFont = QtGui.QFont()
        self.configFont.setPixelSize(16)
        self.configFont.setBold(True)

        self.colours = window.guess
        self.setGeometry(10, 10, 500, 88)
        self.setFixedHeight(88)
        self.textToDrawTop = (str("Exact: " + str(window.evaluation[0])))
        self.textToDrawBottom = (" Correct: " + str(window.evaluation[1]))
        window.theBox.widgetList.append(self)
        if window.trials == 12:  # check if lose
            window.pbSubmit.setEnabled(False)
        if window.evaluation[0] == 4:  # check if win
            window.solved = True
            window.pbSubmit.setEnabled(False)
        self.show()

    def paintEvent(self, e):  # draw circles
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        for i in range(4):
            if self.colours[i] == 0:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            elif self.colours[i] == 1:
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            elif self.colours[i] == 2:
                painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
            elif self.colours[i] == 3:
                painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            elif self.colours[i] == 4:
                painter.setBrush(QBrush(Qt.magenta, Qt.SolidPattern))
            elif self.colours[i] == 5:
                painter.setBrush(QBrush(Qt.cyan, Qt.SolidPattern))
            painter.drawEllipse(25+100*(i), 10, 80, 65)

        painter.setFont(self.configFont)
        painter.drawText(425, 30, self.textToDrawTop)
        painter.drawText(420, 55, self.textToDrawBottom)


class Scrolling(QScrollArea):  # For the board
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        global contents
        self.setWidgetResizable(True)
        # making qwidget object
        contents = QWidget(self)
        self.setWidget(contents)
        # vertical box layout
        self.lay = QVBoxLayout(contents)
        self.widgetList = []

# main window


class Window(QMainWindow):
    def __init__(self):
        super().__init__()  # variables, data
        self.solved = False
        self.isClassic = True
        self.choices = 6
        self.trials = 0
        self.evaluation = []
        self.answer = []
        self.possibleAnswers = ["Red", "Green",
                                "Blue", "Yellow", "Magenta", "Cyan"]
        self.title = "Mastermind Gui"
        self.top = 100
        self.left = 100
        self.width = 710
        self.minimumWidth = 710
        self.height = 675
        self.minimumHeight = 300
        self.GUI()
        self.InitWindow()
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)

    def GUI(self):  # main window
        self.theBox = Scrolling(self)
        self.theBox.setGeometry(10, 75, 550, 565)
        ghostWid = QLabel(contents)
        ghostWid.setGeometry(10, 10, 500, 88)
        ghostWid.setMaximumHeight(450)
        ghostWid.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.theBox.lay.insertWidget(0, ghostWid)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.cbGuess1 = QtWidgets.QComboBox(self)
        self.cbGuess1.setGeometry(QtCore.QRect(10, 10,  85, 50))
        self.cbGuess1.setFont(font)
        self.cbGuess1.addItems(self.possibleAnswers)

        self.cbGuess2 = QtWidgets.QComboBox(self)
        self.cbGuess2.setGeometry(QtCore.QRect(105, 10, 85, 50))
        self.cbGuess2.setFont(font)
        self.cbGuess2.addItems(self.possibleAnswers)

        self.cbGuess3 = QtWidgets.QComboBox(self)
        self.cbGuess3.setGeometry(QtCore.QRect(200, 10, 85, 50))
        self.cbGuess3.setFont(font)
        self.cbGuess3.addItems(self.possibleAnswers)

        self.cbGuess4 = QtWidgets.QComboBox(self)
        self.cbGuess4.setGeometry(QtCore.QRect(295, 10, 85, 50))
        self.cbGuess4.setFont(font)
        self.cbGuess4.addItems(self.possibleAnswers)

        self.pbSubmit = QPushButton("submit", self)
        self.pbSubmit.setGeometry(QRect(390, 10, 100, 50))
        self.pbSubmit.setEnabled(False)
        self.pbSubmit.clicked.connect(self.SubmitClicked)

        self.rbClassic = QRadioButton("classic", self)
        self.rbClassic.setGeometry(QRect(580, 10, 120, 50))
        self.rbClassic.clicked.connect(self.classicClicked)

        self.rbCrazymode = QRadioButton("crazymode", self)
        self.rbCrazymode.setGeometry(QRect(580, 40, 120, 50))
        self.rbCrazymode.clicked.connect(self.crazymodeClicked)

        self.lblRules = QLabel(self)
        self.lblRules.setGeometry(QRect(580, 200, 120, 250))

        self.pbRules = QPushButton("rules", self)
        self.pbRules.setGeometry(QRect(580, 500, 120, 50))
        self.pbRules.clicked.connect(self.showRules)

        self.pbPlayAgain = QPushButton("play again", self)
        self.pbPlayAgain.setGeometry(QRect(580, 550, 120, 50))
        self.pbPlayAgain.clicked.connect(self.playAgainClicked)

        # Classic MM
    def classicEval(self, guess, solution):
        exactGuess = 0
        correctGuess = 0
        for i in range(4):
            if guess[i] == solution[i] and solution[i] != -1:
                solution[i] = 'x'  # Prevent duplicate
                guess[i] = 'y'
                exactGuess += 1
        for i in range(len(guess)):
            if guess[i] in solution:
                solution.remove(guess[i])
                guess[i] = -1
                correctGuess += 1
        return(exactGuess, correctGuess)

    # Mastermind crazy mode allow duplicate evaluation
    def crazymodeEval(self, guess, solution):
        exactGuess = 0
        correctGuess = 0
        for i in range(0, 4):  # Check for correct number in correct position
            if guess[i] == solution[i]:
                exactGuess += 1
            else:
                for sagot in solution:  # Check for correct number in wrong position
                    if sagot == guess[i]:
                        correctGuess += 1
                        break
        return(exactGuess, correctGuess)

    # event func, choose logic
    def classicClicked(self):
        self.solved = False
        self.isClassic = True
        self.pbSubmit.setEnabled(True)
        self.rbClassic.setEnabled(False)
        self.rbCrazymode.setEnabled(False)
        self.answer = []
        self.trials = 0
        for i in range(4):
            self.answer.append(random.randrange(self.choices))

    # event func
    def crazymodeClicked(self):
        self.solved = False
        self.isClassic = False
        self.pbSubmit.setEnabled(True)
        self.rbClassic.setEnabled(False)
        self.rbCrazymode.setEnabled(False)
        self.answer = []
        self.trials = 0
        for i in range(4):
            self.answer.append(random.randrange(self.choices))

    # display guess and eval after submit
    def AddRow(self):
        self.trials += 1
        nextRow = GuessRow(contents)
        self.theBox.lay.insertWidget(0, nextRow)
        if window.trials == 12:
            nextSepar = Separator(contents)
            window.theBox.lay.insertWidget(0, nextSepar)
        if window.solved == True:
            nextSepar = Separator(contents)
            window.theBox.lay.insertWidget(0, nextSepar)

    # event that gets the guess of player
    def SubmitClicked(self):
        self.guess = (self.cbGuess1.currentIndex(), self.cbGuess2.currentIndex(),
                      self.cbGuess3.currentIndex(), self.cbGuess4.currentIndex())
        if self.isClassic:
            self.evaluation = self.classicEval(
                list(self.guess), list(self.answer))
        else:
            self.evaluation = self.crazymodeEval(
                list(self.guess), list(self.answer))
        self.AddRow()
        contents.update()  # refresh widget

    # file handling, try except, message box
    def showRules(self):
        try:
            self.rules = open("game-rules.txt", "r")
            self.textMessage = self.rules.read()
        except:
            # try to change file name of txt file for debugging
            self.textMessage = "Error: file not found"

        self.mbMessage = QMessageBox()  # no ui file (hardcoded)
        self.mbMessage.setIcon(QMessageBox.Information)
        self.mbMessage.setWindowIcon(QtGui.QIcon('icon.png'))
        self.mbMessage.setWindowTitle("rules")
        self.mbMessage.setText(self.textMessage)
        self.mbMessage.exec_()

    # resets the board - back to start of procedure
    def playAgainClicked(self):
        for i in range(self.theBox.lay.count()):
            self.theBox.lay.itemAt(i).widget().close()
        ghostWid = QLabel(contents)
        ghostWid.setGeometry(10, 10, 500, 88)
        ghostWid.setMaximumHeight(450)
        ghostWid.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.theBox.lay.insertWidget(0, ghostWid)
        self.rbCrazymode.setEnabled(True)
        self.rbClassic.setEnabled(True)
        self.pbSubmit.setEnabled(False)

    # main window size
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
