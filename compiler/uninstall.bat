@echo off
setlocal enabledelayedexpansion

:: This script removes the Nova compiler from the user's PATH and deletes the files.

echo.
echo  ==================================
echo      Nova Language Uninstaller
echo  ==================================
echo.

:: Define the installation directory.
set "INSTALL_DIR=%LOCALAPPDATA%\Nova\bin"
set "BASE_INSTALL_DIR=%LOCALAPPDATA%\Nova"

echo This will remove the Nova compiler from your user PATH.
echo The installation directory is:
echo   %INSTALL_DIR%
echo.

:: Use PowerShell to safely remove the directory from the PATH.
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $installDir = '%INSTALL_DIR%'; $userPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $newPath = ($userPath -split ';') -ne $installDir -join ';'; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Set-ItemProperty -Path 'Registry::HKCU\Environment' -Name 'Path' -Value $newPath; Write-Host 'Nova compiler has been removed from your PATH.'; } catch { Write-Error $_; exit 1 }"

echo.
set /p "delete_files=Do you want to delete the compiler files from %BASE_INSTALL_DIR%? (Y/N) "
if /i "!delete_files!"=="Y" (
    if exist "%BASE_INSTALL_DIR%" (
        echo Deleting compiler files...
        rmdir /s /q "%BASE_INSTALL_DIR%"
        echo Files deleted.
    )
)

echo.
echo ====================================================================
echo  Uninstallation complete.
echo.
echo  You must CLOSE and REOPEN any open terminal windows for the
echo  changes to fully take effect.
echo ====================================================================
echo.
pause