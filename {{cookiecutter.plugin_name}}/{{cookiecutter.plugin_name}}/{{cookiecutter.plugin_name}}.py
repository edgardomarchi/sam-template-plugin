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
import os
from pathlib import Path

try:
    with open(os.path.join(os.path.dirname(__file__),
                           '{{cookiecutter.plugin_name}}.json'), 'r') as plFile:
        defaultParameters = json.load(plFile)
except json.JSONDecodeError as e:
    defaultParameters = {}
    logger.warning('No valid json format! - Exception: {0!s}'.format(e))
except IOError:
    defaultParameters = {}
    logger.exception('No plugin data structure found!')


################################################################################
# Class definiton
################################################################################
class {{cookiecutter.plugin_name}}(BasePlugin):
    """ TODO: place class comments here
    """

    def __init__(self, 
                 parent=None,
                 parameters=None,
                 gui_mode=False):
        super().__init__(parent, parameters, gui_mode)

        if not self._parameters:
            self._parameters = defaultParameters

  
    def cleanUp(self):
        '''TODO: Place comments about cleanUp tasks on plugin destroy here.
        '''
        super().cleanUp()
        # TODO: Add your cleanUp code here

    def fromJson(self, parameters: dict):
        ''' TODO: Place comments about loading data here.
        '''
        super().fromJson
        # TODO: Add your code here

    @_producesChange
    def someTask(self):
        # Example method that changes the plugin state.
        pass
 
