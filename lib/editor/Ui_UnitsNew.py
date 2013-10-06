# -*- coding: utf-8 -*-
#Ver 0.5 edited at 2013-09-29-21:35
#new version

#items needed in replay scene
#grids of map
#soldiers
#cursor

from PyQt4 import QtGui, QtCore
from basic import *
from shortest import *
import copy



TRAP_TRIGGERED = 8

TEMP_SOLDIER = 100
TEMP_HERO = 101

AVAILABLE_TERRAIN = (PLAIN, MOUNTAIN, FOREST, BARRIER, TURRET, TEMPLE, MIRROR)
MAP_BASE = (Map_Basic, Map_Basic, Map_Basic, Map_Basic, Map_Turret, Map_Temple, Map_Mirror)

AVAILABLE_UNIT_TYPE = (SABER, LANCER, ARCHER, DRAGON_RIDER, WARRIOR, WIZARD,
                       HERO_1, HERO_2, HERO_3)
AVAILABLE_HERO_TYPE = (HERO_1, HERO_2, HERO_3)

#types of map grid, unit defined by ui


UNIT_WIDTH = 60
UNIT_HEIGHT = 60
PEN_WIDTH = 0.5


LABEL_WIDTH = 40
LABEL_HEIGHT = 20
MARGIN_WIDTH = 30
LABEL_LEFT_MARGIN = 30
DRAG_SPOT = QtCore.QPoint(20, 20)

def GetPos(mapX, mapY):
    return QtCore.QPointF(mapX*UNIT_WIDTH, mapY*UNIT_HEIGHT)
def GetGrid(corX, corY):
    x = int(corX/UNIT_WIDTH)
    y = int(corY/UNIT_HEIGHT)
    return x, y

#################################################################

class Ui_GridUnit(QtGui.QGraphicsObject):
    "the superclass of all grid units"
    def __init__(self, x = 0, y = 0, parent = None):
        QtGui.QGraphicsObject.__init__(self, parent)
        self.mapX = x
        self.mapY = y
        self.selected = False
        self.setPos(self.GetPos())

    def SetMapPos(self, x, y):
        self.mapX = x
        self.mapY = y
        self.setPos(self.GetPos())
    def GetPos(self):
        return GetPos(self.mapX, self.mapY)

    def SetEnabled(self, flag):
        if (flag):
            self.setVisible(True)
            self.setEnabled(True)
        else:
            self.setEnabled(False)
            self.setVisible(False)
    def IsEnabled(self):
        return (self.isVisible() and self.isEnabled())

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    def paint(self, painter, option, widget):
        pass#

    def MousePressEvent(self, args):
        return False
    def MouseEnterEvent(self, args):
        return False
    def MouseLeaveEvent(self, args):
        return False
    def DragStartEvent(self, args):
        return False
    def DragStopEvent(self, args):
        return False
    def DragComplete(self, args):
        pass
    def DragFail(self, args):
        self.setPos(self.GetPos())
    #my event

    enability = QtCore.pyqtProperty(bool, fget = IsEnabled,
                                    fset = SetEnabled)




class Ui_MapUnit(Ui_GridUnit):
    "the unit of the map."
    def __init__(self, x, y, mapGrid, parent = None):
        Ui_GridUnit.__init__(self, x, y, parent)
        self.terrain = mapGrid.kind
        self.relatedLabel = []#label items of scene connecting
        #load pixmap
        #self.coverColor = None
        
    def DragStopEvent(self, args):
        return True
    #my event

    mapGridSelected = QtCore.pyqtSignal(int, int)


class Ui_SoldierUnit(Ui_GridUnit):
    "the unit of the soldiers."
    def __init__(self, idNum, side, unit, parent = None):
        Ui_GridUnit.__init__(self, unit.position[0], unit.position[1], parent)
        self.type = unit.kind
        self.idNum = idNum
        self.side = side

    def boundingRect(self):
        return QtCore.QRectF(0-PEN_WIDTH, 0-PEN_WIDTH,
                             UNIT_WIDTH+PEN_WIDTH, UNIT_HEIGHT+PEN_WIDTH)
        #regard the upleft corner as origin

    soldierSelected = QtCore.pyqtSignal(int)#no need


class Ui_GridLabel(Ui_GridUnit):
    "used to show info on map grids"
    def __init__(self, text, mapX, mapY, parent = None):
        Ui_GridUnit.__init__(self, mapX, mapY, parent)
        self.text = text

    def boundingRect(self):
        return QtCore.QRectF(LABEL_LEFT_MARGIN-PEN_WIDTH, 0-LABEL_HEIGHT-PEN_WIDTH,
                             LABEL_WIDTH+PEN_WIDTH, LABEL_HEIGHT+PEN_WIDTH)
        #regard the downleft corner as origin

    def paint(self, painter, option, widget):
        font = QtGui.QFont("Times New Roman", 20)
        #font.setColor(QtGui.QColor(0, 0, 0))
        painter.setFont(font)
        #painter.setColor(QtGui.QColor(0, 0, 0))
        painter.drawText(QtCore.QPointF(LABEL_LEFT_MARGIN, 0), self.text)


        



class Ui_GridCursor(Ui_GridUnit):
    def __init__(self, x = 0, y = 0):
        Ui_GridUnit.__init__(self, x, y)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RLINE*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF(RLINE*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RLINE)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RLINE)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
    

class Ui_MouseCursor(Ui_GridCursor):
    "the cursor moving along with mouse"
    def __init__(self):
        Ui_GridCursor.__init__(self)

        #self.isFixed = False #show whether the cursor should stop frickering
        self.timerId = self.startTimer(500)#frickering period
    def timerEvent(self, event):
        if (event.timerId()==self.timerId):
            self.setOpacity(1-self.opacity()) #make the cursor fricker
    #timer
    def MouseLeaveEvent(self, info):
        if (info.isValid and self.isEnabled()):
            x, y = info.nowPos
            self.SetMapPos(x, y)
        return False
    #my event
    #mouse cursor


class Ui_TargetCursor(Ui_GridUnit):
    "the cursor used to point out the target"
    def __init__(self, x = 0, y = 0):
        Ui_GridUnit.__init__(self, x, y)

    def paint(self, painter, option, widget):
        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        painter.setPen(pen)

        RMARGIN = 0.05 #rate of margin
        RLINE = 0.4 #rate of line
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF(RMARGIN*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))
        painter.drawLine(QtCore.QPointF((1-RMARGIN)*UNIT_WIDTH, RMARGIN*UNIT_HEIGHT),
                         QtCore.QPointF(RMARGIN*UNIT_WIDTH, (1-RMARGIN)*UNIT_HEIGHT))

#class Ui_KeyboardCursor(Ui_GridUnit):


#animation
class Ui_Animation(QtCore.QPropertyAnimation):
    def __init__(self, widget = None, prop = ""):
        QtCore.QPropertyAnimation.__init__(self, widget, prop)

    def interpolated(self, start, end, progress):
        if (start.type()==QtCore.QVariant.Bool
            and end.type()==QtCore.QVariant.Bool):
            return start
        #customed interpolator
        else:
            return QtCore.QPropertyAnimation.interpolated(self, start, end, progress)


###########################################
        
#data of game
def ConvertTo1D(iniUnits):
    units = {}
    for i in (0, 1):
        for j in range(len(iniUnits[i])):
            units[(i, j)] = iniUnits[i][j]
    return units
def ConvertBackTo2D(units):
    iniUnits = [[], []]
    for idNum in units.keys():
        i, j = idNum
        while (len(iniUnits[i])<=j):
            iniUnits[i].append(None)
        iniUnits[i][j] = units[idNum]
    return iniUnits

class UiD_BeginChanges:
    def __init__(self, beginInfo):
        self.templeRenew = None#

class UiD_EndChanges:
    def __init__(self, begInfo, cmd, endInfo, maps):
        self.idNum = idNum = begInfo.id
        self.route = endInfo.route
        self.order = cmd.order
        if (cmd.order==1):
            self.target = target = cmd.target
            begUnits = ConvertTo1D(begInfo.base)
            endUnits = ConvertTo1D(endInfo.base)
            self.damage = (endUnits[idNum].life-begUnits[idNum].life,
                           endUnits[target].life-begUnits[target].life) #(self, enemy)
            self.note = ["", ""]
            for i in (0, 1):
                if (self.damage[i]==0):
                    if (endInfo.effect[i]==1):
                        self.note[i] = "Blocked!"
                    elif (endInfo.effect[i]==0):
                        self.note[i] = "Miss"
            self.fightBack = (endInfo.effect[1]!=-1) and (endUnits[target].life!=0)
            self.isDead = (endUnits[idNum].life==0, endUnits[target].life==0)
        elif (cmd.order==2):
            raise NotImplementedError#skill

class UiD_RoundInfo:
    "info of every round"
    def __init__(self, begInfo, cmd, endInfo, maps):
        self.begChanges = UiD_BeginChanges(begInfo)
        self.idNum = begInfo.id
        if (endInfo==None and cmd==None):
            self.begUnits = ConvertTo1D(begInfo.base)
            self.endUnits = None
            self.cmdChanges = None
            self.score = None
            self.isCompleted = False
        else:
            self.cmdChanges = UiD_EndChanges(begInfo, cmd, endInfo, maps)
            self.begUnits = None #if it is none, there's no changes in the unit info
            self.endUnits = ConvertTo1D(endInfo.base)
            self.score = endInfo.score
            self.isCompleted = True

class UiD_BattleData:
    "info of the entire battle(not completed)"
    def __init__(self, iniInfo, begInfo):
        self.map = iniInfo.map
        self.side0SoldierNum = len(iniInfo.base[0])
        self.iniUnits = ConvertTo1D(iniInfo.base)
        self.roundInfo = []
        self.nextRoundInfo = None
        self.UpdateBeginData(begInfo)
        self.result = None #result, not complete

    def GetUnitArray(self, roundNum, isEnd):
        if (isEnd):
            units = self.roundInfo[roundNum].endUnits
        else:
            units = self.roundInfo[roundNum].begUnits
            if (units==None):
                if (roundNum>0):
                    units = self.roundInfo[roundNum-1].endUnits
                else:
                    units = self.iniUnits
        return units

    def UpdateBeginData(self, begInfo):
#        assert(not self.roundInfo or self.roundInfo[-1].isCompleted,
#               "error in update")
        self.nextRoundInfo = begInfo
        self.roundInfo.append(UiD_RoundInfo(begInfo, None, None, self.map))
    def UpdateEndData(self, cmd, endInfo):
#        assert(not self.roundInfo[-1].isCompleted, "error in update")
        rInfo = UiD_RoundInfo(self.nextRoundInfo, cmd, endInfo, self.map)
        self.roundInfo[-1] = rInfo
        self.nextRoundInfo = None

class UiD_BaseUnit:
    #substitution of Base_Unit, only used for displaying
    def __init__(self, kind, pos = (0, 0)):
        self.soldier = None
        if (kind in AVAILABLE_UNIT_TYPE):
            if (kind in AVAILABLE_HERO_TYPE):
                self.soldier = Hero(kind, pos)
                self.baseClass = Hero
            else:
                self.soldier = Base_Unit(kind, pos)
                self.baseClass = Base_Unit
        else:
            self.kind = kind
            self.position = pos

    def __getattr__(self, name):
        try:
            if (name in self.soldier.__dict__.keys()):
                value = self.soldier.__dict__[name]
            else:
                value = self.baseClass.__dict__[name]
        except KeyError:
            raise AttributeError, name
        except AttributeError:
            raise AttributeError, name
        if (callable(value)):
            return METHODWRAPPER(value, self.soldier)
        return value

class METHODWRAPPER:
    def __init__(self, func, inst):
        self.function = func
        self.instance = inst
        self.__name__ = self.function.__name__
    def __call__(self, *args):
        return apply(self.function, (self.instance,)+args)
        


