import os
import sys
from geocoder import *
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, address_ll, delta):
        super().__init__()
        self.getImage(address_ll, delta)
        self.initUI()

    def getImage(self, address_ll, delta):
        map_params = {
            "ll": address_ll,
            "spn": delta,
            "l": "map",
            "pt": f"{address_ll},pm2dgl"
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

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    s = input('Напиши адрес')
    print(get_ll_span(s))
    adress = get_ll_span(s)[0]
    delta = get_ll_span(s)[1]
    app = QApplication(sys.argv)
    ex = Example(adress, delta)
    ex.show()
    sys.exit(app.exec())