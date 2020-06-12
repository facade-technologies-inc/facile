from PySide2.QtCore import Qt, QMetaObject, Signal, Slot, QSize, QRect, QPoint
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QMenu,
                            QLabel, QSizePolicy, QDialog, QApplication, QGraphicsDropShadowEffect)
from ._utils import PLATFORM, resource_path
import pyautogui


_FL_STYLESHEET = resource_path('resources/frameless.qss')
""" str: Frameless window stylesheet. """


class WindowDragger(QWidget):

    doubleClicked = Signal()

    def __init__(self, window: QWidget, parent=None):
        """
        This is the frame/titlebar.

        :param window: The contained window
        :type window:
        """
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            if event.globalPos().y() < 5 and not self._window.maximized:  # Within the top part of the screen
                self._window.move(0, 0)
                self._window.showMaximized()
            elif event.globalPos().y() > 5:  # Any other part of screen
                if self._window.maximized:  # Coming from top part of screen
                    self._window.showNormal()
                    newX = event.globalPos().x() - \
                           self._window.size().width() * (event.globalPos().x() / self._window.screenSize.width())
                    self._window.move(newX, event.globalPos().y())
                    self._windowPos = QPoint(newX, event.globalPos().y()-8)
                    self._mousePos = event.globalPos()
                else:  # anywhere else
                    self._window.move(self._windowPos + (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False
        self.fromMaxed = None

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QDialog):
    """
    Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    # MODAL_WINDOWS = []
    # INST = False

    def __init__(self, w, parent=None, modal=True):
        # Since all parent windows will also have these wrappers, the parent is actually the modernwindow
        QDialog.__init__(self, parent)

        # w.wrapper = self
        self._w = w
        self.setupUi()

        # -1 so that task bar can be shown on Windows
        self.screenSize = QSize(pyautogui.size().width, pyautogui.size().height - 1)
        self.usualSize = self.size()
        self.maximized = False
        self._movedToCenter = 0
        self.showNormal()

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        # w.windowTitleChanged.connect(lambda title: self.setWindowTitle(title))

        rect = w.geometry()
        rect.setHeight(rect.height() + self.titleBar.size().height())
        self.setGeometry(rect)

        # Adding attribute to clean up the parent window when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self.__child_was_closed)

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        self.setGraphicsEffect(effect)

        self.modal = modal
        if modal:
            # Modality doesn't usually work, this fixes it, kind of.
            # Kind of an overkill bc it stays over other windows too, but otherwise doesn't work.
            self.setWindowModality(Qt.ApplicationModal)
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            # ModernWindow.MODAL_WINDOWS.append(self)

            # if not ModernWindow.INST:  # Trying to get normal modal behavior
            #     def modalityHandler(x, y):
            #         wins = [win for win in QApplication.topLevelWidgets() if isinstance(win, ModernWindow)]
            #         if x is None and y is not None:
            #             if y.window() in ModernWindow.MODAL_WINDOWS:
            #                 y.window().setWindowFlag(Qt.WindowStaysOnTopHint)
            #         elif y is None and x is not None:
            #             if x.window() in ModernWindow.MODAL_WINDOWS:
            #                 x.window().setWindowFlag(Qt.WindowStaysOnTopHint, False)
            #             for win in wins:
            #                 win.show()
            #
            #     QApplication.instance().focusChanged.connect(lambda x, y: modalityHandler(x, y))
            #     ModernWindow.INST = True

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setObjectName('vboxWindow')
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Fixed))

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignCenter)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)

        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)

        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)

        if PLATFORM == "Darwin":
            self.hboxTitle.addWidget(self.btnClose)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.lblTitle)
        else:
            self.hboxTitle.addWidget(self.lblTitle)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.btnClose)

        # set window flags
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET) as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None  # The child was deleted, remove the reference to it and close the parent window
        self.close()

    def closeEvent(self, event):
        # if self.modal:
        #     ModernWindow.MODAL_WINDOWS.remove(self)

        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        QDialog.setWindowTitle(self, "                " + title)
        self.lblTitle.setText("                " + title)

    def _setWindowButtonState(self, hint, state):
        btns = {
            Qt.WindowCloseButtonHint: self.btnClose,
            Qt.WindowMinimizeButtonHint: self.btnMinimize,
            Qt.WindowMaximizeButtonHint: self.btnMaximize
        }
        button = btns.get(hint)

        maximized = bool(self.windowState() & Qt.WindowMaximized)

        if button == self.btnMaximize:  # special rules for max/restore
            self.btnRestore.setEnabled(state)
            self.btnMaximize.setEnabled(state)

            if maximized:
                self.btnRestore.setVisible(state)
                self.btnMaximize.setVisible(False)
            else:
                self.btnMaximize.setVisible(state)
                self.btnRestore.setVisible(False)
        else:
            button.setEnabled(state)

        allButtons = [self.btnClose, self.btnMinimize, self.btnMaximize, self.btnRestore]
        if True in [b.isEnabled() for b in allButtons]:
            for b in allButtons:
                b.setVisible(True)
            if maximized:
                self.btnMaximize.setVisible(False)
            else:
                self.btnRestore.setVisible(False)
            self.lblTitle.setContentsMargins(0, 0, 0, 0)
        else:
            for b in allButtons:
                b.setVisible(False)
            self.lblTitle.setContentsMargins(0, 2, 0, 0)

    def setWindowFlag(self, Qt_WindowType, on=True):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]

        if Qt_WindowType in buttonHints:
            self._setWindowButtonState(Qt_WindowType, on)
        else:
            QWidget.setWindowFlag(self, Qt_WindowType, on)

    def setWindowFlags(self, Qt_WindowFlags):
        buttonHints = [Qt.WindowCloseButtonHint, Qt.WindowMinimizeButtonHint, Qt.WindowMaximizeButtonHint]
        for hint in buttonHints:
            self._setWindowButtonState(hint, bool(Qt_WindowFlags & hint))

        QWidget.setWindowFlags(self, Qt_WindowFlags)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.showMinimized()

    @Slot()
    def on_btnMaximize_clicked(self):
        if self.maximized:
            self.showNormal()
        else:
            self.showMaximized()

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        self.on_btnMaximize_clicked()

    def showMaximized(self):
        """
        Overrides showMaximized to give normal functionality (not usually normal since this is a widget)
        """
        self.usualSize = self.size()
        self.setWindowState(Qt.WindowMaximized)
        self.move(0, 0)
        self.setFixedSize(QSize(self.screenSize.width(), self.screenSize.height()))
        self.maximized = True
        QWidget.showMaximized(self)

    def showNormal(self):
        self.setWindowState(Qt.WindowNoState)
        self.setMinimumSize(100, 50)
        self.resize(self.usualSize)
        self.maximized = False
        QWidget.showNormal(self)

    def exec_(self) -> int:
        """
        Overloads the original exec function to give expected behavior with custom title bar.
        Returns button clicked if dialog.
        :return: integer bit value of button clicked
        :rtype: int
        """
        self._w.finished.connect(lambda state: self.done(state))
        return QDialog.exec_(self)

    def resizeEvent(self, event: 'QResizeEvent'):
        """
        Catches when self is resized, and makes sure

        :param event: The resize event, storing the new size
        :type event: QResizeEvent
        """
        newSize = event.size()
        # self.setMask(QRegion(self.rect()))

        if self._movedToCenter < 3:  # 2 size adjustments are done before self reaches its final assigned size.
            self.move(self.screenSize.width() / 2 - newSize.width() / 2,
                      self.screenSize.height() / 2 - newSize.height() / 2)
            self._movedToCenter += 1
