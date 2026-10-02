"""Fiches de contenu — lot 1 : Python, JavaScript, TypeScript.

Clés : CONTENT[langage][kind][titre exact de l'élément du curriculum].
Format texte brut (aucun balisage) : en-têtes en capitales, tirets, exemples.
"""
from __future__ import annotations

CONTENT = {
    "Python": {
        "lessons": {
            "Variables et types": """OBJECTIFS
- déclarer des variables et connaître les types de base
- convertir d'un type à l'autre sans provoquer d'erreur
- afficher des valeurs de façon lisible

POINTS CLÉS
- le type suit la valeur : 30 est un int, 9.99 un float, « salut » un str
- types de base : int, float, str, bool, None
- str() convertit en texte, int() / float() convertissent en nombre
- f"{var} ..." intègre une variable dans une chaîne
- type(x) affiche le type d'une valeur
- une variable change de type : x = 5 puis x = « 5 »
- bool se convertit : int(True) vaut 1, float(False) vaut 0.0

EXEMPLE
age = 30
prix = 9.99
etudiant = True
message = f"{age} ans, prix de {prix} euros"
print(message)                  # 30 ans, prix de 9.99 euros
print(type(age), type(prix))    # <class 'int'> <class 'float'>

nb = "42"
total = int(nb) + 8             # 50 : on convertit avant d'additionner
print(float(nb), str(total))    # 42.0 50

EN PRATIQUE
Les saisies clavier arrivent en texte : convertissez avant de calculer
(prix, scores, âges), puis reconvertissez pour afficher.

PIÈGES À ÉVITER
- int("12.5") lève une ValueError : passez par float() d'abord
- == compare, = affecte : confusion classique
- « age : » + 30 plante : écrivez str(30) ou une f-string

À RETENIR
- le type dépend de la valeur, pas du nom de la variable
- convertir tôt évite les erreurs plus loin
- f"{x}" affiche n'importe quoi simplement
""",
            "Conditions": """OBJECTIFS
- structurer un programme avec if / elif / else
- maîtriser les opérateurs de comparaison et les opérateurs logiques
- éviter les pièges d'égalité et d'indentation

POINTS CLÉS
- opérateurs de comparaison : == != < > <= >=
- opérateurs logiques : and, or, not (priorité : not, puis and, puis or)
- un bloc se reconnaît à son indentation (4 espaces) et se termine par :
- elif veut dire « else if » : on enchaîne les tests
- if / elif / else ne font tourner qu'un seul bloc
- le ternaire resultat = a if test else b écrit un résultat en une ligne
- in teste l'appartenance : if jour in ("samedi", "dimanche")

EXEMPLE
note = 14
if note >= 16:
    mention = "excellent"
elif note >= 10:
    mention = "admissible"
else:
    mention = "à revoir"

age = 17
jour = "samedi"
if age >= 18 and jour in ("samedi", "dimanche"):
    print("vous pouvez entrer")
else:
    print("fermé")

EN PRATIQUE
Derrière un bouton « Valider », on teste les champs saisis avant d'envoyer
quoi que ce soit au serveur : chaque refus a son test et son message.

PIÈGES À ÉVITER
- = affecte et == compare : « if x = 5 » est une SyntaxError
- None se teste avec « is None », pas avec ==
- oublier les deux points après if provoque une IndentationError

À RETENIR
- un seul bloc s'exécute : le premier test qui est vrai
- comparer se fait avec ==, affecter avec =
- prévoir un else évite les silences inexplicables
""",
            "Boucles": """OBJECTIFS
- répéter des instructions avec for et while
- contrôler le flux avec break, continue et else de boucle
- parcourir des séquences proprement

POINTS CLÉS
- for parcourt une liste, une chaîne, un dict ou range(a, b, pas)
- range(1, 6) produit 1 2 3 4 5 : la borne de fin est exclue
- while répète tant que la condition reste vraie
- break sort de la boucle la plus proche
- continue saute directement à l'itération suivante
- else de boucle suit une boucle terminée sans break
- enumerate() donne l'indice et l'élément, zip parcourt deux séquences à la fois

EXEMPLE
for i in range(1, 6):
    if i == 3:
        continue
    print(i)              # 1 2 4 5

somme = 0
while somme < 10:
    somme += 2
print(somme)              # 10

for lettre in "babi":
    if lettre == "b":
        break
    print(lettre)         # rien : break sort avant la première ligne

EN PRATIQUE
On parcourt des commandes, des lignes de fichier ou des résultats :
for quand la quantité est connue, while quand elle dépend d'une condition.

PIÈGES À ÉVITER
- range(len(liste)) : préférez enumerate(liste)
- une while dont la condition ne change jamais tourne à l'infini : Ctrl+C
- modifier une liste pendant le parcours crée des sauts : construisez-en une nouvelle

À RETENIR
- for si le nombre d'itérations est connu, while sinon
- break interrompt, continue saute : ni l'un ni l'autre n'arrête le programme
""",
            "Fonctions": """OBJECTIFS
- regrouper du code réutilisable dans une fonction
- passer des paramètres et renvoyer un résultat
- comprendre la portée des variables

POINTS CLÉS
- def nom(param): deux points, puis return à l'indentation du def
- paramètres par défaut : def moyenne(notes, arrondi=1)
- return renvoie une valeur ; sans return, la fonction renvoie None
- portée locale : la variable disparaît à la fin de la fonction
- les paramètres sont locaux, global pour une variable externe
- docstring pour documenter la fonction
- lambda écrit une fonction minuscule, pour les cas simples

EXEMPLE
def moyenne(notes, arrondi=1):
    \"\"\"Moyenne des notes, 0 si la liste est vide.\"\"\"
    if not notes:
        return 0
    resultat = sum(notes) / len(notes)
    return round(resultat, arrondi)

print(moyenne([12, 15, 9]))     # 12.0
print(moyenne([10, 11], 2))     # 10.5

EN PRATIQUE
Une application découpe son travail : lire_saisie(), calculer_total(),
afficher_recap(). Une fonction se nomme en verbe et se teste seule.

PIÈGES À ÉVITER
- un if sans else peut renvoyer None : ajoutez un return
- oublier les deux points après def provoque une SyntaxError
- modifier une variable extérieure demande global, à éviter si possible

À RETENIR
- une fonction = une responsabilité, un nom en verbe, un return lisible
- sans return, la fonction renvoie None
- une docstring courte épargne des explications
""",
            "Listes et dictionnaires": """OBJECTIFS
- stocker des séquences ordonnées (list) et des paires clé-valeur (dict)
- parcourer, filtrer et transformer avec les compréhensions
- choisir la bonne structure selon le besoin

POINTS CLÉS
- list : ordonnée, modifiable, indexée à partir de 0, négatifs aussi
- [:3] prend le début, [1:] saute le premier, [:] copie la liste
- dict : recherche instantanée par clé, ordre conservé
- dict.get(clé, défaut) évite la KeyError d'une clé absente
- append() en fin, insert() insère, remove() par valeur, pop() par index
- sorted(liste) renvoie une copie triée, .sort() trie sur place
- compréhension : [x * 2 for x in liste if x > 0], même idée avec { } et ( )
- len() compte, in teste, + concatène deux listes

EXEMPLE
notes = {"alice": 15, "bob": 12}
notes["carla"] = 17
gagnants = [n for n, v in notes.items() if v >= 15]
print(gagnants)               # ["alice", "carla"]
print(notes.get("dan", 0))    # 0 : clé absente

EN PRATIQUE
Un panier reste une liste de dictionnaires produits (nom, prix, stock).
On le filtre avec une compréhension et on trie avant l'affichage.

PIÈGES À ÉVITER
- notes["dan"] lève une KeyError : utilisez get()
- réaffecter une liste dans une fonction ne change pas l'original
- incrémenter une clé absente plante : initialisez-la d'abord à 0

À RETENIR
- liste pour l'ordre, dictionnaire pour la recherche par clé
- get() et sorted() règlent la plupart des soucis
""",
            "Fichiers": """OBJECTIFS
- lire un fichier texte sans le charger entièrement en mémoire
- écrire ou ajouter du contenu de façon sûre
- fermer proprement les fichiers

POINTS CLÉS
- with open(...) as f : fermeture automatique, même en cas d'erreur
- modes : "r" lecture, "w" écriture (écrase), "a" ajout en fin
- encoding="utf-8" explicite : sinon les accents cassent selon la machine
- f.read() tout, f.readline() une ligne, une boucle for = lignes
- f.write() n'ajoute pas de saut de ligne : écrivez \\n vous-même
- un chemin relatif dépend du répertoire de lancement

EXEMPLE
with open("notes.txt", encoding="utf-8") as f:
    for ligne in f:
        print(ligne.strip())   # strip retire le saut de ligne

with open("sortie.txt", "w", encoding="utf-8") as f:
    f.write("bonjour\\n")
    f.write("tout le monde\\n")

with open("journal.txt", "a", encoding="utf-8") as f:
    f.write("nouvelle partie\\n")   # s'ajoute à la fin

EN PRATIQUE
Scores, préférences et journaux : tout ce qui doit survivre à la fermeture
du programme est enregistré dans un fichier.

PIÈGES À ÉVITER
- le mode "w" efface tout au premier write : pensez à "a" pour ajouter
- ouvrir sans with : une exception plus tard laisse le fichier verrouillé
- sans encoding="utf-8", les accents cassent sous Windows

À RETENIR
- toujours with open(...) as f
- "r" lit, "w" remplace, "a" ajoute
- strip() évite les sauts de ligne parasites
""",
            "Erreurs": """OBJECTIFS
- anticiper les erreurs avec try / except
- lever soi-même des exceptions avec raise
- distinguer les cas prévus des vrais bugs

POINTS CLÉS
- except TypeError: cible un type précis ; plusieurs s'enchaînent
- else si aucune exception, finally dans tous les cas
- raise ValueError("message") signale un problème de données
- on lève où elle se produit, on gère où on peut corriger
- except Exception attrape presque tout, jamais un vide
- la traceback se lit de bas en haut : la dernière ligne nomme le coupable

EXEMPLE
try:
    age = int(input("âge : "))
except ValueError:
    print("nombre invalide")
else:
    print(f"vous avez {age} ans")
finally:
    print("fin de la saisie")

def saluer(age):
    if age < 0:
        raise ValueError("l'âge ne peut pas être négatif")
    print(f"bonjour, {age} ans")

EN PRATIQUE
Lire un champ saisi par l'utilisateur ou une réponse réseau : on prévoit
l'erreur de format, puis on laisse les vrais bugs remonter avec leur traceback.

PIÈGES À ÉVITER
- except: sans type masque tout, y compris les interruptions du clavier
- attraper sans rien faire : le plan échoue plus loin, sans indice
- lever puis attraper juste en dessous : c'est du code inutile

À RETENIR
- attraper précisément, message utile, correction possible
- finally s'exécute toujours : idéal pour fermer un fichier
- une exception non gérée affiche sa traceback : lisez-la
""",
            "Modules et paquets": """OBJECTIFS
- découper un programme en modules réutilisables
- importer la bibliothèque standard et des paquets externes
- comprendre l'organisation pip / dossiers

POINTS CLÉS
- import math puis math.sqrt(9) : le module reste qualifié
- from random import randint importe un nom précis
- un .py est un module, un dossier avec __init__.py un paquet
- pip install nom_paquet installe un paquet externe
- pip freeze > requirements.txt fige les versions installées
- if __name__ == "__main__": n'exécute que si on lance ce fichier
- la stdlib suffit souvent : math, random, datetime, json

EXEMPLE
import math
from datetime import date

print(math.pi)               # 3.141592653589793
print(date.today().year)

def formater(prix):          # dans utils.py
    return f"{prix:.2f} euros"

from utils import formater   # import du module
print(formater(9.5))         # 9.50 euros

EN PRATIQUE
Une application se découpe en briques : base_de_donnees.py,
interfaces.py, calculs.py, chacun testable seul.

PIÈGES À ÉVITER
- from module import * : illisible, importez les noms utiles
- un import en bas de fichier crée des imports circulaires : remontez-le
- un dossier nommé comme un module standard casse les imports

À RETENIR
- imports en haut, modules en minuscules
- la bibliothèque standard d'abord, pip ensuite
- __name__ == "__main__" rend le module exécutable
""",
        },
        "exercises": {
            "Salut le monde": """ÉNONCÉ
- afficher « Bonjour le monde ! » à l'écran, puis saluer personnellement la personne qui lance le programme.
- le programme se joue en deux temps : un message fixe, puis une phrase construite à partir de la saisie.
- on y découvre print(), input() et l'insertion d'une variable dans une phrase.

ÉTAPES
1. écrire un print avec le message fixe « Bonjour le monde ! »
2. demander un nom avec input() et stocker la réponse dans une variable
3. afficher une phrase de bienvenue contenant ce nom
4. afficher le nombre de lettres du nom avec len()
5. tester avec un nom vide pour vérifier que tout s'affiche quand même

RÉSULTAT ATTENDU
- Bonjour le monde !
- Entrez votre nom : Babi
- Bonjour Babi !
- votre nom contient 4 lettres

POUR TESTER
- lancez le programme avec « Alice » puis avec « ada lovelace » : la phrase doit s'adapter
- vérifiez qu'aucune accolade ni guillemet parasite n'apparaît dans la sortie
- validez un champ vide : le programme doit afficher un résultat sans planter

INDICE
- input() renvoie toujours du texte : aucune conversion n'est nécessaire ici, et len() fonctionne directement sur la chaîne obtenue.
""",
            "Calculatrice": """ÉNONCÉ
- proposer les quatre opérations (+ - * /) sur deux nombres saisis, avec gestion de la division par zéro.
- l'utilisateur saisit les deux nombres puis le symbole de l'opération à effectuer.
- le programme affiche le résultat, ou un message d'erreur clair quand la saisie est invalide.

ÉTAPES
1. lire deux nombres et les convertir en float
2. demander l'opérateur parmi + - * /
3. vérifier que l'opérateur fait partie des quatre attendus
4. appliquer l'opération correspondante
5. afficher le résultat arrondi à 2 décimales
6. afficher « division impossible » si le diviseur vaut 0

RÉSULTAT ATTENDU
- 12 / 4 donne 3.0 ; 5 + 3 donne 8.0 ; 7 * 6 donne 42.0
- 7 / 0 affiche « division impossible »
- un opérateur comme % affiche « opération inconnue »

POUR TESTER
- essayez les quatre opérations avec des nombres négatifs et décimaux (−2.5 * 4)
- testez 10 / 0, puis une saisie non numérique comme « dix »
- aucun cas ne doit afficher de traceback : tout est signalé par un message

INDICE
- un dictionnaire {op: fonction} évite une longue chaîne de if ; pensez à vérifier le diviseur avant d'appeler la division.
""",
            "FizzBuzz": """ÉNONCÉ
- afficher de 1 à 100 : « Fizz » pour les multiples de 3, « Buzz » pour ceux de 5, « FizzBuzz » pour les deux.
- un classique des tests de logique : l'ordre dans lequel on écrit les conditions décide du résultat.
- seul l'affichage change, la suite des nombres reste intacte.

ÉTAPES
1. boucler de 1 à 100 inclus avec range(1, 101)
2. calculer les deux tests : multiple de 3 et multiple de 5
3. traiter d'abord le cas où les deux sont vrais (FizzBuzz)
4. sinon tester le multiple de 3, puis celui de 5
5. sinon afficher le nombre lui-même
6. vérifier le total des FizzBuzz affichés

RÉSULTAT ATTENDU
- 1 2 Fizz 4 Buzz Fizz 7 8 Fizz 11 Buzz 12 Fizz 14 FizzBuzz 16 ...
- 9 affiche Fizz, 10 affiche Buzz, 15 affiche FizzBuzz
- FizzBuzz apparaît 6 fois (15, 30, 45, 60, 75, 90)

POUR TESTER
- la dixième ligne doit afficher Buzz et la quinzième FizzBuzz
- les Buzz doivent être 20 au total, les Fizz 33
- réduisez d'abord la boucle à 1 à 20 pour lire la sortie sans vous perdre

INDICE
- le modulo % donne le reste : 15 % 3 vaut 0. Si vous testez 3 avant 15, le nombre 15 affichera « Fizz » au lieu de « FizzBuzz ».
""",
            "Moyenne d'une liste": """ÉNONCÉ
- calculer la moyenne d'une liste de notes, sans planter si la liste est vide.
- la fonction renvoie 0 quand il n'y a aucune note, et arrondit le résultat à 1 décimale.
- on suppose des notes déjà saisies et converties en nombres.

ÉTAPES
1. définir une fonction moyenne(notes)
2. vérifier en premier si la liste est vide et renvoyer 0
3. sinon diviser sum(notes) par len(notes)
4. arrondir le résultat à 1 décimale avec round()
5. afficher la moyenne, puis la conserver dans un tableau de suivi

RÉSULTAT ATTENDU
- [12, 15, 9] donne 12.0
- [] donne 0
- [10] donne 10.0
- [8, 9, 10, 11] donne 9.5

POUR TESTER
- testez la liste vide en premier : c'est le cas qui plante le plus souvent
- une seule note doit renvoyer exactement cette note
- essayez des décimales ([9.5, 8.5]) pour contrôler l'arrondi affiché

INDICE
- sum() et len() font tout le travail, mais pensez au cas vide AVANT de diviser : une division par zéro lève une ZeroDivisionError.
""",
            "Compteur de mots": """ÉNONCÉ
- compter les occurrences d'un mot donné dans un texte, en ignorant la casse.
- « Le », « le » et « LE » doivent compter exactement pareil.
- le texte réel contient des ponctuations et des espaces multiples à gérer.

ÉTAPES
1. saisir un texte libre et le mot à chercher
2. mettre les deux en minuscules avec lower()
3. découper le texte en mots avec split()
4. parcourir les mots et compter les égalités avec le mot cherché
5. afficher le total, puis refaire un essai avec un mot absent du texte

RÉSULTAT ATTENDU
- « le chat et le chien », mot = « le » donne 2
- « Babi Programmeur », mot = « babi » donne 1
- un mot absent du texte donne 0

POUR TESTER
- cherchez un mot écrit en majuscules au début de phrase : le compte doit être juste
- essayez une phrase où le mot cherché est le premier et le dernier mot
- testez plusieurs espaces entre les mots : aucune tabulation parasite ne doit fausser le total

INDICE
- lower() d'abord, split() ensuite, et appliquez les deux aux mêmes chaînes : « Le » et « le » doivent se retrouver identiques.
""",
            "Convertisseur": """ÉNONCÉ
- convertir des températures entre Celsius et Fahrenheit dans les deux sens.
- l'utilisateur saisit une valeur puis indique le sens de la conversion (Celsius vers Fahrenheit, ou l'inverse).
- le résultat s'affiche arrondi à 1 décimale, et une saisie non numérique est refusée.

ÉTAPES
1. demander la valeur et le sens de la conversion
2. convertir la saisie en float, sinon afficher une erreur de saisie
3. appliquer F = C × 9/5 + 32 quand on part des Celsius
4. appliquer C = (F − 32) × 5/9 quand on part des Fahrenheit
5. afficher le résultat arrondi à 1 décimale avec son unité

RÉSULTAT ATTENDU
- 0 en Celsius donne 32.0 °F
- 100 en Celsius donne 212.0 °F
- 98.6 en Fahrenheit donne 37.0 °C
- les deux échelles se croisent à moins 40, les deux affichent la même valeur

POUR TESTER
- convertissez 0 °C : vous devez retrouver 32.0 °F
- reconvertissez ensuite 32.0 °F : le programme doit afficher 0.0 °C
- saisissez « vingt » : le programme refuse sans planter et propose de recommencer

INDICE
- l'inverse de × 9/5 + 32 est (F − 32) × 5/9 ; validez votre formule avec l'aller-retour 0 puis 32 puis 0.
""",
            "Nombre mystère": """ÉNONCÉ
- deviner un nombre entre 1 et 100 que l'ordinateur a choisi, avec des indices « plus grand / plus petit », en 7 essais maximum.
- chaque proposition est comparée à la cible, puis le programme indique dans quelle direction chercher.
- à la fin, on affiche le nombre d'essais utilisés, ou la solution si les essais sont épuisés.

ÉTAPES
1. générer un nombre aléatoire entre 1 et 100 (module random)
2. demander une proposition à l'utilisateur et la convertir en entier
3. afficher « plus grand », « plus petit » ou « trouvé » selon la comparaison
4. répéter tant que ce n'est pas trouvé et qu'il reste des essais
5. compter chaque proposition et afficher le total à la fin
6. afficher « perdu » avec la solution après 7 essais ratés

RÉSULTAT ATTENDU
- avec 42 choisi : 50 affiche « plus petit », 30 affiche « plus grand », 42 affiche « trouvé »
- succès : « bravo, vous avez gagné en 3 essais »
- échec : « dommage, le nombre était 42 »

POUR TESTER
- une proposition hors de 1 à 100 doit être refusée sans compter comme essai
- relancez le programme : l'ordinateur doit choisir un autre nombre à chaque partie
- rejouez la même valeur : le compteur d'essais doit bien avancer

INDICE
- la stratégie optimale est binaire : coupez l'intervalle en deux à chaque essai (50, puis 25, puis 12...), 7 essais suffisent toujours pour 100 valeurs.
""",
        },
    },
    "JavaScript": {
        "lessons": {
            "Variables et portée": """OBJECTIFS
- déclarer des variables avec let, const et var
- comprendre la portée des blocs et le hoisting
- choisir la déclaration adaptée à chaque cas

POINTS CLÉS
- const par défaut, let seulement si la valeur change
- var a une portée de fonction : à éviter
- une constante d'objet reste modifiable
- le hoisting hisse les déclarations, pas les valeurs
- typeof d'une variable non initialisée ne plante pas
- une accolade crée une portée pour let et const

EXEMPLE
const TVA = 0.2;               // jamais réaffectée
let total = 100;
total = total * (1 + TVA);     // 120

if (true) {
  let interne = 1;             // invisible dehors
  var global = 2;              // fuit à l'extérieur
}

const config = { actif: true };
config.actif = false;          // contenu modifiable
console.log(typeof total);     // "number"

EN PRATIQUE
On garde en const l'URL de l'API et le taux de TVA, en let les compteurs et
les variables de boucle : on voit ce qui a le droit de changer.

PIÈGES À ÉVITER
- « const obj = ... » puis « obj = ... » : réaffectation interdite
- utiliser une let avant sa ligne lève une ReferenceError
- var reste visible après son bloc : ne l'utilisez plus

À RETENIR
- const par défaut, let quand ça change, var jamais
- la portée suit les accolades, pas l'indentation
- déclarer près de l'usage évite les confusions
""",
            "Conditions et boucles": """OBJECTIFS
- écrire des conditions et des choix multiples
- boucler avec for, for…of et forEach
- maîtriser les opérateurs de comparaison

POINTS CLÉS
- === compare valeur ET type, == convertit avant
- if / else if / else n'exécute qu'une seule branche
- switch : sans break, la chute se fait automatiquement
- for…of parcourt les valeurs, for…in les clés
- ternaire : condition ? si_vrai : si_faux
- for classique : init ; test ; incrément

EXEMPLE
const notes = [12, 15, 9];
let somme = 0;
for (let i = 0; i < notes.length; i++) {
  somme += notes[i];
}
console.log(somme / notes.length);       // 12

for (const n of notes) {
  if (n >= 10) console.log(n, "admisible");
}
const statut = notes.length ? "ok" : "vide";
console.log(1 === "1", 1 == "1");        // false true

EN PRATIQUE
Une page de commerce teste le stock, le prix et le rôle de l'utilisateur
avant d'afficher un bouton : chaque clic recalcule le total du panier.

PIÈGES À ÉVITER
- oublier break dans un switch fait chuter les cases suivantes
- for…in sur un tableau renvoie des chaînes : préférez for…of
- boucler jusqu'à tab.length inclus déborde du tableau

À RETENIR
- === pour comparer, = pour affecter
- for…of pour les valeurs, for…in pour les clés
- un ternaire se lit sur une seule ligne
""",
            "Fonctions": """OBJECTIFS
- définir des fonctions classiques, flèche et anonymes
- passer des paramètres par défaut et regrouper les arguments
- comprendre this et les fermetures

POINTS CLÉS
- function f(a, b = 1) { ... } : déclaration classique
- const f = (a) => a * 2; : pas de this propre
- ...args regroupe les arguments surnuméraires
- une fermeture garde son environnement de création
- sans return, la fonction renvoie undefined
- une fonction est une valeur : on peut la passer

EXEMPLE
const ajouter = (a, b = 10) => a + b;
console.log(ajouter(5));               // 15
console.log(ajouter(5, 1));            // 6

function compter(...nombres) {
  return nombres.length;
}
console.log(compter(1, 2, 3));         // 3

const doubler = (n) => n * 2;    // return implicite
const carre = (n) => { return n * n; };

let total = 0;
const ajouterAuTotal = (n) => { total += n; };
ajouterAuTotal(5);

EN PRATIQUE
On confie une fonction à addEventListener, map, filter ou setTimeout ; le
formulaire appelle valider(saisie) et affiche le message renvoyé.

PIÈGES À ÉVITER
- une flèche avec des accolades ne renvoie rien sans return
- ne pas confondre f() qui appelle et f qui désigne
- this dans une flèche vient du code englobant

À RETENIR
- un nom en verbe, un seul rôle, un return lisible
- ...args remplace les arguments fixes
- la flèche convient aux rappels courts
""",
            "Tableaux et objets": """OBJECTIFS
- transformer des tableaux avec map, filter et reduce
- décomposer objets et tableaux (destructuring)
- organiser les données en objets littéraux

POINTS CLÉS
- map transforme, filter sélectionne, reduce agrège
- décomposition : const { nom, age } = personne
- spread copie : [...tab, x] crée un nouveau tableau
- Object.keys / values / entries parcourent un objet
- map et filter ne modifient jamais l'original
- un tableau d'objets représente une liste réelle

EXEMPLE
const notes = [12, 15, 9];
const doublées = notes.filter(n => n >= 10)
  .map(n => n * 2);
console.log(doublées);              // [24, 30]

const total = notes.reduce((s, n) => s + n, 0);
console.log(total);                 // 36

const personne = { nom: "Babi", age: 30 };
const { nom, age } = personne;
console.log(Object.keys(personne)); // ["nom", "age"]

EN PRATIQUE
Les réponses d'une API arrivent en tableau d'objets : on le filtre, on le
mappe vers l'affichage, on le réduit vers un total.

PIÈGES À ÉVITER
- oublier le return dans map renvoie des undefined
- confondre filter (condition) et map (transformation)
- reduce sans valeur initiale plante sur tableau vide

À RETENIR
- map pour transformer, filter pour trier, reduce pour calculer
- spread crée une copie : l'original reste intact
- une donnée répétée se range dans un tableau
""",
            "Le DOM": """OBJECTIFS
- sélectionner et modifier des éléments de la page
- écouter les événements (clic, saisie)
- créer et supprimer des nœuds dynamiquement

POINTS CLÉS
- querySelector("#id") / ".classe" renvoie un élément
- querySelectorAll renvoie une liste à parcourir
- textContent change le texte, classList la classe
- addEventListener vaut mieux qu'onclick en ligne
- createElement puis append pour l'ajout dynamique
- l'événement input se déclenche à chaque frappe

EXEMPLE
const btn = document.querySelector("#ok");
const zone = document.querySelector("#sortie");

btn.addEventListener("click", (e) => {
  zone.textContent = "clic " + e.target.textContent;
  e.target.classList.add("vert");
});

const champ = document.querySelector("#nom");
champ.addEventListener("input", () => {
  zone.textContent = "salut " + champ.value;
});

EN PRATIQUE
Toute interface se résume à des sélecteurs, des écouteurs et une fonction
d'affichage qui réécrit le contenu de la zone concernée.

PIÈGES À ÉVITER
- querySelector renvoie null si l'élément n'existe pas
- écrire dans innerHTML avec une saisie : injection
- un écouteur par nouveau nœud : écoutez le parent

À RETENIR
- un écouteur par intention, une fonction d'affichage par zone
- textContent pour le texte, classList pour les styles
- le script se place après le HTML
""",
            "Asynchrone": """OBJECTIFS
- comprendre la boucle d'événements et le code asynchrone
- utiliser les promesses et async / await
- appeler une API avec fetch et gérer les erreurs

POINTS CLÉS
- setTimeout planifie : son rappel attend la fin du code synchrone
- une promesse est pending, puis resolved ou rejected
- async / await écrit l'asynchrone comme du séquentiel
- fetch renvoie une Response : .json() est asynchrone aussi
- Response.ok vaut vrai entre 200 et 299
- une exception dans un await se rattrape avec try / catch

EXEMPLE
async function charger(url) {
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.status);
    return await r.json();
  } catch (e) {
    console.error("échec", e.message);
  }
}

console.log("avant");
charger("/api").then(d => console.log("reçu"));
console.log("après");     // s'affiche avant « reçu »

EN PRATIQUE
Un tableau de bord interroge plusieurs services puis affiche le résultat :
sans try / catch, une API coupée fige l'écran sans explication.

PIÈGES À ÉVITER
- appeler .json() sans await : c'est une promesse, pas des données
- oublier try / catch : la promesse rejetée reste muette
- await hors fonction async : erreur de syntaxe

À RETENIR
- async / await pour lire, promesses pour enchaîner
- toujours tester r.ok avant de faire confiance
- le code synchrone passe avant tout travail asynchrone
""",
            "Modules": """OBJECTIFS
- découper le code en modules import / export
- organiser un projet en fichiers responsables
- distinguer un script d'un module

POINTS CLÉS
- export const x / export default fonction publient du code
- import x from "./fichier.js" : extension obligatoire
- import { a, b } pour les exports nommés, renommage avec as
- <script type="module"> s'exécute après le HTML
- un module ne s'exécute qu'une fois : résultat mis en cache
- les imports sont remontés avant tout le module

EXEMPLE
// utils.js
export const double = (n) => n * 2;
export default function direBonjour(nom) {
  console.log("bonjour " + nom);
}

// main.js
import direBonjour, { double } from "./utils.js";
console.log(double(4));                 // 8
direBonjour("Babi");

EN PRATIQUE
On range la logique dans un fichier, l'affichage dans un autre ; le point
d'entrée n'assemble que les deux, et chaque module n'est lu qu'une fois.

PIÈGES À ÉVITER
- oublier l'extension .js : la recherche échoue au chargement
- mélanger default et nommés : la syntaxe d'import diffère
- ouvrir en double-clic : les modules exigent un serveur

À RETENIR
- un fichier = une responsabilité
- un export principal, les autres nommés
- importé deux fois, exécuté une seule fois
""",
        },
        "exercises": {
            "Message d'accueil": """ÉNONCÉ
- afficher dans la page un message de bienvenue contenant le nom saisi dans un champ, mis à jour à chaque frappe.
- la saisie se fait sans bouton : la page réagit pendant que l'on tape.
- au chargement, le champ est vide : il faut un message de repli.
- on y découvre les écouteurs d'événement et la liaison entre champ et texte.

ÉTAPES
1. écrire un HTML simple : un champ input et un paragraphe
2. sélectionner les deux éléments avec querySelector
3. écouter l'événement input sur le champ
4. dans le rappel, lire la valeur et réécrire le paragraphe
5. afficher un texte par défaut quand la valeur est vide
6. signaler les noms de plus de 10 lettres avec une classe CSS

RÉSULTAT ATTENDU
- champ vide : « Qui suis-je ? » affiché au chargement
- saisie « Babi » : « Bonjour Babi ! » apparaît lettre après lettre
- saisie « BabiProgrammeur » : « Bonjour BabiProgrammeur ! »

POUR TESTER
- tapez un nom puis effacez tout : le message de repli doit revenir
- collez un nom entouré d'espaces : aucun « undefined » ne doit apparaître
- rechargez la page : le champ repart à vide, sans erreur dans la console

INDICE
- input.value est toujours du texte : concaténez-le avec la phrase d'accueil, et testez sa longueur avant d'afficher pour gérer le champ vide.
""",
            "Compteur de clics": """ÉNONCÉ
- créer un bouton qui s'incrémente un compteur à chaque clic, accompagné d'un bouton « Réinitialiser ».
- le compteur s'affiche en permanence dans la page et repart de zéro.
- il faut que le total survive d'un clic à l'autre : c'est tout l'exercice.
- on réutilise la leçon sur la portée des variables et les écouteurs.

ÉTAPES
1. afficher un paragraphe contenant le compteur initialisé à 0
2. ajouter un premier bouton « Ajouter » et un second « Réinitialiser »
3. déclarer la variable du compteur avant les écouteurs, à portée commune
4. incrémenter la variable à chaque clic et réécrire l'affichage
5. remettre la variable à 0 dans le second écouteur
6. factoriser une fonction maj() unique pour l'affichage

RÉSULTAT ATTENDU
- au chargement : compteur affiché à 0
- trois clics successifs : 1, puis 2, puis 3
- clic sur « Réinitialiser » : retour immédiat à 0

POUR TESTER
- cliquez 10 fois puis réinitialisez : le retour à 0 doit être instantané
- alternez ajout et remise à zéro : jamais de NaN dans l'affichage
- rafraîchissez la page : le compteur repart de 0, pas de la dernière valeur

INDICE
- la variable du compteur vit hors des rappels d'événement : si vous la déclarez à l'intérieur d'un écouteur, chaque clic repart de zéro.
""",
            "FizzBuzz": """ÉNONCÉ
- afficher dans la page les nombres de 1 à 100, en colorant « Fizz », « Buzz » et « FizzBuzz » différemment.
- chaque nombre occupe une ligne ou une cellule, dans l'ordre croissant.
- la classe CSS change selon le cas : la mise en forme reste dans le style.
- l'exercice mêle boucle, condition et création d'éléments par JavaScript.

ÉTAPES
1. créer un conteneur vide dans le HTML, sans écrire les 100 lignes à la main
2. boucler de 1 à 100 avec une boucle for
3. calculer les deux tests : multiple de 3 et multiple de 5
4. traiter d'abord le cas où les deux sont vrais (FizzBuzz)
5. sinon tester le multiple de 3, puis celui de 5, sinon le nombre
6. créer un élément, lui donner sa classe CSS et l'ajouter au conteneur
7. vérifier le nombre total d'éléments créés

RÉSULTAT ATTENDU
- 1 et 2 s'affichent en normal, 3 en Fizz, 5 en Buzz, 15 en FizzBuzz
- FizzBuzz apparaît 6 fois (15, 30, 45, 60, 75, 90)
- 100 éléments au total, dans l'ordre croissant jusqu'à 100

POUR TESTER
- la dixième position doit être Buzz, la quinzième FizzBuzz
- comptez les Fizz (33), les Buzz (20) et les FizzBuzz (6) à l'écran
- réduisez la boucle à 1 à 20 d'abord : la sortie reste lisible

INDICE
- l'ordre des tests décide du résultat : si vous testez 3 avant 15, le nombre 15 affiche « Fizz » au lieu de « FizzBuzz ». Testez le cas combiné en premier.
""",
            "Statistiques de notes": """ÉNONCÉ
- à partir d'un tableau de notes, afficher le minimum, le maximum, la moyenne et la mention correspondante.
- les notes sont déjà saisies et correctes : l'exercice porte sur le calcul.
- la moyenne s'arrondit à 1 décimale, la mention suit une échelle fixe : 16 et plus « excellent », 10 et plus « admisible », sinon « à revoir ».
- chaque valeur s'affiche sur sa propre ligne, avec son libellé.

ÉTAPES
1. stocker les notes dans un tableau de nombres
2. obtenir le minimum et le maximum avec Math.min et Math.max
3. calculer la somme avec reduce, puis diviser par le nombre de notes
4. arrondir la moyenne à 1 décimale avec Math.round(x * 10) / 10
5. déduire la mention avec une suite if / else if / else
6. écrire les quatre résultats dans la page

RÉSULTAT ATTENDU
- [12, 15, 9] donne min 9, max 15, moyenne 12, mention « admisible »
- [18, 17] donne moyenne 17.5, mention « excellent »
- [8, 9] donne moyenne 8.5, mention « à revoir »

POUR TESTER
- un tableau d'une seule note : min, max et moyenne doivent être identiques
- des décimales comme [9.5, 8.5] : vérifiez l'arrondi affiché à 1 décimale
- relisez la mention d'une moyenne pile à 10 : elle doit dire « admisible »

INDICE
- Math.min(...tab) reçoit les valeurs une par une grâce au spread ; la moyenne se calcule avec reduce et une valeur initiale de 0.
""",
            "Liste de tâches": """ÉNONCÉ
- construire une liste de tâches : on en ajoute par un formulaire, on la coche comme faite, on la supprime.
- chaque tâche porte deux informations : son texte et son état (faite ou non).
- l'état vit dans un tableau d'objets, la page n'est qu'un reflet de ce tableau.
- rien ne doit être écrit en dur dans le HTML : tout est créé par JavaScript.

ÉTAPES
1. écrire le formulaire (champ + bouton) et une liste vide
2. empêcher le rechargement de la page avec preventDefault
3. ajouter un objet { texte, fait } au tableau d'état
4. écrire une fonction render() qui reconstruit la liste à chaque changement
5. cocher ou décocher une tâche au clic sur sa case
6. supprimer une tâche avec un bouton, puis rappeler render()
7. effacer le champ après chaque ajout

RÉSULTAT ATTENDU
- ajout de « coder » : la ligne apparaît immédiatement
- coche cochée : la ligne est barrée au prochain rendu
- croix cliquée : la ligne disparaît et le tableau perd un objet

POUR TESTER
- ajoutez trois tâches, cochez la deuxième, supprimez la première
- envoyez le formulaire à vide : aucune ligne vide ne doit s'ajouter
- rafraîchissez la page : tout repart à zéro, sans erreur console

INDICE
- une fonction render() unique évite de dupliquer l'affichage ; pensez à lui faire balayer le tableau d'état et à effacer l'ancien contenu avant de reconstruire.
""",
            "Recherche produit": """ÉNONCÉ
- filtrer une liste de produits par texte saisi et par prix maximal, dans une même page.
- la recherche se met à jour à chaque frappe, sans bouton de validation.
- le compteur de résultats reste visible même quand aucun produit ne passe le filtre.
- c'est le cas d'usage le plus courant d'un tableau de commerce.

ÉTAPES
1. stocker les produits dans un tableau d'objets { nom, prix }
2. afficher tous les produits au chargement
3. écouter l'événement input du champ de texte
4. filtrer avec includes en minuscules pour ignorer la casse
5. filtrer à nouveau avec le prix maximal saisi
6. chaîner les deux filtres puis afficher le compteur
7. afficher un message quand le résultat est vide

RÉSULTAT ATTENDU
- recherche « par » avec prix maximum 50 : seuls les produits correspondants restent
- champ vidé : la liste complète revient
- aucune correspondance : « 0 produit » s'affiche au lieu d'une zone blanche

POUR TESTER
- tapez « PAR » en majuscules : les mêmes produits doivent rester
- saisissez un prix très bas : le compteur doit tomber à 0 sans erreur
- essayez des caractères spéciaux : rien ne doit planter ni figer la page

INDICE
- chaînez deux filter() : un premier pour le texte, un second pour le prix, et pensez à comparer en minuscules des deux côtés.
""",
            "Mini-jeu": """ÉNONCÉ
- deviner un nombre de 1 à 100 en 7 essais maximum, avec affichage des indices « plus grand » ou « plus petit ».
- le joueur saisit sa proposition dans un champ, la page répond et compte les essais.
- après chaque essai, on indique combien il en reste ; la partie se termine par une victoire ou un épuisement.
- la cible est choisie par le navigateur à chaque nouvelle partie.

ÉTAPES
1. générer la cible avec Math.random() et l'arrondir en entier de 1 à 100
2. initialiser le compteur d'essais à 0 et le nombre maximum à 7
3. lire la proposition à chaque envoi du formulaire
4. comparer et afficher « plus grand », « plus petit » ou « trouvé »
5. incrémenter le compteur et afficher les essais restants
6. bloquer le formulaire après victoire ou essais épuisés

RÉSULTAT ATTENDU
- cible 42 : la proposition 50 donne « plus petit », 30 donne « plus grand »
- proposition 42 : « trouvé en 3 essais ! » et le formulaire se verrouille
- 7 essais ratés : « perdu, la cible était 42 »

POUR TESTER
- essayez la même proposition deux fois : le compteur doit bien avancer
- une saisie non numérique doit être refusée sans compter comme essai
- relancez la partie : une nouvelle cible est tirée à chaque fois

INDICE
- la stratégie optimale coupe l'intervalle en deux à chaque essai : 50, puis 25, puis 12... 7 essais suffisent toujours pour 100 valeurs.
""",
        },
    },
    "TypeScript": {
        "lessons": {
            "Types de base": """OBJECTIFS
- annoter les variables, paramètres et retours
- connaître les types primitifs et les tableaux typés
- laisser faire l'inférence quand elle est fiable

POINTS CLÉS
- let n: number = 3 ; const s: string = "x"
- bool, null, undefined, any (à éviter), unknown (sûr)
- tableaux : string[] ou Array<string>
- une annotation fausse arrête la compilation
- le compilateur signale toute incompatibilité
- sans annotation, le type se déduit de la valeur

EXEMPLE
let age: number = 30;
age = "trente";              // erreur : string attendu

function ajouter(a: number, b: number): number {
  return a + b;
}
const total = ajouter(2, 3);     // number deviné
const notes: number[] = [12, 15, 9];

let valeur: unknown = 42;
if (typeof valeur === "number") {
  console.log(valeur + 1);       // sécurité avant calcul
}

EN PRATIQUE
Les annotations vivent surtout dans les signatures de fonctions : le reste
se déduit. Un projet typé attrape la faute au moment de la compilation.

PIÈGES À ÉVITER
- any désactive tout contrôle : préférer unknown + vérification
- const annoté large gaspille l'inférence
- number pour un identifiant affiché : préférez string

À RETENIR
- unknown est sûr, any est confiance totale
- le compilateur relit le code à votre place
- annoter les frontières, laisser deviner l'intérieur
""",
            "Interfaces et objets": """OBJECTIFS
- décrire la forme des données avec interface
- typer les objets littéraux et les littéraux de chaîne
- étendre des interfaces existantes

POINTS CLÉS
- interface Utilisateur { id: number; nom: string }
- propriété optionnelle : age?: number
- extends hérite, & combine deux types
- typage structurel : la forme compte, pas le nom
- type alias : type P = { ... } pour les unions
- readonly fige une propriété après création

EXEMPLE
interface Produit {
  id: number;
  nom: string;
  prix: number;
  promo?: boolean;
}
const p: Produit = { id: 1, nom: "Clavier", prix: 49.9 };
console.log(p.prix.toFixed(2));   // 49.90

interface Promo extends Produit {
  remise: number;
}
const t: Promo = { id: 2, nom: "Souris", prix: 19, remise: 10 };

EN PRATIQUE
Une réponse d'API décrite par une interface devient un document : chaque
champ manquant ou mal nommé est signalé avant même l'exécution.

PIÈGES À ÉVITER
- un champ obligatoire manquant refuse l'objet
- readonly manquant : rien n'empêche de réaffecter
- typer avec string perd le littéral « admin »

À RETENIR
- décrivez ce que la donnée contient, pas d'où elle vient
- optionnel avec ?, figé avec readonly
- tout objet de forme équivalente passe
""",
            "Fonctions typées": """OBJECTIFS
- annoter paramètres et valeur de retour
- gérer les retours optionnels et le void
- utiliser les surcharges quand nécessaire

POINTS CLÉS
- (a: number, b: number) => number décrit une fonction
- le type de retour se déduit du return
- fonction sans résultat : void
- retour parfois absent : number | undefined
- surcharges : plusieurs signatures au-dessus du corps
- paramètre par défaut : max = 20 garde son type

EXEMPLE
function tronquer(texte: string, max = 20): string {
  return texte.length > max ? texte.slice(0, max) + "…" : texte;
}
console.log(tronquer("une phrase bien trop longue"));
// "une phrase bien trop…"

const doubler = (n: number): number => n * 2;
console.log(doubler(21));                   // 42

function chercher(id: number): string | undefined {
  return id > 0 ? "trouvé" : undefined;
}

EN PRATIQUE
Une fonction exposée à d'autres fichiers se type en premier : ses
annotations forment le contrat que les appelants lisent et que le
compilateur surveille à chaque appel.

PIÈGES À ÉVITER
- annoncer string et renvoyer number : erreur signalée sur place
- oublier undefined dans le retour d'une recherche
- écrire void pour une fonction qui renvoie pourtant une valeur

À RETENIR
- le contrat se lit dans la signature, pas dans le corps
- un retour qui peut manquer s'écrit | undefined
- void dit qu'on n'attend rien du tout
""",
            "Union et réduction": """OBJECTIFS
- représenter plusieurs formes possibles avec les unions
- exploiter la réduction (narrowing) pour sécuriser le code
- utiliser les unions discriminées

POINTS CLÉS
- string | number : l'une OU l'autre
- typeof / instanceof réduisent le type
- champ discriminé : { etat: "vide" } | { etat: "plein" }
- une propriété exclusive s'accède après un test
- « | undefined » signale une valeur qui peut manquer
- le type réduit se voit à la ligne suivante

EXEMPLE
function afficher(v: string | number) {
  if (typeof v === "string") {
    console.log(v.toUpperCase());   // v est string ici
  } else {
    console.log(v.toFixed(2));      // v est number ici
  }
}
afficher("babi");           // BABI
afficher(12.5);             // 12.50

type Etat = { etat: "vide" } | { etat: "plein"; contenu: number };

EN PRATIQUE
Une donnée venue d'une API est souvent dans deux états : absente ou
présente. L'union oblige à traiter les deux cas avant l'affichage.

PIÈGES À ÉVITER
- accéder à une propriété exclusive sans test : refus
- écrire any pour débloquer : la protection disparaît
- oublier le default d'un switch sur une union

À RETENIR
- l'union élargit, la réduction resserre
- un test sur un champ suffit à préciser tout le type
- chaque branche doit être traitée
""",
            "Génériques": """OBJECTIFS
- écrire du code réutilisable avec un paramètre de type
- comprendre l'inférence des génériques
- borner les types avec des contraintes

POINTS CLÉS
- function identique<T>(x: T): T { return x; }
- classe Boîte<T> { contenu: T }
- contrainte : <T extends { id: number }>
- l'appelant peut préciser : identique<string>("x")
- le plus souvent, le type se devine de l'argument
- générique et union : deux outils, deux usages

EXEMPLE
function premier<T>(tab: T[]): T | undefined {
  return tab[0];
}
const n = premier([1, 2, 3]);       // number | undefined
const s = premier(["a", "b"]);      // string | undefined

function avecId<T extends { id: number }>(x: T): number {
  return x.id;
}
console.log(avecId({ id: 7, nom: "Babi" }));   // 7
console.log(premier<string>([]));              // undefined

EN PRATIQUE
Une même fonction de cache, de liste ou de requête sert les produits, les
clients et les commandes : le générique évite de la copier à l'identique.

PIÈGES À ÉVITER
- <T> oublié : le paramètre devient any silencieusement
- trop de génériques dans une fonction simple
- contrainte trop large : n'importe quoi passe

À RETENIR
- T représente le type que l'appelant fournit
- extends impose une forme minimale
- commencez simple, ajoutez un générique quand la copie apparaît
""",
            "Classes et visibilité": """OBJECTIFS
- typer les classes (champs, méthodes, constructeur)
- maîtriser readonly, private, protected, public
- implémenter une interface avec implements

POINTS CLÉS
- private hors classe, protected aussi pour les sous-clases
- readonly : modifiable à l'initialisation seulement
- implements impose les membres annoncés
- raccourci : constructor(private nom: string) {}
- le privé TypeScript reste visible dans le JS compilé
- nommer en camelCase comme partout ailleurs

EXEMPLE
interface Serializable {
  serialiser(): string;
}
class Compte implements Serializable {
  constructor(
    public id: number,
    private solde: number,
  ) {}
  serialiser(): string {
    return JSON.stringify({ id: this.id });
  }
}
const c = new Compte(1, 50);
console.log(c.serialiser());   // {"id":1}
console.log(c.solde);          // erreur : privé

EN PRATIQUE
On cache derrière une classe ce qui ne doit pas être touché de l'extérieur :
solde d'un compte, état d'une connexion. Le compilateur fait le gardien.

PIÈGES À ÉVITER
- private n'empêche qu'une erreur de type, pas un curieux
- un champ déclaré sans valeur exige un constructeur
- interface incomplète : la compilation échoue

À RETENIR
- public par défaut, private pour l'interne
- implements vérifie le contrat à la compilation
- le vrai secret se gère côté serveur
""",
            "Modules de types": """OBJECTIFS
- organiser le code en modules et déclarer leurs types
- configurer tsconfig.json
- distinguer bibliothèque JS et bibliothèque de types

POINTS CLÉS
- import / export identiques à JavaScript
- module sans types : fichier .d.ts ou paquet @types
- compiler : tsc puis node, ou ts-node en direct
- options clés : strict, target, module, outDir
- strict: true active tous les contrôles utiles
- l'import ne mentionne jamais l'extension .ts

EXEMPLE
// math.ts
export function double(n: number): number {
  return n * 2;
}
export const PI = 3.14;

// main.ts
import { double, PI } from "./math";
console.log(double(4), PI);         // 8 3.14

EN PRATIQUE
Une équipe découpe son code en fichiers .ts et garde un tsconfig unique à
la racine : la même configuration s'applique à tout le projet.

PIÈGES À ÉVITER
- importer avec extension .ts : erreur
- un paquet sans @types : tout passe en any
- strict à false : les fautes simples passent

À RETENIR
- tsc écrit le JavaScript, node l'exécute
- @types vérifie là où le paquet se tait
- strict dès le départ évite des bugs entiers
""",
        },
        "exercises": {
            "Typer une fonction": """ÉNONCÉ
- prendre une fonction JavaScript existante non typée et lui ajouter des annotations sans changer son comportement.
- on suppose une petite fonction utilitaire : calcul, formatage ou filtre.
- chaque paramètre et le retour doivent être décrits précisément.
- seul le typage change : les résultats affichés restent identiques.

ÉTAPES
1. ouvrir la fonction et lister ce qu'elle reçoit puis ce qu'elle rend
2. annoter chaque paramètre (number, string, boolean, tableau...)
3. annoter la valeur de retour
4. lancer tsc --noEmit et lire la première erreur
5. corriger une erreur à la fois, sans toucher à la logique
6. relancer jusqu'à zéro erreur
7. exécuter le programme et comparer les résultats d'avant

RÉSULTAT ATTENDU
- tsc --noEmit ne remonte plus aucune erreur
- la compilation produit bien un fichier JavaScript
- les résultats affichés sont identiques à ceux d'avant

POUR TESTER
- appelez la fonction avec un mauvais type : erreur signalée
- changez une valeur en dur dans un appel : le compilateur se plaint
- retirez une annotation : le résultat affiché ne doit pas bouger

INDICE
- commencez par any pour faire taire le compilateur, puis remplacez chaque
any par un type précis : les erreurs qui réapparaissent vous guident.
""",
            "Profil utilisateur": """ÉNONCÉ
- modéliser un profil avec interface : id, nom, email, âge optionnel et rôle.
- le rôle n'accepte que « admin » ou « membre », jamais autre chose.
- une fonction affiche le rôle du profil reçu.
- l'exercice vérifie qu'un objet invalide est refusé à la compilation.

ÉTAPES
1. définir l'interface Profil avec ses champs et leurs types
2. marquer l'âge comme optionnel
3. décrire le rôle avec un littéral de chaîne en union
4. créer un objet conforme et l'afficher
5. écrire une fonction qui accepte un Profil
6. déclarer un objet invalide et lire l'erreur de compilation

RÉSULTAT ATTENDU
- un objet complet compile sans une seule erreur
- un rôle comme « super » est refusé par le compilateur
- un email manquant bloque aussi la compilation

POUR TESTER
- retirez le champ âge : l'objet doit rester valide
- ajoutez un troisième rôle dans l'objet : erreur attendue
- remplacez l'adresse email par un nombre : erreur attendue

INDICE
- un littéral de chaîne (« admin ») borne la valeur bien mieux qu'un string :
la réunion des deux littéraux forme le type exact du rôle.
""",
            "Convertisseur JSON": """ÉNONCÉ
- écrire une fonction qui transforme un objet en JSON puis le relit en vérifiant sa forme.
- la forme attendue est celle d'un profil : id, nom, email.
- un JSON incomplet doit provoquer une erreur explicite.
- on découvre la sérialisation, la lecture et les gardes de type.

ÉTAPES
1. décrire l'interface attendue (champs requis, âge optionnel)
2. JSON.stringify pour sérialiser l'objet
3. JSON.parse pour relire la chaîne
4. attribuer le résultat à une variable typée
5. vérifier chaque champ obligatoire avant de renvoyer
6. lancer throw new Error("JSON incomplet") si un champ manque

RÉSULTAT ATTENDU
- {"id":1,"nom":"Babi","email":"babi@exemple.fr"} : objet renvoyé
- {"id":1} seul : erreur « JSON incomplet » affichée
- un objet sans email : même erreur, sans plantage

POUR TESTER
- sérialisez puis relisez un profil complet : résultat identique
- supprimez un champ dans la chaîne avant le parse : erreur attendue
- essayez une chaîne mal formée : l'exception doit être rattrapée

INDICE
- JSON.parse renvoie any : attribuez-le aussitôt à votre type, puis testez
les champs un par un avant de les utiliser.
""",
            "Cache générique": """ÉNONCÉ
- implémenter une Map<K, V> typée avec get, set, has et clear.
- la classe refuse toute valeur d'un autre type que celui annoncé.
- une clé absente répond undefined, pas une erreur.
- l'exercice montre à quoi sert un paramètre de type.

ÉTAPES
1. déclarer une classe Cache<K, V>
2. garder la Map<K, V> dans un champ privé
3. écrire set(cle: K, valeur: V)
4. écrire get(cle: K): V | undefined
5. exposer size en lecture seule et ajouter clear()
6. créer un Cache<string, number> puis tenter d'y mettre un texte

RÉSULTAT ATTENDU
- get d'une clé absente renvoie undefined
- mettre un string dans Cache<string, number> ne compile pas
- size suit les ajouts et revient à 0 après clear()

POUR TESTER
- ajoutez puis effacez des entrées : size doit suivre
- essayez une clé du mauvais type : erreur attendue
- réutilisez la classe pour Cache<number, string> sans la modifier

INDICE
- V | undefined reflète l'absence de clé sans planter ; typez le champ Map
avec les mêmes paramètres K et V que la classe elle-même.
""",
            "États d'une commande": """ÉNONCÉ
- représenter quatre états de commande avec une union discriminée.
- les états : en attente, expédiée, livrée, annulée.
- chaque état transporte ses propres informations (suivi, date ou raison).
- une fonction renvoie le message correspondant à l'état reçu.

ÉTAPES
1. décrire Etat comme une réunion d'objets ayant chacun un champ etat
2. ajouter suivi, date ou raison selon l'état
3. écrire message(e: Etat): string avec un switch
4. traiter chaque cas et renvoyer son texte
5. prévoir un default pour un état inconnu
6. créer un objet par état et afficher les messages
7. tenter un état inexistant et lire l'erreur

RÉSULTAT ATTENDU
- chaque état affiche son propre message
- un objet sans champ etat ne compile pas
- un état inconnu n'apparaît jamais à l'exécution

POUR TESTER
- passez une commande de « attente » à « expedie » : le message change
- retirez le suivi d'un envoi : erreur de compilation attendue
- affichez les quatre messages d'affilée : aucun ne se ressemble

INDICE
- le champ etat sert de discriminant : dans le switch, TypeScript déduit
tout seul le reste de l'objet, sans vérification supplémentaire.
""",
            "Corriger un bug": """ÉNONCÉ
- un morceau de code JavaScript échoue à la compilation TypeScript.
- votre rôle : lister les erreurs, les corriger une à une et expliquer chacune.
- la logique du programme ne doit pas changer, seulement les types.
- vous travaillez avec tsc --noEmit, qui ne génère aucun fichier.

ÉTAPES
1. lancer tsc --noEmit et lire la première erreur affichée
2. ouvrir la ligne indiquée et identifier le type fautif
3. corriger (type manquant, comparaison ==, variable inconnue)
4. relancer la compilation immédiatement
5. répéter jusqu'à zéro erreur
6. commenter chaque correction en français dans le code

RÉSULTAT ATTENDU
- tsc --noEmit se termine sans aucune erreur
- chaque correction porte un commentaire explicatif
- le programme donne exactement les mêmes résultats qu'avant

POUR TESTER
- cassez volontairement un type : l'erreur doit réapparaître
- comparez la sortie avant et après : elle doit être identique
- relisez vos commentaires : chacun dit le pourquoi, pas le quoi

INDICE
- corrigez d'abord les erreurs en cascade : une cause racine en produit
plusieurs. Traitez celle qui apparaît en premier dans la liste.
""",
            "Réponse d'API": """ÉNONCÉ
- typer la réponse d'une API JSON (champs optionnels compris) et l'afficher en sécurité.
- la réponse contient une liste d'articles et un total.
- le champ data peut manquer : il faut un message clair, pas un plantage.
- l'exercice mêle interface, optionnel et appel asynchrone.

ÉTAPES
1. décrire l'interface Reponse { data: Article[]; total: number }
2. typer Article (titre, prix, état optionnel)
3. récupérer avec fetch puis annoter le résultat de .json()
4. tester l'existence de data avant de le parcourir
5. afficher le total et le titre du premier article
6. afficher un message si data manque ou si la requête échoue

RÉSULTAT ATTENDU
- réponse complète : total et premier titre affichés
- data absent : « réponse incomplète » affiché, rien ne plante
- requête en échec : message réseau affiché

POUR TESTER
- simulez une réponse sans data : pas d'erreur à l'exécution
- simulez un statut 500 : le message réseau doit sortir
- vérifiez qu'un titre non typé ne passe pas à l'affichage

INDICE
- les champs optionnels se déclarent avec ? et se testent avant usage ;
une garde du type « s'il existe » suffit à satisfaire le compilateur.
""",
        },
    },
}
