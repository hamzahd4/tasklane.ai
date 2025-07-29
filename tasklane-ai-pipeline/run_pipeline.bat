@echo off
echo TaskLane AI Pipeline - Video to SOP Converter
echo =============================================

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check setup
echo Checking setup...
python main.py --check-setup

REM Run the pipeline
echo.
echo Starting pipeline...
python main.py %*

pause 