import sys

from PyQt5.QtCore import QSize, Qt, QStringListModel, QItemSelectionModel, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlDatabase
from PyQt5.QtWidgets import QMdiSubWindow, QWidget, QGridLayout, QApplication, QGroupBox, QVBoxLayout, QTableView, \
    QHBoxLayout, QPushButton, QBoxLayout, QSpacerItem, QSizePolicy, QMainWindow, QToolBar, QAction, QLabel, QLineEdit, \
    QWidgetAction, QMdiArea, QListView, QTreeView
from Search_Info import Search_Info
from Update_Info import Update_Info
from Insert import App
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

class NhanVien(QMdiSubWindow):
    switch_window = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.NhanVien()
        self.dia = QMdiSubWindow()

    def NhanVien(self):

        self.setGeometry(200, 50, 1180, 685)
        widlayout = QWidget()


        IconTim = QPixmap(150, 150)
        IconTim.load('E://search.png')
        IconThem = QPixmap(150, 150)
        IconThem.load('E://insert.png')
        IconSua = QPixmap(150, 150)
        IconSua.load('E://update.png')
        IconLammoi = QPixmap(150, 150)
        IconLammoi.load('E://refresh.png')



        tim = QAction(QIcon(IconTim), '&Tìm kiếm', self)
        them = QAction(QIcon(IconThem), '&Thêm', self)
        sua = QAction(QIcon(IconSua), '&Sửa', self)
        lammoi = QAction(QIcon(IconLammoi), '&Tải lại', self)
        self.mainwin = QMainWindow()
        self.mainwin.setMaximumHeight(40)
        tlbtim = QToolBar('Tim kiem', self.mainwin)
        tlbtim.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tlbthem = QToolBar('Them', self.mainwin)
        tlbthem.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tlbsua = QToolBar('Sua', self.mainwin)
        tlbsua.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        #tlblammoi = QToolBar('Tai lai', self.mainwin)
        #tlblammoi.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.mainwin.addToolBar(tlbthem)
        self.mainwin.addToolBar(tlbsua)
        #self.mainwin.addToolBar(tlblammoi)
        self.mainwin.addToolBar(tlbtim)
        self.txtTim = QLineEdit(self)
        self.txtTim.setMaximumWidth(100)
        self.txtTim.setCursorPosition(10)


        tlbtim.addAction(tim)
        tlbtim.addWidget(self.txtTim)
        tlbthem.addAction(them)
        tlbsua.addAction(sua)
        #tlblammoi.addAction(lammoi)


        gbTT = QGroupBox()
        gbTT.setTitle('Thông tin nhân viên')
        grid = QGridLayout()
        grid.setSpacing(10)
        lbMNV= QLabel('Mã nhân viên: ', self)
        grid.addWidget(lbMNV, 0, 0)
        self.MaNV = QLabel(self)
        grid.addWidget(self.MaNV, 0, 1)
        lbHoten = QLabel('Họ tên: ', self)
        grid.addWidget(lbHoten, 1, 0)
        self.Hoten = QLabel(self)
        grid.addWidget(self.Hoten, 1, 1)
        lbNgaySinh = QLabel('Ngày sinh: ', self)
        grid.addWidget(lbNgaySinh, 2, 0)
        self.Ngaysinh = QLabel(self)
        grid.addWidget(self.Ngaysinh, 2, 1)
        lbGioiTinh = QLabel('Giới tính: ', self)
        grid.addWidget(lbGioiTinh, 0, 2)
        self.GioiTinh = QLabel(self)
        grid.addWidget(self.GioiTinh, 0, 3)
        lbTienNgay = QLabel('Tiền ngày: ', self)
        grid.addWidget(lbTienNgay, 1, 2)
        self.TienNgay = QLabel(self)
        grid.addWidget(self.TienNgay, 1, 3)


        gbTT.setLayout(grid)


        self.view = QTableView()
        self.view.setMinimumHeight(50)
        self.view.setMaximumHeight(300)
        if createConnection():
            print('Ket noi thanh cong')
            self.SQL_STATEMENT = 'SELECT MaNV, HoTen, NgaySinh, TienNgay, GioiTinh FROM nhanvien'
            self.view.setModel(self.displayData(self.SQL_STATEMENT))
            self.selection_model = QItemSelectionModel()
            self.selection_model = self.view.selectionModel()
            self.selection_model.selectionChanged.connect(self.select_click)
            #self.view.show()

        else:
            print('Ket noi that bai')




        layout = QVBoxLayout()
        layout.addWidget(gbTT)
        #layout.addWidget(gbCN)
        layout.addWidget(self.mainwin)
        layout.addWidget(self.view)





        widlayout.setLayout(layout)


        self.setWidget(widlayout)
        tim.triggered.connect(self.Searching)
        them.triggered.connect(self.Insert)
        sua.triggered.connect(self.Update)

    def displayData(self, sqlStatement):
        qry = QSqlQuery(db)
        qry.prepare(sqlStatement)
        qry.exec()

        model = QSqlQueryModel()
        model.setQuery(qry)

        return model

    def Searching(self):
        global ex
        self.close()
        self.ex = Search_Info(self.txtTim.text())



    def Insert(self):
        self.close()
        self.dia = App()
        self.dia.show()

    def Update(self):
        self.close()
        self.update = Update_Info()
        self.update.show()
    def Update_clicked(self):
        self.switch_window.emit()

    def select_click(self):
        model = self.displayData(self.SQL_STATEMENT)
        row = self.selection_model.currentIndex().row()
        MaNV_data = model.data(model.index(row, 0))
        Hoten_data = model.data(model.index(row, 1))
        NgaySinh_data = model.data(model.index(row, 2))
        GioiTinh_data = model.data(model.index(row, 4))
        if (GioiTinh_data==1):
            self.GioiTinh.setText('Nam')
        else:
            self.GioiTinh.setText('Nữ')
        TienNgay_data = model.data(model.index(row, 3))
        self.MaNV.setText(MaNV_data)
        self.Hoten.setText(Hoten_data)
        self.Ngaysinh.setText(NgaySinh_data)

        self.TienNgay.setText(str(TienNgay_data) + " VND")






