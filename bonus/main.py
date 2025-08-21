

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Carnet numérique (CLI + menu)")
    p.add_argument("--quiet", action="store_true", help="Mode silencieux")
    return p

def run():
    parser = build_parser()
    args = parser.parse_args()
    
    if args.quiet:
        print("I am running quiet")
    else:
        print("I am running normal")


if (__name__ == "__main__"):
    run()