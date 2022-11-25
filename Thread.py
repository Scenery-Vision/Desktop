from PyQt5.QtCore import QThread, pyqtSignal

from exel_part import *
from multiprocessing import Process, Pipe

glob_size = 0
load_flag = False
emit_data = pd.DataFrame()

final_data = pd.DataFrame()
f_data_cnt = 0
first_load_flag = True
final_data_copy = pd.DataFrame()


def menu():
    while True:
        time.sleep(9)


def mega_process_suka(conn_s, path_to_table, batch, conn):
    count = 0
    table = load_and_processing_excel_csv(path_to_table)
    size = table.shape[0]
    conn_s.send(size)
    conn_s.close()
    while count <= size:
        slice = table.iloc[count: count + batch]
        conn.send(slice)
        count += batch


def update_data(data):
    print("пришло в update")  # Получение данных с обновлением API
    global final_data
    final_data = final_data.append(data, ignore_index=True)
    global f_data_cnt
    f_data_cnt = len(final_data.index)
    global final_data_copy
    final_data_copy = final_data.copy()
    # print(final_data)

    global first_load_flag
    first_load_flag = False


class APIThread(QThread):
    update_api_data = pyqtSignal()

    def __init__(self, path_to_table=""):
        super().__init__()
        self.batch = 16
        with open("ip.txt") as f:
            ip = f.read().strip()
        self.url_to_api = ip

        self.path_to_table = path_to_table
        self.table = pd.DataFrame()
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

                    parent_conn_s, child_conn_s = Pipe()
                    parent_conn, child_conn = Pipe()
                    p = Process(target=mega_process_suka,
                                args=(child_conn_s, self.path_to_table, self.batch, child_conn))
                    # p2 = Process(target=menu)
                    p.start()
                    # p2.start()
                    self.size = parent_conn_s.recv()
                    # self.table = load_and_processing_excel_csv(self.path_to_table)  # type: pd.DataFrame
                if self.count >= self.size:
                    return
                slice = parent_conn.recv()
                # slice = self.table.iloc[self.count: self.count + self.batch]
                # ---------->
                slice_copy = slice.drop(columns=["Комплект номенклатуры"]).copy()
                # slice_copy = slice[['Название', 'Бренд', 'Изделие с регулируемым размером', 'Средний вес',
                #                     'Ценовой сегмент', 'Тип металла', 'Проба', 'Цвет металла/покрытия',
                #                     'Цвет изделия', 'Дизайн 1', 'Дизайн 2', 'Дизайн 3', 'Стиль',
                #                     'Стиль номенклатуры', 'Перечисление тематик номенклатуры',
                #                     'Перечисление всех вставок', 'Общее количество вставок',
                #                     'Камень основной вставки', 'Каратный вес основного бриллианта',
                #                     'Подкласс товара', 'Тип изделия', 'Основная категория',
                #                     'Товарная категория', 'Товарная подкатегория', 'Общий тип изделия',
                #                     'Уточнение типа изделия', 'Дополнительное описание изделия',
                #                     'Плетение цепи', 'Вид замка', 'Символы и надписи', 'Знак зодиака',
                #                     'Религия', 'Лик святого', 'Для детей', 'Для мужчин', 'Для женщин',
                #                     'Теги']]
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
                self.count += self.batch
                if self.count >= self.size:
                    p.join()

            except Exception as ex:
                print("Error", ex)
                time.sleep(1)
                # load_flag = False

    def get_response(self, json_request):
        response = requests.post(self.url_to_api, json=json_request)
        return response.json()
