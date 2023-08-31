# Mengimpor modul yang diperlukan
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from laptop import *
from user import *
from peminjaman import *

class FormUtama(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('folder_ui/formutama.ui', self)
        self.setWindowTitle('AMRTech')
        self.btnLogout.clicked.connect(self.logout)
        self.btnUSER.clicked.connect(self.formuser)
        self.btnLAPTOP.clicked.connect(self.formlaptop)
        self.btnPINJAM.clicked.connect(self.formpinjam)

    #fungsi konfirm
    def konfirm(self, pesan):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(pesan)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec()
    
    #Fungsi membuka form user
    def formuser(self):
        self.formuser = FormUser()
        self.formuser.show()

    #Fungsi membuka form laptop
    def formlaptop(self):
        self.formlaptop = FormLaptop()
        self.formlaptop.show()

    #Fungsi membuka form pinjam
    def formpinjam(self):
        self.formpinjam = FormPeminjaman()
        self.formpinjam.show()

    #Fungsi Logout
    def logout(self):
        konfirm = self.konfirm('Apakah anda ingin Logout?')
        if konfirm == QMessageBox.Ok:
            self.close()

# Eksekusi jika ini adalah program utama
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form=FormUtama()
    form.show()
    app.exec_()
        