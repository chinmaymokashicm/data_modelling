import tkinter as tk

class Properties:
    def __init__(self):
        self.window = {
            "main": {
                "width": 1600,
                "height": 800
            },
            "popup": {
                "width": 400,
                "height": 600
            }
        }
        self.frame = {
            "main": {
                "widgets": {
                    "relwidth": 1,
                    "relheight": 0.2
                },
                "view": {
                    "relwidth": 1,
                    "relheight": 0.8
                }
            },
            "options": {
                "relwidth": 1,
                "relheight": 0.1
            }
        }

        self.default_directory = "/home/chinmay/Documents/indian_liver_patients/"
        
        self.df = {
            "raw": None,
            "processed": None,
            "describe": None
        }

        self.number_of_rows_in_preview = 20
        self.number_of_rows_in_preview_default = self.number_of_rows_in_preview
        self.number_of_rows_widgets = 3
        self.number_of_columns_widgets = 5

        self.list_tab_names = ["raw", "processed", "describe", "model", "plot"]

        self.list_list_sort_and_order = [[], []]

        self.string_default_text_transform_function = """df.apply(\n\tlambda row: ,\n\taxis=1\n\t)
        """

        # self.list_labels_view_options = ["preview", "filter", "groupby", "where"]
        self.list_labels_view_options = ["preview"]
        self.dict_menubutton_view_options = None

        self.list_listbox_filter_columns_indices = []
        self.string_where_condition_filter = None

        self.list_listbox_groupby_columns_indices = []
        self.list_groupby_aggregations = ["mean", "median", "max", "min", "sum", "count", "custom"]
        # self.list_groupby_aggregations = ["mean", "median", "max", "min", "sum", "count"]
        self.dict_groupby_aggregations = {}

        self.list_dtypes = [
            "int", "float", "bool", "obj", "str", 
            r"datetime | %m/%d/%Y | ns", 
            r"datetime | %m/%d/%Y | s", 
            r"datetime | %m/%d/%Y | dayofweek",
            r"datetime | %m/%d/%Y | day",
            r"datetime | %m/%d/%Y | week",
            r"datetime | %m/%d/%Y | date",
            r"datetime | %m/%d/%Y | time",
            r"datetime | %m/%d/%Y | year",
            r"datetime | %d-%m-%Y | ns",
            r"datetime | %d-%m-%Y | s",
            r"datetime | %d-%m-%Y | dayofweek",
            r"datetime | %d-%m-%Y | day",
            r"datetime | %d-%m-%Y | week",
            r"datetime | %d-%m-%Y | date",
            r"datetime | %d-%m-%Y | time",
            r"datetime | %d-%m-%Y | year"

        ]
        
        self.widget_properties = {
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
                    "height": "",
                    "highlightcolor": "",
                    "image": "",
                    "justify": "",
                    "padx": "",
                    "pady": "",
                    "relief": "",
                    "underline": "",
                    "width": "",
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
                    "justify": "center" ,
                    "relief": "" ,
                    "selectbackground": "" ,
                    "selectborderwidth": "" ,
                    "selectforeground": "" ,
                    "show": "" ,
                    "state": "disabled" ,
                    "textvariable": "" ,
                    "width": "" ,
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
                    "height": "",
                    "image": "",
                    "justify": "",
                    "padx": "",
                    "pady": "",
                    "relief": "",
                    "text": "Default label text",
                    "textvariable": "",
                    "underline": "",
                    "width": "",
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
                },
                "optionmenu": {
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
                    "padx": "",
                    "pady": "",
                    "relief": "",
                    "state": "disabled",
                    "text": "",
                    "textvariable": "",
                    "underline": "",
                    "variable": "",
                    "value": "",
                    "width": "",
                    "wraplength": ""
                },
                "listbox": {
                    "bg" : "",
                    "bd" : "",
                    "cursor" : "",
                    "font" : "",
                    "fg" : "",
                    "height" : "",
                    "highlightcolor" : "",
                    "highlightthickness" : "",
                    "relief" : "",
                    "selectbackground" : "",
                    "selectmode" : "",
                    "width" : "",
                    "xscrollcommand" : "",
                    "yscrollcommand" : ""
                }
            }

    def set_properties(self, widget, **kwargs):
        type_widget = str(widget.__class__).split(".")[-1].lower().replace("'", "").replace(">", "")
        for key, value in self.widget_properties[type_widget].items():
            try:
                widget[key] = value
            except Exception as e:
                # print(e)
                pass
                
        for key, value in kwargs.items():
            try:
                widget[key] = value
                # print(type_widget, key, value)
            except Exception as e:
                print(e)
            
        return(widget)

    def generate_menubutton_values(self, menubutton, list_labels):
        menubutton.menu = tk.Menu(menubutton)   
        menubutton["menu"]= menubutton.menu
        dict_column_key_value = {label: tk.IntVar() for label in list_labels}
        for key, value in dict_column_key_value.items():
            menubutton.menu.add_checkbutton(
                label=key,
                variable=value
            )
        return(dict_column_key_value)


