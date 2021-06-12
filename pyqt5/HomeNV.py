from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, \
    QRadioButton, QComboBox, QTableView, QTableWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QBoxLayout, QGroupBox, \
    QMenu, QAction, qApp, QDialog, QToolBar, QMdiArea, QMdiSubWindow
from TrangChu import TrangChu
from NhanVien import NhanVien

class HomeNV(QMainWindow):
    switch_window = pyqtSignal()
    def __init__(self, parent=None):
        super(HomeNV, self).__init__(parent)
        self.GUI()
        self.dia = None



    def GUI(self):
        self.setWindowTitle('Home')

        home = QPixmap(150, 150)
        home.load('home04.png')
        self.Home = QAction(QIcon(home), '&Trang chủ', self)
        menu = self.menuBar()
        self.File = menu.addMenu('&File')


        self.tlbHome = QToolBar(self)
        self.setIconSize(QSize(180, 180))
        self.tlbHome.setToolButtonStyle(Qt.ToolButtonTextBesideIcon | Qt.AlignLeading)
        self.addToolBar(Qt.LeftToolBarArea, self.tlbHome)
        self.tlbHome.addAction(self.Home)





        self.Home.triggered.connect(self.subwindow_TrangChu)



        ###QMdiArea
        self.mdi = QMdiArea(self)
        self.setCentralWidget(self.mdi)
        self.showMaximized()







    def subwindow_TrangChu(self):
        self.switch_window.emit()




