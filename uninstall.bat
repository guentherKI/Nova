@echo off
setlocal

:: This script removes the Nova compiler directory from the user's PATH.

echo.
echo  ==================================
echo      Nova Language Uninstaller
echo  ==================================
echo.

:: Get the directory where this script is located.
set "NOVA_DIR=%~dp0"
if "%NOVA_DIR:~-1%"=="\" set "NOVA_DIR=%NOVA_DIR:~0,-1%"

echo This will remove the following directory from your user PATH:
echo   %NOVA_DIR%
echo.

:: Use PowerShell to safely read, filter, and set the new path.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$userPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $newPath = ($userPath.Split(';') | Where-Object { $_ -ne '%NOVA_DIR%' }) -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')"

echo.
echo ====================================================================
echo  SUCCESS! The Nova compiler has been removed from your user PATH.
echo.
echo  IMPORTANT: You must CLOSE and REOPEN any terminal windows
echo  for the change to take effect.
echo ====================================================================
echo.
pause