import sys
import urllib.request
from requests import get
from multiprocessing import Queue
from shutil import copyfileobj
from os import environ, path, cpu_count, makedirs
from netifaces import gateways, ifaddresses, AF_LINK, AF_INET
from platform import uname
from hashlib import sha256
from subprocess import Popen

#Qt5
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import QThread, Qt
from PyQt5.Qt import QCoreApplication

class downloadFile(QThread):

    def __init__(self, url, nomeFile, parent=None):
        super().__init__(parent)
        self.url = url
        self.nomefile = nomeFile
        self.finished.connect(window.unlockScreen)

    def run(self):
        local_filename = self.nomefile
        print("downloading")
        with get(self.url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                copyfileobj(r.raw, f)
        print("finito")

class MainWindow(QMainWindow):
    # INIT
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Config
        self.statUp_password = 0
        self.show_proxy_allert = 0
        self.install_dir = ""
        self.cmd = path.join(environ["SYSTEMDRIVE"], "\\windows", "system32", "cmd.exe")

        self.startUp()

    # Util funct
    def changeScreen(self, fileUi, nextFunct=""):
        self.__nextFunct = nextFunct
        uic.loadUi(fileUi, self)
        if self.__nextFunct != "":
            self.__nextFunct()
        self.show()

    def passwordScreen(self):
        passkey = "93e289bfc27ef917a03509c590e408f1a7ce5510143cb9a31012e975a724c736"
        hs = sha256(self.password.text().encode('utf-8')).hexdigest()
        if passkey == hs:
            self.changeScreen("styles/pickDir.ui", self.pickDir) # load ui
            #statUi() #run ui

    def setInstallDir(self, nome_dir):
        # Set download dir
        # Global install dir
        self.install_dir = nome_dir

        ## Verifica cartella
        if not path.exists(self.install_dir):
            ## Crea cartella
            makedirs(self.install_dir)

        ## Verifica file
        """
        if not os.path.exists(dir_file+"\\"+file_scaricato):
            self.testo.setText(fr'''Downloading...\nDa: {url}\nPeso: {peso}''')
            QApplication.processEvents()
            ## Download file
            urllib.request.urlretrieve(url, dir_file+"\\"+file_scaricato)
        
            self.testo.setText(self.testo.text()+"\nDownload finito\n")
        
        if file_scaricato.endswith("zip"):
            
            run_exe_temp = dir_file + '\\' + zip_uncompress + '\\' + zip_run
            
            if not os.path.exists(run_exe_temp):
            
                self.testo.setText(self.testo.text()+"\nUnzipping...")
                
                ## Unzip
                zip_ref = zipfile.ZipFile(run_exe, 'r')
                zip_ref.extractall(dir_file)
                zip_ref.close()
                
                
                
                self.testo.setText(self.testo.text()+"\nUnzip finito\n\n")
        
            run_exe = run_exe_temp
            
        if not self.testo.text():
            self.testo.setText('File già scaricato\n')
        
        self.testo.setText(self.testo.text()+r'''Cosa vuoi fare?\nAprire la cartella\nEseguire il programma\nTornare indietro''')
        """

        # TO main window
        self.changeScreen("styles/mainWin.ui", self.mainWin)

    def openDir(self, cartella):
        
        try:
            Popen(fr'explorer /separate, {cartella}')
        except:
            Popen(fr'explorer')

    def runProgram(self, program, parm=None):
        # Global run program
        try:
            if parm != None:
                Popen(r'Powershell -Command "& { Start-Process \"' + program + r' \" \"' + parm + r'\" -Verb RunAs } " ')
            else:
                Popen(r'Powershell -Command "& { Start-Process \"' + program + r' \" -Verb RunAs } " ')
        except:
            pass

    def lockScreen(self):
        butt = self.findChild(QPushButton, 'back')
        butt.setEnabled(False)

    def unlockScreen(self):
        butt = self.findChild(QPushButton, 'back')
        butt.setEnabled(True)

    def download(self, thread, fileUi, nextFunct=""):
        self.lockScreen()
        thread.start()
        #self.changeScreen(fileUi, nextFunct)


    # Screens
    def startUp(self):
        if self.statUp_password:
            self.changeScreen("styles/password.ui") # load ui
            #statUi() #run ui
        else:
            statUi = self.changeScreen("styles/statUp.ui") # load ui
            #statUi() #run ui

        
        if self.statUp_password:
            self.conferma.clicked.connect(lambda: self.passwordScreen() ) # Remember to pass the definition/method, not the return value!
        else:
            self.conferma.clicked.connect(lambda: self.changeScreen("styles/pickDir.ui", self.pickDir) )

    def pickDir(self):

        desktop_path = path.join(environ["systemdrive"], environ["HOMEPATH"], "Desktop", "Windows 10 tool")    ## <K>:\Users\<user>\Desktop
        temp_path = path.join(environ["systemdrive"], environ["temp"], "Windows 10 tool")                   ## <K>:\Users\<user>\AppData\Local\Temp
        download_path = path.join(environ["systemdrive"], environ["HOMEPATH"], "Downloads", "Windows 10 tool") ## <K>:\Users\<user>\Download

        self.cartelle.setText(f'''Desktop\t\t( {desktop_path} )\nTemp\t\t( {temp_path} )\nDownload\t\t( {download_path} )''')

        self.desktop.clicked.connect(lambda: self.setInstallDir(desktop_path)) # Remember to pass the definition/method, not the return value!
        self.temp.clicked.connect(lambda: self.setInstallDir(temp_path)) # Remember to pass the definition/method, not the return value!
        self.download_dir.clicked.connect(lambda: self.setInstallDir(download_path)) # Remember to pass the definition/method, not the return value!
    
    def mainWin(self):

        if self.info.text() == "Info":
            gateway, interface = list(gateways()['default'].values())[0]
            mac = ifaddresses(interface)[AF_LINK][0]['addr']
            ip, subnet, broadcast = ifaddresses(interface)[AF_INET][0].values()
            sistema, nome, _, versione, _, processore = list(uname())

            testo = '''###### Info ######\n'''
            if urllib.request.getproxies() or self.show_proxy_allert:
                testo = testo + f"\n⚠️ Sono impostati dei proxy su Windows\n\n"
            testo = testo + f'''Network info:\n\tMAC interface:\t\t{mac}\n\tGateway:\t\t\t{gateway}\n\tLocal IP:\t\t\t{ip}\n\tBroadcast:\t\t{broadcast}\n\tSubnet:\t\t\t{subnet}\n\nSystem info:\n\tOperating System:\t\t{sistema}\n\tVersion:\t\t\t{versione}\n\tProcessor:\t\t{processore}\n\tLogical Processor:\t\t{cpu_count()}\n\tSystem Name:\t\t{nome}'''

            self.info.setText(testo)

        self.toolWindowsUpdate.clicked.connect(lambda: self.changeScreen("styles/toolWinUp.ui", self.toolWinUp))
        self.antivirusBnt.clicked.connect(lambda: self.changeScreen("styles/antivirus.ui", self.antivirus))
        self.cmdCommands.clicked.connect(lambda: self.changeScreen("styles/cmdScript.ui", self.cmdScript))
        self.misc.clicked.connect(lambda: self.changeScreen("styles/misc.ui", self.miscScreen))

    def toolWinUp(self):

        back = self.findChild(QPushButton, 'back')
        back.clicked.connect(lambda: self.changeScreen("styles/mainWin.ui", self.mainWin))

        self.openWinUp.clicked.connect(lambda: self.openDir('ms-settings:windowsupdate-options'))

        downWinUpCleaning_file = downloadFile("https://gallery.technet.microsoft.com/scriptcenter/Reset-Windows-Update-Agent-d824badc/file/224689/1/ResetWUEng.zip", self.install_dir + "//ResetWUEng.zip")
        self.downWinUpCleaning.clicked.connect(lambda: self.download(downWinUpCleaning_file, None, None))

        downWinUpAssist_file = downloadFile("https://go.microsoft.com/fwlink/?LinkID=799445", self.install_dir + "//Windows10Upgrade.exe")
        self.downWinUpAssist.clicked.connect(lambda: self.download(downWinUpAssist_file, None, None))

    def antivirus(self):
        back = self.findChild(QPushButton, 'back')
        back.clicked.connect(lambda: self.changeScreen("styles/mainWin.ui", self.mainWin))

        downKaspNoInstall_file = downloadFile("https://devbuilds.s.kaspersky-labs.com/devbuilds/KVRT/latest/full/KVRT.exe", self.install_dir + "//KVRT.exe")
        self.downKaspNoInstall.clicked.connect(lambda: self.download(downKaspNoInstall_file, None, None))

        downKaspInstall_file = downloadFile("https://trial.s.kaspersky-labs.com/registered/ptlklc45zcck7s2ghjeb/3235323732337c44454c7c32/ks3.020.0.14.1085abcdeit_19851.exe", self.install_dir + "//KVRT.exe")
        self.downKaspInstall.clicked.connect(lambda: self.download(downKaspInstall_file, None, None))

    def cmdScript(self):
        back = self.findChild(QPushButton, 'back')
        back.clicked.connect(lambda: self.changeScreen("styles/mainWin.ui", self.mainWin))

        self.runDismCommand.clicked.connect(lambda: self.runProgram(self.cmd, r"/k DISM.exe /Online /Cleanup-image /Restorehealth"))
        self.runSfcCommand.clicked.connect(lambda: self.runProgram(self.cmd, r"/k sfc /scannow"))
        self.emptyDnsCache.clicked.connect(lambda: self.runProgram(self.cmd, r"/k ipconfig /flushdns"))
        self.emptyArpTable.clicked.connect(lambda: self.runProgram(self.cmd, r"/k arp -d && echo Done"))

    def miscScreen(self):
        back = self.findChild(QPushButton, 'back')
        back.clicked.connect(lambda: self.changeScreen("styles/mainWin.ui", self.mainWin))

        host = path.join(environ["systemdrive"], "\\Windows", "System32", "drivers", "etc")

        self.openHostsFile.clicked.connect(lambda: self.openDir(host))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
