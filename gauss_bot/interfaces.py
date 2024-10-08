from os import path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QVBoxLayout,
    QPushButton, QLabel,
)

from PyQt6.QtGui import QFont, QIcon
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        main_menu_widget = MainMenuWidget()
        layout.addWidget(main_menu_widget)


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
        # matrices_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'matrices.png')))
        matrices_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        matrices_button.clicked.connect(self.operaciones_matrices)
        layout.addWidget(matrices_button)

        vectores_button = QPushButton("Menú de Vectores")
        # vectores_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'vectores.png')))
        vectores_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        vectores_button.clicked.connect(self.operaciones_vectores)
        layout.addWidget(vectores_button)

        close_button = QPushButton("Cerrar")
        # close_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'close.png')))
        close_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        close_button.clicked.connect(self.close_program)
        layout.addWidget(close_button)


    def operaciones_matrices(self):
        self.menu_matriz = MenuMatriz()
        self.menu_matriz.show()

    def operaciones_vectores(self):
        self.menu_vector = MenuVector()
        self.menu_vector.show()

    def close_program(self):
        self.close()


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

        # Add buttons for matrix operations
        operations = [
            ("Mostrar matrices", self.op_mats.imprimir_matrices),
            ("Agregar matriz", self.op_mats.agregar_matriz),
            ("Resolver sistema de ecuaciones", self.op_mats.resolver_sistema),
            ("Suma y resta de matrices", self.op_mats.suma_resta_matrices),
            ("Multiplicación de matrices", self.op_mats.mult_matrices),
            ("Transposición de matrices", self.op_mats.transponer),
            ("Regresar al menú principal", self.close)
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
            ("Regresar al menú principal", self.close)
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