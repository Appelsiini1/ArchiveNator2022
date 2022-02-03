'''Main window for archive handling'''
import sqlite3
import PySimpleGUI as sg

def arc_window(file):
    menu_def = [["Tiedosto", ["Poistu"]], ["Tietoa", ["Tietoa", "Lisenssit"]]]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text(" " * 15)],
        [sg.Text("", key="db_name", font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="Red",)],
        [sg.Button("Takaisin", font=("Verdana", 12), size=(12, 1),key="Poistu")],
    ]
    with sqlite3.connect(file) as conn:
        c = conn.cursor()

        window = sg.Window("Tietokannan hallinta", layout)
        while True:
            event, values = window.read()

            if event in (None, "Poistu"):
                break
        window.close()