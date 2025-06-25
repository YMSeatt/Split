# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller Spec file for BehaviorLogger.

To build the executable, run the following command in your terminal
from the same directory as this spec file:
    pyinstaller BehaviorLogger.spec

This will create a 'build' and 'dist' folder. Your final .exe file
will be inside the 'dist' folder.
"""

from PyInstaller.utils.hooks import collect_all

# --- Configuration ---
# It's highly recommended to use relative paths for portability.
# For example, if this spec file is in your project root:
# SCRIPT_PATH = 'Split/__main__.py'
# ICON_PATH = 'assets/LightningChocolate.ico'
# For Windows executables, it's best to use a .ico file for the icon.
SCRIPT_PATH = "C:\\Users\\Yaakov M\\Jaffe Project\\Split\\__main__.py"
ICON_PATH = "C:\\Users\\Yaakov M\\OneDrive\\Pictures\\Logo\\Variations\\LightningChocolate.png"
APP_NAME = "BehaviorLogger v54"

# --- Data and Binary Collection ---
# Use the collect_all utility to gather necessary files from packages.
# Note: collect_all uses the package's import name (e.g., 'sv_ttk' not 'sv-ttk').
datas, binaries = [], []
packages_to_collect = ['openpyxl', 'tkcalendar', 'sv_ttk', 'darkdetect']
for package in packages_to_collect:
    pkg_datas, pkg_binaries = collect_all(package)
    datas.extend(pkg_datas)
    binaries.extend(pkg_binaries)

# --- Analysis ---
# This is the core of the spec file. It finds all the code your app needs.
a = Analysis(
    [SCRIPT_PATH],
    pathex=[],  # You can add paths to your own modules here
    binaries=binaries,
    datas=datas,
    hiddenimports=[],  # List any modules PyInstaller might miss
    hookspath=[],
    runtime_hooks=[],
    # Exclude modules to reduce final executable size
    excludes=['PyQt5', 'PySide6', 'tkcap', 'matplotlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# --- PYZ (Python Zipped Archive) & EXE ---
# This bundles everything into the final single-file executable.
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=APP_NAME,
    debug=False,
    strip=False,
    upx=True,  # UPX compression, set to False if it causes issues
    runtime_tmpdir=None,
    console=False, # Creates a windowed (GUI) app
    icon=ICON_PATH,
)