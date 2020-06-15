from os import environ, path


class StartUpClass():
    def __init__(self, master_class, statUp_password):

        self.master_class = master_class

        if statUp_password:
            self.master_class.changeScreen("styles/password.ui")
            self.master_class.conferma.clicked.connect(
                lambda: self.master_class.passwordScreen())
        else:
            self.master_class.changeScreen("styles/statUp.ui")
            self.master_class.conferma.clicked.connect(
                lambda: self.master_class.changeScreen("styles/pickDir.ui", self.pickDir))

    def pickDir(self):

        # <K>:\Users\<user>\Desktop
        desktop_path = path.join(
            environ["systemdrive"], environ["HOMEPATH"], "Desktop", "Windows 10 tool")
        # <K>:\Users\<user>\AppData\Local\Temp
        temp_path = path.join(
            environ["systemdrive"], environ["temp"], "Windows 10 tool")
        # <K>:\Users\<user>\Download
        download_path = path.join(
            environ["systemdrive"], environ["HOMEPATH"], "Downloads", "Windows 10 tool")

        self.master_class.cartelle.setText(
            f'''Desktop\t\t( {desktop_path} )\nTemp\t\t( {temp_path} )\nDownload\t\t( {download_path} )''')

        # Remember to pass the definition/method, not the return value!
        self.master_class.desktop.clicked.connect(
            lambda: self.master_class.setInstallDir(desktop_path))
        # Remember to pass the definition/method, not the return value!
        self.master_class.temp.clicked.connect(
            lambda: self.master_class.setInstallDir(temp_path))
        # Remember to pass the definition/method, not the return value!
        self.master_class.download_dir.clicked.connect(
            lambda: self.master_class.setInstallDir(download_path))
