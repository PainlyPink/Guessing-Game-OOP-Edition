@echo off

REM Activate virtual environment if available
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found.
)

REM Prompt for Python script path or use argument
set "file=%~1"
if not defined file (
    set /p "file=Enter Python script path/file: "
) else (
    if not exist "%file%" (
        echo File "%file%" not found. Exiting...
        goto end
    )
)

python "%file%"

:end
pause

