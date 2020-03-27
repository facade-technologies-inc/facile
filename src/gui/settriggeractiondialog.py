"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This module contains the code for the "Set Trigger Action" dialog.
"""
import sys
import os
import data.statemachine as sm

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem
from gui.ui.ui_settriggeractiondialog import Ui_Dialog as Ui_SetTriggerActionDialog

from data.tguim.visibilitybehavior import VisibilityBehavior
from data.apim.componentaction import ComponentAction


class SetTriggerActionDialog(QDialog):
    """
    This class is a dialog that allows the user to set the trigger action for a visibility behavior.
    """


    def __init__(self, vb: VisibilityBehavior):
        """
        Constructs a SetTriggerActionDialog object

        :param vb: The visibility behavior to set the trigger action for.
        :type vb: VisibilityBehavior
        :return: The constructed new Api Compiler dialog object.
        :rtype: ApiCompilerDialog
        """

        super(SetTriggerActionDialog, self).__init__(None)
        self.ui = Ui_SetTriggerActionDialog()
        self.ui.setupUi(self)

        self._vb = vb
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        self._curAction = vb.getTriggerAction()

        try:
            name = self._curAction.getName()
        except:
            name = "None"
        finally:
            self.ui.triggerActionLabel.setText(name)

        # Get all actions for src component
        src = vb.getSrcComponent()
        cType = src.getProperties().getProperty('Class Name')[1].getValue()
        specs = sm.StateMachine.instance._project.getAPIModel().getSpecifications(cType)
        self._itemActionMapping = {}
        for spec in specs:
            action = ComponentAction(src, spec)
            item = QListWidgetItem(action.getName())
            self._itemActionMapping[item.text()] = action
            self.ui.actionListWidget.addItem(item)

        def onItemSelected(item: QListWidgetItem):
            text = item.text()
            self._curAction = self._itemActionMapping[text]
            self.ui.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)
            self.ui.triggerActionLabel.setText(self._curAction.getName())

        self.ui.actionListWidget.itemClicked.connect(onItemSelected)

    def accept(self):
        """
        When the dialog is accepted, save the trigger action and close the dialog
        """

        self._vb.setTriggerAction(self._curAction)

        try:
            sm.StateMachine.instance.view.onItemSelected(self._vb.getId())
        except:
            pass

        return QDialog.accept(self)