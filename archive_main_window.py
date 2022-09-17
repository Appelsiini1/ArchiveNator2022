"""Main window for archive handling"""
import sqlite3
import PySimpleGUI as sg
from archive_windows_layouts import new_file_layout, archive_main_window, info_update_window
from db_func import get_db_info, update_db_info, update_db_tables


def create_new(file: str):
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
                    (values["name"], values["description"], 0, None),
                )
                conn.commit()
            window.close()
            arc_window(file)
            break


def update_db_window(file: str):
    """Creates a window to update database info"""

    db_name, db_desc, _ = get_db_info(file)

    layout = info_update_window(db_name, db_desc)
    window = sg.Window("Tietokannan hallinta", layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (None, "peruuta"):
            break
        if event == "ok":
            if values["name"] is not db_name:
                update_db_info(file, new_name=values["name"])
            if values["description"] is not db_desc:
                update_db_info(file, new_desc=values["description"])
            break
    window.close()
    return [values["name"],values["description"]]


def arc_dropdown_menu(value:str, file:str):
    """Select a database table to view"""
    if value == "(Uusi taulu)":
        table_name=sg.popup_get_text("Anna uuden taulun nimi:")
        if table_name is None:
            return
        else:
            update_db_tables(file, [[table_name, 2]])
    #else:



def arc_window(file: str):
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
            window.Hide()
            arc_dropdown_menu(values["dropdown"], file)
            _, _, db_tables = get_db_info(file)
            window["dropdown"].update(value=db_tables[0], values=db_tables)
            window.UnHide()

        if event == "dropdown_delete":
            if values["dropdown"] == "(Uusi taulu)":
                continue
            update_db_tables(file, [[values["dropdown"], 0]])
            sg.popup_ok(f"Taulu '{values['dropdown']}' poistettu.")
            _, _, db_tables = get_db_info(file)
            window["dropdown"].update(value=db_tables[0], values=db_tables)

        if event == "dropdown_change":
            if values["dropdown"] == "(Uusi taulu)":
                continue
            window.Hide()
            table_name=sg.popup_get_text("Anna uuden taulun nimi:")
            if table_name is not None:
                update_db_tables(file, [[values["dropdown"], 1, table_name]])
            window.UnHide()
            _, _, db_tables = get_db_info(file)
            window["dropdown"].update(value=db_tables[0], values=db_tables)


        if event == "change_info_button":
            window.Hide()
            new_name, new_desc = update_db_window(file)
            window["db_name"].update(f"Tietokanta: {new_name}")
            window["db_desc_text"].update(new_desc)
            window.UnHide()

    window.close()
