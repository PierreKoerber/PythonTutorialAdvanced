"""
prompt_privacy.py — Anonymisation réversible de prompts (regex + HMAC), avec mini-CLI.
Aucune dépendance externe. Python 3.9+ conseillé.

Fonctions clés
--------------
- anonymize(text, secret, mode="placeholder"): remplace PII/identifiants par des tags stables {{TYPE_xxx}}.
- deanonymize(text, mapping): restaure le texte original à partir d'un mapping.
- save_mapping(path, mapping, secret): sauvegarde le mapping signé (HMAC-SHA256) pour intégrité.
- load_mapping(path, secret): recharge + vérifie l'intégrité du mapping.

Couverture par défaut (adaptable)
---------------------------------
EMAIL, PHONE (y compris +41), IBAN (CH), AHV (AVS suisse), URL, PERSON_NAME (basique),
CLIENT_ID (ex: CUST-123456), INVOICE (ex: INV-2025-000123), DATE (aaaa-mm-jj, dd.mm.yyyy),
ADDRESS_HINT (mentions d'adresse simples: rue, avenue, ch., route… + numéro).

⚠ Limites
---------
- Les NER complexes (noms ambigus, adresses complètes) nécessitent des modèles ML (ex: Presidio).
- La stylométrie / le contexte très spécifique peut ré-identifier même sans PII.
- Le mapping est signé pour intégrité, pas chiffré. Stockez le fichier mapping en lieu sûr
  (ou chiffré par votre système — e.g., fs chiffré, KMS, Vault).

CLI
---
Anonymiser un fichier (stdout) et sauver le mapping:
    python prompt_privacy.py anon --in input.txt --mapping map.json --secret-file .key

Désanonymiser (stdout) en utilisant un mapping existant:
    python prompt_privacy.py deanon --in anon.txt --mapping map.json --secret-file .key

Générer une clé secrète (base64) pour les tags/HMAC:
    python prompt_privacy.py genkey > .key

API rapide
----------
    from prompt_privacy import anonymize, deanonymize
    secret = b"...32+ bytes..."
    anon, mapping = anonymize("Jean <jean@ex.com> IBAN CH93...", secret)
    original = deanonymize(anon, mapping)
"""

from __future__ import annotations
from typing import Dict, Tuple, List, Pattern, Iterable
import re
import hmac
import hashlib
import base64
import json
import unicodedata
from dataclasses import dataclass, field


# ---------------------------- Patterns ---------------------------------

def _re(p: str, flags=re.IGNORECASE) -> Pattern[str]:
    return re.compile(p, flags)

PATTERNS: Dict[str, Pattern[str]] = {
    # E-mails
    "EMAIL": _re(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b"),
    # Téléphones (accents, séparateurs, +41, formats FR/CH approximatifs)
    "PHONE": _re(r"(?:\+?\s?4?1\s?[\s().-]?)?(?:0?\d[\s().-]?){8,}"),
    # IBAN (CH…)
    "IBAN": _re(r"\bCH\d{2}[A-Z0-9]{17}\b"),
    # Numéro AVS/AHV Suisse (forme la plus courante: 756.XXXX.XXXX.XX ou 756XXXXXXXXXX)
    "AHV": _re(r"\b756(?:[\s\.-]?\d){10}\b"),
    # URL
    "URL": _re(r"\bhttps?://[^\s)]+"),
    # Noms très basiques (Capitalisé(s)), évite les mots trop courts
    "PERSON_NAME": _re(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b"),
    # IDs métiers (modifiez selon vos conventions)
    "CLIENT_ID": _re(r"\bCUST-\d{4,}\b"),
    "INVOICE": _re(r"\bINV-[0-9]{4}-[0-9]{3,}\b"),
    # Dates usuelles (ajoutez-en d'autres si besoin)
    "DATE": _re(r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4})\b"),
    # Adresse rudimentaire (rue/av./route/ch.), très heuristique
    "ADDRESS_HINT": _re(r"\b(?:(?:rue|avenue|av\.?|route|rt\.?|chemin|ch\.?)\s+[A-Za-zÀ-ÖØ-öø-ÿ'’.-]+(?:\s+\d{1,4}[A-Za-z]?)?)\b"),
}


# ------------------------ Core anonymization ----------------------------

def _normalize(s: str) -> str:
    # Normalise unicode et espaces
    s = unicodedata.normalize("NFC", s)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return s

def _stable_tag(secret: bytes, kind: str, value: str) -> str:
    digest = hmac.new(secret, (kind + ":" + value).encode("utf-8"), hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(digest)[:10].decode("ascii")
    return f"{{{{{kind}_{token}}}}}"

@dataclass
class AnonResult:
    text: str
    mapping: Dict[str, str] = field(default_factory=dict)

def anonymize(text: str, secret: bytes, include: Iterable[str] | None = None,
              exclude: Iterable[str] | None = None,
              mode: str = "placeholder") -> AnonResult:
    """
    Remplace les occurrences trouvées par des tags stables {{TYPE_token}}.
    - secret: bytes pour HMAC (32+ octets recommandé).
    - include/exclude: limiter/retirer certains types.
    - mode: "placeholder" (par défaut) ou "redact" (masquage partiel).

    Retour: AnonResult(text, mapping) — mapping[tag] = valeur originale
    """
    if not isinstance(secret, (bytes, bytearray)) or len(secret) < 16:
        raise ValueError("secret doit être en bytes et faire au moins 16 octets (32+ recommandé).")

    text = _normalize(text)
    mapping: Dict[str, str] = {}

    kinds = list(PATTERNS.keys())
    if include:
        include_set = set(include)
        kinds = [k for k in kinds if k in include_set]
    if exclude:
        exclude_set = set(exclude)
        kinds = [k for k in kinds if k not in exclude_set]

    # On applique les patterns un par un (du plus spécifique au plus générique si nécessaire)
    for kind in kinds:
        rx = PATTERNS[kind]

        def repl(m: re.Match) -> str:
            val = m.group(0)
            # Évite de retagger un tag déjà présent
            if val.startswith("{{") and val.endswith("}}"):
                return val
            tag = _stable_tag(secret, kind, val)
            if mode == "redact":
                # Masquage partiel lisible
                masked = _mask_value(kind, val)
                mapping[tag] = val
                return f"{tag}({masked})"
            else:
                mapping[tag] = val
                return tag

        text = rx.sub(repl, text)

    return AnonResult(text=text, mapping=mapping)

def _mask_value(kind: str, val: str) -> str:
    v = val.strip()
    if kind in ("EMAIL",):
        # aaa@***.com
        try:
            name, dom = v.split("@", 1)
            return (name[:1] + "***@" + _mask_mid(dom))
        except ValueError:
            return _mask_mid(v)
    if kind in ("PHONE", "IBAN", "AHV"):
        return _keep_last(v, 4, fill="•")
    if kind in ("CLIENT_ID", "INVOICE"):
        return _keep_last(v, 3, fill="•")
    if kind in ("PERSON_NAME", "ADDRESS_HINT"):
        return v[0] + "…" if v else v
    if kind in ("URL",):
        return v.split("/", 3)[2] if v.startswith("http") else _mask_mid(v)
    return _mask_mid(v)

def _keep_last(s: str, n: int, fill: str = "•") -> str:
    s2 = re.sub(r"\s+", "", s)
    if len(s2) <= n:
        return s2
    return fill * (len(s2) - n) + s2[-n:]

def _mask_mid(s: str) -> str:
    if len(s) <= 4:
        return "•" * len(s)
    left = len(s) // 3
    right = len(s) // 3
    return s[:left] + "•" * (len(s) - left - right) + s[-right:]


# ---------------------- Mapping persistence (HMAC) ----------------------

def save_mapping(path: str, mapping: Dict[str, str], secret: bytes) -> None:
    """
    Sauve mapping + MAC (HMAC-SHA256) pour intégrité.
    Ne chiffre pas les valeurs -> stockez le fichier en lieu sûr.
    """
    payload = {"mapping": mapping}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    mac = hmac.new(secret, raw, hashlib.sha256).hexdigest()
    data = {"mapping": mapping, "mac": mac}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_mapping(path: str, secret: bytes) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = data.get("mapping", {})
    payload = {"mapping": mapping}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    mac = hmac.new(secret, raw, hashlib.sha256).hexdigest()
    if mac != data.get("mac"):
        raise ValueError("Mapping corrompu: MAC invalide (secret incorrect ou fichier altéré).")
    return mapping


# ------------------------------- CLI -----------------------------------

def _read_secret(secret: str | None, secret_file: str | None) -> bytes:
    if secret and secret_file:
        raise SystemExit("--secret et --secret-file sont exclusifs.")
    if secret:
        return base64.b64decode(secret) if _looks_b64(secret) else secret.encode("utf-8")
    if secret_file:
        with open(secret_file, "rb") as f:
            s = f.read().strip()
            return base64.b64decode(s) if _looks_b64_bytes(s) else s
    raise SystemExit("Fournissez --secret ou --secret-file (utilisez 'genkey' pour en générer une).")

def _looks_b64(s: str) -> bool:
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False

def _looks_b64_bytes(b: bytes) -> bool:
    try:
        base64.b64decode(b, validate=True)
        return True
    except Exception:
        return False

def cmd_genkey(args):
    # Clé 32 bytes aléatoire, exportée en base64
    key = secrets.token_bytes(32)
    print(base64.b64encode(key).decode("ascii"))

def cmd_anon(args):
    secret = _read_secret(args.secret, args.secret_file)
    text = sys.stdin.read() if args.infile == "-" else open(args.infile, "r", encoding="utf-8").read()
    include = args.include.split(",") if args.include else None
    exclude = args.exclude.split(",") if args.exclude else None
    result = anonymize(text, secret, include=include, exclude=exclude, mode=args.mode)
    if args.mapping:
        save_mapping(args.mapping, result.mapping, secret)
    print(result.text)

def cmd_deanon(args):
    secret = _read_secret(args.secret, args.secret_file)
    mapping = load_mapping(args.mapping, secret)
    text = sys.stdin.read() if args.infile == "-" else open(args.infile, "r", encoding="utf-8").read()
    out = deanonymize(text, mapping)
    print(out)


def deanonymize(text: str, mapping: Dict[str, str]) -> str:
    # Remplacement direct; en cas de collisions partielles, on remplace les tags plus longs d'abord
    items = sorted(mapping.items(), key=lambda kv: -len(kv[0]))
    for tag, val in items:
        text = text.replace(tag, val)
    return text


def _build_arg_parser() -> "argparse.ArgumentParser":
    p = argparse.ArgumentParser(description="Anonymiseur de prompts réversible (regex + HMAC).")
    sub = p.add_subparsers(dest="cmd", required=True)

    # genkey
    g = sub.add_parser("genkey", help="Génère une clé secrète (32 bytes, base64).")
    g.set_defaults(func=cmd_genkey)

    # anon
    a = sub.add_parser("anon", help="Anonymise un texte.")
    a.add_argument("--in", dest="infile", required=True, help="Fichier d'entrée ou '-' pour stdin.")
    a.add_argument("--mapping", help="Chemin du fichier mapping (JSON) à écrire.")
    a.add_argument("--include", help="Types à inclure (liste séparée par des virgules).")
    a.add_argument("--exclude", help="Types à exclure (liste séparée par des virgules).")
    a.add_argument("--mode", choices=["placeholder","redact"], default="placeholder",
                   help="placeholder: tags {{TYPE_hash}}; redact: tags + masque court lisible.")
    a.add_argument("--secret", help="Clé secrète en clair ou en base64.")
    a.add_argument("--secret-file", help="Fichier contenant la clé secrète (binaire ou base64).")
    a.set_defaults(func=cmd_anon)

    # deanon
    d = sub.add_parser("deanon", help="Désanonymise un texte avec un mapping existant.")
    d.add_argument("--in", dest="infile", required=True, help="Fichier d'entrée ou '-' pour stdin.")
    d.add_argument("--mapping", required=True, help="Chemin du mapping JSON (avec MAC).")
    d.add_argument("--secret", help="Clé secrète en clair ou en base64.")
    d.add_argument("--secret-file", help="Fichier contenant la clé secrète.")
    d.set_defaults(func=cmd_deanon)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())