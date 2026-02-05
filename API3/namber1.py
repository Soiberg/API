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

        # === ПАРАМЕТРЫ КАРТЫ ===
        self.lon = 37.620070
        self.lat = 55.753630
        self.zoom = 10

        self.min_zoom = 0
        self.max_zoom = 17

        self.min_lon = -180
        self.max_lon = 180
        self.min_lat = -85
        self.max_lat = 85

        self.map_type = "map"

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

        response = requests.get(url, params=params)
        with open("map.png", "wb") as f:
            f.write(response.content)

        self.label.setPixmap(QPixmap("map.png"))

    def move_map(self, dx, dy):
        self.lon = min(max(self.lon + dx, self.min_lon), self.max_lon)
        self.lat = min(max(self.lat + dy, self.min_lat), self.max_lat)
        self.load_map()

    def keyPressEvent(self, event):
        step = 0.5 / (2 ** self.zoom) * 100  # шаг меньше экрана

        if event.key() == Qt.Key.Key_PageUp and self.zoom < self.max_zoom:
            self.zoom += 1
            self.load_map()

        elif event.key() == Qt.Key.Key_PageDown and self.zoom > self.min_zoom:
            self.zoom -= 1
            self.load_map()

        elif event.key() == Qt.Key.Key_Up:
            self.move_map(0, step)

        elif event.key() == Qt.Key.Key_Down:
            self.move_map(0, -step)

        elif event.key() == Qt.Key.Key_Right:
            self.move_map(step, 0)

        elif event.key() == Qt.Key.Key_Left:
            self.move_map(-step, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
