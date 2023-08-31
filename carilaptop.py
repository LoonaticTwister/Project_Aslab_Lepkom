import sys
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector

class CariLID(QDialog):
    __lid = ''

    def __init__(self):
        QDialog.__init__(self)
        loadUi('folder_ui/carilaptop.ui', self)
        self.setWindowTitle('AMRTech')
        self.tampildata()
        self.btnCari.clicked.connect(self.caridata)
        self.tblLaptop.doubleClicked.connect(self.pilihdata)

    def pesan(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('AMRTech')
        msg.setText(pesan)
        msg.exec()

    #fungsi tampil data
    def tampildata(self):
        try:
            #koneksi ke database
            con = mysql.connector.connect(user='root', password='', host='localhost', database='amrtech')
            query = 'select * from tbl_laptop'
            cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            #menutup koneksi
            con.close()

            #menampilkan data
            baris=0
            self.tblLaptop.setRowCount(len(data))
            for user in data:
                self.tblLaptop.setItem(baris, 0, QTableWidgetItem(user[0]))
                self.tblLaptop.setItem(baris, 1, QTableWidgetItem(user[1]))
                self.tblLaptop.setItem(baris, 2, QTableWidgetItem(user[2]))
                self.tblLaptop.setItem(baris, 3, QTableWidgetItem(str(user[3])))
                baris += 1
        except:
            self.pesan('Terjadi kesalahan saat menampilkan data')

    def caridata(self):
        try:
            cari = self.editCari.text()
            con = mysql.connector.connect(user='root', password='', host='localhost', database='amrtech')
            query = "select * from tbl_laptop where laptop_id like '%"+cari+"%' or merk like '%"+cari+"%' or tipe like '%"+cari+"%'"
            cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            #menutup koneksi
            con.close()
            #menampilkan data
            baris=0
            self.tblLaptop.setRowCount(len(data))
            for user in data:
                self.tblLaptop.setItem(baris, 0, QTableWidgetItem(user[0]))
                self.tblLaptop.setItem(baris, 1, QTableWidgetItem(user[1]))
                self.tblLaptop.setItem(baris, 2, QTableWidgetItem(user[2]))
                self.tblLaptop.setItem(baris, 3, QTableWidgetItem(str(user[3])))
                baris += 1
        except:
            self.pesan('Terjadi kesalahan saat menampilkan data')            

    def pilihdata(self):
        get = self.tblLaptop.selectedItems()
        self.__lid=get[0].text()
        self.close()
    
    def getData(self):
        return self.__lid

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form=CariLID()
    form.exec()
    app.exec_()