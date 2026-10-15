@echo off
title Mark XLVIII - Windows Installer
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          MARK XLVIII - WINDOWS INSTALLER                         ║
echo ║                                                                  ║
echo ║   This will install everything automatically.                    ║
echo ║   No Git required. No permission issues.                         ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

:: Run the installer
echo Starting installation...
echo.
python install_windows.py

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    echo.
    echo Try running as Administrator:
    echo   1. Right-click this file
    echo   2. Select "Run as administrator"
    echo.
)

echo.
pause
