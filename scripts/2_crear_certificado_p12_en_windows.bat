@echo off
chcp 65001 >nul
cls
echo ==============================================================================
echo      GENERADOR DE CERTIFICADOS IOS (.p12) DIRECTO EN WINDOWS CON OPENSSL
echo ==============================================================================
echo.
echo Este asistente te permite crear los certificados oficiales de Apple (.p12)
echo necesarios para firmar apps iOS sin necesidad de una computadora Mac.
echo.

set OPENSSL_BIN=
if exist "C:\Program Files\Git\usr\bin\openssl.exe" (
    set "OPENSSL_BIN=C:\Program Files\Git\usr\bin\openssl.exe"
) else (
    where openssl >nul 2>nul
    if %errorlevel% equ 0 set "OPENSSL_BIN=openssl"
)

if not defined OPENSSL_BIN (
    echo [ERROR] No se encontro OpenSSL. Por favor instala Git for Windows
    echo o agrega openssl.exe a tu variable PATH.
    pause
    exit /b 1
)

echo OpenSSL detectado: "%OPENSSL_BIN%"
echo.
echo Selecciona la accion que deseas realizar:
echo   [1] PASO A: Generar Clave Privada (.key) y Peticion CSR (.csr) para Apple Developer
echo   [2] PASO B: Convertir certificado descargado (distribution.cer) a .p12 con clave privada
echo   [3] Salir
echo.
set /p OPCION="Elige una opcion (1, 2 o 3): "

if "%OPCION%"=="1" goto PASO_A
if "%OPCION%"=="2" goto PASO_B
goto FIN

:PASO_A
echo.
echo ------------------------------------------------------------------------------
echo   PASO A: GENERAR CLAVE PRIVADA Y CSR
echo ------------------------------------------------------------------------------
set /p EMAIL="Ingresa tu correo de Apple Developer (ej: dev@miempresa.com): "
set /p NOMBRE="Ingresa tu nombre o empresa (ej: Soporte CONNECT): "
set /p PAIS="Codigo de 2 letras de tu pais (ej: CO, MX, ES, US): "

if "%PAIS%"=="" set PAIS=CO

echo.
echo Generando clave privada de 2048 bits (mi_llave_privada.key)...
"%OPENSSL_BIN%" genrsa -out mi_llave_privada.key 2048

echo Generando Certificate Signing Request (peticion.csr)...
"%OPENSSL_BIN%" req -new -key mi_llave_privada.key -out peticion.csr -subj "/emailAddress=%EMAIL%, CN=%NOMBRE%, C=%PAIS%"

echo.
echo ==============================================================================
echo                       ARCHIVOS CREADOS CON EXITO:
echo   - mi_llave_privada.key  (?NUNCA COMPARTAS ESTE ARCHIVO!)
echo   - peticion.csr          (Este es el archivo que subiras a Apple)
echo ==============================================================================
echo.
echo SIGUIENTE PASO:
echo 1. Entra a https://developer.apple.com/account/resources/certificates/list
echo 2. Haz click en el boton '+' para agregar certificado.
echo 3. Selecciona 'Apple Distribution' (o 'iOS Distribution').
echo 4. Sube el archivo 'peticion.csr'.
echo 5. Descarga el certificado generado por Apple, renombralo a 'distribution.cer'
echo    y guardalo en esta misma carpeta.
echo 6. Vuelve a ejecutar este script y elige la OPCION 2.
echo.
pause
goto FIN

:PASO_B
echo.
echo ------------------------------------------------------------------------------
echo   PASO B: FUSIONAR CERTIFICADO APPLE (.cer) Y CLAVE PRIVADA (.key) A .p12
echo ------------------------------------------------------------------------------
if not exist "distribution.cer" (
    echo [ERROR] No se encontro el archivo 'distribution.cer' en esta carpeta.
    echo Asegurate de haber descargado el certificado desde Apple Developer
    echo y colocarlo aqui con el nombre exacto 'distribution.cer'.
    pause
    goto FIN
)

if not exist "mi_llave_privada.key" (
    echo [ERROR] No se encontro 'mi_llave_privada.key'.
    echo Debes usar la misma clave privada generada en el PASO 1.
    pause
    goto FIN
)

set /p P12_PASS="Ingresa una contrasena para proteger tu archivo .p12 (anotala bien): "

echo.
echo [1/2] Convirtiendo distribution.cer a formato PEM...
"%OPENSSL_BIN%" x509 -in distribution.cer -inform DER -out certificado.pem -outform PEM

echo [2/2] Exportando a archivo PKCS#12 (CONNECT.p12)...
"%OPENSSL_BIN%" pkcs12 -export -inkey mi_llave_privada.key -in certificado.pem -out CONNECT.p12 -passout pass:%P12_PASS% -legacy

echo.
if exist "CONNECT.p12" (
    echo ==============================================================================
    echo              ?FELICIDADES! TU CERTIFICADO .p12 HA SIDO GENERADO
    echo ==============================================================================
    echo Archivo generado: CONNECT.p12
    echo Contrasena:       %P12_PASS%
    echo.
    echo Ahora puedes usar este archivo .p12 para configurar IOSbuilder o Codemagic.
) else (
    echo [ERROR] Ocurrio un fallo al generar CONNECT.p12. Revisa los mensajes arriba.
)
echo.
pause

:FIN
