# 🎬 GUION MAESTRO PARA GRABAR VIDEO TUTORIAL
## "Cómo Compilar Apps de iOS en Windows (TestFlight y Archivo IPA Sin Tener Mac)"

---

### 📌 Ficha Técnica del Video
- **Título Sugerido 1 (Alto impacto):** Cómo Compilar Apps de iOS en WINDOWS Sin Tener una Mac (Flutter, Codemagic y GitHub Actions)
- **Título Sugerido 2 (Directo al grano):** De Windows a la App Store: Guía Definitiva para Compilar iOS (TestFlight y Archivo IPA)
- **Duración Estimada:** 12 a 15 minutos.
- **Tono:** Seguro, dinámico, didáctico, profesional y sin rodeos.
- **Recursos necesarios para la grabación:**
  - OBS Studio o grabador de pantalla en 1080p o 4K.
  - Micrófono nítido.
  - Ventanas preparadas: VS Code con el proyecto abierto, GitHub (`WormSlice/iosbuilder`), Codemagic dashboard, Portal Apple Developer y App Store Connect.
  - Un iPhone con la app **TestFlight** instalada para mostrar el resultado final en vivo.

---

### ⏱️ Estructura Temporal del Video
| Bloque | Minutos | Tema Principal |
| :--- | :--- | :--- |
| **01** | `00:00 - 01:10` | **Gancho Inicial & Derribando el Mito de la Mac** |
| **02** | `01:10 - 02:40` | **La Arquitectura: ¿Cómo funciona el método que usamos?** |
| **03** | `02:40 - 05:30` | **Paso 1: Credenciales de Apple desde Windows (API Key .p8 y Certificados)** |
| **04** | `05:30 - 08:30` | **Paso 2: Método IOSbuilder (Compilar IPA directo con GitHub Actions)** |
| **05** | `08:30 - 12:30` | **Paso 3: Método CodeMagic (Pipeline profesional directo a TestFlight)** |
| **06** | `12:30 - 14:00` | **Errores Comunes y Soluciones (Error -19232 de Versión y CocoaPods)** |
| **07** | `14:00 - 14:45` | **Cierre, Pack de Herramientas y Llamada a la Acción** |

---

## 🎬 GUION ESCENA POR ESCENA (Con Indicaciones Visuales y Diálogo Exacto)

---

### 🟢 BLOQUE 1: GANCHO INICIAL Y EL MITO DE LA MAC
**Duración:** `00:00 - 01:10`

#### 🖥️ En Pantalla:
- **Cámara o Captura:** Primeros 5 segundos: Primer plano tuyo en cámara o tu pantalla de Windows mostrando el escritorio con VS Code abierto en una app Flutter y una ventana de Codemagic terminando una compilación verde con el texto *"Successfully uploaded to TestFlight"*.
- **Corte B-Roll:** Notificación en un iPhone físico: *"CONNECT está listo para probar en TestFlight"*.

#### 🎙️ Qué Decir (Voz):
> *"¿Alguna vez te han dicho que para programar y compilar aplicaciones de iOS estás obligado a gastar dos mil dólares en una computadora Mac?*
> 
> *Déjame decirte que hoy en día, eso es completamente FALSO.*
> 
> *En este video te voy a enseñar el método exacto y profesional que utilizamos a diario para desarrollar nuestras aplicaciones en Windows y compilarlas directamente para iPhone: tanto para generar archivos `.ipa` listos para instalar, como para publicarlas de forma automática a TestFlight y la App Store oficial de Apple.*
> 
> *Todo el código lo escribimos en Windows, y la compilación la delegamos a servidores macOS en la nube usando dos herramientas brutales: **CodeMagic** y nuestro propio **IOSbuilder con GitHub Actions**.*
> 
> *Quédate hasta el final, porque además te voy a dejar una carpeta con todos los scripts y herramientas automatizadas para que lo hagas en menos de 5 minutos. ¡Comencemos!"*

---

### 🟢 BLOQUE 2: LA ARQUITECTURA (CÓMO FUNCIONA EL MÉTODO)
**Duración:** `01:10 - 02:40`

#### 🖥️ En Pantalla:
- Diagrama sencillo o animación en pantalla mostrando las 3 partes:
  1. Tu PC con Windows (Flutter / VS Code).
  2. Repositorio en GitHub (`WormSlice/iosbuilder`).
  3. Servidor macOS en la nube (Codemagic Mac mini M2 / GitHub Actions) -> TestFlight.
- Pasa a mostrar tu terminal de Windows y el explorador de archivos.

#### 🎙️ Qué Decir (Voz):
> *"Antes de tocar código, entendamos la lógica. ¿Por qué necesitamos este puente?*
> 
> *Apple exige por motivos de licencias que el compilador de Xcode se ejecute sobre el sistema operativo macOS. Pero en lugar de tener una máquina física al lado de tu escritorio consumiendo luz y dinero, lo que hacemos es un flujo de CI/CD (Integración y Despliegue Continuo).*
> 
> *Tú trabajas en tu entorno habitual en Windows. Cuando terminas una funcionalidad, haces un `git push` a tu repositorio en GitHub.*
> 
> *En ese instante, se activa un servidor remoto con procesador Mac mini M2 en la nube. Este servidor clona tu proyecto, instala CocoaPods, descarga los certificados oficiales de Apple usando llaves API seguras, compila el binario `.ipa` y lo manda directo a TestFlight.*
> 
> *Hoy te voy a enseñar dos vías:*
> - *La primera es **IOSbuilder con GitHub Actions**, excelente si quieres compilar rápido un archivo IPA y descargarlo a tu PC para pruebas directas o enviarlo a un cliente.*
> - *La segunda es **CodeMagic**, el estándar de oro para publicar actualizaciones continuas a la App Store sin intervención manual."*

---

### 🟢 BLOQUE 3: CREDENCIALES DE APPLE DESDE WINDOWS (SIN MAC)
**Duración:** `02:40 - 05:30`

#### 🖥️ En Pantalla:
- Abre el navegador web en [developer.apple.com](https://developer.apple.com) y luego en [appstoreconnect.apple.com](https://appstoreconnect.apple.com).
- Zoom al cursor mientras creas el App ID y la API Key.
- Luego muestra la carpeta `tools_ios_windows\scripts` y ejecuta el script `2_crear_certificado_p12_en_windows.bat`.

#### 🎙️ Qué Decir (Voz):
> *"Para que cualquier servidor pueda firmar en nombre de tu cuenta de Apple, necesitas dos cosas fundamentales.*
> 
> *Lo primero: tu **App ID**. Entramos a `developer.apple.com` en la sección de Identifiers, creamos un nuevo App ID de tipo App, y le ponemos nuestro Bundle Identifier exacto. En nuestro caso de ejemplo: `com.connectapp.co`.*
> 
> *Lo segundo, y la verdadera joya de la corona: la **Clave API de App Store Connect**.*
> *Entramos a `appstoreconnect.apple.com`, vamos a la pestaña 'Acceso', luego a 'Claves' o 'Keys', y generamos una nueva Team Key con permisos de Administrador o App Manager.*
> 
> *Apple nos dará tres datos cruciales:*
> 1. *El **Key ID**, que es un código de 10 caracteres.*
> 2. *El **Issuer ID**, que es este código largo de aquí.*
> 3. *Y el botón para descargar un archivo con extensión `.p8`.*
> 
> *¡MUCHA ATENCIÓN AQUÍ!: Este archivo `.p8` solo se puede descargar UNA sola vez en la vida. Si cierras la ventana y no lo guardaste, tendrás que revocarlo y crear otro.*
> 
> *Ahora bien, ¿qué pasa si necesitas un certificado clásico `.p12` para firmar manualmente y no tienes una Mac con 'Acceso a Llaveros'?*
> 
> *No te preocupes. Si tienes Git instalado en Windows, ya tienes la herramienta **OpenSSL** en tu sistema.*
> *En la carpeta de herramientas que les preparé, simplemente abren el script `2_crear_certificado_p12_en_windows.bat`.*
> 
> *(Muestra la consola ejecutándose)*
> *Escriben su correo, su nombre, y el script genera una clave privada y un archivo `peticion.csr`. Ese archivo lo suben a Apple Developer en la sección 'Certificates', descargan el `.cer`, lo pegan en esta carpeta y el script les genera su archivo `.p12` listo con su contraseña. ¡Cero Mac requerida!"*

---

### 🟢 BLOQUE 4: MÉTODO 1 - COMPILAR CON IOSBUILDER (GITHUB ACTIONS)
**Duración:** `05:30 - 08:30`

#### 🖥️ En Pantalla:
- Abre VS Code. Muestra el archivo `builder.json` en la raíz.
- Abre una ventana de terminal en Windows (PowerShell / CMD).
- Muestra el archivo ejecutable `builder.exe` en `tools_ios_windows`.
- Muestra cómo se ejecuta el comando de firma y luego el comando de compilación:
  `.\tools_ios_windows\builder.exe ios build -o dist`
- Muestra la consola mostrando el progreso en tiempo real y cómo se crea el archivo `.ipa` dentro de la carpeta `dist\`.

#### 🎙️ Qué Decir (Voz):
> *"Veamos el primer método: **IOSbuilder**.*
> 
> *En la raíz de nuestro proyecto tenemos un archivo llamado `builder.json`. Aquí solo definimos el nombre de la app, nuestro usuario y repositorio de GitHub, la versión de Flutter, y que la plataforma es iOS.*
> 
> *Para que GitHub Actions pueda firmar la app, primero subimos nuestros certificados a los secretos del repositorio. En lugar de hacerlo a mano, usamos nuestra herramienta con este comando:*
> 
> ```powershell
> .\tools_ios_windows\builder.exe signing setup -c CONNECT.p12 -p CONNECT.mobileprovision
> ```
> 
> *Nos pedirá la contraseña del certificado `.p12`, lo cifra en base64 y lo inyecta directamente como GitHub Secrets.*
> 
> *Y ahora, para compilar la app, simplemente ejecutamos:*
> ```powershell
> .\tools_ios_windows\builder.exe ios build -o dist
> ```
> 
> *Fíjense en la magia que ocurre aquí: nuestra terminal en Windows se conecta con los servidores de GitHub Actions, activa una máquina virtual con macOS, ejecuta `flutter pub get`, instala los pods, firma el binario con nuestro perfil, y cuando termina el proceso... ¡miren esto!*
> 
> *(Muestra el explorador de Windows abriendo la carpeta dist)*
> *Descarga automáticamente el archivo `.ipa` firmado directamente en nuestra computadora con Windows.*
> 
> *Y si quisieran una versión sin firmar para sideloading rápido con AltStore o Sideloadly, solo le añaden el flag `--unsigned`."*

---

### 🟢 BLOQUE 5: MÉTODO 2 - PIPELINE PROFESIONAL CON CODEMAGIC (TESTFLIGHT)
**Duración:** `08:30 - 12:30`

#### 🖥️ En Pantalla:
- Abre el archivo `codemagic.yaml` en VS Code.
- Señala con el mouse las partes clave:
  1. `instance_type: mac_mini_m2`
  2. `groups: - app_store_credentials`
  3. `xcode-project use-profiles`
  4. Script de auto-incremento de versión comparando contra TestFlight.
  5. `publishing: submit_to_testflight: true`.
- Muestra la web de Codemagic con la aplicación configurada y las variables de entorno.
- Ejecuta en Windows el script `5_incrementar_y_subir_codemagic.bat`.
- Muestra en Codemagic cómo la barra de progreso avanza y se completa.
- Muestra el iPhone físico abriendo TestFlight y viendo la nueva versión disponible para instalar.

#### 🎙️ Qué Decir (Voz):
> *"Ahora vamos al método supremo: **CodeMagic**.*
> 
> *Este es el flujo que usamos cuando queremos que la app llegue automáticamente a los teléfonos de nuestros testers en TestFlight o para mandar la app a revisión de la App Store.*
> 
> *En la raíz de nuestro proyecto tenemos el archivo `codemagic.yaml`. Quiero que presten especial atención a tres líneas maestras que les incluí en la plantilla:*
> 
> *Primero: le decimos que use una máquina `mac_mini_m2`. Esto hace que la compilación tarde apenas 6 a 8 minutos.*
> 
> *Segundo: en la sección de scripts, ejecutamos `xcode-project use-profiles`. Esta sola línea se comunica con la API de App Store Connect usando la clave `.p8` que descargamos hace un momento, y genera o descarga los perfiles de aprovisionamiento en la nube de forma transparente. ¡No tienes que volver a pelear con perfiles expirados jamás!*
> 
> *Y tercero: este script inteligente que les preparé aquí. Este bloque de código consulta a Apple cuál fue el último número de compilación que subimos a TestFlight. Si en nuestro `pubspec.yaml` teníamos el build 97 y en TestFlight ya existía, automáticamente lo sube a 98 antes de compilar. Esto erradica el típico error que frustra a todos los desarrolladores.*
> 
> *Para disparar la subida, ni siquiera tenemos que entrar a la página web.*
> *Hicimos cambios en el código en Windows, abrimos nuestro script:*
> ```cmd
> tools_ios_windows\scripts\5_incrementar_y_subir_codemagic.bat
> ```
> *El script sube la versión en `pubspec.yaml`, hace commit, hace `git push origin main`...*
> *(Transición a pantalla de Codemagic)*
> *...y en menos de 10 segundos, Codemagic detecta el cambio y comienza a construir la versión de iOS en una Mac remota.*
> 
> *(Cámara rápida o corte al build exitoso en verde)*
> *Al finalizar, el propio pipeline envía el `.ipa` a TestFlight.*
> *(Muestra la pantalla del iPhone con la notificación de TestFlight)*
> *Y como pueden ver aquí en mi iPhone, ya tengo la notificación de TestFlight lista para descargar y probar la app en vivo."*

---

### 🟢 BLOQUE 6: ERRORES TÍPICOS Y CÓMO EVITARLOS
**Duración:** `12:30 - 14:00`

#### 🖥️ En Pantalla:
- Muestra diapositiva o texto en pantalla con las alertas:
  - Error 1: Apple Error -19232 (Duplicate Bundle Version).
  - Error 2: Permisos faltantes en `ios/Runner/Info.plist`.
  - Error 3: Caché de CocoaPods.
- Muestra el archivo `ios/Runner/Info.plist` en VS Code mostrando `NSCameraUsageDescription`, etc.

#### 🎙️ Qué Decir (Voz):
> *"Antes de terminar, quiero ahorrarles horas de dolor de cabeza con los 3 errores más comunes:*
> 
> *El primero: el infame **Error -19232 de Apple**. Ocurre cuando intentas subir un build que tiene el mismo número que uno anterior. Apple te devolverá un error diciendo que el bundle version debe ser estrictamente mayor. Recuerden siempre incrementar el número después del signo `+` en su `pubspec.yaml`, o usar nuestro script automatizado.*
> 
> *El segundo: **Rechazo por permisos en Info.plist**. Si en Flutter usas paquetes como `image_picker`, `camera` o `permission_handler`, Apple rechazará tu IPA en el procesamiento si no pusiste los textos descriptivos en el archivo `Info.plist`: como `NSCameraUsageDescription` o `NSPhotoLibraryUsageDescription`.*
> 
> *Y el tercero: **Conflictos de CocoaPods**. Si cambiaste versiones de dependencias en Flutter, a veces los servidores en la nube fallan por caché vieja. Por eso en nuestro `codemagic.yaml` siempre incluimos un paso de limpieza con `rm -rf ios/Pods ios/Podfile.lock` y `pod install --repo-update`."*

---

### 🟢 BLOQUE 7: CIERRE Y RECURSOS
**Duración:** `14:00 - 14:45`

#### 🖥️ En Pantalla:
- Muestra el explorador de archivos con la carpeta `tools_ios_windows` que creamos hoy con todos los scripts, guías y plantillas.
- Pantalla final con tu canal, botón de suscribirse y videos recomendados.

#### 🎙️ Qué Decir (Voz):
> *"Como pudieron ver, no tener una Mac ya no es ninguna limitación para crear, compilar y publicar aplicaciones profesionales en la App Store trabajando cómodamente desde tu PC con Windows.*
> 
> *En la descripción del video les dejé el enlace con la carpeta completa de herramientas: incluye el ejecutable de `builder.exe`, la plantilla de `codemagic.yaml`, la guía paso a paso con todos los comandos y los 5 scripts para automatizar todo el proceso con un solo clic.*
> 
> *Si este video te sirvió y te ahorró los miles de dólares de una Mac, déjame un buen like, suscríbete para más contenido de desarrollo profesional y déjame en los comentarios qué otra parte del flujo te gustaría que profundicemos.*
> 
> *¡Nos vemos en el próximo video!"*

---
*(Fin del Guion)*
