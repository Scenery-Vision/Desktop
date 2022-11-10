##############################################################################################################
# # IMPORTS
##############################################################################################################
import sys
import time

from PyQt5.QtGui import QFont, QIcon

import Thread
from exel_part import download_image, excel_save
from resources import *
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


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.clickPosition = None
        self.oldPosition = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # fonts init
        ################################################################################################################
        font_abhaya_libre_id = QFontDatabase.addApplicationFont(":/fonts/fonts/AbhayaLibre-Regular.ttf")
        fontName = QFontDatabase.applicationFontFamilies(font_abhaya_libre_id)[0]
        self.font_abhaya_libre = QFont(fontName, 42)
        self.ui.scenary_vision_label.setFont(self.font_abhaya_libre)

        font_mulish_medium_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Medium.ttf")
        fontName = QFontDatabase.applicationFontFamilies(font_mulish_medium_id)[0]
        self.font_mulish_medium = QFont(fontName, 19)
        self.ui.title_label.setFont(self.font_mulish_medium)

        font_mulish_bold_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(font_mulish_bold_id)[0]
        self.font_mulish_bold = QFont(fontName, 12)
        self.ui.label_2.setFont(self.font_mulish_bold)
        self.ui.label_5.setFont(self.font_mulish_bold)

        font_mulish_regular_id = QFontDatabase.addApplicationFont(":/fonts/fonts/Mulish-Regular.ttf")
        fontName = QFontDatabase.applicationFontFamilies(font_mulish_regular_id)[0]
        self.font_mulish_regular = QFont(fontName, 10)
        self.ui.characteristics_label.setFont(self.font_mulish_regular)
        self.ui.descreption_label.setFont(self.font_mulish_regular)
        ################################################################################################################

        # Remove window title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # type: ignore
        self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)

        # Set window title and icon
        self.setWindowTitle("Scenery Vision")
        self.setWindowIcon(QIcon(":/newPrefix/images/scenery_icon.png"))
        self.api_thread = APIThread()
        self.ui.title_label.setText("dddddddeeeeeeeeeeeeeввyy\ngyvyyydddddddd")

        # Minimize window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        # Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        # Restore/Maximize window
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

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

        self.api_thread.update_api_data.connect(self.end_of_first_loading, QtCore.Qt.QueuedConnection)

        # Function to Move window on mouse drag event on the title bar
        def moveWindow(e):
            if not self.isMaximized():
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

        self.ui.top_header.mouseMoveEvent = moveWindow

        self.show()

    # Description radio buttons function
    def description_buttons(self, n):
        global desc_index
        desc_index = n
        self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                      Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                       char_index, desc_index)

    # Characteristics radio buttons function
    def characteristic_buttons(self, n):
        global char_index
        char_index = n
        self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                      Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                       char_index, desc_index)

    # Browse files function
    def browse_files(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)
        file_name = QFileDialog.getOpenFileName(self, 'open file', 'C:', 'XLSX files (*xlsx);;CSV files (*csv)')[0]
        self.ui.stackedWidget.setCurrentWidget(self.ui.loading_page)
        if file_name != "":
            self.api_thread.reset_file(file_name)
            self.api_thread.start()
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.exel_page)

    @QtCore.pyqtSlot()
    def end_of_first_loading(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        print('111')
        print(Thread.final_data["Артикул"])
        print('111')
        print(download_image(Thread.final_data["Путь к фото"][page_index], Thread.final_data["Артикул"][page_index]))
        print('111')
        print(page_index)
        print(char_index)
        self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                      Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                       char_index, 0)


    def save_files(self):
        file_name = QFileDialog.getSaveFileName(self, 'save file', 'C:', 'XLSX files (*xlsx)')[0] + '.xlsx'
        print(file_name)
        print(Thread.final_data)
        excel_save(Thread.final_data, file_name)

    def change_page_left(self):  # left
        global page_index
        print(page_index)
        if page_index > 0:
            page_index = page_index - 1
            print(page_index)
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

        print(page_index)
        if page_index < len(Thread.final_data.index) - 1:
            page_index = page_index + 1
            print(page_index)
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)
        else:
            page_index = 0
            self.load_page(download_image(Thread.final_data["Путь к фото"][page_index],
                                          Thread.final_data["Артикул"][page_index]), Thread.final_data, page_index,
                           char_index, desc_index)



    def load_chars(self, chars_data: pd.Series) -> None:
        generated_text = "\n".join(
            [f"{char_key}: {char_val}" for char_key, char_val in zip(chars_data.index, chars_data.values)])
        self.ui.characteristics_label.setText(generated_text)
        self.ui.characteristics_label.setWordWrap(True)

    def load_description(self, description_data: pd.Series) -> None:
        generated_description = description_data
        self.ui.descreption_label.setText(generated_description)  # type: ignore
        self.ui.descreption_label.setWordWrap(True)

    def load_page(
            self, image_path: str,
            generated_data: pd.DataFrame,
            page_idx: int, chars_idx: int,
            description_idx: int,
            description_col: str = "Описание",
            chars_on_page: int = 4
    ) -> None:
        print('im in')
        pixmap = QtGui.QPixmap(image_path)
        self.ui.image_label.setPixmap(pixmap)

        #self.ui.title_label.setWordWrap(True)
        self.ui.title_label.setText(generated_data["Название"][page_idx])
        self.ui.title_label.setTextFormat(1)
        print(1)
        #characteristics = generated_data.drop(description_col, axis=1).dropna(axis=1).columns.tolist()
        characteristics = generated_data.columns.tolist()

        print(2)
        cur_characteristics = characteristics[chars_idx * chars_on_page:chars_idx * chars_on_page + chars_on_page]
        print(3)
        characteristics_data = generated_data[cur_characteristics].iloc[page_idx].copy()

        self.load_chars(characteristics_data)
        print(4)
        self.load_description(
            description_data=generated_data[f"{description_col}{description_idx + 1}"].iloc[page_idx])  # type: ignore

    # Add mouse events to the window

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    # Update restore button icon on maximizing or minimizing window
    # Also it is possible to add changing icon on the button
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.ui.restore_window_button.setStyleSheet(
                "QPushButton#restore_window_button {\nwidth: 30px;\nheight: 30px;\nborder-image: url(:/newPrefix/images/restore_maximize_2.svg);\n}\nQPushButton#restore_window_button::hover {\nwidth: 30px;\nheight: 30px;\nbackground-color: rgb(85, 170, 255);\nborder-image: url(:/newPrefix/images/restore_maximize_2.svg);\n}")
            self.showNormal()
        else:
            self.ui.restore_window_button.setStyleSheet(
                "QPushButton#restore_window_button {\nwidth: 30px;\nheight: 30px;\nborder-image: url(:/newPrefix/images/restore_maximize_1.svg);\n}\nQPushButton#restore_window_button::hover {\nwidth: 30px;\nheight: 30px;\nbackground-color: rgb(85, 170, 255);\nborder-image: url(:/newPrefix/images/restore_maximize_1.svg);\n}")
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