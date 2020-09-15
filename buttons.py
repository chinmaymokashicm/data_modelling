import tkinter as tk


"""
Buttons
"""
def generate(root, ui_obj):
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
                label_df_config.configure(text="Total rows: {}".format(len(ui_obj.get_df_current().index))) 
                # ui_obj.set_df_new(df)
                button_generate_preview.configure(state=tk.ACTIVE)
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
                )
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