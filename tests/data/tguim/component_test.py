
import sys, os

from pprint import pprint

# sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.abspath("../../../src/")))
sys.path.insert(0, os.path.abspath("./src/"))
pprint(sys.path)


import unittest
from PySide2.QtWidgets import QApplication
from src.data.tguim.targetguimodel import TargetGuiModel
from src.data.tguim.component import Component
from src.data.tguim.visibilitybehavior import VisibilityBehavior

class TestComponent(unittest.TestCase):
    def test_add_remove_vis_behaviors(self):
        app = QApplication([])

        # Initialize data.
        tguim = TargetGuiModel()
        comp_1 = Component(tguim)
        vb_1 = VisibilityBehavior()
        vb_2 = VisibilityBehavior()

        # Check that add functions verify input param types.
        self.assertRaises(TypeError, comp_1.addDestVisibilityBehavior, "wrong")
        self.assertRaises(TypeError, comp_1.addSrcVisibilityBehavior, "wrong")
