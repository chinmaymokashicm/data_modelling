import tkinter as tk


"""
Entries
"""
def generate(root, ui_obj):
    entry_number_of_rows_in_preview = ui_obj.set_properties(
        tk.Entry(ui_obj.frame_raw_data_widgets),
        textvariable=tk.StringVar(),
        state=tk.NORMAL
    )
    # entry_number_of_rows_in_preview.configure(command=change_rows_table_entry)
    entry_number_of_rows_in_preview.grid(row=0, column=2)

    ui_obj.entry_number_of_rows_in_preview = entry_number_of_rows_in_preview

    return([root, ui_obj])