@echo off
setlocal

:: This script adds the Nova compiler directory to the user's PATH.

echo.
echo  ================================
echo      Nova Language Installer
echo  ================================
echo.

:: Get the directory where this script is located.
set "NOVA_DIR=%~dp0"
:: Remove the trailing backslash for a clean path.
if "%NOVA_DIR:~-1%"=="\" set "NOVA_DIR=%NOVA_DIR:~0,-1%"

echo This will add the following directory to your user PATH:
echo   %NOVA_DIR%
echo.

:: Use a PowerShell command to safely add the path, avoiding duplicates.
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%NOVA_DIR%', 'User')"

echo.
echo ====================================================================
echo  SUCCESS! The Nova compiler has been added to your user PATH.
echo.
echo  IMPORTANT: You must CLOSE and REOPEN any terminal windows
echo  for the change to take effect.
echo ====================================================================
echo.
pause