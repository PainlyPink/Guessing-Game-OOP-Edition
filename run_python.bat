@echo off
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found. Please ensure the venv folder is in the current directory.
    goto end
)

python %1

:end
pause