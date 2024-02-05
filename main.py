import math
import os
import sys
from geocoder import *
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]
# Подобранные константы для поведения карты.
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.002
coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
coord_to_geo_y = 0.0000428


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = 37.612308
        self.lat = 55.658444
        self.z = 15
        self.getImage()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ','.join([str(self.lon), str(self.lat)]),
            #"spn": delta,
            "z": self.z,  # 0 - 21
            "l": "map",
            "pt": f"{','.join([str(self.lon), str(self.lat)])},pm2dgl"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.lon += LON_STEP * math.pow(2, 15 - self.z)
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def new_address(self):
        s = input('Напиши адрес')
        self.lon = get_coordinates(s)[0]
        self.lat = get_coordinates(s)[1]
        self.z = 12
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    #ex.new_address()
    sys.exit(app.exec())