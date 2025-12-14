@echo off
setlocal enabledelayedexpansion

:: This script transpiles, compiles, and runs a Nova file,
:: then cleans up all intermediate files.

:: --- Argument Parsing ---
set "INPUT_FILE="
set "KEEP_CPP=0"

:parse_args
if "%~1"=="" goto :args_done
if /i "%~1"=="--cpp" (
    set "KEEP_CPP=1"
) else (
    if not defined INPUT_FILE (
        set "INPUT_FILE=%~f1"
    )
)
shift
goto :parse_args
:args_done

if not defined INPUT_FILE (
    echo Usage: nova [filename.nova] [--cpp]
    exit /b 1
)

:: --- Configuration ---
:: Get just the name of the file without extension
for %%F in ("!INPUT_FILE!") do set "BASENAME=%%~nF"
:: Get the directory where this script is located
set "COMPILER_DIR=__INSTALL_DIR__"

:: --- File Paths ---
:: Use a unique name for temp files to avoid collisions
set "UNIQUE_ID=%RANDOM%%RANDOM%"
set "EXE_FILE=!BASENAME!.exe"

:: Decide where to put the C++ file
if !KEEP_CPP! == 1 (
    set "CPP_FILE=!BASENAME!.cpp"
) else (
    set "CPP_FILE=%TEMP%\!BASENAME!_%UNIQUE_ID%.cpp"
)

:: 1. Transpile Nova to a C++ file
python "%COMPILER_DIR%compiler.py" "!INPUT_FILE!" > "!CPP_FILE!"
if %errorlevel% neq 0 goto cleanup

if !KEEP_CPP! == 1 (
    echo Successfully transpiled to !CPP_FILE!
)

:: 2. Compile the C++ file to a temporary executable
g++ -std=c++17 -O2 "!CPP_FILE!" -o "!EXE_FILE!"

:: Check if compilation was successful
if %errorlevel% neq 0 (
    echo.
    echo ERROR: C++ compilation failed.
    goto cleanup
)

echo Successfully compiled to !EXE_FILE!

:: 3. Run the compiled program
echo.
echo --- Running !BASENAME!.nova ---
!EXE_FILE!

:cleanup
:: 4. Clean up all intermediate files
if !KEEP_CPP! == 0 (
    del "!CPP_FILE!" >nul 2>nul
)

endlocal
