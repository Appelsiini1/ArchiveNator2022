"""Functions for programn initialization"""
import logging
from os import path, mkdir
from PySimpleGUI import UserSettings
from constants import ENVPATH, VERSION

def load_configs():
    """Load program configurations"""
    settings = UserSettings(filename=path.join(ENVPATH, "settings.json"))
    if not bool(settings):
        logging.info("No settings found, loading defaults.")
        settings["theme"] = "Reddit"
        settings["ButtonColour"] = "Red"
        settings["defaultDBPath"] = ENVPATH

    logging.info("Settings loaded.")
    return settings


def init():
    """Program initiliazation"""

    logname = path.join(ENVPATH, "log.txt")
    if path.exists(ENVPATH) is False:
        mkdir(ENVPATH)
    logging.basicConfig(
        filename=logname,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    logging.info(  # pylint: disable=logging-fstring-interpolation
        f"ArchiveNator2022 v{VERSION}"
    )
