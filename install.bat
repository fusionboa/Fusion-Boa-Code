@echo off
setlocal enabledelayedexpansion

echo.
echo   ========================================
echo     FusionBoa Language - One-Click Install
echo   ========================================
echo.

:: Get the directory where this script lives
set "FUSIONBOA_HOME=%~dp0"
set "FUSIONBOA_HOME=%FUSIONBOA_HOME:~0,-1%"

echo   Installing from: %FUSIONBOA_HOME%
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Python not found! Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo   [+] Python found:
python --version 2>&1

:: Delegate to the Python installer which handles pip install + PATH setup
:: (pip install is done first so dependencies are resolved)
echo.
echo   [*] Running installer...
python "%FUSIONBOA_HOME%\install.py"
if %errorlevel% neq 0 (
    echo.
    echo   [X] Installation failed. See errors above.
    pause
    exit /b 1
)

:: Refresh current session PATH so fusionboa works immediately
set "PATH=%PATH%;%FUSIONBOA_HOME%"

echo.
echo   ========================================
echo     FusionBoa is ready!
echo   ========================================
echo.
echo   Commands:
echo.
echo     fusionboa run    file.fusboa     Run a FusionBoa file
echo     fusionboa build  file.fusboa     Compile to 23 targets
echo     fusionboa init   my_project      Create a new project
echo     fusionboa help                   Show all commands
echo     fusionboa targets                List 23 compile targets
echo.
echo   [!] Restart your terminal for PATH changes to take effect everywhere.
echo       (This session: try 'fusionboa version')
echo.
echo   ========================================
pause
