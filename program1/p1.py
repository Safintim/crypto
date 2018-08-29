import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QFileDialog, QMessageBox
from random import shuffle
from copy import copy


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fname = None
        self.dict_crypto=None
        self.initUI()

        self.ALPHABET = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н','о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я','А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф','Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        self.FILE_KEY = 'key.txt'

    def initUI(self):

        btn_select=QPushButton('Select file',self)
        btn_select.resize(btn_select.sizeHint())
        btn_select.setGeometry(30, 20, 75, 30)
        btn_select.clicked.connect(self.select_file)

        btn_generate = QPushButton('Create key', self)
        btn_generate.resize(btn_generate.sizeHint())
        btn_generate.setGeometry(30, 80, 75, 30)
        btn_generate.clicked.connect(self.create_key)

        btn_code = QPushButton('Encrypted', self)
        btn_code.resize(btn_code.sizeHint())
        btn_code.setGeometry(30, 140, 75, 30)
        btn_code.clicked.connect(self.encrypted_file)

        btn_decode = QPushButton('Decrypted', self)
        btn_decode.resize(btn_decode.sizeHint())
        btn_decode.setGeometry(30, 200, 75, 30)
        btn_decode.clicked.connect(self.decrypted_file)

        self.setGeometry(400, 200, 140, 250)
        self.setWindowTitle('Шифратор')
        self.show()

    def select_file(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/timur/source','*.txt')[0]

    def create_key(self):
        alphabet_key = self.ALPHABET.copy()
        shuffle(alphabet_key)
        f = open(self.FILE_KEY, 'w')
        f.write(''.join(alphabet_key))
        self.dict_crypto = dict(zip(self.ALPHABET, alphabet_key))

    def encrypted_file(self):
        if self.fname is not None and self.fname != '':
            if self.dict_crypto is not None:
                input_file = open(self.fname, 'r')
                output_file = open(self.fname + '_crypto', 'w')
                for char in input_file.read():
                    if char in self.dict_crypto.keys():
                        output_file.write(self.dict_crypto[char])
            else:
                self.message2()
        else:
            self.message1()

    def decrypted_file(self):
        if self.fname is not None and self.fname != '':
            try:
                key_file=open(self.FILE_KEY, 'r')
            except IOError as e:
                self.message3()
            else:
                f = open(self.FILE_KEY, 'r')
                alphabet_key = []
                for char in f.read():
                    alphabet_key.append(char)
                dict_crypto = dict(zip(alphabet_key, self.ALPHABET))
                input_file = open(self.fname + '_crypto', 'r')
                output_file = open(self.fname + '_decrypto', 'w')
                for char in input_file.read():
                    if char in dict_crypto.keys():
                        output_file.write(dict_crypto[char])
        else:
            self.message1()

    def message1(self):
        reply=QMessageBox()
        reply.setText("You must select a file")
        reply.exec()

    def message2(self):
        reply = QMessageBox()
        reply.setText("You must generate a key")
        reply.exec()

    def message3(self):
        reply = QMessageBox()
        reply.setText("Key.txt doesn't exist")
        reply.exec()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())