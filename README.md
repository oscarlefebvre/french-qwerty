# french-qwerty

Écrire en français avec ses accents sur un clavier QWERTY, sans y penser.

Vous tapez `probleme`, `deja`, `etait` ; macOS écrit **problème**, **déjà**, **était**.
Pas de disposition de clavier à apprendre, pas de touche morte : ce dépôt est une
liste de mots à importer dans les *remplacements de texte* de macOS.

## Installation (Mac)

1. Téléchargez [`french-qwerty.plist`](french-qwerty.plist) (bouton de téléchargement en haut à droite de la page du fichier).
2. Ouvrez **Réglages Système → Clavier → Saisie de texte → Remplacements de texte…**
3. Glissez le fichier `.plist` dans la liste qui s'affiche.

Les remplacements se synchronisent avec iCloud : ils arrivent aussi sur votre iPhone
et votre iPad.

Pour mettre à jour, refaites la même chose avec le nouveau fichier. Pour retirer un
mot, sélectionnez-le dans la liste et cliquez sur **−**.

> Dans certaines apps, il faut activer **Édition → Substitutions → Remplacement de texte**.

## Les règles

La liste doit pouvoir être installée les yeux fermés, y compris par quelqu'un qui écrit
aussi en anglais. Un mot n'entre que s'il respecte les trois règles :

1. **Sans accent, il n'existe pas en anglais.**
   `selection` → sélection est refusé : il casserait « selection » dans un texte anglais.
2. **Sans accent, il n'existe pas en français.**
   `foret` → forêt est refusé : un foret est aussi un outil.
3. **Il n'a qu'une seule forme accentuée courante.**
   `ameliore` est refusé : impossible de savoir si vous vouliez « améliore » ou « amélioré ».
   C'est pour cela que la liste contient surtout des noms, des adverbes et des infinitifs,
   et très peu de verbes conjugués.

Une forme concurrente très rare (« maniéré » face à « manière ») ne bloque pas un mot
courant ; cela se discute au cas par cas.

Les mots refusés sont conservés dans [`exclus.txt`](exclus.txt) avec leur raison, pour
ne pas refaire le débat.

## Proposer un mot

**Sans rien installer** : [ouvrez une issue « Proposer un mot »](../../issues/new?template=proposer-un-mot.yml).

**Ou directement** : modifiez [`mots.txt`](mots.txt) depuis GitHub (icône crayon) et
ajoutez votre mot, **avec ses accents**, à sa place alphabétique. Une ligne, un mot :

```
problème
```

C'est tout : le raccourci sans accent (`probleme`) est déduit automatiquement, et le
fichier `.plist` est régénéré après la fusion. Ne le modifiez pas à la main.

Chaque proposition est vérifiée automatiquement (doublons, ordre, mots exclus). Les
règles 1 à 3 sont vérifiées par un humain : dites-le dans votre proposition si vous
avez un doute.

Pour vérifier en local :

```bash
python3 scripts/build.py
```

Sur Mac, le script signale aussi les mots qui semblent exister en anglais.

## Licence

[MIT](LICENSE)
