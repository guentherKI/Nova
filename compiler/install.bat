@echo off
setlocal enabledelayedexpansion

:: This script installs the Nova compiler to a standard user directory and adds it to the PATH.

echo.
echo  ================================
echo      Nova Language Installer
echo  ================================
echo.

:: Define the installation directory in the user's local app data.
set "INSTALL_DIR=%LOCALAPPDATA%\Nova\bin"

:: Get the directory where this script is located (the source).
set "SOURCE_DIR=%~dp0"

echo Installing Nova compiler to:
echo   %INSTALL_DIR%
echo.
echo Press any key to continue, or close this window to cancel.
pause > nul
echo.

:: Create the installation directory if it doesn't exist.
if not exist "%INSTALL_DIR%" (
    echo Creating directory: %INSTALL_DIR%
    mkdir "%INSTALL_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create installation directory. Please check permissions.
        pause
        exit /b 1
    )
)

echo Copying compiler files...
copy /Y "%SOURCE_DIR%compiler.py" "%INSTALL_DIR%"
copy /Y "%SOURCE_DIR%nova.bat" "%INSTALL_DIR%"
echo.

echo Configuring compiler path...
:: PowerShell command to replace the placeholder in the copied nova.bat
powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-Content '%INSTALL_DIR%\nova.bat') -replace '__INSTALL_DIR__', '%INSTALL_DIR%\\' | Set-Content '%INSTALL_DIR%\nova.bat'"
if errorlevel 1 (
    echo ERROR: Failed to configure the compiler path in nova.bat.
    pause
    exit /b 1
)
echo Configuration successful.

:: Use PowerShell to add the new, stable path to the user's PATH variable if it's not already there.
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $installDir = '%INSTALL_DIR%'; $userPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if (-not ($userPath -split ';').Contains($installDir)) { $newPath = ($userPath, $installDir) -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Set-ItemProperty -Path 'Registry::HKCU\Environment' -Name 'Path' -Value $newPath; Write-Host 'SUCCESS: Nova compiler has been installed and added to your PATH.'; } else { Write-Host 'INFO: Nova compiler is already in your PATH.'; } } catch { Write-Error $_; exit 1 }"

echo.
echo ====================================================================
echo  Installation complete! You can now safely delete the installer folder.
echo  You must CLOSE and REOPEN any open terminal windows for the 'nova'
echo  command to become available.
echo ====================================================================
echo.
pause