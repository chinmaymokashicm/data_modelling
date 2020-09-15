import tkinter as tk


"""
Labels
"""
def generate(root, ui_obj):
    label_path_file = ui_obj.set_properties(
        tk.Label(ui_obj.frame_raw_data_widgets), 
        text="Select raw dataset",
        width=20
        )
    label_path_file.configure(anchor="c")
    label_path_file.grid(row=0, column=1)

    label_df_config = ui_obj.set_properties(
        tk.Label(ui_obj.frame_raw_data_widgets), 
        text="EMPTY",
        width=20
        )
    label_df_config.configure(anchor="c")
    label_df_config.grid(row=1, column=1)

    return([root, ui_obj])