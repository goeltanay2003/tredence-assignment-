@echo off
REM Quick start script for running the demo on Windows

echo.
echo ============================================================
echo   Workflow Engine - Demo & Test Suite
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import fastapi, pydantic" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Run the demo
echo Running demo...
echo.

python demo.py

if errorlevel 1 (
    echo.
    echo Demo failed!
    pause
    exit /b 1
) else (
    echo.
    echo Demo completed successfully!
    pause
)
