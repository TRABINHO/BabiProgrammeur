"""Corrections commentées — lot 5 : Kotlin, Flutter, Autre.

Une entrée par exercice du curriculum (titre exact, copié-collé depuis
core/curriculum.py, clé "exercises" obligatoire) :

    CONTENT["Kotlin"]["exercises"]["FizzBuzz"] = \"\"\"SOLUTION
    ...
    \"\"\"

Fusionnées dans core/solutions.py. Contrôle :
    python tests/check_solutions.py Kotlin Flutter Autre
"""
CONTENT = {
    "Kotlin": {
        "exercises": {
            "Bonjour main": """SOLUTION

fun main() {
    val nom = "Babi"
    val lecon = 1
    println("Bonjour, $nom !")
    println("Nous sommes à la leçon $lecon.")
    print("Sans retour à ligne")
    print(", donc tout tient sur une seule ligne.")
    println()
}

EXPLICATION

fun main() est le point d'entrée du programme : la machine appelle cette
fonction en premier puis exécute les instructions ligne après ligne.
println écrit le texte et place ensuite le curseur sur la ligne
suivante ; print s'arrête à la fin du texte. Entre guillemets, $nom est
un gabarit de chaîne : Kotlin remplace $nom par la valeur de la variable
avant d'afficher. Les accolades délimitent le corps de la fonction ;
l'indentation ne change pas la compilation mais elle rend le bloc lisible
pour celui qui relira le code.

POINTS DE VÉRIFICATION

- Sortie : « Bonjour, Babi ! » puis « Nous sommes à la leçon 1. », puis
  les deux phrases de print réunies sur une seule ligne.
- $nomX chercherait une variable nomX : écris ${nom} avec des accolades
  dès que le nom se poursuit dans le texte.
- Une accolade oubliée ou une instruction écrite avant fun main()
  empêchent la compilation : erreur de débutant très fréquente.

POUR ALLER PLUS LOIN

- Lire une saisie avec val saisie = readLine(), puis l'afficher : le
  programme devient interactif.
- Concaténer avec + (« Total : " + total) quand le gabarit devient long.
""",
            "Calculatrice": """SOLUTION

fun operer(a: Int, b: Int, op: Char): String = when (op) {
    '+' -> "Somme : ${a + b}"
    '-' -> "Différence : ${a - b}"
    '*' -> "Produit : ${a * b}"
    '/' -> if (b == 0) "Division impossible" else "Quotient : ${a / b}"
    else -> "Opérateur inconnu : $op"
}

fun main() {
    println(operer(7, 2, '+'))
    println(operer(7, 0, '/'))
    println(operer(7, 2, '?'))
}

EXPLICATION

when est utilisé comme expression : il produit une valeur au lieu de
seulement déclencher une action. Chaque branche a la forme « valeur ->
résultat » et else garantit qu'une branche correspond toujours : sans
lui, le code ne compile pas si des cas restent possibles. Le test
if (b == 0) est indispensable car diviser par zéro lève une
ArithmeticException en Kotlin. Toutes les branches renvoient une chaîne,
compatible avec le type String annoncé au départ.

POINTS DE VÉRIFICATION

- operer(7, 2, '+') affiche « Somme : 9 » et operer(7, 2, '*') « Produit : 14 ».
- operer(7, 0, '/') affiche « Division impossible » au lieu de planter.
- operer(7, 2, '?') tombe dans else : « Opérateur inconnu : ? ».
- Un when sans else qui reste incomplet déclenche une erreur de
  compilation : Kotlin exige l'exhaustivité.

POUR ALLER PLUS LOIN

- Combiner des cas avec '+', '-' -> « Opération signée » : une seule
  branche peut traiter plusieurs valeurs.
""",
            "Liste de tâches": """SOLUTION

data class Tache(val id: Int, var titre: String, var faite: Boolean = false)

fun main() {
    val taches = mutableListOf(          // la liste reste modifiable
        Tache(1, "Lire la leçon"),
        Tache(2, "Faire les exercices")
    )
    taches += Tache(3, "Tester le code")
    taches[0] = taches[0].copy(faite = true)
    for (t in taches) {
        val marque = if (t.faite) "[x]" else "[ ]"
        println("$marque ${t.id} ${t.titre}")
    }
    println("Reste à faire : ${taches.count { !it.faite }}")
}

EXPLICATION

data class sert de petite structure : le constructeur primaire déclare
les propriétés et Kotlin fabrique gratuitement equals, hashCode,
toString et copy. mutableListOf crée une liste vraiment mutable : +=
ajoute un élément, [i] remplace celui d'un rang. copy(faite = true)
produit une version modifiée sans toucher à l'original. Enfin
count { !it.faite } filtre puis compte les tâches qui restent à faire.

POINTS DE VÉRIFICATION

- Trois lignes affichées : [x] pour la première, [ ] pour les deux autres.
- « Reste à faire : 2 », car deux tâches ont encore faite = false.
- equals compare les champs : Tache(1, "a") == Tache(1, "a") est vrai.

POUR ALLER PLUS LOIN

- Déclarer la variable en MutableList<Tache> rend la mutabilité visible.
- Passer à listOf fait échouer les ajouts : origine de la souplesse.
""",
            "FizzBuzz": """SOLUTION

fun main() {
    for (n in 1..100) {
        val mot = when {
            n % 15 == 0 -> "FizzBuzz"
            n % 3 == 0 -> "Fizz"
            n % 5 == 0 -> "Buzz"
            else -> n.toString()
        }
        println(mot)
    }
}

EXPLICATION

Le when sans argument évalue des conditions booléennes dans l'ordre : la
première vraie l'emporte et les suivantes ne sont même pas regardées.
C'est pourquoi n % 15 == 0 passe en premier : 15 réunit les deux règles
et doit afficher FizzBuzz, alors qu'un test 3 avant 15 afficherait Fizz
et ferait disparaître le mot FizzBuzz. L'opérateur % donne le reste de
la division entière : il vaut 0 exactement quand le nombre est divisible.
else renvoie n.toString() car toutes les branches doivent produire le
même type, ici String.

POINTS DE VÉRIFICATION

- 15, 30, 45 affichent FizzBuzz ; 3, 6, 9 affichent Fizz ; 5, 10 Buzz.
- 1 affiche 1 et 100 affiche Buzz, car 100 = 5 × 20.
- Trois when indépendants afficheraient Fizz puis Buzz sur deux lignes
  pour 15 : c'est l'ordre des branches qui l'évite.

POUR ALLER PLUS LOIN

- Extraire fun motPour(n: Int) et écrire println(motPour(n)) : le main
  ne reste qu'une boucle d'affichage.
- Parcourir (1..100).forEach { println(motPour(it)) } pour pratiquer
  les fonctions d'ordre supérieur.
""",
            "Statistiques": """SOLUTION

fun main() {
    val notes = listOf(12, 8, 15, 10, 19, 6, 14)
    val total = notes.sum()
    val moyenne = total.toDouble() / notes.size
    val mini = notes.min()
    val maxi = notes.max()
    val admis = notes.count { it >= 10 }
    println("Notes : $notes")
    println("Total $total, moyenne ${"%.2f".format(moyenne)}")
    println("Mini $mini, maxi $maxi, admis $admis sur ${notes.size}")
}

EXPLICATION

listOf construit une liste d'entiers non mutable. sum(), size, min(),
max() et count viennent de la bibliothèque standard ; dans count { },
it désigne l'élément courant et la condition it >= 10 ne garde que les
notes admises. sum() renvoie un Int : diviser directement par size
donnerait un quotient entier, d'où toDouble() avant la division. Enfin
"%.2f".format(moyenne) limite l'affichage à deux décimales sans altérer
la valeur calculée.

POINTS DE VÉRIFICATION

- Total = 84 et moyenne = 12.0 pour 7 notes ; sans toDouble, la
  division entière masquerait les décimales.
- mini = 6, maxi = 19, admis = 5 sur 7.
- max() sur liste vide lève une exception : pensez au cas d'une liste
  vide avant d'afficher des statistiques.

POUR ALLER PLUS LOIN

- Calculer la médiane : notes.sorted() puis l'élément d'indice size / 2,
  la valeur qui coupe la série en deux.
""",
            "Extension utile": """SOLUTION

// Extension : une méthode nouvelle sur String, sans toucher à la classe
fun String.nombreDeMots(): Int =
    trim().split(" ").count { it.isNotEmpty() }

fun String.encadre(): String = "« ${trim()} »"

fun main() {
    val phrase = "  Kotlin est   sympa  "
    println(phrase.nombreDeMots())   // 3
    println(phrase.encadre())        // « Kotlin est   sympa »
    println("abc".nombreDeMots())    // 1
}

EXPLICATION

Une extension se déclare en écrivant le type receveur avant le point :
fun String.nombreDeMots() devient appelable comme une méthode native de
toute String. À l'intérieur, this désigne le texte reçu ; trim() retire
les espaces de bord, split(" ") découpe sur les espaces et count avec
it.isNotEmpty() écarte les chaînes vides laissées par les espaces
multiples. L'extension ne modifie pas String : elle est compilée en
fonction statique et n'a aucun accès aux membres privés.

POINTS DE VÉRIFICATION

- «  Kotlin est   sympa  » donne 3 mots, les vides étant ignorés.
- "abc" renvoie 1 : une chaîne sans espace contient un seul mot.
- encadre() retire les espaces de bord et ajoute les guillemets.

POUR ALLER PLUS LOIN

- Regrouper ces fonctions dans un fichier d'extensions partagé, à
  réutiliser dans toute l'application.
- Écrire fun Int.pair() qui renvoie « pair » ou « impair » selon le
  reste de la division par deux.
""",
            "Compteur asynchrone": """SOLUTION

import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    println("Début")
    val job = launch {
        for (i in 1..5) {
            delay(300)              // attend sans bloquer le thread
            println("Tick $i")
        }
    }
    job.join()                      // attend la fin du compteur
    println("Fin")
}

EXPLICATION

runBlocking sert de pont : elle transforme la fonction main en corotine
suspendue, ce qui autorise delay et launch. launch part sans attendre
et renvoie un Job, une poignée sur le travail lancé. delay est suspend :
elle libère le thread pendant les 300 ms, au lieu de le gaspiller comme
le ferait Thread.sleep. join suspend la coroutine principale jusqu'à la
fin du job ; sans lui, « Fin » serait affiché presque aussitôt, pendant
que les ticks continueraient en arrière-plan.

POINTS DE VÉRIFICATION

- Ordre console : Début, Tick 1 à Tick 5 espacés d'environ 300 ms, puis
  Fin.
- Durée totale environ 1,5 s : cinq attentes mais un seul thread utilisé.
- Sans job.join(), Fin arrive avant les ticks : c'est la durée de vie
  d'une coroutine non attendue.

POUR ALLER PLUS LOIN

- Passer un Dispatchers.Default à launch pour déplacer les calculs sur
  un pool de threads dédié.
- Remplacer launch par async puis await() pour récupérer une valeur.
""",
        },
    },
    "Flutter": {
        "exercises": {
            "Bonjour Flutter": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaPremiereApp());

class MaPremiereApp extends StatelessWidget {
  const MaPremiereApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // le widget racine fournit thème et navigation
      title: 'Bonjour Flutter',
      home: Scaffold(
        appBar: AppBar(title: const Text('Bonjour Flutter')),
        body: const Center(child: Text('Ma première application !')),
      ),
    );
  }
}

EXPLICATION

runApp reçoit le widget racine : un MaterialApp fournit le thème, la
navigation et le canevas, puis Scaffold donne une barre et un corps.
Center centre son enfant et Text affiche le message. Tout est const car
rien ne change à l'exécution : Flutter évite alors des reconstructions
inutiles. StatelessWidget suffit tant qu'aucun état n'évolue, build ne
servant qu'à décrire l'arbre à afficher.

POINTS DE VÉRIFICATION

- L'écran affiche « Bonjour Flutter » dans la barre et le message
  centré au milieu du corps.
- Changer le texte ou ajouter un style suffit à personnaliser
  l'application : aucune autre ligne n'est à toucher.
- Oublier const devant le constructeur déclenche un avertissement de
  l'analyseur Dart.

POUR ALLER PLUS LOIN

- Ajouter un FloatingActionButton avec onPressed pour découvrir
  l'état avec setState.
""",
            "Compteur de clics": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: CompteurPage()));

class CompteurPage extends StatefulWidget {
  const CompteurPage({super.key});
  @override
  State<CompteurPage> createState() => _CompteurPageState();
}

class _CompteurPageState extends State<CompteurPage> {
  int _clics = 0;   // état : il vit dans le State, pas dans build

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Compteur')),
      body: Center(
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Text('Clics : $_clics'),
          ElevatedButton(
            onPressed: () => setState(() => _clics++),
            child: const Text('Ajouter un clic'),
          ),
        ]),
      ),
    );
  }
}

EXPLICATION

StatelessWidget ne peut pas changer : build lirait une valeur fixe.
CompteurPage délègue donc à _CompteurPageState, qui porte l'état
_clics. Le bouton reçoit onPressed : sans cette fonction il serait
grisé. setState exécute l'incrément puis déclare le widget sale, ce qui
rappelle build avec la nouvelle valeur.

POINTS DE VÉRIFICATION

- Premier affichage « Clics : 0 », puis 1, 2, 3 après chaque appui.
- Sans setState, la variable grandit mais l'écran reste bloqué.
- mainAxisAlignment centre la colonne au milieu de l'écran.

POUR ALLER PLUS LOIN

- Ajouter un bouton « Remettre à zéro » qui remet _clics à 0.
""",
            "Liste de tâches": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: TachesPage()));

class TachesPage extends StatefulWidget {
  const TachesPage({super.key});
  @override
  State<TachesPage> createState() => _TachesPageState();
}

class _TachesPageState extends State<TachesPage> {
  final _taches = ['Lire la leçon', 'Faire les exercices'];  // source de vérité
  final _champ = TextEditingController();

  void _ajouter() {
    final texte = _champ.text.trim();
    if (texte.isEmpty) return;   // saisie vide ignorée
    setState(() {
      _taches.add(texte);
      _champ.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ma liste')),
      body: ListView(children: [
        TextField(controller: _champ),
        for (final t in _taches)
          ListTile(
            title: Text(t),
            trailing: IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () => setState(() => _taches.remove(t)),
            ),
          ),
      ]),
      floatingActionButton: FloatingActionButton(
        onPressed: _ajouter,
        child: const Icon(Icons.add),
      ),
    );
  }
}

EXPLICATION

La liste _taches vit dans le State : c'est la source de vérité affichée.
_ajouter refuse une saisie vide, puis ajoute la tâche et vide le champ
dans un seul setState, donc un seul rebuild. Le contrôleur permet de
lire et de vider le champ ; la boucle for crée un ListTile par tâche et
l'icône de suppression la retire.

POINTS DE VÉRIFICATION

- Deux tâches au départ ; valider une saisie vide ne change rien.
- Après ajout, la tâche apparaît et le champ se vide seul.

POUR ALLER PLUS LOIN

- Donner une Key à chaque ListTile pour réutiliser les cellules.
- Libérer le contrôleur avec _champ.dispose() dans dispose().
""",
            "Convertisseur": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ConvertPage()));

class ConvertPage extends StatefulWidget {
  const ConvertPage({super.key});
  @override
  State<ConvertPage> createState() => _ConvertPageState();
}

class _ConvertPageState extends State<ConvertPage> {
  final _c = TextEditingController();
  String _resultat = '';

  void _convertir() {
    final t = double.tryParse(_c.text.replaceAll(',', '.'));  // null si invalide
    setState(() {
      _resultat = t == null
          ? 'Nombre invalide'
          : '${t.toStringAsFixed(1)} °C = ${((t * 9 / 5) + 32).toStringAsFixed(1)} °F';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Convertisseur')),
      body: Column(children: [
        TextField(
          controller: _c,
          onChanged: (_) => _convertir(),
          decoration: const InputDecoration(labelText: 'Température en °C'),
        ),
        Text(_resultat),
      ]),
    );
  }
}

EXPLICATION

Le contrôleur _c suit la saisie et onChanged déclenche la conversion à
chaque frappe : le champ reste la seule source de vérité. double.tryParse
renvoie null si le texte n'est pas un nombre, d'où le message « Nombre
invalide » au lieu d'une exception. replaceAll(',', '.') accepte la
virgule des claviers français. La formule °F = °C × 9 ÷ 5 + 32 est
affichée avec une décimale grâce à toStringAsFixed(1).

POINTS DE VÉRIFICATION

- 100 donne « 100.0 °C = 212.0 °F », 0 donne 32.0 °F et -40 reste
  -40.0 °F, point de croisement des deux échelles.
- Une saisie « abc » affiche « Nombre invalide », sans planter.

POUR ALLER PLUS LOIN

- Ajouter un bouton « Effacer » qui vide _c et remet _resultat.
- Afficher l'unité dans un Text séparé pour préparer une traduction.
""",
            "Quiz": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: QuizPage()));

class QuizPage extends StatefulWidget {
  const QuizPage({super.key});
  @override
  State<QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends State<QuizPage> {
  final _questions = ['2 + 2 = ?', 'Capitale de la France ?'];
  final _reponses = [['3', '4'], ['Lyon', 'Paris']];
  final _bonnes = [1, 1];   // indice de la bonne réponse
  int _i = 0;               // question en cours
  int _score = 0;

  void _repondre(int choix) {
    setState(() {
      if (choix == _bonnes[_i]) _score++;
      _i++;
    });
  }

  @override
  Widget build(BuildContext context) {
    final fini = _i >= _questions.length;
    return Scaffold(
      appBar: AppBar(title: Text(fini ? 'Résultat' : 'Question ${_i + 1}')),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: fini
            ? [
                Text('Score : $_score / ${_questions.length}'),
                ElevatedButton(
                  onPressed: () => setState(() {
                    _i = 0;
                    _score = 0;
                  }),
                  child: const Text('Recommencer'),
                ),
              ]
            : [
                ListTile(title: Text(_questions[_i])),
                for (var r = 0; r < _reponses[_i].length; r++)
                  ListTile(
                    title: Text(_reponses[_i][r]),
                    onTap: () => _repondre(r),
                  ),
              ],
      ),
    );
  }
}

EXPLICATION

Les trois listes parallèles portent l'énoncé, les réponses et l'indice
de la bonne réponse : même indice = même question. _repondre compare
puis incrémente _i dans un seul setState, donc build affiche aussitôt la
question suivante. Quand _i dépasse le nombre de questions, fini devient
vrai et le body bascule sur l'écran de score, Recommencer remettant _i
et _score à zéro.

POINTS DE VÉRIFICATION

- Répondre juste donne « Score : 1 / 2 » ; faux puis juste aussi 1 / 2.
- Après deux réponses, plus aucune ListTile : le score s'affiche.
- Sans setState, le score change en mémoire mais l'écran reste figé.

POUR ALLER PLUS LOIN

- Regrouper énoncé, réponses et bonne indice dans une classe Question.
""",
            "Fil d'actualité": """SOLUTION

import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: FilPage()));

class Article {
  final String titre;
  final String image;
  const Article(this.titre, this.image);
}

class FilPage extends StatelessWidget {
  const FilPage({super.key});

  @override
  Widget build(BuildContext context) {
    // les données sont fabriquées une seule fois
    final articles = List.generate(
      30,
      (i) => Article('Article ${i + 1}',
          'https://picsum.photos/seed/$i/120/120'),
    );
    return Scaffold(
      appBar: AppBar(title: const Text("Fil d'actualité")),
      body: ListView.builder(
        itemCount: articles.length,
        itemBuilder: (context, i) {
          final a = articles[i];
          return ListTile(
            leading: Image.network(a.image,
                width: 56, height: 56, fit: BoxFit.cover),
            title: Text(a.titre),
            subtitle: const Text('Aperçu de la publication…'),
          );
        },
      ),
    );
  }
}

EXPLICATION

ListView.builder ne fabrique que les lignes visibles : i va de 0 à
itemCount moins un, ce qui évite de créer trente widgets d'un coup.
Image.network télécharge en arrière-plan ; width, height et BoxFit.cover
forcent un carré de 56 pixels, sans quoi l'image casserait l'alignement.

POINTS DE VÉRIFICATION

- Trente « Article 1 » à « Article 30 » défilent sans ralentissement.
- Les vignettes sont carrées et recadrées, jamais déformées.
- Sans connexion, l'espace de l'image reste vide.

POUR ALLER PLUS LOIN

- Ajouter onTap avec Navigator.push pour ouvrir une page de détail.
""",
            "ToDo persistant": """SOLUTION

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(const MaterialApp(home: TodoPage()));

class TodoPage extends StatefulWidget {
  const TodoPage({super.key});
  @override
  State<TodoPage> createState() => _TodoPageState();
}

class _TodoPageState extends State<TodoPage> {
  List<String> _taches = [];

  @override
  void initState() {
    super.initState();
    _charger();   // lecture du JSON dès le démarrage
  }

  Future<void> _charger() async {
    final prefs = await SharedPreferences.getInstance();
    final brut = prefs.getString('taches');
    setState(() {
      _taches = brut == null ? <String>[] : List<String>.from(jsonDecode(brut));
    });
  }

  void _ajouter() async {
    setState(() => _taches.add('Tâche ${_taches.length + 1}'));
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('taches', jsonEncode(_taches));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ToDo persistant')),
      body: ListView(children: [for (final t in _taches) ListTile(title: Text(t))]),
      floatingActionButton: FloatingActionButton(
        onPressed: _ajouter,
        child: const Icon(Icons.add),
      ),
    );
  }
}

EXPLICATION

Les tâches sont stockées en JSON : jsonEncode transforme la liste en
chaîne compacte conservée par SharedPreferences, et jsonDecode la
reconstruit au démarrage. initState lance la lecture une seule fois ;
comme _charger est asynchrone, on attend getInstance avec await. Chaque
modification est suivie d'une écriture, sinon rien n'est conservé.

POINTS DE VÉRIFICATION

- Ajouter puis rouvrir l'application retrouve les tâches.
- Au premier lancement, getString renvoie null : la liste reste vide.
- Le package shared_preferences doit figurer dans pubspec.yaml.

POUR ALLER PLUS LOIN

- Stocker des objets complets (titre et état fait) dans une liste de maps.
""",
        },
    },
    "Autre": {
        "exercises": {
            "Bonjour le monde": """SOLUTION

message = "Bonjour le monde !"
print(message)

nom = "Babi"
print("Bienvenue,", nom)
print("Aujourd'hui, je programme.")  # accents et apostrophes acceptés

EXPLICATION

print écrit le texte demandé sur la sortie standard puis passe à la
ligne : c'est le chemin le plus direct pour voir un résultat. Entre
guillemets, tout est pris littéralement, accents et apostrophes compris.
Hors des guillemets, message est un nom de variable : print(message)
affiche le contenu mémorisé, alors que print("message") afficherait le
mot lui-même. print("Bienvenue,", nom) reçoit deux arguments et les
relie par un espace, sans qu'on ait à concaténer à la main.

POINTS DE VÉRIFICATION

- Trois lignes de sortie, exactement dans l'ordre du fichier : le
  message, puis « Bienvenue, Babi », puis la dernière phrase.
- Écrire print(Bonjour) sans guillemets déclenche NameError, car Bonjour
  n'est déclaré nulle part.
- Un guillemet oublié provoque une erreur de syntaxe : Python s'arrête
  avant tout affichage.

POUR ALLER PLUS LOIN

- Lire une saisie avec nom = input("Votre nom : ") puis afficher le
  message personnalisé.
- Utiliser un gabarit du type f"Bonjour {nom} !" pour insérer une
  variable au milieu d'une phrase.
""",
            "Calculatrice": """SOLUTION

a = 17
b = 5

print("Somme :", a + b)        # 22
print("Différence :", a - b)   # 12
print("Produit :", a * b)      # 85
print("Division :", a / b)     # 3.4, un résultat réel
print("Quotient :", a // b)    # 3, la partie entière
print("Reste :", a % b)        # 2

EXPLICATION

Les quatre opérations ont quatre opérateurs : +, -, * et /. Le résultat
de / est toujours un décimal, même quand la division tombe juste, tandis
que // conserve seulement la partie entière du quotient et % donne le
reste. La vérification naturelle est quotient × b + reste = a, soit
3 × 5 + 2 = 17. Diviser par zéro lève une erreur d'exécution : il faut
tester b avant de calculer, comme le ferait une vraie calculatrice.

POINTS DE VÉRIFICATION

- 17 + 5 = 22, 17 − 5 = 12, 17 × 5 = 85, 17 ÷ 5 = 3.4.
- 17 // 5 = 3 et 17 % 5 = 2, et 3 × 5 + 2 retrouve bien 17.
- 0.1 + 0.2 affiche 0.30000000000000004 : les décimaux sont des
  approximations, on arrondit avec round(x, 1).

POUR ALLER PLUS LOIN

- Convertir la saisie avec a = float(input("Nombre : ")) pour calculer
  sur des valeurs saisies au clavier.
- Afficher deux décimales fixes grâce au gabarit f"{a / b:.2f}".
""",
            "Suite numérique": """SOLUTION

for n in range(1, 101, 5):
    print(n, end=" ")   # un espace au lieu d'un passage à la ligne
print()                 # saut de ligne final

EXPLICATION

range(début, fin, pas) produit une suite d'entiers : on part de 1, on
avance de 5 et on s'arrête avant 101, car la borne de fin n'est jamais
atteinte. Le dernier nombre affiché est donc 96, car 101 serait déjà
trop grand. Le paramètre end=" " remplace le passage à la ligne de print
par un simple espace, ce qui aligne la suite sur une seule ligne ; le
print() final replace le curseur pour la suite du programme.

POINTS DE VÉRIFICATION

- La suite commence par 1 puis 6, 11, 16 et se termine par 96.
- Vingt nombres sont affichés : 19 sauts de 5, plus le départ.
- Sans end=" ", chaque nombre occuperait sa propre ligne, ce qui reste
  correct mais change l'affichage attendu.

POUR ALLER PLUS LOIN

- Réécrire avec n = 1 puis while n <= 100 en faisant n += 5 : même
  résultat, logique explicite.
- Construire la liste list(range(1, 101, 5)) pour trier ou additionner
  les valeurs d'un coup.
""",
            "Inverser une chaîne": """SOLUTION

mot = "programmation"
inverse = ""

for lettre in mot:
    inverse = lettre + inverse   # la lettre passe devant

print(mot)                       # programmation
print(inverse)                   # noitammargorp
print(len(mot) == len(inverse))  # True

EXPLICATION

La boucle parcourt le mot de gauche à droite, mais chaque lettre est
placée devant la chaîne déjà construite : après « p », puis « rp », puis
« orp », l'ordre se retourne à chaque tour. C'est la concaténation qui
fabrique l'inversion, et non un tri. La variable inverse commence vide
pour que la première lettre ait quelque chose devant elle. La longueur
ne change jamais : on déplace les lettres, on n'en crée pas.

POINTS DE VÉRIFICATION

- « programmation » et « noitammargorp » font tous deux 13 lettres.
- Après le premier tour, inverse vaut « p » ; après le deuxième, « rp ».
- Pour une chaîne vide, la boucle ne s'exécute pas et inverse reste "".

POUR ALLER PLUS LOIN

- Utiliser la notation dédiée mot[::-1] dont le pas vaut −1 : une ligne
  au lieu d'une boucle.
- Tester un palindrome avec mot == inverse, puis enchaîner les mots
  proposés par l'utilisateur.
""",
            "Compteur": """SOLUTION

compteur = 0

for _ in range(1, 11):
    compteur += 1
    print("Clic n°", compteur)

print("Total :", compteur)   # 10

EXPLICATION

Le compteur doit être initialisé avant la boucle : sans valeur de départ,
la première addition ne pourrait pas se faire. L'instruction compteur += 1
ajoute 1 à la valeur mémorisée, ce qui revient à compteur = compteur + 1.
La boucle for est bornée : elle s'exécute dix fois puis s'arrête toute
seule, ce qui sécurise le décomptage. Le caractère _ remplace un indice
inutilisé : Python l'accepte et signifie qu'on ne lira jamais cette valeur.

POINTS DE VÉRIFICATION

- Dix lignes « Clic n° 1 » à « Clic n° 10 », puis « Total : 10 ».
- Le total reste 10 même si le print est déplacé hors de la boucle.
- Oublier compteur += 1 dans une boucle while provoque une boucle
  infinie : le programme ne rend plus la main.

POUR ALLER PLUS LOIN

- Envelopper le calcul dans une fonction def compter(n) puis appeler
  compter(5) pour réutiliser le compteur.
- Compter deux choses à la fois avec un dictionnaire du type
  {"clics": 0, "vues": 0}.
""",
            "Lecture de fichier": """SOLUTION

try:
    with open("notes.txt", encoding="utf-8") as fichier:
        for ligne in fichier:
            print(ligne.rstrip())
except FileNotFoundError:
    print("Fichier introuvable : notes.txt")

EXPLICATION

open ouvre le fichier et with garantit la fermeture, même si une erreur
survient au milieu : aucune ressource n'est oubliée. L'argument
encoding="utf-8" conserve les accents, que Windows pourrait sinon
casser. Parcourir le fichier avec for ligne in fichier lit une ligne à
la fois, très économique en mémoire, et rstrip() retire le retour à
ligne de fin pour éviter les lignes vides en sortie. Le bloc try attrape
l'erreur si le fichier manque et propose un message lisible.

POINTS DE VÉRIFICATION

- Avec un fichier de trois lignes, trois lignes sont affichées, sans
  ligne vide entre elles.
- Si notes.txt n'existe pas, on lit « Fichier introuvable : notes.txt »
  au lieu d'une trace d'erreur.
- Un fichier sans encoding utf-8 affiche des accents cassés.

POUR ALLER PLUS LOIN

- Utiliser fichier.read() pour tout lire d'un coup, ou readlines()
  pour obtenir une liste de lignes.
- Écrire à son tour avec open("sortie.txt", "w", encoding="utf-8") :
  même principe, mode d'écriture.
""",
            "Mini-projet": """SOLUTION

depenses = []


def ajouter(libelle, montant):
    depenses.append((libelle, montant))


def total():
    return sum(montant for _, montant in depenses)


while True:
    print("1) Ajouter  2) Afficher  3) Quitter")
    choix = input("Choix : ")
    if choix == "3":
        break
    elif choix == "1":
        ajouter(input("Libellé : "), float(input("Montant : ")))
    elif choix == "2":
        for libelle, montant in depenses:
            print("-", libelle, montant, "€")
        print("Total :", total(), "€")

EXPLICATION

Le programme est un carnet de dépenses : une liste de tuples garde les
données, deux fonctions isolent les traitements et la boucle while True
sert de menu. break interrompt la boucle proprement. float() convertit
la saisie texte en nombre pour que sum() puisse additionner ; le
découpage en fonctions rend le code testable séparément.

POINTS DE VÉRIFICATION

- Choix 3 sort du programme sans erreur ; une saisie inconnue
  réaffiche le menu sans planter.
- Une saisie « 2,5 » provoque ValueError : on remplace la virgule puis
  on convertit avec float(saisie.replace(",", ".")).
- Sur un carnet vide, « Afficher » donne « Total : 0 € », car sum d'une
  liste vide vaut 0.

POUR ALLER PLUS LOIN

- Enregistrer les dépenses avec json.dump(depenses, f) pour retrouver
  le carnet après redémarrage.
- Compter les entrées avec len(depenses) et filtrer par libellé.
""",
        },
    },
}
