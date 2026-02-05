import sys
import requests
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yandex Maps API (PyQt6)")
        self.setFixedSize(600, 450)

        self.lon = 37.620070      # долгота
        self.lat = 55.753630      # широта
        self.zoom = 10            # масштаб (0–17)
        self.map_type = "map"     # map | sat | skl

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(self.size())

        self.load_map()

    def load_map(self):
        url = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.zoom,
            "l": self.map_type,
            "size": "600,450"
        }

        response = requests.get(url)
        response = requests.get(url, params=params)

        with open("map.png", "wb") as f:
            f.write(response.content)

        pixmap = QPixmap("map.png")
        self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
