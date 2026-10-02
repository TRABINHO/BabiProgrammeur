# BabiProgrammeur 🧬

Application mobile de suivi d'activité de programmation, écrite en **Python** avec
**Kivy / KivyMD**. Elle chronomètre tes sessions de code, calcule des statistiques,
suit des objectifs et t'enregistre un historique exportable — le tout **100 % local**,
sans serveur ni compte. Un onglet **Formation** propose des parcours de cours et
d'exercices pré-définis pour 15 langages, avec progression cochable, fiches de
contenu détaillé et courbe d'évolution ; un onglet **Correction** donne la
solution commentée de chacun des 105 exercices.

## Fonctionnalités

| Onglet | Ce qu'il fait |
|---|---|
| **Chronomètre** | Démarre / met en pause / arrête une session de code (projet, langage, notes). Affiche le temps en cours en direct. |
| **Statistiques** | Temps du jour / de la semaine, série de jours consécutifs, meilleure journée, répartition par langage et par projet, graphique des 14 derniers jours, courbe d'évolution de la formation. |
| **Formation** | Parcours de cours + exercices pré-définis pour 15 langages (8 cours, 7 exercices par langage) : cases à cocher, progression par langage, derniers jalons datés. Un bouton **« Lire »** sur chaque ligne ouvre la fiche plein écran (objectifs, points clés, exemple / énoncé, étapes, indice). **La fiche doit être ouverte une fois avant de pouvoir cocher la ligne** : tant qu'elle ne l'est pas, la pastille « Lire » est pleine (résumé en bleu) et l'appui sur la ligne ouvre la fiche au lieu de cocher. La fiche d'exercice embarque un espace **« Mon essai »** (brouillon enregistré automatiquement dans `data.json`, pré-rempli à la prochaine ouverture) et un bouton **« Voir la correction »** qui ouvre la solution commentée par-dessus. |
| **Correction** | Solution commentée des **105 exercices** (7 par langage), choisie par puce de langage. Un appui sur une ligne ouvre la correction plein écran : **SOLUTION** (code complet commenté), **EXPLICATION** (le raisonnement), **POINTS DE VÉRIFICATION** (sorties attendues et cas limites), **POUR ALLER PLUS LOIN**. Lecture seule : aucune incidence sur la progression. |
| **Objectifs** | Objectif quotidien et hebdomadaire (minutes), jauge de progression du jour, rappels programmés (notifications). |
| **Historique & export** | Liste des sessions (filtre par jour), suppression, export **CSV** ou **JSON** d'un clic. |

- **Stockage local uniquement** : tout est dans un simple fichier `data.json`.
- **Thème sombre** personnalisé, interface en français, format mobile (390 × 760).
- **Couleur unique par langage** : chaque langage a sa propre teinte (puces de
  sélection, barres de progression et de répartition) — aucun doublon sur les
  15 langages, pour les distinguer d'un coup d'œil pendant la sélection.
- **Logo « Babi Programmez »** utilisé comme icône de l'application : barre de
  titre / barre des tâches en desktop, icône du lanceur sur Android
  (`assets/icon.png` : le logo complet `Babi_programmez.jpeg` encadré sur un
  carré 256 × 256).
- **Écran d'accueil animé** : au démarrage, le logo au centre (pulsation douce
  sur plaque sombre) au-dessus d'une pluie de nombres binaires verts, puis
  fondu de sortie d'environ 1,6 s — inerte au toucher. Sur Android, le splash
  du système affiche aussi le logo de l'application (`assets/presplash.png`)
  au lieu du logo Kivy. Désactivable avec la variable `BABI_SPLASH=0`.
- **Aucune permission** requise sur Android (hors notifications pour les rappels).

## Téléchargement (Android)

- **APK de release signé** : [Releases du dépôt](https://github.com/TRABINHO/BabiProgrammeur/releases/latest)
  (`babiprogrammeur-1.0.0-arm64-v8a-release.apk`, arm64-v8a, Android 5.0+).
  Télécharger puis ouvrir le fichier ; autoriser l'installation des sources
  inconnues si le système le demande. Signature de release `CN=BabiProgrammeur`
  (empreinte SHA-256 `e08dcf06…`) — elle remplace l'APK de debug, qui devra donc
  être désinstallé avant la première installation.
- **Politique de confidentialité** : <https://trabinho.github.io/BabiProgrammeur/privacy.html>
  (application 100 % locale, aucune donnée collectée, seule permission :
  notifications locales).

## Installation (desktop)

```bash
pip install -r requirements.txt
python main.py
```

Options de démarrage (utilitaires de test) :

```bash
python main.py --demo              # injecte des données de démonstration
python main.py --tab stats         # ouvre directement un onglet (timer|stats|learn|corrections|goals|history)
```

## Tests

```bash
python tests/smoke.py        # tests fonctionnels (chronomètre, stats, formation, lecture obligatoire avant coche, brouillons « Mon essai », corrections, fiches, objectifs, export, dialogues)
python tests/check_layout.py # vérifie l'absence de débordements sur les 6 écrans
python tests/check_content.py # couverture des fiches de formation (cours + exercices)
python tests/check_solutions.py # couverture + qualité des corrections (105 exercices)
```

Autres outils de test : `tests/shot_splash.py` (cycle de vie complet de
l'écran d'accueil : capture en pleine animation, puis retrait après le fondu),
`tests/capture.py` (capture d'écran du framebuffer,
avec `--dialog` / `--fiche` pour les fenêtres modales et `--seed` pour des
données de démo dans un fichier temporaire),
`tests/probe_learn.py` (appui réel sur l'onglet Formation : la fiche non lue
bloque la coche, l'ouverture la débloque),
`tests/probe_scroll_pos.py` (un rafraîchissement ne doit pas déplacer les listes),
`tests/probe_realinput.py` / `probe_scroll.py` / `probe_overscroll.py`
(entrées réelles, défilement, molette), `tests/debug_layout.py` (inspection
détaillée des widgets).

## Où sont les données ?

Le fichier `data.json` est créé automatiquement au premier lancement :

| Système | Emplacement |
|---|---|
| Windows | `%APPDATA%\BabiProgrammeur\data.json` |
| Linux | `~/.babiprogrammeur/data.json` |
| macOS | `~/Library/Application Support/BabiProgrammeur/data.json` |

Les exports CSV/JSON sont écrits dans le dossier `Documents` (sinon `~`).
L'écriture est **atomique** (fichier temporaire puis remplacement) : pas de
perte de données si l'application est fermée pendant une sauvegarde.

## Construire l'APK Android

La compilation Android se fait sous **Linux** (WSL convient) avec [Buildozer](https://buildozer.readthedocs.io) :

```bash
# 1. Installer Buildozer (une fois)
sudo apt update && sudo apt install -y python3-pip git zip unzip
pip install --user buildozer cython2

# 2. Dépendances natives de Kivy
sudo apt install -y build-essential libsqlite3-dev sqlite3 \
    cmake zlib1g-dev libffi-dev libssl-dev

# 3. Compiler (première compilation : ~20 à 40 min)
cd "BabiProgrammeur"
buildozer android debug

# 4. Installer sur un appareil branché en USB (mode débogage activé)
buildozer android debug deploy run logcat
```

L'APK se trouve ensuite dans `bin/`. Le fichier `buildozer.spec` est déjà configuré
(nom `BabiProgrammeur`, portrait, API 33, exclusion des `tests/`, icône
`assets/icon.png` : logo `Babi_programmez.jpeg` complet sur fond carré).

> Note : la première compilation télécharge l'SDK + NDK d'Android (~5 Go).
> Sous Windows, exécutez Buildozer dans **WSL2** (Ubuntu).

## Structure du projet

```
main.py              # entrée : chrome, navigation, minuteurs, rappels
assets/
  icon.png           # icône 256×256 : logo complet encadré (Babi_programmez.jpeg)
core/
  models.py          # modèle Session
  storage.py         # SessionStore : chargement/sauvegarde JSON atomique
  curriculum.py      # parcours de formation (15 langages, cours + exercices)
  content.py         # accès aux fiches détaillées (fusion des lots ci-dessous)
  content_1 … _5.py  # contenu rédigé des cours et exercices (215 fiches)
  solutions.py       # accès aux corrections (fusion des lots ci-dessous)
  solutions_1 … _5.py # corrections commentées des 105 exercices
  stats.py           # agrégats, séries, séries de jours, formatage
  export.py          # export CSV / JSON
  notify.py          # rappels (plyer)
  seed.py            # données de démonstration
ui/
  colors.py          # palette thème sombre
  widgets.py         # cartes, graphiques (barres, courbe), jauges, lignes à cocher / à ouvrir
  dialogs.py         # dialogues modaux + fiche plein écran (« Lire »)
  screens.py         # les 6 écrans
tests/               # suite de tests et outillage
```

## Licence

Projet personnel — libre d'usage et d'adaptation.
