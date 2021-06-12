from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox, \
    QMdiSubWindow
from Update import update

SERVER_NAME = 'PC\SQLEXPRESS'
DATABASE_NAME = 'DoAn1'
USERNAME = ''
PASSWORD = ''

def createConnection():
    conn = f'DRIVER={{SQL Server}};' \
           f'SERVER={SERVER_NAME};' \
           f'DATABASE={DATABASE_NAME}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(conn)

    if db.open():
        #print('Ket noi thanh cong')
        return True
    else:
        #print('Ket noi that bai')
        return False

class Update_Info(QMainWindow):
    switch_window = pyqtSignal()

    global db
    def __init__(self, parent=None):
        super(Update_Info, self).__init__(parent)
        self.search()

    def search(self):
        self.setWindowTitle('Tìm kiếm nhân viên')
        self.setGeometry(400, 200, 700, 200)

        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.vlayout = QVBoxLayout()


        self.lbTim = QLabel('Mã nhân viên', self)
        self.grid.addWidget(self.lbTim, 1, 1)

        self.txtTim = QLineEdit(self)
        self.grid.addWidget(self.txtTim, 1, 2)

        self.btnTim = QPushButton('Tìm', self)
        self.grid.addWidget(self.btnTim, 1, 3)
        self.btnTim.clicked.connect(self.btnTim_click)

        self.vlayout.addLayout(self.grid)
        widLayout = QWidget()
        widLayout.setLayout(self.vlayout)
        self.setCentralWidget(widLayout)
        self.show()


    def btnTim_click(self):
        self.dialog = update(self.txtTim.text())


    def conn(self):
        self.switch_window.emit()









