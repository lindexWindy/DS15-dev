# -*- coding: UTF-8 -*-

#last edition: 2013-09-29-21:35

import sys, math
from Ui_2DReplaySceneNew import *
import qrc_resource
GRID_CENTER = QtCore.QPointF(UNIT_WIDTH/2, UNIT_HEIGHT/2)



class Ui_NewMapUnit(Ui_MapUnit):
	def __init__(self, x, y, mapGrid, parent = None):
		Ui_MapUnit.__init__(self, x, y, mapGrid, parent)
		self.mapGrid = mapGrid
		self.tempPointer = None		
   
	def MousePressEvent(self, info):
		if (self.IsEnabled()):
			self.selected = not self.selected
			for label in self.relatedLabel:
				label.SetEnabled(self.selected)
			return True
		else:
			return False
		
	def MouseReleaseEvent(self, info):
		if (self.tempPointer!=None):
			self.scene().removeItem(self.tempPointer)
			self.tempPointer = None
		return True
	def MouseLeaveEvent(self, info):
		if (self.tempPointer!=None):
			self.scene().removeItem(self.tempPointer)
			self.tempPointer = None
		return True

	def DragStartEvent(self, info):
		if (self.IsEnabled() and self.terrain == MIRROR):
			return self
	def DragStopEvent(self, args):
		dragUnit, info = args
		dragUnit.unsetCursor()
		if (not self.IsEnabled()):
			dragUnit.setPos(info.nowCoor-DRAG_SPOT)#handles the drag-move event
			return True#soldier editing...
		if (info.eventAccept):
			pen = QtGui.QPen()
			pen.setWidth(5)
			pen.setColor(QtGui.QColor(0, 0, 0, 255))
			if (self.tempPointer!=None):
				self.scene().removeItem(self.tempPointer)
			self.tempPointer = self.scene().addLine(QtCore.QLineF(dragUnit.GetPos()+GRID_CENTER,
													  self.GetPos()+GRID_CENTER))
		return True
	def DragComplete(self, info):
#		#what if stops on self?
		if (info.eventAccept):
			if (self.terrain==GEAR):
				if (info.nowPos in self.mapGrid.trap or info.nowPos in self.mapGrid.barrier):
					return
				s = QtCore.QStringList()
				s << "trap" << "barrier"
				selection, ok = QtGui.QInputDialog.getItem(self.window(), "GEAR",
														  "Which should be triggered?",
														  s, 0, False)
				if (ok):
					label = Ui_GridLabel(selection, info.nowPos[0], info.nowPos[1])
					self.scene().addItem(label)
					self.relatedLabel.append(label)
				Ui_MapEditor.DATA_DIRTY = True
			elif (self.terrain==MIRROR):
				if (info.nowPos==self.mapGrid.out):
					return
				label = Ui_GridLabel("exit", info.nowPos[0], info.nowPos[1])
				self.scene().addItem(label)
				for oldlabel in self.relatedLabel:
					self.scene().removeItem(oldlabel)
				self.relatedLabel.append(label)
				Ui_MapEditor.DATA_DIRTY = True

	def paint(self, painter, option, widget):
		#if self.selected and self.onshow:
			#pass
			#brush = QtGui.QBrush()
			#brush.setColor(QtGui.QColor(255, 255, 255))
			#brush.setStyle(QtCore.Qt.SolidPattern)
			#painter.setBrush(brush)
			#painter.drawRect(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT))
		#else:
		ImageName = {PLAIN:":plain.png",
					 MOUNTAIN:":mountain.png",
					 FOREST:":forest.png",
					 BARRIER:":barrier.png",
					 TURRET:":turret.png",
					 TEMPLE:":temple.png",
					 MIRROR:":mirror.png"}

		painter.drawPixmap(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT), QtGui.QPixmap(ImageName[self.terrain]))

class Ui_NewSoldierUnit(Ui_SoldierUnit):
	def __init__(self, idNum, side, unit, parent = None):
		Ui_SoldierUnit.__init__(self, idNum, side, unit, parent)
	def paint(self, painter, option, widget):
		painter.drawRect(10, 10, 50, 50)#for test

	def DragStartEvent(self, info):
		if (self.IsEnabled()):
			return self
		
	def DragStopEvent(self, args):
		if (not self.IsEnabled()):
			return False#map editing...
		dragUnit, info = args
		info.eventAccept = False
		dragUnit.setPos(info.nowCoor-DRAG_SPOT)#handles the drag-move event
		if (dragUnit is not self):
			dragUnit.setCursor(QtCore.Qt.ForbiddenCursor)
		else:
			dragUnit.unsetCursor()
		return True
	
	def DragComplete(self, info):
		for item in self.scene().items():
			item.unsetCursor()
		if (info.eventAccept):
			self.SetMapPos(info.nowPos[0], info.nowPos[1])
			Ui_MapEditor.DATA_DIRTY = True
		else:
			self.setPos(self.GetPos())
	def DragFail(self, info):
		self.unsetCursor()
		self.setPos(self.GetPos())
		
	def paint(self, painter, option, widget):
		ImageName = {SABER:":saber0.png",
					 LANCER:":lancer0.png",
					 ARCHER:":archer0.png",
					 DRAGON_RIDER:":dragon_rider0.png",
					 WARRIOR:":warrior0.png",
					 WIZARD:":wizard0.png",
					 HERO_1:":hero_10.png",
					 HERO_2:":hero_20.png",
					 HERO_3:":hero_30.png"}
		ImageName2 = {SABER:":saber1.png",
					 LANCER:":lancer1.png",
					 ARCHER:":archer2.png",
					 DRAGON_RIDER:":dragon_rider1.png",
					 WARRIOR:":warrior1.png",
					 WIZARD:":wizard1.png",
					 HERO_1:":hero_11.png",
					 HERO_2:":hero_21.png",
					 HERO_3:":hero_31.png"}
		if self.side == 0:
			ImageRoute = ImageName[self.type]
		else:
			ImageRoute = ImageName2[self.type]
		painter.drawPixmap(QtCore.QRect(0, 0, UNIT_WIDTH, UNIT_HEIGHT), QtGui.QPixmap(ImageRoute))			
		
#units of map editor

class Ui_MapEditor(Ui_ReplayView):
	"display widget in map editor. \
	data: \
	newMap : Map \
	iniUnits : array of Units"
	def __init__(self, scene, parent = None):
		Ui_ReplayView.__init__(self, scene, parent)
		self.newMap = []
		#self.usableGrid = []
		self.iniUnits = [[], []]
		self.setAcceptDrops(True)

	def NewMap(self, x = 0, y = 0):
		"Initialize(int x = 0, int y = 0) -> void \
		create a new map(default terrain: PLAIN). \
		x and y is the size of the map. "
		self.newMap = []
		i = 0
		while (i<x):
			j = 0
			newColumn = []
			while (j<y):
				newColumn.append(Map_Basic(PLAIN))
				j += 1
			self.newMap.append(newColumn)
			i += 1
		self.Initialize(self.newMap, {}, Ui_NewMapUnit)
		self.iniUnits = [[], []]

	def LoadMap(self, maps, units):
		self.newMap = maps
		self.Initialize(self.newMap, {}, Ui_NewMapUnit)
		for column in self.mapItem:
			for mapUnit in column:
				for label in mapUnit.relatedLabel:
					self.scene().addItem(label)
		for side in (0, 1):
			for unit in units[side]:
				self.AddUnit(side, unit.kind, unit.position)

	def GetMapData(self):
		maps = self.newMap
		func = lambda item: UiD_BaseUnit(item.type, (item.mapX, item.mapY)).soldier
		units = [map(func, self.iniUnits[0]),
			map(func, self.iniUnits[1])]
		return maps, units

	def ChangeTerrain(self, terrain):
		"ChangeTerrain(enum TERRAIN terrain) -> void \
		change the terrain of selected map grids "
		for i in range(len(self.newMap)):
			for j in range(len(self.newMap[i])):
				if (self.mapItem[i][j].selected):
					self.mapItem[i][j].terrain = terrain
					self.newMap[i][j] = MAP_BASE[terrain](terrain)
					self.mapItem[i][j].selected = False
					for pt in self.mapItem[i][j].relatedLabel:
						self.scene().removeItem(pt)
					self.mapItem[i][j].relatedLabel = []
		Ui_MapEditor.DATA_DIRTY = True
		self.scene().update()

	def AddUnit(self, side, soldierType = TEMP_SOLDIER, position = None):
		"AddUnit(enum(0, 1) side, Coord. position = None) -> Coord. newPos \
		add a new unit to a certain side returning the position it will placed at. \
		position indicates where the new unit should be set. \
		if it is None, a valid and random position will be distributed. \
		error will be raised if the position is invalid."
		usedGrid = []
		for s in (0, 1):
			usedGrid.extend(map(lambda unit: (unit.mapX, unit.mapY),
								self.iniUnits[s]))
		if (position==None):
			for pos in [(i, j) for i in range(self.mapSize[0])
						for j in range(self.mapSize[1])]:
				if (pos not in usedGrid):
					usableGrid = pos
					break
			else:
				raise Ui_Error, ("AddUnitError_0",
								 ("class Ui_MapEditor", "func AddUnit"),
								 "无合法的格点。")
		else:
			if (position not in usedGrid):
				usableGrid = position
			else:
				raise Ui_Error, ("AddUnitError_1",
								 ("class Ui_MapEditor", "func AddUnit"),
								 "所选格点不合法，或已有单位存在。")
		idNum = (side, len(self.iniUnits[side]))
		newSoldier = UiD_BaseUnit(soldierType, usableGrid)
		newUnit = Ui_NewSoldierUnit(idNum, side, newSoldier)
		#newUnit.setPos(newUnit.GetPos())
		self.AddItem(newUnit)
		self.iniUnits[side].append(newUnit)
		#self.scene().update()
		Ui_MapEditor.DATA_DIRTY = True
		return newSoldier
	def DelUnit(self, side):
		"DelUnit(enum(0, 1) side) -> Coord. pos \
		delete the last unit of a certain side returning the position it was placed at. \
		error will be raised if no units is in this side."
		if (self.iniUnits[side]):
			delItem = self.iniUnits[side].pop(-1)
			self.RemoveItem(delItem)
			#self.scene().update()
			Ui_MapEditor.DATA_DIRTY = True
			return UiD_BaseUnit(delItem.type, (delItem.mapX, delItem.mapY))
		else:
			raise Ui_Error, ("DelUnitError",
							 ("class Ui_MapEditor", "func DelUnit"),
							 "无可删除的单位。")

	def EditMapMode(self):
		"EditMapMode() -> void \
		set the widget in the map-editing mode."
		for column in self.mapItem:
			for item in column:
				item.SetEnabled(True)
		for side in (0, 1):
			for unit in self.iniUnits[side]:
				unit.SetEnabled(False)
	def EditUnitMode(self):
		"EditUnitMode() -> void \
		set the widget in the unit-placing mode."
		for column in self.mapItem:
			for item in column:
				item.SetEnabled(False)
				item.setVisible(True)
		for side in (0, 1):
			for unit in self.iniUnits[side]:
				unit.SetEnabled(True)
	#function to change the mode

	#need a clear function to clear the selected state?
	DATA_DIRTY = False

