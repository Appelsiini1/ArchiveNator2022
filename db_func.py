"""Database functions"""

import sqlite3
import logging


def get_db_info(file: str):
    """Returns a list with the database information"""
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        c.execute("SELECT db_name FROM DB_info")
        db_name = c.fetchone()[0]

        c.execute("SELECT db_desc FROM DB_info")
        db_desc = c.fetchone()[0]
        if db_desc == "":
            db_desc = "(Tyhjä)"

        c.execute("SELECT db_table_count, db_tables FROM DB_info")
        db_tables_raw = c.fetchall()[0]
        db_table_count = db_tables_raw[0]
        db_tables = [db_tables_raw[1]]
        if db_table_count == 0:
            db_tables = ["(Uusi taulu)"]
        else:
            db_tables = ["(Uusi taulu)"] + db_tables[0].split(";")
        print(db_tables)
    return [db_name, db_desc, db_tables]


def update_db_info(file: str, new_name=None, new_desc=None):
    """Updates database entry for name and/or description of the database"""

    with sqlite3.connect(file) as conn:
        c = conn.cursor()

        if new_name is not None:
            c.execute(f'UPDATE DB_info SET db_name="{new_name}"')
        if new_desc is not None:
            c.execute(f'UPDATE DB_info SET db_desc="{new_desc}"')
        conn.commit()


def update_db_tables_info(cursor: any, obj: list, upd_type: int):
    """Update metadata for tables"""
    cursor.execute("SELECT db_table_count, db_tables FROM DB_info")
    db_tables_raw = cursor.fetchall()[0]
    try:
        db_tables = db_tables_raw[1].split(";")
        db_table_count = db_tables_raw[0]
    except AttributeError:
        db_tables = []
        db_table_count = 0

    if upd_type == 0:
        db_table_count = db_tables_raw[0] - 1
        try:
            db_tables.remove(obj[0])
        except ValueError:
            logging.exception("Unable to find table to remove in database info.")
            return

    elif upd_type == 1:
        try:
            rm_index = db_tables.index(obj[0])
            
        except ValueError:
            logging.exception("Unable to find table to update in database info.")
            return
        db_tables[rm_index] = obj[2]

    elif upd_type == 2:
        db_table_count = db_table_count + 1
        db_tables.append(obj[0])

    cursor.execute(f'UPDATE Db_info SET db_table_count="{db_table_count}"')
    cursor.execute(f'UPDATE Db_info SET db_tables="{";".join(db_tables)}"')


def update_db_tables(file: str, tables_to_update: list):
    """ "Updates table metadata and adds or removes tables in the database"""
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        for obj in tables_to_update:
            if obj[1] == 0:
                c.execute(f"DROP TABLE IF EXISTS {obj[0]}")
                update_db_tables_info(c, obj, 0)

            elif obj[1] == 1:
                c.execute(f"ALTER TABLE {obj[0]} RENAME TO {obj[2]}")
                update_db_tables_info(c, obj, 1)

            elif obj[1] == 2:
                c.execute(
                    f"""CREATE TABLE IF NOT EXISTS {obj[0]}(
                    ID INT PRIMARY KEY UNIQUE,
                    name TEXT,
                    date TEXT,
                    desc TEXT,
                    path TEXT,
                    other TEXT);"""
                )
                update_db_tables_info(c, obj, 2)

        conn.commit()
