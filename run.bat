@echo off
setlocal EnableDelayedExpansion

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
python --version > version.tmp 2>&1
if %errorlevel% neq 0 (
    echo Error: Could not execute Python. Make sure it is installed and in your PATH.
    del version.tmp 2>nul
    exit /b 1
)

set /p PYTHON_VERSION_LINE=<version.tmp
del version.tmp

echo %PYTHON_VERSION_LINE% | findstr /r "Python [0-9]" > nul
if %errorlevel% neq 0 (
    echo Error: Could not determine Python version.
    exit /b 1
)

for /f "tokens=2" %%V in ('echo %PYTHON_VERSION_LINE%') do set PYTHON_VERSION=%%V

echo Found Python %PYTHON_VERSION%

for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set "PYTHON_MAJOR=%%a"
    set "PYTHON_MINOR=%%b"
)

if "!PYTHON_MAJOR!" LSS "3" (
    echo Error: Python 3.13+ is required.
    exit /b 1
)
if "!PYTHON_MAJOR!"=="3" (
    if "!PYTHON_MINOR!" LSS "13" (
        echo Warning: Python 3.13+ is recommended, but proceeding with version %PYTHON_VERSION%.
    )
)
echo Python version OK!

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

REM Check if we're in a virtual environment
if defined VIRTUAL_ENV (
    REM In virtual env, don't use --user flag
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing dependencies. Trying with --no-cache-dir option...
        pip install -r requirements.txt --no-cache-dir
        if errorlevel 1 (
            echo Error installing dependencies.
            exit /b 1
        )
    )
) else (
    REM Not in virtual env, use --user flag
    pip install -r requirements.txt --user
    if errorlevel 1 (
        echo Error installing dependencies. Trying with --no-cache-dir option...
        pip install -r requirements.txt --user --no-cache-dir
        if errorlevel 1 (
            echo Error installing dependencies.
            exit /b 1
        )
    )
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
