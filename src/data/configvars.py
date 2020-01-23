from PySide2.QtCore import Slot, Signal, QObject

class ConfigVars(QObject):

    updateTGUIMView = Signal()

    def __init__(self):
        self.showBehaviors = True
        self.showTokenTags = True

    @Slot(bool)
    def setShowBehaviors(self, isChecked: bool):
        self.showBehaviors = isChecked
        self.updateTGUIMView.emit()

    @Slot(bool)
    def setShowTokenTags(self, isChecked: bool):
        self.showTokenTags = isChecked
        self.updateTGUIMView.emit()
