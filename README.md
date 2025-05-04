# Content Publishing Platform

A modern content publishing platform with AI moderation features, content quality scoring, and a professional user interface.

## Features

- Create and manage blog posts with a rich text editor
- AI-powered content moderation with quality scoring
- Content tagging system for better organization
- Dashboard with content statistics
- Advanced AI assistant with content improvement suggestions
- Multiple post statuses: draft, flagged, approved, published

## Requirements

- Windows 10 or 11
- Python 3.8+ (recommended: Python 3.11)
- PostgreSQL database
- Internet connection (for loading CDN resources)

## Installation Instructions for Windows

### 1. Install Python

1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
   - Check "Add Python to PATH"
   - Click "Install Now"

### 2. Install PostgreSQL

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer
   - Remember the password you set for the postgres user
   - Keep the default port (5432)
   - Complete the installation

### 3. Create a Database

1. Open Windows Command Prompt
2. Run the following commands:
   ```
   psql -U postgres
   ```
3. When prompted, enter the password you set during installation
4. In the PostgreSQL command prompt, create a database:
   ```
   CREATE DATABASE content_publishing;
   \q
   ```

### 4. Set Up the Project

1. Download this project and extract it
2. Open Command Prompt in the project directory
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
5. Run the setup script:
   ```
   setupdev.bat
   ```

### 5. Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
   ```
   runapplication.bat
   ```
3. Open your web browser and go to: http://localhost:5000

## Troubleshooting

- **Database Connection Issues**: Make sure PostgreSQL is running and check your database connection settings in `.env` file
- **Package Installation Errors**: Make sure you have activated the virtual environment before installing packages
- **Port Already in Use**: If port 5000 is already in use, you can change it in the `runapplication.bat` file

## License

This software is licensed under the MIT License.