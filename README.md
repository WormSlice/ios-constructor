# 📱 iOS Constructor: Plantilla & Herramientas para Compilar iOS en Windows
> Desarrolla en tu PC con Windows y compila aplicaciones para iPhone (.ipa / TestFlight / App Store) utilizando runners en la nube sin necesidad de tener una computadora Mac.

---

## 🚀 Cómo Usar este Repositorio como Plantilla

1. Haz clic en el botón verde arriba a la derecha: **`Use this template`** ➔ **`Create a new repository`**.
2. Asígnalo como privado o público en tu propia cuenta de GitHub.
3. Clónalo en tu computadora con Windows:
   ```bash
   git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
   cd TU-REPOSITORIO
   ```

---

## 🧰 ¿Qué incluye este repositorio?

* **Carpeta `ios/` completa con Swift moderno:**
  * `AppDelegate.swift` con ciclo de vida y plugins registrados.
  * `Info.plist` con permisos de privacidad ya redactados (Cámara, Micrófono, Fotos, Ubicación) para evitar el rechazo de Apple ITMS-90683.
  * `Podfile` optimizado para CocoaPods en CI/CD con flags de compilación preestablecidos.
  * Proyectos de Xcode (`Runner.xcodeproj` y `Runner.xcworkspace`) listos para los runners macOS.
* **Flujo de GitHub Actions (`.github/workflows/ios-build.yml`):**
  * Compila en servidores virtuales con `macos-latest` de GitHub.
  * Soporta compilación firmada (con certificados de Apple) y compilación sin firmar (`--unsigned` para Sideloadly / AltStore).
  * Genera el archivo `.ipa` como artefacto descargable en la pestaña **Actions**.
* **Integración con CodeMagic (`codemagic.yaml`):**
  * Pipeline automático hacia **TestFlight** y **App Store**.
  * Script de protección contra el error `-19232` (auto-incremento de versión contra la API de TestFlight).
  * Firma automática mediante `xcode-project use-profiles` y clave API `.p8`.
* **Herramienta de Automatización en Windows (`AUTO_DEPLOY_IOS.bat`):**
  * Menú interactivo para Windows con 1 clic:
    * `[1]` Bump de versión en `pubspec.yaml`, commit y push inmediato a GitHub.
    * `[2]` Compilar y descargar `.ipa` directamente a tu PC con `builder.exe`.
    * `[3]` Subir secretos de firma a GitHub Actions.
    * `[4]` Generar certificados oficiales de Apple `.p12` con OpenSSL en Windows.

---

## ⚡ Guía Rápida de Compilación en Windows

### Método 1: Compilar IPA gratis con GitHub Actions
1. Configura tus secretos en GitHub (ejecutando `scripts\3_configurar_firma_github.bat` o desde los Settings de tu repositorio).
2. Para compilar y descargar el `.ipa` directamente a tu carpeta local `dist\`:
   ```cmd
   builder.exe ios build -o dist
   ```
   *(O sin firma para pruebas rápidas: `builder.exe ios build --unsigned -o dist`)*.

---

### Método 2: Publicar automáticamente a TestFlight con CodeMagic
1. En [codemagic.io](https://codemagic.io), añade este repositorio.
2. Agrega el grupo de variables de entorno `app_store_credentials` con tu clave API `.p8` de App Store Connect.
3. Cada vez que hagas cambios en Windows, ejecuta:
   ```cmd
   AUTO_DEPLOY_IOS.bat --quick
   ```
   El script incrementará tu versión en `pubspec.yaml`, hará commit y enviará los cambios a GitHub, activando la compilación en la Mac mini M2 hacia TestFlight.

---

## 📄 Guías Detalladas Incluidas

* [GUIA_PASO_A_PASO_COMANDOS.md](GUIA_PASO_A_PASO_COMANDOS.md): Manual técnico completo con todos los comandos y enlaces de Apple Developer.
* [GUION_VIDEO_TUTORIAL.md](GUION_VIDEO_TUTORIAL.md): Guion de video con la estructura paso a paso.

---
Creado por **WormSlice Technologies**