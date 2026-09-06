@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 tools\setup_project.py
) else (
    python tools\setup_project.py
)
echo.
echo Anleitung: README.md. Dieser Check aendert keine WordPress-Dateien.
pause
