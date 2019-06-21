from PySide2 import QtCore, QtGui, QtWidgets
import csv

class RemoveEventDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, selected_date=None, model=None, path=None):
        super().__init__(parent)

        self.setWindowTitle("Delete event")
        self.resize(550, 400)

        self.path = path
        self.events = model._data
        self.model = model
        
        
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        # self.selected_date = selected_date
        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setDisplayFormat('d.M.yyyy.')
        if selected_date != None:
            self.date_input.setDate(selected_date)
        
        
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setModel(model)
        

        self.form_layout.addRow(self.date_input)
        self.vbox_layout.addWidget(self.table_view)
        
        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)
        
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)   
        
        self.setLayout(self.vbox_layout)
            

    def _on_accept(self):
        # Dohvatimo index selektovanog reda za brisanje
        indices = sorted(set(map(lambda x: x.row(), self.table_view.selectedIndexes())), reverse=True)
        indice = indices[0]
        with open(self.path, encoding='utf-8') as inf:
            reader = csv.reader(inf.readlines(), dialect=csv.unix_dialect)

        with open(self.path, "w", encoding='utf-8') as outf:
            writer = csv.writer(outf, dialect=csv.unix_dialect)
            for line in reader:
                # poredimo prvi clan linije u csv-u koji je ime dogadjaja sa dogadjajem selektovanim za brisanje
                if line[0] == self.events[indice][0]:
                    continue
                else:
                    writer.writerow(line)

        self.accept()

    def _on_reject(self):
        pass

    def get_data(self):
        with open(self.path, 'a' , encoding="utf-8") as fp:
            print(self.path)
            events = csv.reader(fp, dialect=csv.unix_dialect)
            print(events)
        return {
            'name' : self.name_input.text(),
            'desc' : self.desc_input.toPlainText(),
            'frequency' : self.iterator_input.currentText(),            
            'date' : self.date_input.text()
        }        