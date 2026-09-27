@echo off
chcp 65001 >nul
cls
echo ==============================================================================
echo        COMPILAR APLICACION IOS CON IOSBUILDER (GITHUB ACTIONS)
echo ==============================================================================
echo.
echo Este script dispara la compilacion en los servidores macOS de GitHub Actions
echo y descarga automaticamente el archivo .ipa resultante a la carpeta 'dist'.
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

echo Selecciona el modo de compilacion:
echo   [1] Compilacion FIRMADA (Release con certificado .p12 configurado en GitHub Secrets)
echo   [2] Compilacion SIN FIRMAR (Unsigned IPA, ideal para Sideloadly, AltStore, Scarlet)
echo   [3] Cancelar
echo.
set /p MODO="Elige una opcion (1 o 2): "

cd /d "%PROJECT_ROOT%"

if "%MODO%"=="1" (
    echo.
    echo Iniciando compilacion firmada en GitHub Actions...
    echo Monitoreando progreso en tiempo real...
    "%BUILDER_EXE%" ios build -o "%PROJECT_ROOT%\dist"
) else if "%MODO%"=="2" (
    echo.
    echo Iniciando compilacion SIN FIRMA (--unsigned) en GitHub Actions...
    "%BUILDER_EXE%" ios build --unsigned -o "%PROJECT_ROOT%\dist"
) else (
    echo Operacion cancelada.
    goto FIN
)

echo.
echo ==============================================================================
echo Compilacion terminada. Verifica la carpeta:
echo %PROJECT_ROOT%\dist
echo ==============================================================================
echo.
pause

:FIN
