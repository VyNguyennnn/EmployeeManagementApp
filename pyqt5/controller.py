import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from Login import Login
from Home import Home
from TrangChu import TrangChu
from NhanVien import NhanVien
from Update_Info import Update_Info
from Update import update
from HomeNV import HomeNV
class Controller:

    def __init__(self):
        self.home = QMainWindow()
        self.dia = None

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_home)
        self.login.switch_window2.connect(self.show_home_NV)

        if self.home.isVisible():
            self.home.close()
        #self.login.show()

    def show_home(self):
        self.home = Home()
        self.home.switch_window.connect(self.show_window_two)
        self.home.switch_window2.connect(self.show_window_two_NV)
        self.login.close()
        #self.home.show()

    def show_home_NV(self):
        self.home = HomeNV()
        self.home.switch_window.connect(self.show_window_two)
        self.login.close()

    def show_window_two(self):
        if self.dia is None:
            self.dia = TrangChu()
            self.home.mdi.addSubWindow(self.dia)
            self.dia.switch_window.connect(self.show_login)
            self.dia.show()
        else:
            if self.dia.isVisible():
                self.dia.close()
            self.dia = None

    def show_window_two_NV(self):
        if self.dia is None:
            self.dia = NhanVien()
            self.home.mdi.addSubWindow(self.dia)
            self.dia.switch_window.connect(self.show_update_info)
            # self.dia.switch_window.connect(self.show_login)
            self.dia.show()
        else:
            if self.dia.isVisible():
                self.dia.close()
            self.dia = None

    def show_update_info(self):
        self.update_info = Update_Info()
        self.update_info.switch_window.connect(self.show_update)


    def show_update(self):
        self.update = update(self.update_info.txtTim.text())







def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()