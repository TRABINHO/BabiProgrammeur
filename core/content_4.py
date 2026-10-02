"""Fiches de contenu — lot 4 : HTML/CSS, PHP, Swift."""
from __future__ import annotations

CONTENT = {
    "HTML/CSS": {
        "lessons": {
            "Structure HTML": """OBJECTIFS
- écrire le squelette d'une page HTML5 valide
- comprendre le DOM et la sémantique des balises
- relier une feuille de style et un script à la page

POINTS CLÉS
- <!DOCTYPE html> déclenche le mode standard, sans lui le rendu dérive
- <html lang="fr"> guide lecteurs d'écran et traduction
- head : meta, title, link ; body : tout ce qui s'affiche à l'écran
- balises sémantiques : header, nav, main, section, article, footer
- <link rel="stylesheet" href="style.css"> pour le CSS, <script src="app.js"> pour le JS
- attributs : class (styler plusieurs éléments), id (cible unique), alt, lang

EXEMPLE
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Ma page</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header><h1>Bienvenue</h1></header>
    <main><section id="intro"><p>Contenu principal.</p></section></main>
    <footer><p>Pied de page</p></footer>
  </body>
</html>

EN PRATIQUE
Une page se lit comme un arbre : html contient head et body, body ses
sections. Navigateurs et lecteurs d'écran s'appuient sur cette structure.

PIÈGES À ÉVITER
- une balise oubliée ferme parfois tout le bloc suivant
- plusieurs h1 par page brouillent la hiérarchie des titres
- oublier charset="utf-8" casse les accents

À RETENIR
- head décrit la page, body la montre.
- la sémantique ne coûte rien et se relit mieux.
""",
            "Texte et liens": """OBJECTIFS
- structurer le texte avec une hiérarchie de titres claire
- créer des liens internes et externes sûrs
- intégrer des images réellement accessibles

POINTS CLÉS
- h1 à h6 hiérarchisent ; un seul h1 par page, sans sauter de niveau
- target="_blank" s'accompagne toujours de rel="noopener"
- href accepte une URL, un chemin relatif (page.html) ou une ancre (#section)
- img exige alt : description pour les lecteurs d'écran et si l'image manque
- ul (puces), ol (numérotée), li (chaque élément)
- strong insiste, em accentue le sens

EXEMPLE
<h1>Titre de la page</h1>
<h2>Sous-titre</h2>
<p>Un <a href="https://example.com" target="_blank" rel="noopener">lien</a> utile.</p>
<img src="photo.jpg" alt="Description de la photo" width="600" height="400">
<ul>
  <li>Premier point</li>
  <li>Second point</li>
</ul>

EN PRATIQUE
Dans un article, le titre principal porte le h1 et chaque section un h2.
Les liens internes restent relatifs : le site fonctionne alors quel que
soit le dossier d'hébergement choisi.

PIÈGES À ÉVITER
- une balise <a> sans href ne se clique pas
- « image » ou le nom du fichier dans alt : décrivez la scène
- des div partout à la place des titres rendent la page illisible pour un logiciel

À RETENIR
- les titres forment un plan, pas simplement de la taille.
- alt et href sont les deux attributs les plus lus du web.
""",
            "Images et médias": """OBJECTIFS
- afficher des images, de l'audio et de la vidéo
- choisir le bon format et alléger les fichiers
- servir la bonne taille avec srcset et le lazy loading

POINTS CLÉS
- formats : PNG (aplats nets), JPG (photo), SVG (vectoriel), WebP (léger)
- width et height déclarent la taille : plus de saut de mise en page
- <picture> propose plusieurs sources au navigateur
- srcset + sizes sélectionne l'image selon la largeur de l'écran
- loading="lazy" diffère le chargement des images hors écran
- alt décrit l'image ; alt vide est réservé au décoratif
- <video controls> et <audio controls> lisent les médias sans lecteur imposé

EXEMPLE
<img src="chat-800.webp"
     srcset="chat-400.webp 400w, chat-800.webp 800w"
     alt="Un chat roux endormi sur un canapé"
     width="800" height="533" loading="lazy">
<video controls>
  <source src="film.mp4" type="video/mp4">
</video>

EN PRATIQUE
Une page d'accueil pèse souvent plus de 2 Mo, dont l'essentiel en images.
Passer en WebP et activer le lazy loading divise ce poids par trois.

PIÈGES À ÉVITER
- sans width et height, le texte saute quand l'image arrive
- trop agrandir, l'image devient floue : prévoyez sa taille d'affichage
- un alt générique ralentit la lecture vocale : soyez précis et court

À RETENIR
- compresser les images reste le gain de performance n°1 d'une page.
- servir la bonne taille au bon écran, c'est le vrai responsive.
""",
            "Formulaires": """OBJECTIFS
- créer des champs et les associer à des labels
- valider côté navigateur avant tout serveur
- soumettre et récupérer les données côté PHP

POINTS CLÉS
- label for="champ" rend le clic plus large et lie le texte au champ
- types : text, email, number, date, checkbox, radio, password, textarea
- required, min, max, minlength, pattern : validation native du navigateur
- name décide de la clé reçue côté serveur ; sans name, rien n'est envoyé
- fieldset et legend regroupent les champs liés
- method="post" pour les données sensibles, get pour une recherche simple

EXEMPLE
<form action="/envoi" method="post">
  <fieldset>
    <legend>Vos coordonnées</legend>
    <label for="mail">E-mail</label>
    <input id="mail" name="mail" type="email" required>
    <label for="msg">Message</label>
    <textarea id="msg" name="msg" minlength="10" rows="5"></textarea>
    <button type="submit">Envoyer</button>
  </fieldset>
</form>

EN PRATIQUE
Un formulaire se valide d'abord dans le navigateur : l'utilisateur
corrige sans attendre de requête. Le serveur revalide tout ensuite.

PIÈGES À ÉVITER
- un champ sans name n'apparaît jamais dans $_POST
- valider uniquement en JavaScript : on peut désactiver le script
- oublier l'attribut for : le clic sur le libellé ne marche plus

À RETENIR
- name des champs = clés reçues côté serveur.
- la validation native coûte zéro ligne de JavaScript.
""",
            "Sélecteurs et cascade": """OBJECTIFS
- cibler des éléments avec précision
- comprendre la cascade et la spécificité
- organiser une feuille de style qui reste lisible

POINTS CLÉS
- sélecteurs : .classe, #id, div > p, p.suite, :hover, ::before, [type="email"]
- spécificité : style inline, puis id, puis classe, puis balise
- ordre de priorité : feuille navigateur, feuille du site, style inline
- les virgules appliquent une règle à plusieurs cibles
- privilégiez les classes réutilisables : un id ne s'utilise qu'une fois
- hériter les couleurs et polices évite de répéter les mêmes déclarations

EXEMPLE
.nav a { color: #999; text-decoration: none; }
.nav a:hover { color: #fff; }
.nav a:focus-visible { outline: 2px solid #0af; }
.nav .actif { border-bottom: 2px solid #0af; }
.nav .actif, .nav li + li { margin-left: 12px; }

EN PRATIQUE
Une feuille se divise en couches : couleurs et typographie globales,
composants réutilisables, puis réglages de page. La barre de navigation
d'un site utilise presque toujours .actif pour marquer la page courante.

PIÈGES À ÉVITER
- styler par id puis chercher à le surcharger : la spécificité vous bat
- !important partout : empilez des sélecteurs cohérents à la place
- une faute de nom de classe reste silencieuse : rien ne s'applique

À RETENIR
- la cascade tranche les conflits, la spécificité pèse dans la balance.
- classes pour le style, id pour cibler et lier.
""",
            "Flexbox": """OBJECTIFS
- aligner des éléments en une dimension avec display: flex
- répartir l'espace disponible (justify-content, align-items)
- gérer le retour à la ligne et la réduction des enfants

POINTS CLÉS
- justify-content place les éléments sur l'axe principal (row par défaut)
- align-items les place sur l'axe transversal (colonne pour row)
- flex: 1 fait occuper l'espace restant, flex: 0 0 200px fige la largeur
- gap ajoute un espacement régulier, sans marges collées
- flex-wrap: wrap autorise le passage à la ligne
- flex-direction: column empile verticalement ; order réordonne visuellement
- min-width: 0 évite qu'un enfant déborde de son conteneur

EXEMPLE
.bandeau {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.bandeau .logo { flex: 0 0 auto; }
.bandeau nav { flex: 1 1 320px; }

EN PRATIQUE
Barre d'en-tête, pied de page, barre d'outils et cartes en ligne passent
par Flexbox : on décide d'un axe, on répartit avec justify, on centre
avec align. Le retour à la ligne assure le passage en dessous de 700 px.

PIÈGES À ÉVITER
- sans flex-wrap, tout déborde sur un petit écran
- oublier gap : les marges s'additionnent
- un enfant trop large refuse de rétrécir : ajoutez min-width: 0

À RETENIR
- Flexbox pour une ligne ou une colonne, Grid pour le quadrillage.
- justify aligne l'axe principal, align items l'autre axe.
""",
            "Grid": """OBJECTIFS
- construire des mises en page en deux dimensions
- définir colonnes, lignes et zones
- adapter avec les unités modernes

POINTS CLÉS
- display: grid sur le conteneur : les enfants deviennent des cellules
- grid-template-columns: repeat(3, 1fr) ; 1fr partage l'espace disponible
- gap crée les gouttières, sans marges à cumuler
- grid-column et grid-row étalent un élément sur plusieurs cellules
- grid-template-areas nomme des zones lues comme un dessin
- minmax(280px, 1fr) garantit une largeur minimale à chaque cellule
- auto-fill place autant de colonnes que la place le permet

EXEMPLE
.grille {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.carte-large { grid-column: span 2; }
.entete { grid-area: entete; }

EN PRATIQUE
Catalogue, galerie et tableau de bord se construisent en Grid : on
déclare les colonnes une fois et le navigateur répartit les cellules. Les
zones nommées rendent la mise en page lisible dans le fichier CSS.

PIÈGES À ÉVITER
- oublier display: grid : les enfants gardent leur mise en page normale
- cumuler gap et marges : l'espacement devient irrégulier
- une cellule trop large déborde : pensez à min-width: 0

À RETENIR
- auto-fill + minmax = grille responsive sans media query.
- Grid pilote les deux axes, Flexbox n'en pilote qu'un.
""",
            "Responsive": """OBJECTIFS
- adapter l'affichage aux tailles d'écran
- utiliser viewport et media queries
- concevoir mobile d'abord

POINTS CLÉS
- <meta name="viewport" content="width=device-width, initial-scale=1"> obligatoire
- @media (max-width: 700px) { ... } applique un style sous 700 px
- partir du petit écran : min-width pour ajouter des colonnes en grand
- images fluides : max-width: 100% et height: auto
- unités relatives : rem pour le texte, % pour les largeurs, vh et vw pour l'écran
- (hover: hover) n'active le survol que sur les appareils souris
- tester 360, 768 et 1440 px couvre l'essentiel du parc public

EXEMPLE
img { max-width: 100%; height: auto; }
.grille {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
@media (max-width: 700px) {
  .grille { grid-template-columns: 1fr; }
}

EN PRATIQUE
La majorité des visites arrive d'un téléphone : on dessine d'abord la
version étroite, puis on ajoute des colonnes quand la place grandit. Un
seul bloc de styles suffit souvent, sans multiplier les media queries.

PIÈGES À ÉVITER
- oublier la balise viewport : le mobile affiche une page large réduite
- une largeur fixe en px casse la mise en page sur petit écran
- des media queries placées sans ordre cohérent se contredisent

À RETENIR
- la balise viewport conditionne tout le responsive.
- tester tôt sur un vrai petit écran reste le meilleur réflexe.
""",
        },
        "exercises": {
            "Page CV": """ÉNONCÉ
- Vous réalisez une page de CV en HTML pur, sans aucune mise en forme CSS :
  en-tête avec photo et coordonnées, expériences, compétences, formation.
- La page doit rester lisible sans style et compréhensible par un lecteur d'écran.

ÉTAPES
1. Créer le squelette HTML5 : header, main, footer, lang="fr", charset utf-8.
2. Dans le header, placer un h1 avec le nom, une photo et une liste de contacts.
3. Créer les sections expériences, compétences et formation, chacune avec son h2.
4. Détailler avec des listes ul ou ol et des paragraphes datés.
5. Ajouter alt à la photo, puis passer la page dans le validateur W3C.

RÉSULTAT ATTENDU
- Une page structurée en header, main et footer, lisible sans aucune règle CSS.
- Un seul h1 portant le nom, puis exactement un h2 par section.
- Une liste de contacts d'au moins trois éléments.

POUR TESTER
- Désactiver la feuille de style : la page doit rester parfaitement lisible.
- Naviguer au clavier : la tabulation parcourt les liens dans l'ordre du document.
- Chercher un titre sauté (h1 puis h3) : il ne doit y en avoir aucun.

INDICE
- Construisez d'abord l'ossature vide, puis remplissez section par section :
  ajouter du contenu est plus simple que réparer une structure pleine.
""",
            "Menu responsive": """ÉNONCÉ
- Une barre de navigation s'affiche en ligne sur grand écran et s'enroule
  en colonne sous 700 px, avec la page courante clairement signalée.
- Le menu doit rester confortable au clavier comme au doigt.

ÉTAPES
1. Construire nav > ul > li > a avec au moins cinq liens.
2. Passer ul en display: flex, ajouter gap et retirer les puces.
3. Créer la classe .actif et la poser sur le lien de la page courante.
4. Écrire la media query (max-width: 700px) et y passer flex-direction: column.
5. Prévoir un état :focus-visible net, distinct de :hover.
6. Vérifier la largeur juste au-dessus et juste en dessous de 700 px.

RÉSULTAT ATTENDU
- Au-dessus de 700 px : cinq liens alignés sur une ligne, espacés régulièrement.
- En dessous : les mêmes liens empilés verticalement, pleine largeur.
- Le lien actif se distingue par une couleur ou un soulignement.

POUR TESTER
- Redimensionner de 800 à 600 px : la bascule doit se faire en un seul passage.
- Appuyer sur Tab : chaque lien montre un contour de focus bien visible.
- En colonne, vérifier qu'aucun libellé ne déborde de la fenêtre.

INDICE
- Écrivez d'abord le style grand écran, puis annulez-le dans la media query :
  deux mises en page à la fois sont plus difficiles à déboguer.
""",
            "Galerie en grille": """ÉNONCÉ
- Vous composez une galerie d'images responsive : le nombre de colonnes
  s'ajuste seul à la largeur disponible, l'espacement reste régulier et
  chaque image occupe toute sa cellule.

ÉTAPES
1. Créer un conteneur .galerie avec display: grid.
2. Définir grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)).
3. Poser gap: 16px sur le conteneur.
4. Écrire .galerie img { width: 100%; height: auto; } et fixer width et height.
5. Rédiger un alt différent pour chaque image.
6. Compter les colonnes à 400, 700 et 1200 px de large.

RÉSULTAT ATTENDU
- Vers 1200 px : quatre colonnes égales ; vers 700 px : deux ; vers 400 px : une.
- Des gouttières de 16 px identiques partout, sans marge superflue.
- Aucune image étirée : les proportions d'origine sont conservées.

POUR TESTER
- Déplacer lentement la fenêtre : les colonnes s'ajoutent ou disparaissent
  sans jamais laisser de trou dans la grille.
- Comparer deux images côte à côte : leurs hauteurs de ligne se calent.
- Désactiver le CSS : la liste des images reste visible dans l'ordre.

INDICE
- minmax fixe la largeur minimale d'une cellule et 1fr lui laisse le reste ;
  auto-fill répète cette colonne aussi souvent que la place le permet.
""",
            "Formulaire contact": """ÉNONCÉ
- Vous construisez un formulaire de contact : nom, e-mail, message long,
  case d'accord obligatoire. La saisie est validée par le navigateur,
  sans une seule ligne de JavaScript.

ÉTAPES
1. Regrouper les champs dans un fieldset avec un legend explicite.
2. Associer chaque champ à son label par for et id.
3. Utiliser type="email" et required sur l'e-mail, textarea pour le message.
4. Ajouter minlength sur le message et une checkbox required pour l'accord.
5. Placer un bouton submit dans un formulaire en method="post".
6. Tester chaque champ vide, puis chaque champ valide.

RÉSULTAT ATTENDU
- Envoyer avec un e-mail incomplet : le navigateur bloque et signale le champ.
- E-mail valide mais accord non coché : l'envoi reste bloqué.
- Tous les champs corrects : le formulaire se soumet normalement.

POUR TESTER
- Effacer le contenu de chaque champ un par un et essayer d'envoyer : à
  chaque fois, un message doit apparaître devant le coupable.
- Saisir « bidon » dans l'e-mail : le format doit être refusé.
- Vérifier après envoi que chaque champ porte bien un name distinct.

INDICE
- Le navigateur affiche déjà des messages clairs : déplacez-vous d'un champ
  à l'autre avec Tab et observez ce qu'il refuse, avant d'écrire du code.
""",
            "Carte produit": """ÉNONCÉ
- Vous créez une fiche produit (image, titre, prix, bouton d'achat) affichée
  sur deux colonnes en largeur et empilée en une seule colonne sous 600 px,
  avec une hauteur de carte constante d'un produit à l'autre.

ÉTAPES
1. Écrire la structure : article, puis img, puis une div pour le contenu.
2. En grand écran, passer le article en display: flex avec gap.
3. Fixer la largeur de l'image et laisser flex: 1 à la zone de texte.
4. Ajouter une media query (max-width: 600px) qui repasse en colonne.
5. Mettre le prix en gras et coller le bouton en bas avec margin-top: auto.
6. Contrôler le rendu à 601 px puis à 599 px de large.

RÉSULTAT ATTENDU
- À 700 px : image à gauche, texte à droite, bouton aligné tout en bas.
- À 450 px : image pleine largeur, puis titre, prix et bouton empilés.
- Deux cartes côte à côte affichent exactement la même hauteur.

POUR TESTER
- Réduire la fenêtre : le passage d'une colonne à deux doit rester net.
- Comparer deux cartes : prix et boutons doivent rester alignés.
- Vérifier que l'image ne déborde jamais de sa colonne.

INDICE
- margin-top: auto sur le bouton le pousse en bas de carte, et un article
  en flex aligne ses enfants : hauteur égale sans calcul de hauteur.
""",
            "Section hero": """ÉNONCÉ
- Vous réalisez un bloc d'accueil pleine largeur : titre, sous-titre et deux
  boutons d'action, sur un fond dégradé, centrés et adaptés au petit écran.

ÉTAPES
1. Créer section.hero avec min-height: 60vh et un padding intérieur.
2. Appliquer un fond avec linear-gradient(135deg, couleur1, couleur2).
3. Passer la section en display: flex, flex-direction: column.
4. Centrer avec justify-content: center et align-items: center, ajouter gap.
5. Regrouper les boutons dans une div en display: flex avec gap.
6. Empiler les boutons sous 480 px avec une media query.

RÉSULTAT ATTENDU
- Titre, sous-titre et boutons parfaitement centrés sur un écran de 800 px.
- Les deux boutons côte à côte en grand, empilés en petit écran.
- Le texte reste lisible sur toute la largeur du dégradé.

POUR TESTER
- Redresser la fenêtre de 1000 à 400 px : aucun élément ne doit se chevaucher.
- Mesurer : le bloc occupe environ six dixièmes de la hauteur d'écran.
- Sur petit écran, aucun défilement horizontal ne doit apparaître.

INDICE
- 60vh lie la hauteur à celle de l'écran sans forcer le défilement, et en
  flex colonne justify et align centrent sur les deux axes à la fois.
""",
            "Thème sombre": """ÉNONCÉ
- Vous mettez en place un thème clair et sombre piloté par des variables CSS
  et par la préférence système, avec un bouton de bascule manuel en plus.

ÉTAPES
1. Déclarer dans :root les variables --fond, --texte, --surface, --accent.
2. Remplacer toutes les couleurs en dur par var(--nom-de-variable).
3. Ajouter une media query prefers-color-scheme: dark qui redéfinit ces variables.
4. Prévoir une classe .sombre sur html pour imposer le choix manuel.
5. Ajouter une transition douce sur les couleurs de fond et de texte.
6. Créer le bouton qui bascule cette classe avec un petit script.

RÉSULTAT ATTENDU
- Page claire par défaut, qui s'assombrit seule quand le système est en sombre.
- Le bouton inverse le thème immédiatement, sans recharger la page.
- Aucune couleur hexadécimale en dehors du bloc :root.

POUR TESTER
- Changer le thème dans les réglages système : la page doit suivre sans action.
- Cliquer sur le bouton puis recharger : observez ce que vous décidez de garder.
- Chercher une couleur codée en dur hors de :root : il ne doit y en avoir aucune.

INDICE
- Une seule variable suffit à changer toute la page : si --fond change, tous
  les blocs qui utilisent var(--fond) suivent automatiquement.
""",
        },
    },
    "PHP": {
        "lessons": {
            "Syntaxe et variables": """OBJECTIFS
- écrire du code PHP entre <?php et ?>
- déclarer des variables, des constantes et des littéraux
- afficher et assembler du texte sans erreur

POINTS CLÉS
- toute variable commence par $ : $nom, $age ; les constantes non
- typage faible : 1 + "1" vaut 2, la chaîne est convertie en nombre
- concaténation avec le point, interpolation avec "$var" entre guillemets doubles
- chaîne nowdoc <<<'EOF' conserve le HTML brut sans interprétation
- define("TVA", 20) ou const TVA = 20 pour une valeur figée
- echo affiche, print_r et var_dump déboguent
- PHP s'exécute côté serveur : le navigateur ne reçoit jamais le code source

EXEMPLE
<?php
$nom = "Babi";
$age = 30;
$vip = true;
echo "Bonjour $nom, vous avez $age ans." . PHP_EOL;
echo "Âge dans 5 ans : " . ($age + 5) . PHP_EOL;
var_dump($age, $vip);          // int(30) bool(true)
?>

EN PRATIQUE
Chaque requête relit le fichier et repart de zéro : sessions et base de
données gardent ce qui doit durer. PHP et HTML se mélangent dans un même
fichier pour générer chaque page.

PIÈGES À ÉVITER
- oublier le $ devant une variable provoque une erreur de syntaxe
- « Bonjour » suivi de $nom sans point : erreur de syntaxe
- un fichier sans extension .php est renvoyé tel quel au navigateur

À RETENIR
- $ pour les variables, . pour assembler, echo pour afficher.
- le serveur exécute, le navigateur affiche seulement.
""",
            "Conditions et boucles": """OBJECTIFS
- structurer avec if / elseif / else
- boucler avec foreach, for et while
- comparer correctement avec === plutôt que ==

POINTS CLÉS
- == compare en convertissant les types, === compare valeur ET type
- foreach ($tab as $valeur) puis foreach ($tab as $cle => $valeur)
- for pour un compteur connu, while pour une condition ouverte
- switch exige break, sinon les cas suivants s'exécutent
- ternaire : $x ? "oui" : "non" pour une condition courte
- empty() teste une valeur vide, isset() teste une variable définie

EXEMPLE
$notes = ["Babi" => 15, "Zoé" => 8, "Ali" => 10];
foreach ($notes as $nom => $note) {
  if ($note >= 10) {
    echo "$nom : admis" . PHP_EOL;
  } elseif ($note >= 8) {
    echo "$nom : rattrapage" . PHP_EOL;
  } else {
    echo "$nom : ajourné" . PHP_EOL;
  }
}
for ($i = 1; $i <= 3; $i++) { echo "Essai $i" . PHP_EOL; }

EN PRATIQUE
Un panier, une liste d'articles ou un tableau de résultats se parcourt en
foreach. Les conditions trient ensuite, affichent un message adapté ou
bloquent une opération interdite.

PIÈGES À ÉVITER
- == contre === : « 0 » == false vaut vrai, ce surprend à chaque fois
- un foreach sur une variable non tableau lève un avertissement
- oublier break dans un switch fait fuiter les cas suivants

À RETENIR
- foreach est la boucle la plus sûre sur les tableaux PHP.
- pour comparer sérieusement, utilisez toujours ===.
""",
            "Tableaux": """OBJECTIFS
- créer des tableaux indexés et associatifs
- parcourir, trier, filtrer et combiner
- échanger des données en JSON

POINTS CLÉS
- [1, 2, 3] est indexé (clés 0, 1, 2), ["nom" => "Babi"] est associatif
- count() compte, array_push() ajoute, array_key_exists() vérifie une clé
- array_keys et array_values isolent les clés ou les valeurs
- sort trie par valeur, asort conserve les clés associatives
- array_column extrait une colonne, array_merge fusionne
- json_encode transforme en JSON, json_decode revient en tableau PHP
- une clé absente lève un avertissement : testez isset() ou ?? 0

EXEMPLE
$produits = [
  ["nom" => "Clavier", "prix" => 49.9],
  ["nom" => "Souris", "prix" => 19.9],
];
$noms = array_column($produits, "nom");      // ["Clavier", "Souris"]
$total = array_sum(array_column($produits, "prix"));
$flux = json_encode($produits, JSON_UNESCAPED_UNICODE);

EN PRATIQUE
Les données arrivent en JSON depuis une API et repartent ainsi vers une
application mobile. Le tableau associatif porte aussi bien une ligne de
base de données qu'une configuration complète.

PIÈGES À ÉVITER
- $tab["inexistant"] sans test crée un avertissement en PHP 8
- sort() perd les clés associatives : utilisez asort()
- confondre [] et array() : les crochets suffisent

À RETENIR
- clé => valeur : c'est le schéma dominant du PHP moderne.
- encodez en JSON pour échanger, décodez pour exploiter.
""",
            "Fonctions": """OBJECTIFS
- définir des fonctions et des paramètres typés
- utiliser les paramètres par défaut
- comprendre la portée des variables

POINTS CLÉS
- function f(int $a, string $b = "x"): string { ... }
- la signature devient un contrat vérifié à l'exécution
- fonction fléchée : fn($x) => $x * 2, elle capture le contexte
- return renvoie une valeur et arrête immédiatement la fonction
- une variable créée dans la fonction y reste : global $x pour la partager
- func_get_args() reçoit les arguments non déclarés

EXEMPLE
$double = fn($n) => $n * 2;
echo $double(21);                    // 42

function moyenne(array $n): float {
  if (empty($n)) { return 0.0; }
  return array_sum($n) / count($n);
}
echo moyenne([12, 15, 9]);           // 12.0
echo moyenne([]);                    // 0.0

EN PRATIQUE
Une fonction fait une chose et le dit par son nom : valider un e-mail,
formater un prix, préparer une requête. Les projets rangent ces fonctions
dans des fichiers inclus plutôt que de les recopier.

PIÈGES À ÉVITER
- oublier return : la fonction renvoie null sans prévenir
- définir deux fois la même fonction déclenche une erreur fatale
- modifier une variable globale depuis une fonction crée des bugs discrets

À RETENIR
- paramètres typés et type de retour : l'erreur se voit tôt.
- une fonction courte et bien nommée se réutilise partout.
""",
            "Formulaires": """OBJECTIFS
- récupérer les données de $_GET et $_POST
- valider et assainir chaque saisie
- afficher des messages d'erreur utiles

POINTS CLÉS
- $_POST concerne method="post", $_GET les paramètres d'URL
- $_SERVER["REQUEST_METHOD"] indique comment la page a été appelée
- htmlspecialchars($texte, ENT_QUOTES) neutralise le HTML à l'affichage
- filter_var($mail, FILTER_VALIDATE_EMAIL) valide un e-mail
- trim() enlève les espaces, ?? "" évite l'index manquant
- aucune donnée venue du navigateur n'est fiable en l'état

EXEMPLE
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $nom = trim($_POST["nom"] ?? "");
  $mail = trim($_POST["mail"] ?? "");
  $erreurs = [];
  if ($nom === "") { $erreurs[] = "Nom requis"; }
  if (!filter_var($mail, FILTER_VALIDATE_EMAIL)) {
    $erreurs[] = "E-mail invalide";
  }
  if (!$erreurs) { echo "Merci " . htmlspecialchars($nom); }
}

EN PRATIQUE
Le schéma ne change jamais : on reçoit, on valide, puis on affiche les
erreurs ou on enregistre. Un formulaire mal protégé reste la porte
d'entrée la plus empruntée d'un site web.

PIÈGES À ÉVITER
- afficher $_POST["x"] tel quel : faille XSS classique
- valider seulement en JavaScript, qu'on peut désactiver
- un champ sans ?? "" déclenche un avertissement s'il est absent

À RETENIR
- validez à l'entrée, échappez à la sortie : deux étapes distinctes.
- chaque champ doit porter un name et une règle de contrôle.
""",
            "Bases de données": """OBJECTIFS
- se connecter à MySQL avec PDO
- exécuter des requêtes préparées
- parcourir les résultats sans les perdre

POINTS CLÉS
- new PDO(dsn, utilisateur, mot de passe, options)
- ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION : toute erreur devient une exception
- requête préparée : les marqueurs ? remplacent toute donnée utilisateur
- execute([$valeur]) transmet les valeurs à part du texte du SQL
- fetch(PDO::FETCH_ASSOC) renvoie une ligne, fetchAll en renvoie toutes
- fetch en boucle jusqu'à ce qu'il ne reste plus rien

EXEMPLE
$pdo = new PDO(
  "mysql:host=localhost;dbname=babi;charset=utf8mb4",
  "user", "pass",
  [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);
$stmt = $pdo->prepare("SELECT nom FROM users WHERE id = ?");
$stmt->execute([$id]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
echo $user["nom"] ?? "inconnu";

EN PRATIQUE
Toute donnée affichée vient d'une table et toute écriture passe par une
requête préparée. Plusieurs opérations liées se regroupent en transaction
pour réussir ou échouer d'un seul bloc.

PIÈGES À ÉVITER
- concaténer une variable dans le SQL : c'est l'injection SQL
- une variable posée dans une chaîne préparée n'est pas protégée pour autant
- ouvrir un second curseur sans terminer le premier fausse le parcours

À RETENIR
- les marqueurs ? ne protègent que dans la requête préparée.
- en cas de doute, préparez puis exécutez : jamais l'inverse.
""",
            "Sessions et cookies": """OBJECTIFS
- conserver l'état entre deux requêtes avec session()
- utiliser les cookies de façon responsable
- déconnecter proprement

POINTS CLÉS
- session_start() se place tout en haut, avant le moindre HTML
- $_SESSION["connecte"] = true : les données vivent sur le serveur
- le cookie ne contient qu'un identifiant de session, rien d'autre
- session_regenerate_id(true) à la connexion bloque la fixation de session
- session_unset() puis session_destroy() ferment la session
- setcookie accepte httponly, samesite et secure

EXEMPLE
session_start();
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  if (verifie($mail, $mdp)) {
    session_regenerate_id(true);
    $_SESSION["utilisateur"] = $mail;
    $_SESSION["debut"] = time();
  }
}
if (empty($_SESSION["utilisateur"])) {
  header("Location: /connexion.php");
  exit;
}
echo "Bonjour " . htmlspecialchars($_SESSION["utilisateur"]);

EN PRATIQUE
Le panier, l'espace membre et les préférences vivent en session : le
serveur garde les données, le navigateur ne détient qu'un numéro.

PIÈGES À ÉVITER
- session_start() après un echo : « en-têtes déjà envoyés »
- stocker un mot de passe ou un numéro de carte en session est interdit
- oublier exit après la redirection continue d'exécuter la page

À RETENIR
- la session appartient au serveur, le cookie n'en est que la clé.
- régénérez cette clé à chaque connexion réussie.
""",
        },
        "exercises": {
            "Première page": """ÉNONCÉ
- Vous créez votre première page PHP : un message d'accueil, la date du jour
  formatée en français et l'année courante affichée en pied de page.

ÉTAPES
1. Créer index.php et ouvrir avec <?php puis fermer avec ?>.
2. Afficher « Bonjour PHP ! » avec echo.
3. Construire la date avec DateTimeImmutable et sa méthode format().
4. Ajouter un pied de page contenant l'année courante.
5. Contrôler le rendu, puis recharger le lendemain.

RÉSULTAT ATTENDU
- Une ligne « Bonjour PHP ! » suivie de la date au format jj/mm/aaaa.
- Le pied de page affiche l'année courante, par exemple © 2026.
- La date reste juste si vous relisez la page le lendemain.

POUR TESTER
- Changer la date du système : l'affichage doit suivre sans modifier le code.
- Aucune balise PHP brute ne doit rester visible dans la page rendue.
- Afficher la date deux fois : les deux valeurs doivent être identiques.

INDICE
- Le raccourci <?= ... ?> fonctionne en PHP moderne, et DateTimeImmutable
  protège contre une date modifiée sans que vous l'ayez voulu.
""",
            "Calculatrice web": """ÉNONCÉ
- Vous reliez un formulaire HTML à un script PHP : deux nombres et une
  opération donnent un résultat, et chaque saisie invalide affiche son propre
  message plutôt qu'une erreur technique.

ÉTAPES
1. Créer un formulaire POST avec deux champs numériques et un select d'opérations.
2. Traiter la soumission seulement si REQUEST_METHOD vaut POST.
3. Contrôler chaque saisie avec is_numeric avant toute conversion.
4. Dispatcher avec switch : addition, soustraction, multiplication, division.
5. Gérer le cas du diviseur nul et réafficher les valeurs saisies.
6. Essayer les quatre opérations puis les cas limites.

RÉSULTAT ATTENDU
- Avec 10 et 4 en division, le résultat affiché vaut 2.5.
- Avec 0 comme diviseur, le message « division impossible » remplace le résultat.
- Avec « abc » en saisie, le message « nombre invalide » s'affiche.

POUR TESTER
- Envoyer le formulaire vide : chaque champ doit être signalé.
- Diviser par zéro : aucun avertissement PHP ne doit paraître.
- Regarder la source : les valeurs saisies doivent être réaffichées.

INDICE
- Créez d'abord une chaîne de message vide, remplissez-la au fil des
  contrôles, puis affichez-la : le programme reste facile à suivre.
""",
            "Validation d'inscription": """ÉNONCÉ
- Vous validez une inscription côté serveur : nom, e-mail, mot de passe répété
  et acceptation des conditions. Chaque refus affiche sa propre explication
  sous le formulaire.

ÉTAPES
1. Contrôler le nom : non vide et d'au moins deux caractères après trim().
2. Valider l'e-mail avec filter_var et FILTER_VALIDATE_EMAIL.
3. Comparer les deux mots de passe et exiger huit caractères minimum.
4. Exiger la case des conditions cochée.
5. En cas d'erreur, réafficher le formulaire et la liste des messages.
6. En cas de succès, confirmer sans rien conserver en clair.

RÉSULTAT ATTENDU
- Données valides : le message « compte créé » apparaît seul.
- E-mail sans arrobase : « e-mail invalide » rejoint la liste d'erreurs.
- Mots de passe différents : « mots de passe non identiques » s'affiche.

POUR TESTER
- Vider un champ à la fois : chacun doit déclencher son propre message.
- Saisir « bidon@bidon » : le format doit être refusé.
- Vérifier qu'aucun mot de passe n'apparaît dans la page affichée.

INDICE
- password_hash() produit une empreinte que password_verify() contrôle :
  md5 et sha1 ne conviennent plus jamais à des mots de passe.
""",
            "Mini CMS": """ÉNONCÉ
- Vous construisez un mini CMS : la liste des articles vient de MySQL, un
  formulaire en ajoute, une page montre le détail et une dernière action
  supprime après confirmation.

ÉTAPES
1. Créer la table articles (id, titre, contenu, cree_le) via PDO.
2. index.php : SELECT et liste de liens vers detail.php?id=.
3. detail.php : convertir l'id en entier et interroger avec un marqueur ?.
4. ajouter.php : traiter le POST et insérer avec une requête préparée.
5. supprimer.php : accepter seulement le POST, après confirmation.
6. Valider chaque étape avant de passer à la suivante.

RÉSULTAT ATTENDU
- Après un ajout, l'article apparaît aussitôt dans la liste.
- Un id inexistant affiche « article introuvable », sans erreur PHP.
- Le cycle créer, lister, voir, supprimer fonctionne de bout en bout.

POUR TESTER
- Appeler supprimer.php en GET : il doit refuser de supprimer.
- Insérer un titre contenant des balises HTML : elles ne doivent pas s'exécuter.
- Passer un id non numérique dans l'URL : aucun avertissement ne doit paraître.

INDICE
- Les actions destructives passent par POST puis redirection : un simple
  rafraîchissement ne répète alors plus l'opération.
""",
            "Compteur de visiteurs": """ÉNONCÉ
- Vous comptez les visites dans un fichier texte : un total global augmente à
  chaque arrivée et un cookie retient la date de la visite précédente.

ÉTAPES
1. Lire le compteur avec file_get_contents et le convertir en nombre.
2. Incrémenter puis réécrire avec file_put_contents en mode LOCK_EX.
3. Créer le cookie avec setcookie et une expiration prévue.
4. Lire la date portée par le cookie, sinon annoncer la première visite.
5. Afficher le total et le message qui correspond au cas rencontré.

RÉSULTAT ATTENDU
- Deux rafraîchissements donnent un total qui avance de deux.
- À la seconde visite, la page annonce la date de la première.
- Sans cookie, le visiteur lit « première visite ».

POUR TESTER
- Ouvrir la page en fenêtre privée : le total monte toujours.
- Supprimer le cookie puis recharger : le message de première visite revient.
- Effacer le fichier compteur : le compte repart proprement de zéro.

INDICE
- file_get_contents et file_put_contents travaillent en texte simple :
  LOCK_EX évite que deux visites simultanées n'écrasent l'une l'autre.
""",
            "Lecture JSON": """ÉNONCÉ
- Vous consommez une API qui renvoie du JSON, vous affichez ses champs un par
  un et vous traitez proprement le cas où la réponse est vide ou mal formée.

ÉTAPES
1. Récupérer le flux avec file_get_contents($url).
2. Décoder avec json_decode($json, true) pour obtenir un tableau PHP.
3. Contrôler json_last_error() avant d'utiliser le résultat.
4. Parcourir le tableau et afficher deux champs par élément.
5. Annoncer clairement une réponse vide, refusée ou mal formée.

RÉSULTAT ATTENDU
- Une réponse correcte affiche une ligne par élément, titres compris.
- Une réponse vide affiche « aucune donnée reçue ».
- Une réponse non JSON affiche « format JSON incorrect ».

POUR TESTER
- Casser volontairement l'URL : le message d'erreur doit rester lisible.
- Fournir une accolade isolée : le contrôle doit la refuser sans crash.
- Vérifier qu'aucun avertissement PHP ne s'affiche en haut de la page.

INDICE
- json_decode($x, true) renvoie un tableau PHP, sans true un objet stdClass :
  choisissez true pour rester cohérent avec le reste du code.
""",
            "Connexion PDO": """ÉNONCÉ
- Vous réalisez un écran de connexion : les identifiants sont vérifiés dans
  la base, la session s'ouvre, la page protégée devient accessible et la
  déconnexion referme le tout proprement.

ÉTAPES
1. Récupérer e-mail et mot de passe du formulaire envoyé en post.
2. Chercher le compte avec une requête préparée WHERE mail = ?.
3. Contrôler l'empreinte avec password_verify, jamais avec ==.
4. Ouvrir la session, régénérer l'identifiant, stocker l'utilisateur.
5. Rediriger vers le tableau de bord, sinon afficher « identifiants invalides ».
6. Exiger la session sur la page protégée, sinon renvoyer vers la connexion.
7. Créer logout.php : session_destroy() puis redirection.

RÉSULTAT ATTENDU
- Bon mot de passe : redirection vers le tableau de bord.
- Mauvais mot de passe : retour à la connexion avec un message unique,
  identique à celui d'un e-mail inconnu.
- Après déconnexion, la page protégée redemande de se connecter.

POUR TESTER
- Taper le mot de passe en clair : il ne doit jamais apparaître dans la page.
- Ouvrir la page protégée directement dans le navigateur : redirection attendue.
- Rester inactif puis revenir : observez la durée de session retenue.

INDICE
- Un message identique pour e-mail inconnu et mauvais mot de passe évite de
  faire deviner quels comptes existent : ne différenciez jamais les deux cas.
""",
        },
    },
    "Swift": {
        "lessons": {
            "Variables et optionnels": """OBJECTIFS
- distinguer var et let
- maîtriser les optionnels et guard
- convertir et afficher sans faire planter le programme

POINTS CLÉS
- var modifie, let fige ; le compilateur déduit le type
- String? peut valoir nil, ?? fournit une valeur de repli
- guard let x = y else { return } sort proprement de la fonction
- as? produit un optionnel, as! échoue avec un arrêt brutal
- Int("42") renvoie un optionnel à contrôler avant usage
- print accepte plusieurs valeurs séparées par des virgules

EXEMPLE
var nom: String? = "Babi"
guard let nom = nom else { return }
let prenom = nom ?? "Anonyme"
let age = Int("30") ?? 0
print("Bonjour " + prenom, age)

let chiffre = 42
let texte = String(chiffre)
let inverse = String(texte.reversed())

EN PRATIQUE
Toute donnée externe arrive en optionnel : saisie clavier, fichier lu,
réponse réseau. Plutôt que de forcer avec !, on teste, on déplie avec
guard, puis on travaille avec une valeur non nullable.

PIÈGES À ÉVITER
- forcer un nil avec ! arrête l'application sur-le-champ
- Int("12a") renvoie nil sans explication : contrôlez toujours le retour
- une constante let ne se modifie pas, même à l'intérieur d'une boucle

À RETENIR
- l'optionnel dit « peut ne pas exister » : traitez-le explicitement.
- guard garde le cas nominal en haut, les replis à la fin.
""",
            "Conditions et boucles": """OBJECTIFS
- écrire if et switch avec assurance
- boucler avec for-in sur plages et collections
- exploiter tuples et plages dans les cases

POINTS CLÉS
- switch doit être exhaustif : une case manquante bloque la compilation
- case 1...5 pour une plage fermée, case ..<5 exclut la borne haute
- case (let a, let b) décompose un tuple, _ accepte n'importe quoi
- where filtre : case let n where n > 10
- for i in 1...5, for x dans une collection ; une plage vide est refusée
- if let déplie un optionnel et le bloc else gère l'absence

EXEMPLE
switch (jour, mois) {
case (1, 1): print("Nouvel An")
case (_, 12): print("Décembre")
default: break
}
for i in 1...5 where i % 2 == 0 {
  print(i)
}
let note = 14
if note >= 10 { print("admis") } else { print("ajourné") }

EN PRATIQUE
Un switch sur un tuple se lit comme une table de décision : on sépare les
cas particuliers du cas général. Les plages conviennent aux bornes de
prix, d'âges et d'index, où chaque limite compte.

PIÈGES À ÉVITER
- oublier le default : le code ne compile plus
- une case mal terminée laisse croire que l'exécution continue
- ... et ..< se confondent souvent : testez les bornes limites

À RETENIR
- chaque case se termine, sans exception.
- cas particuliers d'abord, cas général à la fin.
""",
            "Fonctions": """OBJECTIFS
- définir des fonctions avec étiquettes de paramètres
- retourner plusieurs valeurs grâce aux tuples
- utiliser les closures, y compris en position finale

POINTS CLÉS
- func f(a: Int, b: Int = 1) -> Int
- l'appel s'écrit f(a: 1, b: 2) : les étiquettes font partie du nom
- _ retire l'étiquette : func diviser(_ a: Double, par b: Double)
- un tuple peut servir de retour : -> (Bool, String)
- closure : { (x: Int) -> Int in x * 2 }, $0 désigne le premier argument
- une closure en fin d'appel peut s'écrire sans accolade fermante

EXEMPLE
func diviser(_ a: Double, par b: Double) -> Double? {
  guard b != 0 else { return nil }
  return a / b
}
if let r = diviser(10, par: 4) { print(r) }

let nombres = [3, 8, 15]
let pairs = nombres.filter { $0 % 2 == 0 }
print(pairs)

EN PRATIQUE
Grâce aux étiquettes, une fonction se lit comme une phrase. On la range
dans une extension ou un service, puis on la teste avec des valeurs
ordinaires et des cas limites, avant de l'utiliser ailleurs.

PIÈGES À ÉVITER
- changer une étiquette casse tous les appels : c'est voulu, vérifiez-les
- un return manquant dans une closure multiligne ne compile pas
- un type de retour non déclaré force le compilateur à deviner

À RETENIR
- l'étiquette rend l'appel lisible : diviser(10, par: 4).
- un retour optionnel dit que le calcul peut échouer.
""",
            "Structures et classes": """OBJECTIFS
- choisir struct (valeur) ou class (référence)
- initialiser avec init
- comprendre mutating et les méthodes de classe

POINTS CLÉS
- une struct est copiée à l'assignation, une class partage la même instance
- init configure les propriétés, let interdit toute modification ensuite
- mutating autorise une méthode de struct à changer sa propre valeur
- une class peut hériter et nettoyer ses ressources avec deinit
- equatable fournit ==, hashable permet d'entrer dans un dictionnaire
- une propriété lazy ne se calcule qu'à la première lecture

EXEMPLE
struct Point {
  var x = 0.0
  var y = 0.0
  mutating func deplacer(dx: Double) { x += dx }
}
var a = Point()
var b = a
b.deplacer(dx: 5)
print(a.x, b.x)      // deux valeurs indépendantes

class Compte {
  var solde = 0.0
  deinit { print("compte fermé") }
}

EN PRATIQUE
On commence presque toujours par une struct : tests plus simples, aucun
partage caché. La class intervient quand plusieurs endroits doivent agir
sur la même entité, comme un gestionnaire partagé.

PIÈGES À ÉVITER
- modifier une struct sans mutating : refus immédiat du compilateur
- croire qu'une copie de class reste indépendante : elle partage l'état
- oublier d'initialiser une propriété obligatoire dans init

À RETENIR
- privilégiez struct : moins d'effets de bord, code plus prévisible.
- la class sert aux identités partagées, pas aux valeurs simples.
""",
            "Tableaux et dictionnaires": """OBJECTIFS
- manipuler [Element] et [Clé: Valeur]
- transformer avec map, filter et reduce
- gérer les accès qui peuvent échouer

POINTS CLÉS
- un index hors des bornes fait planter l'app : d'où array.first, un optionnel
- dictionary["clé"] renvoie aussi un optionnel, jamais la valeur directement
- map transforme, filter sélectionne, reduce additionne en un seul appel
- sorted prend une closure de tri : sorted { $0.age < $1.age }
- append ajoute, remove(at:) retire, count donne la taille
- ?? fournit un repli immédiat sur un accès optionnel

EXEMPLE
let notes = [12, 15, 9]
let admis = notes.filter { $0 >= 10 }.map { "note \\($0)" }
let total = notes.reduce(0, +)
let scores = ["babi": 1, "zoe": 2]
let valeur = scores["babi"] ?? 0
print(admis, total, valeur)

EN PRATIQUE
Le tableau range une liste homogène, le dictionnaire des données nommées
comme un cache ou des préférences. Enchaîner map et filter évite les
boucles imbriquées et se lit en une seule ligne.

PIÈGES À ÉVITER
- lire un index qui n'existe pas : passez par first ou un garde-fou
- compter sur une copie de tableau partagé : précisez ce que vous voulez
- trier sans critère stable : l'ordre à égalité change d'un passage à l'autre

À RETENIR
- accès optionnel puis valeur par défaut : la paire qui évite les crashes.
- map, filter et reduce remplacent la plupart des boucles.
""",
            "Protocoles": """OBJECTIFS
- décrire des capacités avec protocol
- adopter et étendre un protocole
- utiliser un protocole comme type courant

POINTS CLÉS
- protocol Affichable { func afficher() }
- struct, enum ou classe se conforme en écrivant : NomDuProtocole
- une extension peut fournir une implémentation par défaut
- var obj: Affichable accepte toute valeur conforme, même hétérogène
- ProtocoleA & ProtocoleB exige les deux contrats à la fois
- Codable, Equatable et Identifiable sont des protocoles de la bibliothèque

EXEMPLE
protocol Serializable {
  func versJSON() -> String
}
extension String: Serializable {
  func versJSON() -> String { "\\"\\(self)\\"" }
}
struct Produit: Serializable {
  let nom: String
  func versJSON() -> String { "{\\"nom\\":\\"\\(nom)\\"}" }
}
let objets: [Serializable] = ["salut", Produit(nom: "Clavier")]

EN PRATIQUE
On code contre un protocole plutôt qu'une classe concrète : les tests
utilisent un faux objet et de nouveaux types arrivent sans toucher au code
appelant. C'est le principe de composition qui remplace l'héritage.

PIÈGES À ÉVITER
- annoncer la conformité sans implémenter tout : la compilation refuse
- étendre un type en oubliant une méthode exigée
- garder une liste de classes hétérogènes au lieu d'un protocole

À RETENIR
- décrivez ce que l'objet sait faire, pas ce qu'il est.
- composition plutôt que héritage profond.
""",
            "Erreurs": """OBJECTIFS
- lancer des erreurs avec throw
- les attraper avec do et catch
- distinguer un échec prévu d'un vrai bug

POINTS CLÉS
- enum MonErreur: Error { case invalide }
- la fonction qui lève est marquée throws et s'appelle avec try
- do { try f() } catch MonErreur.invalide { ... }
- try? transforme le résultat en optionnel, nil en cas d'échec
- try! suppose le succès : un échec arrête l'application
- guard throw raccourcit la validation au début de la fonction

EXEMPLE
enum ConnexionError: Error {
  case identifiantsInvalides
}
func connecter(mdp: String) throws {
  guard mdp.count >= 8 else {
    throw ConnexionError.identifiantsInvalides
  }
}
do {
  try connecter(mdp: "court")
} catch {
  print("échec :", error)
}

EN PRATIQUE
Un échec métier, comme un mot de passe trop court ou un fichier absent,
mérite un throw : l'appelant décide du message à afficher. Un vrai bug, en
revanche, doit faire échouer les tests plutôt que d'être dissimulé.

PIÈGES À ÉVITER
- appeler try sans do ni try? : la compilation refuse
- attraper sans distinguer les cas : le message reste vague
- tout convertir en optionnel avec try? et perdre la cause

À RETENIR
- try? pour le cas simple, do/catch quand il faut expliquer.
- une erreur métier est une information, pas un plantage.
""",
        },
        "exercises": {
            "Premier playground": """ÉNONCÉ
- Vous ouvrez un playground Xcode et vous y affichez un message d'accueil,
  la version de Swift utilisée et votre nom entièrement en majuscules.

ÉTAPES
1. Dans Xcode, choisir File > New > Playground puis le modèle Blank.
2. Écrire print("Bonjour Swift !").
3. Indiquer la version utilisée, par exemple avec une constante.
4. Ajouter un nom en minuscules puis appeler .uppercased().
5. Exécuter et lire la zone de résultats à droite.

RÉSULTAT ATTENDU
- « Bonjour Swift ! » occupe sa propre ligne de sortie.
- La version de Swift apparaît juste après, par exemple 5.9.
- Le nom s'affiche en majuscules intégrales, par exemple BABI.

POUR TESTER
- Modifier le message puis exécuter : la zone de résultats doit suivre.
- Passer un nom déjà en majuscules : la sortie ne doit pas le double.
- Placer le curseur sur une sortie : le numéro de ligne doit correspondre.

INDICE
- L'interpolation \\(expr) s'écrit dans n'importe quelle chaîne Swift et
 accepte une expression complète entre parenthèses.
""",
            "Convertisseur": """ÉNONCÉ
- Vous créez un convertisseur de températures : des fonctions pures
  celsiusVersFahrenheit et l'inverse, plus un affichage formaté à une
  décimale près.

ÉTAPES
1. Créer une enum Convertisseur avec des fonctions statiques.
2. Écrire c × 9 / 5 + 32 et l'inverse (f − 32) × 5 / 9.
3. Typer paramètres et retours en Double.
4. Formater l'affichage avec String(format: "%.1f", valeur).
5. Tester les valeurs basses, hautes et négatives.

RÉSULTAT ATTENDU
- 0 degré Celsius donne 32.0 Fahrenheit.
- 100 degrés Celsius donnent 212.0 Fahrenheit.
- 98.6 Fahrenheit donne 37.0 Celsius.

POUR TESTER
- Repartir d'un résultat et le reconvertir : vous devez retrouver le départ.
- Essayer -40 : les deux échelles doivent afficher la même valeur.
- Vérifier qu'aucune fonction n'affiche elle-même du texte.

INDICE
- Une fonction pure ne lit ni n'écrit rien autour d'elle : elle reçoit un
 Double et en renvoie un autre, ce qui la rend très facile à tester.
""",
            "Compteur pas à pas": """ÉNONCÉ
- Vous modélisez un compteur avec une struct Compteur et trois méthodes :
  incrémenter, décrémenter et remettre à zéro, avec un pas réglable.

ÉTAPES
1. Déclarer struct Compteur avec une propriété var valeur: Int = 0.
2. Marquer de mutating chaque méthode qui modifie la valeur.
3. Ajouter un paramètre pas dont la valeur par défaut vaut 1.
4. Refuser un pas négatif dans l'incrémentation.
5. Afficher la valeur après chaque appel pour suivre l'évolution.

RÉSULTAT ATTENDU
- Partant de 0, deux incréments donnent 2 puis un décrément redonne 1.
- La remise à zéro ramène à 0 sans rien conserver.
- Un pas de 5 fait passer de 0 à 5 en une seule étape.

POUR TESTER
- Appeler une méthode depuis une constante : le compilateur refuse.
- Passer un pas nul : la valeur ne doit pas bouger.
- Afficher entre chaque appel : la suite des nombres doit être continue.

INDICE
- Sans mutating, Swift interdit à une méthode de struct de se modifier
 elle-même : ce refus est le signal qu'il manque le mot-clé.
""",
            "FizzBuzz": """ÉNONCÉ
- Vous réalisez FizzBuzz de 1 à 100 avec un switch et des cases multiples,
  puis vous collectez la sortie pour l'afficher dix éléments par dix.

ÉTAPES
1. Déclarer un tableau de chaînes et une boucle for i in 1...100.
2. Construire le tuple (i % 3, i % 5) et le passer au switch.
3. Écrire les cases (0, 0), (0, _) et (_, 0), dans cet ordre.
4. Ajouter un default qui convertit l'entier en chaîne.
5. Ajouter au tableau puis afficher par groupes de dix.

RÉSULTAT ATTENDU
- 15 donne FizzBuzz, 9 donne Fizz, 10 donne Buzz, 7 reste 7.
- La suite commence par 1, 2, Fizz, 4, Buzz.
- Chaque ligne affiche exactement dix éléments.

POUR TESTER
- Compter les FizzBuzz entre 1 et 100 : il doit y en avoir exactement 6.
- Vérifier qu'aucun multiple de 3 ne s'affiche nu sur la première ligne.
- Réduire la plage à 1...10 : le reste du programme ne doit pas bouger.

INDICE
- Le _ accepte n'importe quelle valeur : case (0, _) signifie divisible
 par 3, quel que soit le reste obtenu face à 5.
""",
            "Compte bancaire": """ÉNONCÉ
- Vous modélisez un compte bancaire avec une classe : dépôt autorisé,
  retrait conditionné au solde et description lisible. L'exercice montre
  aussi la différence entre une référence et une valeur.

ÉTAPES
1. Créer class CompteBancaire avec let titulaire et private(set) var solde.
2. Écrire deposer(_:) qui refuse tout montant négatif.
3. Écrire retirer(_:) -> Bool qui ne retire que si le solde suffit.
4. Se conformer à CustomStringConvertible pour afficher le compte.
5. Copier la référence dans une seconde variable, puis modifier par l'une.

RÉSULTAT ATTENDU
- Après un dépôt de 100 et un retrait de 30, le solde vaut 70.
- Un retrait de 500 renvoie false et laisse le solde inchangé.
- Modifier par la copie change aussi l'original : c'est une référence.

POUR TESTER
- Écrire compte.solde = 0 depuis l'extérieur : le compilateur refuse.
- Déposer un montant négatif : le solde doit rester identique.
- Afficher le compte : la description doit contenir le solde formaté.

INDICE
- private(set) rend la lecture publique et l'écriture privée : le solde se
 consulte partout, mais il ne peut se modifier que dans la classe.
""",
            "Décodage JSON": """ÉNONCÉ
- Vous décodez une chaîne JSON décrivant un produit (id, nom, prix) avec
  Codable, vous affichez le produit et vous traitez un JSON volontairement
  cassé sans faire planter le programme.

ÉTAPES
1. Déclarer struct Produit: Decodable avec id, nom et prix.
2. Convertir la chaîne en Data grâce à Data(...utf8).
3. Appeler JSONDecoder().decode(Produit.self, from: data).
4. Traiter l'échec avec do/catch ou avec try?, selon le message voulu.
5. Afficher le produit, sinon « format invalide ».

RÉSULTAT ATTENDU
- Un JSON complet affiche le nom et le prix du produit.
- Une accolade manquante affiche « format invalide », sans arrêt.
- Un prix écrit en texte déclenche lui aussi l'échec du décodage.

POUR TESTER
- Supprimer une virgule puis relancer : le message doit apparaître.
- Renommer un champ : observez ce qui reste affiché.
- Vérifier qu'aucun détail technique n'apparaît devant l'utilisateur.

INDICE
- Les noms de champs JSON doivent correspondre aux propriétés Swift :
 sinon décrivez le mapping avec une énumération CodingKeys.
""",
            "Tri de personnes": """ÉNONCÉ
- Vous triez un tableau de Personne (nom, âge) d'abord par âge croissant,
  puis par nom lorsque deux âges sont identiques, et vous affichez l'avant
  et l'après.

ÉTAPES
1. Déclarer struct Personne avec let nom et let age.
2. Créer un tableau de quatre personnes, dont deux du même âge.
3. Trier avec sorted et la closure { $0.age < $1.age }.
4. Ajouter le critère sur le nom quand les âges sont égaux.
5. Afficher le tableau d'origine et le tableau trié, côte à côte.

RÉSULTAT ATTENDU
- La personne la plus jeune apparaît en tête de liste.
- À âge égal, les noms s'ordonnent alphabétiquement.
- Le tableau d'origine reste strictement inchangé.

POUR TESTER
- Compter les éléments avant et après : les deux tailles sont égales.
- Inverser le critère : l'ordre doit se retourner complètement.
- Trier deux fois de suite : le second tri ne doit rien changer.

INDICE
- sorted renvoie un nouveau tableau sans modifier le récepteur : c'est ce
 qui vous permet d'afficher l'avant et l'après sans copie préalable.
""",
        },
    },
}
