import tkinter as tk



"""
LabelFrames
"""
def generate(root, ui_obj):
    frame_main = ui_obj.set_properties(
        tk.LabelFrame(root), 
        text="Main",
        height=ui_obj.get_window_dimensions()["y"] - 50,
        width=ui_obj.get_window_dimensions()["x"]
    )
    frame_main.pack_propagate(0)
    frame_main.pack(side=tk.TOP, fill=tk.X, expand=False)

    ui_obj.frame_main = frame_main

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
    ui_obj.frame_status = frame_status



    frame_raw_main = ui_obj.set_properties(
        tk.LabelFrame(frame_main),
        text="Raw Main",
        height=ui_obj.get_window_dimensions()["y"],
        width=ui_obj.get_window_dimensions()["x"]/2 - 5,
        bg="Red"
    )
    frame_raw_main.pack_propagate(0)
    frame_raw_main.pack(side=tk.LEFT, expand=False)
    ui_obj.frame_raw_main = frame_raw_main

    frame_dataset_main = ui_obj.set_properties(
        tk.LabelFrame(frame_main),
        text="Dataset Main",
        height=ui_obj.get_window_dimensions()["y"],
        width=ui_obj.get_window_dimensions()["x"]/2 - 5,
        bg="Blue"
    )
    frame_dataset_main.pack_propagate(0)
    frame_dataset_main.pack(side=tk.RIGHT, expand=False)
    ui_obj.frame_dataset_main = frame_dataset_main

    frame_raw_data_widgets = ui_obj.set_properties(
        tk.LabelFrame(frame_raw_main),
        text="Raw Data Widgets",
        height=ui_obj.get_window_dimensions()["y"]/2 - 10,
        bg="Pink"
    )
    frame_raw_data_widgets.pack_propagate(0)
    frame_raw_data_widgets.pack(side=tk.TOP, expand=False, fill=tk.X)
    ui_obj.frame_raw_data_widgets = frame_raw_data_widgets

    frame_raw_data_widgets_aggregations = ui_obj.set_properties(
        tk.LabelFrame(frame_raw_data_widgets),
        text="Aggregations",
        height=ui_obj.get_window_dimensions()["y"]/6,
        width=ui_obj.get_window_dimensions()["x"]/6,
        bg="Yellow"
    )
    frame_raw_data_widgets_aggregations.grid(row=2, column=2, rowspan=2, columnspan=3)
    ui_obj.frame_raw_data_widgets_aggregations = frame_raw_data_widgets_aggregations

    # def create_aggregations():
    #     list_aggregations = ui_obj.get_list_group_agg()
    #     dict_mapping = {}
    #     # Create the aggregation options
    #     for i in range(list_aggregations):
    #         dict_mapping[str(i)] = 



    frame_raw_data = ui_obj.set_properties(
        tk.LabelFrame(frame_raw_main),
        text="Raw Data Visualization",
        height=ui_obj.get_window_dimensions()["y"]/2 - 10,
        bg="Brown"
    )
    frame_raw_data.pack_propagate(0)
    frame_raw_data.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
    ui_obj.frame_raw_data = frame_raw_data

    frame_dataset_widgets = ui_obj.set_properties(
        tk.LabelFrame(frame_dataset_main),
        text="Dataset Widgets",
        height=ui_obj.get_window_dimensions()["y"]/2 - 10,
        bg="Yellow"
    )
    frame_dataset_widgets.pack_propagate(0)
    frame_dataset_widgets.pack(side=tk.TOP, expand=False, fill=tk.X)
    ui_obj.frame_dataset_widgets = frame_dataset_widgets

    frame_dataset = ui_obj.set_properties(
        tk.LabelFrame(frame_dataset_main),
        text="Dataset Visualization",
        height=ui_obj.get_window_dimensions()["y"]/2 - 10,
        bg="Maroon"
    )
    frame_dataset.pack_propagate(0)
    frame_dataset.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
    ui_obj.frame_dataset = frame_dataset



    return[root, ui_obj]