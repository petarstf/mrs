from PySide2 import QtCore
import csv
import os

class CalendarModel(QtCore.QAbstractTableModel):
    def __init__(self, path=""):
        super().__init__()
        self._data = []
        self.load_data(path)

    def data(self, index, role):
        element = self.get_element(index)
        if element is None:
            return None
        if role == QtCore.Qt.DisplayRole:
            return element
    
    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return 'Name'
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return 'Description'
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return 'Frequency'
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return 'Date'

    def add(self, data : dict):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data['name'], data['desc'], data['frequency'], data['date']])
        self.endInsertRows()
        
    def remove(self, indices):
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()
        
    def get_element(self, index : QtCore.QModelIndex):
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None
    
    def get_elements_date(self, date):
        elements = []
        date = date.toString('d.M.yyyy.')
        for index in range(len(self._data)):
            element = self._data[index][3]
            if (element and (element == date)):
                # print("Same")
                elements.append(self._data[index])
        return elements

    def get_elements_frequency(self):
        dates = []
        for index in range(len(self._data)):
            frequency = self._data[index][2]
            date = self._data[index][3]
            first_dot = date.find('.')
            second_dot = date.index('.', first_dot+1)

            day = int(date[:first_dot])
            month = int(date[first_dot+1:second_dot])
            year = 2019
            if frequency == "Daily":
                dates = self.increment_daily(day, month, year)
            if frequency == "Monthly":
                dates = self.increment_monthly(day, month, year)
        return dates

    def load_data(self, path=""):
        with open(path, 'r', encoding='utf-8') as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def load_data_array(self, arr):
        self._data = list()
            
    def save_data(self, path=''):
        with open(path, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for row in self._data:
                writer.writerow(row)

    def flags(self, index):
        """
        Vraca flagove koji su aktivni za dati indeks modela.
        Ova metoda je vazna ako zelimo da nas model moze da se menja.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- flagovi koji treba da budu aktivirani.
        """
        # ne damo da menja datum rodjenja (primera radi)
        if index.column() != 4: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # sve ostale podatke korisnik moze da menja
        else: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def increment_daily(self, day, month, year):
        array = []
        for i in range(364):
            day = int(day)
            month = int(month)
            year = str(year)
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                if day == 31:
                    month += 1
                    if month == 13:
                        month = 1
                    day = 1
                    month = str(month)

                else:
                    day += 1
                    day = str(day)
            else:
                if day == 30:
                    month += 1
                    if month == 13:
                        month = 1
                    day = 1
                    month = str(month)
                else:
                    day += 1
            day = str(day)
            month = str(month)
            array.append(day+'.'+month+'.'+year+'.')
            
    def increment_weekly(day, month, year, array):
        for i in range(51):
            day = int(day)
            month = int(month)
            year = int(year)
            
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day += 7
                if day > 31:
                    day -= 31
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
            else:
                day += 7
                if day > 30:
                    day -= 30
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
            day = str(day)
            month = str(month)
            year = str(year)
            array.append(day+'.'+month+'.'+year+'.')


    def increment_monthly(self, day, month, year):
        array = []
        for i in range(12):
            month = int(month)
            month += 1
            if month == 13:
                month = 1
                year = int(year)
                year += 1
            day = str(day)
            month = str(month)
            year = str(year)
            array.append(day+'.'+month+'.'+year+'.')
        return array
