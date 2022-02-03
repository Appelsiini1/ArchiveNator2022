"""ArchiveNator2022 is a Python program to index physical documents to a database manually."""
import logging
import os
import sys
import PySimpleGUI as sg
from constants import VERSION, ENVPATH
import archive_window


def load_configs():
    """Load program configurations"""
    settings = sg.UserSettings(filename=os.path.join(ENVPATH, "settings.json"))
    if bool(settings):
        logging.info("No settings found, loading defaults.")
        settings["theme"] = "Reddit"
        settings["ButtonColour"] = "Red"
        settings["defaultDBPath"] = ENVPATH

    logging.info("Settings loaded.")
    return settings


def init():
    """Program initiliazation"""

    logname = os.path.join(ENVPATH, "log.txt")
    if os.path.exists(ENVPATH) is False:
        os.mkdir(ENVPATH)
    logging.basicConfig(
        filename=logname,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    logging.info( # pylint: disable=logging-fstring-interpolation
        f"ArchiveNator2022 v{VERSION}"
    )


def main():
    """Main event loop and startup"""
    init()
    settings = load_configs()

    sg.theme(settings["theme"])
    sg.theme_button_color(color="Red")

    menu_def = [["Tiedosto", ["Poistu"]], ["Tietoa", ["Tietoa", "Lisenssit"]]]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text(" " * 15)],
        [
            sg.Text(
                "ArchiveNator2022",
                font=("Verdana", 15, "bold"),
                size=(20, 1),
                justification="center",
                text_color="Red",
            )
        ],
        [sg.Text(" " * 15)],
        [
            sg.Text(" " * 6),
            sg.FileBrowse(
                "Avaa tietokanta", font=("Verdana", 12), size=(20, 1), key="open", target="invisible", file_types=(('Tietokannat', '*.db'),)
            ), sg.Input("", key="invisible", visible=False, enable_events=True)
        ],
        [
            sg.Text(" " * 6),
            sg.FileSaveAs(
                "Luo uusi tietokanta", font=("Verdana", 12), size=(20, 1), key="new", target="invisible2", file_types=(('Tietokannat', '*.db'),)
            ), sg.Input("", key="invisible2", visible=False, enable_events=True)
        ],
        [sg.Text(" " * 6), sg.Button("Asetukset", font=("Verdana", 12), size=(20, 1))],
        [sg.Text(" " * 6), sg.Button("Poistu", font=("Verdana", 12), size=(20, 1))],
    ]

    main_window = sg.Window("Päävalikko", layout)

    while True:
        event, values = main_window.read()

        if event == "invisible":
            file = values["invisible"]
            if file == "":
                continue
            main_window.Hide()
            archive_window.arc_window(file)
            main_window.UnHide()
        elif event == "invisible2":
            file = values["invisible2"]
            if file == "":
                continue
            elif file.split("/")[-1].split(".")[-1] != "db":
                file += ".db"
            main_window.Hide()
            archive_window.arc_window(file)
            main_window.UnHide()
        elif event == "Asetukset":
            sg.PopupOK("Asetukset", title="Testi")
        elif event in (None, "Poistu"):
            break

    main_window.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
