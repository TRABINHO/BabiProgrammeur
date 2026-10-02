"""Fiches de contenu — lot 5 : Kotlin, Autre, Flutter."""
from __future__ import annotations

CONTENT = {
    "Kotlin": {
        "lessons": {
            "val et var": """OBJECTIFS
- distinguer val (immuable) et var (modifiable)
- connaître l'inférence de type
- déclarer des constantes et choisir le bon type
- éviter les réassignations inutiles

POINTS CLÉS
- val = lecture seule : toute tentative de modification est refusée à la compilation
- var = réassignable autant de fois que nécessaire
- le type se déduit : val n = 3 devient Int, val prenom devient String
- textes : String, entiers : Int, décimaux : Double, booléen : Boolean
- visibilité par défaut : publique, sans mot-clé à écrire
- on peut annoncer le type : val age: Int = 30 (obligatoire si la valeur est inconnue)

EXEMPLE
val nom = "Babi"                 // jamais réaffecté
var age = 30
age = 31                         // autorisé
val pi = 3.14                    // Double
val message = "$nom a $age ans"  // interpolation
val note: Int = 14               // type annoncé

EN PRATIQUE
Dans une application, l'identifiant d'une session, un tarif affiché ou un
seuil de notation restent en val : personne ne doit les modifier par accident.
Les compteurs et les états d'écran, eux, vivent en var.

PIÈGES À ÉVITER
- écrire var partout par habitude : commencez toujours par val
- forcer un décimal en Int est refusé : utilisez une conversion explicite

À RETENIR
- commencer par val et passer à var seulement si nécessaire.
- Kotlin signale lui-même toute réassignation interdite : lisez le message.
""",
            "Conditions et boucles": """OBJECTIFS
- utiliser if et when comme EXPRESSIONS
- boucler avec for sur des plages et while
- maîtriser les opérateurs logiques et les pas de boucle
- éviter les boucles qui ne se terminent jamais

POINTS CLÉS
- if (a > b) 10 else 20 renvoie une valeur : pas de ternaire à chercher
- when remplace le switch et accepte des plages, des listes et n'importe quel test
- when sans branche else doit être exhaustif sur un enum ou une sealed class
- for (i in 1..10) inclut les bornes ; 1 until 10 exclut la dernière
- step donne le pas, downTo fait descendre la plage
- while teste avant chaque tour, do/while teste après le premier

EXEMPLE
val note = 14
val mention = when {
  note >= 16 -> "excellent"
  note >= 10 -> "admisible"
  else -> "à revoir"
}
println(mention)                // admisible

for (i in 10 downTo 1 step 2) print("$i ")
println()                       // 10 8 6 4 2

var essais = 3
while (essais > 0) { essais-- }

EN PRATIQUE
Un formulaire affiche ou masque un message d'erreur avec if, et un import
de données parcourt un fichier avec for : l'essentiel d'une application.

PIÈGES À ÉVITER
- 1..0 est vide : utilisez downTo quand la borne haute est plus petite
- une condition de boucle jamais mise à jour fige le programme

À RETENIR
- when = choisir parmi des cas, if = choisir entre deux chemins
- les bornes 1..10 sont inclusives : vérifiez deux fois avant de corriger
""",
            "Fonctions": """OBJECTIFS
- définir des fonctions avec fun
- exploiter arguments nommés et corps expression
- comprendre les fonctions d'extension
- documenter les paramètres et le type renvoyé

POINTS CLÉS
- fun nom(a: Int): Int = a * 2 : nom, paramètres typés, retour typé
- corps expression : = suivi du résultat, sans accolades
- arguments nommés : f(b = 2, a = 1) pour relire l'appel comme une phrase
- valeur par défaut : fun saluer(nom: String = "Babi")
- une fonction d'extension ajoute une méthode à un type existant

EXEMPLE
fun moyenne(notes: List<Double>): Double =
  if (notes.isEmpty()) 0.0 else notes.average()

fun saluer(nom: String, titre: String = "Bonjour") =
  println("$titre $nom !")

saluer("Babi")                       // Bonjour Babi !
saluer(titre = "Salut", nom = "Babi")
println(moyenne(listOf(12.0, 15.0)))  // 13.5

fun String.entreGuillemets() = "\\"" + this + "\\""
println("ok".entreGuillemets())       // "ok"

EN PRATIQUE
On extrait une fonction dès que la même logique sert deux écrans. Les
fonctions d'extension embellissent les types sans en hériter.

PIÈGES À ÉVITER
- oublier le type de retour quand la fonction renvoie quelque chose
- une fonction qui grandit sans fin : signe qu'elle fait plusieurs métiers

À RETENIR
- une fonction courte en corps expression se lit comme une formule.
- nommez les fonctions avec un verbe : calculerTotal, afficherErreur.
""",
            "Nullabilité": """OBJECTIFS
- distinguer T et T? (nullable)
- éviter le NullPointerException
- utiliser ?. et l'opérateur elvis
- décider quand une valeur peut réellement être nulle

POINTS CLÉS
- String? accepte null, String non : le type porte l'information
- ?. appelle seulement si non nul, renvoie null sinon
- ?: fournit une valeur de repli immédiatement lisible
- !! force la non-nullité et lève une exception si null : à éviter
- if (x != null) déclenche le smart cast : x devient String non nul
- let { } n'exécute son bloc que si la valeur n'est pas nulle

EXEMPLE
val prenom: String? = null
val affichage = prenom?.uppercase() ?: "ANONYME"
println(affichage)               // ANONYME

if (prenom != null) {
  println(prenom.length)         // smart cast : String non nul ici
}

val contact: String? = "Babi"
contact?.let { println(it.length) }   // 4

EN PRATIQUE
Une API renvoie parfois un champ absent : affichez une valeur de repli
plutôt que de planter. En Android, texte vide et image absente sont souvent
des valeurs nulles.

PIÈGES À ÉVITER
- accumuler des !! : le premier champ manquant plante toute l'application
- vérifier la nullité puis passer par une variable intermédiaire non vérifiée
- confondre chaîne vide et null : " " n'est pas null

À RETENIR
- le compilateur « smart cast » après un test de nullité.
- préférez ?: ou ?. à tout !! dans un code de production.
""",
            "Classes et data class": """OBJECTIFS
- définir des classes et un constructeur primaire
- créer des data classes pour les données
- comprendre copy() et l'égalité structurelle
- savoir quand préférer une classe ordinaire

POINTS CLÉS
- class Compte(val id: Int, var solde: Double) : propriétés dans le constructeur
- data class : equals, hashCode, toString et copy offerts gratuitement
- == compare la structure, === compare la référence
- init {} : bloc d'initialisation exécuté à la création de l'objet
- encapsulation : solde privé et méthode deposer() pour le modifier

EXEMPLE
data class Personne(val nom: String, val age: Int)
val p = Personne("Babi", 30)
val p2 = p.copy(age = 31)
println(p == Personne("Babi", 30))   // true
println(p)                           // Personne(nom=Babi, age=30)

class Compte(val id: Int, var solde: Double) {
  init { require(solde >= 0.0) }     // règle de gestion
  fun deposer(montant: Double) { solde += montant }
}

EN PRATIQUE
On stocke des data class reçues d'une API ou lues en base, et une classe
ordinaire pour ce qui porte des règles : compte, panier, session.

PIÈGES À ÉVITER
- data class remplie de variables modifiables : l'égalité devient piégeuse
- classe ordinaire sans toString : les journaux affichent une référence illisible

À RETENIR
- data class pour les porteurs de données, classe ordinaire pour le comportement.
- copy() évite de recopier champ par champ.
""",
            "Collections": """OBJECTIFS
- utiliser listOf, mutableListOf, mapOf
- transformer avec map / filter / sumOf
- distinguer séquences et opérations intermédiaires
- choisir la collection adaptée au besoin

POINTS CLÉS
- listOf : immuable ; mutableListOf : modifiable
- setOf pour l'unicité, mapOf pour les paires clé / valeur
- map transforme, filter sélectionne, sumOf additionne
- firstOrNull / lastOrNull évitent l'exception sur liste vide
- groupBy regroupe, distinct déduplique, sorted trie
- opérations chaînées : chaque étape parcourt la liste en entier

EXEMPLE
val notes = listOf(12, 15, 9, 18)
val admis = notes.filter { it >= 10 }.map { "$it / 20" }
println(admis)                      // [12 / 20, 15 / 20, 18 / 20]
println(notes.sumOf { it })         // 54
println(notes.maxOrNull())          // 18

val parGroupe = notes.groupBy { if (it >= 10) "admis" else "refusé" }
val uniques = listOf(1, 1, 2).distinct()   // [1, 2]

EN PRATIQUE
Filtrer des articles, additionner des scores, retirer les doublons : tout
cela s'écrit en chaîne de map, filter et sorted, sans boucle.

PIÈGES À ÉVITER
- first() sur liste vide : utilisez firstOrNull() puis testez le résultat
- appeler add() sur listOf : elle est immuable, passez par mutableListOf

À RETENIR
- asSequence() diffère les étapes : utile sur les grandes listes.
- une boucle classique reste plus claire si vous ne faites qu'une seule passe.
""",
            "Coroutines": """OBJECTIFS
- exécuter du code asynchrone sans callbacks
- comprendre scope, Job et Dispatchers
- suspendre une fonction avec suspend
- annuler proprement une tâche devenue inutile

POINTS CLÉS
- CoroutineScope(Dispatchers.IO) pour le contexte de travail
- launch démarre une tâche, async renvoie un résultat awaitable
- delay() suspend sans bloquer le thread
- Dispatchers.Main pour l'interface, IO pour réseau et disque, Default pour le calcul
- annulation cooperative : le code suspendu s'arrête proprement
- une exception d'un enfant remonte selon le Job parent

EXEMPLE
scope.launch {
  val donnees = withContext(Dispatchers.IO) {
    fetchDepuisReseau()            // hors du thread UI
  }
  texte.text = donnees             // retour sur l'UI
}

scope.launch {
  repeat(3) { i ->
    println("$i sur ${Thread.currentThread().name}")
    delay(500)
  }
}

EN PRATIQUE
Charger une liste, enregistrer en base, appeler une API : chaque
opération longue part dans une coroutine pour que l'écran reste réactif.

PIÈGES À ÉVITER
- delay() sur le thread principal sans coroutine : l'application se fige
- lancer dans un scope jamais détruit : la tâche survit à l'écran
- oublier await ou withContext : le résultat arrive avant la fin du calcul

À RETENIR
- jamais de delay() sur le thread principal sans coroutine.
- une coroutine vit dans un scope : annulez-la quand l'écran meurt.
""",
        },
        "exercises": {
            "Bonjour main": """ÉNONCÉ
- écrire un fichier Kotlin avec fun main() qui affiche un message d'accueil, puis votre nom en majuscules.
- le programme produit deux lignes : le message fixe, puis le nom transformé.

ÉTAPES
1. créer un fichier bonjour.kt
2. écrire fun main() { ... }, le point d'entrée du programme
3. afficher le message fixe avec println
4. déclarer val nom avec votre prénom, puis afficher nom.uppercase()
5. exécuter avec kotlin bonjour.kt ou le bouton de l'IDE

RÉSULTAT ATTENDU
- première ligne : votre message d'accueil en français
- si nom vaut « Babi », la seconde ligne affiche BABI
- aucun avertissement ni erreur n'apparaît dans la console

POUR TESTER
- changez la valeur de nom puis relancez : la seconde ligne suit le changement
- commentez la ligne du message : la compilation doit échouer, preuve que
  le programme en dépend bien
- retirez une accolade : l'IDE signale l'erreur à la ligne exacte

INDICE
- println accepte l'interpolation : écrivez "Bonjour $nom !" et vérifiez
  que le dollar est suivi immédiatement du nom de la variable.
""",
            "Calculatrice": """ÉNONCÉ
- lire deux nombres et un opérateur au clavier, afficher le résultat du calcul.
- refuser proprement toute saisie non numérique et tout opérateur inconnu, sans planter.

ÉTAPES
1. lire chaque valeur avec readLine()
2. convertir avec toDoubleOrNull() et tester null avant toute opération
3. lire l'opérateur : +, -, * ou /
4. écrire when (operateur) comme EXPRESSION qui renvoie le calcul
5. traiter la division par zéro comme un cas à part
6. afficher le résultat ou un message de saisie invalide

RÉSULTAT ATTENDU
- avec « 6 », « 7 » et « * », le programme affiche 42.0
- avec « 8 », « 0 » et « / », il affiche un message du type « division impossible »
- avec « abc » ou un opérateur « x », il affiche « saisie invalide »

POUR TESTER
- essayez un nombre décimal « 2.5 » puis un négatif « -4 » : les deux passent
- testez les quatre opérateurs, puis un caractère hors de la liste
- après chaque saisie fausse, le programme doit afficher un message, jamais
  une trace d'exception

INDICE
- toDoubleOrNull() renvoie null au lieu de lever une exception : c'est ce
  test null qui remplace entièrement le bloc try.
""",
            "Liste de tâches": """ÉNONCÉ
- gérer une liste de tâches en console : ajout par texte, coche pour marquer fait, suppression.
- chaque tâche est une data class portant un texte et un état.

ÉTAPES
1. définir data class Tache(var texte: String, var faite: Boolean)
2. créer val taches = mutableListOf<Tache>()
3. proposer un menu : ajouter, cocher, supprimer, lister, quitter
4. ajouter seulement si le texte saisi n'est pas vide
5. basculer faite = !faite sur la tâche choisie, index vérifié avec getOrNull
6. retirer avec removeIf { it.faite } ou par index validé

RÉSULTAT ATTENDU
- l'ajout de « coder » fait apparaître cette tâche dans la liste, non faite
- cocher la première tâche affiche son état « faite »
- la suppression retire cette seule ligne, les autres restent en place

POUR TESTER
- ajoutez une tâche vide : rien ne doit être ajouté
- saisissez un index négatif ou trop grand : le programme refuse proprement
- cochez puis décochez : le compteur de tâches faites revient à zéro

INDICE
- la data class fournit equals gratuitement : vous pouvez comparer deux
  tâches dans vos tests sans écrire aucune méthode de comparaison.
""",
            "FizzBuzz": """ÉNONCÉ
- générer la séquence FizzBuzz de 1 à 100 : le nombre par défaut, des mots quand il est divisible.
- afficher dix éléments par ligne pour garder une sortie lisible.

ÉTAPES
1. boucler avec for (i in 1..100)
2. décider du texte avec when (true) et les tests i % 15, i % 3, i % 5
3. tester d'abord la double divisibilité, sinon le cas simple l'emporte
4. construire chaque élément avec l'interpolation de chaînes
5. passer à la ligne tous les dix éléments affichés

RÉSULTAT ATTENDU
- les dix premiers éléments sont 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz
- l'entier 15 donne FizzBuzz, jamais Fizz seul ni Buzz seul
- la sortie comporte exactement dix lignes de dix éléments

POUR TESTER
- vérifiez les multiples de 15 : ils ne doivent contenir que le mot combiné
- comptez les lignes : dix, pas onze ni neuf
- limitez la boucle à 1..15 et confirmez que le quinzième élément est correct

INDICE
- when (true) { i % 15 == 0 -> "FizzBuzz" ... } écrit les tests dans
  l'ordre : la première branche qui correspond est la seule exécutée.
""",
            "Statistiques": """ÉNONCÉ
- sur une liste de notes, calculer le minimum, le maximum, la moyenne, la médiane et une mention.
- le programme doit refuser une liste vide au lieu de planter.

ÉTAPES
1. construire une List<Int> de notes
2. minOrNull() et maxOrNull() : ils renvoient null si la liste est vide
3. average() pour la moyenne, après un test isNotEmpty()
4. médiane : trier une copie puis prendre la valeur centrale
5. mention avec when rangé sur la moyenne

RÉSULTAT ATTENDU
- avec [12, 15, 9] : minimum 9, maximum 15, moyenne 12.0, médiane 12
- pour cette moyenne, la mention affichée correspond à la tranche de 12
- liste vide : message d'erreur clair, aucun chiffre affiché

POUR TESTER
- liste de deux éléments : la médiane doit valoir la moyenne des deux
- liste d'un seul élément : minimum, maximum et médiane sont identiques
- liste vide : aucune exception ne doit remonter dans la console

INDICE
- average() sur une liste vide lève une exception : vérifiez isNotEmpty()
  avant tout calcul, et n'oubliez pas de trier une copie pour la médiane.
""",
            "Extension utile": """ÉNONCÉ
- créer une extension String.entreGuillemets() qui renvoie le texte entouré de guillemets, puis l'appliquer à plusieurs chaînes.
- écrire aussi une seconde extension qui compte les voyelles.

ÉTAPES
1. écrire fun String.entreGuillemets(): String en corps expression
2. appeler comme une méthode : "salut".entreGuillemets()
3. écrire fun String.compterVoyelles(): Int en parcourant les caractères
4. tester sur une chaîne vide et sur des majuscules
5. afficher les résultats avec println

RÉSULTAT ATTENDU
- « salut » devient le texte salut entouré de guillemets
- « bonjour » compte 3 voyelles
- la chaîne vide ne provoque aucune erreur d'exécution

POUR TESTER
- essayez une chaîne qui contient déjà des guillemets : le rendu reste lisible
- essayez des majuscules : le comptage de voyelles ne doit pas en tenir compte
- appelez les extensions depuis un autre fichier du même projet

INDICE
- $this représente la chaîne à l'intérieur de l'extension ; l'import devient
  inutile si l'extension est déclarée dans le même package.
""",
            "Compteur asynchrone": """ÉNONCÉ
- lancer une coroutine qui affiche un compteur de 1 à 5 avec une seconde d'attente entre chaque valeur, sans bloquer le reste du programme.

ÉTAPES
1. créer scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
2. lancer scope.launch { ... }
3. boucler de 1 à 5, afficher la valeur puis delay(1000)
4. afficher aussi le nom du thread utilisé
5. garder le programme vivant le temps du décompte avec Thread.sleep en fin de main

RÉSULTAT ATTENDU
- les nombres 1 à 5 apparaissent, un par seconde environ, dans l'ordre
- la durée totale est d'environ cinq secondes
- le thread annoncé n'est pas celui de l'interface

POUR TESTER
- raccourcissez l'attente à 200 ms : le décompte doit s'accélérer
- lancez deux compteurs en parallèle : leurs valeurs s'entremêlent
- interrompez le programme avant la fin : aucune erreur anormale n'apparaît

INDICE
- delay() suspend la coroutine au lieu de figer le thread : c'est ce qui
  permet à l'interface de rester réactive pendant tout le décompte.
""",
        },
    },
    "Autre": {
        "lessons": {
            "Mise en place": """OBJECTIFS
- installer un éditeur et l'environnement d'exécution
- exécuter un premier programme
- comprendre compilation et interprétation
- diagnostiquer un échec d'installation

POINTS CLÉS
- éditeur : VS Code, Vim, IntelliJ… texte enrichi, jamais de traitement de texte
- interpréteur : le langage s'exécute directement, le fichier est lu à la volée
- compilateur : étape de traduction avant exécution
- vérifier la version : langage --version
- le chemin PATH doit contenir l'exécutable, sinon la commande est introuvable
- le premier message d'erreur indique souvent la ligne exacte

EXEMPLE
1. installer le SDK du langage
2. écrire hello (extension du langage)
3. exécuter : hello
4. lire le message dans la console
5. modifier le texte puis relancer pour observer l'effet

EN PRATIQUE
Un projet débute toujours par la vérification de l'environnement : version
installée, éditeur, terminal. Cette étape, rapide une fois faite, évite des
heures de doute sur un code qui est pourtant juste.

PIÈGES À ÉVITER
- installer plusieurs versions et mélanger les chemins d'accès
- copier un script depuis un traitement de texte : les caractères changent
- ignorer un avertissement qui deviendra une erreur plus loin

À RETENIR
- un environnement fonctionnel est la moitié du travail : gardez-le à jour.
- en cas de doute, un « exemple exécutable » minimal valide tout.
""",
            "Syntaxe de base": """OBJECTIFS
- lire la structure d'un fichier source
- écrire des commentaires
- respecter ponctuation et terminateurs
- reconnaître les conventions du langage

POINTS CLÉS
- commentaires : // ligne, /* bloc */ (ou # selon le langage)
- les points-virgules et retours à la ligne varient selon les langages
- la casse distingue souvent les noms : Nom et nom sont deux identifiants
- l'indentation peut être significative (Python) ou simplement décorative
- les accolades délimitent les blocs dans la plupart des langages
- l'encodage UTF-8 permet d'écrire les accents sans casse

EXEMPLE
// mon premier programme
afficher("Bonjour")     // appel de fonction

/* bloc commenté :
   ignoré par le compilateur */

si (condition) {
  afficher("oui")
} sinon {
  afficher("non")
}

EN PRATIQUE
Un fichier mélange déclarations, instructions et commentaires. Lire un code
inconnu commence par repérer les blocs, les fonctions qui les composent et
les commentaires qui les décrivent.

PIÈGES À ÉVITER
- oublier une accolade : tout le reste du fichier devient incompréhensible
- coller du code depuis un document : les espaces invisibles posent problème
- commenter une ligne en la désactivant mal : un slash de trop ou de trop peu

À RETENIR
- en cas de doute sur la syntaxe : toujours un « exemple exécutable » de référence.
- la machine ignore les commentaires, les lecteurs humains s'y appuient.
""",
            "Variables et types": """OBJECTIFS
- déclarer des variables et constantes
- connaître les types fondamentaux
- convertir entre types
- choisir entre variable et constante

POINTS CLÉS
- entier, décimal, chaîne, booléen sont les quatre piliers
- constante = ne change jamais, variable = modifiable
- conversion explicite souvent nécessaire : du texte vers un nombre
- le typage est fort (erreur à la compilation) ou faible (à l'exécution)
- déclarer deux fois la même variable peut masquer la première valeur
- la saisie utilisateur est toujours du texte, quel que soit le champ

EXEMPLE
var age = 30            // entier
const TVA = 0.2         // constante
texte = "30 ans"        // chaîne
n = convertir(texte)    // renvoie 30

si age >= 18 et texte != "":
  afficher("majeur")

EN PRATIQUE
Toute saisie arrive sous forme de texte : prix, âge, quantité sont convertis
avant d'être calculés, puis reconvertis pour l'affichage. Le type d'une
variable décide des opérations que l'on peut lui appliquer.

PIÈGES À ÉVITER
- additionner deux chaînes : « 1 » + « 2 » donne « 12 » et non 3
- convertir sans vérifier : « abc » fait échouer le programme
- écrire une constante là où la règle change en cours d'année

À RETENIR
- vérifiez toujours le type renvoyé par une saisie utilisateur.
- nommez les constantes en capitales pour les repérer d'un coup d'œil.
""",
            "Contrôle de flux": """OBJECTIFS
- orienter l'exécution avec des conditions
- répéter des actions avec des boucles
- sortir ou poursuivre proprement
- choisir entre les différentes formes de boucle

POINTS CLÉS
- condition : la valeur est vraie ou fausse
- sinon : la branche alternative, avec un else ou un sinon
- boucle bornée (compteur) vs boucle conditionnelle (tant que)
- break sort immédiatement, continue passe au tour suivant
- les opérateurs de combinaison : et, ou, non
- une boucle peut parcourir une collection élément par élément

EXEMPLE
pour i dans 1 à 5:
  si i == 3: continuer
  afficher(i)

compteur = 0
tant que compteur < 3:
  compteur = compteur + 1

EN PRATIQUE
Valider une saisie, répéter une action tant que l'utilisateur le demande,
interrompre une recherche dès qu'un résultat est trouvé : le flux
conditionnel structure la moitié des écrans d'une application.

PIÈGES À ÉVITER
- une condition de boucle qui ne change jamais crée une boucle infinie
- oublier d'avancer le compteur, ou repartir de zéro à chaque tour
- placer break au mauvais niveau et sortir plus tôt que prévu

À RETENIR
- testez vos conditions avec des valeurs aux bords : 0, vide, négatif.
- une boucle qui ne finit jamais est presque toujours un problème d'état.
""",
            "Fonctions": """OBJECTIFS
- découper le code en unités nommées
- passer des paramètres et renvoyer un résultat
- documenter l'interface
- reconnaître un paramètre optionnel

POINTS CLÉS
- nom, paramètres, corps, retour : les quatre morceaux d'une fonction
- portée : une variable déclarée dans la fonction reste locale
- valeur par défaut pour les paramètres optionnels
- fonctions pures, sans effet de bord, sont faciles à tester
- une fonction qui renvoie un booléen se nomme souvent comme une question
- les fonctions s'appellent entre elles, mais pas récursivement à l'infini

EXEMPLE
fonction double(n):
  retourner n * 2

fonction saluer(nom, titre = "Bonjour"):
  afficher(titre + " " + nom)

afficher(double(4))      # 8
saluer("Babi")           # Bonjour Babi

EN PRATIQUE
Une fonction regroupe une logique réutilisée à plusieurs endroits. Quand le
même bloc de code apparaît deux fois, extrayez-le : la correction ne se fera
plus qu'à un seul endroit.

PIÈGES À ÉVITER
- créer une fonction de 80 lignes : elle cache plusieurs responsabilités
- modifier une variable globale depuis une fonction : impossible à tester
- renommer un paramètre sans mettre à jour tous les appelants

À RETENIR
- une fonction = une responsabilité, nommée en verbe.
- si vous hésitez sur son nom, c'est qu'elle n'est pas encore claire.
""",
            "Structures de données": """OBJECTIFS
- choisir entre liste, dictionnaire / map et ensemble
- parcourir et manipuler les éléments
- connaître les opérations courantes
- lire une structure imbriquée

POINTS CLÉS
- liste : ordonnée, indexée, doublons acceptés
- dictionnaire : recherche rapide par clé, paires clé / valeur
- ensemble : éléments uniques, tests d'appartenance rapides
- ajouter, supprimer, compter, trier sont les opérations de base
- l'accès par index commence à 0 pour la plupart des langages
- une liste peut contenir d'autres listes ou des enregistrements

EXEMPLE
noms = ["ada", "bob"]
notes = {"ada": 15, "bob": 12}
uniques = ensemble([1, 1, 2])     # {1, 2}

pour nom dans noms:
  afficher(nom + " : " + notes[nom])

EN PRATIQUE
Un panier est une liste ordonnée, un carnet de contacts se lit par nom, un
ensemble retient les identifiants déjà traités. Le choix du départ détermine
la facilité de tout le reste du programme.

PIÈGES À ÉVITER
- lire une clé qui n'existe pas : vérifiez son existence avant l'accès
- chercher dans une grande liste avec « in » : préférez un ensemble
- modifier une liste pendant son parcours : utilisez une copie

À RETENIR
- la structure choisie détermine la complexité des opérations suivantes.
- commencez par la structure la plus simple qui convient.
""",
            "Gestion des erreurs": """OBJECTIFS
- prévoir les cas limites (vide, nul, division par zéro)
- signaler clairement un problème
- ne jamais laisser une erreur s'échapper silencieusement
- distinguer erreur de saisie et erreur technique

POINTS CLÉS
- attraper une erreur = gérer un cas prévu, pas masquer un bug
- message d'erreur : quoi, pourquoi, que faire ensuite
- validation en entrée avant tout traitement
- ressources : fermer fichiers et connexions dans tous les cas
- une erreur remonte tant que personne ne la traite
- annoncer un échec vaut mieux qu'une exception muette

EXEMPLE
essayer:
  resultat = a / b
sinon erreur:
  afficher("problème de calcul")

si b == 0:
  afficher("division impossible : vérifiez la seconde valeur")

EN PRATIQUE
Formulaire, import de fichier, appel réseau : chaque frontière du programme
reçoit des données qui peuvent être absentes ou fausses. La validation à
l'entrée évite de devoir deviner plus loin dans le code.

PIÈGES À ÉVITER
- attraper l'erreur puis ne rien faire : le bug devient invisible
- afficher une trace technique à l'utilisateur final
- fermer un fichier avant le traitement au lieu de le fermer à la fin

À RETENIR
- tester les bords (0, vide, négatif) fait partie du développement, pas du bonus.
- un bon message d'erreur fait gagner dix minutes à qui le lit.
""",
            "Bonnes pratiques": """OBJECTIFS
- écrire un code lisible et maintenable
- nommer clairement les identifiants
- versionner et documenter
- relire son code avant de le livrer

POINTS CLÉS
- nommage explicite : compteurLignes plutôt que c
- formatage automatique (Prettier, Black…) : une seule style, jamais de débat
- commentez le POURQUOI, pas le QUOI
- git : un commit = une idée, message explicite
- petites étapes : le code fonctionne le plus souvent possible
- un fichier qui grandit sans limite se découpe en modules

EXEMPLE
# mauvais : c = n * p
# bon : totalTTC = montantHT * (1 + tauxTVA)

git add calcul.py
git commit -m "corrige le calcul de la TVA sur les arrondis"

EN PRATIQUE
Votre futur vous-même relira ce code dans six mois, et une personne de
l'équipe le relira demain. Un nom clair et un commit propre leur font
gagner du temps ; un raccourci obscur leur en coûte.

PIÈGES À ÉVITER
- commenter du code qui n'existe plus ou qui va bientôt changer
- un commit qui mélange trois correctifs distincts
- copier-coller un bloc au lieu d'extraire une fonction

À RETENIR
- le code est lu bien plus souvent qu'il n'est écrit : la lecture prime.
- si personne ne le comprend en cinq minutes, simplifiez-le.
""",
        },
        "exercises": {
            "Bonjour le monde": """ÉNONCÉ
- afficher un message de bienvenue, puis demander son prénom à l'utilisateur et le saluer personnellement.
- le salut intègre la saisie, le message initial reste inchangé.

ÉTAPES
1. afficher le message fixe au lancement
2. lire le prénom au clavier
3. afficher le salut en concaténant ou en interpolant la saisie
4. compiler puis exécuter selon votre environnement
5. relancer avec un autre prénom pour vérifier

RÉSULTAT ATTENDU
- première ligne : le message de bienvenue
- puis l'invite qui attend la saisie
- après saisie de « Babi », un nouveau salut contient Babi sur sa ligne

POUR TESTER
- saisissez un prénom avec accent : le texte doit rester correct
- saisissez un prénom composé : il doit apparaître entier dans le salut
- saisissez seulement un espace : le programme réagit sans planter

INDICE
- la saisie est toujours du texte : aucune conversion n'est nécessaire,
 il suffit de l'insérer dans le message affiché.
""",
            "Calculatrice": """ÉNONCÉ
- demander deux nombres et une opération, afficher le résultat, en refusant les entrées non numériques.
- la division par zéro est traitée comme un cas particulier.

ÉTAPES
1. lire puis convertir chaque nombre avec un test d'échec
2. lire l'opérateur : +, -, * ou /
3. calculer selon l'opérateur, avec une condition par cas
4. refuser la division par zéro avant tout calcul
5. afficher le résultat ou un message clair

RÉSULTAT ATTENDU
- 8 et 2 avec l'opérateur / donnent 4
- 8 et 0 avec le même opérateur donnent « division impossible »
- la saisie « abc » donne « nombre invalide »

POUR TESTER
- testez les quatre opérateurs, puis un caractère inconnu de la liste
- testez un nombre négatif puis un nombre décimal
- après une saisie fausse, le programme doit rester utilisable

INDICE
- une fonction convertir(texte) qui renvoie un nombre ou un échec
  centralise le contrôle : on ne l'appelle qu'une seule fois.
""",
            "Suite numérique": """ÉNONCÉ
- afficher les nombres de 1 à 100 par pas de 5, en rangées de dix valeurs, puis annoncer le nombre total d'éléments affichés.

ÉTAPES
1. boucler de 1 à 100 avec un pas de 5
2. compter chaque valeur affichée
3. passer à la ligne tous les dix éléments
4. afficher le total après la boucle
5. vérifier que la dernière rangée est complète

RÉSULTAT ATTENDU
- la première rangée commence par 1 puis 6, 11, 16…
- les valeurs finissent à 96 sans dépasser 100
- le total annoncé est 20, réparti sur deux rangées de dix

POUR TESTER
- comptez les rangées : chacune doit contenir dix valeurs
- aucun retour à la ligne ne doit se trouver en fin de sortie
- vérifiez que la sortie ne contient ni espace ni caractère superflu
- changez le pas à 10 puis à 25 et confirmez que le total suit

INDICE
- le modulo du compteur d'affichage sur dix déclenche le retour à la
  ligne : c'est un second compteur, distinct de celui des valeurs.
""",
            "Inverser une chaîne": """ÉNONCÉ
- inverser les caractères d'un mot saisi, sans utiliser (au départ) la méthode dédiée du langage.
- comparer ensuite votre résultat avec la méthode native.

ÉTAPES
1. lire le mot
2. boucler du dernier caractère au premier et accumuler le résultat
3. comparer avec la méthode native du langage
4. tester les cas limites : chaîne vide, un seul caractère
5. afficher les deux résultats pour les confronter

RÉSULTAT ATTENDU
- « programme » devient « emargorp »
- « bonjour » devient « ruojnob »
- la chaîne vide reste vide
- la version manuelle et la version native donnent le même résultat

POUR TESTER
- essayez un mot de longueur paire puis un mot de longueur impaire
- essayez un mot contenant un accent
- les deux versions doivent s'accorder sur tous les essais

INDICE
- l'accès par index commence souvent à 0 et se termine à longueur moins 1 :
  partez de l'indice le plus grand et décroissez jusqu'à zéro.
""",
            "Compteur": """ÉNONCÉ
- compter le nombre de mots d'une phrase saisie, puis le nombre d'occurrences d'un mot précis, indépendamment de la casse.

ÉTAPES
1. lire la phrase
2. découper sur les espaces pour compter les mots
3. demander le mot à compter
4. mettre la phrase et le mot en minuscules
5. parcourir, comparer chaque mot et additionner les trouvailles

RÉSULTAT ATTENDU
- « le chat et le chien » contient cinq mots
- le mot « le » y apparaît deux fois
- « Le » et « le » sont comptés exactement de la même façon
- une phrase sans espace ne contient qu'un seul mot

POUR TESTER
- phrase sans espace : le total doit rester cohérent
- espaces en début ou en fin : aucun mot vide ne doit être compté
- plusieurs espaces consécutifs ne doivent pas fausser le total
- mot absent de la phrase : le compteur affiche zéro, sans erreur

INDICE
- mettez tout en minuscules avant les comparaisons, et retirez les espaces
  superflus autour de chaque mot avant de le comparer.
""",
            "Lecture de fichier": """ÉNONCÉ
- lire un fichier texte ligne à ligne et afficher son contenu numéroté, que le fichier existe ou non.

ÉTAPES
1. demander le nom du fichier
2. ouvrir en mode lecture avec l'encodage UTF-8
3. parcourir les lignes et afficher « 1 : … », « 2 : … »
4. si le fichier n'existe pas : afficher un message clair, sans plantage
5. fermer le fichier dans tous les cas

RÉSULTAT ATTENDU
- un fichier de trois lignes produit trois lignes numérotées
- les numéros s'alignent sur la gauche, même au-delà de la ligne 9
- un nom inconnu produit un message du type « introuvable »
- aucun message technique brut n'apparaît à l'écran

POUR TESTER
- essayez un fichier vide : aucun numéro ne doit s'afficher
- essayez un nom erroné : le programme doit continuer de fonctionner
- essayez un fichier contenant des accents pour vérifier l'encodage

INDICE
- l'ouverture dans un bloc « with / try / using » ferme le fichier même
  en cas d'erreur : c'est la forme la plus sûre.
""",
            "Mini-projet": """ÉNONCÉ
- réaliser un petit outil personnel au choix : carnet d'adresses, gestionnaire de dépenses ou convertisseur d'unités, avec menu et persistance des données.

ÉTAPES
1. choisir l'outil et définir la structure de données de base
2. écrire le menu en boucle : ajouter, lister, quitter
3. implémenter l'ajout avec validation du contenu saisi
4. sauvegarder dans un fichier et recharger au démarrage
5. documenter le format du fichier et ajouter un README
6. tester la séquence complète puis relancer le programme

RÉSULTAT ATTENDU
- l'outil fonctionne de bout en bout depuis le menu
- les données ajoutées sont conservées après fermeture puis redémarrage
- l'option de sortie referme proprement le programme

POUR TESTER
- redémarrez après plusieurs ajouts : tout doit être relu correctement
- supprimez le fichier de données : le premier lancement repart de zéro
- testez la saisie vide et une entrée inconnue du menu

INDICE
- commencez par la partie « en mémoire », la sauvegarde vient ensuite :
  on ne débogue jamais deux inconnues en même temps.
""",
        },
    },
    "Flutter": {
        "lessons": {
            "Dart pour Flutter": """OBJECTIFS
- maîtriser le Dart nécessaire à Flutter
- distinguer var, final, const
- écrire du code asynchrone simple
- comprendre la nullabilité de Dart

POINTS CLÉS
- var modifie, final ne se réaffecte pas, const est connu à la compilation
- fonctions fléchées : (x) => x * 2
- nullabilité : String? et l'opérateur ?? pour la valeur de repli
- async / await diffère une opération, Future porte le résultat
- une fonction peut passer en argument : onPressed: () => faire()
- interpolation : "$nom" ou "${objet.champ}" quand le nom est composé

EXEMPLE
Future<String> charger() async {
  final donnees = await recup();
  return donnees;
}

final msg = titre ?? "Sans titre";
final double2 = (int x) => x * 2;
print("${double2(21)}");       // 42

EN PRATIQUE
Dart porte toute la logique : calculs, appels réseau, formatage. Flutter
n'affiche que ce que Dart lui fournit, et la frontière entre les deux reste
nette tout au long du développement.

PIÈGES À ÉVITER
- confondre final et const : final s'évalue à l'exécution, const non
- oublier await : la variable contient un Future et non la valeur
- déclarer un champ nullable puis l'utiliser sans le vérifier

À RETENIR
- Flutter impose l'immutabilité des widgets : c'est le cœur du modèle.
- un await oublié est le bug le plus fréquent au démarrage.
""",
            "Widgets et arbre": """OBJECTIFS
- comprendre que tout est un Widget
- composer avec StatelessWidget et StatefulWidget
- connaître les widgets essentiels de base
- lire un arbre de widgets imbriqué

POINTS CLÉS
- l'interface est un arbre reconstruit à chaque setState
- StatelessWidget : sans état, dépend de ses paramètres
- StatefulWidget : état mutable via sa classe State
- Text, Container, Scaffold, AppBar, Center, Image
- un widget ne se modifie jamais : on en construit un nouveau
- super.key identifie le widget dans l'arbre, l'analyseur le réclame

EXEMPLE
class Salut extends StatelessWidget {
  final String nom;
  const Salut({super.key, required this.nom});
  @override
  Widget build(BuildContext context) => Text("Bonjour $nom");
}

Scaffold(
  appBar: AppBar(title: const Text("Accueil")),
  body: const Center(child: Salut(nom: "Babi")),
)

EN PRATIQUE
Un écran est un Scaffold composé d'une AppBar, d'un corps et parfois d'une
barre du bas. Chaque partie se nomme dans un widget dédié afin que la
lecture de l'arbre reste immédiate.

PIÈGES À ÉVITER
- écrire un build de 200 lignes : extrayez des widgets privés
- ignorer les const proposés par l'analyseur : rendu plus lent
- réutiliser sans clé un widget qui change de position

À RETENIR
- le constructeur prend super.key : la clé identifie le widget dans l'arbre.
- si build est difficile à lire, c'est que l'arbre doit être découpé.
""",
            "Mise en page": """OBJECTIFS
- structurer l'écran avec Row, Column et Stack
- gérer l'espace avec Expanded, Padding, SizedBox
- aligner avec MainAxis et CrossAxis
- éviter les débordements d'écran

POINTS CLÉS
- Row = horizontale, Column = verticale
- Expanded occupe l'espace restant, Flexible se limite à une part
- mainAxisAlignment aligne sur l'axe principal, crossAxisAlignment sur l'autre
- Stack superpose, Positioned place un enfant dans un Stack
- Padding crée une marge intérieure, SizedBox impose une taille
- un parent non borné qui reçoit Expanded déclenche une erreur de rendu

EXEMPLE
Row(
  children: [
    const Icon(Icons.star),
    const SizedBox(width: 8),
    Expanded(child: Text(titre, overflow: TextOverflow.ellipsis)),
  ],
)

Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [Text("Titre"), Text("Sous-titre")],
)

EN PRATIQUE
Ligne d'icône et de texte, en-tête et corps superposés à un voile teinté :
la quasi-totalité des écrans se construit avec ces quelques dispositions.

PIÈGES À ÉVITER
- Row dans un Column non borné : la hauteur devient infinie
- oublier Expanded : le texte dépasse et le layout casse
- empiler padding dans padding : une seule marge suffit

À RETENIR
- un Row dans un Column borné : toujours donner une contrainte de hauteur.
- quand ça déborde, réduisez d'abord la largeur d'un Expanded.
""",
            "Gestion d'état": """OBJECTIFS
- mettre à jour l'interface avec setState
- comprendre le cycle de vie du State
- savoir où placer le State
- éviter les reconstructions inutiles

POINTS CLÉS
- setState(() { ... }) déclenche la reconstruction du widget
- initState : une fois à la création ; dispose : à la destruction
- l'état va le plus bas possible, le plus haut s'il est partagé
- les widgets sont immuables : on remplace, on ne modifie pas
- didUpdateWidget réagit au changement des paramètres reçus
- une valeur qui se déduit se calcule dans build, pas dans le State

EXEMPLE
class Compteur extends StatefulWidget {
  @override
  State<Compteur> createState() => _CompteurState();
}
class _CompteurState extends State<Compteur> {
  int n = 0;
  @override
  void initState() {
    super.initState();        // toujours la première ligne
  }
  @override
  Widget build(BuildContext context) => Text("$n");
}

EN PRATIQUE
Compteur de clics, champ qui active un bouton, sélection dans une liste :
chaque écran interactif conserve son état dans une classe State dédiée.

PIÈGES À ÉVITER
- setState sans changement réel : reconstructions inutiles
- modifier un champ puis oublier setState : l'écran ne bouge pas
- placer l'état trop haut : tout l'arbre se reconstruit aussi

À RETENIR
- setState sans changement réel provoque des reconstructions inutiles.
- l'état vit le plus bas possible dans l'arbre.
""",
            "Boutons et champs": """OBJECTIFS
- créer des boutons et des champs de saisie
- gérer les événements de tap et de frappe
- valider un formulaire
- lire la valeur saisie au moment utile

POINTS CLÉS
- ElevatedButton(onPressed: () { ... }, child: ...)
- onPressed: null désactive le bouton
- TextField avec onChanged et controller
- Form + GlobalKey<FormState> + validator pour la validation
- obscureText masque un mot de passe
- keyboardType affiche le clavier adapté à la saisie

EXEMPLE
final ctrl = TextEditingController();
TextField(
  controller: ctrl,
  onChanged: (v) => setState(() {}),
  decoration: const InputDecoration(labelText: "Nom"),
)
ElevatedButton(
  onPressed: ctrl.text.isEmpty ? null : () => ajouter(ctrl.text),
  child: const Text("Ajouter"),
)

EN PRATIQUE
Connexion, création de compte, recherche : chaque formulaire combine des
champs, un bouton conditionnel et un message d'erreur affiché sous le champ
qui a échoué.

PIÈGES À ÉVITER
- oublier dispose() : le controller survit à la mort de l'écran
- lire la valeur pendant build au lieu du moment de l'appui
- désactiver un bouton sans explication : l'utilisateur est bloqué

À RETENIR
- libérez les controllers dans dispose() : pas de fuite mémoire.
- un bouton désactivé doit s'accompagner d'une explication.
""",
            "Listes défilantes": """OBJECTIFS
- afficher une liste avec ListView
- construire à la volée avec ListView.builder
- gérer l'ajout et la suppression dynamiques
- choisir la bonne clé pour chaque élément

POINTS CLÉS
- ListView construit tous ses enfants d'un coup : listes courtes seulement
- ListView.builder : itemBuilder ne construit que les lignes visibles
- itemBuilder : (context, index) => widget
- Clés (ValueKey) stabilisent les éléments modifiés ou supprimés
- ListView.separator insère un séparateur entre les éléments
- SingleChildScrollView reçoit un contenu d'une seule page

EXEMPLE
ListView.builder(
  itemCount: taches.length,
  itemBuilder: (ctx, i) => ListTile(
    key: ValueKey(taches[i].id),
    title: Text(taches[i].texte),
    trailing: const Icon(Icons.delete),
  ),
)

EN PRATIQUE
Messages, produits, contacts : toute liste potentiellement longue passe par
builder pour ne construire que ce qui se trouve à l'écran, au prix d'une
mémoire très raisonnable.

PIÈGES À ÉVITER
- ListView avec des centaines d'enfants : l'écran rame à l'affichage
- oublier itemCount : erreur de rendu ou liste vide
- clés dupliquées : les animations et les états se décalent

À RETENIR
- builder pour toute liste potentiellement longue : performance gratuite.
- donnez une clé stable à chaque élément modifié ou supprimé.
""",
            "Navigation": """OBJECTIFS
- naviguer entre écrans avec Navigator
- passer et recevoir des arguments
- gérer le retour et l'empilement des routes

POINTS CLÉS
- MaterialPageRoute builder: (context) => Ecran(...)
- push renvoie un Future : await permet de récupérer le résultat
- pop(valeur) ferme l'écran en renvoyant une donnée
- arguments : constructeur du widget ou RouteSettings
- pushReplacement remplace l'écran courant, utile après connexion
- popUntil revient jusqu'à une route précise de la pile

EXEMPLE
final choix = await Navigator.push<String>(
  context,
  MaterialPageRoute(builder: (_) => EcranChoix()),
);
if (choix != null) setState(() => valeur = choix);

Navigator.pop(context, "Babi");   // côté écran fils

EN PRATIQUE
Liste vers détail, écran de connexion vers accueil, boîte de dialogue qui
renvoie un choix : toute navigation repose sur push et pop, et le résultat
revient sous forme de Future.

PIÈGES À ÉVITER
- appuyer sans await : le résultat arrive et personne ne l'écoute
- pousser un écran dans une boucle : l'historique explose
- passer les données par une variable globale : difficile à tester

À RETENIR
- passez les données par constructeur : testable et clair, pas de singleton.
- tout push qui attend un résultat a besoin d'un await quelque part.
""",
            "Réseau et données": """OBJECTIFS
- appeler une API avec package:http
- décoder le JSON en objets Dart
- gérer chargement, erreur et état vide
- afficher les trois états d'un écran de données

POINTS CLÉS
- http.get renvoie une Response, jsonDecode(response.body) donne la structure
- FutureBuilder ou setState après await
- typer la réponse et vérifier statusCode (200)
- états affichés : chargement, données, erreur
- Uri.parse construit l'URL, y compris avec des paramètres
- sérialiser un objet avec toMap et fromJson

EXEMPLE
final r = await http.get(Uri.parse(url));
if (r.statusCode == 200) {
  final data = jsonDecode(r.body) as List;
  setState(() => articles = data.map(Article.fromMap).toList());
} else {
  setState(() => erreur = "HTTP ${r.statusCode}");
}

EN PRATIQUE
Catalogue, météo, fil d'actualités : presque tous les écrans d'une
application lisent une API et doivent afficher les trois états : chargement,
contenu, échec.

PIÈGES À ÉVITER
- appeler http dans build : la requête repart à chaque reconstruction
- ignorer statusCode : un 500 serait lu comme des données
- laisser l'état vide sans message : l'utilisateur croit à un bug

À RETENIR
- prévoyez toujours l'échec réseau : pas de Wi-Fi, timeout, erreur serveur.
- chaque écran de données affiche chargement, contenu ou erreur.
""",
        },
        "exercises": {
            "Bonjour Flutter": """ÉNONCÉ
- partir du projet flutter create par défaut et personnaliser l'écran d'accueil : titre du AppBar, texte affiché au centre et couleur du thème.
- le compteur du projet doit continuer de fonctionner.

ÉTAPES
1. flutter create mon_app puis flutter run
2. modifier MaterialApp(title:, theme:) et le Text du centre
3. remplacer la couleur primaire du thème
4. recharger avec « r » dans le terminal
5. vérifier le rendu sur un écran plus étroit

RÉSULTAT ATTENDU
- l'AppBar affiche le titre choisi
- le centre affiche le message d'accueil personnalisé, à la couleur définie
- le compteur s'incrémente toujours au clic, sans erreur dans la console

POUR TESTER
- tapez « r » après modification : le changement apparaît sans rebuild complet
- modifiez un seul fichier : seul ce fichier est recompilé
- lancez flutter analyze : aucun avertissement nouveau n'apparaît

INDICE
- flutter run relance le hot reload sur « r » : inutile de relancer le
  build complet à chaque changement.
""",
            "Compteur de clics": """ÉNONCÉ
- un bouton incrémente un compteur affiché au centre, un second le remet à zéro, un troisième le décrémente.
- les trois boutons partagent une même ligne.

ÉTAPES
1. StatefulWidget avec int _n = 0 dans le State
2. ElevatedButton(onPressed: () => setState(() => _n++), ...)
3. boutons − / + / reset disposés dans une Row
4. afficher _n au centre dans un Text
5. empiler Row et Text dans une Column centrée

RÉSULTAT ATTENDU
- le premier appui sur + affiche 1, le second affiche 2
- l'appui sur − redescend le compteur, y compris sous zéro si vous l'autorisez
- reset ramène l'affichage à 0, et ce à chaque appui

POUR TESTER
- appuyez dix fois très vite : le compteur suit sans manquer d'appui
- retirez setState d'un bouton : rien ne bouge, preuve de son rôle
- rechargement à chaud : le compteur repart bien de zéro

INDICE
- tout changement d'affichage passe par setState : sans lui, rien ne bouge.
""",
            "Liste de tâches": """ÉNONCÉ
- liste de tâches ajoutables par un champ en haut, cochables et supprimables, avec un compteur « x / y » des tâches terminées.
- la saisie vide est refusée.

ÉTAPES
1. List<Tache> dans le State, ListView.builder pour l'affichage
2. champ + bouton d'ajout, avec test de la saisie vide
3. Checkbox pour basculer faite / pas faite
4. icône de suppression et Text du compteur en bas
5. donner une clé stable à chaque ListTile

RÉSULTAT ATTENDU
- ajouter « coder » fait apparaître une nouvelle ligne
- cocher cette ligne augmente le compteur affiché en bas
- appuyer sur la corbeille retire la ligne et met le compteur à jour

POUR TESTER
- ajoutez trois tâches puis cochez-en deux : le compteur affiche 2 / 3
- saisissez seulement des espaces : rien ne s'ajoute
- supprimez une tâche cochée : le compteur redescend

INDICE
- passez la clé (key: ValueKey(t.id)) à la ListTile pour un rebuild fiable.
""",
            "Convertisseur": """ÉNONCÉ
- convertisseur entre Celsius et Fahrenheit avec deux champs de saisie et un bouton d'inversion du sens de conversion.
- la conversion se déclenche à la demande.

ÉTAPES
1. déclarer deux TextEditingController
2. mémoriser le sens courant dans un booléen du State
3. bouton de sens qui inverse ce booléen dans un setState
4. calculer C × 9/5 + 32 ou (F − 32) × 5/9 selon le sens
5. afficher le résultat arrondi et traiter la saisie invalide

RÉSULTAT ATTENDU
- 0 degré Celsius donne 32.0 degrés Fahrenheit
- basculer le sens recalcule dans l'autre sens sans effacer la saisie
- une saisie non numérique affiche un message d'erreur

POUR TESTER
- essayez 100 puis la conversion inverse : vous retrouvez 100
- saisissez un nombre négatif puis un nombre décimal
- laissez un champ vide : aucun résultat ne doit s'afficher

INDICE
- double.tryParse() renvoie null au lieu de planter sur une saisie fausse :
  c'est ce test null qui déclenche le message d'erreur.
""",
            "Quiz": """ÉNONCÉ
- mini-quiz de 5 questions : une question par écran, boutons de réponse, puis un écran final affichant le score avec la possibilité de rejouer.

ÉTAPES
1. créer une classe Question (énoncé, réponses, index de la bonne)
2. écran question : un bouton par réponse, passage à la suivante
3. incrémenter le score seulement si la réponse choisie est la bonne
4. écran final : score sur 5 et bouton « Rejouer »
5. utiliser pushReplacement ou popUntil pour repartir de zéro

RÉSULTAT ATTENDU
- les 5 questions défilent une par une, dans l'ordre
- le score final s'affiche sous la forme « x / 5 »
- le bouton de reprise revient à la première question, score remis à zéro

POUR TESTER
- répondez volontairement faux partout : le score affiche 0 / 5
- répondez juste partout : le score affiche 5 / 5
- revenez en arrière pendant le quiz : la pile ne s'allonge pas indéfiniment

INDICE
- conservez l'index de la question et le score dans le State de l'écran
  racine, ou transmettez-les par constructeur à chaque nouvel écran.
""",
            "Fil d'actualité": """ÉNONCÉ
- fil d'actualités simulé : ListView.builder sur une liste de posts (auteur, texte, date), avec un indicateur de chargement au démarrage.
- un bouton permet de relancer la lecture.

ÉTAPES
1. créer une classe Post avec fromMap
2. FutureBuilder ou setState avec un délai pour simuler le chargement
3. itemBuilder construit une Card par post
4. gérer les états : CircularProgressIndicator, liste, message d'erreur
5. ajouter un bouton de rechargement qui relance la simulation

RÉSULTAT ATTENDU
- l'indicateur tourne environ une seconde, puis dix cartes s'affichent
- chaque carte montre l'auteur, le texte et la date du post
- le rechargement repasse par l'indicateur avant de réafficher la liste

POUR TESTER
- comptez les cartes construites : elles doivent correspondre à la liste
- simulez une erreur : le message remplace la liste, il ne s'y ajoute pas
- changez la durée du délai : le temps d'affichage de l'indicateur suit

INDICE
- jamais de await directement dans build : le futur serait relancé à
  chaque reconstruction. Conservez-le dans une variable du State.
""",
            "ToDo persistant": """ÉNONCÉ
- la liste de tâches survit à la fermeture de l'application : sauvegarde et relecture d'un fichier JSON dans les documents de l'application.

ÉTAPES
1. ajouter path_provider et obtenir le répertoire documents
2. écrire la liste serialisée à chaque modification
3. lire au démarrage, si le fichier existe, et remplir l'état
4. gérer le fichier absent au premier lancement
5. effectuer l'écriture de façon asynchrone, sans bloquer l'interface

RÉSULTAT ATTENDU
- les tâches ajoutées sont toujours présentes après fermeture et relance
- le premier lancement démarre avec une liste vide et sans erreur
- l'ordre d'ajout des tâches reste conservé d'une session à l'autre

POUR TESTER
- ajoutez deux tâches puis relancez : elles réapparaissent à l'identique
- supprimez le fichier JSON puis relancez : tout repart de zéro, sans plantage
- cassez le JSON à la main : un message clair remplace la liste

INDICE
- encodeJson d'une List<Map> suffit : chaque Tache fournit toMap / fromMap,
  et l'écriture se fait dans un bloc await.
""",
        },
    },
}
