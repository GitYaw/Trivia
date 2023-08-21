from PyQt5.QtWidgets import QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore

# global dictionary of widgets
widgets = {
	"logo": [],
	"button": [],
	"score": [],
	"question": [],
	"answer1": [],
	"answer2": [],
	"answer3": [],
	"answer4": [],
	"message": [],
	"message2": []
}

# initialize grid layout
grid = QGridLayout()

def clearWidgets():
	''' hide all existing widgets
		and remove from global dictionary '''
	for widget in widgets:
		if widgets[widget] != []:
			widgets[widget][-1].hide()
		for i in range(0, len(widgets[widget])):
			widgets[widget].pop()

def startGame():
	# start game, reset all widgets
	clearWidgets()
	frame2()

def answerButton(answer, left, right):
	# create answer button with custom left & right margins
	button = QPushButton(answer)
	button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
	button.setFixedWidth(485)
	button.setStyleSheet(
		# set variable margins
		"*{margin-left: " + str(left) + "px; " + 
		"margin-right: " + str(right) + "px; " + 
		'''
		border: 4px solid '#BC006C';
		color: white;
		font-family: 'shanti';
		font-size: 16px;
		border-radius: 25px;
		padding: 15px 0px;
		margin-top: 20px;
		}
		*:hover{
			background: '#BC006C';
		}
		'''
	)
	return button

#****************************************
#				FRAME 1
#****************************************

def frame1():
	# logo widget
	image = QPixmap("logo.png")
	logo = QLabel()
	logo.setPixmap(image)
	logo.setAlignment(QtCore.Qt.AlignCenter)
	logo.setStyleSheet("margin-top: 100px;")
	widgets["logo"].append(logo)

	# start button widget
	button = QPushButton("PLAY")
	button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
	button.setStyleSheet(
		'''
		*{
			border: 4px solid '#BC006C';
			border-radius: 45px;
			font-size: 35px;
			color: 'white';
			padding: 25px 0px;
			margin: 100px 200px;
		}
		*:hover{
			background: '#BC006C';
		}
		'''
	)
	# button callback
	button.clicked.connect(startGame)
	widgets["button"].append(button)

	# place widgets on grid
	grid.addWidget(logo, 0, 0, 1, 2)
	grid.addWidget(button, 1, 0, 1, 2)

#****************************************
#				FRAME 2
#****************************************

def frame2():
	# score widget
	score = QLabel("80")
	score.setAlignment(QtCore.Qt.AlignRight)
	score.setStyleSheet(
		'''
		font-size: 35px;
		color: 'white';
		padding: 15px 10px;
		margin: 20px 200px;
		background: '#64A314';
		border: 1px solid '#64A314';
		border-radius: 35px;
		'''
	)
	widgets["score"].append(score)
	
	# trivia question widget
	question = QLabel("Placeholder for the text of the trivia question")
	question.setAlignment(QtCore.Qt.AlignCenter)
	question.setWordWrap(True)
	question.setStyleSheet(
		'''
		font-family: 'shanti';
		font-size: 25px;
		color: 'white';
		padding: 75px;
		'''
	)
	widgets["question"].append(question)

	# answer button widgets
	button1 = answerButton("answer1", 85, 5)
	button2 = answerButton("answer2", 5, 85)
	button3 = answerButton("answer3", 85, 5)
	button4 = answerButton("answer4", 5, 85)

	widgets["answer1"].append(button1)
	widgets["answer2"].append(button2)
	widgets["answer3"].append(button3)
	widgets["answer4"].append(button4)

	# footer logo widget
	image = QPixmap("logo_bottom.png")
	logo = QLabel()
	logo.setPixmap(image)
	logo.setAlignment(QtCore.Qt.AlignCenter)
	logo.setStyleSheet("margin-top: 75px; margin-bottom: 30px;")
	widgets["logo"].append(logo)
	
	# place widgets on grid
	grid.addWidget(score, 0, 1)
	grid.addWidget(question, 1, 0, 1, 2)
	grid.addWidget(button1, 2, 0,)
	grid.addWidget(button2, 2, 1)
	grid.addWidget(button3, 3, 0)
	grid.addWidget(button4, 3, 1)
	grid.addWidget(logo, 4, 0, 1, 2)