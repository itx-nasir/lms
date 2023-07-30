@echo off
title Lab Management System - ONE-CLICK INSTALLER
cls

echo ============================================
echo    Lab Management System - INSTALLER
echo ============================================
echo.
echo This will automatically install everything needed!
echo Please wait...
echo.

REM Check if Python is already installed
echo [1/5] Checking for Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo ✅ Python is already installed!
    goto :setup_app
)

echo Python not found. Installing Python automatically...
echo.

REM Download Python 3.11 installer
echo [2/5] Downloading Python 3.11 installer...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist python_installer.exe (
    echo ❌ Failed to download Python installer
    echo Please check your internet connection
    pause
    exit /b 1
)

echo ✅ Python installer downloaded!

REM Install Python 3.11 silently
echo [3/5] Installing Python 3.11...
echo This may take a few minutes...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0 Include_dev=0

REM Wait for installation to complete
echo Waiting for Python installation to complete...
timeout /t 45 /nobreak >nul

REM Clean up installer
del python_installer.exe

REM Refresh environment variables for Python 3.11
set PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts
refreshenv >nul 2>&1

echo ✅ Python installed successfully!

:setup_app
echo.
echo [4/5] Setting up Lab Management System...

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing required components...
pip install -r requirements.txt >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ Failed to install components
    echo Trying alternative method...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo [5/5] Creating startup file...

REM Create run script
echo @echo off > START_LAB_SYSTEM.bat
echo title Lab Management System >> START_LAB_SYSTEM.bat
echo cd /d "%%~dp0" >> START_LAB_SYSTEM.bat
echo call venv\Scripts\activate.bat >> START_LAB_SYSTEM.bat
echo cls >> START_LAB_SYSTEM.bat
echo echo ============================================ >> START_LAB_SYSTEM.bat
echo echo         Lab Management System >> START_LAB_SYSTEM.bat
echo echo ============================================ >> START_LAB_SYSTEM.bat
echo echo. >> START_LAB_SYSTEM.bat
echo echo 🚀 Starting the system... >> START_LAB_SYSTEM.bat
echo echo. >> START_LAB_SYSTEM.bat
echo echo 📱 OPEN YOUR WEB BROWSER AND GO TO: >> START_LAB_SYSTEM.bat
echo echo    http://localhost:8000 >> START_LAB_SYSTEM.bat
echo echo. >> START_LAB_SYSTEM.bat
echo echo 🔑 LOGIN WITH: >> START_LAB_SYSTEM.bat
echo echo    Username: admin >> START_LAB_SYSTEM.bat
echo echo    Password: LMSadmin2024! >> START_LAB_SYSTEM.bat
echo echo. >> START_LAB_SYSTEM.bat
echo echo ⚠️  KEEP THIS WINDOW OPEN WHILE USING THE SYSTEM >> START_LAB_SYSTEM.bat
echo echo    Press Ctrl+C to stop >> START_LAB_SYSTEM.bat
echo echo ============================================ >> START_LAB_SYSTEM.bat
echo echo. >> START_LAB_SYSTEM.bat
echo python main.py >> START_LAB_SYSTEM.bat
echo pause >> START_LAB_SYSTEM.bat

cls
echo ============================================
echo         INSTALLATION COMPLETE! ✅
echo ============================================
echo.
echo Everything is ready! Here's what to do:
echo.
echo 1. Double-click "START_LAB_SYSTEM.bat"
echo 2. Open your web browser
echo 3. Go to: http://localhost:8000  
echo 4. Login with: admin / LMSadmin2024!
echo.
echo ============================================
echo         IMPORTANT NOTES:
echo ============================================
echo • Keep this entire folder safe
echo • Always use "START_LAB_SYSTEM.bat" to run
echo • Don't close the black window when system is running
echo • Your data is saved automatically
echo.
echo Ready to start? Press any key...
pause >nul

REM Auto-start the system
echo Starting the system now...
call START_LAB_SYSTEM.bat