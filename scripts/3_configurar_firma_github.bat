@echo off
chcp 65001 >nul
cls
echo ==============================================================================
echo       CONFIGURAR FIRMA AUTOMATICA EN GITHUB ACTIONS CON IOSBUILDER
echo ==============================================================================
echo.
echo Este script subira tu certificado .p12 y tu perfil .mobileprovision
echo cifrados como secretos en tu repositorio de GitHub para que las compilaciones
echo remotas en macOS firmen el IPA automaticamente.
echo.

set "SCRIPT_DIR=%~dp0"
set "TOOLS_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."

set "BUILDER_EXE=%TOOLS_DIR%\builder.exe"
if not exist "%BUILDER_EXE%" (
    if exist "%PROJECT_ROOT%\builder-windows-amd64.exe" (
        set "BUILDER_EXE=%PROJECT_ROOT%\builder-windows-amd64.exe"
    ) else (
        echo [ERROR] No se encontro builder.exe en %TOOLS_DIR%.
        pause
        exit /b 1
    )
)

echo Buscando archivos por defecto en el proyecto...
set DEFAULT_P12=
set DEFAULT_PROV=

if exist "%PROJECT_ROOT%\CONNECT.p12" set "DEFAULT_P12=%PROJECT_ROOT%\CONNECT.p12"
if exist "%TOOLS_DIR%\CONNECT.p12" set "DEFAULT_P12=%TOOLS_DIR%\CONNECT.p12"
if exist "CONNECT.p12" set "DEFAULT_P12=CONNECT.p12"

if exist "%PROJECT_ROOT%\CONNECT.mobileprovision" set "DEFAULT_PROV=%PROJECT_ROOT%\CONNECT.mobileprovision"
if exist "%TOOLS_DIR%\CONNECT.mobileprovision" set "DEFAULT_PROV=%TOOLS_DIR%\CONNECT.mobileprovision"
if exist "CONNECT.mobileprovision" set "DEFAULT_PROV=CONNECT.mobileprovision"

echo.
if defined DEFAULT_P12 (
    echo Se detecto certificado: %DEFAULT_P12%
)
set /p P12_PATH="Ruta al archivo .p12 [%DEFAULT_P12%]: "
if "%P12_PATH%"=="" set "P12_PATH=%DEFAULT_P12%"

if not exist "%P12_PATH%" (
    echo [ERROR] No existe el archivo: %P12_PATH%
    pause
    exit /b 1
)

echo.
if defined DEFAULT_PROV (
    echo Se detecto perfil de aprovisionamiento: %DEFAULT_PROV%
)
set /p PROV_PATH="Ruta al archivo .mobileprovision [%DEFAULT_PROV%]: "
if "%PROV_PATH%"=="" set "PROV_PATH=%DEFAULT_PROV%"

if not exist "%PROV_PATH%" (
    echo [ERROR] No existe el archivo: %PROV_PATH%
    pause
    exit /b 1
)

echo.
echo ==============================================================================
echo Ejecutando configuracion de firma en GitHub...
echo (Se te pedira la contrasena de tu archivo .p12)
echo ==============================================================================
echo.

cd /d "%PROJECT_ROOT%"
"%BUILDER_EXE%" signing setup -c "%P12_PATH%" -p "%PROV_PATH%"

echo.
echo Proceso finalizado.
pause
