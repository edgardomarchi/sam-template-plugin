#!/usr/bin/python3

# Logging facilities:
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Plugins:
from plugins.basePlugin import BasePlugin
from plugins import _producesChange

# Qt:
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import pyqtSlot

# Others (built-in):
import copy
import json
from enum import IntEnum
import os
from pathlib import Path

from .ui.ui import Ui

# Intrumentos a utilizar (Ej: Analizador de espectro)
from instruments.spectrum_analyzer.safrontend import SAFrontend
from instruments import satrace

#### Read plugin default data file:
try:
    with open(os.path.join(os.path.dirname(__file__),
                           '{{cookiecutter.plugin_name}}.json'), 'r') as plFile:
        pluginDefaultData = json.load(plFile)
except json.JSONDecodeError as e:
    pluginDefaultData = {}
    logger.warning('No valid json format! - Exception: {0!s}'.format(e))
except IOError:
    pluginDefaultData = {}
    logger.exception('No plugin data structure found!')


class Status(IntEnum):
    ''' Estado del plugin.
    '''
    CREADO = 0              # El plugin ha sido creado. Valor por default
    EQUIPO_CONFIGURADO = 1  # Se configuró el equipo, es posible abrir OT
    ENSAYO_CONFIGURADO = 2  # Se cargaron los parámetros necesarios para empezar a medir
    ENSAYO_FINALIZADO = 3   # Ensayo completamente finalizado
    ENSAYO_PAUSADO = 4      # Ensayo empezado pero no concluido


################################################################################
# Class definiton
################################################################################
class {{cookiecutter.plugin_name}}(BasePlugin):
    """ TODO: place class comments here
    """

    def __init__(self, 
                 parent=None,
                 path='.',
                 pluginData={},
                 gui_mode=False):
        super().__init__(parent=parent, path=path, pluginData=pluginData, gui_mode=gui_mode)
  
        self._saFrontend = SAFrontend(gui_mode=gui_mode, parent=self)
        # GUI (if required)
        if self._gui_mode:
            self.ui = Ui(saWidget=self._saFrontend.widget())
            self._widget = self.ui      # Para compatibilidad
            self.ui.parameterSpinBox.valueChanged.connect(self.setValue)
            self.ui.runPushButton.clicked.connect(self.acquireData)

	    # Parámetros
        if not self._pluginData:
            self.fromJsonDict(pluginDefaultData)
        else:
            self.fromJsonDict(self._pluginData)
  
    def cleanUp(self):
        '''TODO: Place comments about cleanUp tasks on plugin destroy here.
        '''
        super().cleanUp()
        # TODO: Add your cleanUp code here

    def fromJsonDict(self, pluginData: dict):
        ''' Carga los parámetros y datos recibidos

        Parameters
        ----------
        pluginData: dict
            Diccionario que contiene los datos del plugin.
        '''
        if pluginData:
            self._pluginData = copy.deepcopy(pluginData)
            if self._pluginData['results']['trace'] != {}:
                self._trace = satrace.SATrace.fromLongJSON(
                    self._pluginData['results']['trace'], savespath=self._path)
            else:
                self._trace = None
            if self._gui_mode:
                self.ui.update(self._pluginData)
                if self._trace:
                    self.doMeasure() # Si hay trazo guardado se lo grafica.
        else:
            logger.info('Se recibió un diccionario vacío')
        
    def toJsonDict(self):
        ''' Devuelve un diccionario Json'able' con los datos del plugin
        '''
        if self._trace:
            self._trace.savespath = self._path
            self._pluginData['results']['trace'] = self._trace.toLongJSON()
        return super().toJsonDict()

    def getStatus(self):
        return Status(super().status)
    
   @_producesChange
    def acquireData(self, *args, **kwargs):
        '''Lee datos nuevos del analizador de espectro.
        '''
	    # Medición real del Analizador de espectro:
        #sa = self._saFrontend.controller().getInstrument()
        #sa._visa_handle.timeout = 10e3
        #self._trace = sa.getSATrace()
        #self._trace.savespath = self._path

        #TODO: Remover el código de abajo y reemplazar por un mock adecuado
        self._trace = satrace.SATrace.fromFile(Path(__file__).parent/'testtrace.csv') 
        self.doMeasure()
    
    @_producesChange
    def doMeasure(self):
        '''Ejecuta la medición con los parámetros y el trazo disponibles.
        '''
        if not self._trace:
            logger.warning('Se está intentando procesar un trazo, pero el trazo todavía no fue adquirido.')
        else:
            value = self._trace.y.data.max()
            self._pluginData['results']['value'] = value
            if (self._gui_mode):
                fig, ax = self.ui.mplWidget.canvas.fig, self.ui.mplWidget.canvas.ax
                ax.clear()
                self._trace.N9030Aplot(fig, ax)
                fig.canvas.draw()
                self.ui.update(self._pluginData)
 
    @_producesChange
    def setValue(self, value=0):
        self._pluginData['parameters']['value']=value
	    if self._gui_mode: self.ui.update(self._pluginData)

    def getValue(self):
        return self._pluginData['parameters']['value']

    def getResult(self):
        return self._pluginData['results']['value']


