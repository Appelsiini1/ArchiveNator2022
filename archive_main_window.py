"""Main window for archive handling"""
import sqlite3
import string
import PySimpleGUI as sg
from archive_windows_layouts import new_file_layout, archive_main_window


def create_new(file: string):
    """Create new database config window"""

    layout = new_file_layout()

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


def update_db_window(file: string):
    """Creates a window to update database info"""
    pass


def arc_window(file: string):
    """Create archive control window"""

    db_desc_visible = False

    layout = archive_main_window(file)

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
