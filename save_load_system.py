"""Module which contains system for save and load data for the game"""

import pickle as pc
from os import mkdir, path
from typing import Any
from constants import DATA_FOLDER_NAME, DATA_FILE_EXTENSION, ABSOLUTE_DATA_FOLDER_PATH


class GameSaveLoadSystem:

    def __init__(self) -> None:
        """
        Args:
            absolute_folder_path (str): absolute path to the folder which will contain data_folder
            file_extension (str): file extension which will be used for data saving (starts with .); Example: .data
        """
        self.absolute_folder_path: str = ABSOLUTE_DATA_FOLDER_PATH
        self.file_extension: str = DATA_FILE_EXTENSION
        self.data_folder_name: str = DATA_FOLDER_NAME

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

    def load_game_data(self, files_to_load_dict: dict[str, Any]) -> dict[str, Any]:
        """Method to load all data from all files in one dict

        Args:
            files_to_load_dict (dict[str, Any]): dictionary which contains key-value pairs where key is the name for the file
            and value is the default value which will be returned in case file is empty.

        Returns:
            dict: key is the name of the file and the value is the value assigned to it
        """
        return_data: dict[str, Any] = files_to_load_dict.copy()
        for file_name in files_to_load_dict:
            file_path: str = path.join(
                self.absolute_folder_path, self.data_folder_name, file_name + self.file_extension
            )
            if path.exists(file_path):
                return_data[file_name] = self.load_data(file_name)

        return return_data

    def save_game_data(self, files_to_save_dict) -> None:
        """Method to save all data from game with 1 dict

        Args:
            files_to_save_dict (dict[str, Any]): dictionary which contains key-value pairs where key is the name for the file
            and value is the value to write in this file.
        """
        for file_name, data in files_to_save_dict.items():
            self.save_data_to_file(file_name, data)
