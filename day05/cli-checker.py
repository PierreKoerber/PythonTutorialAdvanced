

from myparser import check_url

# Exemple d’usage
urls = [
    "https://www.eca-vaud.ch",
    "https://www.eca-vaud.ch/particuliers",
    "https://www.eca-vaud.ch/faq"
]

for u in urls:
    print(u, "OK" if check_url(u) else "NOT OK")
