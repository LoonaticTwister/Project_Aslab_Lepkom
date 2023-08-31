import sys
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector

class CariUID(QDialog):
    __uid = ''

    def __init__(self):
        QDialog.__init__(self)
        loadUi('cariuser.ui', self)
        self.setWindowTitle('AMRTech')
        self.tampildata()
        self.btnCari.clicked.connect(self.caridata)
        self.tblUser.doubleClicked.connect(self.pilihdata)

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
            con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
            query = 'select * from tbl_user'
            cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            #menutup koneksi
            con.close()
            #menampilkan data
            baris=0
            self.tblUser.setRowCount(len(data))
            for user in data:
                self.tblUser.setItem(baris, 0, QTableWidgetItem(user[0]))
                self.tblUser.setItem(baris, 1, QTableWidgetItem(user[1]))
                self.tblUser.setItem(baris, 2, QTableWidgetItem(user[2]))
                self.tblUser.setItem(baris, 3, QTableWidgetItem(user[3]))
                self.tblUser.setItem(baris, 4, QTableWidgetItem(user[4]))
                baris += 1
        except:
            self.pesan('Terjadi kesalahan saat menampilkan data')

    def caridata(self):
        try:
            cari = self.editCari.text()
            con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
            query = "select * from tbl_user where user_id like '%"+cari+"%' or nama like '%"+cari+"%' or email like '%"+cari+"%' or alamat like '%"+cari+"%' or email like '%"+cari+"%'"
            cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            #menutup koneksi
            con.close()
            #menampilkan data
            baris=0
            self.tblUser.setRowCount(len(data))
            for user in data:
                self.tblUser.setItem(baris, 0, QTableWidgetItem(user[0]))
                self.tblUser.setItem(baris, 1, QTableWidgetItem(user[1]))
                self.tblUser.setItem(baris, 2, QTableWidgetItem(user[2]))
                self.tblUser.setItem(baris, 3, QTableWidgetItem(user[3]))
                self.tblUser.setItem(baris, 4, QTableWidgetItem(user[4]))
                baris += 1
        except:
            self.pesan('Terjadi Kesalahan saat mencari data')

    def pilihdata(self):
        get = self.tblUser.selectedItems()
        self.__uid=get[0].text()
        self.close()
    
    def getData(self):
        return self.__uid


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form=CariUID()
    form.exec()
    app.exec_()