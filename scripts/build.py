#!/usr/bin/env python3
"""Valide les listes de mots et génère les .plist (remplacements de texte macOS).

    python3 scripts/build.py           valide puis génère les .plist
    python3 scripts/build.py --check   valide seulement
"""
import plistlib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUS = ROOT / "exclus.txt"
DICO_ANGLAIS = Path("/usr/share/dict/words")  # présent sur macOS

# (liste de mots, .plist généré, signaler les mots qui existent en anglais ?)
LISTES = [
    ("mots.txt", "french-qwerty.plist", True),
    ("mots-optionnels.txt", "french-qwerty-optionnel.plist", False),
]


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


def valider(nom, vus, exclus, anglais):
    """`vus` (raccourci -> « mot » (fichier)) est partagé entre les listes."""
    erreurs, avertissements, entrees = [], [], []
    precedent = ""
    for numero, mot in lire(ROOT / nom):
        court = raccourci(mot)
        ou = f"{nom}:{numero} « {mot} »"
        if not re.fullmatch(r"[a-z]+", court):
            erreurs.append(f"{ou} : un seul mot, lettres uniquement")
            continue
        if court == mot:
            erreurs.append(f"{ou} : le mot n'a pas d'accent, rien à remplacer")
        if court in exclus:
            erreurs.append(f"{ou} : « {court} » est dans exclus.txt (la raison y figure)")
        if court in vus:
            erreurs.append(
                f"{ou} : même raccourci « {court} » que {vus[court]} "
                "(doublon, ou mot à plusieurs formes accentuées)"
            )
        if court < precedent:
            erreurs.append(f"{ou} : à placer avant « {precedent} » (ordre alphabétique)")
        if court in anglais:
            avertissements.append(
                f"{ou} : « {court} » semble exister en anglais, "
                "à vérifier (sa place est peut-être dans mots-optionnels.txt)"
            )
        vus.setdefault(court, f"« {mot} » ({nom})")
        precedent = max(precedent, court)
        entrees.append({"phrase": mot, "shortcut": court})
    return entrees, erreurs, avertissements


def main():
    exclus = {raccourci(mot) for _, mot in lire(EXCLUS)}
    anglais = set()
    if DICO_ANGLAIS.exists():
        anglais = {m.lower() for m in DICO_ANGLAIS.read_text().split()}

    vus, resultats, erreurs = {}, [], []
    for nom, plist, verifier_anglais in LISTES:
        entrees, err, avertissements = valider(
            nom, vus, exclus, anglais if verifier_anglais else set()
        )
        for message in avertissements:
            print(f"attention : {message}")
        erreurs += err
        resultats.append((nom, plist, entrees))

    for message in erreurs:
        print(f"erreur : {message}")
    if erreurs:
        return 1
    for nom, plist, entrees in resultats:
        if "--check" not in sys.argv:
            with (ROOT / plist).open("wb") as fichier:
                plistlib.dump(entrees, fichier)
        print(f"{nom} : {len(entrees)} mots valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
