"""Corrections commentées — lot 1 : Python, JavaScript, TypeScript.

Une entrée par exercice du curriculum (titre exact, copié-collé depuis
core/curriculum.py, clé "exercises" obligatoire) :

    CONTENT["Python"]["exercises"]["FizzBuzz"] = \"\"\"SOLUTION
    ...
    \"\"\"

Fusionnées dans core/solutions.py. Contrôle :
    python tests/check_solutions.py Python JavaScript TypeScript
"""
CONTENT = {
    "Python": {"exercises": {}},
    "JavaScript": {"exercises": {}},
    "TypeScript": {"exercises": {}},
}

CONTENT["Python"]["exercises"]["Salut le monde"] = """SOLUTION

message = "Bonjour, le monde !"
print(message)

auteur = "BabiProgrammeur"
print("Ce message vient de " + auteur + ".")

EXPLICATION

print() écrit le texte entre parenthèses dans la console, puis place le
curseur sur la ligne suivante. On range d'abord la phrase dans une
variable : elle reste réutilisable tout au long du programme. L'opérateur
+ colle les chaînes bout à bout, mais il exige que chaque morceau soit
déjà du texte : additionner un nombre à une chaîne provoque une erreur
TypeError.

POINTS DE VÉRIFICATION

- La console affiche d'abord Bonjour, le monde ! puis la seconde phrase.
- print(Bonjour) sans guillemets échoue : Bonjour serait lu comme une
  variable qui n'existe pas.
- print("Total : " + 3) échoue aussi : il faut str(3) ou un f-string.
- Deux print donnent deux lignes : il n'existe pas d'affichage côte à
  côte sans fin de ligne explicite.

POUR ALLER PLUS LOIN

- Réécrire la phrase avec un f-string, print(f"Message de {auteur} !"),
  plus lisible dès que plusieurs variables se mêlent au texte.
- Ajouter une saisie : prénom = input("Comment t'appelles-tu ? ") puis
  réutiliser la réponse dans le message affiché."""

CONTENT["Python"]["exercises"]["Calculatrice"] = """SOLUTION

a = float(input("Premier nombre : "))
b = float(input("Second nombre : "))

print("Somme :", a + b)
print("Différence :", a - b)
print("Produit :", a * b)

if b != 0:
    print("Quotient :", a / b)
else:
    print("Quotient : impossible, division par zéro")

EXPLICATION

input() renvoie toujours du texte : float() le transforme en nombre à
virgule, condition indispensable pour calculer. La forme
print("Somme :", valeur) insère automatiquement un espace entre les
éléments. La division mérite une vérification : diviser par zéro lève
ZeroDivisionError et arrête net le programme, donc on teste b != 0
avant d'utiliser l'opérateur de division.

POINTS DE VÉRIFICATION

- Avec 12 puis 4 : 16.0, 8.0, 48.0 et 3.0 (les résultats flottants
  s'affichent avec une décimale même quand le nombre est entier).
- Avec 5 puis 0 : les trois premières lignes passent, la dernière
  annonce l'impossibilité au lieu de planter.
- Saisir des lettres provoque ValueError à float() : la saisie n'est
  pas validée.
- Pour des entiers stricts, int(input(...)) remplace float().

POUR ALLER PLUS LOIN

- Ajouter le choix de l'opération avec input("Opération (+ - × ÷) : ")
  puis un couple de tests if / elif par symbole.
- Écrire une fonction resultats(a, b) qui renvoie les quatre valeurs :
  le code principal se réduit alors à un simple affichage."""

CONTENT["Python"]["exercises"]["FizzBuzz"] = """SOLUTION

for n in range(1, 101):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)

EXPLICATION

On teste d'abord le multiple de 15, car il réunit les deux règles : la
branche n % 15 == 0 est la seule à afficher FizzBuzz, et les elif
suivants ne sont même pas regardés. L'ordre des tests compte : si le
cas 3 venait avant le cas 15, le nombre 15 afficherait Fizz et FizzBuzz
ne sortirait jamais. L'opérateur % donne le reste de la division
entière : il vaut 0 exactement quand le nombre est divisible.

POINTS DE VÉRIFICATION

- 15, 30, 45, 60, 75 et 90 affichent FizzBuzz (6 occurrences).
- 3, 6 et 9 affichent Fizz ; 5, 10 et 20 affichent Buzz.
- 1 affiche 1 et 100 affiche Buzz (100 est multiple de 5).
- Avec trois if au même niveau, 15 affiche Fizz puis Buzz sur deux
  lignes : c'est l'erreur classique que les elif évitent.

POUR ALLER PLUS LOIN

- Ranger les règles dans une liste [(15, "FizzBuzz"), (3, "Fizz"),
  (5, "Buzz")] puis boucler dessus : ajouter une règle ne demande plus
  de toucher au code d'affichage."""

CONTENT["Python"]["exercises"]["Moyenne d'une liste"] = """SOLUTION

notes = [12, 15, 9, 18, 11]

total = 0
for note in notes:
    total = total + note

moyenne = total / len(notes)
print("Moyenne :", moyenne)  # 13.0

EXPLICATION

La moyenne vaut la somme des valeurs divisée par leur nombre. La
variable total s'initialise à 0 avant la boucle : placée à l'intérieur,
elle repartirait à zéro à chaque tour et ne garderait que la dernière
note. len(notes) renvoie l'effectif, et l'opérateur de division produit
toujours un flottant, même quand toutes les notes sont des entiers.

POINTS DE VÉRIFICATION

- Ici la somme vaut 65 pour 5 notes : l'affichage est 13.0.
- Une liste vide donnerait une division par zéro : on teste len(notes)
  si la saisie est facultative.
- total = total + note s'écrit aussi total += note, c'est exactement
  la même opération.
- sum(notes) / len(notes) obtient le même résultat en une seule ligne.

POUR ALLER PLUS LOIN

- Afficher aussi le minimum, le maximum et la médiane : min(notes),
  max(notes), puis la valeur centrale d'une copie triée.
- Arrondir l'affichage avec round(moyenne, 2) pour deux décimales."""

CONTENT["Python"]["exercises"]["Compteur de mots"] = """SOLUTION

texte = "le chat dort et le chat ronronne"
mot = "chat"

mots = texte.split()
compte = mots.count(mot)
print(mot, "apparaît", compte, "fois")  # chat apparaît 2 fois

EXPLICATION

split() découpe la phrase sur les espaces et rend une liste de mots :
« le », « chat », « dort », « et », « chat », « ronronne ». La méthode
count() de cette liste compare chaque élément au mot cherché et renvoie
le total. La comparaison est stricte et sensible à la casse : « Chat »
et « chat » restent deux éléments différents. Chercher une simple
sous-chaîne donnerait d'autres résultats.

POINTS DE VÉRIFICATION

- L'affichage est exactement : chat apparaît 2 fois.
- Remplacer mot par « ronronne » donne 1, par « chien » donne 0.
- Chercher « ch » renvoie 0 dans la liste, mais texte.count("ch")
  renvoie 2, car « ch » se trouve deux fois dans « chat ».
- Sans passer par lower(), un mot écrit en majuscule en début de
  phrase ne correspond jamais.

POUR ALLER PLUS LOIN

- Compter tous les mots d'un coup avec un dictionnaire, mot -> nombre,
  incrémenté à chaque tour d'une boucle for.
- Normaliser avant de découper : texte.lower().split() ignore la casse."""

CONTENT["Python"]["exercises"]["Convertisseur"] = """SOLUTION

celsius = float(input("Température en Celsius : "))

fahrenheit = celsius * 9 / 5 + 32
print(celsius, "°C équivalent à", fahrenheit, "°F")

retour = (fahrenheit - 32) * 5 / 9
print("Retour :", retour, "°C")

EXPLICATION

La formule vers Fahrenheit multiplie par 9, divise par 5 puis ajoute
32 : comme les multiplications passent avant les additions, le résultat
est juste sans parenthèse. La formule inverse doit être entièrement
parenthésée : sans elles, * et / passeraient avant - et le calcul serait
faux. float() transforme la saisie texte en nombre exploitable.

POINTS DE VÉRIFICATION

- 0 °C donne 32 °F et 100 °C donne 212 °F : les deux repères classiques.
- 37 °C donne 98.6 °F, la température du corps humain.
- Saisir 12,5 avec une virgule provoque ValueError : il faut un point.
- Le calcul de retour redonne la valeur de départ à l'unité près.

POUR ALLER PLUS LOIN

- Autoriser la virgule avec float(saisie.replace(",", ".")).
- Écrire deux fonctions vers_fahrenheit(c) et vers_celsius(f) puis les
  réutiliser dans un petit menu répétitif."""

CONTENT["Python"]["exercises"]["Nombre mystère"] = """SOLUTION

import random

mystere = random.randint(1, 100)
essais = 0

while True:
    proposition = int(input("Votre nombre : "))
    essais = essais + 1
    if proposition < mystere:
        print("Trop petit !")
    elif proposition > mystere:
        print("Trop grand !")
    else:
        print("Bravo, trouvé en", essais, "essais")
        break

EXPLICATION

randint(1, 100) inclut les deux bornes : 1 et 100 peuvent tomber. La
boucle tourne jusqu'à ce qu'une branche déclenche break, qui saute
immédiatement après la boucle : c'est la sortie du jeu. Chaque saisie
est convertie en entier, sinon on comparerait du texte à un nombre.
Les deux indices resserrent l'intervalle à chaque essai.

POINTS DE VÉRIFICATION

- Chaque indice coupe l'intervalle en deux : sept essais suffisent en
  théorie pour couvrir 100 valeurs.
- int("abc") lève ValueError : rien ne vérifie la saisie pour l'instant.
- Le compteur s'incrémente avant le test, la victoire est donc comptée.
- random.randrange(1, 100) exclurait 100, contrairement à randint.

POUR ALLER PLUS LOIN

- Limiter la partie à 7 essais avec une boucle for, puis annoncer la
  défaite quand la boucle se termine sans break.
- Envelopper la conversion dans un try / except pour rejeter les
  saisies non numériques sans planter."""

CONTENT["JavaScript"]["exercises"]["Message d'accueil"] = """SOLUTION

<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Accueil</title></head>
<body>
  <p id="accueil"></p>
  <script>
    const nom = "Léa";
    const message = "Bienvenue " + nom + " !";
    document.getElementById("accueil").textContent = message;
  </script>
</body>
</html>

EXPLICATION

Le paragraphe existe dans la page mais reste vide : c'est le script qui
lui donne son texte. getElementById renvoie l'élément portant l'identifiant
accueil, puis textContent écrit la chaîne dedans. Le script est placé
après le paragraphe, sans quoi l'élément n'existe pas encore au moment
de la recherche et la variable vaut null. const convient : nom ne change
pas ensuite.

POINTS DE VÉRIFICATION

- La page affiche exactement : Bienvenue Léa !
- Déplacer le script avant le paragraphe provoque l'erreur « ne peut
  pas lire les propriétés de null ».
- textContent montre le texte tel quel ; innerHTML interpréterait les
  balises éventuellement présentes dans la chaîne.
- Réaffecter nom ensuite lève une erreur, la constante est figée.

POUR ALLER PLUS LOIN

- Lire une saisie avec document.querySelector("#prenom") puis l'ajouter
  au message au moment du chargement.
- Accumuler du texte avec textContent += pour écrire plusieurs lignes
  sans écraser le paragraphe."""

CONTENT["JavaScript"]["exercises"]["Compteur de clics"] = """SOLUTION

<button id="bouton">Clics : 0</button>
<script>
  let compteur = 0;
  const bouton = document.getElementById("bouton");

  bouton.addEventListener("click", function () {
    compteur = compteur + 1;
    bouton.textContent = "Clics : " + compteur;
  });
</script>

EXPLICATION

addEventListener attache une fonction au clic : elle ne s'exécute pas
au chargement, mais à chaque fois que l'utilisateur clique. Elle lit
compteur, ajoute une unité, puis réécrit tout le libellé du bouton avec
la nouvelle valeur. let est obligatoire pour compteur, car const
interdit la réaffectation. L'écouteur reste en place : il rafraîchit le
bouton autant de fois que nécessaire.

POINTS DE VÉRIFICATION

- Après trois clics, le bouton affiche Clics : 3.
- bouton.onclick = fonction écrase l'écouteur précédent, contrairement
  à addEventListener qui en conserve plusieurs.
- Enregistrer deux fois le même écouteur ferait sauter le compteur de
  deux unités par clic.
- textContent remplace le libellé entier : le texte « Clics : » doit
  être réécrit à chaque appel.

POUR ALLER PLUS LOIN

- Placer le compte dans un <span> à côté du bouton pour ne jamais
  réécrire le libellé.
- Désactiver le bouton avec bouton.disabled = true après un nombre
  maximal de clics."""

CONTENT["JavaScript"]["exercises"]["FizzBuzz"] = """SOLUTION

for (let n = 1; n <= 100; n++) {
  if (n % 15 === 0) {
    console.log("FizzBuzz");
  } else if (n % 3 === 0) {
    console.log("Fizz");
  } else if (n % 5 === 0) {
    console.log("Buzz");
  } else {
    console.log(n);
  }
}

EXPLICATION

Le squelette est identique à la version Python : le multiple de 15 passe
en premier, sinon les tests suivants l'intercepteraient. L'opérateur %
donne le reste de la division entière, et === compare sans conversion de
type, à la différence de ==. La boucle for porte l'initialisation, la
condition et l'incrément sur la même ligne : n parcourt 1 à 100.

POINTS DE VÉRIFICATION

- 15 affiche FizzBuzz, 3 affiche Fizz, 5 affiche Buzz, 7 affiche 7.
- Trois if indépendants afficheraient Fizz puis Buzz sur deux lignes
  pour 15.
- console.log(100) affiche 100 sans guillemets : le nombre reste un
  nombre, « 100 » serait une chaîne de caractères.
- Écrire n < 100 au lieu de n <= 100 fait perdre la dernière ligne.

POUR ALLER PLUS LOIN

- Ranger les règles dans un tableau [[15, "FizzBuzz"], [3, "Fizz"],
  [5, "Buzz"]] et boucler dessus en gardant un booléen trouvé.
- Afficher dans la page en ajoutant un élément <li> à une liste <ul>
  au lieu de la console."""

CONTENT["JavaScript"]["exercises"]["Statistiques de notes"] = """SOLUTION

const notes = [12, 8, 15, 19, 6, 11];

let minimum = notes[0];
let maximum = notes[0];
let total = 0;

for (const note of notes) {
  if (note < minimum) minimum = note;
  if (note > maximum) maximum = note;
  total = total + note;
}

const moyenne = total / notes.length;
console.log("Min :", minimum, "Max :", maximum, "Moyenne :", moyenne);

EXPLICATION

Un seul parcours calcule les trois statistiques : la boucle for...of
donne chaque note, qu'on compare aux deux bornes et qu'on additionne.
minimum et maximum s'initialisent avec le premier élément ; les mettre
à 0 fausserait tout, car aucune note réelle ne serait inférieure à 0
dans ce jeu de données. La moyenne se calcule après la boucle, une fois
la somme complète, en divisant par notes.length.

POINTS DE VÉRIFICATION

- La somme vaut 71 pour 6 notes : min 6, max 19, moyenne 11.83 environ.
- Des bornes initialisées à 0 renverraient 0 au lieu de 6.
- Un tableau vide donnerait NaN, à savoir 0 divisé par 0 : on teste
  length avant de diviser.
- Math.min(...notes) et Math.max(...notes) donnent les mêmes valeurs en
  une ligne, sans boucle.

POUR ALLER PLUS LOIN

- Regrouper le tout dans un objet { min, max, moyenne } renvoyé par une
  fonction statistiques(tableau).
- Calculer la médiane sur une copie triée : [...notes].sort((a, b) =>
  a - b)."""

CONTENT["JavaScript"]["exercises"]["Liste de tâches"] = """SOLUTION

<input id="tache">
<button id="ajout">Ajouter</button>
<ul id="liste"></ul>

<script>
  const champ = document.getElementById("tache");
  const liste = document.getElementById("liste");

  document.getElementById("ajout").addEventListener("click", function () {
    const texte = champ.value.trim();
    if (texte === "") return;

    const item = document.createElement("li");
    item.textContent = texte;

    const bouton = document.createElement("button");
    bouton.textContent = "Supprimer";
    bouton.addEventListener("click", function () {
      item.remove();
    });

    item.appendChild(bouton);
    liste.appendChild(item);
    champ.value = "";
  });
</script>

EXPLICATION

Chaque clic fabrique un élément en mémoire, le remplit, y greffe son
propre bouton puis l'insère avec appendChild. Le bouton Supprimer naît
avec la ligne : sa fonction ferme sur item, la ligne à effacer. trim()
écarte les saisies vides, le champ est ensuite vidé.

POINTS DE VÉRIFICATION

- Saisir « pain » puis cliquer ajoute une ligne avec son bouton.
- Une saisie vide ou d'espaces seule est ignorée.
- Chaque bouton Supprimer n'efface que sa ligne, grâce à la fermeture
  sur item.
- Oublier champ.value = "" laisse l'ancien texte à la saisie suivante.

POUR ALLER PLUS LOIN

- Vider tout d'un coup avec liste.innerHTML = "".
- Conserver les tâches dans localStorage après rechargement."""

CONTENT["JavaScript"]["exercises"]["Recherche produit"] = """SOLUTION

const produits = [
  { nom: "Clavier", prix: 45, categorie: "informatique" },
  { nom: "Souris", prix: 25, categorie: "informatique" },
  { nom: "Bureau", prix: 120, categorie: "meuble" },
  { nom: "Chaise", prix: 40, categorie: "meuble" }
];

const filtres = produits.filter(function (p) {
  return p.categorie === "informatique" && p.prix <= 50;
});

const noms = filtres.map(function (p) { return p.nom; });
console.log(noms);  // ["Clavier", "Souris"]

EXPLICATION

filter parcourt le tableau et garde les objets pour lesquels la fonction
renvoie true : le tableau d'origine n'est pas touché, on obtient une
copie filtrée. La condition réunit deux critères avec && : il faut la
bonne catégorie et un prix inférieur ou égal à 50. map transforme ensuite
chaque objet retenu en son seul nom, ce qui donne une liste de texte
prête à afficher.

POINTS DE VÉRIFICATION

- Deux objets passent : Clavier et Souris. La Chaise, bien que sous 50,
  est un meuble.
- Avec || à la place de &&, la Chaise passerait aussi : le filtre
  deviendrait trop large.
- Une callback sans return renvoie undefined et vide le résultat.
- Le tableau produits reste intact : filtres est une nouvelle liste.

POUR ALLER PLUS LOIN

- Lire un champ input et filtrer à chaque frappe avec
  p.nom.toLowerCase().indexOf(mot) !== -1.
- Trier les retenus par prix avec filtres.sort((a, b) => a.prix - b.prix)."""

CONTENT["JavaScript"]["exercises"]["Mini-jeu"] = """SOLUTION

const mystere = Math.floor(Math.random() * 100) + 1;
const maximum = 7;
let essais = 0;
let trouve = false;

while (essais < maximum) {
  const saisie = prompt("Votre nombre (1 à 100) :");
  if (saisie === null) break;

  essais = essais + 1;
  const proposition = Number(saisie);

  if (proposition < mystere) {
    alert("Trop petit ! Essai " + essais + "/" + maximum);
  } else if (proposition > mystere) {
    alert("Trop grand ! Essai " + essais + "/" + maximum);
  } else {
    alert("Bravo en " + essais + " essais !");
    trouve = true;
    break;
  }
}

if (!trouve) {
  alert("Perdu, le nombre était " + mystere);
}

EXPLICATION

Math.random() va de 0 à 1 exclu : après multiplication et arrondi on
obtient 0 à 99, et le +1 décale sur 1 à 100. La boucle s'arrête seule
après 7 tours. Le drapeau trouve distingue une victoire au dernier essai
d'une défaite : sans lui, le message Perdu s'afficherait aussi après une
réussite.

POINTS DE VÉRIFICATION

- Le nombre tiré est toujours entier, de 1 à 100 inclus.
- Réussir au 7e essai affiche Bravo et trouve empêche le message de
  défaite.
- Annuler prompt() renvoie null : Number(null) donnerait 0 et mentirait.
- Saisir 0 ou 1000 consomme quand même un essai.

POUR ALLER PLUS LOIN

- Remplacer prompt et alert par des champs et boutons de la page.
- Dichotomie : couper l'intervalle en deux à chaque essai, 7 suffisent."""

CONTENT["TypeScript"]["exercises"]["Typer une fonction"] = """SOLUTION

function bonjour(nom: string): string {
  return "Bonjour " + nom + " !";
}

function addition(a: number, b: number): number {
  return a + b;
}

console.log(bonjour("Léa"));  // Bonjour Léa !
console.log(addition(3, 4));  // 7

EXPLICATION

Les annotations décrivent les types des paramètres et celui du retour.
Le compilateur les vérifie avant toute exécution : un appel
bonjour(42) est refusé même si la ligne ne s'exécute jamais. Le type de
retour peut être omis, tsc le déduit du return, mais l'écrire documente
la fonction. À la compilation, ces mots sont effacés : le JavaScript
produit ne contient plus que des valeurs.

POINTS DE VÉRIFICATION

- bonjour("Léa") affiche Bonjour Léa ! et addition(3, 4) affiche 7.
- addition("3", 4) est refusé : string n'est pas number. En JavaScript
  simple, le résultat serait « 34 » sans aucun avertissement.
- Une branche sans return provoque une erreur quand le type de retour
  est annoncé : le chemin manquant est détecté.
- Oublier l'annotation du paramètre laisse le type implicite any selon
  la configuration, ce qui neutralise la protection.

POUR ALLER PLUS LOIN

- Ajouter une valeur par défaut, function bonjour(nom: string =
  "monde"), pour autoriser bonjour() sans argument.
- Vérifier tout le projet sans produire de fichier : tsc --noEmit."""

CONTENT["TypeScript"]["exercises"]["Profil utilisateur"] = """SOLUTION

interface Utilisateur {
  id: number;
  nom: string;
  email: string;
  admin: boolean;
}

const lea: Utilisateur = {
  id: 1,
  nom: "Léa",
  email: "lea@example.fr",
  admin: false
};

lea.admin = true;
console.log(lea.nom);  // Léa

EXPLICATION

Une interface décrit la forme exacte d'un objet : chaque propriété doit
exister et porter le bon type. L'objet littéral affecté à lea doit
satisfaire ce contrat, ni plus ni moins, car TypeScript contrôle les
littéraux affectés à une variable typée. const empêche de réaffecter la
variable lea, mais n'empêche pas de modifier ses propriétés : ce n'est
pas un objet gelé.

POINTS DE VÉRIFICATION

- Omettre email déclenche une erreur : propriété manquante.
- Écrire admin: "oui" est refusé : boolean attendu, pas string.
- Ajouter age: 30 au littéral est refusé : propriété inconnue du type.
- const lea n'interdit pas lea.admin = true ; seule une réaffectation
  complète, lea = {...}, est bloquée.

POUR ALLER PLUS LOIN

- Rendre un champ optionnel avec admin?: boolean pour les profils
  simples.
- Définir type MiseAJour = Partial<Utilisateur> pour un formulaire qui
  n'envoie que certains champs."""

CONTENT["TypeScript"]["exercises"]["Convertisseur JSON"] = """SOLUTION

interface Mesure {
  nom: string;
  poids: number;
}

function versMesure(brut: string): Mesure {
  const obj = JSON.parse(brut) as Record<string, unknown> | null;
  if (obj === null || typeof obj.nom !== "string"
      || typeof obj.poids !== "number") {
    throw new Error("Champs nom (texte) et poids (nombre) attendus");
  }
  return { nom: obj.nom, poids: obj.poids };
}

console.log(versMesure('{"nom": "brique", "poids": 2.5}'));

EXPLICATION

JSON.parse accepte tout JSON valide et ne garantit rien de la structure
attendue. L'assertion as Record<string, unknown> | null ne vérifie rien :
elle permet seulement de lire des propriétés de type unknown.
Le test obj === null traite le JSON null, puis typeof contrôle chaque
champ et le transforme en string ou number, ce qui autorise le return.
Sans cette étape, la faille n'apparaîtrait qu'à l'exécution.

POINTS DE VÉRIFICATION

- Un objet sans nom, ou avec poids en texte, déclenche l'erreur avant
  le return.
- JSON.parse sur du texte corrompu lève SyntaxError avant validation.
- typeof null vaut « object » : sans le premier test, la lecture des
  propriétés planterait.
- L'interface garantit la sortie, pas l'entrée : elle ne prouve rien du
  JSON.

POUR ALLER PLUS LOIN

- Ajouter un champ unite?: string pour tolérer des mesures sans unité.
- Confier la validation à zod quand les objets deviennent profonds."""

CONTENT["TypeScript"]["exercises"]["Cache générique"] = """SOLUTION

class Cache<K, V> {
  private entrees = new Map<K, V>();

  obtenir(cle: K): V | undefined {
    return this.entrees.get(cle);
  }

  poser(cle: K, valeur: V): void {
    this.entrees.set(cle, valeur);
  }

  taille(): number {
    return this.entrees.size;
  }
}

const nombres = new Cache<string, number>();
nombres.poser("un", 1);
console.log(nombres.obtenir("un"));  // 1

EXPLICATION

K et V sont des paramètres de type : la classe ne choisit pas les types
qu'elle manipule, elle les laisse décider à l'appel. L'instanciation
fige K en string et V en number pour toute la variable nombres. Map
impose des clés de type K, et le retour V | undefined traduit le fait
qu'une clé peut manquer. private interdit d'atteindre la map de
l'extérieur : tout passe par les méthodes.

POINTS DE VÉRIFICATION

- nombres.poser("un", "deux") est refusé : V vaut number ici.
- nombres.poser(1, 1) est refusé : K vaut string.
- obtenir("inconnu") renvoie undefined, jamais une erreur : on teste
  if (v === undefined) avant d'utiliser la valeur.
- new Cache<number, string>() réutilise la même classe pour d'autres
  types, sans écrire une seconde classe.

POUR ALLER PLUS LOIN

- Ajouter supprimer(cle: K): boolean qui renvoie true si la clé
  existait déjà.
- Limiter la taille : refuser l'écriture quand entrees.size atteint une
  borne maximale."""

CONTENT["TypeScript"]["exercises"]["États d'une commande"] = """SOLUTION

type Commande =
  | { statut: "en attente"; paiement: string }
  | { statut: "expédiée"; suivi: string }
  | { statut: "livrée"; signature: boolean };

function resume(c: Commande): string {
  switch (c.statut) {
    case "en attente":
      return "Paiement " + c.paiement + " en cours";
    case "expédiée":
      return "Suivi numéro " + c.suivi;
    case "livrée":
      return c.signature ? "Livrée et signée" : "Livrée à réclamer";
  }
}

console.log(resume({ statut: "expédiée", suivi: "FR123" }));

EXPLICATION

Le type est une union discriminée par statut : chaque membre porte une
valeur littérale différente. Dans une branche du switch, TypeScript
restreint c au membre correspondant : dans case "expédiée", seules
statut et suivi existent. Ce narrowing remplace les tests imbriqués de
JavaScript.

POINTS DE VÉRIFICATION

- Dans case "expédiée", c.paiement est refusé : cette propriété
  n'existe pas sur ce membre de l'union.
- resume({ statut: "expédiée" }) est refusé aussi : suivi manque.
- Oublier un cas laisse la fin de fonction atteignable alors que string
  est annoncé : tsc le signale.
- Des if imbriqués exigeraient de retester c.statut à chaque niveau.

POUR ALLER PLUS LOIN

- Ajouter une branche default qui déclare const jamais: never = c pour
  prouver que tous les cas sont traités.
- Ajouter un statut « annulée » : tsc repère les endroits à compléter."""

CONTENT["TypeScript"]["exercises"]["Corriger un bug"] = """SOLUTION

function moyenne(notes: number[]): number {
  if (notes.length === 0) return 0;
  let total = 0;
  for (const note of notes) {
    total += note;
  }
  return total / notes.length;
}

const saisie = "12, 15, 9";
const liste = saisie.split(", ").map(function (valeur) {
  return Number(valeur);
});

console.log(moyenne(liste));  // 12

EXPLICATION

L'erreur ne venait pas de la fonction mais de son appel : on lui passait
la chaîne entière alors que le paramètre annonce un tableau de nombres.
Deux solutions existent, mais changer le type du paramètre en string
déplacerait simplement le problème et ferait perdre la garantie du
typage. On convertit donc la saisie : split découpe sur le séparateur et
map(Number) transforme chaque morceau. La compilation détecte le bug
avant même l'exécution.

POINTS DE VÉRIFICATION

- Le message « not assignable to type number[] » disparaît dès que la
  conversion se fait à l'appel.
- split(", ") doit correspondre au séparateur réel : « 12,15 » exige
  split(",").
- Number("") vaut 0 : une valeur vide dans la saisie fausse la moyenne
  au lieu de planter.
- Le garde-fou sur notes.length évite une division par zéro, NaN.

POUR ALLER PLUS LOIN

- Remplacer la boucle par notes.reduce((somme, n) => somme + n, 0).
- Écrire le paramètre en readonly number[] pour interdire toute
  modification du tableau dans la fonction."""

CONTENT["TypeScript"]["exercises"]["Réponse d'API"] = """SOLUTION

interface Article {
  id: number;
  titre: string;
  vues: number;
  auteur: { nom: string; ville: string };
  tags: string[];
}

async function charger(url: string): Promise<Article> {
  const reponse = await fetch(url);
  if (!reponse.ok) throw new Error("HTTP " + reponse.status);
  const donnees = (await reponse.json()) as Article;
  return donnees;
}

charger("https://exemple.fr/api/article").then(function (article) {
  console.log(article.titre, article.auteur.ville);
});

EXPLICATION

La fonction async accepte await : la promesse se résout et le code
enchaîne normalement. fetch ne rejette pas sur une erreur HTTP : un
404 renvoie une promesse tenue, d'où le contrôle de reponse.ok avant de
parler JSON. L'assertion as Article ne vérifie rien à l'exécution : elle
donne une forme aux données, et c'est l'interface qui décrit cette
forme.

POINTS DE VÉRIFICATION

- Sans l'assertion, reponse.json() vaut any : aucune faute n'est
  détectée.
- article.auteur.ville n'existe que parce que l'interface le décrit.
- Une promesse rejetée casse le then : en async, un try / catch la
  capture.
- Retirer un champ de l'interface ne change pas le JSON, mais son accès
  devient refusé.

POUR ALLER PLUS LOIN

- Envelopper l'appel dans try / catch pour signaler un échec réseau à
  l'utilisateur.
- Rendre un champ optionnel, vues?: number, si l'API peut l'omettre."""
