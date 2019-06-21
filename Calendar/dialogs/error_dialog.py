from PySide2 import QtWidgets, QtGui, QtCore

class ErrorDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Warning')
        self.resize(100, 100)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setText('There has been an error!\nCheck file path.')
        self.label.setStyleSheet('background: white; color: black; font: 15px; margin: auto; text-align: center;')
        self.setStyleSheet('font: bold 15px; background: white;')
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        