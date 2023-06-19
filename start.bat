@echo off
echo Starting Lab Management System...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting the Lab Management System...
echo Open your browser and go to: http://localhost:8000
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py