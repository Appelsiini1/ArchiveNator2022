"""Functions to create layouts for archive management windows"""
import PySimpleGUI as sg
from constants import MENU_DEF
from db_func import get_db_info


def new_file_layout():
    """Layout for new database window"""
    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                "Tietokannan nimi:",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [sg.InputText("", key="name")],
        [
            sg.Text(
                "Kuvaus:",
                font=("Verdana", 12),
                size=(20, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [sg.Multiline(key="description", size=(50, 5))],
        [
            sg.Button("OK", font=("Verdana", 12), size=(12, 1), key="ok"),
            sg.Button("Peruuta", font=("Verdana", 12), size=(12, 1), key="peruuta"),
        ],
    ]

    return layout


def archive_main_window(file: str):
    """Define layout for main window of archive management"""
    db_name, db_desc, db_tables = get_db_info(file)

    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                f"Tietokanta: {db_name}",
                key="db_name",
                font=("Verdana", 12, "bold"),
                size=(22, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [
            sg.Button(
                "Näytä tietokannan kuvaus",
                font=("Verdana", 12),
                size=(25, 1),
                key="desc_button",
            ),
            sg.Button(
                "Muuta tietoja",
                font=("Verdana", 12),
                size=(25, 1),
                key="change_info_button",
            ),
        ],
        [
            sg.Text(
                db_desc,
                font=("Verdana", 10),
                # size=(45, desc_newlines + 1),
                justification="left",
                text_color="Black",
                expand_y=True,
                visible=False,
                key="db_desc_text",
                auto_size_text=True,
            )
        ],
        [sg.Text(" " * 40, size=(50, 1))],
        [
            sg.DropDown(
                db_tables,
                default_value="(Uusi taulu)",
                size=(25, 2),
                key="dropdown",
            ),
            sg.Button("Valitse", font=("Verdana", 12), size=(5, 1), key="dropdown_select"),
            sg.Button("Poista", font=("Verdana", 12), size=(5, 1), key="dropdown_delete"),
            sg.Button("Muuta", font=("Verdana", 12), size=(5, 1), key="dropdown_change")
        ],
        [sg.Button("Takaisin", font=("Verdana", 12), size=(12, 1), key="Poistu")],
    ]

    return layout


def info_update_window(db_name: str, db_desc: str):
    """Window for changing database information"""

    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                "Tietokannan nimi:",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [sg.InputText(db_name, key="name")],
        [
            sg.Text(
                "Kuvaus:",
                font=("Verdana", 12),
                size=(20, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [sg.Multiline(db_desc, key="description", size=(50, 5))],
        [
            sg.Button("OK", font=("Verdana", 12), size=(12, 1), key="ok"),
            sg.Button("Peruuta", font=("Verdana", 12), size=(12, 1), key="peruuta"),
        ],
    ]

    return layout
