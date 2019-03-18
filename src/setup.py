from cx_Freeze import setup, Executable
#import PyQt5


OSv = "Win32GUI"    

param = Executable(
        script="Windows 10 Tools.py", 
        base=OSv,
        icon="icon.ico"
        )

includefiles = [r"C:\Users\aless\Desktop\python\pytoexe\windows10tool\platforms"]

packages = ["idna","os","ctypes","urllib.request","zipfile","ipaddress","sys","netifaces","platform","subprocess","PyQt5"]

options = {
    'build_exe': {    
        'packages':packages,
        'include_files':includefiles
        
    },    
}

setup(
      name = 'Windows 10 Tools',
      version = '1.8',
      description = 'Creato da alessandrobasi.it',
      author = 'alessandrobasi.it',
      options = options,
      executables = [param]
)