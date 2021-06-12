from sys import exit as sysExit
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox, \
    QMdiSubWindow, QDateTimeEdit
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

class Widget(QWidget):
    switch_window = pyqtSignal()
    global db
    def __init__(self):
        super().__init__()
        self.GUI()

    def GUI(self):
        self.setWindowTitle('Trang chủ')
        self.setGeometry(200, 200, 1180, 685)

        self.vlayout = QVBoxLayout()
        self.gbox = QGroupBox()
        self.gbox.setMaximumSize(800, 800)
        self.gbox.setGeometry(100, 100, 300, 300)
        self.TT = QLabel('Thông tin cá nhân',self)
        self.TT.setAlignment(Qt.AlignCenter)
        self.TT.setStyleSheet("font-size: 25px ")
        font = QFont()
        font.setBold(True)
        self.TT.setFont(font)
        self.TT.setGeometry(100, 20, 100, 100)
        #self.gbox.setMinimumSize(100, 100)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.lbMNV = QLabel('Mã nhân viên', self)
        self.grid.addWidget(self.lbMNV, 1, 0)
        self.txtMNV = QLabel(self)
        self.txtMNV.setText(self.tim().record(0).value(0))
        self.grid.addWidget(self.txtMNV, 1, 1)

        # Ho va ten nhan vien
        self.lbHoten = QLabel('Họ và tên', self)
        self.grid.addWidget(self.lbHoten, 2, 0)
        self.txtHoten = QLineEdit(self)
        self.txtHoten.setText(self.tim().record(0).value(1))
        self.grid.addWidget(self.txtHoten, 2, 1)
        self.lbstHoten = QLabel("", self)
        self.grid.addWidget(self.lbstHoten, 3, 0)
        self.gbox.setLayout(self.grid)
        #self.vlayout.addLayout(self.gbox)

        # Radio gioi tinh
        self.lbGioiTinh = QLabel('Giới tính', self)
        self.grid.addWidget(self.lbGioiTinh, 4, 0)
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
        self.grid.addWidget(self.gb, 4, 1)

        # Ngay sinh
        self.lbNgaySinh = QLabel('Ngày sinh', self)
        self.grid.addWidget(self.lbNgaySinh, 5, 0)
        #self.txtNgaySinh = QLineEdit(self)
        #self.txtNgaySinh.setText(self.tim().record(0).value(2))
        #self.grid.addWidget(self.txtNgaySinh, 4, 1)
        self.gb_NS = QGroupBox()
        self.qdate = QDate().fromString(self.tim().record(0).value(2), "yyyy-MM-dd")

        self.lbNgay = QLabel("Ngày:", self)
        self.dateedit_day = QDateTimeEdit(self.qdate, self)
        self.dateedit_day.setDisplayFormat("dd")

        self.lbThang = QLabel("Tháng:", self)
        self.dateedit_month = QDateTimeEdit(self.qdate, self)
        self.dateedit_month.setDisplayFormat("MM")

        self.lbNam = QLabel("Năm:", self)
        self.dateedit_year = QDateTimeEdit(self.qdate, self)
        self.dateedit_year.setDisplayFormat("yyyy")

        self.hbox_NS = QHBoxLayout()
        self.hbox_NS.setSpacing(30)
        self.hbox_NS.addWidget(self.lbNgay)
        self.hbox_NS.addWidget(self.dateedit_day)
        self.hbox_NS.addWidget(self.lbThang)
        self.hbox_NS.addWidget(self.dateedit_month)
        self.hbox_NS.addWidget(self.lbNam)
        self.hbox_NS.addWidget(self.dateedit_year)

        self.gb_NS.setLayout(self.hbox_NS)
        self.grid.addWidget(self.gb_NS, 5, 1)
        self.lbstNgaySinh = QLabel("", self)
        self.grid.addWidget(self.lbstNgaySinh, 6, 0)

        # Chuc vu
        self.lbChucVu = QLabel('Chức vụ', self)
        self.grid.addWidget(self.lbChucVu, 7, 0)
        self.txtChucVu = QLabel(self)
        if self.tim().record(0).value(5) == 1:
            self.txtChucVu.setText("Trưởng phòng")
        else:
            self.txtChucVu.setText("Nhân viên")
        self.grid.addWidget(self.txtChucVu, 7, 1)

        # Tien ngay
        self.lbTienNgay = QLabel('Tiền ngày', self)
        self.grid.addWidget(self.lbTienNgay, 8, 0)
        self.txtTienNgay = QLineEdit(self)
        self.txtTienNgay.setText((str)(self.tim().record(0).value(3)))
        self.grid.addWidget(self.txtTienNgay, 8, 1)
        self.lbstTienNgay = QLabel('', self)
        self.grid.addWidget(self.lbstTienNgay, 9, 0)








        #self.btnLogout.click.connect(self.logout)







    def tim(self):
        if createConnection():
            query = QSqlQuery(db)
            sql = "select MaNV, HoTen, NgaySinh, TienNgay, GioiTinh, VaiTro from NhanVien where MaNV = '"+ TaiKhoan.getMaNV(TaiKhoan) +"'"
            query.prepare(sql)
            query.exec()

        model = QSqlQueryModel()
        model.setQuery(query)
        return model

    def Sua(self):
        if createConnection():
            gioitinh = '0'
            if (self.RdbNam.isChecked()):
                gioitinh = '1'
            query = QSqlQuery(db)
            sql = "update nhanvien set Hoten = N'" + self.txtHoten.text() + "', NgaySinh ='" + self.txtNgaySinh.text() + "', TienNgay =" +self.txtTienNgay.text() +"," \
                " GioiTinh = " +gioitinh + " where MaNV = '"+TaiKhoan.getMaNV(TaiKhoan)+"'"
            query.prepare(sql)
            query.exec()
            mb = QMessageBox.information(self, 'Thông báo', 'Cập nhật thành công!', QMessageBox.Ok, QMessageBox.Ok)
        else:
            mb = QMessageBox.Warning(self, 'Lỗi', 'Cập nhật thất bại!', QMessageBox.Ok, QMessageBox.Ok)

    def logout(self):
        self.switch_window.emit()
        self.close()




