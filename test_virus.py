import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class Virus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(600, 100, 300, 100)
        self.setWindowTitle('Get Jebaited')
        self.message = QLabel('Je je je je jebaited', self)
        self.message.move(100, 25)
        self.message.resize(150, 50)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vir = Virus()
    vir.show()
    sys.exit(app.exec())