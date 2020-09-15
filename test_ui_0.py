from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from pandastable import Table, TableModel
import pandas as pd
import yaml
import os
from hurry.filesize import size as file_size

from modules import ui, raw_data

ui_obj = ui.UI()
raw_obj = raw_data.Raw()

root = Tk()
root.geometry("{}x{}".format(ui_obj.get_window_dimensions()["x"], ui_obj.get_window_dimensions()["y"]))

"""
LabelFrames
"""
frame_main = ui_obj.set_properties(
    LabelFrame(root), 
    text="Main",
    height=ui_obj.get_window_dimensions()["y"] - 50
    # width=ui_obj.get_window_dimensions()["x"]
)
frame_main.pack_propagate(0)
frame_main.pack(side=TOP, fill=X, expand=False)

# Frame for status widgets
frame_status = ui_obj.set_properties(
    LabelFrame(root), 
    text="General",
    height=50
    # width=50
    )
# frame_status.grid(row=3, column=1)
frame_status.pack_propagate(0)
frame_status.pack(side=BOTTOM, fill=BOTH)



frame_raw_main = ui_obj.set_properties(
    LabelFrame(frame_main),
    text="Raw Main",
    height=ui_obj.get_window_dimensions()["y"],
    width=ui_obj.get_window_dimensions()["x"]/2 - 5,
    bg="Red"
)
frame_raw_main.pack_propagate(0)
frame_raw_main.pack(side=LEFT, expand=False)

frame_dataset_main = ui_obj.set_properties(
    LabelFrame(frame_main),
    text="Dataset Main",
    height=ui_obj.get_window_dimensions()["y"],
    width=ui_obj.get_window_dimensions()["x"]/2 - 5,
    bg="Blue"
)
frame_dataset_main.pack_propagate(0)
frame_dataset_main.pack(side=RIGHT, expand=False)

frame_raw_data_widgets = ui_obj.set_properties(
    LabelFrame(frame_raw_main),
    text="Raw Data Widgets",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Pink"
)
frame_raw_data_widgets.pack_propagate(0)
frame_raw_data_widgets.pack(side=TOP, expand=False, fill=X)

frame_raw_data = ui_obj.set_properties(
    LabelFrame(frame_raw_main),
    text="Raw Data Visualization",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Brown"
)
frame_raw_data.pack_propagate(0)
frame_raw_data.pack(side=BOTTOM, expand=False, fill=X)

frame_dataset_widgets = ui_obj.set_properties(
    LabelFrame(frame_dataset_main),
    text="Dataset Widgets",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Yellow"
)
frame_dataset_widgets.pack_propagate(0)
frame_dataset_widgets.pack(side=TOP, expand=False, fill=X)

frame_dataset = ui_obj.set_properties(
    LabelFrame(frame_dataset_main),
    text="Dataset Visualization",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Maroon"
)
frame_dataset.pack_propagate(0)
frame_dataset.pack(side=BOTTOM, expand=False, fill=X)

def quit():
    root.destroy()
    return

button_exit = ui_obj.set_properties(Button(frame_status), text="EXIT", state=ACTIVE, command=exit)
button_exit.pack(side=RIGHT, fill=Y)

root.mainloop()