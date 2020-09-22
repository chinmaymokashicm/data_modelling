import tkinter as tk
from tkinter import filedialog as fd
import os
import pandas as pd
from pandastable import Table

from modules.ui import UI_Properties
 
class MainApplication(tk.Tk): 
    def __init__(self): 
        super().__init__()
        self.ui_properties = UI_Properties()
        self.geometry("{}x{}".format(self.ui_properties.width_window, self.ui_properties.height_window))
        self.generate_frames()
        self.set_frame_bottom()
        self.set_frame_raw_widgets()
        self.set_frame_processed_widgets()
    
    def generate_frames(self):
        """
        Frames
        """
        self.frame_main = self.ui_properties.set_properties(
            tk.Frame(self),
            bg="Red"
        )
        self.frame_main.place(relwidth=1, relheight=0.9)

        self.frame_bottom = self.ui_properties.set_properties(
            tk.Frame(self),
            bg="Blue"
        )
        self.frame_bottom.place(relwidth=1, relheight=0.1, rely=0.9)

        self.frame_raw_widgets =self.ui_properties.set_properties(
            tk.Frame(self.frame_main),
            bg="Orange"
        )
        self.frame_raw_widgets.place(relwidth=0.5, relheight=0.5, relx=0, rely=0)

        self.frame_raw_data = self.ui_properties.set_properties(
            tk.Frame(self.frame_main),
            bg="Magenta"
        )
        self.frame_raw_data.place(relwidth=0.5, relheight=0.5, relx=0, rely=0.5)

        self.frame_processed_widgets = self.ui_properties.set_properties(
            tk.Frame(self.frame_main),
            bg="Yellow"
        )
        self.frame_processed_widgets.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0)

        self.frame_processed_data = self.ui_properties.set_properties(
            tk.Frame(self.frame_main),
            bg="Green"
        )
        self.frame_processed_data.place(relwidth=0.5, relheight=0.5, relx=0.5, rely=0.5)

        self.frame_groupby_agg_raw_data_widgets = self.ui_properties.set_properties(
            tk.Frame(self.frame_raw_widgets),
            bg="Red"
        )
        self.frame_groupby_agg_raw_data_widgets.place(
            relwidth=1/self.ui_properties.raw_widgets_number_of_columns * 2, 
            relheight=1/self.ui_properties.raw_widgets_number_of_rows * 1, 
            relx=1/self.ui_properties.raw_widgets_number_of_columns * 1, 
            rely=1/self.ui_properties.raw_widgets_number_of_rows * 3
        )

    def set_frame_bottom(self):
        self.button_close = self.ui_properties.set_properties(
            tk.Button(self.frame_bottom),
            state=tk.ACTIVE,
            text="Close",
            command=exit
        )
        self.button_close.pack(side=tk.RIGHT)
 
    def activate_processed_widgets(self):
        self.button_view_processed.configure(state=tk.ACTIVE)
        self.menubutton_processed_use_options.configure(state=tk.ACTIVE)
        self.entry_processed_number_of_preview_rows.configure(state=tk.NORMAL)
        self.entry_processed_number_of_preview_rows.delete(0, tk.END)
        self.entry_processed_number_of_preview_rows.insert(0, self.ui_properties.number_of_rows_in_preview)
        self.optionmenu_change_dtype_change_column_name.configure(state="active")
        self.optionmenu_change_dtype_change_column_name.children["menu"].delete(0, "end")
        # def show(value):
        #     self.var_processed_dtype_change_column_name.set(value)
        for column_name in self.ui_properties.df_current.columns:
            self.optionmenu_change_dtype_change_column_name.children["menu"].add_command(
                label="{} | {}".format(column_name, self.ui_properties.df_current[column_name].dtype),
                command=lambda value=column_name: self.var_processed_dtype_change_column_name.set(value)
            )
        self.optionmenu_change_dtype_change_dtype.configure(state="active")
        self.button_change_dtype.configure(state=tk.ACTIVE)

        self.button_show_na.configure(
            state=tk.ACTIVE,
            command=lambda: self.view_table_processed(
                self.ui_properties.df_current[self.ui_properties.df_current.isna().any(axis=1)]
            )
        )

        # Configure columns_with_na optionmenu
        list_columns_with_na = [
            column_name for column_name in self.ui_properties.df_current.columns 
            if self.ui_properties.df_current[column_name].isna().any()
        ]
        self.optionmenu_columns_with_na.children["menu"].delete(0, "end")
        def show_columns_with_na(col):
            self.var_processed_columns_with_na.set(col)
            self.view_table_processed(self.ui_properties.df_current[self.ui_properties.df_current[col].isnull()])
        for column_name in list_columns_with_na:
            self.optionmenu_columns_with_na.children["menu"].add_command(
                label=column_name,
                command=lambda col=column_name: show_columns_with_na(col)
            )
        self.optionmenu_columns_with_na.configure(state="active")

        # Configure actions_for_na optionmenu
        def perform_action_on_na(action_for_na):
            column_name = self.var_processed_columns_with_na.get()
            if(action_for_na in ["drop", "mean", "median", "0", "1"]):
                # tk.messagebox.showinfo(title="Cool", message="Cool Cool Cool Cool Cool...")
                if(action_for_na in ["0", "1"]):
                    # print(self.var_processed_columns_with_na.get())
                    self.ui_properties.df_current[column_name] = self.ui_properties.df_current[column_name].fillna(value=int(action_for_na))
                    print(self.ui_properties.df_current[column_name].head())
                    print(self.ui_properties.df_current[self.ui_properties.df_current[column_name].isnull()])
                    self.view_table_processed(self.ui_properties.df_current)
                    tk.messagebox.showinfo(title="Success", message="Null value in {} replaced with {}".format(column_name, action_for_na))
            else:
                tk.messagebox.showerror(title="No doubt", message="No doubt No doubt No doubt No doubt")
            self.var_processed_actions_for_column_with_na.set(action_for_na)

        self.optionmenu_actions_for_column_with_na.children["menu"].delete(0, "end")
        for action in self.ui_properties.list_optionmenu_actions_for_na:
            self.optionmenu_actions_for_column_with_na["menu"].add_command(
                label=action,
                command=lambda col=action: perform_action_on_na(col)
            )
        self.optionmenu_actions_for_column_with_na.configure(state="active")

        # Filter processed columns
        self.menubutton_processed_filter_columns.configure(state=tk.ACTIVE)
        self.ui_properties.dict_processed_filter_columns = self.generate_menubutton_values(
            self.menubutton_processed_filter_columns,
            self.ui_properties.df_current.columns
        )

    def view_table_raw(self, df=None):
        print("Generating table...")
        # Consider options menubutton
        if(self.ui_properties.dict_menubutton_raw_use_options["groupby"].get() == 1):
            dict_agg = {}
            if(self.ui_properties.dict_menubutton_groupby_agg != {}):
                for agg, dict_ in self.ui_properties.dict_menubutton_groupby_agg.items():
                    for column_name, value in dict_.items():
                        column = column_name.split("|")[0].split(" ")[0]
                        if(value.get() == 1):
                            if(column not in dict_agg):
                                dict_agg[column] = []
                            dict_agg[column].append(agg)
                # print(self.ui_properties.dict_menubutton_raw_groupby_columns)
                list_groupby_columns = [column for column, value in self.ui_properties.dict_menubutton_raw_groupby_columns.items() if value.get() == 1]
                if(dict_agg != {}):
                    if(len(list_groupby_columns) != 0):
                        try:
                            df = df.groupby(list_groupby_columns).agg(dict_agg).reset_index()
                        except Exception as e:
                            tk.messagebox.showerror(title="Error grouping data", message=e)
                            return
                    
        if(self.ui_properties.dict_menubutton_raw_use_options["preview"].get() == 1):
            try:
                df = df.head(self.var_raw_entry_preview.get())
            except Exception as e:
                tk.messagebox.showerror(title="Error previewing data", message=e)
                return
        

        if(self.ui_properties.dict_menubutton_raw_use_options["filter"].get() == 1 and self.ui_properties.dict_menubutton_raw_use_options["groupby"].get() == 0):
            # Ignore filter option if groupby is chosen
            list_columns = [column_name for column_name, value in self.ui_properties.dict_menubutton_filter_columns.items() if value.get() == 1]
            if(len(list_columns) == 0):
                list_columns = [column_name for column_name in self.ui_properties.dict_menubutton_filter_columns.keys() if column_name in df.columns]
            # print(list_columns)
            try:
                df = df[list_columns]
            except Exception as e:
                tk.messagebox.showerror(title="Error filtering data", message=e)
                return

        try:
            table = Table(self.frame_raw_data, dataframe=df, showtoolbar=True, showstatusbar=True)
            table.redraw()
            table.show()
        except Exception as e:
            tk.messagebox.showerror(title="Error generating table", message=e)

        try:
            # Activate the widgets on the processed data (TK) frame
            self.activate_processed_widgets()


        except Exception as e:
            print(e)
            tk.messagebox.showerror(title="Error activating widgets", message=e)

    def generate_menubutton_values(self, menubutton, list_labels, callback_func=None):
        menubutton.menu = tk.Menu(menubutton)   
        menubutton["menu"]= menubutton.menu
        dict_column_key_value = {label: tk.IntVar() for label in list_labels}
        if(callback_func is None):
            for key, value in dict_column_key_value.items():
                menubutton.menu.add_checkbutton(
                    label=key,
                    variable=value
                )
        else:
            for key, value in dict_column_key_value.items():
                menubutton.menu.add_checkbutton(
                    label=key,
                    variable=value,
                    command=lambda: callback_func(dict_column_key_value)
                )
        return(dict_column_key_value)

    def menubutton_callback(self, dict_column_key_value):
        # self.ui_properties.dict_menubutton_groupby_agg = {label: tk.IntVar() for label, value in dict_column_key_value.items() if value.get() == 0}
        self.ui_properties.dict_menubutton_groupby_agg = {}
        for agg in self.ui_properties.list_group_agg:
            self.ui_properties.dict_menubutton_groupby_agg[agg] = {label: tk.IntVar() for label, value in dict_column_key_value.items() if value.get() == 0}
            # print(self.ui_properties.dict_menubutton_names_groupby_agg)
            self.ui_properties.dict_menubutton_groupby_agg[agg]= self.generate_menubutton_values(
                self.ui_properties.dict_menubutton_names_groupby_agg[agg],
                ["{} | {}".format(label, self.ui_properties.df_raw[label].dtype) for label in self.ui_properties.dict_menubutton_groupby_agg[agg].keys()]
            )
            self.ui_properties.dict_menubutton_names_groupby_agg[agg].configure(state=tk.ACTIVE)

        # print(self.ui_properties.dict_menubutton_groupby_agg)

    def set_frame_raw_widgets(self):
        def set_select_file():
            def select_file():
                try:
                    path_file = fd.askopenfilename(
                        initialdir=self.ui_properties.default_dir,
                        title="Select raw dataset",
                        filetypes = (("CSV files","*.csv"),("TXT files","*.txt"))
                        )
                    if(isinstance(path_file, str) and path_file !=""):
                        print(path_file)
                        self.ui_properties.default_dir = os.path.dirname(path_file)
                        
                        # Load the file onto a pandas dataset
                        # self.ui_properties.df_raw = pd.read_csv(path_file, delimiter=self.ui_properties.data_delimiter)
                        
                        self.ui_properties.df_raw = pd.read_csv(path_file)
                        self.ui_properties.df_current = self.ui_properties.df_raw.copy(deep=True)

                        # Update value on label
                        self.label_raw_info.configure(text="{}: {} rows".format(
                            os.path.basename(self.ui_properties.default_dir).split(".")[-1].upper(),
                            len(self.ui_properties.df_raw.index))
                        )

                        # Activate other widgets
                        try:
                            self.button_view.configure(state=tk.ACTIVE)

                            self.entry_raw_number_of_preview_rows.configure(state=tk.NORMAL)
                            self.entry_raw_number_of_preview_rows.delete(0, tk.END)
                            self.entry_raw_number_of_preview_rows.insert(0, self.ui_properties.number_of_rows_in_preview)

                            self.menubutton_filter_columns.configure(state=tk.ACTIVE)
                            self.ui_properties.dict_menubutton_filter_columns = self.generate_menubutton_values(
                                self.menubutton_filter_columns, 
                                self.ui_properties.df_raw.columns
                            )
                            # Select all columns on the filter menubutton by default
                            # for value in self.ui_properties.dict_menubutton_filter_columns.values():
                            #     value.set(1)
                            
                            self.menubutton_raw_use_options.configure(state=tk.ACTIVE)

                            # Select all columns on the options menubutton by default
                            for value in self.ui_properties.dict_menubutton_raw_use_options.values():
                                value.set(1)

                            self.menubutton_raw_groupby.configure(state=tk.ACTIVE)
                            self.ui_properties.dict_menubutton_raw_groupby_columns = self.generate_menubutton_values(
                                self.menubutton_raw_groupby,
                                self.ui_properties.df_raw.columns,
                                self.menubutton_callback
                            )
                            self.button_df_describe.configure(state=tk.ACTIVE)
                            

                        except Exception as e:
                            print(e)

                    else:
                        self.label_raw_info.configure(text="N.A.")
                except Exception as e:
                    self.label_raw_info.configure(text="...")
                    print(e)
                    tk.Message(text=str(e))
                   
            self.button_select_file = self.ui_properties.set_properties(
                tk.Button(self.frame_raw_widgets),
                state=tk.ACTIVE,
                text="Select file",
                command=select_file
            )
            self.button_select_file.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=0, 
                rely=0
            )

        def set_raw_info_label():
            self.label_raw_info = self.ui_properties.set_properties(
                tk.Label(self.frame_raw_widgets),
                text="..."
            )
            self.label_raw_info.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=1/self.ui_properties.raw_widgets_number_of_columns * 1, 
                rely=0)

        def generate_view():
            self.button_view = self.ui_properties.set_properties(
                tk.Button(self.frame_raw_widgets),
                text="View",
                command=lambda: self.view_table_raw(self.ui_properties.df_raw)
            )
            self.button_view.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=0, 
                rely=1/self.ui_properties.raw_widgets_number_of_rows
            )

        def use_preview():
            # self.ui_properties.bool_use_preview = tk.IntVar()
            self.menubutton_raw_use_options = self.ui_properties.set_properties(
                tk.Menubutton(self.frame_raw_widgets),
                text="Options"
                # variable=self.ui_properties.bool_use_preview
            )
            self.menubutton_raw_use_options.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=1/self.ui_properties.raw_widgets_number_of_columns * 1, 
                rely=1/self.ui_properties.raw_widgets_number_of_rows * 1
            )

            # Generate the checkbuttons as well
            self.ui_properties.dict_menubutton_raw_use_options = self.generate_menubutton_values(
                self.menubutton_raw_use_options,
                ["preview", "filter", "groupby"]
            )

        def enter_preview():
            self.var_raw_entry_preview = tk.IntVar()
            self.entry_raw_number_of_preview_rows = self.ui_properties.set_properties(
                tk.Entry(self.frame_raw_widgets),
                text="Number of rows in preview",
                textvariable=self.var_raw_entry_preview
            )
            self.entry_raw_number_of_preview_rows.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=1/self.ui_properties.raw_widgets_number_of_columns * 2, 
                rely=0
            )

        def filter_columns():
            # Decide which columns to display
            self.menubutton_filter_columns = self.ui_properties.set_properties(
                tk.Menubutton(self.frame_raw_widgets),
                text="Filter Columns"
            )
            self.menubutton_filter_columns.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=1/self.ui_properties.raw_widgets_number_of_columns * 2, 
                rely=1/self.ui_properties.raw_widgets_number_of_rows * 1
            )
        
        def groupby_columns():
            # Decide which columns to group by
            self.menubutton_raw_groupby = self.ui_properties.set_properties(
                tk.Menubutton(self.frame_raw_widgets),
                text="Group By"
            )
            self.menubutton_raw_groupby.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=0, 
                rely=1/self.ui_properties.raw_widgets_number_of_rows * 3
            )

        def groupby_agg():
            # Display options for aggregations
            number_of_columns = len(self.ui_properties.list_group_agg)
            number_of_rows = 1
            width_frame = self.ui_properties.width_window / (2 * 3) * 2  
            height_frame = self.ui_properties.height_window / (2 * 3) * 2
            width_widget = width_frame/number_of_columns
            for agg_number, agg in enumerate(self.ui_properties.list_group_agg):
                # self.label_agg = self.ui_properties.set_properties(
                #     tk.Label(self.frame_groupby_agg_raw_data_widgets),
                #     text=self.ui_properties.list_group_agg[agg_number],
                #     width=int(width_widget)
                # )
                # self.label_agg.place(
                #     relwidth=1/number_of_columns,
                #     relheight=1/number_of_rows,
                #     relx=1/number_of_columns * agg_number,
                #     rely=0
                # )
                self.ui_properties.dict_menubutton_names_groupby_agg[agg] = self.ui_properties.set_properties(
                    tk.Menubutton(self.frame_groupby_agg_raw_data_widgets),
                    text=agg,
                    width=int(width_widget)
                )
                self.ui_properties.dict_menubutton_names_groupby_agg[agg].place(
                    relwidth=1/number_of_columns,
                    relheight=1/number_of_rows,
                    relx=1/number_of_columns * agg_number,
                    rely=0
                )

        def df_describe():
            def describe():
                try:
                    df = self.ui_properties.df_raw.describe()
                    df.insert(0, "Attribute", ["count", "mean", "std", "min", "25%", "50%", "75%", "max"], True)
                    table = Table(self.frame_raw_data, dataframe=df, showtoolbar=True, showstatusbar=True)
                    table.redraw()
                    table.show()
                except Exception as e:
                    tk.messagebox.showerror(title="Error generating table", message=e)
            
            self.button_df_describe = self.ui_properties.set_properties(
                tk.Button(self.frame_raw_widgets),
                text="Describe",
                command=describe
            )
            self.button_df_describe.place(
                relwidth=1/self.ui_properties.raw_widgets_number_of_columns, 
                relheight=1/self.ui_properties.raw_widgets_number_of_rows, 
                relx=0, 
                rely=1/self.ui_properties.raw_widgets_number_of_rows * 2
            )


        set_select_file()
        set_raw_info_label()
        generate_view()
        use_preview()
        enter_preview()
        filter_columns()
        groupby_columns()
        groupby_agg()
        df_describe()

    
    """ 
    From here on, we make changes to df_current 
    """
    def view_table_processed(self, df=None):
        try:
            if(df is None):
                df = self.ui_properties.df_current
            if(self.ui_properties.dict_menubutton_processed_use_options["reset"].get() == 1):
                self.ui_properties.df_current = self.ui_properties.df_raw.copy(deep=True)
                df = self.ui_properties.df_current
                self.ui_properties.dict_menubutton_processed_use_options["reset"].set(0)
                tk.messagebox.showinfo(title="Reset", message="Table reset!")
            
            # Check for preview
            if(self.ui_properties.dict_menubutton_processed_use_options["preview"].get() == 1):
                df = df.head(self.var_processed_entry_preview.get())

            # Check for filter
            if(self.ui_properties.dict_menubutton_processed_use_options["filter"].get() == 1):
                list_columns = [column_name for column_name, value in self.ui_properties.dict_processed_filter_columns.items() if value.get() == 1]
                if(len(list_columns) != 0):
                    df = df[list_columns]
            
            table = Table(self.frame_processed_data, dataframe=df, showtoolbar=True, showstatusbar=True)
            table.redraw()
            table.show()
        except Exception as e:
            tk.messagebox.showerror(title="Error generating table", message=e)

    def set_frame_processed_widgets(self):
        def generate_view():
            self.button_view_processed = self.ui_properties.set_properties(
                tk.Button(self.frame_processed_widgets),
                text="View/Reset",
                command=lambda: self.view_table_processed(self.ui_properties.df_current)
            )
            self.button_view_processed.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=0,
                rely=0
            )
    
        def use_preview():
            # self.ui_properties.bool_use_preview = tk.IntVar()
            self.menubutton_processed_use_options = self.ui_properties.set_properties(
                tk.Menubutton(self.frame_processed_widgets),
                text="Options"
                # variable=self.ui_properties.bool_use_preview
            )
            self.menubutton_processed_use_options.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 1, 
                rely=0
            )
            # Generate the checkbuttons as well
            self.ui_properties.dict_menubutton_processed_use_options = self.generate_menubutton_values(
                self.menubutton_processed_use_options,
                ["preview", "filter", "groupby", "reset"]
            )
            for key, value in self.ui_properties.dict_menubutton_processed_use_options.items():
                if(key != "reset"):
                    value.set(1)
        
        def enter_preview():
            self.var_processed_entry_preview = tk.IntVar()
            self.entry_processed_number_of_preview_rows = self.ui_properties.set_properties(
                tk.Entry(self.frame_processed_widgets),
                text="Number of rows in preview",
                textvariable=self.var_processed_entry_preview
            )
            self.entry_processed_number_of_preview_rows.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 2, 
                rely=0
            )

        def change_dtype():
            def change():
                column_name = self.var_processed_dtype_change_column_name.get()
                dtype = self.var_processed_dtype_change_dtype.get()
                try:
                    self.ui_properties.df_current[column_name] = self.ui_properties.df_current[column_name].astype(dtype)
                    # Update the dtypes in the columns list
                    self.optionmenu_change_dtype_change_column_name.children["menu"].delete(0, "end")
                    for column_name in self.ui_properties.df_current.columns:
                        self.optionmenu_change_dtype_change_column_name.children["menu"].add_command(
                            label="{} | {}".format(column_name, self.ui_properties.df_current[column_name].dtype),
                            command=lambda value=column_name: self.var_processed_dtype_change_column_name.set(value)
                        )
                    self.optionmenu_change_dtype_change_dtype.configure(bg="Green")
                    self.optionmenu_change_dtype_change_column_name.configure(bg="Green")
                    self.button_change_dtype.configure(bg="Green")
                except Exception as e:
                    print(e)
                    self.optionmenu_change_dtype_change_dtype.configure(bg="Red")
                    self.optionmenu_change_dtype_change_column_name.configure(bg="Red")
                    self.button_change_dtype.configure(bg="Red")
                    tk.messagebox.showerror(title="Error converting dtypes", message=e)

            # Change the data type of any particular column
            self.var_processed_dtype_change_column_name = tk.StringVar()
            self.optionmenu_change_dtype_change_column_name = tk.OptionMenu(
                self.frame_processed_widgets,
                self.var_processed_dtype_change_column_name,
                *[1,2,3,4,5]
            )
            self.optionmenu_change_dtype_change_column_name.configure(state="disabled")
            self.var_processed_dtype_change_column_name.set("Column Name")

            self.optionmenu_change_dtype_change_column_name.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 0, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 1
            )

            
            self.var_processed_dtype_change_dtype = tk.StringVar()
            self.optionmenu_change_dtype_change_dtype = tk.OptionMenu(
                self.frame_processed_widgets,
                self.var_processed_dtype_change_dtype,
                *["int", "float", "str", "object", "bool", "datetime"]
            )
            self.optionmenu_change_dtype_change_dtype.configure(state="disabled")
            self.var_processed_dtype_change_dtype.set("DType")
            self.optionmenu_change_dtype_change_dtype.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 1, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 1
            )

            # Button to execute the change
            self.button_change_dtype = self.ui_properties.set_properties(
                tk.Button(self.frame_processed_widgets),
                text="Change DType",
                command=change
            )
            self.button_change_dtype.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 2, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 1
            )

        def show_na():
            self.button_show_na = self.ui_properties.set_properties(
                tk.Button(self.frame_processed_widgets),
                text="Rows with NA"
            )
            self.button_show_na.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 0, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 2
            )
        
        def deal_with_na():
            # What to do with NA values
            self.var_processed_columns_with_na = tk.StringVar()
            self.optionmenu_columns_with_na = tk.OptionMenu(
                self.frame_processed_widgets,
                self.var_processed_columns_with_na,
                *[1,2,3,4,5]
            )
            self.optionmenu_columns_with_na.configure(state="disabled")
            self.var_processed_columns_with_na.set("Column with NA")
            self.optionmenu_columns_with_na.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 1, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 2
            )
            
            self.var_processed_actions_for_column_with_na = tk.StringVar()
            self.optionmenu_actions_for_column_with_na = tk.OptionMenu(
                self.frame_processed_widgets,
                self.var_processed_actions_for_column_with_na,
                # *self.ui_properties.list_optionmenu_actions_for_na
                *[1,2,3,4,5]
            )
            self.optionmenu_actions_for_column_with_na.configure(state="disabled")
            self.var_processed_actions_for_column_with_na.set("Action for NA value")
            self.optionmenu_actions_for_column_with_na.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows,
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 2, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 2
            )

        def filter_columns():
            # Decide which columns to display
            self.menubutton_processed_filter_columns = self.ui_properties.set_properties(
                tk.Menubutton(self.frame_processed_widgets),
                text="Filter Columns"
            )
            self.menubutton_processed_filter_columns.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 0, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 3
            )

        def where_condition():
            # Where condition: opens a new window
            self.button_where_condition = self.ui_properties.set_properties(
                tk.Button(self.frame_processed_widgets),
                text="Where"
            )
            self.button_where_condition.place(
                relwidth=1/self.ui_properties.processed_widgets_number_of_columns, 
                relheight=1/self.ui_properties.processed_widgets_number_of_rows, 
                relx=1/self.ui_properties.processed_widgets_number_of_columns * 1, 
                rely=1/self.ui_properties.processed_widgets_number_of_rows * 3
            )

        generate_view()
        use_preview()
        enter_preview()
        change_dtype()
        show_na()
        deal_with_na()
        filter_columns()
        where_condition()
        


if __name__ == "__main__": 
    app = MainApplication() 
    app.title("My Tkinter app") 
    app.mainloop()