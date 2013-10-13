#-*- coding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lib.human.Humanai_Replay_event import HumanReplay

class AiReplayWidget(QWidget):
	def __init__(self, scene, parent = None):
		QWidget.__init__(self, parent)

		self.isPaused = False
		self.started = False
		self.replayWidget = HumanReplay(scene, parent)
		self.ctrlSlider = QSlider()
		self.ctrlSlider.setRange(0, 300)
		self.totalLabel = QLabel(QString.fromUtf8("总回合:"))
		self.nowLabel = QLabel(QString.fromUtf8("当前显示回合:"))
		self.totalInfo = QLCDNumber()
		self.totalInfo.display(0)
		self.totalInfo.setSegmentStyle(QLCDNumber.Flat)
		self.totalStatusInfo = QLabel(QString.fromUtf8("开始阶段"))
		self.nowInfo = QLineEdit("")
		self.nowInfo.setText("0")
		self.pauseButton = QPushButton("暂停")
		self.pauseButton.setCheckable(True)
		self.totalStatusInfo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))
		self.pauseLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed|QSizePolicy.Fixed))

		hlayout = QHBoxLayout()
		hlayout.addWidget(self.totalLabel)
		hlayout.addWidget(self.totalInfo)
		hlayout.addWidget(self.totalStatusInfo)
		hlayout.addWidget(self.nowLabel)
		hlayout.addWidget(self.nowInfo)
		hlayout.addWidget(self.pauseButton)
		hlayout.addStretch()
		hlayout.addWidget(self.pauseLabel)

		vlayout = QVBoxLayout()
		vlayout.addWidget(self.replayWidget)
		vlayout.addWidget(self.ctrlSlider)
		vlayout.addLayout(hlayout)

		self.setLayout(vlayout)

		self.connect(self.ctrlSlider, SIGNAL("valueChanged(int)"),
					 self.setNowRound,Qt.QueuedConnection)
		#self.connect(self.ctrlSlider, SIGNAL("totalChanged()"),
		#			 self.updateUI)
		self.connect(self.nowInfo, SIGNAL("textEdited(QString)"), self.setNowRound)
		self.connect(self.pauseButton, SIGNAL("toggled(bool)"), self.pauseGame)
		self.replayWidget.moveAnimEnd.connect(self.on_aniF)#partial(self.ctrlSlider.changeNowRound,
													  #self.ctrlSlider.nowRound+1,
													  #not self.ctrlSlider.nowStatus))
		self.updateUI()
		
	def setNowRound(self, new_round):
		if isinstance(new_round, QString):
			new_round = unicode(new_round)
			if not len(new_round):
				self.nowInfo.setText("%d", self.replayWidget.nowRound)
				self.nowInfo.selectAll()
				self.nowInfo.setFocus()
			elif new_round.isdigit() and 0 <= int(new_round) <= self.replayWidget.latestRound:
				self.ctrlSlider.setValue(int(new_round) * 2)
			else:
				self.nowInfo.setText("%d", self.replayWidget.nowRound)
				self.nowInfo.selectAll()
				self.nowInfo.setFocus()
		else:
			if new_round == self.replayWidget.nowRound * 2 + self.replayWidget.nowStatus:
				return
			if 0 <= new_round <= self.replayWidget.latestRound * 2 + self.replayWidget.nowStatus:
				self.replayWidget.GoToRound(int(new_round / 2), new_round % 2)
				self.emit(SIGNAL("goToRound"), self.replayWidget.nowRound, self.replayWidget.nowStatus, self.replayWidget.gameBegInfo[self.replayWidget.nowRound],
									self.replayWidget.gameEndInfo[self.replayWidget.nowRound])
				self.nowInfo.setText("%d", self.replayWidget.nowRound)
				if not self.isPaused:
					if self.replayWidget.nowStatus:
						self.ctrlSlider.setValue((self.replayWidget.nowRound + 1) * 2)
					else:
						if self.okToPlay():
							self.replayWidget.Play()
						else:
							self.pauseButton.setChecked(True)
			else:
				self.replayWidget.GoToRound(self.replayWidget.latestRound, 0)
				self.nowInfo.setText("%d", self.replayWidget.nowRound)
				self.ctrlSlider.setValue(self.replayWidget.latestRound * 2 + self.replayWidget.latestStatus)
				self.pauseButton.setChecked(True)
				
	def okToPlay(self):
		if self.replayWidget.nowRound == self.replayWidget.latestRound and len(self.replayWidget.gameEndInfo) < self.replayWidget.latestRound + 1:
			return False
		return True

	def updateIni(self, begInfo, frInfo):
		self.replayWidget.Initialize(begInfo, frInfo)

	def updateBeg(self, begInfo):
		self.replayWidget.UpdateBeginData(begInfo)
		self.totalInfo.display(self.replayWidget.latestRound)

	def updateEnd(self, cmdInfo, endInfo):
		self.replayWidget.UpdateEndData(cmdInfo, endInfo)
		if not self.isPaused:
			self.pauseGame(False)

	def pauseGame(self, pause):
		self.isPaused = pause
		if pause:
			self.replayWidget.GoToRound(self.replayWidget.nowRound, self.replayWidget.nowStatus)
		else:
			if self.replayWidget.nowStatus:
				self.setNowRound((self.replayWidget.nowRound+1) * 2)
			else:
				if okToPlay():
					self.replayWidget.Play()
					
	def on_aniF(self):
		self.setNowRound((self.replayWidget.nowRound + 1) * 2)
		if not self.isPaused:
			self.replayWidget.Play()
			