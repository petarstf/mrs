from PySide2 import QtWidgets, QtGui, QtCore
from ..models.calendar_model import CalendarModel
from ..dialogs.add_event_dialog import AddEventDialog
from ..dialogs.remove_event_dialog import RemoveEventDialog
from ..dialogs.error_dialog import ErrorDialog
from ..dialogs.add_label_dialog import AddLabelDialog

class CalendarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.path = ""
        self.path_labels = "C:/Users/Petar Stefanovic/Desktop/singi/I_semestar/MRS/P_1/labels.csv"
        self.model = 0
        self.layout = QtWidgets.QVBoxLayout()
        
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout_1 = QtWidgets.QHBoxLayout()
        self.hbox_layout_2 = QtWidgets.QHBoxLayout()
        self.hbox_layout_3 = QtWidgets.QHBoxLayout()
        
# =============================================================================
#         Buttons
# =============================================================================
        self.open_calendar = QtWidgets.QPushButton(QtGui.QIcon('resources/icons/folder-open-document.png'), 'Open calendar', self)
        self.delete_event = QtWidgets.QPushButton(QtGui.QIcon('resources/icons/cross.png'), 'Remove event', self)
        self.save_event = QtWidgets.QPushButton(QtGui.QIcon('resources/icons/disk.png'), 'Save calendar', self)
        self.create_label = QtWidgets.QPushButton(QtGui.QIcon('resources/icons/application-plus.png'), 'Create label', self)

        self.open_calendar.clicked.connect(self._on_open)
        self.delete_event.clicked.connect(self._on_remove)
        self.save_event.clicked.connect(self._on_save)
        self.create_label.clicked.connect(self._on_create_label)

      
# =============================================================================
#         Kalendar
# =============================================================================
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setGridVisible(True)
        self.calendar.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget().HorizontalHeaderFormat(3))
        
        # format = QtGui.QTextCharFormat()
        # format.setFontCapitalization(QtGui.QFont().Capitalization(1))
        # self.calendar.setHeaderTextFormat(format)
        
        self.calendar.setStyleSheet('background: white; color: black; font: 15px')
        self.calendar.setWindowTitle('Calendar Widget')
        
        # self.calendar.mousePressEvent()

        # rmb = QtGui.QMouseEvent(QtCore.QPoint(QtGui.QMouseEvent().globalX(), QtGui.QMouseEvent().globalY()))
        # print(rmb)
# =============================================================================
#         Current Date
# =============================================================================
        self.current_date = QtWidgets.QDateEdit()
        self.current_date.setDisplayFormat('dd MMM yyyy')
        self.current_date.setDate(self.calendar.selectedDate())
        self.current_date.dateChanged.connect(self.calendar.setSelectedDate)
        

        self.current_date.setStyleSheet('font: 15px bold')
        # self.calendar.selectionChanged.connect(self.selected_date_change)
        # self.calendar.selectionChanged.connect(self.table_change)
# =============================================================================
#         Pravimo apstraktni View preko kalendara kako bi omogucili otvaranje meni-ja na RMB
# =============================================================================
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_view.setStyleSheet('font: 15px')


        self.hbox_layout_1.addWidget(self.open_calendar)
        self.hbox_layout_1.addWidget(self.delete_event)
        self.hbox_layout_1.addWidget(self.save_event)
        self.hbox_layout_1.addWidget(self.create_label)
        self.hbox_layout_2.addWidget(self.current_date)
        self.hbox_layout_3.addWidget(self.calendar)
        self.vbox_layout.addLayout(self.hbox_layout_1)
        self.vbox_layout.addLayout(self.hbox_layout_2)
        self.vbox_layout.addLayout(self.hbox_layout_3)
        self.vbox_layout.addWidget(self.table_view, 1, 0)

        self.layout.addLayout(self.vbox_layout)
        self.setLayout(self.layout)



        self._table = self.calendar.findChild(QtWidgets.QTableView)
        self._table.setMouseTracking(True)
        self._table.viewport().installEventFilter(self)

        self.single_click_timer = QtCore.QTimer()
        self.single_click_timer.setInterval(200)
        # self.single_click_timer.timeout.connect(self.single_click)
# =============================================================================
#         Funkcije
# =============================================================================

    def set_model(self, model):
        self.table_view.setModel(model)
        self.model = model

    def _on_open(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open calendars file', '.', 'CSV files (*.csv)')
        self.set_model(CalendarModel(path[0]))
        self.path = path[0]
        print(self.path)

    def _on_save(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save calendar file", ".", "CSV Files (*.csv)")
        self.table_view.model().save_data(path[0])
    
    def _on_remove(self):
        self.table_view.model().remove(self.table_view.selectedIndexes())

    def _on_add(self):
        #selected_date = selected_date.toString('dd MMM yyyy')
        self.selected_date = self.calendar.selectedDate()
        if self.path == "":
            dialog = ErrorDialog(self.parent())
        else:
            model = self.set_model(CalendarModel(self.path))
            self.model_day(self.selected_date)
            dialog = AddEventDialog(self.parent(), self.selected_date, self.path)
        dialog.show()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_view.model().add(dialog.get_data())
            self._on_save

    def _on_delete(self):
        self.selected_date = self.calendar.selectedDate()
        if self.path == "":
            dialog = ErrorDialog(self.parent())
        else:
            model = self.set_model(CalendarModel(self.path))
            self.model_day(self.selected_date)
            dialog = RemoveEventDialog(self.parent(), self.selected_date, self.model, self.path)
        dialog.show()

    def _on_create_label(self):
        if self.path == "":
            dialog = ErrorDialog(self.parent())
        else:
            model = self.set_model(CalendarModel(self.path))
            # self.model_day(self.selected_date)
            dialog = AddLabelDialog(self.parent(), self.path_labels)
        dialog.show()

    def selected_date_change(self):
        self.current_date.setDate(self.calendar.selectedDate())
        
    def table_change(self):
        self.selected_date = self.calendar.selectedDate()
        if(self.model):
            if((self.model.get_elements_date(self.calendar.selectedDate())) == []):
                return;
            model = self.set_model(CalendarModel(self.path))
            self.model_day(self.selected_date)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if self.model:
                model = self.set_model(CalendarModel(self.path))
            index = self._table.indexAt(event.pos())
            current_date = QtCore.QDate(self.calendar.yearShown(), self.calendar.monthShown(), index.data())
            self.current_date.setDate(current_date)
            if event.button() == QtCore.Qt.RightButton:
                if self.model:
                    self.selected_date = current_date
                    model = self.set_model(CalendarModel(self.path))
                    self.model_day(self.selected_date)
                self.context_menu = QtWidgets.QMenu()
                self.action_add = QtWidgets.QAction('Add event', self)
                self.action_delete = QtWidgets.QAction('Delete event', self)
                self.context_menu.addAction(self.action_add)
                self.context_menu.addAction(self.action_delete)
                self.action_add.triggered.connect(self._on_add)
                self.action_delete.triggered.connect(self._on_delete)
                self.context_menu.exec_(QtCore.QPoint(event.globalX(), event.globalY()))
                return True
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                self._on_add()
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.model:
                index = self._table.indexAt(event.pos())
                current_date = QtCore.QDate(self.calendar.yearShown(), self.calendar.monthShown(), index.data())
                model = self.set_model(CalendarModel(self.path))
                # self.model_day(current_date)
                if(self.model._data) == []:
                    model = self.set_model(CalendarModel(self.path))
            

        return False

    def model_day(self, date):
        self.model._data = (self.model.get_elements_date(date))
    

