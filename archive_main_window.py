"""Main window for archive handling"""
import sqlite3
import string
import PySimpleGUI as sg
from constants import MENU_DEF
from db_func import get_db_info


def create_new(file:string):
    """Create new database config window"""
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

    window = sg.Window("Uusi tietokanta", layout)
    while True:
        event, values = window.read()

        if event in (None, "Peruuta"):
            window.close()
            break
        if event == "ok":
            with sqlite3.connect(file) as conn:
                c = conn.cursor()
                c.execute(
                    """CREATE TABLE IF NOT EXISTS DB_info(
                    db_name TEXT PRIMARY KEY,
                    db_desc TEXT,
                    db_table_count INT,
                    db_tables TEXT);"""
                )
                c.execute(
                    "INSERT INTO DB_info VALUES (?,?,?,?)",
                    (values["name"], values["description"], 0, "None"),
                )
            window.close()
            arc_window(file)
            break


def arc_window(file:string):
    """Create archive control window"""

    db_desc_visible = False
    db_name, db_desc, db_tables = get_db_info(file)

    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                db_name,
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
            sg.Button(
                ">>>", font=("Verdana", 12), size=(5, 1), key="dropdown_select"
            ),
        ],
        [sg.Button("Takaisin", font=("Verdana", 12), size=(12, 1), key="Poistu")],
    ]

    window = sg.Window("Tietokannan hallinta", layout, finalize=True)
    while True:
        event, values = window.read()

        if event in (None, "Poistu"):
            break
        if event == "desc_button":

            if db_desc_visible is False:
                window["desc_button"].update("Piilota tietokannan kuvaus")
                window["db_desc_text"].update(visible=True)
                db_desc_visible = True
            else:
                window["desc_button"].update("Näytä tietokannan kuvaus")
                window["db_desc_text"].update(visible=False)
                db_desc_visible = False
        if event == "dropdown_select":
            sg.PopupOK("TESTI")
            print(values["dropdown"])
    window.close()