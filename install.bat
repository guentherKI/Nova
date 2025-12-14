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
echo Press any key to continue, or close this window to cancel.
pause > nul
echo.

:: Use a more robust PowerShell command to add the path only if it doesn't already exist.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$novaDir = '%NOVA_DIR%';" ^
    "$userPath = [Environment]::GetEnvironmentVariable('Path', 'User');" ^
    "$pathItems = $userPath.Split(';') | Where-Object { $_.Trim() -ne '' };" ^
    "if ($pathItems -notcontains $novaDir) {" ^
    "    $newPath = ($pathItems + $novaDir) -join ';';" ^
    "    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User');" ^
    "    Write-Host 'SUCCESS: Nova compiler added to your PATH.'" ^
    "} else {" ^
    "    Write-Host 'INFO: Nova compiler is already in your PATH.'" ^
    "}"

echo.
echo ====================================================================
echo  Installation complete.
echo  You must CLOSE and REOPEN any open terminal windows for the
echo  changes to take effect.
echo ====================================================================
echo.
pause