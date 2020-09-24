# import test
from test import *
from modules import listbox
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import os
from pandastable import Table
import json
import pandas as pd
import numpy as np
from pprint import pformat

"""
Class containing the code to activate widgets
"""
class Activate(Application):
    def __init__(self):
        super().__init__()
        self.select_file()

        self.window_main.mainloop()

    def activate_widgets_trigger(self):
        try:
            list_widgets = self.frame_widgets.winfo_children()
            [widget.configure(state=tk.NORMAL) for widget in list_widgets]
            self.view_options()
            self.reset()
            self.preview_rows()
            self.filter_columns()
            self.where()
            self.groupby()
            self.change_dtype()
            self.sort()
            self.describe()
            self.transform()
            self._reload()
        except Exception as e:
            print(e)
            messagebox.showerror(title="Error activating widgets", message=e)
        
    def view_table_trigger(self, frame_tab_name=None, df=None, _preview=None):
        try:
            if(frame_tab_name is None):
                frame_tab_name = "processed"
            if(df is None):
                df = self.properties.df["processed"]
            
            # if(_filter is None):
            #     _filter = self.properties.dict_menubutton_view_options["filter"].get()
            # if(_filter == 1):
            #     list_columns = [
            #         column_name for column_name in df.columns.tolist() 
            #         if df.columns.tolist().index(column_name) in self.properties.list_listbox_filter_columns_indices
            #     ]
            #     if(len(list_columns) == 0):
            #         print("Empty...")
            #         list_columns = [column_name for column_name in df.columns.tolist()]
            #     df = df[list_columns]
            
            # if(_where is None):
            #     _where = self.properties.dict_menubutton_view_options["where"].get()
            # if(_where == 1):
            #     str_filter = self.properties.string_where_condition_filter
            #     # print(str_filter)
            #     if(str_filter is not None):
            #         if(len(str_filter) > 0):
            #             # df = df[str_filter]
            #             str_command = "out = df[{}]".format(str_filter)
            #             namespace = {}
            #             exec(str_command, {"df": df}, namespace)
            #             df = namespace["out"]

            # if(_groupby is None):
            #     _groupby = self.properties.dict_menubutton_view_options["groupby"].get()
            # if(_groupby == 1):
            #     list_columns_grouping_by = [
            #         column_name for column_name in df.columns.tolist() 
            #         if df.columns.tolist().index(column_name) in self.properties.list_listbox_groupby_columns_indices
            #     ]
            #     dict_agg = self.properties.dict_groupby_aggregations
            #     if(len(list_columns_grouping_by) != 0):
            #         df = df.groupby(list_columns_grouping_by).agg(dict_agg)

            self.properties.df[frame_tab_name] = df.copy(deep=True)
            if(_preview is None):
                _preview = self.properties.dict_menubutton_view_options["preview"].get()
            if(_preview == 1):
                df = df.head(self.intvar_preview_number_of_rows.get())

            table = Table(self.dict_tabs[frame_tab_name], dataframe=df, showtoolbar=True, showstatusbar=True)
            table.redraw()
            table.show()
            self.tab_controller.select(self.properties.list_tab_names.index(frame_tab_name))
            print("Viewing table in {}...".format(frame_tab_name))
        except Exception as e:
            tk.messagebox.showerror(title="Error displaying table", message=e)

    def select_file(self):
        def func():
            try:
                path_file = fd.askopenfilename(
                    initialdir=self.properties.default_directory,
                    title="Select raw dataset",
                    filetypes = (("CSV files","*.csv"),("TXT files","*.txt"))
                    )
                if(isinstance(path_file, str) and path_file !=""):
                    self.properties.default_dir = os.path.dirname(path_file)
                    # Activate everything 
                    self.activate_widgets_trigger()
                    self.properties.dict_menubutton_view_options["preview"].set(1)
                    # Load the table on the Raw Tab
                    self.properties.df["raw"] = pd.read_csv(path_file)
                    # Load the table on the Processed Tab
                    self.properties.df["processed"] = self.properties.df["raw"].copy(deep=True)

                    self.view_table_trigger("raw", self.properties.df["raw"])
                    self.view_table_trigger("processed", self.properties.df["processed"])
                else:
                    messagebox.showerror(title="Select File!", message="Did not select file")
                

            except Exception as e:
                print(e)
                messagebox.showerror(title="Error loading data", message=e)
  
        self.button_select_file.configure(command=func)
    
    def view_options(self):
        self.properties.dict_menubutton_view_options = self.properties.generate_menubutton_values(
            self.menubutton_view_options,
            self.properties.list_labels_view_options
        )
        # self.properties.dict_menubutton_view_options["preview"].set(1)
    
    def reset(self):
        # Reset everything
        def func():
            self.view_table_trigger(df=self.properties.df["raw"])

        self.button_reset_data.configure(command=func)
    
    def preview_rows(self):
        # Enter number of rows for preview
        self.intvar_preview_number_of_rows = tk.IntVar()
        self.entry_preview_number_of_rows.configure(textvariable=self.intvar_preview_number_of_rows)
        self.intvar_preview_number_of_rows.set(self.properties.number_of_rows_in_preview_default)
        
    def filter_columns(self):
        def func():
            def exit_window(save=False):
                if(save):
                    # if(all(column_name in list(self.listbox_filter_columns.curselection()) for column_name in self.properties.list_listbox_filter_columns_indices)):
                    #     # Do not change anything in groupby and other selections
                    #     print("Not updating")
                    #     pass
                    # else:
                    #     print("Updating..")
                    self.properties.list_listbox_groupby_columns_indices = []
                    self.properties.dict_groupby_aggregations = {}
                    self.properties.string_where_condition_filter = None
                    self.properties.list_list_sort_and_order =[[], []]
                    self.properties.list_listbox_filter_columns_indices = list(self.listbox_filter_columns.curselection())
                    tk.messagebox.showwarning(title="Warning", message="Every time you update columns to filter, all other parameters are reset.")
                    # Display the table
                    df = self.properties.df["processed"]
                    list_columns = [
                        column_name for column_name in df.columns.tolist() 
                        if df.columns.tolist().index(column_name) in self.properties.list_listbox_filter_columns_indices
                    ]
                    if(len(list_columns) == 0):
                        # print("Empty...")
                        list_columns = [column_name for column_name in df.columns.tolist()]
                    self.view_table_trigger(df=df[list_columns])
                    # Reset list of indices
                    self.properties.list_listbox_filter_columns_indices = []

                self.window_filter_columns.destroy()
                self.window_filter_columns.update()
            
            self.window_filter_columns = tk.Toplevel(
                self.window_main
            )
            self.window_filter_columns.title("Filter Columns")

            window_width = self.properties.window["popup"]["width"]
            window_height = self.properties.window["popup"]["height"]
            self.window_filter_columns.geometry("{}x{}".format(window_width, window_height))
            self.frame_filter_columns_main = frame.Frame(self.window_filter_columns).widget
            self.frame_filter_columns_names = frame.Frame(self.frame_filter_columns_main).widget
            self.frame_filter_columns_options = frame.Frame(self.frame_filter_columns_main).widget
            button_cancel = button.Button(
                self.frame_filter_columns_options, 
                state=tk.ACTIVE, 
                text="Cancel",
                command=exit_window
            ).widget
            button_select = button.Button(
                self.frame_filter_columns_options, 
                state=tk.ACTIVE, 
                text="Select", 
                command=lambda save=True: exit_window(save)
            ).widget
            button_reset = button.Button(
                self.frame_filter_columns_options, 
                state=tk.ACTIVE, 
                text="Reset", 
                command=lambda: self.listbox_filter_columns.select_clear(0, "end")
            ).widget
            
            self.frame_filter_columns_main.pack(expand=1, fill=tk.BOTH)
            self.frame_filter_columns_names.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.frame_filter_columns_options.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
            button_cancel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            button_select.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            button_reset.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

            # Set values to the listbox variable
            self.stringvar_listbox_filter_columns = tk.StringVar()
            self.listbox_filter_columns = listbox.ListBox(
                self.frame_filter_columns_main,
                listvariable=self.stringvar_listbox_filter_columns,
                selectmode=tk.EXTENDED
            ).widget
            self.stringvar_listbox_filter_columns.set(tuple(self.properties.df["processed"].columns))
            self.listbox_filter_columns.yview_scroll(5, tk.UNITS)
            # Set previously selected values
            self.listbox_filter_columns.select_clear(0, "end")
            for index in self.properties.list_listbox_filter_columns_indices:
                self.listbox_filter_columns.selection_set(index)
                self.listbox_filter_columns.see(index)
                self.listbox_filter_columns.activate(index)
                self.listbox_filter_columns.selection_anchor(index)

            self.listbox_filter_columns.pack(expand=1, fill=tk.BOTH)

        self.button_filter_columns.configure(command=func)
    
    def where(self):
        def func():
            def exit_window(save=False):
                if(save):
                    self.properties.string_where_condition_filter = self.stringvar_entry_where_filter.get()
                    str_filter = self.properties.string_where_condition_filter
                    df = self.properties.df["processed"]
                    if(str_filter is not None):
                        if(len(str_filter) > 0):
                            str_command = "out = df[{}]".format(str_filter)
                            namespace = {}
                            exec(str_command, {"df": df}, namespace)
                            df = namespace["out"]
                    self.view_table_trigger(df=df)
                self.window_where.destroy()
                self.window_where.update()
            
            def reset():
                self.entry_where_filter.delete(0, tk.END)
            
            def check():
                string_filter = self.stringvar_entry_where_filter.get()
                df = self.properties.df["processed"]
                string_command = "df[{}]".format(string_filter)
                # print(string_command)
                try:
                    exec(string_command, {}, {"df": df})
                    tk.messagebox.showinfo(title="Success", message="Filter string is valid")
                except Exception as e:
                    print(e)
                    tk.messagebox.showerror(title="Invalid filter string", message=e)

            def copy_column_name():
                index_insert_current = self.entry_where_filter.index(tk.INSERT)
                column_name = self.stringvar_combobox_where.get().split("|")[0].split(" ")[0]
                self.entry_where_filter.insert(index_insert_current, 'df["{}"]'.format(column_name))
                # print("Copied")

            self.window_where = tk.Toplevel(
                self.window_main
            )
            self.window_where.title("WHERE")
            window_width = self.properties.window["popup"]["width"]
            window_height = self.properties.window["popup"]["height"]
            self.window_where.geometry("{}x{}".format(window_width, window_height))
            self.frame_where_main = frame.Frame(self.window_where).widget
            self.frame_where_options = frame.Frame(self.window_where).widget
            self.label_ttk_column_select = ttk.Label(
                self.frame_where_main,
                text="Select Column"
            )
            self.stringvar_combobox_where = tk.StringVar()
            self.combobox_column_select = ttk.Combobox(
                self.frame_where_main,
                values=[
                    "{} | {}".format(
                        column_name, 
                        self.properties.df["processed"][column_name].dtype
                    ) 
                    for column_name in self.properties.df["processed"].columns.tolist()
                ],
                textvariable=self.stringvar_combobox_where
            )
            self.combobox_column_select.current(0)
            self.button_copy_column_name_where = button.Button(
                self.frame_where_main,
                text="Copy Column Name",
                state=tk.ACTIVE,
                command=copy_column_name
            ).widget
            self.stringvar_entry_where_filter = tk.StringVar()
            self.entry_where_filter = entry.Entry(
                self.frame_where_main,
                state=tk.NORMAL,
                textvariable=self.stringvar_entry_where_filter
            ).widget
            

            button_cancel = button.Button(
                self.frame_where_options,
                text="Cancel",
                command=exit_window,
                state=tk.ACTIVE
            ).widget
            button_select = button.Button(
                self.frame_where_options,
                text="Select",
                command=lambda save=True: exit_window(save),
                state=tk.ACTIVE
            ).widget
            button_check = button.Button(
                self.frame_where_options,
                text="Check",
                command=check,
                state=tk.ACTIVE
            ).widget
            button_reset = button.Button(
                self.frame_where_options,
                text="Reset",
                command=reset,
                state=tk.ACTIVE
            ).widget

            self.frame_where_main.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.frame_where_options.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
            self.label_ttk_column_select.pack(side=tk.TOP, expand=1, fill=tk.X)
            self.combobox_column_select.pack(side=tk.TOP, expand=1, fill=tk.X)
            self.button_copy_column_name_where.pack(side=tk.TOP, expand=1, fill=None)
            self.entry_where_filter.pack(side=tk.BOTTOM, expand=1, fill=tk.X, ipady=4)

            button_cancel.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            button_select.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            button_check.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            button_reset.pack(side=tk.RIGHT, expand=False, fill=tk.Y)

            self.entry_where_filter.delete(0, tk.END)
            self.entry_where_filter.insert(0, self.properties.string_where_condition_filter)


        self.button_where_condition.configure(command=func)

    def groupby(self):
        # Group by functionality
        def func():
            self.window_groupby = tk.Toplevel(
                self.window_main
            )
            self.window_groupby.title("Group By")
            window_width = self.properties.window["popup"]["width"] * 2
            window_height = self.properties.window["popup"]["height"]
            self.window_groupby.geometry("{}x{}".format(window_width, window_height))
            self.frame_groupby_columns_main = frame.Frame(self.window_groupby).widget
            self.frame_groupby_columns_names = frame.Frame(self.frame_groupby_columns_main).widget
            self.frame_groupby_columns_options= frame.Frame(self.frame_groupby_columns_main).widget
            self.frame_groupby_aggregations_main = frame.Frame(self.window_groupby).widget
            self.frame_groupby_aggregations_names = frame.Frame(self.frame_groupby_aggregations_main).widget
            self.frame_groupby_aggregations_options = frame.Frame(self.frame_groupby_aggregations_main).widget

            self.frame_groupby_columns_main.place(relwidth=1/2, relheight=1, relx=0, rely=0)
            self.frame_groupby_columns_names.place(relwidth=1, relheight=0.95, relx=0, rely=0)
            self.frame_groupby_columns_options.place(relwidth=1, relheight=0.05, relx=0, rely=0.95)
            self.frame_groupby_aggregations_main.place(relwidth=1/2, relheight=1, relx=1/2, rely=0)
            self.frame_groupby_aggregations_names.place(relwidth=1, relheight=0.95, relx=0, rely=0)
            self.frame_groupby_aggregations_options.place(relwidth=1, relheight=0.05, relx=0, rely=0.95)

            """
            Group by column names
            """
            self.scrollbar_listbox_groupby_column_names_yview = tk.Scrollbar(self.frame_groupby_columns_names)

            self.stringvar_listbox_groupby_columns = tk.StringVar()
            self.listbox_groupby_columns = listbox.ListBox(
                self.frame_groupby_columns_names,
                listvariable=self.stringvar_listbox_groupby_columns,
                selectmode=tk.EXTENDED,
                yscrollcommand= self.scrollbar_listbox_groupby_column_names_yview.set
            ).widget
            self.stringvar_listbox_groupby_columns.set(tuple(self.properties.df["processed"].columns))
            self.scrollbar_listbox_groupby_column_names_yview.config(command=self.listbox_groupby_columns.yview)
            self.scrollbar_listbox_groupby_column_names_yview.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Set previous values
            self.listbox_groupby_columns.select_clear(0, "end")
            for index in self.properties.list_listbox_groupby_columns_indices:
                self.listbox_groupby_columns.selection_set(index)
                self.listbox_groupby_columns.see(index)
                self.listbox_groupby_columns.activate(index)
                self.listbox_groupby_columns.selection_anchor(index)
            
            
            self.listbox_groupby_columns.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

            """
            Aggregations
            """
            self.label_ttk_column_select_agg = ttk.Label(
                self.frame_groupby_aggregations_names,
                text="Select Column"
            )
            self.stringvar_combobox_agg = tk.StringVar()
            def check_for_custom(event):
                if(self.stringvar_combobox_agg_function.get() == "custom"):
                    self.entry_add_agg.configure(state=tk.NORMAL)
                    self.entry_add_agg.configure(bg="White")
                else:
                    self.entry_add_agg.configure(state=tk.DISABLED)
                    self.entry_add_agg.configure(bg="Pink")

            self.combobox_column_select_agg = ttk.Combobox(
                self.frame_groupby_aggregations_names,
                values=[],
                textvariable=self.stringvar_combobox_agg
            )
            self.stringvar_combobox_agg_function = tk.StringVar()
            self.combobox_column_select_agg_function = ttk.Combobox(
                self.frame_groupby_aggregations_names,
                values=self.properties.list_groupby_aggregations,
                textvariable=self.stringvar_combobox_agg_function
            )
            self.combobox_column_select_agg_function.current(0)
            self.combobox_column_select_agg_function.bind("<<ComboboxSelected>>", check_for_custom)
            def add_agg():
                column_name = self.stringvar_combobox_agg.get().split("|")[0].split(" ")[0]
                if(column_name not in self.properties.dict_groupby_aggregations.keys()):
                    self.properties.dict_groupby_aggregations[column_name] = []
                agg = self.stringvar_combobox_agg_function.get()
                if(agg != "custom"):
                    if(agg not in self.properties.dict_groupby_aggregations[column_name]):
                        self.properties.dict_groupby_aggregations[column_name].append(agg)
                
                str_dict = json.dumps(self.properties.dict_groupby_aggregations, indent=2)
                self.label_show_aggregation.configure(text=str_dict, justify=tk.LEFT)
            self.button_add_agg = button.Button(
                self.frame_groupby_aggregations_names,
                text="Add Aggregation",
                command=add_agg
            ).widget
            def reset_agg_dict():
                self.properties.dict_groupby_aggregations = {}
                str_dict = json.dumps(self.properties.dict_groupby_aggregations, indent=2)
                self.label_show_aggregation.configure(text=str_dict, justify=tk.LEFT)
            self.button_reset_agg_dict = button.Button(
                self.frame_groupby_aggregations_names,
                text="Reset",
                command=reset_agg_dict
            ).widget
            self.stringvar_entry_agg = tk.StringVar()
            self.entry_add_agg = entry.Entry(
                self.frame_groupby_aggregations_names,
                state=tk.DISABLED,
                textvariable=self.stringvar_entry_agg,
                relief=tk.FLAT,
                borderwidth=15,
                bg="Pink"
            ).widget
            self.label_show_aggregation = label.Label(
                self.frame_groupby_aggregations_names,
                text=json.dumps(self.properties.dict_groupby_aggregations, indent=2),
                justify=tk.LEFT
            ).widget

            self.label_ttk_column_select_agg.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.combobox_column_select_agg.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.combobox_column_select_agg_function.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.entry_add_agg.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.button_add_agg.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.button_reset_agg_dict.pack(side=tk.TOP, expand=False, fill=tk.X)
            self.label_show_aggregation.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            
            """
            Options for groupby column names
            """
            def select_columns_groupby():
                self.properties.list_listbox_groupby_columns_indices = list(self.listbox_groupby_columns.curselection())
                list_columns_for_agg = [
                    "{} | {}".format(
                        column_name, 
                        self.properties.df["processed"][column_name].dtype
                    ) 
                    for column_name in self.properties.df["processed"].columns.tolist() 
                    if self.properties.df["processed"].columns.tolist().index(column_name) not in self.properties.list_listbox_groupby_columns_indices
                ]
                if(len(self.properties.df["processed"].columns.tolist()) != len(list_columns_for_agg)):
                    self.combobox_column_select_agg.configure(values=list_columns_for_agg)
                    self.combobox_column_select_agg.current(0)
                    self.button_add_agg.configure(state=tk.ACTIVE)
                    self.button_reset_agg_dict.configure(state=tk.ACTIVE)
                    # self.button_check_aggregation.configure(state=tk.ACTIVE)
                else:
                    self.combobox_column_select_agg.configure(values=[])
                    self.combobox_column_select_agg.set("")
                    self.button_add_agg.configure(state=tk.DISABLED)
                    self.button_reset_agg_dict.configure(state=tk.DISABLED)
                    # self.button_check_aggregation.configure(state=tk.DISABLED)
                    
                
            self.button_groupby_columns_select = button.Button(
                self.frame_groupby_columns_options,
                text="Select Columns",
                state=tk.ACTIVE,
                command=select_columns_groupby
            ).widget
            self.button_groupby_columns_reset = button.Button(
                self.frame_groupby_columns_options,
                text="Reset",
                state=tk.ACTIVE,
                command=lambda: self.listbox_groupby_columns.select_clear(0, "end")
            ).widget
            self.button_groupby_columns_select.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            self.button_groupby_columns_reset.pack(side=tk.RIGHT, expand=False, fill=tk.Y)

            """
            Options for Groupby aggregations
            """
            def check_aggregation():
                df = self.properties.df["processed"]
                list_columns_grouping_by = [
                    column_name for column_name 
                    in df.columns.tolist() 
                    if df.columns.tolist().index(column_name) not in self.properties.list_listbox_groupby_columns_indices
                ]
                dict_agg = self.properties.dict_groupby_aggregations
                try:
                    df_checking = df[list_columns_grouping_by].agg(dict_agg)
                    tk.messagebox.showinfo(title="Success", message="Filtered string works!")
                except Exception as e:
                    tk.messagebox.showerror(title="Error", message=e)
            self.button_check_aggregation = button.Button(
                self.frame_groupby_aggregations_options,
                text="Check",
                state=tk.ACTIVE,
                command=check_aggregation
            ).widget
            def select():
                df = self.properties.df["processed"]
                list_columns_grouping_by = [
                    column_name for column_name in df.columns.tolist() 
                    if df.columns.tolist().index(column_name) in self.properties.list_listbox_groupby_columns_indices
                ]
                dict_agg = self.properties.dict_groupby_aggregations
                if(len(list_columns_grouping_by) != 0):
                    df = df.groupby(list_columns_grouping_by).agg(dict_agg).reset_index()
                    df.columns = ["_".join(x) for x in df.columns.ravel()]
                    self.view_table_trigger(df=df)
                self.window_groupby.destroy()
                self.window_groupby.update()
            self.button_select_aggregation_window = button.Button(
                self.frame_groupby_aggregations_options,
                text="Select",
                state=tk.ACTIVE,
                command=select
            ).widget
            def close():
                self.window_groupby.destroy()
                self.window_groupby.update()
            self.button_close_aggregation = button.Button(
                self.frame_groupby_aggregations_options,
                text="Close",
                state=tk.ACTIVE,
                command=close
            ).widget
            self.button_close_aggregation.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            self.button_select_aggregation_window.pack(side=tk.RIGHT, expand=False, fill=tk.Y)
            self.button_check_aggregation.pack(side=tk.RIGHT, expand=False, fill=tk.Y)

        self.button_groupby.configure(command=func)

    def change_dtype(self):
        def func():
            self.window_change_dtype = tk.Toplevel(
                self.window_main
            )
            self.window_change_dtype.title("Filter Columns")

            window_width = self.properties.window["popup"]["width"]
            window_height = int(self.properties.window["popup"]["height"] * 0.5)
            self.window_change_dtype.geometry("{}x{}".format(window_width, window_height))
            self.label_ttk_column_select_change_dtype = ttk.Label(
                self.window_change_dtype,
                text="Select Column"
            )

            self.stringvar_combobox_dtype_column = tk.StringVar()
            df = self.properties.df["processed"]
            self.combobox_column_select_change_dtype = ttk.Combobox(
                self.window_change_dtype,
                values=[
                    "{} | {}".format(
                        column_name, 
                        self.properties.df["processed"][column_name].dtype
                    )
                    for column_name in df.columns.tolist()
                ],
                textvariable=self.stringvar_combobox_dtype_column
            )
            
            self.stringvar_combobox_dtype = tk.StringVar()
            self.combobox_select_dtype = ttk.Combobox(
                self.window_change_dtype,
                values= self.properties.list_dtypes,
                textvariable=self.stringvar_combobox_dtype
            )

            def change():
                column_name = self.stringvar_combobox_dtype_column.get().split("|")[0].split(" ")[0]
                old_dtype = self.stringvar_combobox_dtype_column.get().split("|")[-1].split(" ")[-1]
                new_dtype = self.stringvar_combobox_dtype.get()
                try:
                    if(new_dtype.find("datetime") != -1):
                        _format = new_dtype.split("|")[1].split(" ")[1]
                        _precision = new_dtype.split("|")[2].split(" ")[1]
                        self.properties.df["processed"][column_name] = pd.to_datetime(self.properties.df["processed"][column_name])
                        self.properties.df["processed"][column_name] = pd.to_datetime(self.properties.df["processed"][column_name], format=_format)
                        if(_precision not in ["date", "day", "week", "dayofweek", "time", "year"]):
                            self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].astype("datetime64[{}]".format(_precision))
                        else:
                            if(_precision == "date"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.date
                            elif(_precision == "day"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.day
                            elif(_precision == "week"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.week
                            elif(_precision == "dayofweek"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.dayofweek
                            elif(_precision == "time"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.time
                            elif(_precision == "year"):
                                self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].dt.year
                            else:
                                print("Datetime option N.A.")


                    else:
                        self.properties.df["processed"][column_name] = self.properties.df["processed"][column_name].astype(new_dtype)
                    tk.messagebox.showinfo(title="Success", message="DType of {} changed from {} to {}".format(column_name, old_dtype, new_dtype))
                    list_columns_and_dtypes = [
                        "{} | {}".format(
                            column_name, 
                            self.properties.df["processed"][column_name].dtype
                        )
                        for column_name in self.properties.df["processed"].columns.tolist()
                    ]
                    self.combobox_column_select_change_dtype.configure(values=list_columns_and_dtypes)
                    self.combobox_column_select_change_dtype.current(0)
                except Exception as e:
                    tk.messagebox.showerror(title="Error", message=e)
            self.button_change_dtype = button.Button(
                self.window_change_dtype,
                text="Change DType",
                state=tk.ACTIVE,
                command=change
            ).widget

            def close():
                self.view_table_trigger(df=self.properties.df["processed"])
                self.window_change_dtype.destroy()
                self.window_change_dtype.update()

            self.button_close_window_dtype = button.Button(
                self.window_change_dtype,
                text="Close",
                state=tk.ACTIVE,
                command=close
            ).widget

            self.label_ttk_column_select_change_dtype.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_column_select_change_dtype.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_select_dtype.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_change_dtype.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_close_window_dtype.pack(side=tk.TOP, fill=tk.X, expand=False)

            self.combobox_column_select_change_dtype.current(0)
            self.combobox_select_dtype.current(0)


        self.button_change_dtype.configure(command=func)

    def sort(self):
        def func():
            self.window_sort = tk.Toplevel(
                self.window_main
            )
            self.window_sort.title("Sort")
            window_width = self.properties.window["popup"]["width"]
            window_height = self.properties.window["popup"]["height"]
            self.window_sort.geometry("{}x{}".format(window_width, window_height))
            # Label
            self.label_sort_select_column = ttk.Label(
                self.window_sort,
                text="Select Column"
            )
            # Combobox column
            self.stringvar_combobox_sort_column_select = tk.StringVar()
            self.combobox_sort_column_select = ttk.Combobox(
                self.window_sort,
                values=self.properties.df["processed"].columns.tolist(),
                textvariable=self.stringvar_combobox_sort_column_select
            )
            # Combobox sorting order
            self.stringvar_combobox_sort_order = tk.StringVar()
            self.combobox_sort_order = ttk.Combobox(
                self.window_sort,
                values=["Ascending", "Descending"],
                textvariable=self.stringvar_combobox_sort_order
            )
            # Button to add
            def add():
                column_name = self.stringvar_combobox_sort_column_select.get()
                order = self.stringvar_combobox_sort_order.get()
                if(column_name in self.properties.list_list_sort_and_order[0]):
                    index_column_name = self.properties.list_list_sort_and_order[0].index(column_name)
                    self.properties.list_list_sort_and_order[1][index_column_name] = True if order == "Ascending" else False
                else:
                    self.properties.list_list_sort_and_order[0].append(column_name)
                    self.properties.list_list_sort_and_order[1].append(True if order == "Ascending" else False)
                self.label_show_sort.configure(text=display())
            self.button_add_sort = button.Button(
                self.window_sort,
                state=tk.ACTIVE,
                text="Add",
                command=add
            ).widget
            # Button to reset
            def reset():
                self.properties.list_list_sort_and_order =[[], []]
                self.label_show_sort.configure(text=display())
            self.button_reset_sort = button.Button(
                self.window_sort,
                state=tk.ACTIVE,
                text="Reset",
                command=reset
            ).widget
            # Button to close
            def close():
                list_sort = self.properties.list_list_sort_and_order
                if(len(list_sort[0]) > 0):
                    self.properties.df["processed"] = self.properties.df["processed"].sort_values(list_sort[0], ascending=list_sort[1])
                self.view_table_trigger()
                self.window_sort.destroy()
                self.window_sort.update()
            self.button_close_sort = button.Button(
                self.window_sort,
                state=tk.ACTIVE,
                text="Close",
                command=close
            ).widget
            # Label for display
            def display():
                label_string = "" if(len(self.properties.list_list_sort_and_order[0]) == 0) else [] 
                for index in range(len(self.properties.list_list_sort_and_order[0])):
                    label_string.append("{}: {}".format(
                        self.properties.list_list_sort_and_order[0][index],
                        "Ascending" if self.properties.list_list_sort_and_order[1][index] else "Descending"
                    ))
                if(isinstance(label_string, str)):
                    out = label_string
                else:
                    out = "\n".join(label_string)
                return(out)
            self.label_show_sort = label.Label(
                self.window_sort,
                text=display()
            ).widget

            # Packing
            self.label_sort_select_column.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_sort_column_select.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_sort_order.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_add_sort.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_reset_sort.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_close_sort.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.label_show_sort.pack(side=tk.TOP, fill=tk.X, expand=False)

            # Setting values
            self.combobox_sort_column_select.current(0)
            self.combobox_sort_order.current(0)



        self.button_sort.configure(command=func)

    def describe(self):
        def func():
            df = self.properties.df["processed"].describe()
            df.insert(0, "Attribute", ["count", "mean", "std", "min", "25%", "50%", "75%", "max"], True)
            self.view_table_trigger(frame_tab_name="describe", df=df)
        
        self.button_describe.configure(command=func)

    def transform(self):
        def func():
            # Window
            self.window_transform = tk.Toplevel(
                self.window_main
            )
            self.window_transform.title("Transform")
            window_width = self.properties.window["popup"]["width"] * 2
            window_height = self.properties.window["popup"]["height"]
            self.window_transform.geometry("{}x{}".format(window_width, window_height))

            # Frames
            self.frame_transform_main = frame.Frame(self.window_transform).widget
            self.frame_transform_options = frame.Frame(self.window_transform).widget

            # Widgets
            self.label_ttk_column_select_transform = ttk.Label(
                self.frame_transform_main,
                text="Select Column"
            )
            self.stringvar_combobox_select_column_transform = tk.StringVar()
            self.combobox_column_select_transform = ttk.Combobox(
                self.frame_transform_main,
                values=self.properties.df["processed"].columns.tolist(),
                textvariable=self.stringvar_combobox_select_column_transform
            )
            # def add_column_name_to_text(event):
            #     string_complete_expression = self.text_transform_function.get("1.0", tk.END)
            #     try:
            #         string_expression = str(string_complete_expression.split("=")[1:])
            #     except Exception:
            #         string_expression = str(self.properties.string_default_text_transform_function.split("=")[1:])
            #     column_name = self.combobox_column_select_transform.get()
            #     string_complete_expression = 'df["{}"] = '.format(column_name) + string_expression
            #     self.text_transform_function.delete("1.0", tk.END)
            #     self.text_transform_function.insert("1.0", string_complete_expression)

            # self.combobox_column_select_transform.bind("<<ComboboxSelected>>", add_column_name_to_text)
            self.label_ttk_column_transform_copy_column = ttk.Label(
                self.frame_transform_main,
                text="Copy Column to function"
            )
            self.stringvar_combobox_copy_column_transform = tk.StringVar()
            self.combobox_column_copy_transform = ttk.Combobox(
                self.frame_transform_main,
                values=self.properties.df["processed"].columns.tolist(),
                textvariable=self.stringvar_combobox_copy_column_transform
            )
            def copy_column():
                column_name = self.stringvar_combobox_copy_column_transform.get()
                self.text_transform_function.insert(tk.INSERT, 'row["{}"]'.format(column_name))
            self.button_copy_column_name_transform = button.Button(
                self.frame_transform_main,
                text="Copy column",
                command=copy_column,
                state=tk.ACTIVE
            ).widget
            self.text_transform_function = tk.Text(
                self.frame_transform_main,
                height=10,
                undo=True
            )
            self.text_transform_function.insert("1.0", self.properties.string_default_text_transform_function)

            def close_window():
                self.window_transform.destroy()
                self.window_transform.update()

            self.button_close_window_transform = button.Button(
                self.frame_transform_options,
                text="Close",
                command=close_window,
                state=tk.ACTIVE
            ).widget


            def select():
                string_transform = self.text_transform_function.get("1.0", tk.END)
                df = self.properties.df["processed"]
                string_command = "series = {}".format(string_transform)
                try:
                    # exec(string_command, {}, {"df": df})
                    namespace = {}
                    exec(string_command, {"df": df, "np": np, "pd": pd}, namespace)
                    self.properties.df["processed"][self.combobox_column_select_transform.get()] = namespace["series"]
                    close_window()
                    self.view_table_trigger()
                except Exception as e:
                    tk.messagebox.showerror(title="Error transforming data", message=e)

            self.button_select_transform = button.Button(
                self.frame_transform_options,
                text="Select",
                command=select,
                state=tk.ACTIVE
            ).widget

                    
            def check():
                try:
                    string_transform = self.text_transform_function.get("1.0", tk.END)
                    df = self.properties.df["processed"]
                    string_command = "{}".format(string_transform)
                    exec(string_command, {"df": df, "np": np, "pd": pd})
                    tk.messagebox.showinfo(title="Success", message="Transformation string is valid!")
                except Exception as e:
                    tk.messagebox.showerror(title="Error transforming data", message=e)

            self.button_check_transform = button.Button(
                self.frame_transform_options,
                text="Check",
                command=check,
                state=tk.ACTIVE
            ).widget

            # Packing
            self.frame_transform_main.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.frame_transform_options.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
            self.label_ttk_column_select_transform.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_column_select_transform.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.label_ttk_column_transform_copy_column.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.combobox_column_copy_transform.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_copy_column_name_transform.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.text_transform_function.pack(side=tk.TOP, fill=tk.X, expand=False)
            self.button_close_window_transform.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            self.button_check_transform.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            self.button_select_transform.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

            # Selecting current
            self.combobox_column_select_transform.current(0)
            self.combobox_column_copy_transform.current(1)

        self.button_transform_column.configure(command=func)

    def _reload(self):
        def func():
            self.view_table_trigger()
        self.button_reload.configure(command=func)

if(__name__ == "__main__"):
    Activate()