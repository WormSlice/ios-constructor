"""
Generador de Videos en Blanco y Negro (Minimalista / Editorial)
Resolucion: 1920x1080 @ 30 FPS
Genera archivos de video reales .mp4 directamente listos para edicion.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\Soporte\Documents\Tutorial\videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tipografias del sistema Windows
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font(FONT_BOLD, 36)
font_subtitle = get_font(FONT_REGULAR, 20)
font_card_title = get_font(FONT_BOLD, 22)
font_body = get_font(FONT_REGULAR, 17)
font_body_bold = get_font(FONT_BOLD, 17)
font_mono = get_font(FONT_MONO, 16)
font_mono_small = get_font(FONT_MONO, 14)
font_clock = get_font(FONT_REGULAR, 76)
font_badge = get_font(FONT_BOLD, 13)

# Colores estrictos Blanco y Negro
BG_COLOR = (12, 12, 14)          # Negro fondo mate
CARD_BG = (22, 22, 26)           # Gris muy oscuro para tarjetas
CARD_BORDER = (60, 60, 66)       # Borde sutil
CARD_BORDER_HI = (255, 255, 255) # Borde blanco activo
TEXT_WHITE = (255, 255, 255)     # Blanco principal
TEXT_MUTED = (160, 160, 165)     # Gris claro
TEXT_FAINT = (95, 95, 100)       # Gris tenue
LINE_COLOR = (50, 50, 56)        # Lineas de conexion


def create_blank_canvas():
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    return img


# ==============================================================================
# VIDEO 1: ARQUITECTURA Y FLUJO DE COMPILACION (12 Segundos / 360 Frames)
# ==============================================================================
def render_video_1():
    out_path = os.path.join(OUTPUT_DIR, "1_arquitectura_flujo_ios.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    total_frames = 360  # 12 segundos
    writer = cv2.VideoWriter(out_path, fourcc, fps, (1920, 1080))
    print(f"Generando {out_path} ({total_frames} frames)...")

    nodes = [
        {"title": "1. PC WINDOWS", "sub": "Flutter / VS Code", "detail": "Desarrollo local en Dart\ngit push origin main", "x": 160},
        {"title": "2. GITHUB", "sub": "WormSlice/iosbuilder", "detail": "Repositorio y Secretos\nDispara Webhook de CI", "x": 580},
        {"title": "3. MACOS RUNNER", "sub": "Codemagic Mac mini M2", "detail": "xcode-project use-profiles\nflutter build ipa (Release)", "x": 1000},
        {"title": "4. TESTFLIGHT", "sub": "App Store Connect", "detail": "Subida automatica\nListo para instalar en iPhone", "x": 1420},
    ]

    card_w = 340
    card_h = 240
    card_y = 380

    for f in range(total_frames):
        img = create_blank_canvas()
        draw = ImageDraw.Draw(img)

        # Header
        draw.text((160, 120), "ARQUITECTURA DE COMPILACION IOS DESDE WINDOWS", font=font_title, fill=TEXT_WHITE)
        draw.line([(160, 175), (600, 175)], fill=TEXT_WHITE, width=2)
        draw.text((160, 195), "Flujo automatizado de Integracion Continua en la Nube (Sin necesidad de Mac fisica)", font=font_subtitle, fill=TEXT_MUTED)

        # Determinar fase activa (cada fase dura 75 frames)
        active_phase = min(3, f // 75)
        phase_progress = (f % 75) / 75.0

        # Dibujar lineas de conexion entre nodos
        for i in range(len(nodes) - 1):
            x1 = nodes[i]["x"] + card_w
            x2 = nodes[i + 1]["x"]
            mid_y = card_y + card_h // 2
            draw.line([(x1, mid_y), (x2, mid_y)], fill=LINE_COLOR, width=2)

            # Paquete animado que viaja
            if i == active_phase:
                travel_x = int(x1 + (x2 - x1) * phase_progress)
                draw.rectangle([(travel_x - 12, mid_y - 4), (travel_x + 12, mid_y + 4)], fill=TEXT_WHITE)

        # Dibujar tarjetas de nodos
        for i, node in enumerate(nodes):
            x = node["x"]
            y = card_y
            is_active = (i <= active_phase)
            is_current = (i == active_phase)

            border_c = CARD_BORDER_HI if is_current else (CARD_BORDER if not is_active else (150, 150, 155))
            fill_c = (30, 30, 35) if is_current else CARD_BG

            draw.rectangle([(x, y), (x + card_w, y + card_h)], fill=fill_c, outline=border_c, width=2 if is_current else 1)

            # Titulo del nodo
            draw.text((x + 24, y + 24), node["title"], font=font_card_title, fill=TEXT_WHITE if is_active else TEXT_MUTED)
            draw.text((x + 24, y + 60), node["sub"], font=font_mono_small, fill=TEXT_MUTED if is_active else TEXT_FAINT)
            draw.line([(x + 24, y + 90), (x + card_w - 24, y + 90)], fill=LINE_COLOR, width=1)

            # Detalles del nodo
            lines = node["detail"].split("\n")
            draw.text((x + 24, y + 115), lines[0], font=font_body, fill=TEXT_WHITE if is_active else TEXT_FAINT)
            if len(lines) > 1:
                draw.text((x + 24, y + 155), lines[1], font=font_mono_small, fill=TEXT_MUTED if is_active else TEXT_FAINT)

            # Indicador de estado
            status_text = "[ COMPLETADO ]" if (i < active_phase or (active_phase == 3 and f > 320)) else ("[ EN PROCESO ]" if is_current else "[ ESPERA ]")
            draw.text((x + 24, y + 195), status_text, font=font_mono_small, fill=TEXT_WHITE if is_current else (TEXT_MUTED if i < active_phase else TEXT_FAINT))

        # Barra inferior de terminal log
        term_y = 780
        draw.rectangle([(160, term_y), (1760, term_y + 110)], fill=(18, 18, 20), outline=CARD_BORDER, width=1)
        draw.text((190, term_y + 20), "CONSOLA DE COMPILACION (CI/CD LOG):", font=font_mono_small, fill=TEXT_MUTED)

        if active_phase == 0:
            log_line = "> git add . && git commit -m 'release: v1.1.52+98' && git push origin main"
        elif active_phase == 1:
            log_line = "> github: Push recibido en WormSlice/iosbuilder (rama main) -> Ejecutando webhook"
        elif active_phase == 2:
            log_line = "> codemagic: Provisioning Apple certs (.p8) -> Xcode compile (mac_mini_m2) -> IPA generado"
        else:
            log_line = "> testflight: IPA subido y validado exitosamente. Build 98 disponible para evaluadores."

        draw.text((190, term_y + 55), log_line, font=font_mono, fill=TEXT_WHITE)

        # Convertir PIL a OpenCV BGR
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        writer.write(frame)

    writer.release()
    print(f"Listo: {out_path}")


# ==============================================================================
# VIDEO 2: ERRORES FRECUENTES Y SOLUCIONES (15 Segundos / 450 Frames)
# ==============================================================================
def render_video_2():
    out_path = os.path.join(OUTPUT_DIR, "2_errores_y_soluciones.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    total_frames = 450  # 15 segundos (3 errores de 5s c/u)
    writer = cv2.VideoWriter(out_path, fourcc, fps, (1920, 1080))
    print(f"Generando {out_path} ({total_frames} frames)...")

    errors_data = [
        {
            "tag": "ERROR 1 DE 3",
            "title": "Error -19232: Duplicate Bundle Version",
            "causa": "Apple rechaza el build porque el numero de compilacion ya existe en TestFlight.",
            "codigo_err": 'ENTITY_ERROR.ATTRIBUTE.INVALID.DUPLICATE\n"The bundle version must be higher than the previously uploaded version."',
            "solucion": "Incrementar el numero despues del signo '+' en pubspec.yaml antes de subir:",
            "codigo_sol": "# pubspec.yaml\nversion: 1.1.52+98   # <-- Cambiar a un build superior al previo (ej: 98)\n\n# O ejecutar en Windows: tools_ios_windows\\scripts\\5_incrementar_y_subir_codemagic.bat"
        },
        {
            "tag": "ERROR 2 DE 3",
            "title": "ITMS-90683: Missing Purpose Strings (Info.plist)",
            "causa": "Apple procesa el IPA pero lo rechaza si usas camara o galeria sin descripciones de privacidad.",
            "codigo_err": '"Missing purpose string in Info.plist: Your app uses APIs\nthat access sensitive user data without NSCameraUsageDescription."',
            "solucion": "Declarar los permisos requeridos con descripcion legible en ios/Runner/Info.plist:",
            "codigo_sol": "<!-- ios/Runner/Info.plist -->\n<key>NSCameraUsageDescription</key>\n<string>Requerido para tomar fotos de publicaciones y perfil.</string>\n<key>NSPhotoLibraryUsageDescription</key>\n<string>Requerido para seleccionar imagenes de la galeria.</string>"
        },
        {
            "tag": "ERROR 3 DE 3",
            "title": "Conflictos de Cache en CocoaPods (Podfile.lock)",
            "causa": "Versiones antiguas en cache del runner causan fallos al instalar librerias de iOS.",
            "codigo_err": "[!] CocoaPods could not find compatible versions for pod\n    In Podfile: firebase_core (= 3.12.1) Specs satisfying dependency not found.",
            "solucion": "Ejecutar limpieza profunda de dependencias antes de compilar en el pipeline:",
            "codigo_sol": "# Scripts incluidos en codemagic.yaml:\nrm -rf ios/Pods ios/Podfile.lock ios/.symlinks\nflutter clean\nflutter pub get\ncd ios && pod install --repo-update && cd .."
        }
    ]

    for f in range(total_frames):
        img = create_blank_canvas()
        draw = ImageDraw.Draw(img)

        # Header comun
        draw.text((160, 100), "RESOLUCION DE ERRORES CRITICOS DE APPLE EN WINDOWS", font=font_title, fill=TEXT_WHITE)
        draw.line([(160, 155), (600, 155)], fill=TEXT_WHITE, width=2)
        draw.text((160, 175), "Soluciones tecnicas comprobadas para garantizar aprobacion en App Store y TestFlight", font=font_subtitle, fill=TEXT_MUTED)

        # Seleccionar error actual (cada uno dura 150 frames = 5 seg)
        err_idx = min(2, f // 150)
        item = errors_data[err_idx]

        # Indicador de paso superior
        draw.text((160, 240), f"[ {item['tag']} ]", font=font_mono, fill=TEXT_WHITE)
        draw.text((320, 238), item["title"], font=font_card_title, fill=TEXT_WHITE)

        # Tarjeta Izquierda: Problema
        col_w = 760
        y_cards = 300
        h_cards = 560

        draw.rectangle([(160, y_cards), (160 + col_w, y_cards + h_cards)], fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.text((195, y_cards + 30), "PROBLEMA / RECHAZO DE APPLE:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((195, y_cards + 70), item["causa"], font=font_body, fill=TEXT_WHITE)

        # Bloque de codigo error
        draw.rectangle([(195, y_cards + 160), (160 + col_w - 35, y_cards + 510)], fill=(15, 15, 18), outline=(50, 50, 55), width=1)
        draw.text((215, y_cards + 180), "MENSAJE DEL SERVIDOR APPLE:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((215, y_cards + 225), item["codigo_err"], font=font_mono_small, fill=TEXT_WHITE)

        # Tarjeta Derecha: Solucion
        rx = 1000
        draw.rectangle([(rx, y_cards), (rx + col_w, y_cards + h_cards)], fill=CARD_BG, outline=CARD_BORDER_HI, width=1)
        draw.text((rx + 35, y_cards + 30), "SOLUCION RECOMENDADA:", font=font_mono_small, fill=TEXT_WHITE)
        draw.text((rx + 35, y_cards + 70), item["solucion"], font=font_body, fill=TEXT_WHITE)

        # Bloque de codigo solucion
        draw.rectangle([(rx + 35, y_cards + 160), (rx + col_w - 35, y_cards + 510)], fill=(15, 15, 18), outline=CARD_BORDER, width=1)
        draw.text((rx + 55, y_cards + 180), "CODIGO / COMANDO EXACTO:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((rx + 55, y_cards + 225), item["codigo_sol"], font=font_mono_small, fill=TEXT_WHITE)

        # Barra inferior de progreso
        draw.line([(160, 920), (1760, 920)], fill=LINE_COLOR, width=1)
        prog_w = int((f / total_frames) * 1600)
        draw.line([(160, 920), (160 + prog_w, 920)], fill=TEXT_WHITE, width=2)
        draw.text((160, 940), f"Paso {err_idx + 1} de 3 • Guion Video Tutorial iOS en Windows", font=font_mono_small, fill=TEXT_MUTED)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        writer.write(frame)

    writer.release()
    print(f"Listo: {out_path}")


# ==============================================================================
# VIDEO 3: NOTIFICACION DE TESTFLIGHT EN IPHONE (9 Segundos / 270 Frames)
# ==============================================================================
def render_video_3():
    out_path = os.path.join(OUTPUT_DIR, "3_notificacion_testflight.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    total_frames = 270  # 9 segundos
    writer = cv2.VideoWriter(out_path, fourcc, fps, (1920, 1080))
    print(f"Generando {out_path} ({total_frames} frames)...")

    # Geometria del telefono centrado
    phone_w = 400
    phone_h = 800
    phone_x = (1920 - phone_w) // 2
    phone_y = (1080 - phone_h) // 2

    for f in range(total_frames):
        img = create_blank_canvas()
        draw = ImageDraw.Draw(img)

        # Informacion lateral izquierda
        draw.text((160, 200), "RESULTADO FINAL EN IPHONE", font=font_title, fill=TEXT_WHITE)
        draw.line([(160, 255), (450, 255)], fill=TEXT_WHITE, width=2)
        draw.text((160, 280), "Despliegue automatico a TestFlight\nrecibido en el dispositivo de prueba.", font=font_subtitle, fill=TEXT_MUTED)

        draw.text((160, 390), "CARACTERISTICAS DEL DESPLIEGUE:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((160, 430), "• Compilado en servidor remoto Mac M2\n• Firma digital con API Key (.p8)\n• Version verificada: v1.1.52 (Build 98)\n• Cero Mac fisica requerida en local", font=font_body, fill=TEXT_WHITE)

        # Informacion lateral derecha
        draw.text((1400, 430), "TIEMPO ESTIMADO:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((1400, 465), "6 a 8 minutos", font=font_card_title, fill=TEXT_WHITE)
        draw.text((1400, 530), "ESTADO DE ENTREGA:", font=font_mono_small, fill=TEXT_MUTED)
        draw.text((1400, 565), "LISTO PARA INSTALAR", font=font_card_title, fill=TEXT_WHITE)

        # Silueta minimalista del telefono
        draw.rounded_rectangle([(phone_x, phone_y), (phone_x + phone_w, phone_y + phone_h)], radius=50, fill=(0, 0, 0), outline=CARD_BORDER_HI, width=2)

        # Dynamic Island minimalista
        di_w = 120
        di_h = 32
        di_x = phone_x + (phone_w - di_w) // 2
        draw.rounded_rectangle([(di_x, phone_y + 18), (di_x + di_w, phone_y + 18 + di_h)], radius=16, fill=(25, 25, 28), outline=CARD_BORDER, width=1)

        # Pantalla de bloqueo vs App Screen
        # Fases:
        # Frames 0 a 45: Solo reloj
        # Frames 45 a 150: Aparece la notificacion de TestFlight
        # Frames 150 a 270: Abre pantalla de la app con boton INSTALAR -> LISTO
        if f < 150:
            # Reloj en pantalla de bloqueo
            draw.text((phone_x + 95, phone_y + 110), "09:41", font=font_clock, fill=TEXT_WHITE)
            draw.text((phone_x + 85, phone_y + 205), "Domingo, 27 de Septiembre", font=font_mono_small, fill=TEXT_MUTED)

            # Notificacion deslizable (entra a partir del frame 45)
            if f >= 45:
                # Animacion de entrada
                slide_prog = min(1.0, (f - 45) / 20.0)
                notif_w = 350
                notif_h = 135
                notif_x = phone_x + (phone_w - notif_w) // 2
                target_y = phone_y + 280
                curr_y = int(target_y - (1.0 - slide_prog) * 30)

                draw.rounded_rectangle([(notif_x, curr_y), (notif_x + notif_w, curr_y + notif_h)], radius=18, fill=(28, 28, 32), outline=CARD_BORDER_HI, width=1)

                draw.text((notif_x + 20, curr_y + 16), "TESTFLIGHT  •  AHORA", font=font_mono_small, fill=TEXT_MUTED)
                draw.text((notif_x + 20, curr_y + 44), "CONNECT está listo para probar", font=font_body_bold, fill=TEXT_WHITE)
                draw.text((notif_x + 20, curr_y + 78), "Version 1.1.52 (Build 98) disponible\npara instalar en este dispositivo.", font=font_mono_small, fill=TEXT_MUTED)
        else:
            # Pantalla de TestFlight abierta
            draw.text((phone_x + 30, phone_y + 80), "< Apps", font=font_mono, fill=TEXT_WHITE)
            draw.text((phone_x + 30, phone_y + 130), "CONNECT", font=font_card_title, fill=TEXT_WHITE)
            draw.text((phone_x + 30, phone_y + 165), "WormSlice Technologies", font=font_mono_small, fill=TEXT_MUTED)
            draw.text((phone_x + 30, phone_y + 195), "Version 1.1.52 (Build 98)", font=font_mono_small, fill=TEXT_WHITE)

            # Boton de instalacion
            btn_w = 340
            btn_h = 50
            btn_x = phone_x + 30
            btn_y = phone_y + 245

            if f < 210:
                draw.rounded_rectangle([(btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h)], radius=12, fill=(255, 255, 255), outline=TEXT_WHITE, width=1)
                draw.text((btn_x + 130, btn_y + 14), "INSTALAR", font=font_body_bold, fill=(0, 0, 0))
            else:
                draw.rounded_rectangle([(btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h)], radius=12, fill=(28, 28, 32), outline=CARD_BORDER_HI, width=1)
                draw.text((btn_x + 120, btn_y + 14), "INSTALADO", font=font_body_bold, fill=TEXT_WHITE)

            # Notas de version
            draw.line([(phone_x + 30, phone_y + 330), (phone_x + phone_w - 30, phone_y + 330)], fill=LINE_COLOR, width=1)
            draw.text((phone_x + 30, phone_y + 355), "NOVEDADES:", font=font_mono_small, fill=TEXT_MUTED)
            notes = "• Compilado 100% en Windows\n• Version build 98 verificada\n• Optimizacion de chats y perfil\n• Rendimiento nativo iOS"
            draw.text((phone_x + 30, phone_y + 390), notes, font=font_body, fill=TEXT_WHITE)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        writer.write(frame)

    writer.release()
    print(f"Listo: {out_path}")


if __name__ == "__main__":
    print(f"Iniciando renderizado de videos en blanco y negro a: {OUTPUT_DIR}")
    render_video_1()
    render_video_2()
    render_video_3()
    print("Todos los videos han sido generados exitosamente.")
