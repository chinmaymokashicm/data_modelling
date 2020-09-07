"""
Load, analyse and process raw data
"""
import csv
import yaml
import os

from exceptions import exceptions

class Raw:
    def __init__(self):
        with open(os.path.join("properties", "csv_delimiters.yaml")) as file_yaml:
            self.list_allowed_delimiters = yaml.load(file_yaml, Loader=yaml.FullLoader)
        with open(os.path.join("properties", "defaults.yaml")) as file_yaml:
            self.dict_defaults = yaml.load(file_yaml, Loader=yaml.FullLoader)
        self.delimiter = self.dict_defaults["delimiter"]
        self.number_of_rows_in_preview = self.dict_defaults["number_of_rows_in_preview"]
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

    def set_delimiter(self, delimiter):
        if(delimiter not in self.list_allowed_delimiters):
            raise exceptions.CustomError("Invalid delimiter")

        self.delimiter = delimiter
        return
    
    def get_delimiter(self):
        return(self.delimiter)

    def generate_delimiter(self, path_file=None):
        """
        Returns a list of probable delimiters in decreasing order of probability
        """
        if(path_file is None):
            path_file = self.get_path_file()
        if(self.get_path_file() is None):
            raise exceptions.CustomError("Cannot find source file")

        self.set_path_file(path_file)

        with open(self.get_path_file(), "r", newline="") as csvfile:
            list_lines = csvfile.readlines()
        if(len(list_lines) > 0):
            dict_delimiter_count = {}
            for line_number in range(0, min(len(list_lines), self.get_number_of_rows_in_preview())):
                for delimiter in self.list_allowed_delimiters:
                    if(delimiter not in dict_delimiter_count.keys()):
                        dict_delimiter_count[delimiter] = 0
                    else:
                        dict_delimiter_count[delimiter] += list(list_lines[line_number]).count(delimiter)
            list_tuple_delimiter_count = sorted(dict_delimiter_count.items(), key=lambda item: item[1], reverse=True)
            self.set_delimiter(list_tuple_delimiter_count[0][0])
            self.set_path_file(path_file)
            return(list_tuple_delimiter_count)
        else:
            return(None)

    def generate_preview_table(self, number_of_rows_in_preview=None, path_file=None):
        if(number_of_rows_in_preview is None):
            number_of_rows_in_preview = self.get_number_of_rows_in_preview()
        if(self.get_number_of_rows_in_preview() is None):
            raise exceptions.CustomError("Error in default values. Cannot find default number of rows in preview")
        if(path_file is None):
            path_file = self.get_path_file()
        if(self.get_path_file() is None):
            raise exceptions.CustomError("Cannot find file path.")

        self.set_path_file(path_file)

        with open(self.get_path_file(), "r", newline="") as csvfile:
            list_lines = csvfile.readlines()
        
        list_lines = list_lines[:self.get_number_of_rows_in_preview()]
        min_number_of_columns = min([len(line.split(self.get_delimiter())) for line in list_lines])

        list_rows = []
        for line in list_lines:
            row = []
            counter = 0
            for cell in line.split(self.get_delimiter()):
                if(counter == min_number_of_columns):
                    row.append(str(line.split(self.get_delimiter())[counter:]))
                else:
                    row.append(cell)
            list_rows.append(row)
        return(list_rows)