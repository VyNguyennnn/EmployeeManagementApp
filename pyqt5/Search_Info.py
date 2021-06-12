from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMdiSubWindow, QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox

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


class Search_Info(QMdiSubWindow):
    global db
    def __init__(self, listInfo, parent = None):
        super().__init__(parent)
        self.MaNV = listInfo
        self.GUIIn()

    def GUIIn(self):
        self.setWindowTitle('Thông tin nhân viên')
        self.setGeometry(400, 200, 400, 300)

        self.vlayout = QVBoxLayout()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        if (self.check()):
            mb = QMessageBox.information(self,'Thông báo', 'Không có nhân viên này!', QMessageBox.Ok, QMessageBox.Ok)
        else:
            # Ma nhan vien
            self.lbMNV = QLabel('Mã nhân viên', self)
            self.grid.addWidget(self.lbMNV, 1, 0)
            self.txtMNV = QLineEdit(self)
            self.txtMNV.setText(self.tim().record(0).value(0))
            self.grid.addWidget(self.txtMNV, 1, 1)

            # Ho va ten nhan vien
            self.lbHoten = QLabel('Họ và tên', self)
            self.grid.addWidget(self.lbHoten, 2, 0)
            self.txtHoten = QLineEdit(self)
            self.txtHoten.setText(self.tim().record(0).value(1))
            self.grid.addWidget(self.txtHoten, 2, 1)
            self.vlayout.addLayout(self.grid)

            # Radio gioi tinh
            self.lbGioiTinh = QLabel('Giới tính', self)
            self.grid.addWidget(self.lbGioiTinh, 3, 0)
            self.gb = QGroupBox()
            self.RdbNam = QRadioButton('Nam', self)
            self.RdbNu = QRadioButton('Nữ', self)
            if (self.tim().record(0).value(4) == 1):
                self.RdbNam.setChecked(True)
            else:
                self.RdbNu.setChecked(True)

            self.hbox = QHBoxLayout()
            self.hbox.addWidget(self.RdbNam)
            self.hbox.addWidget(self.RdbNu)
            self.gb.setLayout(self.hbox)
            self.grid.addWidget(self.gb, 3, 1)

            # Ngay sinh
            self.lbNgaySinh = QLabel('Ngày sinh', self)
            self.grid.addWidget(self.lbNgaySinh, 4, 0)
            self.txtNgaySinh = QLineEdit(self)
            self.txtNgaySinh.setText(self.tim().record(0).value(2))
            self.grid.addWidget(self.txtNgaySinh, 4, 1)

            # Chuc vu
            self.lbChucVu = QLabel('Chức vụ', self)
            self.grid.addWidget(self.lbChucVu, 5, 0)
            self.cmb = QComboBox(self)
            self.cmb.addItems(['Không có chức vụ', 'Trưởng phòng'])
            self.grid.addWidget(self.cmb, 5, 1)
            if self.tim().record(0).value(5) == 1:
                self.cmb.setCurrentIndex(1)
            else:
                self.cmb.setCurrentIndex(0)

            # Tien ngay
            self.lbTienNgay = QLabel('Tiền ngày', self)
            self.grid.addWidget(self.lbTienNgay, 6, 0)
            self.txtTienNgay = QLineEdit(self)
            self.txtTienNgay.setText((str)(self.tim().record(0).value(3)))
            self.grid.addWidget(self.txtTienNgay, 6, 1)

            self.btnThoat = QPushButton('Thoát')
            self.btnThoat.clicked.connect(self.showMinimized)

            self.vlayout.addLayout(self.grid)
            #self.vlayout.addWidget(self.btnThoat)
            widLayout = QWidget()
            widLayout.setLayout(self.vlayout)


            self.setWidget(widLayout)
            self.show()

    def tim(self):
        if createConnection():
            query = QSqlQuery(db)
            sql = "select MaNV, HoTen, NgaySinh, TienNgay, GioiTinh, VaiTro from NhanVien where MaNV = '"+self.MaNV+"'"
            query.prepare(sql)
            query.exec()

        model = QSqlQueryModel()
        model.setQuery(query)
        return model

    def check(self):
        if ((self.tim().record(0).value(0) == None) or self.MaNV == None):
            return True
        return False





