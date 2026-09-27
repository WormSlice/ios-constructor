@echo off
chcp 65001 >nul
cls
echo ==============================================================================
echo       INCREMENTAR VERSION Y DISPARAR BUILD EN CODEMAGIC (TESTFLIGHT)
echo ==============================================================================
echo.
echo Este script actualiza el build number en pubspec.yaml, hace commit y push
echo a GitHub en la rama 'main' para activar el flujo automatico en Codemagic.
echo.

set "SCRIPT_DIR=%~dp0"
set "TOOLS_DIR=%SCRIPT_DIR%.."
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."

set "PUBSPEC_PATH=%PROJECT_ROOT%\pubspec.yaml"
if not exist "%PUBSPEC_PATH%" (
    if exist "%TOOLS_DIR%\pubspec.yaml" set "PUBSPEC_PATH=%TOOLS_DIR%\pubspec.yaml"
    if exist "pubspec.yaml" set "PUBSPEC_PATH=pubspec.yaml"
)

if not exist "%PUBSPEC_PATH%" (
    echo [ERROR] No se encontro pubspec.yaml
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "& {" ^
    "$path = '%PUBSPEC_PATH%';" ^
    "$content = Get-Content -Raw -Encoding UTF8 $path;" ^
    "if ($content -match 'version:\s*([0-9\.]+)\+([0-9]+)') {" ^
    "    $verName = $matches[1];" ^
    "    $currBuild = [int]$matches[2];" ^
    "    $nextBuild = $currBuild + 1;" ^
    "    Write-Host 'Version actual detectada: ' -NoNewline; Write-Host \"$verName+$currBuild\" -ForegroundColor Yellow;" ^
    "    Write-Host 'Nueva version a asignar:  ' -NoNewline; Write-Host \"$verName+$nextBuild\" -ForegroundColor Green;" ^
    "    $newContent = $content -replace 'version:\s*[0-9\.]+\+[0-9]+', \"version: $verName+$nextBuild\";" ^
    "    [System.IO.File]::WriteAllText($path, $newContent, [System.Text.Encoding]::UTF8);" ^
    "    Write-Host '[OK] pubspec.yaml actualizado correctamente.' -ForegroundColor Cyan;" ^
    "    Set-Content -Path (Join-Path '%SCRIPT_DIR%' 'temp_build_info.txt') -Value \"$verName+$nextBuild\";" ^
    "} else {" ^
    "    Write-Host '[ERROR] No se encontro patron version: X.Y.Z+N en pubspec.yaml' -ForegroundColor Red;" ^
    "    exit 1;" ^
    "}" ^
"}"

if %errorlevel% neq 0 (
    echo Ocurrio un problema al leer o modificar pubspec.yaml.
    pause
    exit /b 1
)

set /p NEW_VER=<"%SCRIPT_DIR%temp_build_info.txt"
del "%SCRIPT_DIR%temp_build_info.txt" 2>nul

echo.
set /p COMMIT_MSG="Mensaje para el commit [chore(release): bump build to %NEW_VER%]: "
if "%COMMIT_MSG%"=="" set "COMMIT_MSG=chore(release): bump build to %NEW_VER%"

echo.
echo Entrando a la raiz del repositorio (%PROJECT_ROOT%)...
cd /d "%PROJECT_ROOT%"

echo.
echo Guardando cambios y enviando a GitHub (origin main)...
git add pubspec.yaml codemagic.yaml
git commit -m "%COMMIT_MSG%"
git push origin main

echo.
echo ==============================================================================
echo               ?CAMBIOS ENVIADOS A GITHUB SATISFACTORIAMENTE!
echo ==============================================================================
echo.
echo Ahora Codemagic detectara el push en la rama 'main' y comenzara la compilacion.
echo Puedes ver el progreso en vivo en:
echo   ?? https://codemagic.io/apps
echo.
echo El script de Codemagic:
echo   1. Limpiara la cache de CocoaPods
echo   2. Verificara contra TestFlight que el build sea superior
echo   3. Firmara con los perfiles oficiales de Apple
echo   4. Subira el .ipa directamente a TestFlight
echo.
pause
