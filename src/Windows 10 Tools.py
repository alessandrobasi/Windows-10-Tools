import os
import ctypes
#import socket
#import win32gui
#import pywinauto
import urllib.request
import zipfile
#import threading 

#from requests import get  # to make GET request
from ipaddress import ip_address
from sys import executable
from netifaces import gateways, ifaddresses, AF_LINK, AF_INET
from platform import uname
from subprocess import Popen


##  QT5

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

##

class Program(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # Set window title
        self.setWindowTitle('Windows 10 Tool')
        
        # Aspect of the window
        self.x = 200
        self.y = 200
        self.lunghezza = 500
        self.altezza = 250
        
        # Set where and how big is the window
        self.setGeometry(self.x, self.y, self.lunghezza, self.altezza)
        
        # Set status bar text
        self.statusBar().showMessage('By alessandrobasi.it')
        
        # Global cmd path
        self.cmd = os.path.join(os.environ["SYSTEMDRIVE"],"\\windows","system32","cmd.exe")
        
        ## TO startup
        self.startup()
        
        pass
    
    
    def startup(self):
        # Global text message
        self.testo = QLabel()
        
        # Set text message
        self.testo.setText('''Benvenuto nel tool di Windows 10

Creato da alessandrobasi.it
Ver. 1.8
03/03/2019\n''')
        
        # Local button
        button_desktop = QPushButton("Ok")
        
        ## TO scelta_cartella on click event
        button_desktop.clicked.connect(self.scelta_cartella)
        
        # Local layout
        # Horizontal layout
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        # Horizontal layout
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(button_desktop)
        layout1.addStretch(1)
        
        # Vertical layout
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addStretch(1)
        
        # Layout master
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
        
        ## START GUI
        self.show()
        
        pass
    
    
    def open_directory(self,cartella):
        # Global open directory
        
        def call():
            Popen(fr'explorer /separate, {cartella}')
        
        
        return call
    
    
    def run_program(self,programma,parm=None):
        # Global run program
        
        def call():
            
            if parm != None:
                Popen(r'Powershell -Command "& { Start-Process \"' + programma + r' \" \"' + parm + r'\" -Verb RunAs } " ')
            else:
                Popen(r'Powershell -Command "& { Start-Process \"' + programma + r' \" -Verb RunAs } " ')
            
        return call
    
    ## Install dir ##
    
    def scelta_cartella(self):
        # Location dir
        
        desktop  = os.path.join(os.environ["systemdrive"], os.environ["HOMEPATH"], "Desktop", "Windows 10 tool")   ## <K>:\Users\<user>\Desktop
        temp_dir = os.path.join(os.environ["systemdrive"], os.environ["temp"], "Windows 10 tool")                  ## <K>:\Users\<user>\AppData\Local\Temp
        
        # Local button
        button_desktop = QPushButton("Desktop")
        ## TO main on click event
        button_desktop.clicked.connect( self.set_install_dir(desktop) )
        
        # Local button
        button_temp = QPushButton("Temp")
        ## TO main on click event
        button_temp.clicked.connect(self.set_install_dir(temp_dir))
        
        
        self.testo.setText(f'''Scegliere dove salvare eventuali file scaricati

Desktop\t\t( {desktop} )
Temp\t\t( {temp_dir} )
''')
        
        # 
        # Same layout property
        # 
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(button_desktop)
        layout1.addWidget(button_temp)
        layout1.addStretch(1)
        
        
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addStretch(1)
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
        
        pass
    
    ## Intall dir ##
    
    def set_install_dir(self,nome_dir):
        
        # Set download dir
        
        def call():
            # Global install dir
            self.install_dir = nome_dir
            
            # TO main window
            self.main()
        
        return call
    
    ## End Install dir ##
    
    ## Download manager ##
    
    def download(self, tipo, downloadurl, file_scaricato, peso, zip_uncompress='', zip_run=''):
        
        # Global download window
        
        def call():
            
            dir_file = self.install_dir+"\\"+tipo
            run_exe = dir_file+"\\"+file_scaricato
            
            
            self.testo.clear()
            
            
            
            layout = QHBoxLayout()
            layout.addStretch(1)
            layout.addWidget(self.testo)
            layout.addStretch(1)
            
            
            layout1 = QHBoxLayout()
            
            
            
            vlayout = QVBoxLayout()
            vlayout.addLayout(layout)
            vlayout.addStretch(1)
            
            
            
            wid = QWidget(self)
            self.setCentralWidget(wid)
            wid.setLayout(vlayout)
            
            
            
            ## Sorgente file
            url = downloadurl 
            
            
            ## Verifica cartella
            if not os.path.exists(dir_file):
                ## Crea cartella
                os.makedirs(dir_file)
            
            ## Verifica file
            if not os.path.exists(dir_file+"\\"+file_scaricato):
                self.testo.setText(fr'''Downloading...
Da: {url}
Peso: {peso}
''')
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
            
            self.testo.setText(self.testo.text()+r'''Cosa vuoi fare?
    
Aprire la cartella
Eseguire il programma
Tornare indietro
''')
            
            
            
#            t1 = threading.Thread(target=thread_download )
#            
#            t2 = threading.Thread(target=gui)
#            
#            t1.start()
#            t2.start()
#            
#            t1.join()
#            t2.join()
            
            
            apri_cartella = QPushButton("Aprire la cartella")
            apri_cartella.clicked.connect( self.open_directory(dir_file) )
            
            #print(self.cmd,r"/k " + run_exe + r"")
            
            esegui_programma = QPushButton("eseguire il programma")
            if file_scaricato.endswith(".cmd") or zip_run.endswith(".cmd"):
                #esegui_programma.clicked.connect( self.run_program(self.cmd,r"/k " + run_exe + r"") )
                esegui_programma.clicked.connect( self.run_program(run_exe) )
            else:
                esegui_programma.clicked.connect( self.run_program(run_exe) )
            
            back = QPushButton("<-- Tornare indietro")
            back.clicked.connect( self.main )
                
            layout1.addStretch(1)
            layout1.addWidget(apri_cartella)
            layout1.addWidget(esegui_programma)
            layout1.addStretch(1)
            
            vlayout.addLayout(layout1)
            vlayout.addStretch(1)
            vlayout.addWidget(back)
            
            
        return call
    
    ## End Download manager ##
    
    ## Home window  ##
    
    def main(self):
        
        # Get network info from library (netiface)
        for nic in gateways()['default'].values():
            if ip_address(nic[0]).version == 4:
                gateway = nic[0]
                interface = nic[1]
        
        mac = ifaddresses(interface)[AF_LINK][0]['addr']
        ip, subnet, broadcast = ifaddresses(interface)[AF_INET][0].values()
        
        # Get system info form library (platform)
        sistema,nome,_,versione,_,processore = list(uname())
        
        self.testo.setText(f'''###### Info ######
Network info:
    GUID interfaccia:\t\t{interface}
    MAC interface:\t\t{mac}
    Gateway:\t\t{gateway} 
    IP:\t\t\t{ip} 
    Broadcast:\t\t{broadcast}
    Subnet:\t\t{subnet}

System info:
    Sistema:\t\t{sistema}
    Versione:\t\t{versione}
    Processore:\t\t{processore}
    Processori logici:\t\t{os.cpu_count()}
    Nome di sistema:\t\t{nome}

Cosa devo fare?
''')
    
        
        win_update = QPushButton("Tool Windows Update")
        win_update.clicked.connect( self.windows_update )
        
        download_antivirus = QPushButton("Scaricare Antivirus")
        download_antivirus.clicked.connect( self.download_antivirus )
        
        cmd_commandi = QPushButton("Comandi CMD")
        cmd_commandi.clicked.connect( self.cmd_command )
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(win_update)
        layout1.addWidget(download_antivirus)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(cmd_commandi)
        layout2.addStretch(1)
        
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addLayout(layout2)
        vlayout.addStretch(1)
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
    
    
        pass
    
    
    def windows_update(self):
        
        self.testo.setText(f'''Cosa vuoi aprire?

''')
        
        win_update = QPushButton("Aprire impostazioni di Windows Update")
        win_update.clicked.connect( self.open_directory('ms-settings:windowsupdate-options') )
        
        tool_win_update = QPushButton("Scaricare tool di pulizia di Window Update")
        tool_win_update.clicked.connect( self.download('win_update_tool','https://gallery.technet.microsoft.com/scriptcenter/Reset-Windows-Update-Agent-d824badc/file/201129/1/ResetWUEng.zip','ResetWUEng.zip','8 KB','Reset Windows Update Tool','ResetWUEng.cmd') )
        
        update_assistant = QPushButton("Scaricare Windows Update Assistant")
        update_assistant.clicked.connect( self.download('win_update_assistant','https://download.microsoft.com/download/9/4/E/94E04254-741B-4316-B1DF-8CAEDF2DF16C/Windows10Upgrade9252.exe','Windows10Upgrade9252.exe','5.8 MB') )
        
        back = QPushButton("<-- Tornare indietro")
        back.clicked.connect( self.main )
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(win_update)
        layout1.addWidget(tool_win_update)
        layout1.addStretch(1)
        
        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(update_assistant)
        layout2.addStretch(1)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(back)
        
        
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addStretch(1)
        vlayout.addLayout(layout2)
        vlayout.addStretch(1)
        vlayout.addLayout(layout3)
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
    
    
        pass
    
    
    def download_antivirus(self):
        self.testo.setText('''Scegliere quale antivirus scaricare
Kaspersky (no-install)
Kaspersky Free (install)
''')
        
        download_kaspersky_no_install = QPushButton("Kaspersky (no-install)")
        download_kaspersky_no_install.clicked.connect( self.download('Kaspersky_no_install','http://devbuilds.kaspersky-labs.com/devbuilds/KVRT/latest/full/KVRT.exe','KVRT.exe','150 MB'))
        
        download_kaspersky_install = QPushButton("Kaspersky Free (install)")
        download_kaspersky_install.clicked.connect( self.download('Kaspersky_install','https://products.s.kaspersky-labs.com/homeuser/kfa2019/19.0.0.1088ab/italian-0.3880.0/5c42f68b/startup_15002.exe','startup_15002.exe','2.45 MB\n(Il file effettua download aggiuntivi)') )
        
        back = QPushButton("<-- Tornare indietro")
        back.clicked.connect( self.main )
        
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(download_kaspersky_no_install)
        layout1.addWidget(download_kaspersky_install)
        layout1.addStretch(1)
        
        
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addStretch(1)
        vlayout.addWidget(back)
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
        
        
        pass

    def cmd_command(self):
        self.testo.setText('''Scegliere quale comando eseguire
''')
        
        cmd_dism = QPushButton("Integrità Windows DISM")
        cmd_dism.clicked.connect( self.run_program(self.cmd,r"/k DISM.exe /Online /Cleanup-image /Restorehealth") )
        
        cmd_sfc = QPushButton("File check SFC")
        cmd_sfc.clicked.connect( self.run_program(self.cmd,r"/k sfc /scannow") )
        
        back = QPushButton("<-- Tornare indietro")
        back.clicked.connect( self.main )
        
        
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.testo)
        layout.addStretch(1)
        
        
        layout1 = QHBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(cmd_dism)
        layout1.addWidget(cmd_sfc)
        layout1.addStretch(1)
        
        
        vlayout = QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addStretch(1)
        vlayout.addLayout(layout1)
        vlayout.addStretch(1)
        vlayout.addWidget(back)
        
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vlayout)
        
        
        pass



## Start GUI
def start():
    
    # QT auto pixel scale
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    # Create instance of GUI
    app = QApplication([])
    
    # QT auto pixel scale
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    # QT GUI icon  -  USELESS
    app.setWindowIcon(QIcon('icon.ico'))
    
    ## RUN
    ex = Program()
    app.exec_()



# Function for checking privileges
def is_admin():
    
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    # Return True if is in privilege mode
    # Return False if isn't in privilege mode
    return is_admin


## Start program ##

# APP ID  -  useless?
myappid = 'alessandrobasiit.windows01tool.program.18'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Check if the program is in privilege mode, if is not
if not is_admin():
    
    # Call privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, executable, None, 1)
    
# If the program has privilage
if is_admin():
    
    
    ## Start GUI
    start()

## If not error message
else:
    ctypes.windll.user32.MessageBoxW(0, "Avvia il programma come amministratore", "Errore", 0)


## END