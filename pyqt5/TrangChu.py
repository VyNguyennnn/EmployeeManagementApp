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

class TrangChu(QMdiSubWindow):
    switch_window = pyqtSignal()
    global db
    def __init__(self):
        super().__init__()
        self.TrangChu()

    def TrangChu(self):
        self.setWindowTitle('Trang chủ')
        self.setGeometry(200, 200, 1180, 685)

        self.vlayout = QVBoxLayout()
        self.gbox = QGroupBox()
        self.gbox.setMaximumSize(800, 800)
        self.TT = QLabel('Thông tin cá nhân',self)
        self.TT.setAlignment(Qt.AlignCenter)
        self.TT.setStyleSheet("font-size: 25px ")
        font = QFont()
        font.setBold(True)
        self.TT.setFont(font)
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
        self.lbstHoten.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstHoten, 3, 1)
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

        #datetimeedit lien ket
        self.dateedit = QDateTimeEdit(self.qdate)
        self.dateedit.setDisplayFormat("yyyy-MM-dd")
        self.dateedit.dateChanged.connect(self.main_change)
        self.lbNgay = QLabel("Ngày:", self)
        self.dateedit_day = QDateTimeEdit(self.qdate, self)
        self.dateedit_day.setDisplayFormat("dd")
        self.dateedit_day.dateChanged.connect(self.day_main)

        self.lbThang = QLabel("Tháng:", self)
        self.dateedit_month = QDateTimeEdit(self.qdate, self)
        self.dateedit_month.setDisplayFormat("MM")
        self.dateedit_month.dateChanged.connect(self.month_main)

        self.lbNam = QLabel("Năm:", self)
        self.dateedit_year = QDateTimeEdit(self.qdate, self)
        self.dateedit_year.setDisplayFormat("yyyy")
        self.dateedit_year.dateChanged.connect(self.year_main)

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
        self.lbstNgaySinh.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstNgaySinh, 6, 1)

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
        #self.TienNgay = (int)(self.tim().record(0).value(3))
        self.txtTienNgay.setText((str)(self.tim().record(0).value(3)))
        self.grid.addWidget(self.txtTienNgay, 8, 1)
        self.lbstTienNgay = QLabel('', self)
        self.lbstTienNgay.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstTienNgay, 9, 1)

        self.hb = QHBoxLayout(self)
        self.btnSua = QPushButton('Sửa', self)
        self.btnSua.clicked.connect(self.Sua)
        self.hb.addWidget(self.btnSua)
        self.btnDangXuat = QPushButton('Đăng xuất', self)
        self.btnDangXuat.clicked.connect(self.logout)
        self.hb.addWidget(self.btnDangXuat)







        #self.btnLogout.click.connect(self.logout)
        self.vlayout.addWidget(self.TT)
        self.vlayout.addWidget(self.gbox)
        self.vlayout.addLayout(self.hb)
        self.vlayout.setAlignment(Qt.AlignCenter)
        widLayout = QWidget()
        widLayout.setLayout(self.vlayout)
        self.setWidget(widLayout)






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
            if(self.Hoten_Check()==True and self.TienNgay_Check() == True and self.NgaySinh_Check()==True):
                gioitinh = '0'
                if (self.RdbNam.isChecked()):
                    gioitinh = '1'
                query = QSqlQuery(db)
                sql = "update nhanvien set Hoten = N'" + self.txtHoten.text() + "', NgaySinh ='" + self.dateedit.date().toString(
                    'yyyy-MM-dd') + "', TienNgay =" + self.txtTienNgay.text() + "," \
                                                                                " GioiTinh = " + gioitinh + " where MaNV = '" + TaiKhoan.getMaNV(
                    TaiKhoan) + "'"
                query.prepare(sql)
                query.exec()
                mb = QMessageBox.information(self, 'Thông báo', 'Cập nhật thành công!', QMessageBox.Ok, QMessageBox.Ok)

        else:
            mb = QMessageBox.Warning(self, 'Lỗi', 'Kết nối thất bại!', QMessageBox.Ok, QMessageBox.Ok)

    def logout(self):
        self.switch_window.emit()
        self.close()

    def month_main(self):
        self.dateedit.setDate(self.dateedit_month.date())
    def year_main(self):
        self.dateedit.setDate(self.dateedit_year.date())
    def day_main(self):
        self.dateedit.setDate(self.dateedit_day.date())
    def main_change(self):
        self.dateedit_day.setDate(self.dateedit.date())
        self.dateedit_month.setDate(self.dateedit.date())
        self.dateedit_year.setDate(self.dateedit.date())

    def Hoten_Check(self):
        if(self.txtHoten.text() == ""):
            self.lbstHoten.setText("Vui lòng nhập họ tên!")
            return False
        else:
            if (all(chr.isalpha() or chr.isspace() for chr in self.txtHoten.text())):
                self.lbstHoten.setText("")
                return True
            else:
                self.lbstHoten.setText("Họ và tên không bao gồm số và ký tự đặc biệt!")
                return False

    def TienNgay_Check(self):
        self.So = 0
        for char in self.txtTienNgay.text():
            if (char == "."):
                self.So = self.So + 1
        if (self.txtTienNgay.text() == ""):
            self.lbstTienNgay.setText("Vui lòng nhập tiền ngày!")
            return False
        else:
            if not (all(chr.isnumeric() or chr == '.' for chr in self.txtTienNgay.text())):
                self.lbstTienNgay.setText("Tiền ngày không bao gồm chữ, khoảng trắng hoặc ký tự đặc biệt!")
                return False
            else:
                if (self.So > 1):
                    self.lbstTienNgay.setText("Tiền ngày không hợp lệ!")
                    return False

                else:
                    if ((float)(self.txtTienNgay.text()) < 0):
                        self.lbstTienNgay.setText("Tiền ngày không hợp lệ!")
                        return False
                    else:
                        self.lbstTienNgay.setText("")
                        return True

    def NgaySinh_Check(self):
        self.NamSinh = QDate.currentDate().year() - self.dateedit.date().year()
        print(QDate.currentDate().year() - self.dateedit.date().year())
        if(self.NamSinh>=18 and self.NamSinh<=55):
            self.lbstNgaySinh.setText("")
            return True
        else:
            self.lbstNgaySinh.setText("Năm sinh không hợp lệ!")
            return False





