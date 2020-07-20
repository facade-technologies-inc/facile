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

This module contains the Theme class, which lets users customize colors in Facile.
"""

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QColor
import gui.frame.styles as styles
import graphics.tguim.toplevelwrappergraphics as tlwg

class Theme:

    def __init__(self, base, custom: bool = False):
        """
        Initializes a theme, basing it off of a QtModern Style

        :param base: The Facile layout colors, entered as a function coming from QtModern
        :param custom: Whether this Theme is custom or one of the defaults
        :type custom: bool
        """

        # Useful variables and functions
        self._base = base
        self._name = ''
        self._custom = custom

        # Default the colors
        self.tguimColorSettings = {}
        self.apimColors = {}  # These are public for easy access

        if not custom:  # Shaves off some microseconds
            self._setDefaultColors()

    def isCustom(self) -> bool:
        """
        Whether or not this is a custom theme
        """
        return self._custom

    def setName(self, name: str):
        """
        Sets this theme's name

        :param name: The name of the Theme
        :type name: str
        """
        self._name = name

    def baseStr(self):
        """
        Gets the base function's name
        """
        return self._base.__name__

    def getName(self) -> str:
        """
        Gets this Theme's name

        :return: This theme's name
        :rtype: str
        """
        return self._name

    def applyTo(self, view: 'FacileView'):
        """
        Applies this theme to Facile

        :param view: The current FacileView
        :type view: FacileView
        """

        # Theme the structure of Facile using the base
        self._base(QApplication.instance())

        # Then apply the saved colors
        view.updateColors(self.tguimColorSettings, self.apimColors)

        # Then update all necessary images and icons
        # The EC Section's expand/collapse button
        if self.baseStr() in ('darkClassic', 'darkUltra', 'darkModern'):
            tlwg.TopLevelWrapperGraphics.Button.BUTTON_IMG_THM = 0
        else:
            tlwg.TopLevelWrapperGraphics.Button.BUTTON_IMG_THM = 1

    def _setDefaultColors(self):
        """
        Sets the default color combos based on the base function passed in
        """

        if self._base is styles.darkClassic:

            self._name = 'Classic (Dark)'

            self.setTGUIMColorSettings(QColor(0, 141, 222).lighter(f=75), False)

            self.apimColors['Action Pipeline'] = QColor(0, 141, 222).lighter(f=75)
            self.apimColors['Action Wrapper'] = QColor(52, 73, 94)
            self.apimColors['Inside Port'] = QColor(121, 125, 127)
            self.apimColors['Outside Port'] = QColor(121, 125, 127)
            self.apimColors['Sequence Tag'] = QColor(121, 125, 127)

        elif self._base is styles.lightClassic:

            self._name = 'Classic (Light)'

            self.setTGUIMColorSettings(QColor(0, 141, 222), False)

            self.apimColors['Action Pipeline'] = QColor(0, 141, 222)
            self.apimColors['Action Wrapper'] = QColor(52, 73, 94).lighter()
            self.apimColors['Inside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Outside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Sequence Tag'] = QColor(121, 125, 127).lighter()

        elif self._base is styles.darkModern:

            self._name = 'Modern (Dark)'

            self.setTGUIMColorSettings(QColor(0, 141, 222).lighter(f=85), True)

            self.apimColors['Action Pipeline'] = QColor(0, 141, 222).lighter(f=85)
            self.apimColors['Action Wrapper'] = QColor(52, 73, 94).lighter(f=110)
            self.apimColors['Inside Port'] = QColor(100, 100, 100)
            self.apimColors['Outside Port'] = QColor(100, 100, 100)
            self.apimColors['Sequence Tag'] = QColor(121, 125, 127)

        elif self._base is styles.lightModern:

            self._name = 'Modern (Light)'

            self.setTGUIMColorSettings(QColor(0, 141, 222).lighter(f=120), True)

            self.apimColors['Action Pipeline'] = QColor(0, 76, 153).lighter()
            self.apimColors['Action Wrapper'] = QColor(52, 73, 94).lighter()
            self.apimColors['Inside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Outside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Sequence Tag'] = QColor(121, 125, 127).lighter()

        elif self._base is styles.darkUltra:

            self._name = 'Ultra Dark'

            self.setTGUIMColorSettings(QColor(42, 65, 88), True)

            self.apimColors['Action Pipeline'] = QColor(42, 65, 88)
            self.apimColors['Action Wrapper'] = QColor(89, 115, 135)
            self.apimColors['Inside Port'] = QColor(60, 70, 72)
            self.apimColors['Outside Port'] = QColor(60, 70, 72)
            self.apimColors['Sequence Tag'] = QColor(149, 138, 86)

        elif self._base is styles.lightUltra:

            self._name = 'Ultra Light'

            self.setTGUIMColorSettings(QColor(70, 190, 210).lighter(f=110), True)

            self.apimColors['Action Pipeline'] = QColor(70, 190, 210)
            self.apimColors['Action Wrapper'] = QColor(52, 73, 94).lighter(f=130)
            self.apimColors['Inside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Outside Port'] = QColor(121, 125, 127).lighter(f=140)
            self.apimColors['Sequence Tag'] = QColor(121, 125, 127).lighter(f=180)

    def setTGUIMColorSettings(self, color: QColor, flat: bool):
        """
        Sets the TGUIM base color to color, and sets Is Flat to flat

        :param color: color to be applied
        :type color: QColor
        :param flat: Whether the TGUIM color is assigned on depth
        :type flat: bool
        """

        self.tguimColorSettings['Base Color'] = color
        self.tguimColorSettings['Is Flat'] = flat

    def base(self):
        """
        Gets the base function
        """
        return self._base

    def getCopy(self) -> 'Theme':
        """
        Creates an exact replica of this theme, and returns it
        """

        thm = Theme(self._base, custom=self._custom)

        thm.setName(self._name)
        thm.tguimColorSettings = self.tguimColorSettings.copy()
        thm.apimColors = self.apimColors.copy()

        return thm

    # Get/set APIM colors just by accessing/writing to the apimColors dictionary

    def asDict(self) -> dict:
        """
        Returns this theme's information in a dictionary, only if it is a custom theme

        :return: This Theme as a dictionary
        :rtype: dict
        """

        if not self._custom:  # We don't want to save the default themes, they'll be made automatically
            return

        d = {}

        tguimDict = {
            'Base Color': self.tguimColorSettings['Base Color'].rgba(),
            'Is Flat':    self.tguimColorSettings['Is Flat']
        }
        apimDict = {
            'Action Pipeline': self.apimColors['Action Pipeline'].rgba(),
            'Action Wrapper':  self.apimColors['Action Wrapper'].rgba(),
            'Inside Port':     self.apimColors['Inside Port'].rgba(),
            'Outside Port':    self.apimColors['Outside Port'].rgba(),
            'Sequence Tag':    self.apimColors['Sequence Tag'].rgba()
        }

        d['tguim'] = tguimDict
        d['apim'] = apimDict
        d['name'] = self._name
        d['base'] = self._base.__name__

        return d

    @staticmethod
    def fromDict(d: dict) -> 'Theme':
        """
        Constructs a theme object from a dictionary

        :param d: The dictionary containing Theme information
        """

        baseFunc = getattr(styles, d['base'])
        thm = Theme(baseFunc, custom=True)  # Only saving custom functions

        tguimDict = {
            'Base Color': QColor.fromRgba(d['tguim']['Base Color']),
            'Is Flat':    d['tguim']['Is Flat']
        }
        apimDict = {
            'Action Pipeline': QColor.fromRgba(d['apim']['Action Pipeline']),
            'Action Wrapper':  QColor.fromRgba(d['apim']['Action Wrapper']),
            'Inside Port':     QColor.fromRgba(d['apim']['Inside Port']),
            'Outside Port':    QColor.fromRgba(d['apim']['Outside Port']),
            'Sequence Tag':    QColor.fromRgba(d['apim']['Sequence Tag'])
        }

        thm.tguimColorSettings = tguimDict
        thm.apimColors = apimDict
        thm.setName(d['name'])

        return thm
