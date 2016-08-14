import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], 
                     "includes": ["matplotlib.backends.backend_qt4agg","matplotlib.pyplot"],
                     "include_files":[('HKAsserts.db', 'HKAsserts.db'),('PortfolioMan.ico', 'PortfolioMan.ico')] , 
                     "icon": "PortfolioMan.ico"
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PortfolioMan",
        version = "0.1",
        description = "PortfolioMan application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("PortfolioMan.py", base=base)])

# python setup.py build

# copy dll lib\site-packages\numpy\core mkl_intel_thread.dll, mkl_*.dll, libiomp5md.dll