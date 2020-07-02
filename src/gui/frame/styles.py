from PySide2.QtGui import QPalette, QColor, Qt
from PySide2.QtWidgets import QGraphicsRectItem
from ._utils import resource_path

_STYLESHEET = resource_path('resources/style.qss')
""" str: Main stylesheet. """


def _apply_base_theme(app, withStyleSheet: bool = True):
    """
    Apply theme to the application.

    :param app: QApplication instance
    :type app: QApplication
    :param withStyleSheet: whether or not to apply qtmodern's stylesheet
    :type withStyleSheet: bool
    """

    app.setStyle('Fusion')

    if withStyleSheet:
        with open(_STYLESHEET) as stylesheet:
            app.setStyleSheet(stylesheet.read())
    else:
        app.setStyleSheet("""
QScrollArea > QWidget > QWidget {
  background-color: palette(alternate-base);
}

#v_scrollArea > QWidget > QWidget {
  background-color: palette(base);
}""")


def darkModern(app, view):
    """
    Apply a modern dark-colored theme to Facile. This palette is from qtmodern.

    :param app: QApplication instance
    :type app: QApplication
    :param view: the main view of Facile
    :type view: QMainWindow
    """

    darkPalette = QPalette()

    # base
    darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.Light, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90))
    darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
    darkPalette.setColor(QPalette.Text, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Link, QColor(56, 252, 196))
    darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.LinkVisited, QColor(80, 80, 80))

    # disabled
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

    app.setPalette(darkPalette)

    _apply_base_theme(app)


def darkUltra(app, view):
    """
    Apply a super dark-colored theme to Facile. This palette is custom made, based on qtmodern dark.

    :param app: QApplication instance
    :type app: QApplication
    """

    darkPalette = QPalette()

    # base
    darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53).darker())
    darkPalette.setColor(QPalette.Light, QColor(180, 180, 180).darker())
    darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90).darker())
    darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35).darker())
    darkPalette.setColor(QPalette.Text, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.Base, QColor(42, 42, 42).darker())
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53).darker())
    darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20).darker())
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218).darker())
    darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.Link, QColor(56, 252, 196).darker())
    darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66).darker())
    darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53).darker())
    darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180).darker(f=150))
    darkPalette.setColor(QPalette.LinkVisited, QColor(80, 80, 80).darker())

    # disabled
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127).darker())
    darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127).darker())
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127).darker())
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80).darker())
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127).darker())

    app.setPalette(darkPalette)

    _apply_base_theme(app)


def lightUltra(app, view):
    """
    Apply the ultra light theme to Facile. This palette is a slightly modified version of qtmodern light.

    :param app: QApplication instance
    :type app: QApplication
    """

    lightPalette = QPalette()

    # base
    lightPalette.setColor(QPalette.WindowText, QColor(20, 20, 20))
    lightPalette.setColor(QPalette.Button, QColor(240, 240, 240))
    lightPalette.setColor(QPalette.Light, QColor(180, 180, 180))
    lightPalette.setColor(QPalette.Midlight, QColor(200, 200, 200))
    lightPalette.setColor(QPalette.Dark, QColor(225, 225, 225))
    lightPalette.setColor(QPalette.Text, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.BrightText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.Base, QColor(235, 235, 235))
    lightPalette.setColor(QPalette.Window, QColor(250, 250, 250))
    lightPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    lightPalette.setColor(QPalette.Highlight, QColor(76, 163, 224))
    lightPalette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.Link, QColor(0, 162, 232))
    lightPalette.setColor(QPalette.AlternateBase, QColor(223, 223, 223))
    lightPalette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240))
    lightPalette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.LinkVisited, QColor(222, 222, 222))

    # disabled
    lightPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(115, 115, 115))
    lightPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(115, 115, 115))
    lightPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(115, 115, 115))
    lightPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(190, 190, 190))
    lightPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(115, 115, 115))

    app.setPalette(lightPalette)

    _apply_base_theme(app)


def lightModern(app, view):
    """
    Apply the modern light theme to Facile. This palette is custom made, based on qtmodern light.

    :param app: QApplication instance
    :type app: QApplication
    """

    lightPalette = QPalette()

    # base
    lightPalette.setColor(QPalette.WindowText, QColor(20, 20, 20))
    lightPalette.setColor(QPalette.Button, QColor(240, 240, 240).darker(f=110))
    lightPalette.setColor(QPalette.Light, QColor(180, 180, 180).darker(f=110))
    lightPalette.setColor(QPalette.Midlight, QColor(200, 200, 200).darker(f=110))
    lightPalette.setColor(QPalette.Dark, QColor(225, 225, 225).darker(f=110))
    lightPalette.setColor(QPalette.Text, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.BrightText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.Base, QColor(237, 237, 237).darker(f=130))
    lightPalette.setColor(QPalette.Window, QColor(240, 240, 240).darker(f=110))
    lightPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    lightPalette.setColor(QPalette.Highlight, QColor(76, 163, 224))
    lightPalette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.Link, QColor(0, 162, 232))
    lightPalette.setColor(QPalette.AlternateBase, QColor(225, 225, 225).darker(f=130))
    lightPalette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240).darker(f=120))
    lightPalette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    lightPalette.setColor(QPalette.LinkVisited, QColor(222, 222, 222).darker(f=110))

    # disabled
    lightPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(115, 115, 115).darker(f=110))
    lightPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(115, 115, 115).darker(f=110))
    lightPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(115, 115, 115).darker(f=110))
    lightPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(190, 190, 190).darker(f=110))
    lightPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(115, 115, 115).darker(f=110))

    app.setPalette(lightPalette)

    _apply_base_theme(app)


def darkClassic(app, view):
    """
    Apply the classic dark theme to Facile. This palette is the default option,
    derived from https://gist.github.com/QuantumCD/6245215, and was the original theme that came with Facile.

    :param app: QApplication instance
    :type app: QApplication
    """

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Light, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.Midlight, QColor(90, 90, 90))
    dark_palette.setColor(QPalette.Dark, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.LinkVisited, QColor(80, 80, 80))

    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(115, 115, 115))
    dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
    dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(115, 115, 115))

    app.setPalette(dark_palette)
    # app.setStyleSheet("QScrollArea > QWidget > QWidget { background-color: palette(base); }")
    _apply_base_theme(app, False)


def lightClassic(app, view):
    """
    Apply the classic light theme to Facile.
    This theme is meant to imitate the classic dark theme, just lighter.

    :param app: QApplication instance
    :type app: QApplication
    """

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(180, 180, 180))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(130, 130, 130))
    palette.setColor(QPalette.AlternateBase, QColor(180, 180, 180))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(180, 180, 180))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Light, QColor(180, 180, 180).darker(f=110))
    palette.setColor(QPalette.Midlight, QColor(200, 200, 200).darker(f=110))
    palette.setColor(QPalette.Dark, QColor(225, 225, 225).darker(f=110))
    palette.setColor(QPalette.Shadow, QColor(20, 20, 20))

    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(60, 60, 60))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(115, 115, 115))
    palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(190, 190, 190).darker(f=110))
    palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(115, 115, 115).darker(f=110))

    app.setPalette(palette)
    _apply_base_theme(app, False)
