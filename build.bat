@echo off
:: ─────────────────────────────────────────────────────────────────────────────
:: build.bat  —  One-click build script for Lab Management System
::
:: Run this from the project root:   build.bat
::
:: What it does:
::   1. Installs PyInstaller if not already installed
::   2. Cleans previous builds
::   3. Bundles the app with PyInstaller  →  dist\LabManagement\
::   4. Reminds you to compile installer.iss with Inno Setup
:: ─────────────────────────────────────────────────────────────────────────────

echo.
echo ========================================
echo  Lab Management System - Build Script
echo ========================================
echo.

:: ── Step 1: Make sure PyInstaller is installed ────────────────────────────────
echo [1/4] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo      Installing PyInstaller...
    pip install pyinstaller
) else (
    echo      PyInstaller is already installed.
)

:: ── Step 2: Clean old build artifacts ─────────────────────────────────────────
echo.
echo [2/4] Cleaning old build folders...
if exist build     rmdir /s /q build
if exist dist      rmdir /s /q dist

:: ── Step 3: Run PyInstaller ───────────────────────────────────────────────────
echo.
echo [3/4] Bundling application with PyInstaller...
echo       (This may take 2-5 minutes on first run)
echo.

pyinstaller app.spec --clean

if errorlevel 1 (
    echo.
    echo  ERROR: PyInstaller failed. Check the output above for details.
    pause
    exit /b 1
)

echo.
echo  SUCCESS: App bundled to:  dist\LabManagement\
echo  You can test it by running:  dist\LabManagement\LabManagement.exe

:: ── Step 4: Remind about Inno Setup ──────────────────────────────────────────
echo.
echo ========================================
echo [4/4] Create the installer .exe
echo ========================================
echo.
echo  1. Download and install Inno Setup from:
echo     https://jrsoftware.org/isdl.php
echo.
echo  2. Open Inno Setup Compiler
echo.
echo  3. File - Open  →  select  installer.iss  in this folder
echo.
echo  4. Build - Compile  (or press F9)
echo.
echo  5. Your installer will be saved as:
echo     installer_output\LabManagementSetup.exe
echo.
echo  That .exe is what you give to the end user.
echo.

pause
