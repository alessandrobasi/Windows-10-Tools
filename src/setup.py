from cx_Freeze import setup, Executable

OSv = "Win32GUI"    

param = Executable(
        script="Windows 10 Tools.py", 
        base=OSv,
        icon="icon.ico"
        )

includefiles = [r"platforms",r"icon.ico",r"styles"]

packages = ["sys","urllib","multiprocessing","idna.idnadata","requests","shutil","os","netifaces","platform","hashlib","subprocess","PyQt5"]

options = {
    'build_exe': {    
        'packages':packages,
        'include_files':includefiles
        
    },    
}

setup(
      name = 'Windows 10 Tools',
      version = '2.0',
      description = 'Created by alessandrobasi.it',
      author = 'alessandrobasi.it',
      options = options,
      executables = [param]
)