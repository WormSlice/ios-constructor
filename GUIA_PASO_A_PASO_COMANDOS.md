# 📱 GUÍA DEFINITIVA: COMPILAR APPS DE IOS EN WINDOWS (PASO A PASO)
### Métodos: CodeMagic (TestFlight / App Store) y IOSbuilder (GitHub Actions / IPA Directo)

---

## 🎯 1. ¿Cómo es posible compilar iOS sin tener una Mac física?

Apple exige que la compilación y firma final de aplicaciones para iOS ocurra dentro de un entorno **macOS** con las herramientas de Xcode. Tradicionalmente, los desarrolladores en Windows estaban obligados a comprar una Mac costosa.

Hoy en día, el estándar de la industria es utilizar **Integración Continua en la Nube (Cloud CI/CD)**:
1. Desarrollas, pruebas y programas cómodamente en tu PC con **Windows** (usando VS Code, Android Studio, Flutter, etc.).
2. Guardas tus cambios y los envías a **GitHub** (`git push origin main`).
3. Un servidor **macOS virtualizado en la nube** (ya sea en **Codemagic** con runners Mac mini M2, o en **GitHub Actions**) recibe tu código, instala las dependencias de CocoaPods, descarga los certificados de Apple automáticamente, compila el binario `.ipa` y lo publica a **TestFlight / App Store** o lo deja listo para descargar a tu computadora.

---

## 🧰 2. Requisitos Previos en tu Computadora Windows

| Herramienta | Para qué sirve | Dónde descargarla |
| :--- | :--- | :--- |
| **Git for Windows** | Control de versiones y provee **OpenSSL** nativo | [git-scm.com](https://git-scm.com/) |
| **Flutter SDK** | Framework de desarrollo de la app | [flutter.dev](https://docs.flutter.dev/get-started/install/windows) |
| **Cuenta Apple Developer** | Obligatoria para crear App IDs, certificados y subir a TestFlight ($99 USD/año) | [developer.apple.com](https://developer.apple.com/) |
| **Repositorio GitHub** | Aloja tu código y dispara los flujos remotos | [github.com](https://github.com/) |
| **Cuenta Codemagic** | Plataforma de CI/CD especializada en Flutter & iOS | [codemagic.io](https://codemagic.io/) |

> 💡 **Dato clave sobre OpenSSL:** Si instalaste Git for Windows, ya tienes OpenSSL en:  
> `C:\Program Files\Git\usr\bin\openssl.exe`. ¡No necesitas instalar nada raro!

---

## 🔑 3. Configuración de Credenciales de Apple desde Windows (Sin Mac)

Para que los servidores en la nube firmen tus apps, necesitas dos tipos de llaves de Apple:
1. **App Store Connect API Key (`.p8`)**: Permite que Codemagic descargue y cree perfiles automáticamente sin pedirte usuario y contraseña ni códigos 2FA.
2. **Certificado de Distribución (`.p12`) y Perfil (`.mobileprovision`)**: Usado para firmas locales o en GitHub Actions con IOSbuilder.

---

### Paso 3.1: Crear el App ID (Bundle Identifier)
1. Entra a: [developer.apple.com/account/resources/identifiers/list](https://developer.apple.com/account/resources/identifiers/list)
2. Haz clic en el botón azul **`+`** (Register a new identifier).
3. Selecciona **App IDs** -> Continue.
4. Tipo: **App** -> Continue.
5. **Description**: Nombre de tu app (ej: `CONNECT`).
6. **Bundle ID**: Selecciona **Explicit** y coloca tu identificador único (ej: `com.connectapp.co`).
7. Marca las capacidades que tu app requiera (Push Notifications, Sign In with Apple, Associated Domains, etc.).
8. Haz clic en **Register**.

---

### Paso 3.2: Generar la Clave API de App Store Connect (`.p8`)
1. Entra a: [appstoreconnect.apple.com/access/api](https://appstoreconnect.apple.com/access/api)
2. Ve a la pestaña **Keys** (o Claves).
3. En la sección **Team Keys**, haz clic en el botón **`+`** (Generate API Key).
4. Asigna un nombre: `Codemagic CI Key`.
5. En **Access**, selecciona el rol: **App Manager** o **Admin**.
6. Haz clic en **Generate**.
7. Inmediatamente verás:
   - **Key ID** (Identificador de Clave): Un código de 10 caracteres (ej: `GTQR99QA2Q`). **¡Cópialo!**
   - **Issuer ID**: Un UUID en la parte superior (ej: `69a6de88-xxxx-xxxx-xxxx-xxxxxxxxxxxx`). **¡Cópialo!**
   - **Download API Key**: Haz clic para descargar el archivo `AuthKey_XXXXXXXXXX.p8`.  
     ⚠️ *Nota: Apple solo te permite descargar este archivo UNA sola vez. Guárdalo en un lugar seguro.*

---

### Paso 3.3: Generar el Certificado `.p12` en Windows con OpenSSL
*En Mac se usa la app "Acceso a Llaveros", pero en Windows lo hacemos en 3 comandos:*

#### Opción Rápida (Asistente Automático):
Ejecuta el script incluido:
```cmd
tools_ios_windows\scripts\2_crear_certificado_p12_en_windows.bat
```

#### Opción Manual por Comandos:
Abre PowerShell o CMD y navega a tu carpeta de herramientas:

1. **Generar la clave privada (.key):**
   ```cmd
   "C:\Program Files\Git\usr\bin\openssl.exe" genrsa -out mi_llave_privada.key 2048
   ```

2. **Generar el Certificate Signing Request (CSR):**
   ```cmd
   "C:\Program Files\Git\usr\bin\openssl.exe" req -new -key mi_llave_privada.key -out peticion.csr -subj "/emailAddress=tuemail@ejemplo.com, CN=Tu Nombre, C=CO"
   ```

3. **Subir el CSR a Apple:**
   - Entra a [developer.apple.com/account/resources/certificates/list](https://developer.apple.com/account/resources/certificates/list)
   - Clic en `+` -> Selecciona **Apple Distribution** (o **iOS Distribution**).
   - Sube el archivo `peticion.csr`.
   - Descarga el certificado generado por Apple y guárdalo como `distribution.cer`.

4. **Convertir el certificado y fusionarlo con tu clave privada en `.p12`:**
   ```cmd
   "C:\Program Files\Git\usr\bin\openssl.exe" x509 -in distribution.cer -inform DER -out certificado.pem -outform PEM
   "C:\Program Files\Git\usr\bin\openssl.exe" pkcs12 -export -inkey mi_llave_privada.key -in certificado.pem -out CONNECT.p12 -legacy
   ```
   *(Ingresa una contraseña para proteger el archivo .p12 y guárdala).*

5. **Descargar el Provisioning Profile (`.mobileprovision`):**
   - Entra a [developer.apple.com/account/resources/profiles/list](https://developer.apple.com/account/resources/profiles/list)
   - Clic en `+` -> Selecciona **App Store** (o **Ad Hoc** si vas a registrar UDIDs de prueba).
   - Selecciona tu App ID (`com.connectapp.co`).
   - Selecciona el certificado de distribución que acabas de crear.
   - Asigna un nombre al perfil (ej: `CONNECT_AppStore`).
   - Haz clic en **Generate** y descárgalo como `CONNECT.mobileprovision`.

---

## 🚀 4. MÉTODO 1: Compilar IPA con IOSbuilder CLI y GitHub Actions
*(Ideal para generar un archivo `.ipa` directo a tu carpeta `dist/` en Windows sin pasar por TestFlight)*

El proyecto incluye el ejecutable `builder.exe` en `tools_ios_windows\builder.exe`.

### 4.1. Archivo de Configuración (`builder.json`)
En la raíz de tu proyecto debe existir el archivo `builder.json`:
```json
{
  "project": "CONNECT",
  "platform": "ios",
  "github": {
    "owner": "WormSlice",
    "repo": "iosbuilder"
  },
  "ios": {
    "path": "ios",
    "signing": true,
    "configuration": "Release"
  },
  "flutter": {
    "version": "3.44.1",
    "watch": {}
  }
}
```

### 4.2. Configurar la Firma en GitHub (Una sola vez)
Ejecuta el script:
```cmd
tools_ios_windows\scripts\3_configurar_firma_github.bat
```
O directamente con el CLI:
```cmd
tools_ios_windows\builder.exe signing setup -c CONNECT.p12 -p CONNECT.mobileprovision
```
*El comando te pedirá la contraseña del `.p12` y subirá los secretos cifrados a GitHub Secrets:*
- `IOS_CERTIFICATE`
- `IOS_CERTIFICATE_PASSWORD`
- `IOS_PROVISIONING_PROFILE`

### 4.3. Disparar la Compilación y Descargar el `.ipa`
Ejecuta:
```cmd
tools_ios_windows\scripts\4_compilar_con_iosbuilder.bat
```
O con comandos directos:
- **Compilación Firmada (Release Oficial):**
  ```cmd
  tools_ios_windows\builder.exe ios build -o dist
  ```
- **Compilación Sin Firma (Unsigned IPA para Sideloadly / AltStore / Scarlet):**
  ```cmd
  tools_ios_windows\builder.exe ios build --unsigned -o dist
  ```

*El CLI monitorea el workflow en GitHub Actions, espera a que termine el runner de macOS y descarga el archivo `.ipa` final directamente en tu carpeta local `dist/` de Windows.*

---

## ☁️ 5. MÉTODO 2: Pipeline Profesional con CodeMagic (Directo a TestFlight)
*(El método recomendado para producción y publicación a la tienda de Apple)*

### 5.1. Conectar tu Repositorio en Codemagic
1. Entra a [codemagic.io](https://codemagic.io/) e inicia sesión con tu cuenta de GitHub.
2. En la lista de aplicaciones, añade tu repositorio (ej: `WormSlice/iosbuilder`).
3. Selecciona el tipo de proyecto: **Flutter App (via codemagic.yaml)**.

### 5.2. Configurar el Environment Group en Codemagic
1. Ve a la pestaña **Environment variables** en tu aplicación de Codemagic.
2. Crea un grupo llamado exactamente: `app_store_credentials`.
3. Añade las siguientes variables dentro de ese grupo:

| Variable | Tipo | Valor |
| :--- | :--- | :--- |
| `APP_STORE_CONNECT_KEY_IDENTIFIER` | Texto | Tu Key ID de 10 caracteres (ej: `GTQR99QA2Q`) |
| `APP_STORE_CONNECT_ISSUER_ID` | Texto | Tu Issuer ID UUID de Apple |
| `APP_STORE_CONNECT_PRIVATE_KEY` | Archivo o Secreto Seguro | Pega todo el contenido del archivo `AuthKey_XXXXXXXXXX.p8` (incluyendo `-----BEGIN PRIVATE KEY-----`) |
| `CERTIFICATE_PRIVATE_KEY` | Secreto Seguro | Clave privada RSA para generar certificados si no tienes uno previo |

### 5.3. El archivo `codemagic.yaml`
Asegúrate de que en la raíz de tu proyecto esté tu archivo `codemagic.yaml`.

Puntos clave que realiza este archivo:
1. **Máquina rápida:** Usa `instance_type: mac_mini_m2`.
2. **Caché limpia:** Elimina Pods antiguos para que ninguna dependencia quede desalineada (`pod install --repo-update`).
3. **Firma Cero-Touch:** Ejecuta `xcode-project use-profiles`, descargando y sincronizando automáticamente el certificado y perfil de App Store Connect.
4. **Protección de versión:** Consulta a TestFlight el último build subido (`app-store-connect get-latest-testflight-build-number`) y si el build local es menor o igual, lo incrementa automáticamente para que Apple jamás rechace la subida por duplicado.
5. **Compilación Release:** Genera el `.ipa` oficial optimizado.
6. **Subida automática:** Envía el binario directamente a TestFlight con `publishing.app_store_connect.submit_to_testflight: true`.

### 5.4. Cómo disparar la compilación desde Windows
Cada vez que hagas un cambio en tu código y quieras subir una nueva versión:
Ejecuta el script:
```cmd
tools_ios_windows\scripts\5_incrementar_y_subir_codemagic.bat
```
Este script:
1. Lee `pubspec.yaml` e incrementa automáticamente el build number (ej: `1.1.52+98` -> `1.1.52+99`).
2. Realiza el `git commit` y `git push origin main`.
3. Codemagic detecta el cambio en segundos y arranca la compilación en la Mac mini M2.
4. En 10-15 minutos recibirás la notificación de Apple de que tu app ya está procesada en TestFlight.

---

## 🛠️ 6. Solución de Errores Comunes (Troubleshooting)

### Error 1: "The bundle version must be higher than the previously uploaded version" (Error -19232)
- **Causa:** Subiste un build a TestFlight con el mismo número o uno inferior (ej: build 97 cuando ya existía el 97).
- **Solución:** Incrementa el número después del signo `+` en `pubspec.yaml` (ej: `version: 1.1.52+98`). Nuestro script `5_incrementar_y_subir_codemagic.bat` y el pipeline de `codemagic.yaml` ya previenen esto automáticamente.

### Error 2: "Missing purpose string in Info.plist" (Permisos de Cámara/Micrófono)
- **Causa:** Apple rechaza la subida si alguna librería usa cámara, micrófono o galería y no tienes la descripción en `ios/Runner/Info.plist`.
- **Solución:** Verifica que `ios/Runner/Info.plist` tenga las claves requeridas:
  ```xml
  <key>NSCameraUsageDescription</key>
  <string>Requerido para tomar fotos de publicaciones y perfil.</string>
  <key>NSPhotoLibraryUsageDescription</key>
  <string>Requerido para seleccionar imágenes de la galería.</string>
  <key>NSMicrophoneUsageDescription</key>
  <string>Requerido para notas de voz y llamadas de audio.</string>
  ```

### Error 3: "CocoaPods could not find compatible versions"
- **Causa:** Caché antigua de Pods en el servidor o versiones de librerías desactualizadas en `ios/Podfile.lock`.
- **Solución:** En el `codemagic.yaml` ya incluimos los pasos:
  ```bash
  rm -rf ios/Pods ios/Podfile.lock ios/.symlinks
  flutter clean
  flutter pub get
  cd ios && pod install --repo-update
  ```

---

## 📋 7. Resumen de Comandos Rápidos

| Acción | Comando en Windows |
| :--- | :--- |
| **Diagnóstico del entorno** | `tools_ios_windows\scripts\1_preflight_check.bat` |
| **Generar certificado .p12** | `tools_ios_windows\scripts\2_crear_certificado_p12_en_windows.bat` |
| **Configurar firma en GitHub** | `tools_ios_windows\scripts\3_configurar_firma_github.bat` |
| **Compilar IPA con GitHub Actions** | `tools_ios_windows\scripts\4_compilar_con_iosbuilder.bat` |
| **Subir versión a TestFlight con Codemagic** | `tools_ios_windows\scripts\5_incrementar_y_subir_codemagic.bat` |

---
¡Listo! Siguiendo esta guía tienes control total sobre el desarrollo y publicación de iOS trabajando 100% desde Windows.
