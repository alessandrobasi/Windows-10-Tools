from requests import get
from shutil import copyfileobj

from PyQt5.QtCore import QThread


class downloadFile(QThread):

    def __init__(self, masterClass, url, nomeFile, parent=None):
        super().__init__()
        self.url = url
        self.masterClass = masterClass
        self.nomefile = nomeFile

        self.finished.connect(self.masterClass.unlockScreen)

    def run(self):
        local_filename = self.nomefile
        print("downloading")
        with get(self.url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                copyfileobj(r.raw, f)
        print("finito")
