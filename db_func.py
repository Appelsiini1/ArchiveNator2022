'''Database functions'''
import sqlite3
import string

def get_db_info(file:string):
    """Returns a list with the database information"""
    with sqlite3.connect(file) as conn:
        c = conn.cursor()
        c.execute("SELECT db_name FROM DB_info")
        db_name = c.fetchone()[0]

        c.execute("SELECT db_desc FROM DB_info")
        db_desc = c.fetchone()[0]
        if db_desc == "":
            db_desc = "(Tyhjä)"
        # desc_newlines = db_desc.count("\n")

        c.execute("SELECT db_table_count, db_tables FROM DB_info")
        db_tables_raw = c.fetchall()[0]
        db_table_count = db_tables_raw[0]
        db_tables = [db_tables_raw[1]]
        if db_table_count == 0:
            db_tables = ["(Uusi taulu)"]
        else:
            db_tables = ["(Uusi taulu)"] + db_tables[0].split(";")
    return [db_name, db_desc, db_tables]