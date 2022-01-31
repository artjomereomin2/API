import os
import sys

from PyQt5 import uic

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [350,450]

import requests


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.spn_x, self.spn_y = 10,10
        self.initUI()

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        print(123)

        lat = self.wight.text()
        lon = self.longitude.text()

        print(lon,lat)

        if not lat:
            lat = 55.703118
        else:
            lat = float(lat)
        if not lon:
            lon = 7.530887
        else:
            lon = float(lon)


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

        pixmap = QPixmap(self.map_file)
        self.image.setPixmap(pixmap)

    def initUI(self):
        super().__init__()
        uic.loadUi('01.ui', self)

        self.image = QLabel(self)

        self.getImage()

        pixmap = QPixmap(self.map_file)

        self.image.move(0, 200)
        self.image.resize(SCREEN_SIZE[0],SCREEN_SIZE[1]-200)
        self.image.setPixmap(pixmap)

        self.button_to_teleport.clicked.connect(self.getImage)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
