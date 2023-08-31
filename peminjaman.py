# Mengimpor modul yang diperlukan
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector
from datetime import datetime
from cariuser import *
from carilaptop import *

title = 'AMRTech'
class FormPeminjaman(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('peminjaman.ui', self)  # Memuat tata letak dari peminjaman.ui
        self.setWindowTitle(title)
        self.btnUID.clicked.connect(self.cariuser)
        self.btnLID.clicked.connect(self.carilaptop)
        self.btnBaru.clicked.connect(self.clear)
        self.btnSimpan.clicked.connect(self.simpandata)
        self.tblPinjam.clicked.connect(self.getdata)
        self.btnHapus.clicked.connect(self.hapusdata)
        self.tampildata()
        self.clear()

    # Fungsi untuk mencari user
    def cariuser(self):
        form = CariUID()
        form.exec()
        self.editUID.setText(form.getData())

    # Fungsi untuk mencari laptop
    def carilaptop(self):
        form = CariLID()
        form.exec()
        self.editLID.setText(form.getData())

    # Fungsi untuk menampilkan pesan dialog
    def pesan(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(pesan)
        msg.exec()

    # Fungsi untuk menghapus input pada field peminjaman
    def clear(self):
        self.editPID.setText('PID')
        self.editLID.setText('')
        self.editUID.setText('')
        self.datePinjam.setDate(datetime.today())
        self.dateBalik.setDate(datetime.today())
        self.tampildata()

    # Fungsi untuk konfirmasi aksi
    def konfirm(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(pesan)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec()
    
    # Fungsi untuk mengambil data dari tabel
    def getdata(self):
        get = self.tblPinjam.selectedItems()
        pid = get[0].text()
        uid = get[1].text()
        lid = get[2].text()
        self.editPID.setText(pid) 
        self.editUID.setText(uid) 
        self.editLID.setText(lid)
    
    # Fungsi untuk menampilkan data pada tabel
    def tampildata(self):
        try:
            #koneksi ke database
            con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
            query = 'SELECT * FROM tbl_peminjaman'
            cursor = con.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            #menutup koneksi
            con.close()

            #menampilkan data
            baris = 0
            self.tblPinjam.setRowCount(len(data))
            for user in data:
                self.tblPinjam.setItem(baris, 0, QTableWidgetItem(user[0]))
                self.tblPinjam.setItem(baris, 1, QTableWidgetItem(user[1]))
                self.tblPinjam.setItem(baris, 2, QTableWidgetItem(user[2]))
                self.tblPinjam.setItem(baris, 3, QTableWidgetItem(user[3].strftime('%d/%m/%Y')))
                self.tblPinjam.setItem(baris, 4, QTableWidgetItem(user[4].strftime('%d/%m/%Y')))
                baris += 1
        except:
            self.pesan('Terjadi kesalahan saat menampilkan data')

    # Fungsi untuk menyimpan data
    def simpandata(self):
        try:
            uid = self.editUID.text()
            lid = self.editLID.text()
            pid = self.editPID.text()
            tglpinjam = self.datePinjam.date()
            tglbalik = self.dateBalik.date()
            if uid != '' and lid != '' and pid != '':
            # koneksi ke database
                con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                query = 'insert into tbl_peminjaman values(%s, %s, %s, %s, %s)'
                data = (pid,lid,uid,tglpinjam.toString('yyyy-MM-dd'),tglbalik.toString('yyyy-MM-dd'))
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

    # Fungsi untuk menghapus data
    def hapusdata(self):
        try:
            pid = self.editPID.text()
            if pid !='':
                konfirm = self.konfirm('Apakah yakin ingin menghapus data ?')
                if konfirm == QMessageBox.Ok:
                    con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                    query = 'delete from tbl_peminjaman where peminjaman_id=%s'
                    data = (pid,)
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

# Eksekusi jika ini adalah program utama
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FormPeminjaman()
    form.show()
    app.exec_()  
