[app]

# (str) Nom de l'application
title = BabiProgrammeur

# (str) Nom du package
package.name = babiprogrammeur

# (str) Nom du package sous Android (peut contenir un point)
package.domain = org.babiprogrammeur

# (str) Source où se trouve le main.py
source.dir = .

# (str) Nom du module d'entrée
source.main = main.py

# (list) Fichiers et dossiers à inclure en plus du source
source.include.exts = py,png,jpg,kv,atlas,json,ttf

# (list) Modules à exclure
source.exclude.patterns = .git*,__pycache__,tests/*,*.corrupt

# (str) Application versioning (versionCode 100000 + version)
version = 1.0.0

# (str) Niveau de support
requirements = python3,kivy==2.3.1,kivymd==1.2.0,plyer,pillow

# (list) Architectures cibles : arm64-v8a seule (téléphones récents, build plus léger)
android.archs = arm64-v8a

# (str) Orientation : portrait, landscape ou all
orientation = portrait

# (bool) L'application est-elle adaptée aux écrans tactile ?
fullscreen = 0

# (list) Permissions : notifications pour les rappels (obligatoire sur Android 13+)
android.permissions = POST_NOTIFICATIONS

# (str) Android minimum API level
android.minapi = 21

# (str) Android SDK cible / compilateur
android.api = 33
android.ndk = 25b

# (bool) Utiliser du code optimisé
android.arm64_pie = True

# (str) Indicateur d'application (logo Babi Programmez, 256x256)
icon.filename = %(source.dir)s/assets/icon.png

# (str) Splash de démarrage (logo centré sur fond sombre — remplace le Kivy)
presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Format de l'écran
# orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
