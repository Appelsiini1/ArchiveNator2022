"""ArchiveNator2022 is a Python program to index physical documents to a database manually."""
import sys
import PySimpleGUI as sg


from constants import MENU_DEF
import initialization
import archive_main_window


def define_main_window():
    '''Define main window'''

    layout = [
        [sg.Menu(MENU_DEF)],
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
                "Avaa tietokanta",
                font=("Verdana", 12),
                size=(20, 1),
                key="open",
                target="invisible",
                file_types=(("Tietokannat", "*.db"),),
            ),
            sg.Input("", key="invisible", visible=False, enable_events=True),
        ],
        [
            sg.Text(" " * 6),
            sg.FileSaveAs(
                "Luo uusi tietokanta",
                font=("Verdana", 12),
                size=(20, 1),
                key="new",
                target="invisible2",
                file_types=(("Tietokannat", "*.db"),),
            ),
            sg.Input("", key="invisible2", visible=False, enable_events=True),
        ],
        [sg.Text(" " * 6), sg.Button("Asetukset", font=("Verdana", 12), size=(20, 1))],
        [sg.Text(" " * 6), sg.Button("Poistu", font=("Verdana", 12), size=(20, 1))],
    ]

    return layout

def main():
    """Main event loop and startup"""
    initialization.init()
    settings = initialization.load_configs()

    sg.theme(settings["theme"])
    sg.theme_button_color(color="Red")

    layout = define_main_window()

    main_window = sg.Window("Päävalikko", layout)

    while True:
        event, values = main_window.read()

        if event == "invisible":
            file = values["invisible"]
            if file == "":
                continue
            main_window.Hide()
            archive_main_window.arc_window(file)
            main_window.UnHide()
        elif event == "invisible2":
            file = values["invisible2"]
            if file == "":
                continue
            elif file.split("/")[-1].split(".")[-1] != "db":
                file += ".db"
            main_window.Hide()
            archive_main_window.create_new(file)
            main_window.UnHide()
        elif event == "Asetukset":
            sg.PopupOK("Asetukset", title="Testi")
        elif event in (None, "Poistu"):
            break

    main_window.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
