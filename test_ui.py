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

ui_obj = ui.UI()
raw_obj = raw_data.Raw()

root = tk.Tk()
root.geometry("{}x{}".format(ui_obj.get_window_dimensions()["x"], ui_obj.get_window_dimensions()["y"]))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# root.geometry("")

def reset_raw():
    scale_number_of_rows_in_preview.configure(variable=tk.IntVar(value=ui_obj.get_number_of_rows_in_preview_default()))
    entry_number_of_rows_in_preview.delete(0, tk.END)
    entry_number_of_rows_in_preview.insert(0, ui_obj.get_number_of_rows_in_preview_default())
    entry_number_of_rows_in_preview.configure(bg="White")
    button_generate_preview.configure(text="Generate preview")
    # checkbutton_groupby.configure(state=tk.DISABLED)
    # menubutton_groupby.configure(state=tk.DISABLED)



"""
LabelFrames
"""
frame_main = ui_obj.set_properties(
    tk.LabelFrame(root), 
    text="Main",
    height=ui_obj.get_window_dimensions()["y"] - 50,
    width=ui_obj.get_window_dimensions()["x"]
)
frame_main.pack_propagate(0)
frame_main.pack(side=tk.TOP, fill=tk.X, expand=False)

# Frame for status widgets
frame_status = ui_obj.set_properties(
    tk.LabelFrame(root), 
    text="General",
    height=50
    # width=50
    )
# frame_status.grid(row=3, column=1)
frame_status.pack_propagate(0)
frame_status.pack(side=tk.BOTTOM, fill=tk.BOTH)



frame_raw_main = ui_obj.set_properties(
    tk.LabelFrame(frame_main),
    text="Raw Main",
    height=ui_obj.get_window_dimensions()["y"],
    width=ui_obj.get_window_dimensions()["x"]/2 - 5,
    bg="Red"
)
frame_raw_main.pack_propagate(0)
frame_raw_main.pack(side=tk.LEFT, expand=False)

frame_dataset_main = ui_obj.set_properties(
    tk.LabelFrame(frame_main),
    text="Dataset Main",
    height=ui_obj.get_window_dimensions()["y"],
    width=ui_obj.get_window_dimensions()["x"]/2 - 5,
    bg="Blue"
)
frame_dataset_main.pack_propagate(0)
frame_dataset_main.pack(side=tk.RIGHT, expand=False)

frame_raw_data_widgets = ui_obj.set_properties(
    tk.LabelFrame(frame_raw_main),
    text="Raw Data Widgets",
    height=ui_obj.get_window_dimensions()["y"]/2,
    bg="Pink"
)
frame_raw_data_widgets.pack_propagate(0)
frame_raw_data_widgets.pack(side=tk.TOP, expand=False, fill=tk.BOTH)


def create_aggregations_frame(frame):
    list_aggregations = ui_obj.get_list_group_agg()

    dict_mapping = {}
    # Create the aggregation options
    for i in range(0, len(list_aggregations)):
        label_aggregation_option = ui_obj.set_properties(
            tk.Label(frame),
            text=list_aggregations[i]
        )
        label_aggregation_option.grid(row=i, column=0)

        menubutton_aggregation = ui_obj.set_properties(
            tk.Menubutton(frame),
            text="Agg columns"
            # state=tk.ACTIVE
        )
        menubutton_aggregation.grid(row=i, column=1)

        dict_mapping[list_aggregations[i]] = [label_aggregation_option, menubutton_aggregation]

    ui_obj.set_dict_aggregation_frame_components(dict_mapping) 


frame_raw_data_widgets_aggregations = ui_obj.set_properties(
    tk.LabelFrame(frame_raw_data_widgets),
    text="Aggregations",
    height=ui_obj.get_window_dimensions()["y"]/4,
    # height=120,
    width=ui_obj.get_window_dimensions()["x"]/4,
    # width=100,
    bg="Yellow"
)
frame_raw_data_widgets_aggregations.pack_propagate(0)
frame_raw_data_widgets_aggregations.grid(row=2, column=1, rowspan=3, columnspan=2, sticky="ne")
# frame_raw_data_widgets_aggregations.grid(row=2, column=2)
create_aggregations_frame(frame_raw_data_widgets_aggregations)


frame_raw_data = ui_obj.set_properties(
    tk.LabelFrame(frame_raw_main),
    text="Raw Data Visualization",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Brown"
)
frame_raw_data.pack_propagate(0)
frame_raw_data.pack(side=tk.BOTTOM, expand=False, fill=tk.X)

frame_dataset_widgets = ui_obj.set_properties(
    tk.LabelFrame(frame_dataset_main),
    text="Dataset Widgets",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Yellow"
)
frame_dataset_widgets.pack_propagate(0)
frame_dataset_widgets.pack(side=tk.TOP, expand=False, fill=tk.X)






frame_dataset = ui_obj.set_properties(
    tk.LabelFrame(frame_dataset_main),
    text="Dataset Visualization",
    height=ui_obj.get_window_dimensions()["y"]/2 - 10,
    bg="Maroon"
)
frame_dataset.pack_propagate(0)
frame_dataset.pack(side=tk.BOTTOM, expand=False, fill=tk.X)

"""
Tables
"""
# table_raw_data = Table(frame_raw_data_widgets, showtoolbar=True, showstatusbar=True, dataframe=ui_obj.get_df_raw())
# table_raw_data.pack()
# table_raw_data.show()

# df = pd.read_csv("/home/chinmay/Documents/indian_liver_patients/indian_liver_patient.csv", engine="python")
# table_raw_data = Table(frame_raw_data, dataframe=TableModel.getSampleData(), showtoolbar=True, showstatusbar=True)
# table_raw_data.show()



"""
Labels
"""
label_path_file = ui_obj.set_properties(
    tk.Label(frame_raw_data_widgets), 
    text="Select raw dataset",
    width=20
    )
label_path_file.configure(anchor="c")
label_path_file.grid(row=0, column=1)

label_df_config = ui_obj.set_properties(
    tk.Label(frame_raw_data_widgets), 
    text="EMPTY",
    width=20
    )
label_df_config.configure(anchor="c")
label_df_config.grid(row=1, column=1)

"""
Entries
"""

entry_number_of_rows_in_preview = ui_obj.set_properties(
    tk.Entry(frame_raw_data_widgets),
    textvariable=tk.StringVar(),
    state=tk.NORMAL
)
# entry_number_of_rows_in_preview.configure(command=change_rows_table_entry)
entry_number_of_rows_in_preview.grid(row=0, column=2)



"""
Buttons
"""
def quit():
    root.destroy()
    return

def load_file_path():
    path_file = fd.askopenfilename(
        initialdir=ui_obj.get_default_dir(),
        title="Select raw dataset",
        filetypes = (("CSV files","*.csv"),("TXT files","*.txt"),("XLSX files","*.xlsx"),("all files","*.*"))
        )
    if(path_file != ""):
        try:
            path_folder = os.path.dirname(path_file)
            size_file = file_size(os.stat(path_file).st_size)
            ui_obj.set_path_file(path_file)
            ui_obj.set_default_dir(path_folder)
            label_path_file.configure(text=os.path.basename(path_file))
            df = pd.read_csv(ui_obj.get_path_file(), engine="python", index_col=False)
            ui_obj.set_df_raw(df)
            ui_obj.set_df_current(df)
            label_df_config.configure(text="Total rows: {}".format(len(ui_obj.get_df_raw().index))) 
            # ui_obj.set_df_new(df)
            button_generate_preview.configure(state=tk.ACTIVE)
            button_generate_preview.configure(text="Generate preview")
            button_entry_number_of_rows_in_preview.configure(state=tk.ACTIVE)
            scale_number_of_rows_in_preview.configure(
                state=tk.ACTIVE,
                to=len(ui_obj.get_df_raw().index)
                )
            entry_number_of_rows_in_preview.delete(0, tk.END)
            entry_number_of_rows_in_preview.insert(0, ui_obj.get_number_of_rows_in_preview())
            checkbutton_groupby.configure(state=tk.ACTIVE)
            ui_obj.set_list_menu_groupby(ui_obj.get_df_raw().columns)
            ui_obj.add_checkbuttons_menubutton(
                menubutton_groupby,
                ui_obj.get_list_menu_groupby()
                # ui_obj.dict_menubutton_values
            )
            button_generate_group_by.configure(state=tk.ACTIVE)
            print(path_folder)
            print(path_file)
            print(size_file)
        except Exception as e:
            print(e)
            label_path_file.configure(text=str(e))
    else:
        print("EEEEEE")
    

def generate_preview(df_preview=None):
    # df_preview = ui_obj.get_df_raw().head(ui_obj.get_number_of_rows_in_preview())
    # df_preview = ui_obj.get_df_raw()
    # print(ui_obj.get_number_of_rows_in_preview())
    # print(df_preview.head(3))
    if(df_preview is None):
        df = ui_obj.get_df_raw().head(ui_obj.get_number_of_rows_in_preview_default())
        reset_raw()
    else:
        # print("Here")
        number_of_rows_preview = ui_obj.get_number_of_rows_in_preview()
        # print(type(number_of_rows_preview), number_of_rows_preview)
        df = df_preview.head(number_of_rows_preview)
        # print("Here_1")
    table_raw_data = Table(frame_raw_data, dataframe=df, showtoolbar=True, showstatusbar=True)
    table_raw_data.redraw()
    table_raw_data.show()
    # Update the label showing total number of rows
    # label_df_config.configure(text="Total rows: {}".format(len(df.index)))


button_exit = ui_obj.set_properties(tk.Button(frame_status), text="EXIT", state=tk.ACTIVE, command=exit)
button_exit.pack(side=tk.RIGHT)


button_select_file = ui_obj.set_properties(
    tk.Button(frame_raw_data_widgets), 
    text="Select File", 
    state=tk.ACTIVE, 
    command=load_file_path
)
# button_select_file.pack_propagate(0)
# button_select_file.pack(side=TOP, expand=False, anchor="w")
button_select_file.grid(row=0, column=0)

button_generate_preview = ui_obj.set_properties(
    tk.Button(frame_raw_data_widgets), 
    text="Generate preview", 
    command=generate_preview
)
# button_generate_preview.pack_propagate(0)
# button_generate_preview.pack(side=TOP, expand=False, anchor="w")
button_generate_preview.grid(row=1, column=0)

button_change_delimiter = ui_obj.set_properties(
    tk.Button(frame_raw_data_widgets), 
    text="Update delimiter"
)
button_change_delimiter.grid(row=1, column=2)


def generate_groupby():
    dict_groupby_menubutton_raw = ui_obj.dict_agg_command_pre
    dict_temp = {}
    for agg, dict_ in dict_groupby_menubutton_raw.items():
        for key, value in dict_.items():
            if(value.get() == 1):
                if(key not in dict_temp):
                    dict_temp[key] = []
                dict_temp[key].append(agg)
    
    list_labels_group = [key_ for key_, value_ in ui_obj.get_dict_menubutton_values().items() if value_==1]
    df = ui_obj.get_df_raw()
    list_columns_display = [key for key in dict_temp.keys()]
    df = df.groupby(list_labels_group).agg(dict_temp).reset_index()
    button_generate_preview.configure(text="Reset")
    generate_preview(df)

button_generate_group_by = ui_obj.set_properties(
    tk.Button(frame_raw_data_widgets),
    text="Group",
    command=generate_groupby
)
button_generate_group_by.grid(row=2, column=3, sticky="nw")

def change_rows_table_entry(number_of_rows_in_preview=None):
    if(number_of_rows_in_preview is not None and number_of_rows_in_preview.isdigit()):
        entry_number_of_rows_in_preview.configure(bg="Green")
        ui_obj.set_number_of_rows_in_preview(int(number_of_rows_in_preview))
        ui_obj.set_df_current(ui_obj.get_df_current())
        button_generate_preview.configure(text="Reset")
        generate_preview(ui_obj.get_df_current())
        # time.sleep(5)
        # entry_number_of_rows_in_preview.configure(bg="White")
    else:
        entry_number_of_rows_in_preview.configure(bg="Red")

button_entry_number_of_rows_in_preview = ui_obj.set_properties(
    tk.Button(frame_raw_data_widgets),
    text="Preview",
    command= lambda: change_rows_table_entry(entry_number_of_rows_in_preview.get())
)
button_entry_number_of_rows_in_preview.grid(row=0, column=3)

button_generate_dataset = ui_obj.set_properties(
    tk.Button(frame_dataset_widgets), 
    text="Generate dataset"
)
button_generate_dataset.pack()


"""
Canvases
"""




"""
Listboxes
"""

"""
Menubuttons
"""
menubutton_groupby = ui_obj.set_properties(
    tk.Menubutton(frame_raw_data_widgets),
    text="Group By"
)
# menubutton_groupby = ui_obj.add_checkbuttons_menubutton(
#     menubutton_groupby, 
#     ui_obj.get_list_menu_groupby(),
#     ui_obj.dict_menubutton_values
# )
menubutton_groupby.grid(row=2, column=1, sticky="nw")


"""
Menus
"""

"""
Messages
"""

"""
Radiobuttons
"""

"""
Scales
"""
var_scale = tk.IntVar()
var_scale.set(ui_obj.get_number_of_rows_in_preview())
# scale_number_of_rows_in_preview = Scale(
#     frame_raw_main,
#     from_=0,
#     to=len(ui_obj.get_df_raw.index),
#     variable=var_scale,
#     orient=
# )
def change_rows_table_scale(number_of_rows_in_preview):
    ui_obj.set_number_of_rows_in_preview(int(number_of_rows_in_preview))
    ui_obj.set_df_current(ui_obj.get_df_current().head(ui_obj.get_number_of_rows_in_preview()))
    button_generate_preview.configure(text="Reset")
    generate_preview(ui_obj.get_df_current())
    return

scale_number_of_rows_in_preview = ui_obj.set_properties(
    tk.Scale(frame_raw_data_widgets),
    label="Rows",
    width=15,
    from_=0,
    to=100,
    variable=var_scale,
    cursor=ui_obj.get_number_of_rows_in_preview(),
    orient="horizontal",
    command=change_rows_table_scale,
    state="disabled"
)
# scale_number_of_rows_in_preview.grid(row=0, column=3)

"""
Scrollbars
"""

"""
Texts
"""

"""
CheckButtons
"""
def trigger_groupby_options(state_checkbutton):
    if(state_checkbutton == 1):
        menubutton_groupby.configure(state=tk.ACTIVE)

    else:
        menubutton_groupby.configure(state=tk.DISABLED)
        # ui_obj.get_list_menu_groupby()
        # ui_obj.dict_agg_command_pre
        # ui_obj.set_list_menu_groupby([])
        ui_obj.set_dict_menubutton_values({key: 0 for key in ui_obj.get_dict_menubutton_values().keys()})
        for agg, dict_ in ui_obj.dict_agg_command_pre.items():
            for key, value in dict_.items():
                ui_obj.dict_agg_command_pre[agg][key] = None



var_checkbutton = tk.IntVar()
checkbutton_groupby = ui_obj.set_properties(
    tk.Checkbutton(frame_raw_data_widgets),
    text="Group By?",
    variable=var_checkbutton,
    command=lambda: trigger_groupby_options(var_checkbutton.get()),
)
checkbutton_groupby.grid(row=2, column=0, sticky="nw")


"""
tkMessageBoxes
"""


root.mainloop()
