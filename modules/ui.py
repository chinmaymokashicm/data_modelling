# from tkinter import Frame, StringVar, Entry, BOTH, Tk
from tkinter import *
import yaml
import sys
# import pandas as pd


class UI:
    def __init__(self):
        self.path_file = None
        self.number_of_rows_in_preview = 20
        self.number_of_rows_in_preview_default = self.number_of_rows_in_preview
        # self.default_dir = "."
        # self.default_dir = "/home/chinmay/Documents/covid-19-data/"
        self.default_dir = "/home/chinmay/Documents/indian_liver_patients/"
        self.df_raw = None
        self.df_current = None
        # self.df_new = None
        self.list_menu_groupby = ["..", "A", "B"]
        self.dict_menubutton_values = {}
        self.list_non_groupby_columns = []
        self.list_group_agg = ["sum", "mean", "count", "min", "max"]
        self.dict_aggregation_frame_components = {key: None for key in self.list_group_agg}
        self.dict_agg_command_pre = {key: None for key in self.list_group_agg}
        self.table_height = 300
        self.window_dimensions = {
            "x": 1600,
            "y": 900
        }
        self.widget_dimensions = {
            "small": {
                "x": 15,
                "y": 1
            }
        }
        self.dict_properties = {
            "frame" : {
                "bg": "",
                "bd": "",
                "cursor": "",
                "height": "",
                "highlightbackground": "",
                "highlightcolor": "",
                "highlightthickness": "",
                "relief": "",
                "width": ""
            },
            "button": {
                "text": "Default Button Text",
                "activebackground": "Brown",
                "activeforeground": "Black",
                "bd": 1,
                "bg": "Pink",
                "command": None,
                "fg": "",
                "font": "",
                "height": self.widget_dimensions["small"]["y"],
                "highlightcolor": "",
                "image": "",
                "justify": "",
                "padx": "",
                "pady": "",
                "relief": "",
                "underline": "",
                "width": self.widget_dimensions["small"]["x"],
                "wraplength": "",
                "state": "disabled"
            },
            "labelframe": {
                "bg": "Orange",
                "bd": "",
                "cursor": "Brown",
                "height": "",
                "highlightbackground": "",
                "highlightcolor": "",
                "highlightthickness": "",
                "relief": "",
                "width": "",
                "padx": 0,
                "pady": 0
            },
            "entry": {
                "bg": "" ,
                "bd": "" ,
                "command": "" ,
                "cursor": "" ,
                "font": "" ,
                "exportselection": "" ,
                "fg": "" ,
                "highlightcolor": "" ,
                "justify": "" ,
                "relief": "" ,
                "selectbackground": "" ,
                "selectborderwidth": "" ,
                "selectforeground": "" ,
                "show": "" ,
                "state": "disabled" ,
                "textvariable": "" ,
                "width": self.widget_dimensions["small"]["x"] ,
                "xscrollcommand": "" 
            },
            "label": {
                "anchor": "",
                "bg": "",
                "bitmap": "",
                "bd": "",
                "cursor": "",
                "font": ("Courier", 8),
                "fg": "",
                "height": self.widget_dimensions["small"]["y"],
                "image": "",
                "justify": "",
                "padx": "",
                "pady": "",
                "relief": "",
                "text": "Default label text",
                "textvariable": "",
                "underline": "",
                "width": self.widget_dimensions["small"]["x"],
                "wraplength": ""
            },
            "message": {
                "anchor": "",
                "bg": "",
                "bitmap": "",
                "bd": "",
                "cursor": "",
                "font": "",
                "fg": "",
                "height": "",
                "image": "",
                "justify": "",
                "padx": "",
                "pady": "",
                "relief": "",
                "text": "Default message!",
                "textvariable": "",
                "underline": "",
                "width": "",
                "wraplength": ""
            },
            "scale": {
                "activebackground": "",
                "bg": "",
                "bd": "",
                "command": "",
                "cursor": "",
                "digits": "",
                "font": "",
                "fg": "",
                "from_": "",
                "highlightbackground": "",
                "highlightcolor": "",
                "label": "",
                "length": "",
                "orient": "",
                "relief": "",
                "repeatdelay": "",
                "resolution": "",
                "showvalue": "",
                "sliderlength": "",
                "state": "",
                "takefocus": "",
                "tickinterval": "",
                "to": "",
                "troughcolor": "",
                "variable": "",
                "width": ""
            },
            "checkbutton": {
                "activebackground": "",
                "activeforeground": "",
                "bg": "",
                "bitmap": "",
                "bd": "",
                "command": "",
                "cursor": "",
                "disabledforeground": "",
                "font": "",
                "fg": "",
                "height": "",
                "highlightcolor": "",
                "image": "",
                "justify": "",
                "offvalue": 0,
                "onvalue": 1,
                "padx": "",
                "pady": "",
                "relief": "",
                "selectcolor": "",
                "selectimage": "",
                "state": "disabled",
                "text": "",
                "underline": "",
                "variable": "",
                "width": "",
                "wraplength": ""
            },
            "menubutton": {
                "activebackground": "",
                "activeforeground": "",
                "anchor": "",	
                "bg": "",
                "bitmap": "",	
                "bd": "",
                "cursor": "",
                "direction": "",
                "disabledforeground": "",	
                "fg": "",
                "height": "",
                "highlightcolor": "",
                "image": "",
                "justify": "",
                "menu": "",
                "padx": "",
                "pady": "",
                "relief": "",
                "state": "disabled",
                "text": "",
                "textvariable": "",
                "underline": "",
                "width": "",
                "wraplength": ""
            }
        }
        
        return

    def set_path_file(self, path_file):
        self.path_file = path_file
        return

    def get_path_file(self):
        return(self.path_file)

    def set_number_of_rows_in_preview(self, number_of_rows_in_preview):
        self.number_of_rows_in_preview = number_of_rows_in_preview

    def get_number_of_rows_in_preview(self):
        return(self.number_of_rows_in_preview)

    def set_number_of_rows_in_preview_default(self, number_of_rows_in_preview_default):
        self.number_of_rows_in_preview_default = number_of_rows_in_preview_default

    def get_number_of_rows_in_preview_default(self):
        return(self.number_of_rows_in_preview_default)

    def set_dict_aggregation_frame_components(self, dict_aggregation_frame_components):
        self.dict_aggregation_frame_components = dict_aggregation_frame_components

    def get_dict_aggregation_frame_components(self):
        return(self.dict_aggregation_frame_components)

    def set_default_dir(self, default_dir):
        self.default_dir = default_dir
        return

    def get_default_dir(self):
        return(self.default_dir)

    def set_df_raw(self, df):
        self.df_raw = df
        return

    def get_df_raw(self):
        return(self.df_raw)

    def set_df_current(self, df):
        self.df_current = df
        return

    def get_df_current(self):
        return(self.df_current)

    def set_dict_menubutton_values(self, dict_menubutton_values):
        self.dict_menubutton_values = dict_menubutton_values
        return

    def get_dict_menubutton_values(self):
        return(self.dict_menubutton_values)


    def get_list_group_agg(self):
        return(self.list_group_agg)

    def set_list_non_groupby_columns(self, list_non_groupby_columns):
        self.list_non_groupby_columns = list_non_groupby_columns
        return

    def get_list_non_groupby_columns(self):
        return(self.list_non_groupby_columns)



    # def set_df_new(self, df):
    #     self.df_new = df
    #     return

    # def get_df_new(self):
    #     return(self.df_new)


    # def set_table_raw(self, dict_table_raw):
    #     self.table_raw = dict_table_raw
    #     return
    # def get_table_raw(self):
    #     return(self.table_raw)

    def set_table_height(self, height):
        self.table_height = height
        return
    
    def get_table_height(self):
        return(self.table_height)

    def set_window_dimensions(self, dict_window_dimensions):
        self.window_dimensions = dict_window_dimensions
        return
    
    def get_window_dimensions(self):
        return(self.window_dimensions)

    def set_list_menu_groupby(self, list_menu_groupby):
        self.list_menu_groupby = list_menu_groupby
        return
    
    def get_list_menu_groupby(self):
        return(self.list_menu_groupby)

    def add_checkbuttons_menubutton(self, menubutton, list_labels):
        def save_values():
            # for key, value in dict_int_var.items():
            #     print(key, value.get())
            self.set_dict_menubutton_values({key: value.get() for key, value in dict_int_var.items()})
            
            # Activate menubuttons inside aggregation frame
            # def save_values_0():
            #     # self.dict_agg_command_pre[agg] = {k: v.get() for k, v in dict_dict_int_var_0[agg].items()}
            #     for agg, dict_ in self.dict_agg_command_pre.items():
            #         for key, value in dict_.items():
            #             print(agg, key, value.get())


            dict_dict_int_var_0 = {}

            for key, value in self.get_dict_aggregation_frame_components().items():
                menubutton_0 = value[1]
                menubutton_0.configure(state=ACTIVE)
                menubutton_0.menu = Menu(menubutton_0)
                menubutton_0["menu"]= menubutton_0.menu
                list_labels_0 = [key_ for key_, value_ in self.get_dict_menubutton_values().items() if value_==0]
                dict_int_var_0 = {label: IntVar() for label in list_labels_0}
                self.dict_agg_command_pre[key] = dict_int_var_0
                dict_dict_int_var_0[key] = dict_int_var_0
                for k, v in dict_int_var_0.items():
                    menubutton_0.menu.add_checkbutton(
                        label=k,
                        variable=v
                    )


            
        menubutton.menu = Menu(menubutton)   
        menubutton["menu"]= menubutton.menu 
        dict_int_var = {label: IntVar() for label in list_labels}
        for key, value in dict_int_var.items():
            menubutton.menu.add_checkbutton(
                label=key, 
                variable=value,
                # onvalue=1,
                # offvalue=0,
                command=save_values
            )
        return(menubutton)


    def set_properties(self, tk_widget, **kwargs):
        type_widget = str(tk_widget.__class__).split(".")[-1].lower().replace("'", "").replace(">", "")
        # print(type_widget)
        # dict_properties = self.dict_properties[type_widget]
        for key, value in self.dict_properties[type_widget].items():
            try:
                tk_widget[key] = value
            except Exception as e:
                # print(e)
                pass
                
        for key, value in kwargs.items():
            try:
                tk_widget[key] = value
            except Exception as e:
                # print(e)
                pass
            
        return(tk_widget)
            