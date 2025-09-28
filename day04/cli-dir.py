



import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SuperDir")
    p.add_argument("--dir", default=".", help="Chemin")
    return p

def run():
    print("running")
    p = build_parser()
    args = p.parse_args()  # <-- ici on récupère les valeurs
    print("Fichier :", args.dir)

if __name__ == "__main__":
    run()
