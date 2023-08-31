import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector

title='AMRTech'
class FormUser(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('user.ui',self)
        self.setWindowTitle(title)
        self.tampildata()
        self.btnSimpan.clicked.connect(self.simpandata)
        self.tblUser.clicked.connect(self.getdata)
        self.btnBaru.clicked.connect(self.clear)
        self.btnUbah.clicked.connect(self.updatedata)
        self.btnHapus.clicked.connect(self.hapusdata)

   #fungsi pesan
    def pesan(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(pesan)
        msg.exec()

    #fungsi konfirm
    def konfirm(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(pesan)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec()

    #fungsi clear
    def clear(self):
        self.EditUserID.setText('UID')
        self.EditNamaUser.setText('')
        self.EditEmailUser.setText('')
        self.EditAlamatUser.setText('')
        self.EditTlpnUser.setText('')
        self.tampildata()

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

    #fungsi mendapatkan data yang sudah ada
    def getdata(self):
        get = self.tblUser.selectedItems()
        uid = get[0].text()
        nama = get[1].text()
        email = get[2].text()
        alamat = get[3].text()
        telepon = get[4].text()

        self.EditUserID.setText(uid)
        self.EditNamaUser.setText(nama)
        self.EditEmailUser.setText(email)
        self.EditAlamatUser.setText(alamat)
        self.EditTlpnUser.setText(telepon)

    #fungsi simpan data user
    def simpandata(self):
        try:
            uid=self.EditUserID.text()
            nama= self.EditNamaUser.text()
            email = self.EditEmailUser.text()
            almt = self.EditAlamatUser.text()
            tlp = self.EditTlpnUser.text()

            if uid != '' and nama != '' and email != '' and almt != '' and tlp != '':
                con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                query = 'insert into tbl_user values (%s, %s, %s, %s, %s)'
                data = (uid, nama, email, almt, tlp)
                cursor = con.cursor()
                cursor.execute(query, data)
                con.commit()
                con.close()
                self.pesan('Data Tersimpan')
                self.tampildata()
                self.clear()
            else:
                self.pesan('Data Tidak Lengkap!')
                self.clear()
        except:
            self.pesan('Terjadi Kesalahan saat menyimpan data')
            self.clear()

    #fungsi update data
    def updatedata(self):
        try:
            uid=self.EditUserID.text()
            nama= self.EditNamaUser.text()
            email = self.EditEmailUser.text()
            almt = self.EditAlamatUser.text()
            tlp = self.EditTlpnUser.text()
            if uid != '' and nama != '' and email != '' and almt != '' and tlp != '':
                con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                query = 'update tbl_user set nama=%s, email=%s, alamat=%s, telpon=%s where user_id=%s'
                data=(nama,email,almt,tlp,uid)
                cursor = con.cursor()
                cursor.execute(query, data)
                con.commit()
                con.close()

                self.pesan('Data telah diubah')

                self.tampildata()
                self.clear()

            else:
                self.pesan('Data tidak lengkap!')

        except:
            self.pesan('Terjadi kesalahan saat mengubah data')
            

    #fungsi delete
    def hapusdata(self):
        try:
            uid = self.EditUserID.text()
            if uid !='':
                konfirm = self.konfirm('Apakah yakin ingin menghapus data ?')
                if konfirm == QMessageBox.Ok:
                    con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                    query = 'delete from tbl_user where user_id=%s'
                    data=(uid,)
                    cursor = con.cursor()
                    cursor.execute(query, data)
                    con.commit()
                    con.close()
                    self.pesan("Data berhasil dihapus")
                    self.tampildata()
                    self.clear()
            else:
                self.pesan('Pilih data yang ingin dihapus')
        except:
            self.pesan('Terjadi kesalahan saat menghapus data')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form=FormUser()
    form.show()
    app.exec_()