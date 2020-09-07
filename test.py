from modules import raw_data


path = "/home/chinmay/Documents/covid-19-data/owid-covid-data.csv"
# print(raw_data.Raw().get_delimiter(path))

raw_data_obj = raw_data.Raw()
# print(raw_data_obj.list_allowed_delimiters)
raw_data_obj.set_path_file(path)


output = raw_data_obj.generate_delimiter(path)
# print(output)
# print(raw_data_obj.get_delimiter())

list_rows = raw_data_obj.generate_preview_table()

for row in list_rows:
    print("{}".format(raw_data_obj.get_delimiter()).join(row))
    print("\n\n")