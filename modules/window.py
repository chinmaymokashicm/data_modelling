import tkinter as tk
from .properties import Properties

class Window(tk.Tk):
    def __init__(self, window_type, title="Main Window"):
        super().__init__()
        try:
            properties_obj = Properties()
            self.width = properties_obj.window[window_type]["width"]
            self.height = properties_obj.window[window_type]["height"]
            self.geometry("{}x{}".format(self.width, self.height))
            self.title(title)
        except Exception as e:
            raise Exception(e)