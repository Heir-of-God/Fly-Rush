"""Module which contains system for save and load data for the game"""

import pickle as pc
from os import mkdir, path
from typing import Any


class GameSaveLoadSystem:

    def __init__(self, absolute_folder_path: str, file_extension: str) -> None:
        """
        Args:
            absolute_folder_path (str): absolute path to the folder which will contain data_folder
            file_extension (str): file extension which will be used for data saving (starts with .); Example: .data
        """
        self.absolute_folder_path: str = absolute_folder_path
        self.file_extension: str = file_extension
        self.data_folder_name: str = "data_folder"

    def save_data_to_file(self, file_name: str, data_to_save: str | int | float) -> None:
        """Method to save single data entry to single file"""
        if not path.exists(path.join(self.absolute_folder_path, self.data_folder_name)):
            mkdir(path.join(self.absolute_folder_path, self.data_folder_name))

        file_path: str = path.join(self.absolute_folder_path, self.data_folder_name, file_name + self.file_extension)
        with open(file_path, "wb") as data_file:
            pc.dump(data_to_save, data_file)

    def load_data(self, file_name: str) -> str | int | float:
        """Method to load single data entry from single file"""
        if not path.exists(path.join(self.absolute_folder_path, self.data_folder_name)):
            mkdir(path.join(self.absolute_folder_path, self.data_folder_name))
        file_path: str = path.join(self.absolute_folder_path, self.data_folder_name, file_name + self.file_extension)
        if not path.exists(file_path):
            self.save_data_to_file("", file_name)

        with open(file_path, "rb") as data_file:
            data = pc.load(data_file)

        return data
