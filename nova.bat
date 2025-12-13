@echo off

:: This script compiles and runs a .nova file.
:: It assumes that Python and a C++ compiler (like clang++ or g++)
:: are already available in your system's PATH.

:: Get the directory where this batch file is located.
set "SCRIPT_DIR=%~dp0"

:: Run the compiler using a relative path.
python "%SCRIPT_DIR%compiler.py" %1 --run
