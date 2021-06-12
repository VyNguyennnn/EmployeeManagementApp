from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox
from TaiKhoan import TaiKhoan
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

class Login(QMainWindow):
    switch_window = pyqtSignal()
    switch_window2 = pyqtSignal()
    #global db
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.GUI()

    def GUI(self):
        self.setWindowTitle('Đăng nhập')
        self.setGeometry(20, 20, 380, 200)
        self.statusBar().showMessage("")

        self.vlayout = QVBoxLayout()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # User
        self.lbUser = QLabel('Tên tài khoản', self)
        self.grid.addWidget(self.lbUser, 1, 0)
        self.txtUser = QLineEdit(self)
        self.grid.addWidget(self.txtUser,1,1)


        # Password
        self.lbPwd = QLabel('Mật khẩu', self)
        self.grid.addWidget(self.lbPwd,2,0)
        self.txtPwd = QLineEdit(self)
        self.txtPwd.setEchoMode(QLineEdit.Password)
        self.grid.addWidget(self.txtPwd,2,1)
        self.vlayout.addLayout(self.grid)


        self.hbox = QHBoxLayout(self)
        self.btnDN = QPushButton('Đăng nhập', self)
        self.btnDN.clicked.connect(self.checkLogin)
        self.hbox.addWidget(self.btnDN)
        self.btnThoat = QPushButton('Thoát', self)
        self.btnThoat.clicked.connect(self.close)
        self.hbox.addWidget(self.btnThoat)
        self.vlayout.addLayout(self.hbox)


        widLayout = QWidget()
        widLayout.setLayout(self.vlayout)
        self.setCentralWidget(widLayout)
        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def checkLogin(self):
        if createConnection():
                self.user = self.txtUser.text()
                self.pwd = self.txtPwd.text()
                if (self.user.isalnum()):
                    if (self.tim().record(0).value(0) == None):
                        print('User hoac Password khong dung')
                        self.statusBar().setStyleSheet("color: red")
                        self.statusBar().showMessage("Tên đăng nhập hoặc mật khẩu không đúng!")
                        self.txtUser.clear()
                        self.txtPwd.clear()

                    else:
                        print('Dang nhap thanh cong')
                        if (self.tim_Vaitro().record(0).value(0) ==1):
                            self.Login_Succ()
                            self.open_Home()
                        else:
                            self.Login_Succ()
                            self.open_Home_NV()




                else:
                    print('Tên đăng nhập không bao gồm ký tự đặc biệt hoặc khoảng trắng!')
                    self.statusBar().setStyleSheet("color: red")
                    self.statusBar().showMessage("Tên đăng nhập không bao gồm ký tự đặc biệt hoặc khoảng trắng!")
                    self.txtUser.clear()
                    self.txtPwd.clear()

    def open_Home(self):
        self.switch_window.emit()
    def open_Home_NV(self):
        self.switch_window2.emit()

    def tim(self):
        query = QSqlQuery(db)
        sql = "select MaNV from NhanVien where " \
              "MaNV = '" + self.user + "' and Pwd = '" + self.pwd + "'"
        query.prepare(sql)
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        return model

    def tim_Vaitro(self):
        query = QSqlQuery(db)
        sql = "select VaiTro from NhanVien where MaNV = '"+self.user+"'"
        query.prepare(sql)
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        return model

    def Login_Succ(self):
        TaiKhoan.setMaNV(TaiKhoan, self.txtUser.text())









