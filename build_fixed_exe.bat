@echo off
setlocal
cd /d "%~dp0"

echo [1/4] Checking Python...
python -V >nul 2>&1
if errorlevel 1 (
  py -V >nul 2>&1
  if errorlevel 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b 1
  )
  set "PY_CMD=py"
) else (
  set "PY_CMD=python"
)

echo [2/4] Installing/Updating required packages...
%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install -r automation\requirements_automation.txt pyinstaller
if errorlevel 1 (
  echo Dependency installation failed.
  pause
  exit /b 1
)

echo [3/4] Building FIXED Automation EXE...
%PY_CMD% -m PyInstaller --noconfirm --clean EgyptAutomationAPI_Fixed.spec

if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)

echo [4/4] Done.
echo EXE location: dist\EgyptAutomationAPI_Fixed\EgyptAutomationAPI_Fixed.exe
pause
