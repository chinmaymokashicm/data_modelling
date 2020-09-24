import tkinter as tk
from .properties import Properties

class Frame:
    def __init__(self, master, **kwargs):
        try:
            properties_obj = Properties()
            self.widget = properties_obj.set_properties(tk.Frame(master),**kwargs)
        except Exception as e:
            print(e)
        
