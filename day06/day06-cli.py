import argparse, sys, time, json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

from myutils6 import mylog
from myutils6 import readfile
from myparser6 import fetch_json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_file = sub.add_parser("read-file")
    p_file.add_argument("path")

    p_web = sub.add_parser("fetch-json")
    p_web.add_argument("url")

    p_test = sub.add_parser("self-test")

    args = p.parse_args()
    try:
        if args.cmd == "read-file":
            txt = readfile(Path(args.path))
            mylog(f"Lu {len(txt)} caractères", args.quiet)
            sys.exit(0)

        elif args.cmd == "fetch-json":
            obj = fetch_json(args.url)
            mylog(f"Clés reçues: {list(obj)[:5]}", args.quiet)
            sys.exit(0)

        elif args.cmd == "self-test":
            try:
                readfile(Path("inexistant.txt"))
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("safe_read aurait dû lever FileNotFoundError")
            mylog("Self-test OK ✅", args.quiet)
            sys.exit(0)

    except Exception as e:
        mylog(str(e), args.quiet)
        sys.exit(1)

if __name__ == "__main__":
    main()