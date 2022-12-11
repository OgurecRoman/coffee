import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.loadTable)
        self.pushButton_2.clicked.connect(self.add)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.con = sqlite3.connect('coffee.db')

    def loadTable(self):
        cur = self.con.cursor()
        result = cur.execute("""SELECT * FROM Coffee""").fetchall()

        for i, row in enumerate(result):
            self.tableWidget.setRowCount(i + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def add(self):
        self.second_form = Add_Form()
        self.second_form.show()
        self.close()


class Add_Form(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.cancel)
        self.con = sqlite3.connect('coffee.db')
        self.pushButton_3.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_4.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM Coffee WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE Coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def add(self):
        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        roasting = self.lineEdit_3.text()
        mol = self.lineEdit_4.text()
        delitious = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        v = self.lineEdit_7.text()
        cur = self.con.cursor()
        cur.execute("""INSERT INTO Coffee(ID, Name_sort, roasting, ground, taste, price, volume) 
        VALUES(?, ?, ?, ?, ?, ?, ?)""", (id, name, roasting, mol, delitious, price, v)).fetchall()
        self.cancel()

    def cancel(self):
        self.second_form = MyWidget()
        self.second_form.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
