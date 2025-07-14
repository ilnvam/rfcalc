# Packaging with PyInstaller
use the following command for packaging using Pyinstaller. Do not use onefile option

    PyInstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"
    python -m PyInstaller --noconfirm --onedir --windowed --add-data "C:\Users\61432\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\customtkinter;customtkinter/"  --paths=src run.py 