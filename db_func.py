'''Database functions'''
import sqlite3
import PySimpleGUI as sg

def open_db(file):
    with sqlite3.connect(file) as conn:
        c = conn.cursor()

def add_item():
    pass

def del_item():
    pass

