import os
import sys

from PyQt5 import uic

from random import randrange as r
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]

import requests


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.spn_x, self.spn_y = 10,10
        self.initUI()

    def getImage(self, running=True):
        api_server = "http://static-maps.yandex.ru/1.x/"

        if running:

            lat = self.wight.text()
            lon = self.longitude.text()

            if not lat:
                lat = 0
            if not lon:
                lon = 0
        else:
            lon = 55.703118
            lat = 7.530887

        print(lon,lat)

        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(self.spn_x), str(self.spn_y)]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        super().__init__()
        uic.loadUi('01.ui', self)

        self.getImage(False)
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 600)
        self.image.setPixmap(self.pixmap)

        self.button_to_teleport.clicked.connect(self.getImage)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
