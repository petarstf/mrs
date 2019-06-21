from PySide2 import QtWidgets, QtGui, QtCore
import csv

class AddLabelDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, path=None):
        super().__init__(parent)

        self.path = path
        self.setWindowTitle("Create a label")
        
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.name_input = QtWidgets.QLineEdit(self)
        self.color = ''

        self.color_input = QtWidgets.QPushButton(QtGui.QIcon('resources/icons/application-plus.png'), 'Pick a color', self)
        self.color_input.clicked.connect(self._on_color)
        
        

        self.form_layout.addRow('Name: ', self.name_input)
        self.form_layout.addRow('Color: ', self.color_input)
        
        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        
        children = self.vbox_layout.children()
        self.setStyleSheet('font: 15px')
        self.setLayout(self.vbox_layout)
        
    def _on_color(self):
        if self.path == "":
            dialog = ErrorDialog(self.parent())
        else:
            # model = self.set_model(CalendarModel(self.path))
            # self.model_day(self.selected_date)
            dialog = QtWidgets.QColorDialog(self.parent(), self.path)
            self.color = QtWidgets.QColorDialog(self.parent(), self.path).getColor()
            print(self.color)
        dialog.show()

    def _on_accept(self):
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 'Missing name', "Name input field can't be empty", QtWidgets.QMessageBox.Ok)
            return
            
        with open(self.path, 'a' , encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            print(self.name_input.text().strip(), self.color)
            myCsvRow = [self.name_input.text().strip(), self.color]
            writer.writerow(myCsvRow)
        self.accept()

    def get_data(self):
        # with open(self.path, 'a' , encoding="utf-8") as fp:
        #     writer = csv.writer(fp, dialect=csv.unix_dialect)
        #     print(self.name_input.text().strip(), self.color)
        #     myCsvRow = [self.name_input.text().strip(), self.color]
        #     writer.writerow(myCsvRow)
        return {
            'name' : self.name_input.text(),
            'color' : self.color,
        }

    def _on_reject(self):
        return {
            'name' : self.name_input.text(),
            'desc' : self.desc_input.toPlainText(),
            'frequency' : self.iterator_input.currentText(),            
            'date' : self.date_input.text()
        }    


    