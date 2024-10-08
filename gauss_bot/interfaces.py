from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from matrices import OperacionesMatrices
from vectores import OperacionesVectores

STYLESHEET = """
    QWidget {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    QLabel {
        color: #ecf0f1;
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GaussBot")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.main_menu_widget = MainMenuWidget(self)
        self.menu_matriz = MenuMatriz(self)
        self.menu_vector = MenuVector(self)

        self.central_widget.addWidget(self.main_menu_widget)
        self.central_widget.addWidget(self.menu_matriz)
        self.central_widget.addWidget(self.menu_vector)

        self.central_widget.setCurrentWidget(self.main_menu_widget)

    def show_main_menu(self):
        self.central_widget.setCurrentWidget(self.main_menu_widget)

    def show_menu_matriz(self):
        self.central_widget.setCurrentWidget(self.menu_matriz)

    def show_menu_vector(self):
        self.central_widget.setCurrentWidget(self.menu_vector)


class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title_label = QLabel("GaussBot")
        title_label.setFont(QFont("Nunito", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        matrices_button = QPushButton("Menú de Matrices")
        matrices_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        matrices_button.clicked.connect(parent.show_menu_matriz)
        layout.addWidget(matrices_button)

        vectores_button = QPushButton("Menú de Vectores")
        vectores_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        vectores_button.clicked.connect(parent.show_menu_vector)
        layout.addWidget(vectores_button)

        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        close_button.clicked.connect(parent.close)
        layout.addWidget(close_button)


class MenuMatriz(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operaciones Matriciales")
        self.setGeometry(150, 150, 600, 400)

        self.op_mats = OperacionesMatrices()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Operaciones Matriciales")
        label.setFont(QFont("Nunito", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        operations = [
            ("Mostrar matrices", self.op_mats.imprimir_matrices),
            ("Agregar matriz", self.op_mats.agregar_matriz),
            ("Resolver sistema de ecuaciones", self.op_mats.resolver_sistema),
            ("Suma y resta de matrices", self.op_mats.suma_resta_matrices),
            ("Multiplicación de matrices", self.op_mats.mult_matrices),
            ("Transposición de matrices", self.op_mats.transponer),
            ("Regresar al menú principal", parent.show_main_menu)
        ]

        for op_name, op_method in operations:
            button = QPushButton(op_name)
            button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
            button.clicked.connect(op_method)
            layout.addWidget(button)


class MenuVector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operaciones Vectoriales")
        self.setGeometry(150, 150, 600, 400)

        self.op_vecs = OperacionesVectores()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Operaciones Vectoriales")
        label.setFont(QFont("Nunito", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        operations = [
            ("Mostrar vectores", self.op_vecs.imprimir_vectores),
            ("Agregar vector", self.op_vecs.agregar_vector),
            ("Suma y resta de vectores", self.op_vecs.suma_resta_vectores),
            ("Multiplicación escalar", self.op_vecs.mult_escalar),
            ("Producto punto", self.op_vecs.mult_vectorial),
            ("Producto matriz-vector", self.op_vecs.mult_matriz_vector),
            ("Regresar al menú principal", parent.show_main_menu)
        ]

        for op_name, op_method in operations:
            button = QPushButton(op_name)
            button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
            button.clicked.connect(op_method)
            layout.addWidget(button)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    app.exec()