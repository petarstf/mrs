from PySide2 import QtWidgets, QtGui, QtCore
import csv

class AddEventDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, selected_date=None, path=None):
        super().__init__(parent)

        self.path = path
        self.setWindowTitle("Add event")
        
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.name_input = QtWidgets.QLineEdit(self)

        self.desc_input = QtWidgets.QTextEdit(self)
        self.desc_input.setTabChangesFocus(True)

        self.selected_date = selected_date
        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setDisplayFormat('d.M.yyyy.')
        if self.selected_date != None:
            self.date_input.setDate(selected_date)

        self.iterator_input = QtWidgets.QComboBox()
        self.iterator_input.setStyleSheet('background: white;')
        self.iterator_input.addItem('One time')
        self.iterator_input.addItem('Daily')
        self.iterator_input.addItem('Weekly')
        self.iterator_input.addItem('Monthly')
        self.iterator_input.addItem('Annualy')

        self.form_layout.addRow('Name: ', self.name_input)
        self.form_layout.addRow('Description: ', self.desc_input)
        self.form_layout.addRow('Date: ', self.date_input)
        self.form_layout.addRow('Frequency: ', self.iterator_input)
        
        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        
        children = self.vbox_layout.children()
        self.setStyleSheet('font: 15px')
        self.setLayout(self.vbox_layout)
        

    def _on_accept(self):
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 'Missing name', "Name input field can't be empty", QtWidgets.QMessageBox.Ok)
            return
        if self.desc_input.toPlainText() == '':
            QtWidgets.QMessageBox.warning(self, 'Missing description', "Description input field can't be empty", QtWidgets.QMessageBox.Ok)
            return
        self.accept()

    def get_data(self):
        with open(self.path, 'a' , encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            print(self.name_input.text().strip() , self.desc_input.toPlainText(), self.iterator_input.currentText(), self.date_input.text())
            myCsvRow = [self.name_input.text().strip() , self.desc_input.toPlainText(), self.iterator_input.currentText(), self.date_input.text()]
            writer.writerow(myCsvRow)
        return {
            'name' : self.name_input.text(),
            'desc' : self.desc_input.toPlainText(),
            'frequency' : self.iterator_input.currentText(),            
            'date' : self.date_input.text()
        }

    def _on_reject(self):
        return {
            'name' : self.name_input.text(),
            'desc' : self.desc_input.toPlainText(),
            'frequency' : self.iterator_input.currentText(),            
            'date' : self.date_input.text()
        }    


    