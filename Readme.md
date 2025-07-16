# RF Calculator
Various calculator related to RF measurement 

# Features
- Field strength conversion
- EIRP calculator
- Interpolation for transducer factor
- Antenna to EUT distance based on 3dB beamwidth
- Limit calculator from two different testing distance

# Packaging with PyInstaller
use the following command for packaging using Pyinstaller. Do not use onefile option

    PyInstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"
    python -m PyInstaller --noconfirm --onedir --windowed --add-data "customtkinter path"  --paths=src run.py 
