# Build with python setup.py py2exe

from distutils.core import setup
import py2exe
from glob import glob

data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

setup(
	console=['plink.py'],
	data_files=data_files,
	options={"py2exe":{"includes":["sip"]}},
)