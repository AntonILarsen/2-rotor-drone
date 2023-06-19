#!/usr/bin/python
# -*- coding: utf-8 -*-

#/***************************************************************************
 #*   Copyright (C) 2020 by DTU                             *
 #*   jca@elektro.dtu.dk                                                    *
 #*
 #*   class for gyro calibration and monitoring
 #*
 #*   This program is free software; you can redistribute it and/or modify  *
 #*   it under the terms of the GNU General Public License as published by  *
 #*   the Free Software Foundation; either version 2 of the License, or     *
 #*   (at your option) any later version.                                   *
 #*                                                                         *
 #*   This program is distributed in the hope that it will be useful,       *
 #*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 #*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 #*   GNU General Public License for more details.                          *
 #*                                                                         *
 #*   You should have received a copy of the GNU General Public License     *
 #*   along with this program; if not, write to the                         *
 #*   Free Software Foundation, Inc.,                                       *
 #*   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 #***************************************************************************/

import sys 
import numpy as np
import time
import pyqtgraph as pg
import timeit
from PyQt5 import QtWidgets, QtCore
#from cameraBridge import readFromBridge
#from poseBridge import poseReadFromBridge
#cameraBridgeFile = open("cameraBridge.txt", "r") #MINE#################################################################### 

class UCamera(object):
  
  # class variables
  parent = []
  ui = []
  main = []
  camera = [0,0,0,0] #x,y,dx,dy
  offs = [0,0,0,0]
  offsNew = True
  data = np.zeros((4,100))
  dataNew = True
  dataIdx = 0
  dataCg = []
  dataPw = []
  hasFocus = False


  # methods / functions
  def __init__(self, parent, ui):
    self.parent = parent
    self.ui = ui
    self.main = self.parent.main

    # plot widget NEW
    self.dataPw = pg.PlotWidget(name='camera',title='Drift') 
    self.dataPw.setLabel('left','drift (m)','')
    self.dataPw.addLegend()
    self.ui.horizontalLayout_camera.addWidget(self.dataPw)
    self.dataCg = [self.dataPw.plot(pen='r',name='x'), self.dataPw.plot(pen='c',name='y')]
    self.dataCg[0].setData(self.data[0])
    self.dataCg[1].setData(self.data[1])
    # plot widget NEW
    self.dataPw = pg.PlotWidget(name='camera',title='Velocity') 
    self.dataPw.setLabel('left','drift (m)','')
    self.dataPw.addLegend()
    self.ui.horizontalLayout_camera.addWidget(self.dataPw)
    self.dataCg2 = [self.dataPw.plot(pen='r',name='x'), self.dataPw.plot(pen='c',name='y')]
    self.dataCg2[0].setData(self.data[2])
    self.dataCg2[1].setData(self.data[3])

  def init(self):
    self.ui.pushButton_camera_clear.clicked.connect(self.sendClearOffset)
    #self.ui.pushButton_gyro_calibrate.clicked.connect(self.startCalibrate)
    pass

  def timerUpdate(self, timerCnt):
    if self.offsNew:#don't use
      #self.ui.doubleSpinBox_gyro_roll_offset.setValue(self.offs[0])
      #self.ui.doubleSpinBox_gyro_pitch_offset.setValue(self.offs[1])
      self.offsNew = False
    if self.dataNew:
      self.ui.doubleSpinBox_camera_drift_x.setValue(self.camera[0]) #CHANGE self.gyro[0]
      self.ui.doubleSpinBox_camera_drift_y.setValue(self.camera[1]) #CHANGE self.gyro[1]
      self.ui.doubleSpinBox_camera_dx.setValue(self.camera[2])      #CHANGE self.gyro[0]
      self.ui.doubleSpinBox_camera_dy.setValue(self.camera[3])      #CHANGE self.gyro[1]
      self.dataCg[0].setData(self.data[0])
      self.dataCg[1].setData(self.data[1])
      self.dataCg2[0].setData(self.data[2])
      self.dataCg2[1].setData(self.data[3])
      self.dataNew = False
    if not self.main.isConnected():
      # act as leaving the page
      self.hasFocus = False
    thisTab = self.ui.tabWidget.indexOf(self.ui.tab_camera)
    if self.hasFocus and self.ui.tabWidget.currentIndex() != thisTab:
      # just leaving this tab - stop data flow to this tab
      self.hasFocus = False
      if self.main.wifi.isOpen():
        # we are talking to a bridge - so subscribe off
        self.main.devWrite("camera subscribe 0\n") # data
        self.main.devWrite("camerac subscribe 0\n") # data
      else: # using USB
        self.main.devWrite("sub camera 0\n") # data
        self.main.devWrite("sub camerac 0\n") # data
      pass
    if not self.hasFocus and self.ui.tabWidget.currentIndex() == thisTab:
      # just entering this tab
      self.hasFocus = True
      if self.main.wifi.isOpen():
        # we are talking to a bridge - so subscribe
        self.main.devWrite("camera subscribe 30\n") # data
        self.main.devWrite("camerac subscribe 300\n") # data
      else:
        self.main.devWrite("sub camera 30\n") # data
        self.main.devWrite("sub camerac 300\n") # data
        
    if self.hasFocus:
      #if timerCnt % 3 == 2:
        #self.main.devWrite("imu g\n", True) # imu actual data
      if timerCnt % 30 == 1:
        self.main.devWrite("imucal g\n", True) # imu calibration offsets
    pass 
  
  def sendClearOffset(self):
    self.main.devWrite("imuzero g\n", True)

  def startCalibrate(self):
    self.main.devWrite("offsetcal g\n", True)
    print("# send offsetcal g")
  
  def decode(self, gg):
    isOK = True
    if True:
      #camBridge=readFromBridge()
      #camBridge=poseReadFromBridge(cameraBridgeFile)
      self.camera[0] = float(camBridge[0])
      self.camera[1] = float(camBridge[1])
      self.camera[2] = float(camBridge[2])
      self.camera[3] = float(camBridge[3])
      self.data[0,self.dataIdx] = self.camera[0]
      self.data[1,self.dataIdx] = self.camera[1]
      self.data[2,self.dataIdx] = self.camera[2]
      self.data[3,self.dataIdx] = self.camera[3]
      self.dataIdx += 1
      self.dataNew = True
      if self.dataIdx >= 100:
        self.dataIdx = 0
    elif gg[0] == "camerac":
      self.offs[0] = float(gg[1])
      self.offs[1] = float(gg[2])
      self.offsNew = True
      pass
    else:
      isOK = False
    return isOK



