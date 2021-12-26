'''Common functions used throughout the program'''
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # pylint: disable=no-member, protected-access
    except Exception: #pylint: disable=broad-except
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
