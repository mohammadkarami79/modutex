@echo off
chcp 65001 >nul 2>&1
title ModuTex v1.0 - PDF Compilation

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════
echo                    🚀 ModuTex v1.0 Compiler
echo ════════════════════════════════════════════════════════════════
echo.
echo 📝 Compiling LaTeX document to PDF...
echo Current directory: %CD%
echo.

REM Check if main.tex exists
if not exist "main.tex" (
    echo ❌ ERROR: main.tex not found!
    echo Make sure you are in the correct directory.
    pause
    exit /b 1
)

echo ✅ Found main.tex file
echo.

REM Clean up any previous compilation files
echo 🧹 Cleaning previous compilation files...
if exist "main.pdf" del "main.pdf" >nul 2>&1
if exist "main.aux" del "main.aux" >nul 2>&1
if exist "main.log" del "main.log" >nul 2>&1
if exist "main.out" del "main.out" >nul 2>&1
if exist "main.toc" del "main.toc" >nul 2>&1
if exist "main.bbl" del "main.bbl" >nul 2>&1
if exist "main.blg" del "main.blg" >nul 2>&1

echo ✅ Cleanup completed
echo.

REM Use PDFLaTeX for better compatibility
echo 📝 Starting LaTeX compilation...

where pdflatex >nul 2>&1
if %errorlevel% == 0 (
    echo 🔧 Using PDFLaTeX engine...
    echo.
    echo Pass 1: Initial compilation...
    pdflatex -interaction=nonstopmode main.tex >nul 2>&1
    
    echo Pass 2: Processing bibliography...
    bibtex main >nul 2>&1
    
    echo Pass 3: Resolving cross-references...
    pdflatex -interaction=nonstopmode main.tex >nul 2>&1
    
    echo Pass 4: Final compilation...
    pdflatex -interaction=nonstopmode main.tex >nul 2>&1
    
) else (
    echo ❌ PDFLaTeX not found! Please install TeX Live or MiKTeX.
    pause
    exit /b 1
)

echo.
echo 🔍 Checking compilation results...

REM Check if compilation was successful
if exist "main.pdf" (
    echo ✅ PDF compilation successful!
    
    REM Show file info without complex size checking
    echo 📊 PDF file information:
    dir "main.pdf" | findstr main.pdf
    
    echo.
    echo 🧹 Cleaning up auxiliary files...
    if exist "main.aux" del "main.aux" >nul 2>&1
    if exist "main.log" del "main.log" >nul 2>&1
    if exist "main.out" del "main.out" >nul 2>&1
    if exist "main.toc" del "main.toc" >nul 2>&1
    if exist "main.bbl" del "main.bbl" >nul 2>&1
    if exist "main.blg" del "main.blg" >nul 2>&1
    if exist "main.fdb_latexmk" del "main.fdb_latexmk" >nul 2>&1
    if exist "main.fls" del "main.fls" >nul 2>&1
    if exist "main.synctex.gz" del "main.synctex.gz" >nul 2>&1
    
    echo ✅ Cleanup completed
    echo.
    echo ════════════════════════════════════════════════════════════════
    echo                    🎉 COMPILATION COMPLETE!
    echo ════════════════════════════════════════════════════════════════
    echo.
    echo 📄 Generated file: main.pdf
    echo 📍 Location: %CD%\main.pdf
    echo.
    echo 🚀 Opening PDF file...
    start "" "main.pdf"
    
) else (
    echo ❌ PDF compilation failed!
    echo.
    echo 🔍 Checking for error details in log file...
    if exist "main.log" (
        echo.
        echo 📋 Recent errors found:
        echo ────────────────────────────────────────
        findstr /C:"!" main.log 2>nul | findstr /V /C:"extractbb"
        echo ────────────────────────────────────────
    )
    
    echo.
    echo 💡 Troubleshooting tips:
    echo 1. Check if all LaTeX packages are installed
    echo 2. Run setup.bat again if needed  
    echo 3. Check main.tex for syntax errors
    echo 4. Make sure all referenced files exist
)

echo.
echo Press any key to exit...
pause >nul 