import time

import pandas as pd
import requests
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from exel_part import load_and_processing_excel_csv, transform_to_json

glob_size = 0
load_flag = False
emit_data = pd.DataFrame()

final_data = pd.DataFrame()
f_data_cnt = 0
first_load_flag = True


def update_data(data):
    print("пришло в update")  # Получение данных с обновлением API
    global final_data
    final_data = final_data.append(data, ignore_index=True)
    global f_data_cnt
    f_data_cnt = len(final_data.index)
    print(final_data)

    global first_load_flag
    first_load_flag = False


class APIThread(QThread):
    update_api_data = pyqtSignal()

    def __init__(self, path_to_table=""):
        super().__init__()
        self.batch = 3
        self.url_to_api = "http://127.0.0.1:3350/scenery-vision/api/v1.0/generation"

        self.path_to_table = path_to_table
        self.table = None  # type: ignore
        self.size = 0
        self.count = 0
        self.flag = False

    def reset_file(self, path_to_table: str):
        self.path_to_table = path_to_table
        self.flag = True
        global load_flag
        load_flag = False

    def run(self):
        while True:
            print("Метро Люблино, работаем")
            try:
                if self.flag:
                    self.flag = False
                    self.table = load_and_processing_excel_csv(self.path_to_table)  # type: pd.DataFrame
                    self.size = self.table.shape[0]
                    self.count = 0
                if self.count >= self.size:
                    return
                slice = self.table.iloc[self.count: self.count + self.batch]
                slice_copy = slice.drop(columns=["Комплект номенклатуры"])
                json_slice = transform_to_json(slice_copy)
                response = self.get_response(json_slice)
                slice["Описание1"] = [unit["Описание"][0] for unit in response]
                slice["Описание2"] = [unit["Описание"][1] for unit in response]
                slice["Описание3"] = [unit["Описание"][2] for unit in response]
                update_data(slice)
                global load_flag

                if not load_flag:
                    self.update_api_data.emit()
                    # я пока так сделал, но потом перепишу нормально не бей пж

                load_flag = True
                # self.update_api_data.emit(slice)
                self.count += self.batch
            except Exception as ex:
                print(ex)
                time.sleep(1)
                #load_flag = False

    def get_response(self, json_request):
        response = requests.post(self.url_to_api, json=json_request)
        return response.json()
