@echo off
chcp 65001 >nul
cls
echo ==============================================================================
echo       VERIFICACION PRE-VUELO: ENTORNO DE COMPILACION IOS EN WINDOWS
echo ==============================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "TOOLS_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."

set OPENSSL_BIN=
if exist "C:\Program Files\Git\usr\bin\openssl.exe" (
    set "OPENSSL_BIN=C:\Program Files\Git\usr\bin\openssl.exe"
) else (
    where openssl >nul 2>nul
    if %errorlevel% equ 0 set "OPENSSL_BIN=openssl"
)

echo [1/6] Verificando Git...
where git >nul 2>nul
if %errorlevel% equ 0 (
    echo     [OK] Git instalado:
    git --version
) else (
    echo     [ERROR] Git no esta instalado en PATH. Descargalo de https://git-scm.com/
)
echo.

echo [2/6] Verificando OpenSSL (para certificados Apple en Windows)...
if defined OPENSSL_BIN (
    echo     [OK] OpenSSL detectado en: %OPENSSL_BIN%
    "%OPENSSL_BIN%" version
) else (
    echo     [ADVERTENCIA] OpenSSL no detectado directamente. Si tienes Git for Windows,
    echo     suele estar en C:\Program Files\Git\usr\bin\openssl.exe
)
echo.

echo [3/6] Verificando Flutter SDK...
where flutter >nul 2>nul
if %errorlevel% equ 0 (
    echo     [OK] Flutter detectado:
    flutter --version | findstr /i "Flutter ?"
) else (
    echo     [ERROR] Flutter SDK no esta en el PATH del sistema.
)
echo.

echo [4/6] Verificando version y build en pubspec.yaml...
if exist "%PROJECT_ROOT%\pubspec.yaml" (
    findstr /r "^version:" "%PROJECT_ROOT%\pubspec.yaml"
) else if exist "%TOOLS_DIR%\pubspec.yaml" (
    findstr /r "^version:" "%TOOLS_DIR%\pubspec.yaml"
) else (
    echo     [ADVERTENCIA] No se encontro pubspec.yaml en la ruta esperada.
)
echo.

echo [5/6] Verificando configuracion de Codemagic (codemagic.yaml)...
if exist "%PROJECT_ROOT%\codemagic.yaml" (
    echo     [OK] codemagic.yaml detectado en la raiz del proyecto.
) else if exist "%TOOLS_DIR%\codemagic.yaml" (
    echo     [OK] codemagic.yaml detectado.
) else (
    echo     [ALERTA] codemagic.yaml no encontrado. Usa la plantilla en tools_ios_windows\codemagic.yaml.template
)
echo.

echo [6/6] Verificando IOSbuilder CLI (builder.exe)...
if exist "%TOOLS_DIR%\builder.exe" (
    echo     [OK] builder.exe detectado en: %TOOLS_DIR%\builder.exe
) else if exist "%PROJECT_ROOT%\builder-windows-amd64.exe" (
    echo     [OK] builder-windows-amd64.exe detectado en la raiz.
) else (
    echo     [ADVERTENCIA] builder.exe no encontrado en tools_ios_windows.
)
echo.

echo ==============================================================================
echo                      ESTADO DEL SISTEMA COMPROBADO
echo ==============================================================================
echo.
pause
