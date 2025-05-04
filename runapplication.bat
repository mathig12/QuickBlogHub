@echo off
echo Starting Content Publishing Platform...

echo.
echo Starting backend server...
start cmd /k "call env\Scripts\activate && cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Starting frontend server...
start cmd /k "cd frontend && npm start"

echo.
echo Servers are starting up...
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5000
echo.
echo Press any key to shut down the servers when you're done.
pause

echo.
echo Shutting down servers...
taskkill /f /im cmd.exe /fi "WINDOWTITLE eq *npm start*"
taskkill /f /im cmd.exe /fi "WINDOWTITLE eq *uvicorn*"
echo Servers shut down.
