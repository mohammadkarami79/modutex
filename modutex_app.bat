@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                     ModuTex Application v1.0                    ║
echo ║              Professional AI-Powered LaTeX Generator            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo [STARTUP] Launching beautiful desktop application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please run setup.bat first.
    pause
    exit /b 1
)

REM Launch the GUI application
echo [GUI] Starting ModuTex Desktop Application...
python modutex_gui.py

REM If we get here, the GUI closed
echo.
echo [EXIT] ModuTex Application closed.
echo Thank you for using ModuTex! 🚀
timeout 2 >nul 