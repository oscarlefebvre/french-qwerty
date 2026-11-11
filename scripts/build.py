#!/usr/bin/env python3
"""Valide mots.txt et génère french-qwerty.plist (remplacements de texte macOS).

    python3 scripts/build.py           valide puis génère le .plist
    python3 scripts/build.py --check   valide seulement
"""
import plistlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOTS = ROOT / "mots.txt"
EXCLUS = ROOT / "exclus.txt"
PLIST = ROOT / "french-qwerty.plist"
DICO_ANGLAIS = Path("/usr/share/dict/words")  # présent sur macOS


def raccourci(mot):
    """« Déjà » -> « deja » : ce que l'on tape sur un clavier QWERTY."""
    mot = mot.lower().replace("œ", "oe").replace("æ", "ae")
    decompose = unicodedata.normalize("NFD", mot)
    return "".join(c for c in decompose if not unicodedata.combining(c))


def lire(chemin):
    """Renvoie [(numéro de ligne, mot)] sans les commentaires ni les lignes vides."""
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    for numero, ligne in enumerate(lignes, 1):
        mot = ligne.split("#", 1)[0].strip()
        if mot:
            yield numero, unicodedata.normalize("NFC", mot)


def valider():
    exclus = {raccourci(mot) for _, mot in lire(EXCLUS)}
    anglais = set()
    if DICO_ANGLAIS.exists():
        anglais = {m.lower() for m in DICO_ANGLAIS.read_text().split()}

    erreurs, avertissements, entrees = [], [], []
    vus = {}
    precedent = ""
    for numero, mot in lire(MOTS):
        court = raccourci(mot)
        ou = f"mots.txt:{numero} « {mot} »"
        if not re.fullmatch(r"[a-z]+", court):
            erreurs.append(f"{ou} : un seul mot, lettres uniquement")
            continue
        if court == mot:
            erreurs.append(f"{ou} : le mot n'a pas d'accent, rien à remplacer")
        if court in exclus:
            erreurs.append(f"{ou} : « {court} » est dans exclus.txt (la raison y figure)")
        if court in vus:
            erreurs.append(
                f"{ou} : même raccourci « {court} » que « {vus[court]} » "
                "(doublon, ou mot à plusieurs formes accentuées)"
            )
        if court < precedent:
            erreurs.append(f"{ou} : à placer avant « {precedent} » (ordre alphabétique)")
        if court in anglais:
            avertissements.append(f"{ou} : « {court} » semble exister en anglais, à vérifier")
        vus.setdefault(court, mot)
        precedent = max(precedent, court)
        entrees.append({"phrase": mot, "shortcut": court})
    return entrees, erreurs, avertissements


def main():
    entrees, erreurs, avertissements = valider()
    for message in avertissements:
        print(f"attention : {message}")
    for message in erreurs:
        print(f"erreur : {message}")
    if erreurs:
        return 1
    if "--check" not in sys.argv:
        with PLIST.open("wb") as fichier:
            plistlib.dump(entrees, fichier)
        print(f"{PLIST.name} généré")
    print(f"{len(entrees)} mots valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
