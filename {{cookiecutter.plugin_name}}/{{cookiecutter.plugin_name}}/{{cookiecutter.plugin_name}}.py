#!/usr/bin/python3

# Logging facilities:
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Plugins:
from plugins.basePlugin import BasePlugin
# Qt:
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot

# Others:
import json
import os
from pathlib import Path

try:
    with open(os.path.join(os.path.dirname(__file__),
                           '{{cookiecutter.plugin_name}}.json'), 'r') as plFile:
        defaultParameters = json.load(plFile)
except json.JSONDecodeError as e:
    pluginDefaultData = {}
    logger.warning('No valid json format! - Exception: {0!s}'.format(e))
except IOError:
    pluginDefaultData = {}
    logger.exception('No plugin data structure found!')


################################################################################
# Class definiton
################################################################################
class {{cookiecutter.plugin_name}}(BasePlugin):
    """ TODO: place class comments here
    """

    def __init__(self, 
                 parent=None,
                 pluginData=None,
                 gui_mode=False):
        super().__init__(parent, pluginData, gui_mode)

        if not self._pluginData:
            self._pluginData = pluginDefaultData
        
        # GUI (if required)
        if self._gui_mode:
            self._widget = QtWidgets.QWidget()
            self.ui = uic.loadUi(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'ui', '{{cookiecutter.plugin_name}}.ui'),
                baseinstance=self._widget)
            self.ui.valueSpinBox.valueChanged.connect(self.setValue)
            self.ui.pushMeButton.clicked.connect(self.printValue)

  
    def cleanUp(self):
        '''TODO: Place comments about cleanUp tasks on plugin destroy here.
        '''
        super().cleanUp()
        # TODO: Add your cleanUp code here

    def fromJson(self, pluginData: dict):
        ''' TODO: Place comments about loading data here.
        '''
        super().fromJson(pluginData)
        # TODO: Add your code here

    @BasePlugin._producesChange
    def someTask(self):
        # Example method that changes the plugin state.
        pass
 
    @BasePlugin._producesChange
    def setValue(self, value=0):
        self._pluginData['parameters']['value']=value

    def printValue(self):
        self.ui.printLabel.setText('Measured value: {0!s}'.format(
            self._pluginData['parameters']['value']))
