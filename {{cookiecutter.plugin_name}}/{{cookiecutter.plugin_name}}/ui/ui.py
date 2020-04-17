import logging
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget
from . import ui_rfid

from commonutils.frequency import getCompactFreqUnits, getFloatFreqFromUnits, getStrFreqUnits
from commonutils.formatters import veredictFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



"""
Widget principal del plugin {{cookiecutter.plugin_name}}

:author: {{cookiecutter.full_name}} <{{cookiecutter.email}}>

---
"""

class Ui(QWidget, ui_{{cookiecutter.plugin_name}}.Ui_{{cookiecutter.plugin_name}}):
    """Widget del plugin {{cookiecutter.plugin_name}}

    Aquí se realizan todas las customizaciones programáticas de la UI.
    """

    def __init__(self, parent=None, saWidget=None):
        super(Ui, self).__init__(parent)

        # Load UI
        self.setupUi(self)
        if isinstance(saWidget,QWidget):
            self.saGroupBoxVLayout.removeWidget(self.saWidget)
            self.saWidget = saWidget
            self.saGroupBoxVLayout.insertWidget(0, self.saWidget, QtCore.Qt.AlignLeft)
            self.saWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)

        # connections
        # -
    
    def update(self, pluginData: dict):
    """ Actauliza la interfaz en función de los parámetros almacenados del plugin.
    """
        self.measuredValueLineEdit.setText(
            str(pluginData['results']['value']))
        self.parameterSpinBox.setValue(
            float(pluginData['parameters']['value']))  # Signal valueChanged no se emite si es igual