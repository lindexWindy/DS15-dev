# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_mapeditor import *
from basic import *
from field_shelve import *
from Ui_MapEditorNew import *
import qrc_resource
#reload(sys)
#sys.setdefaultencoding("utf-8")

class Mapeditor(QtGui.QMainWindow):
	def __init__(self, parent = None):
		super(Mapeditor, self).__init__(parent)
		self.ui = Ui_Mapeditor()
		self.ui.setupUi(self)
		self.ui.comboBox.addItem(QString.fromUtf8("无对称性"))
		self.ui.comboBox.addItem(QString.fromUtf8("中心对称"))
		self.ui.comboBox.addItem(QString.fromUtf8("左右对称"))
		self.ui.comboBox.addItem(QString.fromUtf8("上下对称"))
		self.ui.comboBox_2.addItems(["%d" %x for x in range(5, 25)])
		self.ui.comboBox_3.addItems(["%d" %x for x in range(5, 25)])
		self.ui.comboBox_4.addItems(["%d" %x for x in (0, 1)])
		self.side = 0
		self.filename = None
		self.X = 5
		self.Y = 5
		self.scene = QtGui.QGraphicsScene()
		self.view = Ui_MapEditor(self.scene, self)
		self.ui.viewLayout.addWidget(self.view)
		self.map = []
		self.unit = [[],[]]
		
		self.ui.Button2_0.setIcon(QIcon(QPixmap(":saber0.png")))
		self.ui.Button2_1.setIcon(QIcon(QPixmap(":lancer0.png")))
		self.ui.Button2_2.setIcon(QIcon(QPixmap(":archer0.png")))
		self.ui.Button2_3.setIcon(QIcon(QPixmap(":dragon_rider0.png")))
		self.ui.Button2_4.setIcon(QIcon(QPixmap(":warrior0.png")))
		self.ui.Button2_5.setIcon(QIcon(QPixmap(":wizard0.png")))
		self.ui.Button2_6.setIcon(QIcon(QPixmap(":hero_10.png")))
		self.ui.Button2_7.setIcon(QIcon(QPixmap(":hero_20.png")))
		self.ui.Button2_8.setIcon(QIcon(QPixmap(":hero_30.png")))

		QtCore.QObject.connect(self.ui.newButton,\
							   QtCore.SIGNAL('clicked()'), self.NewFile)
		QtCore.QObject.connect(self.ui.openButton,\
							   QtCore.SIGNAL('clicked()'), self.Open)
		QtCore.QObject.connect(self.ui.saveButton,\
							   QtCore.SIGNAL('clicked()'), self.Save)
		QtCore.QObject.connect(self.ui.saveasButton,\
							   QtCore.SIGNAL('clicked()'), self.SaveAs)
		QtCore.QObject.connect(self.ui.exitButton,\
							   QtCore.SIGNAL('clicked()'), self.close)
		QtCore.QObject.connect(self.ui.cancelButton_2,\
							   QtCore.SIGNAL('clicked()'), self.delunit)
		
		QtCore.QObject.connect(self.ui.comboBox_2,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeX)
		QtCore.QObject.connect(self.ui.comboBox_3,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeY)
		QtCore.QObject.connect(self.ui.comboBox_4,\
							   QtCore.SIGNAL('currentIndexChanged(int)'), self.changeside)

		QtCore.QObject.connect(self.ui.Button1_0,\
							   QtCore.SIGNAL('clicked()'), self.button1_0)
		QtCore.QObject.connect(self.ui.Button1_1,\
							   QtCore.SIGNAL('clicked()'), self.button1_1)
		QtCore.QObject.connect(self.ui.Button1_2,\
							   QtCore.SIGNAL('clicked()'), self.button1_2)
		QtCore.QObject.connect(self.ui.Button1_3,\
							   QtCore.SIGNAL('clicked()'), self.button1_3)
		QtCore.QObject.connect(self.ui.Button1_4,\
							   QtCore.SIGNAL('clicked()'), self.button1_4)
		QtCore.QObject.connect(self.ui.Button1_5,\
							   QtCore.SIGNAL('clicked()'), self.button1_5)
		QtCore.QObject.connect(self.ui.Button1_6,\
							   QtCore.SIGNAL('clicked()'), self.button1_6)

		QtCore.QObject.connect(self.ui.Button2_0,\
							   QtCore.SIGNAL('clicked()'), self.button2_0)
		QtCore.QObject.connect(self.ui.Button2_1,\
							   QtCore.SIGNAL('clicked()'), self.button2_1)
		QtCore.QObject.connect(self.ui.Button2_2,\
							   QtCore.SIGNAL('clicked()'), self.button2_2)
		QtCore.QObject.connect(self.ui.Button2_3,\
							   QtCore.SIGNAL('clicked()'), self.button2_3)
		QtCore.QObject.connect(self.ui.Button2_4,\
							   QtCore.SIGNAL('clicked()'), self.button2_4)
		QtCore.QObject.connect(self.ui.Button2_5,\
							   QtCore.SIGNAL('clicked()'), self.button2_5)
		QtCore.QObject.connect(self.ui.Button2_6,\
							   QtCore.SIGNAL('clicked()'), self.button2_6)
		QtCore.QObject.connect(self.ui.Button2_7,\
							   QtCore.SIGNAL('clicked()'), self.button2_7)
		QtCore.QObject.connect(self.ui.Button2_8,\
							   QtCore.SIGNAL('clicked()'), self.button2_8)

		QtCore.QObject.connect(self.ui.tab_1,\
							   QtCore.SIGNAL('currentChanged(int)'), self.changemode)

  
	def delunit(self):
		self.view.DelUnit(self.side)
		
	def changeX(self, x):
		self.X = x + 5

	def changeY(self, y):
		self.Y = y + 5

	def changeside(self, side):
		self.side = side

	def changemode(self, mode):
		if(mode == 0):
			self.view.EditMapMode()
		if(mode == 1):
			self.view.EditUnitMode()
			
	def button1_0(self):
		self.view.ChangeTerrain(0)

	def button1_1(self):
		self.view.ChangeTerrain(1)

	def button1_2(self):
		self.view.ChangeTerrain(2)

	def button1_3(self):
		self.view.ChangeTerrain(3)

	def button1_4(self):
		self.view.ChangeTerrain(4)

	def button1_5(self):
		self.view.ChangeTerrain(5)

	def button1_6(self):
		self.view.ChangeTerrain(6)

	def button2_0(self):
		self.view.AddUnit(self.side, 0)

	def button2_1(self):
		self.view.AddUnit(self.side, 1)

	def button2_2(self):
		self.view.AddUnit(self.side, 2)

	def button2_3(self):
		self.view.AddUnit(self.side, 3)

	def button2_4(self):
		self.view.AddUnit(self.side, 4)

	def button2_5(self):
		self.view.AddUnit(self.side, 5)

	def button2_6(self):
		self.view.AddUnit(self.side, 6)

	def button2_7(self):
		self.view.AddUnit(self.side, 7)

	def button2_8(self):
		self.view.AddUnit(self.side, 8)
		
	def SetMap(self):
		self.map, self.unit = self.view.GetMapData()
		write_to((self.map, self.unit), "%s"%self.filename)
		Ui_MapEditor.DATA_ = False

	def OpenFile(self):
		self.map, self.unit = read_from("%s"%self.filename)
		Ui_MapEditor.DATA_DIRTY = False
		#print self.map
		#print self.unit
	
	def couldSave(self):
		return True

	def isSaved(self):
		return Ui_MapEditor.DATA_DIRTY == False

	def Save(self):
		if self.couldSave():
			if not self.isSaved():
				if self.filename == "Untitled.map":
					self.filename = QFileDialog.getSaveFileName(self, "Save",
															"/.", "*.map")
				if self.filename != QString(""):
					self.SetMap()
				else:
					pass#raise error
		else:
			box = QMessageBox(QMessageBox.Warning, "Error", "The document can't be saved!")
			box.exec_()

	def Open(self):	   
		if self.isSaved():
			self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
			if self.filename != QString(""):
				self.OpenFile()
				self.view.LoadMap(self.map, self.unit)
				Ui_MapEditor.DATA_DIRTY = False
				self.X = len(self.map)
				self.ui.comboBox_2.setCurrentIndex(self.X - 5)
				self.Y = len(self.map[0])
				self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
			else:
				pass#raise error
		else:
			choose = QMessageBox.question(self, "Save", "Do you want to save the changes?",
										  QMessageBox.Save|QMessageBox.Discard|
										  QMessageBox.Cancel)
			if choose == QMessageBox.Save:
				self.Save()
				self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
				if self.filename != QString(""):
					self.OpenFile()
					self.view.LoadMap(self.map, self.unit)
					Ui_MapEditor.DATA_DIRTY = False
					self.X = len(self.map)
					self.ui.comboBox_2.setCurrentIndex(self.X - 5)
					self.Y = len(self.map[0])
					self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
				else:
					pass#raise error
			elif choose == QMessageBox.Discard:
				self.filename = QFileDialog.getOpenFileName(self, "Open File",
														"/.", "*.map")
				if self.filename != QString(""):
					self.OpenFile()
					self.view.LoadMap(self.map, self.unit)
					Ui_MapEditor.DATA_DIRTY = False
					self.X = len(self.map)
					self.ui.comboBox_2.setCurrentIndex(self.X - 5)
					self.Y = len(self.map[0])
					self.ui.comboBox_3.setCurrentIndex(self.Y - 5)
				else:
					pass#raise error
			else:
				pass

	def NewFile(self):
		if self.isSaved():
			self.filename = "Untitled.map"
			self.setWindowTitle("Map Editor --" + self.filename)
			self.view.NewMap(self.X, self.Y)
			Ui_MapEditor.DATA_DIRTY = True
		else:
			choose = QMessageBox.question(self, "Save", "Do you want to save the changes?",
										  QMessageBox.Save|QMessageBox.Discard|
										  QMessageBox.Cancel)
			if choose == QMessageBox.Save:
				self.Save()
				self.filename = "Untitled.map"
				self.setWindowTitle("Map Editor --" + self.filename)
				self.view.NewMap(self.X, self.Y)
				Ui_MapEditor.DATA_DIRTY = True
			elif choose == QMessageBox.Discard:
				self.filename = "Untitled.map"
				self.setWindowTitle("Map Editor --" + self.filename)
				self.view.NewMap(self.X, self.Y)
				Ui_MapEditor.DATA_DIRTY = True
			else:
				pass

	def SaveAs(self):
		if self.couldSave():
			self.filename = QFileDialog.getSaveFileName(self, "Save",
														"/.", "*.map")
			if self.filename != QString(""):
				self.SetMap()
			else:
				pass#raise error
		else:
			box = QMessageBox(QMessageBox.Warning, "Error", "The document can't be saved!")
			box.exec_()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mapapp = Mapeditor()
	mapapp.show()   
	sys.exit(app.exec_())
