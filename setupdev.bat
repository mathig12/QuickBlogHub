@echo off
echo Setting up Content Publishing Platform...

echo Creating .env file with database configuration...
echo # Database Configuration > .env
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/content_publishing >> .env
echo # Add other environment variables as needed >> .env

echo Creating requirements.txt file...
echo fastapi==0.104.0 > backend\requirements.txt
echo uvicorn==0.23.2 >> backend\requirements.txt
echo sqlalchemy==2.0.22 >> backend\requirements.txt
echo pydantic==2.4.2 >> backend\requirements.txt
echo python-dotenv==1.0.0 >> backend\requirements.txt
echo psycopg2-binary==2.9.9 >> backend\requirements.txt
echo alembic==1.12.0 >> backend\requirements.txt
echo jinja2==3.1.2 >> backend\requirements.txt
echo httpx==0.25.0 >> backend\requirements.txt
echo pytest==7.4.2 >> backend\requirements.txt

echo Installing required Python packages...
pip install -r backend\requirements.txt

echo Setting up database...
cd backend
python -c "from database import Base, engine; import models; Base.metadata.create_all(bind=engine)"

echo Setting up database migrations...
python -c "import os; from alembic import command; from alembic.config import Config; from pathlib import Path; config_path = Path('alembic.ini'); config = Config(str(config_path)); config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/content_publishing')); command.stamp(config, 'head')"

echo Creating initial database structure...
psql -U postgres -d content_publishing -c "
ALTER TABLE IF EXISTS posts 
ADD COLUMN IF NOT EXISTS tags VARCHAR,
ADD COLUMN IF NOT EXISTS quality_score FLOAT,
ADD COLUMN IF NOT EXISTS moderation_data JSONB,
ADD COLUMN IF NOT EXISTS warnings TEXT,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS published_at TIMESTAMP WITH TIME ZONE;"

cd ..

echo Setup completed successfully!
echo.
echo Run 'runapplication.bat' to start the application.
echo Then open your browser and go to: http://localhost:5000
echo.
pause