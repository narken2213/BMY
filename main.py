import os
import sys
from geocoder import *
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, address_ll, z):
        super().__init__()
        self.address_ll = address_ll
        self.z = z
        self.getImage()
        self.initUI()

    def getImage(self):
        print('xa', self.address_ll)
        map_params = {
            "ll": self.address_ll,
            #"spn": delta,
            "z": self.z,  # 0 - 21
            "l": "map",
            "pt": f"{self.address_ll},pm2dgl"
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
        if event.key() == Qt.Key_PageUp:
            if self.z <= 20:
                self.z += 1
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
        if event.key() == Qt.Key_PageDown:
            if self.z >= 1:
                self.z -= 1
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    s = input('Напиши адрес')
    print(get_ll_span(s))
    adress = get_ll_span(s)[0]
    z = 6
    app = QApplication(sys.argv)
    ex = Example(adress, z)
    ex.show()
    sys.exit(app.exec())