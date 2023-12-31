from PyQt5.QtWidgets import QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from urllib.request import urlopen # accessing url
import json # data in json format
import pandas as pd # handling data
import random

url = "https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple"
with urlopen(url) as webpage:
	data = json.loads(webpage.read().decode())
	df = pd.DataFrame(data["results"])
	order = list(range(0, len(df)))

def loadQuestion(number):
	question = df["question"][number]
	correct = df["correct_answer"][number]
	wrong = df["incorrect_answers"][number]

	formatting = [
		("#039;", "'"),
		("&'", "'"),
		("&quot;", '"'),
		("&lt;", "<"),
		("&gt;", ">")
	]

	for tuple in formatting:
		question = question.replace(tuple[0], tuple[1])
		correct = correct.replace(tuple[0], tuple[1])
		wrong = [answer.replace(tuple[0], tuple[1]) for answer in wrong]

	parameters["question"].append(question)
	parameters["correct"].append(correct)

	answers = wrong + [correct]
	random.shuffle(answers)

	for i in range(4):
		parameters["answer" + str(i + 1)].append(answers[i])
	
	print(correct) # for testing

parameters = {
	"number": 0,
	"question": [],
	"answer1": [],
	"answer2": [],
	"answer3": [],
	"answer4": [],
	"correct": [],
	"score": 0,
}

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
		widgets[widget].clear()

def clearParameters():
	for parameter in parameters:
		if type(parameters[parameter]) == list:
			parameters[parameter].clear()
	
	parameters["number"] = 0
	parameters["score"] = 0

def startGame():
	clearParameters()

	random.shuffle(order)
	loadQuestion(order[parameters["number"]])
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
		border-radius: 25px;
		color: white;
		font-family: 'Shanti';
		font-size: 16px;
		margin-top: 20px;
		padding: 15px 0px;
		}
		*:hover{
			background: '#BC006C';
		}
		'''
	)
	button.clicked.connect(lambda: checkAnswer(button))
	return button

def checkAnswer(button):
	if button.text() == parameters["correct"][-1]:
		score = parameters["score"] + 10
		parameters["score"] = score
		widgets["score"][-1].setText(str(score))

		if score >= 100:
			frame4()
		else:
			parameters["number"] += 1
			loadQuestion(order[parameters["number"]])
			widgets["question"][-1].setText(parameters["question"][-1])
			widgets["answer1"][-1].setText(parameters["answer1"][-1])
			widgets["answer2"][-1].setText(parameters["answer2"][-1])
			widgets["answer3"][-1].setText(parameters["answer3"][-1])
			widgets["answer4"][-1].setText(parameters["answer4"][-1])

	else:
		frame3()

#****************************************
#				FRAME 1
#****************************************

def frame1():
	clearWidgets()

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
			color: 'white';
			font-size: 35px;
			margin: 100px 200px;
			padding: 25px 0px;
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
	clearWidgets()

	# score widget
	score = QLabel(str(parameters["score"]))
	score.setAlignment(QtCore.Qt.AlignRight)
	score.setStyleSheet(
		'''
		background: '#64A314';
		border: 1px solid '#64A314';
		border-radius: 35px;
		color: 'white';
		font-size: 35px;
		padding: 15px 10px;
		margin: 20px 200px;
		'''
	)
	widgets["score"].append(score)
	
	# trivia question widget
	question = QLabel(parameters["question"][-1])
	question.setAlignment(QtCore.Qt.AlignCenter)
	question.setWordWrap(True)
	question.setStyleSheet(
		'''
		color: 'white';
		font-family: 'Shanti';
		font-size: 25px;
		padding: 75px;
		'''
	)
	widgets["question"].append(question)

	# answer button widgets
	button1 = answerButton(parameters["answer1"][-1], 85, 5)
	button2 = answerButton(parameters["answer2"][-1], 5, 85)
	button3 = answerButton(parameters["answer3"][-1], 85, 5)
	button4 = answerButton(parameters["answer4"][-1], 5, 85)

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

#****************************************
#				FRAME 3
#****************************************

def frame3():
	clearWidgets()

	# retry widget
	message = QLabel("Sorry, your answer\nwas wrong. \nYour score is:")
	message.setAlignment(QtCore.Qt.AlignRight)
	message.setStyleSheet(
		'''
		color: 'white';
		font-family: 'Shanti';
		font-size: 35px;
		margin: 75px 5px;
		padding: 20px;
		'''
	)
	widgets["message"].append(message)

	# score widget
	score = QLabel(str(parameters["score"]))
	score.setStyleSheet(
		'''
		color: white;
		font-size: 100px;
		margin: 0 75px 0px 75px;
		'''
	)
	widgets["score"].append(score)

	# continue button widget
	button = QPushButton('TRY AGAIN')
	button.setStyleSheet(
		'''*{
			background:'#BC006C';
			border: 1px solid '#BC006C';
			border-radius: 40px;
			color: 'white';
			font-family: 'Arial';
			font-size: 25px;
			margin: 10px 300px;
			padding: 25px 0px;
		}
		*:hover{
			background:'#FF1B9E';
		}'''
	)
	button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
	button.clicked.connect(frame1)
	widgets["button"].append(button)

	# footer logo widget
	pixmap = QPixmap('logo_bottom.png')
	logo = QLabel()
	logo.setPixmap(pixmap)
	logo.setAlignment(QtCore.Qt.AlignCenter)
	logo.setStyleSheet(
		'''
		margin-bottom: 20px;
		margin-top: 75px;
		padding: 10px;
		'''
	)
	widgets["logo"].append(logo)

	# place widgets on grid
	grid.addWidget(message, 0, 0)
	grid.addWidget(score, 0, 1)
	grid.addWidget(button, 1, 0, 1, 2)
	grid.addWidget(logo, 2, 0, 1, 2)

#****************************************
#				FRAME 4
#****************************************

def frame4():
	clearWidgets()

	# celebration widget
	message = QLabel("Congratulations! You\nare a true programmer!\nYour score is:")
	message.setAlignment(QtCore.Qt.AlignRight)
	message.setStyleSheet(
		'''
		color: 'white';
		font-family: 'Shanti';
		font-size: 25px;
		margin: 100px 0px;
		'''
	)
	widgets["message"].append(message)

	# score widget
	score = QLabel(str(parameters["score"]))
	score.setStyleSheet(
		'''
		color: #8FC740;
		font-size: 100px;
		margin: 0px 75px 0px 75px;
		'''
	)
	widgets["score"].append(score)

	# continue widget
	message2 = QLabel("Would you like to try again?")
	message2.setAlignment(QtCore.Qt.AlignCenter)
	message2.setStyleSheet(
		'''
		color: 'white';
		font-family: 'Shanti';
		font-size: 30px;
		margin-bottom: 75px;
		margin-top: 0px;
		'''
	)
	widgets["message2"].append(message2)

	# continue button widget
	button = QPushButton('Try Again')
	button.setStyleSheet(
		'''*{
			background:'#BC006C';
			color: 'white';
			border: 1px solid '#BC006C';
			border-radius: 40px;
			font-family: 'Shanti';
			font-size: 25px;
			margin: 10px 300px;
			padding: 25px 0px;
		}
		*:hover{
			background:'#FF1B9E';
		}'''
	)
	button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
	button.clicked.connect(frame1)
	widgets["button"].append(button)

	# footer logo widget
	pixmap = QPixmap('logo_bottom.png')
	logo = QLabel()
	logo.setPixmap(pixmap)
	logo.setAlignment(QtCore.Qt.AlignCenter)
	logo.setStyleSheet(
		'''
		margin-bottom: 20px;
		margin-top: 75px;
		padding: 10px;
		'''
	)
	widgets["logo"].append(logo)

	# place widgets on grid
	grid.addWidget(message, 0, 0)
	grid.addWidget(score, 0, 1)
	grid.addWidget(message2, 1, 0, 1, 2)
	grid.addWidget(button, 2, 0, 1, 2)
	grid.addWidget(logo, 3, 0, 1, 2)