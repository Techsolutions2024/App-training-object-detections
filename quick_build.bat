@echo off
REM Quick Build Script for YOLO Training Studio
REM Publisher: TxTech
REM 
REM This script will:
REM 1. Install PyInstaller if needed
REM 2. Build the executable
REM 3. Create portable package

echo ============================================
echo   YOLO Training Studio - Quick Build
echo   Publisher: TxTech
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Install PyInstaller
echo [2/4] Installing PyInstaller...
pip install pyinstaller pillow
echo.

REM Run build script
echo [3/4] Building executable...
python build.py exe
echo.

REM Create portable package
echo [4/4] Creating portable package...
python build.py portable
echo.

echo ============================================
echo   BUILD COMPLETED!
echo ============================================
echo.
echo Executable: dist\YOLOTrainingStudio.exe
echo Portable:   YOLOTrainingStudio_v1.0.0_Portable.zip
echo.
echo To create installer (requires Inno Setup):
echo   python build.py installer
echo.
echo Or build everything:
echo   python build.py all
echo.
pause
