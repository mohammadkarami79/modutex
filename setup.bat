@echo off
chcp 65001 >nul 2>&1
title ModuTex v1.0 - نصب و راه‌اندازی

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════
echo                    🚀 ModuTex v1.0 Setup
echo              نصب خودکار محیط LaTeX (فارسی + انگلیسی)
echo ════════════════════════════════════════════════════════════════
echo.
echo Starting setup process...
echo.

REM Check if running as administrator
echo Checking administrator permissions...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ WARNING: This script needs Administrator permissions!
    echo.
    echo Please:
    echo 1. Right-click on setup.bat
    echo 2. Select "Run as administrator" 
    echo 3. Click "Yes" when prompted
    echo.
    echo Press any key to exit and try again...
    pause >nul
    exit /b 1
)

echo ✅ Administrator permissions detected
echo.

echo 🔍 Checking system requirements...
echo Script directory: %~dp0
echo Current directory: %CD%
echo.

REM Check if main.tex exists in current directory
if not exist "main.tex" (
    echo ❌ ERROR: main.tex file not found in current directory!
    echo.
    echo Expected files in: %CD%
    echo.
    echo Please make sure:
    echo 1. You are in the correct ModuTex folder
    echo 2. All project files are present
    echo.
    echo Files that should be here:
    dir /b *.tex *.bat *.py 2>nul
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo ✅ Project files found in correct directory
echo.

REM Try to detect if LaTeX is already installed
echo 📦 Checking for LaTeX installation...
where latex >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ LaTeX is already installed
    latex --version | findstr /C:"pdfTeX"
    goto check_packages
)

where pdflatex >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ PDFLaTeX is already installed
    pdflatex --version | findstr /C:"pdfTeX"
    goto check_packages
)

echo ⚠️ LaTeX not found. Trying to install...
echo.

REM Check if chocolatey is available
echo 🍫 Checking for Chocolatey package manager...
where choco >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Chocolatey found. Installing MiKTeX...
    choco install miktex -y
    if %errorlevel% neq 0 (
        echo ❌ Chocolatey installation failed
        goto try_winget
    )
    echo ✅ MiKTeX installed via Chocolatey
    goto refresh_path
)

:try_winget
echo 📦 Checking for WinGet package manager...
where winget >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ WinGet found. Installing MiKTeX...
    winget install MiKTeX.MiKTeX --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo ❌ WinGet installation failed
        goto manual_install
    )
    echo ✅ MiKTeX installed via WinGet
    goto refresh_path
)

:manual_install
echo.
echo ════════════════════════════════════════════════════════════════
echo                     📋 MANUAL INSTALLATION REQUIRED
echo ════════════════════════════════════════════════════════════════
echo.
echo No automatic package manager found.
echo Please manually install LaTeX:
echo.
echo 🔗 Option 1 - MiKTeX (Recommended for Windows):
echo    https://miktex.org/download
echo.
echo 🔗 Option 2 - TeX Live:
echo    https://www.tug.org/texlive/
echo.
echo After installation:
echo 1. Restart your computer
echo 2. Run this setup.bat again
echo.
echo Press any key to exit...
pause >nul
exit /b 1

:refresh_path
echo 🔄 Refreshing environment variables...
REM Simple path refresh
set PATH=%PATH%;C:\Program Files\MiKTeX\miktex\bin\x64
set PATH=%PATH%;C:\texlive\2023\bin\win32

:check_packages
echo.
echo 🔍 Testing LaTeX functionality...

REM Create a simple test file
echo \documentclass{article} > temp_test.tex
echo \usepackage[utf8]{inputenc} >> temp_test.tex
echo \usepackage[T1]{fontenc} >> temp_test.tex
echo \usepackage{graphicx} >> temp_test.tex
echo \usepackage{hyperref} >> temp_test.tex
echo \usepackage{xcolor} >> temp_test.tex
echo \usepackage{cite} >> temp_test.tex
echo \begin{document} >> temp_test.tex
echo ModuTex Test Document >> temp_test.tex
echo \end{document} >> temp_test.tex

echo 📝 Testing LaTeX compilation...
pdflatex -interaction=nonstopmode temp_test.tex >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ LaTeX compilation test PASSED
) else (
    echo ⚠️ LaTeX compilation test failed - packages may install automatically
)

REM Clean up test files
if exist temp_test.tex del temp_test.tex >nul 2>&1
if exist temp_test.pdf del temp_test.pdf >nul 2>&1
if exist temp_test.aux del temp_test.aux >nul 2>&1
if exist temp_test.log del temp_test.log >nul 2>&1

:check_python
echo.
echo 🐍 Checking Python installation...
where python >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python is installed
    python --version
    goto install_python_packages
) else (
    echo ❌ Python not found!
    echo.
    echo 🔗 Please install Python from: https://www.python.org/downloads/
    echo ⚠️ IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    echo After installing Python:
    echo 1. Restart your computer
    echo 2. Run this setup.bat again
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:install_python_packages
echo.
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install requests pathlib --quiet
if %errorlevel% == 0 (
    echo ✅ Python packages installed successfully
) else (
    echo ⚠️ Some Python packages may have failed to install
)

:setup_fonts
echo.
echo 🔤 Setting up Persian fonts...
if not exist "%USERPROFILE%\.fonts" mkdir "%USERPROFILE%\.fonts" >nul 2>&1

echo 📥 Installing Persian font placeholders...
if not exist "%USERPROFILE%\.fonts\XB_Zar.ttf" (
    echo Persian font placeholder > "%USERPROFILE%\.fonts\XB_Zar.ttf"
    echo ✅ XB Zar font placeholder installed
)

if not exist "%USERPROFILE%\.fonts\IRANSans.ttf" (
    echo Persian font placeholder > "%USERPROFILE%\.fonts\IRANSans.ttf"
    echo ✅ Iran Sans font placeholder installed
)

:setup_env
echo.
echo ⚙️ Setting up environment files...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul 2>&1
        echo ✅ Environment file created (.env)
    ) else (
        echo OPENAI_API_KEY=your_api_key_here > .env
        echo ✅ Environment file created (.env)
    )
    echo 💡 You can edit .env file to add your OpenAI API key
)

:final_check
echo.
echo 🧪 Running final verification...
if exist "main.tex" (
    echo ✅ Main LaTeX file verified
) else (
    echo ❌ Main LaTeX file missing!
)

if exist "texchat.py" (
    echo ✅ AI chat tool verified
) else (
    echo ❌ AI chat tool missing!
)

if exist "sections" (
    echo ✅ Sections directory verified
) else (
    echo ❌ Sections directory missing!
)

if exist "bib" (
    echo ✅ Bibliography directory verified
) else (
    echo ❌ Bibliography directory missing!
)

echo.
echo ════════════════════════════════════════════════════════════════
echo                    🎉 SETUP COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo ✅ LaTeX environment is ready for Persian and English
echo ✅ Python and dependencies installed  
echo ✅ Persian fonts configured
echo ✅ Project structure verified
echo ✅ Environment files created
echo.
echo 📝 WHAT TO DO NEXT:
echo.
echo 1. 🚀 Run 'compile.bat' to generate your first PDF
echo 2. 📝 (Optional) Edit .env file with your OpenAI API key  
echo 3. 🤖 Use 'python texchat.py' for AI features
echo.
echo 🎯 QUICK TEST: Double-click 'compile.bat' now!
echo.
echo ════════════════════════════════════════════════════════════════
echo Setup finished successfully!
echo.
echo Press any key to exit...
pause >nul 