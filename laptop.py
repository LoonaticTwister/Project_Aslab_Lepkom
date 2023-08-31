import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector

title='AMRTech'
class FormLaptop(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('folder_ui/laptop.ui',self)
        self.setWindowTitle(title)
        self.tampildata()
        self.btnSimpan.clicked.connect(self.simpandata)
        self.tblLaptop.clicked.connect(self.getdata)
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
        self.editLaptopID.setText('LID')
        self.editMerk.setText('')
        self.editTipe.setText('')
        self.editJumlah.setText('')
        self.tampildata()

    #fungsi tampil data
    def tampildata(self):
        try:
            #koneksi ke database
            con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
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

    #fungsi mendapatkan data yang sudah ada
    def getdata(self):
        get = self.tblLaptop.selectedItems()
        lid = get[0].text()
        merk = get[1].text()
        tipe = get[2].text()
        jumlah = get[3].text()
        self.editLaptopID.setText(lid)
        self.editMerk.setText(merk)
        self.editTipe.setText(tipe)
        self.editJumlah.setText(str(jumlah))
        

    #fungsi simpan data user
    def simpandata(self):
        try:
            lid= self.editLaptopID.text()
            merk= self.editMerk.text()
            tipe = self.editTipe.text()
            jumlah = self.editJumlah.text()

            if lid != '' and merk != '' and tipe != '' and jumlah != '':
                con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                query = 'insert into tbl_laptop values (%s, %s, %s, %s)'
                data = (lid, merk, tipe, int(jumlah))
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
            lid= self.editLaptopID.text()
            merk= self.editMerk.text()
            tipe = self.editTipe.text()
            jumlah = self.editJumlah.text()
            if lid != '' and merk != '' and tipe != '' and jumlah != '':
                con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                query = 'update tbl_laptop set merk=%s, tipe=%s, jumlah_tersedia=%s where laptop_id=%s'
                data=(merk, tipe, int(jumlah), lid)
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
            lid = self.editLaptopID.text()
            if lid !='':
                konfirm = self.konfirm('Apakah yakin ingin menghapus data ?')
                if konfirm == QMessageBox.Ok:
                    con = mysql.connector.connect(user='root', password='', host='localhost', database='pinjam_laptop')
                    query = 'delete from tbl_laptop where laptop_id=%s'
                    data=(lid,)
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
    form=FormLaptop()
    form.show()
    app.exec_()