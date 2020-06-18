import sys
from os.path import join, dirname, abspath
import platform

PLATFORM = platform.system()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, dirname(abspath(__file__)), relative_path)

    return join(dirname(abspath(__file__)), relative_path)
