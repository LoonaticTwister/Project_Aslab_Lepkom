# Mengimpor modul yang diperlukan
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.uic import loadUi
import mysql.connector
from formutama import *  

class FormLogin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('folder_ui/login.ui', self)
        self.setWindowTitle('AMRTech')
        self.btnLogin.clicked.connect(self.adminlogin) 

    # Fungsi untuk menampilkan pesan dialog
    def pesan(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('AMRTech')
        msg.setText(pesan)
        msg.exec()

    # Fungsi untuk menghapus input pada field 
    def clear(self):
        self.EditUsername.setText('')
        self.EditPassword.setText('')

    # Fungsi untuk melakukan proses login
    def adminlogin(self):
        try:
            username = self.EditUsername.text()
            password = self.EditPassword.text()

            # Memeriksa apakah input username dan password tidak kosong
            if username != '' and password != '':
                # koneksi ke database
                con = mysql.connector.connect(user='root', password='', host='localhost', database='amrtech')

                # Melakukan query untuk memeriksa keberadaan admin di tabel tbl_admin
                query = 'select * from tbl_admin where username=%s and password=%s'
                data = (username, password)
                cursor = con.cursor()
                cursor.execute(query, data)
                admin_user = cursor.fetchall()

                # Jika ditemukan satu admin yang cocok, akan membuka FormUtama
                if len(admin_user) == 1:
                    self.form_utama = FormUtama()
                    self.form_utama.show()
                    self.close()
                else:
                    self.pesan('Login Gagal, Periksa Username dan Password kembali!')
                    self.clear()
            else:
                self.pesan('Username dan Password tidak boleh kosong!')
                self.clear()

        except:
            self.pesan('Terjadi kesalahan pada saat login!')
            self.clear()

# Menampilkan window
if __name__ == '__main__':
    app = QApplication(sys.argv)  
    form = FormLogin()  
    form.show()  
    app.exec_()  
