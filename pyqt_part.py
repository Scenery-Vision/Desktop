##############################################################################################################
# # IMPORTS
##############################################################################################################
import sys
import time

from PyQt5.QtGui import QFont, QIcon, QMovie

import Thread
from exel_part import download_image, excel_save
from resources_rc import *
from PyQt5.QtWidgets import *
from PySide2 import *

# IMPORT GUI FILE
from interface import *
# QT MATERIAL
from qt_material import *
import pandas as pd

from Thread import APIThread, final_data, f_data_cnt, first_load_flag

##############################################################################################################
# # MAIN WINDOW CLASS
##############################################################################################################

page_index = 0
char_index = 0
desc_index = 0

active = '''QPushButton {border: solid;border-radius: 0;border-bottom-width: 5px;color: rgb(99, 54, 109);
        border-color:rgb(99, 54, 109);padding-top:5px;}QPushButton::hover {color: rgb(146, 92, 154);
        border-color: rgb(146, 92, 154);background-color: rgba(146, 92, 154, 50);
        }'''
non_active = '''QPushButton {border: solid;border-radius: 0;border-bottom-width: 5px;color: rgb(190, 153, 196);
            border-color: rgb(190, 153, 196);padding-top:5px;}QPushButton::hover {color: rgb(146, 92, 154);
            border-color: rgb(146, 92, 154);background-color: rgba(146, 92, 154, 50);}'''


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.movie = None
        self.clickPosition = None
        self.oldPosition = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # fonts init
        ################################################################################################################
        # font_abhaya_libre_id = QFontDatabase.addApplicationFont(":/fonts/fonts/AbhayaLibre-Regular.ttf")
        # fontName = QFontDatabase.applicationFontFamilies(font_abhaya_libre_id)[0]
        # self.font_abhaya_libre = QFont(fontName, 42)
        # self.ui.scenary_vision_label.setFont(self.font_abhaya_libre)
        #
        # font_mulish_medium_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Medium.ttf")
        # fontName = QFontDatabase.applicationFontFamilies(font_mulish_medium_id)[0]
        # self.font_mulish_medium = QFont(fontName, 19)
        # self.ui.title_label.setFont(self.font_mulish_medium)
        #
        # font_mulish_bold_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Bold.ttf")
        # fontName = QFontDatabase.applicationFontFamilies(font_mulish_bold_id)[0]
        # self.font_mulish_bold = QFont(fontName, 12)
        # self.ui.label_2.setFont(self.font_mulish_bold)
        # self.ui.label_5.setFont(self.font_mulish_bold)
        #
        # font_mulish_regular_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Regular.ttf")
        # fontName = QFontDatabase.applicationFontFamilies(font_mulish_regular_id)[0]
        # self.font_mulish_regular = QFont(fontName, 10)
        # self.ui.characteristics_label.setFont(self.font_mulish_regular)
        # self.ui.descreption_label.setFont(self.font_mulish_regular)
        ################################################################################################################

        # Remove window title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # type: ignore
        self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)
        self.ui.characteristic_stacked_widget.setCurrentWidget(self.ui.characteristic_page_1)
        self.change_characteristic_button_style(0)

        # Set window title, size grip and icon
        self.setWindowTitle("Scenery Vision")
        self.setWindowIcon(QIcon(":/icons/images/add_exel.svg"))
        self.api_thread = APIThread()
        self.ui.title_label.setText("dddddddeeeeeeeeeeeeeввyy\ngyvyyydddddddd")

        # Minimize window
        self.ui.minimize_window_button.clicked.connect(self.showMinimized)
        # Close window
        self.ui.close_window_button.clicked.connect(self.close)
        # Restore/Maximize window
        self.ui.restore_window_button.clicked.connect(self.restore_or_maximize_window)

        # Exel huge button
        self.ui.exel_button.clicked.connect(self.browse_files)

        # Arrows buttons
        self.ui.left_arrow_button.clicked.connect(self.change_page_left)
        self.ui.right_arrow_button.clicked.connect(self.change_page_right)

        # Add button
        self.ui.add_button.clicked.connect(self.browse_files)
        # Add button
        self.ui.download_button.clicked.connect(self.save_files)

        # Characteristics radio buttons
        self.ui.characteristic_button_1.clicked.connect(lambda: self.characteristic_buttons(0))
        self.ui.characteristic_button_2.clicked.connect(lambda: self.characteristic_buttons(1))
        self.ui.characteristic_button_3.clicked.connect(lambda: self.characteristic_buttons(2))

        # Description radio buttons
        self.ui.description_button_1.clicked.connect(lambda: self.description_buttons(0))
        self.ui.description_button_2.clicked.connect(lambda: self.description_buttons(1))
        self.ui.description_button_3.clicked.connect(lambda: self.description_buttons(2))
        self.ui.description_button_4.clicked.connect(lambda: self.description_buttons(3))

        self.api_thread.update_api_data.connect(self.end_of_first_loading, QtCore.Qt.QueuedConnection)

        # Function to Move window on mouse drag event on the title bar
        def moveWindow(e):
            if not self.isMaximized():
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

        self.ui.header.mouseMoveEvent = moveWindow

        self.show()

    # Description radio buttons function
    def description_buttons(self, n):
        global desc_index
        desc_index = n
        if n == 0:
            self.change_description_button_style(0)
        elif n == 1:
            self.change_description_button_style(1)
        elif n == 2:
            self.change_description_button_style(2)
        else:
            self.change_description_button_style(3)
            desc_index = 2
        self.load_page_without_foto(Thread.final_data, page_index, char_index, desc_index)

    # Characteristics radio buttons function
    def characteristic_buttons(self, n):
        global char_index
        char_index = n
        if n == 0:
            self.ui.characteristic_stacked_widget.setCurrentWidget(self.ui.characteristic_page_1)
            self.change_characteristic_button_style(0)
        elif n == 1:
            self.ui.characteristic_stacked_widget.setCurrentWidget(self.ui.characteristic_page_2)
            self.change_characteristic_button_style(1)
        else:
            self.ui.characteristic_stacked_widget.setCurrentWidget(self.ui.characteristic_page_3)
            self.change_characteristic_button_style(2)

        self.load_page_without_foto(Thread.final_data, page_index, char_index, desc_index)

    # Browse files function
    def browse_files(self):
        global page_index
        global char_index
        global desc_index
        page_index = 0
        char_index = 0
        desc_index = 0
        self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)
        file_name = QFileDialog.getOpenFileName(self, 'open file', 'C:', 'XLSX files (*xlsx);;CSV files (*csv)')[0]

        self.ui.stackedWidget.setCurrentWidget(self.ui.loading_page)

        gif_path = 'images/load.gif'
        gif = QtGui.QMovie(gif_path)
        self.ui.loading_label.setMovie(gif)
        gif.start()

        if file_name != "":
            self.api_thread.reset_file(file_name)
            self.api_thread.start()
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)

    @QtCore.pyqtSlot()
    def end_of_first_loading(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                      Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                       char_index, 0)

    def save_files(self):
        user_filename = QFileDialog.getSaveFileName(self, 'save file', 'C:', 'XLSX files (*xlsx)')[0]
        if user_filename != "":
            file_name = user_filename + '.xlsx'
            excel_save(Thread.final_data, file_name)
        else:
            QtWidgets.QMessageBox.critical(None, "Файл не сохранен", "Вы не указали имя файла, попробуйте еще раз")

    def change_page_left(self):  # left
        global page_index
        if page_index > 0:
            page_index = page_index - 1
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)
        else:
            page_index = len(Thread.final_data.index) - 1
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)

    def change_page_right(self):  # Right
        global page_index

        if page_index < len(Thread.final_data.index) - 1:
            page_index = page_index + 1
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)
        else:
            page_index = 0
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)

    def load_chars(self, chars_data: pd.Series) -> None:
        print(chars_data)
        self.ui.characteristic_1.setText(chars_data.values[0])
        self.ui.characteristic_2.setText(chars_data.values[1])
        self.ui.characteristic_3.setText(chars_data.values[2])
        self.ui.characteristic_4.setText(chars_data.values[3])
        self.ui.characteristic_5.setText(chars_data.values[1])
        self.ui.characteristic_6.setText(chars_data.values[2])
        self.ui.characteristic_7.setText(chars_data.values[3])
        self.ui.characteristic_8.setText(chars_data.values[2])
        self.ui.characteristic_9.setText(chars_data.values[3])
        self.ui.characteristic_10.setText(chars_data.values[2])
        self.ui.characteristic_11.setText(chars_data.values[3])
        self.ui.characteristic_12.setText(chars_data.values[3])
        self.ui.characteristic_13.setText(chars_data.values[3])
        self.ui.characteristic_14.setText(chars_data.values[3])
        self.ui.characteristic_15.setText(chars_data.values[3])
        self.ui.characteristic_16.setText(chars_data.values[3])
        self.ui.characteristic_17.setText(chars_data.values[3])
        self.ui.characteristic_18.setText(chars_data.values[3])
        self.ui.characteristic_19.setText(chars_data.values[3])
        self.ui.characteristic_20.setText(chars_data.values[3])
        # artikul = chars_data["Артикул"][page_index]
        # brend = chars_data["Бренд"][page_index]
        # self.ui.characteristic_3.setText(Thread.final_data_copy["Средний вес"][page_index])



    def load_description(self, description_data: pd.Series) -> None:
        generated_description = description_data
        self.ui.descreption_label.setText(generated_description)  # type: ignore
        self.ui.descreption_label.setWordWrap(True)

    def load_page_without_foto(self, generated_data: pd.DataFrame,
                               page_idx: int, chars_idx: int,
                               description_idx: int,
                               description_col: str = "Описание",
                               chars_on_page: int = 4
                               ) -> None:

        # custom WordWarp:
        str_size = 22
        if len(generated_data["Название"][page_idx]) > str_size * 2:
            label = generated_data["Название"][page_idx]
            i = str_size * 2
            while label[i] != ' ':
                i = i - 1
            warped_label = label[:i] + "<br>" + label[i:]
            i = str_size
            while warped_label[i] != ' ':
                i = i - 1
            warped_label = warped_label[:i] + "<br>" + warped_label[i:]
            self.ui.title_label.setText(warped_label)
        if str_size < len(generated_data["Название"][page_idx]) < str_size * 2:
            label = generated_data["Название"][page_idx]
            i = str_size
            while label[i] != ' ':
                i = i - 1
            warped_label = label[:i] + "<br>" + label[i:]
            self.ui.title_label.setText(warped_label)
        if len(generated_data["Название"][page_idx]) < str_size:
            self.ui.title_label.setText(generated_data["Название"][page_idx])

        self.ui.title_label.setTextFormat(1)
        self.ui.title_label.setAlignment(QtCore.Qt.AlignCenter)

        characteristics = generated_data.dropna(axis=1).columns.tolist()
        characteristics_data = generated_data.iloc[page_idx].copy()

        self.load_chars(characteristics_data)
        self.load_description(
            description_data=generated_data[f"{description_col}{description_idx + 1}"].iloc[page_idx])  # type: ignore

    def load_page(
            self, image_path: str,
            generated_data: pd.DataFrame,
            page_idx: int, chars_idx: int,
            description_idx: int,
            description_col: str = "Описание",
            chars_on_page: int = 4
    ) -> None:
        pixmap = QtGui.QPixmap(image_path)
        self.ui.image_label.setPixmap(pixmap)

        # custom WordWarp:
        str_size = 22
        if len(generated_data["Название"][page_idx]) > str_size * 2:
            label = generated_data["Название"][page_idx]
            i = str_size * 2
            while label[i] != ' ':
                i = i - 1
            warped_label = label[:i] + "<br>" + label[i:]
            i = str_size
            while warped_label[i] != ' ':
                i = i - 1
            warped_label = warped_label[:i] + "<br>" + warped_label[i:]
            self.ui.title_label.setText(warped_label)
        if str_size < len(generated_data["Название"][page_idx]) < str_size * 2:
            label = generated_data["Название"][page_idx]
            i = str_size
            while label[i] != ' ':
                i = i - 1
            warped_label = label[:i] + "<br>" + label[i:]
            self.ui.title_label.setText(warped_label)
        if len(generated_data["Название"][page_idx]) < str_size:
            self.ui.title_label.setText(generated_data["Название"][page_idx])

        self.ui.title_label.setTextFormat(1)
        self.ui.title_label.setAlignment(QtCore.Qt.AlignCenter)

        characteristics = generated_data.dropna(axis=1).columns.tolist()
        characteristics_data = generated_data.iloc[page_idx].copy()

        self.load_chars(characteristics_data)
        self.load_description(
            description_data=generated_data[f"{description_col}{description_idx + 1}"].iloc[page_idx])  # type: ignore

    def change_characteristic_button_style(self, n):
        self.ui.characteristic_button_1.setStyleSheet(non_active)
        self.ui.characteristic_button_2.setStyleSheet(non_active)
        self.ui.characteristic_button_3.setStyleSheet(non_active)
        if n == 0:
            self.ui.characteristic_button_1.setStyleSheet(active)
        elif n == 1:
            self.ui.characteristic_button_2.setStyleSheet(active)
        else:
            self.ui.characteristic_button_3.setStyleSheet(active)

    def change_description_button_style(self, n):
        self.ui.description_button_1.setStyleSheet(non_active)
        self.ui.description_button_2.setStyleSheet(non_active)
        self.ui.description_button_3.setStyleSheet(non_active)
        self.ui.description_button_4.setStyleSheet(non_active)
        if n == 0:
            self.ui.description_button_1.setStyleSheet(active)
        elif n == 1:
            self.ui.description_button_2.setStyleSheet(active)
        elif n == 2:
            self.ui.description_button_3.setStyleSheet(active)
        else:
            self.ui.description_button_4.setStyleSheet(active)

    # Add mouse events to the window
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    # Update restore button icon on maximizing or minimizing window
    # Also it is possible to add changing icon on the button
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.ui.restore_window_button.setIcon(QtGui.QIcon((":/icons/images/restore_maximize_1.svg")))

            self.showNormal()
        else:
            self.ui.restore_window_button.setIcon(QtGui.QIcon((":/icons/images/restore_maximize_2.svg")))
            self.showMaximized()


##############################################################################################################
# # EXECUTE APP
##############################################################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

##############################################################################################################
# # END
##############################################################################################################
