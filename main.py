import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from pandastable import Table, TableModel
import pandas as pd
import yaml
import os
from hurry.filesize import size as file_size
import time

from modules import ui, raw_data
import frames, labels, entries

ui_obj = ui.UI()
raw_obj = raw_data.Raw()

root = tk.Tk()
root.geometry("{}x{}".format(ui_obj.get_window_dimensions()["x"], ui_obj.get_window_dimensions()["y"]))

# Generate frames

[root, ui_obj] = frames.generate(root, ui_obj)
[root, ui_obj] = labels.generate(root, ui_obj)
[root, ui_obj] = entries.generate(root, ui_obj)



root.mainloop()