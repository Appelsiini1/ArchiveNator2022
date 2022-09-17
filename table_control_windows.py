"""Table control windows"""

import PySimpleGUI as sg
import table_control_windows_layouts as tcl
from db_func import get_doc_titles, get_doc_info, set_doc_info, update_doc_info


def document_window(file: str, doc_ID: int | None, mode: int, table_name: str):
    """Document information window"""

    if mode == 1:
        doc_ID = "??"
        doc_name = "Uusi dokumentti"
        doc_date = ""
        doc_desc = ""
        doc_path = ""
    if mode == 2:
        doc_info = get_doc_info(file, doc_ID, table_name)
        doc_ID = doc_info[0]
        doc_name = doc_info[1]
        doc_date = doc_info[2]
        doc_desc = doc_info[3]
        doc_path = doc_info[4]

    layout = tcl.doc_window_layout()

    window = sg.Window(f"{table_name}", layout, finalize=True)
    window["title"].update(doc_name)
    window["doc_name"].update(doc_name)
    window["doc_ID"].update(doc_ID)
    window["doc_date"].update(doc_date)
    window["doc_desc"].update(doc_desc)
    window["doc_path"].update(doc_path)
    while True:
        event, values = window.read()

        if event in (None, "cancel"):
            break

        if event == "save":
            if mode == 1:
                doc_info_new = [
                    None,
                    values["doc_name"],
                    values["doc_date"],
                    values["doc_desc"],
                    values["doc_path"],
                ]
                set_doc_info(file, table_name, doc_info_new)
            if mode == 2:
                doc_info_update = [
                    values["doc_ID"],
                    values["doc_name"],
                    values["doc_date"],
                    values["doc_desc"],
                    values["doc_path"],
                ]
                update_doc_info(file, table_name, doc_info_update)
            break
    window.close()


def main_table_window(file: str, table_name: str):
    """Create & handle main table control window"""
    doc_titles = get_doc_titles(file, table_name)

    layout = tcl.table_management_layout(table_name, doc_titles)

    window = sg.Window(f"{table_name}", layout, finalize=True)
    while True:
        event, values = window.read()

        if event in (None, "Poistu"):
            break
        if event == "new_doc":
            document_window(file, None, 1, table_name)

        if event == "show_doc":
            doc_ID_selected = values["listbox"][0].split(" - ")[0]
            document_window(file, doc_ID_selected, 2, table_name)
    window.close()
