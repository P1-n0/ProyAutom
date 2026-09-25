@echo off
title Auto-Registro de Inventario TI
color 0B

cls
echo ===============================================================
echo          ESCANEO Y AUTO-REGISTRO DE HARDWARE
echo ===============================================================
echo.
echo [PASO 1] CONFIGURACION DE RED
echo.
set /p IP_SERVIDOR="IP del Servidor (Ej. 192.168.1.50): "
set PUERTO=5000

echo.
echo [PASO 2] ASIGNACION DE USUARIO
echo.
echo Ingresa el ID del usuario responsable.
echo (Si el equipo estara en bodega sin asignar, teclea 0)
set /p id_usuario="ID de Usuario: "

echo.
echo [PASO 3] PERIFERICOS Y LICENCIA
echo (Si el equipo no tiene alguno, presiona ENTER para omitirlo)
echo.
:: Limpiamos las variables por seguridad antes de preguntar
set id_licencia=
set marca_monitor=
set pulgadas_monitor=
set marca_teclado=
set marca_mouse=

set /p id_licencia="ID de la Licencia (Ej. 1 para OEM, 2 para LTSC): "
set /p marca_monitor="Marca del Monitor: "
set /p pulgadas_monitor="Pulgadas del Monitor (Ej. 24): "
set /p marca_teclado="Marca del Teclado: "
set /p marca_mouse="Marca del Mouse: "

echo.
echo Escaneando componentes fisicos...

set PS_SCRIPT=%temp%\recolector.ps1

:: Extraemos el hardware base
echo $serial = (Get-CimInstance Win32_BIOS).SerialNumber > "%PS_SCRIPT%"
echo $marca = (Get-CimInstance Win32_ComputerSystem).Manufacturer >> "%PS_SCRIPT%"
echo $cpu = (Get-CimInstance Win32_Processor ^| Select-Object -First 1).Name >> "%PS_SCRIPT%"
echo $ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB) >> "%PS_SCRIPT%"
echo $disco = [math]::Round((Get-CimInstance Win32_DiskDrive ^| Select-Object -First 1).Size / 1GB) >> "%PS_SCRIPT%"
echo $os = (Get-CimInstance Win32_OperatingSystem).Caption >> "%PS_SCRIPT%"

echo Write-Host "Generando paquete de datos..." >> "%PS_SCRIPT%"

:: Ensamblamos todos los datos (Escaneados + Tecleados manualmente)
echo $url = "http://%IP_SERVIDOR%:%PUERTO%/api/equipo" >> "%PS_SCRIPT%"
echo $body = @{ >> "%PS_SCRIPT%"
echo     sn_equipo = $serial >> "%PS_SCRIPT%"
echo     marca_equipo = $marca >> "%PS_SCRIPT%"
echo     procesador = $cpu >> "%PS_SCRIPT%"
echo     ram = $ram >> "%PS_SCRIPT%"
echo     almacenamiento = $disco >> "%PS_SCRIPT%"
echo     so_equipo = $os >> "%PS_SCRIPT%"
echo     id_licencia = "%id_licencia%" >> "%PS_SCRIPT%"
echo     marca_monitor = "%marca_monitor%" >> "%PS_SCRIPT%"
echo     pulgadas_monitor = "%pulgadas_monitor%" >> "%PS_SCRIPT%"
echo     marca_teclado = "%marca_teclado%" >> "%PS_SCRIPT%"
echo     marca_mouse = "%marca_mouse%" >> "%PS_SCRIPT%"
echo } >> "%PS_SCRIPT%"

:: Condicional: Solo anexa el id_usuario si NO es 0 y NO esta vacio
echo if ("%id_usuario%" -ne "0" -and "%id_usuario%" -ne "") { >> "%PS_SCRIPT%"
echo     $body.Add('id_usuario', '%id_usuario%') >> "%PS_SCRIPT%"
echo } >> "%PS_SCRIPT%"

echo Write-Host "Enviando datos a %IP_SERVIDOR%:%PUERTO%..." >> "%PS_SCRIPT%"

echo try { >> "%PS_SCRIPT%"
echo     $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -ErrorAction Stop >> "%PS_SCRIPT%"
echo     Write-Host ">>> EXITO: El equipo $serial fue registrado correctamente." -ForegroundColor Green >> "%PS_SCRIPT%"
echo } catch { >> "%PS_SCRIPT%"
echo     Write-Host ">>> ERROR: No se pudo conectar al servidor. Revisa que la IP sea correcta y el servidor este encendido." -ForegroundColor Red >> "%PS_SCRIPT%"
echo } >> "%PS_SCRIPT%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
del "%PS_SCRIPT%"

echo.
echo ===============================================================
echo Proceso finalizado. 
echo ===============================================================
pause
exit