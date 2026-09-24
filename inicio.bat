@echo off
title Gestor del Servidor - TechCorp IT
color 0F

:: ==========================================
:: VALIDACION DE REQUISITOS (Python y PIP)
:: ==========================================
:check_reqs
python --version >nul 2>&1
if %errorlevel% neq 0 (
    goto no_python
)

python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    goto no_pip
)

:: Si ambos existen, va al menu principal
goto menu

:: ==========================================
:: INSTRUCCIONES DE ERROR
:: ==========================================
:no_python
cls
echo ===============================================================
echo ERROR CRITICO: Python no esta instalado o no esta en el PATH.
echo ===============================================================
echo.
echo Para solucionar esto:
echo 1. Ve a https://www.python.org/downloads/
echo 2. Descarga la ultima version para Windows.
echo 3. Abre el instalador y MARCA LA CASILLA que dice:
echo    "Add Python to PATH" (Esto es obligatorio).
echo 4. Haz clic en "Install Now".
echo 5. Cierra esta ventana y vuelve a ejecutar este script.
echo.
pause
exit

:no_pip
cls
echo ===============================================================
echo ERROR CRITICO: PIP (Gestor de paquetes) no fue encontrado.
echo ===============================================================
echo.
echo Tu instalacion de Python parece estar corrupta o incompleta.
echo Por favor, reinstala Python asegurandote de incluir PIP.
echo.
pause
exit

:: ==========================================
:: MENU PRINCIPAL
:: ==========================================
:menu
cls
echo ===============================================================
echo               PANEL DE CONTROL DEL SERVIDOR
echo ===============================================================
echo.
echo  1) Instalar (Crear entorno virtual e instalar requerimientos)
echo  2) Iniciar Servidor (Levantar entorno y ejecutar app.py)
echo  3) Salir
echo.
echo ===============================================================
set /p opcion="Elige una opcion (1, 2 o 3): "

if "%opcion%"=="1" goto instalar
if "%opcion%"=="2" goto iniciar
if "%opcion%"=="3" goto salir

:: Si escriben algo invalido, vuelve a cargar el menu
goto menu

:: ==========================================
:: OPCION 1: INSTALACION
:: ==========================================
:instalar
cls
echo ===============================================================
echo                INSTALANDO ENTORNO Y PAQUETES
echo ===============================================================
echo.

echo [1/4] Creando el entorno virtual (carpeta 'env')...
python -m venv env

echo [2/4] Activando el entorno virtual...
call env\Scripts\activate.bat

echo [3/4] Actualizando PIP a su ultima version...
python -m pip install --upgrade pip >nul

echo [4/4] Instalando dependencias necesarias...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo NOTA: No se encontro requirements.txt. Instalando Flask base...
    pip install Flask
)

echo.
echo ===============================================================
echo Instalacion finalizada correctamente.
echo ===============================================================
pause
goto menu

:: ==========================================
:: OPCION 2: INICIO DEL SERVIDOR
:: ==========================================
:iniciar
cls
echo ===============================================================
echo                 INICIANDO SERVIDOR WEB
echo ===============================================================
echo.

:: Verificar que el entorno virtual exista antes de intentar iniciarlo
if not exist env\Scripts\activate.bat (
    echo ERROR: El entorno virtual no existe.
    echo Por favor, ejecuta la Opcion 1 ^(Instalar^) primero.
    echo.
    pause
    goto menu
)

echo Activando entorno aislado...
call env\Scripts\activate.bat

echo Arrancando aplicacion...
echo (Presiona CTRL+C en cualquier momento para apagar el servidor)
echo.
echo ---------------------------------------------------------------
python app.py
echo ---------------------------------------------------------------
echo.
echo El servidor se ha detenido.
pause
goto menu

:: ==========================================
:: OPCION 3: SALIR
:: ==========================================
:salir
exit