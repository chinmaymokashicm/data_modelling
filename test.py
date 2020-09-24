import tkinter as tk
from tkinter import ttk
from modules import window, frame, button, label, menubutton, entry
from modules.properties import Properties
import pandas as pd
import numpy as np

class Application:
    def __init__(self):
        self.properties = Properties()
        self.window_main = window.Window("main", title="Data Reader")
        self.generate_frames()
        self.generate_widgets()
        
        # self.window_main.mainloop()
        
    def generate_frames(self):
        self.frame_main = frame.Frame(self.window_main).widget
        self.frame_widgets = frame.Frame(self.frame_main).widget
        self.frame_view = frame.Frame(self.frame_main).widget
        self.frame_options = frame.Frame(self.window_main).widget

        self.frame_main.place(
            relwidth=self.properties.frame["main"]["widgets"]["relwidth"],
            relheight=1 - self.properties.frame["options"]["relheight"],
            relx=0,
            rely=0
        )
        self.frame_widgets.place(
            relwidth=self.properties.frame["main"]["widgets"]["relwidth"],
            relheight=self.properties.frame["main"]["widgets"]["relheight"],
            relx=0,
            rely=0
        )
        self.frame_view.place(
            relwidth=self.properties.frame["main"]["view"]["relwidth"],
            relheight=self.properties.frame["main"]["view"]["relheight"],
            relx=0,
            rely=self.properties.frame["main"]["widgets"]["relheight"]
        )
        self.tab_controller = ttk.Notebook(self.frame_view)
        self.dict_tabs = {}
        for tab_name in self.properties.list_tab_names:
            self.dict_tabs[tab_name] = ttk.Frame(self.tab_controller)
            self.tab_controller.add(self.dict_tabs[tab_name], text=tab_name[0].upper() + str(tab_name[1:]))
        self.tab_controller.pack(expand=1, fill=tk.BOTH)


        self.frame_options.place(
            relwidth=self.properties.frame["options"]["relwidth"],
            relheight=self.properties.frame["options"]["relheight"],
            relx=0,
            rely=1 - self.properties.frame["options"]["relheight"]
        )

    def open_new_window(self, **properties):
        self.new_window = tk.Toplevel(self.window_main)
        self.new_window.geometry("200x100")
    

    def _buttons(self):
        # All the buttons here
        self.button_select_file = button.Button(
            self.frame_widgets, 
            text="Select file",
            # command=self.open_new_window,
            state=tk.ACTIVE
        ).widget
        self.button_reset_data = button.Button(
            self.frame_widgets,
            text="Reset"
        ).widget
        self.button_filter_columns = button.Button(
            self.frame_widgets,
            text="Filter Columns"
        ).widget
        self.button_where_condition = button.Button(
            self.frame_widgets,
            text="WHERE"
        ).widget
        self.button_groupby = button.Button(
            self.frame_widgets,
            text="Group By"
        ).widget
        self.button_change_dtype = button.Button(
            self.frame_widgets,
            text="Change DType"
        ).widget
        self.button_view = button.Button(
            self.frame_widgets,
            text="View"
        ).widget
        self.button_sort = button.Button(
            self.frame_widgets,
            text="Sort"
        ).widget
        self.button_describe = button.Button(
            self.frame_widgets,
            text="Describe"
        ).widget
        self.button_get_na = button.Button(
            self.frame_widgets,
            text="Get NA"
        ).widget
        self.button_fill_na = button.Button(
            self.frame_widgets,
            text="Fill NA"
        ).widget
        self.button_transform_column = button.Button(
            self.frame_widgets,
            text="Transform"
        ).widget
        self.button_reload = button.Button(
            self.frame_widgets,
            text="Reload"
        ).widget
        self.button_close = button.Button(
            self.frame_options,
            text="Close",
            command=exit
        ).widget

    def _labels(self):
        # All the labels here
        self.label_info = label.Label(
            self.frame_widgets,
            text="Data information"
        ).widget

    def _menubuttons(self):
        # All the menubuttons
        self.menubutton_view_options = menubutton.MenuButton(
            self.frame_widgets,
            text="View Options"
        ).widget
    
    def _entries(self):
        # All the entries
        self.entry_preview_number_of_rows = entry.Entry(
            self.frame_widgets
        ).widget

    """
    Listing all the widgets
    select_file      view_options    reset_data        preview_number_of_rows  -->| |\  | |---- |---|
    filter_columns   where           groupby           change_dtype               | | \ | |--   |   |
    sort             describe        Transform         Reload                     | |  \| |     |---|
    """

    def generate_widgets(self):
        self._buttons()
        self._labels()
        self._menubuttons()
        self._entries()
        self.list_widgets = [
            [self.button_select_file, self.menubutton_view_options, self.button_reset_data, self.entry_preview_number_of_rows, self.label_info],
            [self.button_filter_columns, self.button_where_condition, self.button_groupby, self.button_change_dtype, None],
            [self.button_sort, self.button_describe, self.button_transform_column, self.button_reload, None]
        ]
        for row_number in range(len(self.list_widgets)):
            for column_number in range(len(self.list_widgets[row_number])):
                if(row_number == 0 and column_number == 4):
                    self.list_widgets[row_number][column_number].place(
                        relwidth=1/self.properties.number_of_columns_widgets,
                        relheight=1/self.properties.number_of_rows_widgets * 3,
                        relx=1/self.properties.number_of_columns_widgets * column_number,
                        rely=1/self.properties.number_of_rows_widgets * row_number
                    )
                else:
                    if(self.list_widgets[row_number][column_number] is not None):
                        self.list_widgets[row_number][column_number].place(
                            relwidth=1/self.properties.number_of_columns_widgets,
                            relheight=1/self.properties.number_of_rows_widgets,
                            relx=1/self.properties.number_of_columns_widgets * column_number,
                            rely=1/self.properties.number_of_rows_widgets * row_number
                        )
        
        self.button_close.pack(side=tk.RIGHT, expand=0, fill=tk.Y)
        self.button_close.configure(state=tk.ACTIVE)


if(__name__ == "__main__"):
    Application()