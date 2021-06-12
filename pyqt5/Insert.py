import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox, \
    QMdiSubWindow, QStatusBar, QDateTimeEdit

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

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()



    def mousePressEvent(self, event):
        super(ClickableLineEdit, self).mousePressEvent(event)
        self.clicked.emit()


class App(QMdiSubWindow):
    global db
    def __init__(self):
        super().__init__() #???
        self.GUI()

    def GUI(self):
        self.setWindowTitle('Nhập thông tin nhân viên')
        self.setGeometry(500, 200, 400, 400)

        self.vlayout = QVBoxLayout()


        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Ma nhan vien
        self.lbMNV = QLabel('Mã nhân viên', self)
        self.grid.addWidget(self.lbMNV, 1, 0)
        self.txtMNV = ClickableLineEdit(self)
        self.txtMNV.setPlaceholderText("0001")
        self.txtMNV.setInputMask("9999")
        self.txtMNV.clicked.connect(self.txtMNV.clear)
        #self.txtMNV.textChanged.connect(self.MaNV_check)
        self.grid.addWidget(self.txtMNV, 1, 1)
        self.lbstMNV = QLabel(self)
        self.lbstMNV.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstMNV, 2, 1)


        # Ho va ten nhan vien
        self.lbHoten = QLabel('Họ và tên', self)
        self.grid.addWidget(self.lbHoten, 3, 0)
        self.txtHoten = ClickableLineEdit(self)
        self.txtHoten.setPlaceholderText("Nguyễn Văn An")
        self.txtHoten.clicked.connect(self.txtHoten.clear)
        self.grid.addWidget(self.txtHoten, 3, 1)
        self.lbstHoten = QLabel(self)
        self.lbstHoten.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstHoten, 4, 1)
        self.vlayout.addLayout(self.grid)

        # Radio gioi tinh
        self.lbGioiTinh = QLabel("Giới tính", self)
        self.grid.addWidget(self.lbGioiTinh, 5, 0)
        self.gb = QGroupBox()
        self.RdbNam = QRadioButton('Nam', self)
        self.RdbNu = QRadioButton('Nu', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.RdbNam)
        self.hbox.addWidget(self.RdbNu)
        #self.gb.setLayout(self.hbox)
        self.grid.addLayout(self.hbox, 5, 1)
        self.lbstGioiTinh = QLabel(self)
        self.lbstGioiTinh.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstGioiTinh, 6, 1)



        # Ngay sinh
        self.lbNgaySinh = QLabel('Ngày sinh', self)
        self.grid.addWidget(self.lbNgaySinh, 7, 0)
        #self.txtNgaySinh = ClickableLineEdit('yyyy-mm-dd', self)
        #self.txtNgaySinh.clicked.connect(self.txtNgaySinh.clear)
        #self.grid.addWidget(self.txtNgaySinh, 5, 1)
        self.gb_NS = QGroupBox()
        self.qdate = QDate.currentDate()

        # datetimeedit lien ket
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
        self.grid.addWidget(self.gb_NS, 7, 1)
        self.lbstNgaySinh = QLabel("", self)
        self.lbstNgaySinh.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstNgaySinh, 8, 1)


        # Chuc vu
        self.lbChucVu = QLabel('Chức vụ', self)
        self.grid.addWidget(self.lbChucVu, 9, 0)
        #self.cmb = QComboBox(self)
        #self.cmb.addItems(['Không có chức vụ', 'Trưởng phòng'])
        #self.grid.addWidget(self.cmb, 6, 1)
        self.txtChucVu = QLabel('Nhân viên', self)
        self.grid.addWidget(self.txtChucVu, 9, 1)

        # Tien ngay
        self.lbTienNgay = QLabel('Tiền ngày', self)
        self.grid.addWidget(self.lbTienNgay, 10, 0)
        self.txtTienNgay = ClickableLineEdit(self)
        self.txtTienNgay.setPlaceholderText("47000.0")
        self.txtTienNgay.clicked.connect(self.txtTienNgay.clear)
        self.grid.addWidget(self.txtTienNgay, 10, 1)
        self.lbstTienNgay = QLabel(self)
        self.lbstTienNgay.setStyleSheet("color: red")
        self.grid.addWidget(self.lbstTienNgay, 11, 1)

        self.hbox1 = QHBoxLayout()
        # Tao nut Xem lai
        self.btnXemLai = QPushButton('Xem lại', self)
        self.hbox1.addWidget(self.btnXemLai)
        # Lien ket den on_click()
        self.btnXemLai.clicked.connect(self.on_click)
        # Tao nut Truy xuat
        self.btnTruyXuat = QPushButton('Truy xuất', self)
        self.hbox1.addWidget(self.btnTruyXuat)
        # Lien ket den btnTruyXuat_click()
        self.btnTruyXuat.clicked.connect(self.btnTruyXuat_click)
        # Tao nut Them
        self.btnThem = QPushButton('Thêm', self)
        self.hbox1.addWidget(self.btnThem)
        #Lien ket den btnThem_click()
        self.btnThem.clicked.connect(self.btnThem_click)


        self.view = QTableView()
        self.vlayout.addWidget(self.view)


        widLayout = QWidget()
        widLayout.setLayout(self.vlayout)
        self.vlayout.addLayout(self.hbox1)





        self.setWidget(widLayout)


    def on_click(self):
        print('----------------------------------------------')
        print('Ma nhan vien: '+ self.txtMNV.text())
        print('Ho va ten: ' + self.txtHoten.text())
        if self.RdbNam.isChecked():
            print('Gioi tinh: Nam')
        else:
            print('Gioi tinh: Nữ')

        print('Ngay sinh: ' + self.txtNgaySinh.text())
        print('Chuc vu: ' + self.cmb.currentText())
        print('Tien ngay: ' + self.txtTienNgay.text())
        print('----------------------------------------------')

    def btnTruyXuat_click(self):
        if createConnection():
            print('Ket noi thanh cong')
            SQL_STATEMENT = 'SELECT * FROM nhanvien'
            self.view.setModel(displayData(SQL_STATEMENT))
            self.view.show()
            #print(str(self.view.rowAt(10)))
        else:
            print('Ket noi that bai')

    def RadioBox_check(self):
        if self.RdbNam.isChecked():
            return "1"
        else:
            return "0"

    def ComboBox_check(self):
        if self.cmb.currentText() == 'Trưởng phòng':
            return 1
        else:
            return 2


    def btnThem_click(self):
        if createConnection():
            print(self.dateedit.date().toString('yyyy-MM-dd'))
            if(self.MaNV_check()==True and self.Hoten_Check()==True and self.GioiTinh_Check() ==True and self.NgaySinh_Check() == True and self.TienNgay_Check()==True):
                SQL_insert = "Insert into NhanVien values ('" + self.txtMNV.text() + "', N'" + self.txtHoten.text() + "','" + self.dateedit.date().toString('yyyy-MM-dd') + "',"+\
                             self.RadioBox_check() +", 2, "+ self.txtTienNgay.text()+", 'NULL')"


                exeDB(SQL_insert)
                mb = QMessageBox.information(self, 'Thông báo', 'Thêm thành công!', QMessageBox.Ok, QMessageBox.Ok)

        else:
            mb = QMessageBox.Warning(self, 'Lỗi', 'Kết nối thất bại!', QMessageBox.Ok, QMessageBox.Ok)




    def MaNV_exist_check(self):
        SQL_insert = "IF EXISTS (SELECT MaNV FROM nhanvien " \
                     "WHERE MaNV = '" + self.txtMNV.text() + "" \
                    "') BEGIN SELECT 1 END ELSE BEGIN SELECT 0 END"

        qry = QSqlQuery(db)
        qry.prepare(SQL_insert)
        qry.exec()

        model = QSqlQueryModel()
        model.setQuery(qry)
        if (model.record(0).value(0) == 1):
            return False
        else:
            return True

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

    def MaNV_check(self):
        if (self.txtMNV.text() == ""):
            self.lbstMNV.setText("Vui lòng nhập mã nhân viên!")
            return False
        else:
            if (self.MaNV_exist_check()==False):
                self.lbstMNV.setText("Mã nhân viên này đã tồn tại!")
                return False
            else:
                if(self.txtMNV.text()=='0000'):
                    self.lbstMNV.setText("Mã nhân viên không hợp lệ!")
                    return False

                else:
                    self.lbstMNV.setText("")
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

    def GioiTinh_Check(self):
        if (self.RdbNam.isChecked() or self.RdbNu.isChecked()):
            self.lbstGioiTinh.setText("")
            return True
        else:
            self.lbstGioiTinh.setText("Vui lòng chọn giới tính!")
            return False

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



def displayData(sqlStatement):
    qry = QSqlQuery(db)
    qry.prepare(sqlStatement)
    qry.exec()

    model = QSqlQueryModel()
    model.setQuery(qry)

    return model

def exeDB(insert):
    qry = QSqlQuery(db)
    qry.prepare(insert)
    qry.exec()

