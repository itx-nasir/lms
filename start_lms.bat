@echo off
echo Starting Lab Management System...
echo.
echo Open your web browser and go to: http://localhost:8000
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo.
where gunicorn >nul 2>&1
if %errorlevel%==0 (
	gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
) else (
	python -m uvicorn main:app --host 0.0.0.0 --port 8000
)
