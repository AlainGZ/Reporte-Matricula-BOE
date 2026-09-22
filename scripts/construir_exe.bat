@echo off
REM ============================================================
REM  Construye el ejecutable .exe con PyInstaller.
REM  IMPORTANTE: usar solo cuando el area de sistemas autorice
REM  ejecutar el .exe en los equipos de la organizacion.
REM ============================================================
setlocal
cd /d "%~dp0\.."

echo Instalando dependencias de desarrollo...
python -m pip install -r requirements-dev.txt

echo.
echo Construyendo el ejecutable...
pyinstaller --noconfirm --onefile --windowed ^
    --name ReporteMatricula ^
    --paths src ^
    main.py

echo.
echo Listo. El ejecutable esta en la carpeta dist\ReporteMatricula.exe
pause
endlocal
