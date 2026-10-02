"""Corrections commentées — lot 4 : HTML/CSS, PHP, Swift.

Une entrée par exercice du curriculum (titre exact, copié-collé depuis
core/curriculum.py, clé "exercises" obligatoire) :

    CONTENT["HTML/CSS"]["exercises"]["Page CV"] = \"\"\"SOLUTION
    ...
    \"\"\"

Fusionnées dans core/solutions.py. Contrôle :
    python tests/check_solutions.py "HTML/CSS" PHP Swift
"""
CONTENT = {
    "HTML/CSS": {
        "exercises": {
            "Page CV": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>CV de Babi</title>
</head>
<body>
  <header>
    <img src="photo.jpg" alt="Portrait de Babi" width="120">
    <h1>Babi, développeur web</h1>
    <ul>
      <li><a href="mailto:babi@example.com">babi@example.com</a></li>
      <li><a href="tel:+33600000000">06 00 00 00 00</a></li>
    </ul>
  </header>
  <main>
    <section>
      <h2>Expériences</h2>
      <ul><li>2025 : développeur en alternance</li></ul>
    </section>
    <section>
      <h2>Compétences</h2>
      <ul><li>HTML, CSS, PHP</li></ul>
    </section>
    <section>
      <h2>Formation</h2>
      <ul><li>BTS informatique</li></ul>
    </section>
  </main>
  <footer>Mise à jour en 2026</footer>
</body>
</html>

EXPLICATION

Le squelette HTML5 est complet : doctype, lang, head, body. Les
régions header, main, section et footer servent de repères aux
lecteurs d'écran. Un seul h1 décrit la personne, chaque section a
son h2, et l'image porte un alt qui décrit la photo.

POINTS DE VÉRIFICATION

- Un seul h1, aucun titre sauté, alt non vide sur l'image.
- La page reste lisible sans CSS et passe le validateur W3C.
- Piège : une balise fermée dans le mauvais parent casse le DOM.

POUR ALLER PLUS LOIN

- Relier une feuille de style externe et habiller la mise en page.
- Ajouter un aside pour les langues parlées.
""",
            "Menu responsive": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Menu</title>
  <style>
    nav { background: #1d2b53; }
    nav ul { display: flex; gap: 4px; margin: 0; padding: 0; list-style: none; }
    nav a { display: block; padding: 14px 16px; color: #fff; text-decoration: none; }
    nav a:hover { background: #3a50c9; }
    nav a:focus-visible { outline: 3px solid #ffcc00; }
    .actif { background: #ffcc00; color: #1d2b53; }
    @media (max-width: 700px) {
      nav ul { flex-direction: column; }
    }
  </style>
</head>
<body>
  <nav>
    <ul>
      <li><a href="#" class="actif">Accueil</a></li>
      <li><a href="#">Services</a></li>
      <li><a href="#">Tarifs</a></li>
    </ul>
  </nav>
</body>
</html>

EXPLICATION

La liste ul est le seul conteneur flex, gap remplace les marges de
raccord. Au-dessus de 700 pixels la barre reste horizontale ; la
media query inverse l'axe principal et chaque lien passe en pleine
largeur. La classe actif, déclarée plus bas, gagne la cascade.

POINTS DE VÉRIFICATION

- Large : trois liens alignés sur une ligne ; sous 700 px : colonne.
- Tabulation : le lien reçu de focus est entouré en jaune.
- Piège : mettre le flex sur les li au lieu du ul.

POUR ALLER PLUS LOIN

- Replier le menu avec une case à cocher, sans JavaScript.
- Ajouter aria-current sur le lien actif.
""",
            "Galerie en grille": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Galerie</title>
  <style>
    .galerie {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 16px;
      padding: 16px;
    }
    .galerie img {
      display: block;
      width: 100%;
      height: 160px;
      object-fit: cover;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <h1>Galerie</h1>
  <div class="galerie">
    <img src="chat.jpg" alt="Un chat endormi">
    <img src="chien.jpg" alt="Un chien dans l'herbe">
    <img src="oiseau.jpg" alt="Un oiseau sur une branche">
    <img src="serpent.jpg" alt="Un serpent sur un rocher">
  </div>
</body>
</html>

EXPLICATION

auto-fill et minmax(200px, 1fr) font tout le travail : chaque
colonne vaut au minimum 200 pixels et le navigateur en crée autant
qu'il en peut placer : la grille passe de quatre colonnes à une
seule sur téléphone, sans media query. gap sépare les cases et
l'image en largeur 100 pour cent remplit sa colonne.

POINTS DE VÉRIFICATION

- 800 pixels de large : quatre colonnes ; 360 : une seule.
- Aucun débordement, chaque img a un alt descriptif.
- Piège : oublier le 100 pour cent, l'image déborde de sa colonne.

POUR ALLER PLUS LOIN

- Remplacer auto-fill par auto-fit pour agrandir les colonnes rares.
- Encadrer les images d'un figcaption.
""",
            "Formulaire contact": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Contact</title>
</head>
<body>
  <form action="/envoi" method="post">
    <fieldset>
      <legend>Écrivez-nous</legend>
      <label for="nom">Nom</label>
      <input id="nom" name="nom" required minlength="2">
      <label for="mail">E-mail</label>
      <input id="mail" name="mail" type="email" required>
      <label for="msg">Message</label>
      <textarea id="msg" name="msg" required minlength="10"></textarea>
      <label for="accord">
        <input id="accord" name="accord" type="checkbox" required>
        J'accepte l'utilisation de mes données.
      </label>
      <button type="submit">Envoyer</button>
    </fieldset>
  </form>
</body>
</html>

EXPLICATION

Chaque champ a un label lié par for et id : le clic focus le
champ et un lecteur d'écran annonce le titre. La validation est
native : required bloque un vide, type email réclame une adresse
crédible, minlength impose une longueur, et la case d'accord
exigée empêche l'envoi sans consentement.

POINTS DE VÉRIFICATION

- Formulaire vide : le premier champ fautif est signalé.
- « bidule » en e-mail : message de type invalide.
- Trois caractères dans le message : refusé par minlength.

POUR ALLER PLUS LOIN

- Personnaliser les messages avec title et pattern sur le nom.
- Habiller ensuite le formulaire avec un peu de CSS.
""",
            "Carte produit": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Carte produit</title>
  <style>
    .carte {
      display: flex; gap: 20px; max-width: 700px; padding: 20px;
      background: #fff; border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, .18);
    }
    .carte img { width: 200px; height: 150px; object-fit: cover; }
    .contenu { display: flex; flex-direction: column; }
    .carte button { margin-top: auto; }
    @media (max-width: 600px) {
      .carte { flex-direction: column; }
      .carte img { width: 100%; }
    }
  </style>
</head>
<body>
  <article class="carte">
    <img src="clavier.jpg" alt="Clavier mécanique rétroéclairé">
    <div class="contenu">
      <h2>Clavier mécanique</h2>
      <p><strong>89,90 €</strong></p>
      <button type="button">Ajouter au panier</button>
    </div>
  </article>
</body>
</html>

EXPLICATION

display flex met l'image et le texte côte à côte. Sous 600
pixels, la media query inverse l'axe et la carte devient
verticale. Les arrondis viennent de border-radius, l'ombre de
box-shadow avec un flou doux, et margin-top auto colle le bouton
en bas quand deux cartes ont la même hauteur.

POINTS DE VÉRIFICATION

- Au-dessus de 600 pixels : image à gauche, texte à droite.
- En dessous : tout s'empile en colonne.
- Piège : largeur fixe sur le img fait déborder la carte.

POUR ALLER PLUS LOIN

- Refaire le même gabarit avec CSS Grid.
- Ajouter un survol qui remonte légèrement l'ombre.
""",
            "Section hero": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Hero</title>
  <style>
    .hero {
      min-height: 60vh; display: flex; flex-direction: column;
      justify-content: center; align-items: center;
      padding: 40px 20px; text-align: center; color: #fff;
      background: linear-gradient(135deg, #4a00e0, #e100ff);
    }
    .hero h1 { font-size: clamp(2rem, 6vw, 3.5rem); }
    .actions { display: flex; gap: 16px; }
    .actions a { padding: 12px 24px; border-radius: 999px; background: #fff; color: #4a00e0; text-decoration: none; }
    @media (max-width: 500px) { .actions { flex-direction: column; } }
  </style>
</head>
<body>
  <section class="hero">
    <h1>Apprends à coder</h1>
    <div class="actions">
      <a href="#">Commencer</a>
      <a href="#">Voir la démo</a>
    </div>
  </section>
</body>
</html>

EXPLICATION

min-height 60vh donne un bloc haut sans forcer le premier scroll :
vh se réfère à la fenêtre, pas au contenu. Le dégradé est un
arrière-plan : linear-gradient part d'un angle et mélange deux
couleurs. Flex en colonne centre le contenu, et clamp fait varier
le titre selon la largeur. Sous 500 pixels, les boutons s'empilent.

POINTS DE VÉRIFICATION

- Le bloc occupe au moins 60 pour cent de la hauteur de fenêtre.
- Boutons côte à côte en grand, empilés sous 500 pixels.
- Piège : sans text-align, le texte reste collé à gauche.

POUR ALLER PLUS LOIN

- Définir les couleurs du dégradé en variables CSS.
""",
            "Thème sombre": """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Thème sombre</title>
  <style>
    :root { --fond: #fff; --texte: #1a1a1a; --accent: #4a00e0; }
    body { background: var(--fond); color: var(--texte); transition: .3s; }
    a { color: var(--accent); }
    @media (prefers-color-scheme: dark) {
      :root { --fond: #121212; --texte: #eee; --accent: #b388ff; }
    }
    html.sombre { --fond: #121212; --texte: #eee; --accent: #b388ff; }
  </style>
</head>
<body>
  <h1>Bienvenue</h1>
  <p><a href="#">Un lien pour voir l'accent</a></p>
  <button type="button" id="bascule">Basculer le thème</button>
  <script>
    document.getElementById("bascule").addEventListener("click", function () {
      document.documentElement.classList.toggle("sombre");
    });
  </script>
</body>
</html>

EXPLICATION

Toutes les couleurs passent par trois variables déclarées sur la
racine : changer la variable change la page entière. La media
query prefers-color-scheme les redéfinit quand le système est en
mode sombre ; arrivant plus bas dans la feuille, elle gagne la
cascade. La classe sombre sur html joue le même rôle au clic et
l'emporte alors sur la préférence système.

POINTS DE VÉRIFICATION

- Système clair : fond blanc, sans rien cliquer.
- Système sombre : la page bascule seule au premier affichage.
- Clic sur le bouton : le thème change même à système clair.

POUR ALLER PLUS LOIN

- Mémoriser le choix dans localStorage.
""",
        },
    },
    "PHP": {
        "exercises": {
            "Première page": """SOLUTION

<?php
// Sert le fichier avec : php -S localhost:8000
$moment = new DateTimeImmutable("now", new DateTimeZone("Europe/Paris"));
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Première page PHP</title>
</head>
<body>
  <h1>Bonjour PHP !</h1>
  <p>Nous sommes le <?= $moment->format("d/m/Y") ?>
     à <?= $moment->format("H:i") ?>.</p>
  <footer>&copy; <?= $moment->format("Y") ?> — BabiProgrammeur</footer>
</body>
</html>

EXPLICATION

Le fichier mélange PHP et HTML : tout ce qui est entre les balises
PHP est exécuté à chaque requête, le reste part tel quel au
navigateur. DateTimeImmutable fabrique l'instant courant avec un
fuseau explicite, ce qui évite la surprise de l'heure du serveur,
et format reprend la date en jour/mois/année puis l'heure. L'année
du pied de page est calculée : elle restera juste l'an prochain.

POINTS DE VÉRIFICATION

- php -S localhost:8000 puis ouverture : titre et date s'affichent.
- Un rafraîchissement change l'heure, jamais la structure.
- Piège : du HTML écrit avant l'ouverture PHP sans fermeture
  s'affiche comme du texte brut.

POUR ALLER PLUS LOIN

- Afficher le jour de la semaine avec format("l").
- Sortir le pied de page dans un fichier inclus avec require.
""",
            "Calculatrice web": """SOLUTION

<?php
// Le formulaire se poste vers lui-même.
$a = trim($_POST["a"] ?? ""); $b = trim($_POST["b"] ?? "");
$op = $_POST["op"] ?? "+"; $erreur = ""; $resultat = null;
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (!is_numeric($a) || !is_numeric($b)) $erreur = "Nombre invalide.";
    elseif ($op === "/" && (float) $b == 0) $erreur = "Division impossible.";
    else {
        $resultat = ["+" => $a + $b, "-" => $a - $b,
                     "*" => $a * $b, "/" => $a / $b][$op];
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Calculatrice</title></head>
<body>
<form method="post">
<input name="a" value="<?= htmlspecialchars($a) ?>">
<input name="op" value="<?= htmlspecialchars($op) ?>">
<input name="b" value="<?= htmlspecialchars($b) ?>">
<button>Calculer</button>
</form>
<?php if ($erreur): ?><p><?= $erreur ?></p>
<?php elseif ($resultat !== null): ?><p>Résultat : <?= $resultat ?></p><?php endif; ?>
</body>
</html>

EXPLICATION

La page se poste vers elle-même : elle reçoit les données puis les
réaffiche. is_numeric filtre avant le calcul, sinon « abc »
deviendrait zéro. Les quatre opérations sont rangées dans un
tableau dont on lit la clé, ce qui évite un switch à quatre
branches. La division est testée à part : diviser par zéro se
refuse avant de calculer.

POINTS DE VÉRIFICATION

- 10 divisé par 4 donne 2.5 ; 10 par 0 affiche l'erreur.
- « abc » donne « Nombre invalide », jamais zéro.
- 5 fois 0 donne zéro, sans erreur.

POUR ALLER PLUS LOIN

- Séparer affichage et traitement dans deux fichiers.
""",
            "Validation d'inscription": """SOLUTION

<?php
$erreurs = []; $cree = false;
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $mail = trim($_POST["mail"] ?? ""); $mdp = $_POST["mdp"] ?? "";
    if (mb_strlen(trim($_POST["nom"] ?? "")) < 2) $erreurs[] = "Nom trop court.";
    if (!filter_var($mail, FILTER_VALIDATE_EMAIL)) $erreurs[] = "E-mail invalide.";
    if (strlen($mdp) < 8 || $mdp !== ($_POST["mdp2"] ?? "")) $erreurs[] = "Mot de passe incorrect.";
    if (!isset($_POST["conditions"])) $erreurs[] = "Conditions requises.";
    if (!$erreurs) { $hash = password_hash($mdp, PASSWORD_DEFAULT); $cree = true; }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Inscription</title></head>
<body>
<?php if ($cree): ?>
<p>Compte créé pour <?= htmlspecialchars($mail) ?>.</p>
<?php else: ?>
<p><?= htmlspecialchars(implode(" ", $erreurs)) ?></p>
<form method="post">
<label>Nom <input name="nom" required></label>
<label>E-mail <input name="mail" type="email" required></label>
<label>Mot de passe <input name="mdp" type="password"></label>
<label>Confirmation <input name="mdp2" type="password"></label>
<label><input name="conditions" type="checkbox"> Conditions acceptées</label>
<button>S'inscrire</button>
</form>
<?php endif; ?>
</body>
</html>

EXPLICATION

Chaque contrôle ajoute un message au tableau, puis une seule
variable décide : le compte n'est créé que si le tableau reste vide.
filter_var refuse les adresses mal formées bien mieux qu'un test
d'arobase, et la comparaison stricte vérifie que les mots de passe
sont identiques sans convertir les types. password_hash transforme
la saisie en empreinte salée.

POINTS DE VÉRIFICATION

- Champs valides : le formulaire devient une confirmation.
- Mots de passe courts ou différents : le message apparaît.
- Case non cochée : l'inscription reste bloquée.

POUR ALLER PLUS LOIN

- Ajouter un champ piège invisible contre les robots.
""",
            "Mini CMS": """SOLUTION

<?php
// Les articles vivent en session : PHP oublie tout entre deux requêtes.
session_start();
if (!isset($_SESSION["articles"])) {
    $_SESSION["articles"] = [1 => ["titre" => "Bienvenue", "contenu" => "Premier article."]];
}
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (isset($_POST["supprimer"])) {
        unset($_SESSION["articles"][(int) $_POST["supprimer"]]);
    } elseif (trim($_POST["titre"] ?? "") !== "") {
        $ids = array_keys($_SESSION["articles"]);
        $_SESSION["articles"][$ids ? max($ids) + 1 : 1] =
            ["titre" => trim($_POST["titre"]), "contenu" => trim($_POST["contenu"] ?? "")];
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Mini CMS</title></head>
<body>
<ul>
<?php foreach ($_SESSION["articles"] as $id => $art): ?>
<li><h2><?= htmlspecialchars($art["titre"]) ?></h2>
<p><?= htmlspecialchars($art["contenu"]) ?></p>
<form method="post"><input type="hidden" name="supprimer" value="<?= $id ?>"><button>Supprimer</button></form></li>
<?php endforeach; ?>
</ul>
<form method="post">
<label>Titre <input name="titre" required></label>
<label>Contenu <input name="contenu"></label>
<button>Publier</button>
</form>
</body>
</html>

EXPLICATION

session_start ouvre l'espace serveur de la session : le tableau
d'articles y survit d'une requête à l'autre tant que le navigateur
renvoie son cookie, contrairement à une variable PHP simple qui
repart à zéro. L'identifiant le plus élevé sert à créer un article
sans écraser l'existant. La suppression passe par un champ caché en
méthode post, jamais par un lien get.

POINTS DE VÉRIFICATION

- Publier : le titre apparaît à la requête suivante.
- Supprimer : la ligne disparaît, les autres restent intactes.
- Un titre contenant du code s'affiche en texte, jamais exécuté.

POUR ALLER PLUS LOIN

- Remplacer la session par un fichier JSON sur le disque.
""",
            "Compteur de visiteurs": """SOLUTION

<?php
// Total mondial dans un fichier, dernière visite personnelle en cookie.
$fichier = "visiteurs.txt";
$total = is_readable($fichier) ? (int) file_get_contents($fichier) : 0;
$total++;
file_put_contents($fichier, (string) $total, LOCK_EX);

$precedente = $_COOKIE["derniere_visite"] ?? "";
setcookie("derniere_visite", date("d/m/Y H:i"), time() + 60 * 60 * 24 * 30);
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Compteur</title></head>
<body>
<h1><?= $total ?> visite(s) sur ce site</h1>
<?php if ($precedente === ""): ?>
<p>Première visite : bienvenue !</p>
<?php else: ?>
<p>Vous étiez venu le <?= htmlspecialchars($precedente) ?>.</p>
<?php endif; ?>
</body>
</html>

EXPLICATION

Le fichier contient le total mondial : on le lit, on l'incrémente,
puis on le réécrit avec LOCK_EX, qui verrouille le fichier pendant
l'écriture et empêche deux requêtes simultanées d'écraser la valeur
de l'autre. Le cookie porte une information personnelle et datée :
il est lu dans la requête courante puis renouvelé pour un mois. Le
premier affichage annonce donc la première visite, car le serveur
ne reçoit le cookie qu'en fin de réponse.

POINTS DE VÉRIFICATION

- Trois rafraîchissements affichent 1, 2 puis 3.
- Deuxième visite : la date précédente s'affiche puis se met à jour.
- Supprimer le cookie : on repart de la première visite.

POUR ALLER PLUS LOIN

- Conserver chaque visite dans un petit journal.
""",
            "Lecture JSON": """SOLUTION

<?php
// Affiche la liste d'articles renvoyée par une API JSON.
$url = "https://api.exemple.org/articles";
$json = @file_get_contents($url);
$articles = []; $erreur = "";
if ($json === false) {
    $erreur = "Impossible de joindre le serveur.";
} else {
    $data = json_decode($json, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        $erreur = "JSON incorrect : " . json_last_error_msg();
    } elseif (is_array($data)) {
        $articles = $data;
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Lecture JSON</title></head>
<body>
<h1>Articles</h1>
<?php if ($erreur): ?><p><?= htmlspecialchars($erreur) ?></p>
<?php elseif (!$articles): ?><p>Réponse vide : aucun article.</p>
<?php else: ?>
<ul>
<?php foreach ($articles as $a): ?>
<li><h2><?= htmlspecialchars($a["titre"] ?? "Sans titre") ?></h2>
<p><?= htmlspecialchars($a["auteur"] ?? "Anonyme") ?></p></li>
<?php endforeach; ?>
</ul>
<?php endif; ?>
</body>
</html>

EXPLICATION

file_get_contents renvoie le corps de la réponse, ou false quand le
réseau a échoué : ce test doit venir en premier, sinon json_decode
reçoit false et signale une erreur trompeuse. true donne un tableau
associatif, plus commode qu'un objet pour foreach. Chaque champ est
lu avec un opérateur de repli : une clé absente déclencherait sinon
un avertissement PHP.

POINTS DE VÉRIFICATION

- Réponse correcte : titres et auteurs s'affichent en liste.
- Réseau coupé : message de serveur injoignable, sans erreur fatale.
- Réponse « coucou » : JSON incorrect avec le détail.

POUR ALLER PLUS LOIN

- Lire le code HTTP avant de traiter le corps de réponse.
""",
            "Connexion PDO": """SOLUTION

<?php
session_start();
$erreur = "";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $mail = trim($_POST["mail"] ?? "");
    $mdp = $_POST["mdp"] ?? "";
    try {
        $pdo = new PDO("mysql:host=localhost;dbname=babi", "utilisateur", "motdepasse",
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $q = $pdo->prepare("SELECT nom, mdp_hash FROM membres WHERE mail = ?");
        $q->execute([$mail]);
        $membre = $q->fetch();
        if ($membre && password_verify($mdp, $membre["mdp_hash"])) {
            $_SESSION["user"] = $membre["nom"];
            session_regenerate_id(true);
            header("Location: tableau-de-bord.php");
            exit;
        }
        $erreur = "Identifiants invalides.";
    } catch (PDOException $e) {
        $erreur = "Base de données indisponible.";
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Connexion</title></head>
<body>
<h1>Connexion</h1>
<?php if ($erreur): ?><p><?= htmlspecialchars($erreur) ?></p><?php endif; ?>
<form method="post">
<label>E-mail <input name="mail" type="email" required></label>
<label>Mot de passe <input name="mdp" type="password" required></label>
<button>Se connecter</button>
</form>
</body>
</html>

EXPLICATION

La requête est préparée avec un marqueur de position : la valeur
saisie est transmise séparément du SQL, ce qui rend l'injection
impossible. fetch renvoie false si aucun membre ne porte cet
e-mail, donc un même message couvre les deux échecs : on ne devine
pas si l'adresse existe. password_verify compare la saisie à
l'empreinte stockée, et session_regenerate_id change l'identifiant
de session contre la fixation.

POINTS DE VÉRIFICATION

- Bon couple : redirection vers le tableau de bord.
- Mauvais mot de passe et e-mail inconnu : même message.
- Piège : concaténer la saisie dans la requête ouvre l'injection.

POUR ALLER PLUS LOIN

- Basculer sur SQLite pour tester sans serveur MySQL.
""",
        },
    },
    "Swift": {
        "exercises": {
            "Premier playground": """SOLUTION

import Foundation

// Version de Swift détectée à l'exécution.
let version = "5.9"
print("Bonjour Swift !")
print("Swift \\(version)")
print("babi".uppercased())

EXPLICATION

Le playground exécute chaque ligne dès qu'elle est terminée, sans
commande de compilation : c'est le lieu d'essai avant un projet
réel. L'interpolation \\(expr) insère n'importe quelle expression
dans une chaîne, entre parenthèses après une antislash. Enfin
uppercased() renvoie une nouvelle chaîne en majuscules : les
chaînes Swift étant immuables, la valeur d'origine est intacte.

POINTS DE VÉRIFICATION

- Trois lignes affichées, dans l'ordre, la dernière entièrement en majuscules.
- Changer « 5.9 » change l'affichage, rien d'autre.
- Piège : une parenthèse non fermée casse la compilation.

POUR ALLER PLUS LOIN

- Afficher l'heure du jour avec Date().
- Stocker le message dans une constante puis le réutiliser.
""",
            "Convertisseur": """SOLUTION

import Foundation

enum Convertisseur {
    // Fonctions pures : ni état ni effet de bord.
    static func celsiusVersFahrenheit(_ c: Double) -> Double {
        c * 9 / 5 + 32
    }
    static func fahrenheitVersCelsius(_ f: Double) -> Double {
        (f - 32) * 5 / 9
    }
}

let c = Convertisseur.celsiusVersFahrenheit(0)
let f = Convertisseur.fahrenheitVersCelsius(98.6)
print(String(format: "%.1f", c))
print(String(format: "%.1f", f))

EXPLICATION

Les fonctions sont rattachées au type et s'appellent sur ce type :
aucune instance n'est nécessaire. Chacune prend un Double et en
renvoie un autre, sans modifier le monde extérieur, ce qui rend le
test unitaire immédiat. Les littéraux sont des Double, donc 9 / 5
vaut bien 1,8 : avec des Int, la division tronquerait à 1.
String(format: "%.1f") impose une décimale à l'affichage.

POINTS DE VÉRIFICATION

- 0 donne 32.0 et 100 donne 212.0 ; 98.6 donne 37.0.
- Aucune variable globale dans le calcul.
- Piège : écrire 9 / 5 avec des entiers perd la décimale.

POUR ALLER PLUS LOIN

- Ajouter la conversion kelvin avec la même structure.
- Lire une saisie au clavier grâce à readLine().
""",
            "Compteur pas à pas": """SOLUTION

struct Compteur {
    var valeur = 0
    // mutating autorise la méthode à modifier la struct elle-même.
    mutating func incrementer(par pas: Int = 1) { valeur += pas }
    mutating func decrementer(par pas: Int = 1) { valeur -= pas }
    mutating func remettreAZero() { valeur = 0 }
}

var compteur = Compteur()
compteur.incrementer()
compteur.incrementer()
compteur.decrementer()
print(compteur.valeur)
compteur.remettreAZero()
print(compteur.valeur)

EXPLICATION

Compteur est une structure : une copie de valeur, légère à créer.
Le mot-clé mutating figure dans la signature de chaque méthode qui
écrit dans valeur ; sans lui, le compilateur refuse la
modification. Le paramètre pas possède une valeur par défaut,
aussi incrementer() et incrementer(par: 5) passent toutes les deux.
La variable doit être déclarée var, jamais let : une constante
n'accepte aucune mutation.

POINTS DE VÉRIFICATION

- L'affichage donne 1 après les trois pas, puis 0 après la remise.
- compteur.incrementer(par: 10) ajoute dix d'un coup.
- Piège : let compteur = Compteur() interdit toute méthode mutating.

POUR ALLER PLUS LOIN

- Comparer avec une classe, où la mutation affecte toutes les références.
- Faire déléguer l'affichage à CustomStringConvertible.
""",
            "FizzBuzz": """SOLUTION

var sortie = ""
for i in 1...100 {
    // case multiple : un tuple comparé, _ accepte n'importe quoi.
    switch (i % 3, i % 5) {
    case (0, 0): sortie += "FizzBuzz "
    case (0, _): sortie += "Fizz "
    case (_, 0): sortie += "Buzz "
    default: sortie += "\\(i) "
    }
}
print(sortie)

EXPLICATION

L'intervalle 1...100 est fermé : les deux bornes sont atteintes.
Le switch reçoit un tuple des deux restes et le compare à des
motifs littéraux ; le trait bas accepte toute valeur à cette
position, ce qui permet d'exprimer la réunion des cas sans
condition imbriquée. La branche default reste obligatoire, Swift
exigeant que tous les cas soient couverts. La concatenation
accumule la ligne complète avant un seul affichage.

POINTS DE VÉRIFICATION

- La quatorzième valeur est FizzBuzz, la deuxième Buzz.
- Aucune sortie manquante : cent valeurs pour cent itérations.
- Piège : tester i % 15 en premier, sinon FizzBuzz devient Fizz.

POUR ALLER PLUS LOIN

- Afficher dix valeurs par ligne avec enumerated().
- Collecter dans un tableau puis utiliser joined(separator:).
""",
            "Compte bancaire": """SOLUTION

class CompteBancaire: CustomStringConvertible {
    let titulaire: String
    private(set) var solde: Double
    init(titulaire: String, solde: Double = 0) {
        self.titulaire = titulaire
        self.solde = solde
    }
    func deposer(_ montant: Double) {
        if montant > 0 { solde += montant }
    }
    func retirer(_ montant: Double) -> Bool {
        guard montant > 0, montant <= solde else { return false }
        solde -= montant
        return true
    }
    var description: String { "\\(titulaire) : \\(solde) euros" }
}

let compte = CompteBancaire(titulaire: "Babi")
compte.deposer(100)
print(compte.retirer(30), compte)
print(compte.retirer(500), compte)

EXPLICATION

Le compte est une classe, donc une référence : la variable copie
l'adresse, pas les données, et toute modification se voit partout.
private(set) rend la lecture publique mais l'écriture réservée à la
classe : de l'extérieur, forcer un solde ne compile pas, seul un
passage par dépôt ou retrait le change. guard arrête la méthode au
premier test qui échoue et renvoie false. La conformité à
CustomStringConvertible rend l'affichage lisible dans print.

POINTS DE VÉRIFICATION

- Dépôt de 100 puis retrait de 30 : solde 70, retour true.
- Retrait de 500 : false et solde inchangé.
- Piège : modifier solde hors de la classe refuse la compilation.

POUR ALLER PLUS LOIN

- Remplacer le Double par des centimes entiers, plus exacts.
- Dériver d'une classe et appeler super dans l'initialiseur.
""",
            "Décodage JSON": """SOLUTION

import Foundation

struct Produit: Decodable {
    let id: Int
    let nom: String
    let prix: Double
}

let brut = #"{"id": 7, "nom": "Clavier", "prix": 89.9}"#
let data = Data(brut.utf8)
if let produit = try? JSONDecoder().decode(Produit.self, from: data) {
    print("\\(produit.nom) : \\(produit.prix) euros")
} else {
    print("Format JSON invalide")
}

EXPLICATION

Le protocol Decodable demande seulement les propriétés : le
décodeur génère le reste à la compilation. Les noms des champs JSON
doivent correspondre à ceux des propriétés, sinon une clé
CodingKeys est nécessaire. try? transforme l'erreur éventuelle en
optionnel, ce qui évite un bloc do/catch quand aucun détail n'est
à afficher. La chaîne est écrite en littéral brut entre dièses : les
guillemets internes restent littéraux, sans échappement.

POINTS DE VÉRIFICATION

- Le JSON valide affiche « Clavier : 89.9 euros ».
- Un JSON tronqué bascule sur le message d'erreur, sans crash.
- Piège : un champ manquant rend le décodeur échouer.

POUR ALLER PLUS LOIN

- Décodez un tableau de produits avec [Produit].self.
- Choisir do/catch pour afficher la raison exacte de l'échec.
""",
            "Tri de personnes": """SOLUTION

struct Personne {
    let nom: String
    let age: Int
}

let monde = [Personne(nom: "Alice", age: 30),
             Personne(nom: "Bob", age: 25),
             Personne(nom: "Alice", age: 22)]

// Âge croissant, puis ordre alphabétique quand les âges sont égaux.
let tri = monde.sorted {
    $0.age != $1.age ? $0.age < $1.age : $0.nom < $1.nom
}
for personne in tri {
    print("\\(personne.nom), \\(personne.age) ans")
}

EXPLICATION

sorted renvoie un tableau neuf et laisse l'original intact :
reversed() ou sort() modifieraient ou inverseraient le résultat.
La fermeture reçoit deux éléments et répond vrai quand le premier
doit précéder le second ; $0 et $1 en sont les raccourcis. Le
ternaire compare d'abord les âges, puis débraye sur le nom quand
les âges sont égaux, ce qui donne un tri stable et sans doublon
visible.

POINTS DE VÉRIFICATION

- Alice 22, Bob 25, Alice 30 : trois lignes dans cet ordre.
- L'ordre d'origine n'est pas modifié.
- Piège : écrire < au lieu de != casse le départage par nom.

POUR ALLER PLUS LOIN

- Rendre Personne conforme à Comparable pour trier partout.
- Trier en ordre décroissant avec $0.age > $1.age.
""",
        },
    },
}
