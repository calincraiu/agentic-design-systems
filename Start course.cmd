@echo off
rem Starts the course app. Double-click this file. Close the window to stop the app.
cd /d "%~dp0"
if exist "%USERPROFILE%\.local\bin\uv.exe" set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where uv >nul 2>nul
if errorlevel 1 (
  echo Installing uv, the program that runs Python for the course. This happens once.
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)
echo Starting the course app. The first time takes a minute.
uv run course
pause
