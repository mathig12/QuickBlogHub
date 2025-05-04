@echo off
echo Setting up Content Publishing Platform...

echo.
echo Setting up backend...
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
cd backend
alembic upgrade head
cd ..

echo.
echo Setting up frontend...
cd frontend
npm install
cd ..

echo.
echo Setup complete! You can now run the application with runapplication.bat
