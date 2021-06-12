import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self.calendar = QtWidgets.QCalendarWidget(self)
        #self.calendar.setGeometry(0, 0, 300, 300)
        #self.calendar.setGridVisible(True)
        #self.calendar.setMinimumDate(QDate(2006, 6, 19))
        qdate = QDate()
        self.dateedit = QtWidgets.QDateTimeEdit(QDate.currentDate(), self)
        #self.dateedit.setMinimumDate(QDate.currentDate().addDays(-365))
        #self.dateedit.setMaximumDate(QDate.currentDate().addDays(365))
       # self.menuBar().setCornerWidget(self.dateedit, QtCore.Qt.TopLeftCorner)
       # self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateedit.setDisplayFormat("yyyy-MM-dd")
        print(self.dateedit.text())
        self.dateedit.dateChanged.connect(self.main_change)

        self.dateedit_day = QtWidgets.QDateTimeEdit(QDate.currentDate(), self)
        self.dateedit_day.setGeometry(10, 40, 130, 30)
        self.dateedit_day.setDisplayFormat("dd")
        self.dateedit_day.dateChanged.connect(self.day_main)

        self.dateedit_year = QtWidgets.QDateTimeEdit(QDate.currentDate(), self)
        self.dateedit_year.setGeometry(300, 40, 100, 30)
        self.dateedit_year.setDisplayFormat("yyyy")
        self.dateedit_year.dateChanged.connect(self.year_main)

        self.dateedit_month = QtWidgets.QDateTimeEdit(QDate.currentDate(), self)
        self.dateedit_month.setGeometry(150, 40, 100, 30)
        self.dateedit_month.setDisplayFormat("MM")
        self.dateedit_month.dateChanged.connect(self.month_main)

    def month_day(self):
        self.dateedit_day.setDate(self.dateedit_month.date())

    def year_month(self):
        self.dateedit_month.setDate(self.dateedit_year.date())

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())