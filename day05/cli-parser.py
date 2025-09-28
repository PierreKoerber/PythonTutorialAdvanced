import argparse

import json 

from myparser import fetch_page



def main():
    p = argparse.ArgumentParser(description="Fetch a web page and extract links")
    p.add_argument("--fetch-url", required=True, help="URL de la page à analyser")
    p.add_argument("--out", default="page.json", help="Fichier de sortie JSON")
    args = p.parse_args()

    data = fetch_page(args.fetch_url)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Résultats sauvegardés dans {args.out}")

if __name__ == "__main__":
    main()