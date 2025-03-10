import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit, QMessageBox, QSizePolicy
)

class NotDefteri(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Defteri")
        self.setGeometry(100, 100, 1280, 720)  # Başlangıç boyutu

        self.initUI()
        self.veritabani_olustur()
        self.notlari_goster()

    def initUI(self):
        main_layout = QVBoxLayout()
        table_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Notları gösteren tablo
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Başlık", "İçerik"])
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Dinamik boyut
        table_layout.addWidget(self.tableWidget)

        # Not başlığı ve içeriği giriş alanları
        self.baslik_input = QLineEdit(self)
        self.baslik_input.setPlaceholderText("Başlık")
        self.baslik_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_layout.addWidget(self.baslik_input)

        self.icerik_input = QTextEdit(self)
        self.icerik_input.setPlaceholderText("İçerik")
        self.icerik_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_layout.addWidget(self.icerik_input)

        # Butonlar
        self.ekle_buton = QPushButton("Not Ekle")
        self.ekle_buton.clicked.connect(self.not_ekle)

        self.sil_buton = QPushButton("Seçili Notu Sil")
        self.sil_buton.clicked.connect(self.not_sil)

        self.duzenle_buton = QPushButton("Seçili Notu Düzenle")
        self.duzenle_buton.clicked.connect(self.not_duzenle)

        button_layout.addWidget(self.ekle_buton)
        button_layout.addWidget(self.sil_buton)
        button_layout.addWidget(self.duzenle_buton)

        # Ana Layout'a ekleme
        main_layout.addLayout(table_layout)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def veritabani_olustur(self):
        conn = sqlite3.connect('notlar.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notlar (id INTEGER PRIMARY KEY, baslik TEXT, not_icerigi TEXT)''')
        conn.commit()
        conn.close()

    def notlari_goster(self):
        self.tableWidget.setRowCount(0)
        conn = sqlite3.connect('notlar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notlar")
        notlar = cursor.fetchall()
        conn.close()

        for satir, not_bilgisi in enumerate(notlar):
            self.tableWidget.insertRow(satir)
            for sutun, deger in enumerate(not_bilgisi):
                self.tableWidget.setItem(satir, sutun, QTableWidgetItem(str(deger)))

    def not_ekle(self):
        baslik = self.baslik_input.text()
        icerik = self.icerik_input.toPlainText()
        if not baslik or not icerik:
            QMessageBox.warning(self, "Hata", "Başlık ve içerik boş olamaz!")
            return

        conn = sqlite3.connect('notlar.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notlar (baslik, not_icerigi) VALUES (?, ?)", (baslik, icerik))
        conn.commit()
        conn.close()

        self.notlari_goster()
        self.baslik_input.clear()
        self.icerik_input.clear()

    def not_sil(self):
        secili_satir = self.tableWidget.currentRow()
        if secili_satir == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir not seçin!")
            return

        not_id = self.tableWidget.item(secili_satir, 0).text()

        conn = sqlite3.connect('notlar.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notlar WHERE id = ?", (not_id,))
        conn.commit()
        conn.close()

        self.notlari_goster()

    def not_duzenle(self):
        secili_satir = self.tableWidget.currentRow()
        if secili_satir == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir not seçin!")
            return

        not_id = self.tableWidget.item(secili_satir, 0).text()
        yeni_baslik = self.baslik_input.text()
        yeni_icerik = self.icerik_input.toPlainText()

        if not yeni_baslik or not yeni_icerik:
            QMessageBox.warning(self, "Hata", "Başlık ve içerik boş olamaz!")
            return

        conn = sqlite3.connect('notlar.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE notlar SET baslik = ?, not_icerigi = ? WHERE id = ?", (yeni_baslik, yeni_icerik, not_id))
        conn.commit()
        conn.close()

        self.notlari_goster()
        self.baslik_input.clear()
        self.icerik_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = NotDefteri()
    pencere.show()
    sys.exit(app.exec_())
