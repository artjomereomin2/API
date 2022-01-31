import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]

import requests



class Example(QWidget):
    def init(self):
        super().init()
        self.getImage()
        self.initUI()

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = 37.530887
        lat = 55.703118
        spn_x = 0.005
        spn_y = 0.005

        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn_x), str(spn_y)]),
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


if name == 'main':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())