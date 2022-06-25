"""Main window for archive handling"""
import sqlite3
import PySimpleGUI as sg
from constants import MENU_DEF


def create_new(file):
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
        [sg.Text("Kuvaus:", font=("Verdana", 12), size=(20,1), justification="left", text_color="Red")],
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
                c.execute("""CREATE TABLE IF NOT EXISTS DB_info(
                    db_name TEXT PRIMARY KEY,
                    db_desc TEXT,
                    db_table_count INT,
                    db_tables TEXT);"""
                )
                c.execute("INSERT INTO DB_info VALUES (?,?,?,?)", (values["name"], values["description"], 0, "None"))
            window.close()
            arc_window(file)
            break

    


def arc_window(file):
    """Create archive control window"""

    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                "",
                key="db_name",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="Red",
            )
        ],
        [sg.Text(" " * 15)],
        [sg.Button("Takaisin", font=("Verdana", 12), size=(12, 1), key="Poistu")],
    ]
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        c.execute("SELECT db_name FROM DB_info")
        db_name = c.fetchone()[0]

        window = sg.Window("Tietokannan hallinta", layout, finalize=True)
        while True:
            window["db_name"].update(db_name)
            event, values = window.read()
            

            if event in (None, "Poistu"):
                break
        window.close()
