@echo off
echo Starting Content Publishing Platform...

cd backend
echo Starting backend server on http://localhost:5000
start "Content Publishing Platform Backend" uvicorn main:app --host 0.0.0.0 --port 5000 --reload

echo.
echo Application is running!
echo.
echo Open your browser and navigate to: http://localhost:5000
echo.
echo Press Ctrl+C in the server window to stop the application when you're done.
echo.
pause