"""Functions to create layouts for database table management windows"""
import PySimpleGUI as sg
from constants import MENU_DEF


def table_management_layout(table_name: str, doc_titles: list):
    """Main table management window layout"""
    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                f"Taulun nimi: {table_name}",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
            )
        ],
        [sg.Text("")],
        [
            sg.Listbox(
                doc_titles,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                key="listbox",
                size=(25, 25),
            )
        ],
        [
            sg.Button(
                "Uusi dokumentti",
                font=("Verdana", 12),
                size=(25, 1),
                key="new_doc",
            ),
            sg.Button(
                "Näytä dokumentti",
                font=("Verdana", 12),
                size=(25, 1),
                key="show_doc",
            ),
        ],
    ]

    return layout


def doc_window_layout():
    """Main document window"""

    layout = [
        [sg.Menu(MENU_DEF)],
        [
            sg.Text(
                "",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
                key="title"
            )
        ],
        [
            sg.Text(
                "",
                font=("Verdana", 10, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
                key="doc_ID"
            )
        ],
        [
            sg.Text(
                "Dokumentin nimi:",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
            )
        ],
        [sg.InputText("", key="doc_name")],
        [
            sg.Text(
                "Dokumentin päivämäärä:",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
            )
        ],
        [sg.InputText("", key="doc_date")],
        [
            sg.Text(
                "Dokumentin kuvaus:",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
            )
        ],
        [sg.Multiline(key="doc_desc", size=(50, 5))],
        [
            sg.Text(
                "Dokumentin polku (valinnainen):",
                font=("Verdana", 12, "bold"),
                size=(20, 1),
                justification="left",
                text_color="red",
            )
        ],
        [
            sg.Input("", key="doc_path", enable_events=True),
            sg.FileBrowse(
                "Valitse...",
                font=("Verdana", 12),
                size=(20, 1),
                key="open",
                target="doc_path",
            ),
        ],
        [sg.Text(" " * 6)],
        [
            sg.Button("Tallenna", font=("Verdana", 12), size=(12, 1), key="save"),
            sg.Button("Peruuta", font=("Verdana", 12), size=(12, 1), key="cancel"),
        ],
    ]

    return layout
