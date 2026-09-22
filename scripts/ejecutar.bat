@echo off
REM ============================================================
REM  Ejecuta el programa del reporte de matricula (interfaz grafica)
REM  No requiere .exe: usa el Python instalado, que si esta permitido.
REM ============================================================
setlocal
cd /d "%~dp0\.."
python main.py
if errorlevel 1 (
    echo.
    echo Hubo un problema al ejecutar. Verifica que Python este instalado
    echo y que ejecutaste "pip install -r requirements.txt".
    pause
)
endlocal
