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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GaussBot")
        self.setGeometry(100, 100, 800, 600)

        # Set up the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Set up the layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Add the main menu widget
        main_menu_widget = MainMenuWidget()
        layout.addWidget(main_menu_widget)


class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title label
        title_label = QLabel("GaussBot")
        title_label.setFont(QFont("Nunito", 24))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Buttons with icons
        matrices_button = QPushButton("Operaciones de matrices")
        matrices_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'matrices.png')))
        matrices_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        matrices_button.clicked.connect(self.matrices_operations)
        layout.addWidget(matrices_button)

        vectores_button = QPushButton("Operaciones de vectores")
        vectores_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'vectores.png')))
        vectores_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        vectores_button.clicked.connect(self.vectores_operations)
        layout.addWidget(vectores_button)

        close_button = QPushButton("Cerrar programa")
        close_button.setIcon(QIcon(path.join('gauss_bot', 'icons', 'close.png')))
        close_button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
        close_button.clicked.connect(self.close_program)
        layout.addWidget(close_button)

        # Apply a stylesheet to the entire widget
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def matrices_operations(self):
        self.matrix_menu = MenuMatriz()
        self.matrix_menu.show()

    def vectores_operations(self):
        self.vector_menu = MenuVector()
        self.vector_menu.show()

    def close_program(self):
        self.close()

class MenuMatriz(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matrix Operations")
        self.setGeometry(150, 150, 600, 400)

        self.op_mat = OperacionesMatrices()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Matrix Operations Menu")
        label.setFont(QFont("Nunito", 20))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add buttons for matrix operations
        operations = [
            ("Agregar matriz", self.mat.agregar_matriz),
            ("Resolver sistema de ecuaciones", self.mat.resolver_sistema),
            ("Suma y resta de matrices", self.mat.suma_resta_matrices),
            ("Multiplicación de matrices", self.mat.mult_matrices),
            ("Transposición de matrices", self.mat.transponer),
            ("Regresar al menú principal", self.close)
        ]

        for op_name, op_method in operations:
            button = QPushButton(op_name)
            button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
            button.clicked.connect(op_method)
            layout.addWidget(button)

        # Apply the same stylesheet as the main menu
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)


class MenuVector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operaciones Vectoriales")
        self.setGeometry(150, 150, 600, 400)

        self.vec = OperacionesVectores()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Menu Operaciones Vectoriales")
        label.setFont(QFont("Nunito", 20))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Add buttons for vector operations
        operations = [
            ("Agregar un vector", self.vec.agregar_vector),
            ("Suma y resta de vectores", self.vec.suma_resta_vectores),
            ("Multiplicación escalar", self.vec.mult_escalar),
            ("Producto punto", self.vec.mult_vectorial),
            ("Producto matriz-vector", self.vec.mult_matriz_vector),
            ("Regresar al menú principal", self.close)
        ]

        for op_name, op_method in operations:
            button = QPushButton(op_name)
            button.setStyleSheet("QPushButton { font-size: 18px; padding: 10px; }")
            button.clicked.connect(op_method)
            layout.addWidget(button)

        # Apply the same stylesheet as the main menu
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()