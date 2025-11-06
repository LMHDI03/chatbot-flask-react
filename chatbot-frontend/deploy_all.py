import os, sys, shutil, subprocess
from pathlib import Path

FRONTEND_PROJECT = Path(r"C:\Users\mehdi\Desktop\chatbot-frontend")
BACKEND_FRONT_DIR = Path(r"C:\Users\mehdi\Desktop\chatbot-mini\frontend")

def find_exe(name: str):
    # sous Windows, npm est npm.cmd
    exe = shutil.which(name)
    if exe: return exe
    if os.name == "nt":
        exe = shutil.which(name + ".cmd")
        if exe: return exe
        # chemin par défaut d'une install Node
        possible = r"C:\Program Files\nodejs\%s.cmd" % name
        if os.path.exists(possible): return possible
    return None

def run(cmd, cwd=None):
    print("→", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def npm_build(project: Path):
    npm = find_exe("npm")
    if not npm:
        print("❌ npm introuvable. Installe Node.js LTS et rouvre PowerShell.")
        sys.exit(1)

    node_modules = project / "node_modules"
    if not node_modules.exists():
        print("📦 node_modules absent → npm ci")
        run([npm, "ci"], cwd=project)
    else:
        print("📦 node_modules déjà présent → skip install")

    print("🏗️  Build Vite (npm run build)")
    run([npm, "run", "build"], cwd=project)
    dist = project / "dist"
    if not dist.exists():
        print("❌ Build terminé mais dist/ introuvable.")
        sys.exit(1)
    return dist

def mirror_dist(dist: Path, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    print(f"🧹 Nettoyage du dossier cible: {dest}")
    for p in dest.iterdir():
        if p.is_file() or p.is_symlink():
            p.unlink()
        else:
            shutil.rmtree(p)
    print(f"📤 Copie du build vers: {dest}")
    for item in dist.iterdir():
        d = dest / item.name
        if item.is_dir():
            shutil.copytree(item, d)
        else:
            shutil.copy2(item, d)

def main():
    print("=== Déploiement Frontend → Flask ===")
    print(f"Frontend: {FRONTEND_PROJECT}")
    print(f"Cible   : {BACKEND_FRONT_DIR}\n")
    try:
        dist = npm_build(FRONTEND_PROJECT)
        mirror_dist(dist, BACKEND_FRONT_DIR)
        print("\n✅ Déploiement terminé.")
        print(r"➡ Lance/relance Flask :  python C:\Users\mehdi\Desktop\chatbot-mini\run_api.py")
        print("➡ Ouvre : http://127.0.0.1:8000")
    except subprocess.CalledProcessError as e:
        print(f"❌ Commande échouée (code {e.returncode}).")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
