"""
IOS AUTO-DEPLOY TOOL FOR WINDOWS
Automatizacion de despliegue, versionado y push continuo a GitHub para GitHub Actions y Codemagic.
"""

import os
import sys
import re
import json
import subprocess
import shutil

def find_project_root():
    curr = os.getcwd()
    if os.path.exists(os.path.join(curr, "pubspec.yaml")):
        return curr
    connect_path = r"C:\Users\Soporte\Documents\CONNECT\CONNECT"
    if os.path.exists(os.path.join(connect_path, "pubspec.yaml")):
        return connect_path
    parent = os.path.abspath(os.path.join(curr, ".."))
    if os.path.exists(os.path.join(parent, "pubspec.yaml")):
        return parent
    return curr

PROJECT_ROOT = find_project_root()
PUBSPEC_PATH = os.path.join(PROJECT_ROOT, "pubspec.yaml")
CODEMAGIC_PATH = os.path.join(PROJECT_ROOT, "codemagic.yaml")
BUILDER_JSON_PATH = os.path.join(PROJECT_ROOT, "builder.json")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plantilla_flutter_ios")


def run_git(args, cwd=PROJECT_ROOT):
    cmd = ["git"] + args
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    return result.returncode == 0, result.stdout.strip(), result.stderr.strip()


def get_git_info():
    _, branch, _ = run_git(["branch", "--show-current"])
    if not branch:
        branch = "main"
    _, remote, _ = run_git(["config", "--get", "remote.origin.url"])
    _, status, _ = run_git(["status", "-s"])
    return branch, remote, status


def parse_github_url(url):
    """Extrae el owner y el repo de una URL HTTPS o SSH de GitHub"""
    match = re.search(r"github\.com[:/]([^/]+)/([^/\.]+)(?:\.git)?", url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def sync_builder_json(owner, repo):
    data = {}
    if os.path.exists(BUILDER_JSON_PATH):
        try:
            with open(BUILDER_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    
    data.setdefault("project", os.path.basename(PROJECT_ROOT))
    data.setdefault("platform", "ios")
    data["github"] = {
        "owner": owner,
        "repo": repo
    }
    data.setdefault("ios", {"path": "ios", "signing": True, "configuration": "Release"})
    data.setdefault("flutter", {"version": "3.44.1", "watch": {}})
    data.setdefault("reactNative", {})
    data.setdefault("mobai", {})

    with open(BUILDER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] builder.json sincronizado con tu repo: {owner}/{repo}")


def configure_remote_interactive():
    _, curr_remote, _ = get_git_info()
    print("\n" + "="*70)
    print("      CONFIGURAR VINCULACION CON REPOSITORIO DE GITHUB")
    print("="*70)
    if curr_remote:
        print(f" Repositorio actual: {curr_remote}")
    else:
        print(" [AVISO] Este proyecto aun NO tiene un repositorio de GitHub vinculado.")
    print("="*70)
    
    url = input("Ingresa la URL de TU repositorio de GitHub\n(ej: https://github.com/tu-usuario/tu-repo.git): ").strip()
    if not url:
        if curr_remote:
            print("Se conserva el repositorio actual.")
            return curr_remote
        else:
            print("[ERROR] No se proporciono ninguna URL.")
            return None

    if not os.path.exists(os.path.join(PROJECT_ROOT, ".git")):
        print("Inicializando repositorio Git local...")
        run_git(["init"])
        run_git(["branch", "-M", "main"])

    if curr_remote:
        run_git(["remote", "set-url", "origin", url])
    else:
        run_git(["remote", "add", "origin", url])

    owner, repo = parse_github_url(url)
    if owner and repo:
        sync_builder_json(owner, repo)

    print(f"\n[OK] Repositorio vinculado exitosamente a: {url}")
    return url


def ensure_git_remote():
    _, remote, _ = get_git_info()
    if not remote:
        print("\n[ALERTA] Este proyecto no tiene un repositorio de GitHub vinculado.")
        remote = configure_remote_interactive()
        if not remote:
            return False
    return True


def get_current_version():
    if not os.path.exists(PUBSPEC_PATH):
        return None, None
    with open(PUBSPEC_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"version:\s*([0-9\.]+)\+([0-9]+)", content)
    if match:
        return match.group(1), int(match.group(2))
    return None, None


def bump_version(next_build=None, next_name=None):
    if not os.path.exists(PUBSPEC_PATH):
        print(f"[ERROR] No se encontro pubspec.yaml en {PUBSPEC_PATH}")
        return None, None
    
    with open(PUBSPEC_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"version:\s*([0-9\.]+)\+([0-9]+)", content)
    if not match:
        print("[ERROR] Formato de version no valido en pubspec.yaml")
        return None, None

    ver_name = next_name if next_name else match.group(1)
    curr_build = int(match.group(2))
    new_build = next_build if next_build is not None else (curr_build + 1)
    new_ver_str = f"{ver_name}+{new_build}"

    new_content = re.sub(r"version:\s*[0-9\.]+\+[0-9]+", f"version: {new_ver_str}", content)
    with open(PUBSPEC_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    if os.path.exists(CODEMAGIC_PATH):
        with open(CODEMAGIC_PATH, "r", encoding="utf-8") as f:
            cm_content = f.read()
        cm_content = re.sub(r"PUBSPEC_BUILD:=\d+", f"PUBSPEC_BUILD:={new_build}", cm_content)
        cm_content = re.sub(r"NEXT_BUILD=\d+", f"NEXT_BUILD={new_build}", cm_content)
        with open(CODEMAGIC_PATH, "w", encoding="utf-8") as f:
            f.write(cm_content)

    return ver_name, new_build


def do_bump_and_push(custom_msg=None):
    if not ensure_git_remote():
        print("[ERROR] Despliegue cancelado: falta configurar el repositorio de GitHub.")
        return False

    curr_name, curr_build = get_current_version()
    if not curr_name:
        print("[ERROR] No se pudo leer la version de pubspec.yaml")
        return False

    next_name, next_build = bump_version()
    new_ver = f"{next_name}+{next_build}"
    print(f"\n[OK] Version incrementada: {curr_name}+{curr_build} -> {new_ver}")

    branch, remote, _ = get_git_info()
    owner, repo = parse_github_url(remote)
    commit_msg = custom_msg if custom_msg else f"chore(release): bump iOS build to {new_ver}"

    print(f"[1/3] Añadiendo cambios a Git (rama '{branch}')...")
    run_git(["add", "."])

    print(f"[2/3] Creando commit: \"{commit_msg}\"...")
    ok, stdout, stderr = run_git(["commit", "-m", commit_msg])
    if not ok and "nothing to commit" not in stderr and "nothing to commit" not in stdout:
        print(f"[ADVERTENCIA] {stderr}")

    print(f"[3/3] Enviando cambios a GitHub (origin {branch})...")
    ok, stdout, stderr = run_git(["push", "origin", branch])
    if ok:
        print("\n" + "="*70)
        print("          ¡DESPLIEGUE ENVIADO CON EXITO A GITHUB!")
        print("="*70)
        print(f"  Version:   {new_ver}")
        print(f"  Rama:      {branch}")
        print(f"  Repositorio: {remote}")
        print("\n  RUTAS DE COMPILACION ACTIVADAS:")
        if owner and repo:
            print(f"  1. GITHUB ACTIONS: https://github.com/{owner}/{repo}/actions")
        print("  2. CODEMAGIC:      https://codemagic.io/apps")
        print("="*70 + "\n")
        return True
    else:
        print(f"[ERROR al hacer push]: {stderr}")
        return False


def install_ios_template(target_dir=PROJECT_ROOT):
    ios_src = os.path.join(TEMPLATE_DIR, "ios")
    ios_dst = os.path.join(target_dir, "ios")

    if not os.path.exists(ios_src):
        print(f"[ERROR] No se encontro la plantilla en {ios_src}")
        return False

    print(f"\nInstalando plantilla base de iOS (Swift) en: {ios_dst}...")
    try:
        shutil.copytree(ios_src, ios_dst, dirs_exist_ok=True)
        print("[OK] Carpeta 'ios/' instalada con AppDelegate.swift, Info.plist y Podfile.")

        # Copiar Workflow de GitHub Actions (.github/workflows/ios-build.yml)
        gh_workflow_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "github_workflow_ios_build.yml")
        gh_workflow_dst_dir = os.path.join(target_dir, ".github", "workflows")
        os.makedirs(gh_workflow_dst_dir, exist_ok=True)
        gh_workflow_dst = os.path.join(gh_workflow_dst_dir, "ios-build.yml")
        if os.path.exists(gh_workflow_src):
            shutil.copy(gh_workflow_src, gh_workflow_dst)
            print("[OK] Workflow de GitHub Actions instalado en: .github/workflows/ios-build.yml")

        # Copiar codemagic.yaml y builder.json si no existen
        cm_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codemagic.yaml.template")
        if os.path.exists(cm_template) and not os.path.exists(os.path.join(target_dir, "codemagic.yaml")):
            shutil.copy(cm_template, os.path.join(target_dir, "codemagic.yaml"))
            print("[OK] 'codemagic.yaml' configurado en la raiz.")

        bj_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "builder.json.template")
        if os.path.exists(bj_template) and not os.path.exists(os.path.join(target_dir, "builder.json")):
            shutil.copy(bj_template, os.path.join(target_dir, "builder.json"))
            print("[OK] 'builder.json' configurado en la raiz.")

        _, remote, _ = get_git_info()
        if remote:
            owner, repo = parse_github_url(remote)
            if owner and repo:
                sync_builder_json(owner, repo)

        return True
    except Exception as e:
        print(f"[ERROR] Fallo al copiar plantilla: {e}")
        return False


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--quick", "-q", "--bump-and-push"]:
        msg = sys.argv[2] if len(sys.argv) > 2 else None
        do_bump_and_push(msg)
        return

    while True:
        curr_name, curr_build = get_current_version()
        branch, remote, status = get_git_info()
        ver_str = f"{curr_name}+{curr_build}" if curr_name else "No detectada"
        owner, repo = parse_github_url(remote) if remote else (None, None)

        print("="*75)
        print("          HERRAMIENTA AUTOMATIZADA: COMPILAR IOS DESDE WINDOWS")
        print("="*75)
        print(f" Proyecto local: {PROJECT_ROOT}")
        print(f" Version actual: {ver_str}")
        print(f" Repositorio:    {remote or '[!] NO VINCULADO (Usa la opcion 6)'}")
        print(f" Rama activa:    {branch}")
        has_changes = "Si (Archivos pendientes de subir)" if status else "No (Al dia)"
        print(f" Estado Git:     {has_changes}")
        print("="*75)
        print("\n--- [ ACCION PRINCIPAL DE SUBIDA ] ---")
        print("  [1] Bump de version y push automatico a GitHub")
        print("      (Dispara la compilacion en GITHUB ACTIONS y en CODEMAGIC a la vez)")
        print("\n--- [ METODO 1: GITHUB ACTIONS (Compilar IPA gratis) ] ---")
        print("  [2] Disparar compilacion remota y descargar .ipa a Windows (builder.exe)")
        print("  [3] Subir certificados .p12 y .mobileprovision a GitHub Secrets")
        print("  [4] Autenticar CLI con tu cuenta de GitHub (builder.exe auth github)")
        print("\n--- [ CONFIGURACION DEL PROYECTO ] ---")
        print("  [5] Instalar / Reparar plantilla completa (iOS Swift + Workflows + Podfile)")
        print("  [6] Vincular o Cambiar Repositorio de GitHub (Remote Origin)")
        print("  [7] Generar certificado de Apple .p12 con OpenSSL en Windows")
        print("  [0] Salir")
        print()

        opcion = input("Elige una opcion (0-7) [1]: ").strip()
        if opcion == "" or opcion == "1":
            do_bump_and_push()
            input("Presiona Enter para continuar...")
        elif opcion == "2":
            builder_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "builder.exe")
            if not os.path.exists(builder_exe):
                builder_exe = os.path.join(PROJECT_ROOT, "builder-windows-amd64.exe")
            print("\nModos de compilacion en GitHub Actions:")
            print("  1. Firmado (Release con tus secretos de GitHub)")
            print("  2. Sin firmar (Unsigned IPA para Sideloadly / AltStore)")
            sub_op = input("Elige (1 o 2) [1]: ").strip()
            dist_dir = os.path.join(PROJECT_ROOT, "dist")
            if sub_op == "2":
                subprocess.run([builder_exe, "ios", "build", "--unsigned", "-o", dist_dir], cwd=PROJECT_ROOT)
            else:
                subprocess.run([builder_exe, "ios", "build", "-o", dist_dir], cwd=PROJECT_ROOT)
            input("Presiona Enter para continuar...")
        elif opcion == "3":
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "3_configurar_firma_github.bat")
            if os.path.exists(script_path):
                subprocess.run(["cmd.exe", "/c", script_path])
            input("Presiona Enter para continuar...")
        elif opcion == "4":
            builder_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "builder.exe")
            if not os.path.exists(builder_exe):
                builder_exe = os.path.join(PROJECT_ROOT, "builder-windows-amd64.exe")
            subprocess.run([builder_exe, "auth", "github"], cwd=PROJECT_ROOT)
            input("Presiona Enter para continuar...")
        elif opcion == "5":
            install_ios_template()
            input("Presiona Enter para continuar...")
        elif opcion == "6":
            configure_remote_interactive()
            input("Presiona Enter para continuar...")
        elif opcion == "7":
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "2_crear_certificado_p12_en_windows.bat")
            if os.path.exists(script_path):
                subprocess.run(["cmd.exe", "/c", script_path])
            input("Presiona Enter para continuar...")
        elif opcion == "0":
            print("Hasta luego.")
            break


if __name__ == "__main__":
    main()
