import tkinter as tk
from .properties import Properties

class Button:
    def __init__(self, master, **kwargs):
        try:
            properties_obj = Properties()
            self.widget = properties_obj.set_properties(tk.Button(master), **kwargs)
        except Exception as e:
            print(e)