from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox, \
    QMenu, QAction, qApp, QDialog, QToolBar, QMdiArea, QMdiSubWindow
from TrangChu import TrangChu
from NhanVien import NhanVien

class Home(QMainWindow):
    switch_window = pyqtSignal()
    switch_window2 = pyqtSignal()
    def __init__(self, parent=None):
        super(Home, self).__init__(parent)
        self.GUI()
        self.dia = None



    def GUI(self):
        self.setWindowTitle('Home')

        nhanvien = QPixmap(150, 150)
        nhanvien.load('nhanvien04.png')
        home = QPixmap(150, 150)
        home.load('home04.png')
        phongban = QPixmap('phongban.png')


        self.NhanVien = QAction(QIcon(nhanvien), '&Nhân viên', self)
        self.Home = QAction(QIcon(home), '&Trang chủ', self)
        self.PhongBan = QAction(QIcon(phongban), '&Phòng ban', self)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)


        menu = self.menuBar()
        self.File = menu.addMenu('&File')
        self.File.addAction(exitAct)
        #self.Edit = menu.addMenu('&Edit')

        self.tlbHome = QToolBar(self)
        self.setIconSize(QSize(180, 180))
        self.tlbHome.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, self.tlbHome)
        self.tlbHome.addAction(self.Home)

        self.tlbNhanVien = QToolBar('&Nhan Vien', self)
        self.setIconSize(QSize(180, 180))
        self.tlbNhanVien.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, self.tlbNhanVien)
        self.tlbNhanVien.addAction(self.NhanVien)

        self.tlbPhongBan = QToolBar(self)
        self.setIconSize(QSize(180, 180))
        self.tlbPhongBan.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, self.tlbPhongBan)
        self.tlbPhongBan.addAction(self.PhongBan)

        self.Home.triggered.connect(self.subwindow_TrangChu)
        self.NhanVien.triggered.connect(self.subwindow_NhanVien)


        ###QMdiArea
        self.mdi = QMdiArea(self)
        self.setCentralWidget(self.mdi)
        self.showMaximized()







    def subwindow_TrangChu(self):
        self.switch_window.emit()



    def subwindow_NhanVien(self):
        self.switch_window2.emit()
