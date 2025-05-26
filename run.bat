@echo off
setlocal

REM Banner
echo ================================
echo TR_tts Project Runner
echo ================================

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo.
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
)

REM Check Python version
echo.
echo Checking Python version...
for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
    set PYTHON_VERSION=%%v
)

if defined PYTHON_VERSION (
    for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
        set PYTHON_MAJOR=%%a
        set PYTHON_MINOR=%%b
    )
    echo Found Python %PYTHON_VERSION%
    if %PYTHON_MAJOR% LSS 3 (
        echo Error: Python 3.13+ is required.
        exit /b 1
    )
    if %PYTHON_MAJOR% EQU 3 (
        if %PYTHON_MINOR% LSS 13 (
            echo Error: Python 3.13+ is required.
            exit /b 1
        )
    )
    echo Python version OK!
) else (
    echo Error: Python not found. Please install Python 3.13+ and ensure it is in your PATH.
    exit /b 1
)

REM Check FFmpeg
echo.
echo Checking FFmpeg...
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: FFmpeg is not installed or not in PATH
    echo Please install FFmpeg from https://github.com/BtbN/FFmpeg-Builds/releases
    exit /b 1
)
echo FFmpeg is installed. OK!

REM Check Google Cloud credentials
echo.
echo Checking Google Cloud credentials...
if not defined GOOGLE_APPLICATION_CREDENTIALS (
    echo Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set
    echo You may need to set up Google Cloud credentials before TTS functionality will work.
    echo See: https://cloud.google.com/docs/authentication/application-default-credentials
)

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies.
    exit /b 1
)

REM Create necessary directories
echo.
echo Setting up directories...
if not exist "output" mkdir output
if not exist "work" mkdir work

REM Run the application
echo.
echo Starting TR_tts application...
echo Access the web interface at http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

endlocal
