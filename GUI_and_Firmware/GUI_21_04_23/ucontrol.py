#!/usr/bin/python
# -*- coding: utf-8 -*-

#/***************************************************************************
 #*   Copyright (C) 2020 by DTU                             *
 #*   jca@elektro.dtu.dk                                                    *
 #*
 #*   class for control loop settings
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
#import os
import numpy as np
import time
from time import sleep
#import ConfigParser
import timeit
try:
  import configparser
except:
  import ConfigParser  
from ucontrol_edit import UControlUnit
from PyQt5 import QtWidgets, QtCore


class UControl(object):
  # class variables
  parent = []
  ui = []
  main = []

  # methods / functions
  def __init__(self, parent, ui):
    self.parent = parent
    self.ui = ui
    self.main = self.parent.main

  def init(self):
    self.ctrlRollVel = UControlUnit("vroll", self.parent, "Roll rate control")
    self.ctrlRoll = UControlUnit("roll", self.parent, "Roll angle control")
    self.ctrlPitchVel = UControlUnit("vpitch", self.parent, "Pitch rate control")
    self.ctrlPitch = UControlUnit("pitch", self.parent, "Pitch angle control")
    self.ctrlYawVel = UControlUnit("vyaw", self.parent, "Yaw rate control")
    self.ctrlYaw = UControlUnit("yaw", self.parent, "Yaw angle control")
    self.ctrlHeight = UControlUnit("height", self.parent, "Height control")
    # < CROSSCOUPLING
    self.ctrlRoll2Pitch = UControlUnit("r2p", self.parent, "Roll2pitch control")
    self.ctrlRoll2Yaw = UControlUnit("r2y", self.parent, "Roll2yaw control")
    self.ctrlRoll2Height = UControlUnit("r2h", self.parent, "Roll2height control")
    
    self.ctrlPitch2Roll = UControlUnit("p2r", self.parent, "Pitch2roll control")
    self.ctrlPitch2Yaw = UControlUnit("p2y", self.parent, "Pitch2yaw control")
    self.ctrlPitch2Height = UControlUnit("p2h", self.parent, "Pitch2height control")
    
    self.ctrlYaw2Roll = UControlUnit("y2r", self.parent, "Yaw2roll control")
    self.ctrlYaw2Pitch = UControlUnit("y2p", self.parent, "Yaw2pitch control")
    self.ctrlYaw2Height = UControlUnit("y2h", self.parent, "Yaw2height control")
    
    self.ctrlHeight2Roll = UControlUnit("h2r", self.parent, "Height2roll control")
    self.ctrlHeight2Pitch = UControlUnit("h2p", self.parent, "Height2pitch control")
    self.ctrlHeight2Yaw = UControlUnit("h2y", self.parent, "Height2yaw control")
    # >
    self.ctrlRollVel.init()
    self.ctrlRoll.init()
    self.ctrlPitchVel.init()
    self.ctrlPitch.init()
    self.ctrlYawVel.init()
    self.ctrlYaw.init()
    self.ctrlHeight.init()
    # < CROSSCOUPLING
    self.ctrlRoll2Pitch.init()
    self.ctrlRoll2Yaw.init()
    self.ctrlRoll2Height.init()
    
    self.ctrlPitch2Roll.init()
    self.ctrlPitch2Yaw.init()
    self.ctrlPitch2Height.init()
    
    self.ctrlYaw2Roll.init()
    self.ctrlYaw2Pitch.init()
    self.ctrlYaw2Height.init()
    
    self.ctrlHeight2Roll.init()
    self.ctrlHeight2Pitch.init()
    self.ctrlHeight2Yaw.init()
    # >
    self.ui.pushButton_ctrl_roll_vel.clicked.connect(self.ctrlRollVel.editControlValues)
    self.ui.pushButton_ctrl_roll.clicked.connect(self.ctrlRoll.editControlValues)
    self.ui.pushButton_ctrl_pitch_vel.clicked.connect(self.ctrlPitchVel.editControlValues)
    self.ui.pushButton_ctrl_pitch.clicked.connect(self.ctrlPitch.editControlValues)
    self.ui.pushButton_ctrl_yaw_vel.clicked.connect(self.ctrlYawVel.editControlValues)
    self.ui.pushButton_ctrl_yaw.clicked.connect(self.ctrlYaw.editControlValues)
    self.ui.pushButton_ctrl_height.clicked.connect(self.ctrlHeight.editControlValues)
    # < CROSSCOUPLING
    self.ui.pushButton_ctrl_roll_to_pitch.clicked.connect(self.ctrlRoll2Pitch.editControlValues) 
    self.ui.pushButton_ctrl_roll_to_yaw.clicked.connect(self.ctrlRoll2Yaw.editControlValues) 
    self.ui.pushButton_ctrl_roll_to_height.clicked.connect(self.ctrlRoll2Height.editControlValues) 
    
    self.ui.pushButton_ctrl_pitch_to_roll.clicked.connect(self.ctrlPitch2Roll.editControlValues) 
    self.ui.pushButton_ctrl_pitch_to_yaw.clicked.connect(self.ctrlPitch2Yaw.editControlValues) 
    self.ui.pushButton_ctrl_pitch_to_height.clicked.connect(self.ctrlPitch2Height.editControlValues) 
    
    self.ui.pushButton_ctrl_yaw_to_roll.clicked.connect(self.ctrlYaw2Roll.editControlValues) 
    self.ui.pushButton_ctrl_yaw_to_pitch.clicked.connect(self.ctrlYaw2Pitch.editControlValues) 
    self.ui.pushButton_ctrl_yaw_to_height.clicked.connect(self.ctrlYaw2Height.editControlValues) 
    
    self.ui.pushButton_ctrl_height_to_roll.clicked.connect(self.ctrlHeight2Roll.editControlValues) 
    self.ui.pushButton_ctrl_height_to_pitch.clicked.connect(self.ctrlHeight2Pitch.editControlValues) 
    self.ui.pushButton_ctrl_height_to_yaw.clicked.connect(self.ctrlHeight2Yaw.editControlValues) 
    # >
    pass

  def timerUpdate(self, timerCnt):
    self.ctrlRollVel.timerUpdate()
    self.ctrlRoll.timerUpdate()
    self.ctrlPitchVel.timerUpdate()
    self.ctrlPitch.timerUpdate()
    self.ctrlYawVel.timerUpdate()
    self.ctrlYaw.timerUpdate()
    self.ctrlHeight.timerUpdate()
    # < CROSSCOUPLING
    self.ctrlRoll2Pitch.timerUpdate()
    self.ctrlRoll2Yaw.timerUpdate()
    self.ctrlRoll2Height.timerUpdate()
    
    self.ctrlPitch2Roll.timerUpdate()
    self.ctrlPitch2Yaw.timerUpdate()
    self.ctrlPitch2Height.timerUpdate()
    
    self.ctrlYaw2Roll.timerUpdate()
    self.ctrlYaw2Pitch.timerUpdate()
    self.ctrlYaw2Height.timerUpdate()
    
    self.ctrlHeight2Roll.timerUpdate()
    self.ctrlHeight2Pitch.timerUpdate()
    self.ctrlHeight2Yaw.timerUpdate()
    # >
    if timerCnt % 10 == 0:
      pass
    if self.ui.tabWidget.currentIndex() == self.ui.tabWidget.indexOf(self.ui.tab_control):
      # no data in this tab, just buttons
      # self.main.message("control timer update")
      pass
    pass 
  
  
  def decode(self, gg):
    isOK = True
    if gg[0] == "control":
        if self.ctrlRollVel.fromString(gg):
          pass
        elif self.ctrlRoll.fromString(gg):
          pass
        elif self.ctrlPitchVel.fromString(gg):
          pass
        elif self.ctrlPitch.fromString(gg):
          pass
        elif self.ctrlYawVel.fromString(gg):
          pass
        elif self.ctrlYaw.fromString(gg):
          pass
        elif self.ctrlHeight.fromString(gg):
          pass
        # < CROSSCOUPLING
        elif self.ctrlRoll2Pitch.fromString(gg):
          pass
        elif self.ctrlRoll2Yaw.fromString(gg):
          pass
        elif self.ctrlRoll2Height.fromString(gg):
          pass
          
        elif self.ctrlPitch2Roll.fromString(gg):
          pass
        elif self.ctrlPitch2Yaw.fromString(gg):
          pass
        elif self.ctrlPitch2Height.fromString(gg):
          pass
          
        elif self.ctrlYaw2Roll.fromString(gg):
          pass
        elif self.ctrlYaw2Pitch.fromString(gg):
          pass
        elif self.ctrlYaw2Height.fromString(gg):
          pass
          
        elif self.ctrlHeight2Roll.fromString(gg):
          pass
        elif self.ctrlHeight2Pitch.fromString(gg):
          pass
        elif self.ctrlHeight2Yaw.fromString(gg):
          pass
        # >
        else:
          isOK = False
    else:
      isOK = False
    return isOK

  def requestControlData(self):
    self.main.devWrite("ctrl roll\n", True)
    self.main.devWrite("ctrl vroll\n", True)
    self.main.devWrite("ctrl pitch\n", True)
    self.main.devWrite("ctrl vpitch\n", True)
    self.main.devWrite("ctrl yaw\n", True)
    self.main.devWrite("ctrl vyaw\n", True)
    self.main.devWrite("ctrl height\n", True)
    # < CROSSCOUPLING
    self.main.devWrite("ctrl r2p\n", True)
    self.main.devWrite("ctrl r2y\n", True)
    self.main.devWrite("ctrl r2h\n", True)
    
    self.main.devWrite("ctrl p2r\n", True)
    self.main.devWrite("ctrl p2y\n", True)
    self.main.devWrite("ctrl p2h\n", True)
    
    self.main.devWrite("ctrl y2r\n", True)
    self.main.devWrite("ctrl y2p\n", True)
    self.main.devWrite("ctrl y2h\n", True)
    
    self.main.devWrite("ctrl h2r\n", True)
    self.main.devWrite("ctrl h2p\n", True)
    self.main.devWrite("ctrl h2y\n", True)
    # >
    time.sleep(0.1);

  def saveToIniFile(self, config):
    # fetch data from teensy
    self.requestControlData()
    self.ctrlRollVel.configurationFileSave(config)
    self.ctrlRoll.configurationFileSave(config)
    self.ctrlPitchVel.configurationFileSave(config)
    self.ctrlPitch.configurationFileSave(config)
    self.ctrlYawVel.configurationFileSave(config)
    self.ctrlYaw.configurationFileSave(config)
    self.ctrlHeight.configurationFileSave(config)
    # < CROSSCOUPLING
    self.ctrlRoll2Pitch.configurationFileSave(config)
    self.ctrlRoll2Yaw.configurationFileSave(config)
    self.ctrlRoll2Height.configurationFileSave(config)
    
    self.ctrlPitch2Roll.configurationFileSave(config)
    self.ctrlPitch2Yaw.configurationFileSave(config)
    self.ctrlPitch2Height.configurationFileSave(config)
    
    self.ctrlYaw2Roll.configurationFileSave(config)
    self.ctrlYaw2Pitch.configurationFileSave(config)
    self.ctrlYaw2Height.configurationFileSave(config)
    
    self.ctrlHeight2Roll.configurationFileSave(config)
    self.ctrlHeight2Pitch.configurationFileSave(config)
    self.ctrlHeight2Yaw.configurationFileSave(config)
    # >

