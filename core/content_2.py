"""Fiches de contenu — lot 2 : Java, C++, C#."""
from __future__ import annotations

CONTENT = {
    "Java": {
        "lessons": {
            "Classes et objets": """OBJECTIFS
- définir une classe avec champs, méthodes et constructeur
- créer des objets et appeler leurs méthodes
- comprendre la différence entre static et instance

POINTS CLÉS
- constructeur : même nom que la classe, sans type de retour
- this.nom désigne le champ, new alloue l'objet et lance le constructeur
- static : membre partagé par toute la classe, accessible sans objet
- equals() compare le contenu, == compare seulement les références
- toString() est appelé par System.out.println(objet)

EXEMPLE
class Compte {
  private String titulaire;      // encapsulé : inaccessible dehors
  private double solde;
  Compte(String t) { titulaire = t; solde = 0; }
  void deposer(double m) { if (m > 0) solde += m; }
  public String toString() { return titulaire + " : " + solde; }
}
Compte c = new Compte("Babi");
c.deposer(50);
System.out.println(c);          // passe par toString()

EN PRATIQUE
Dans une application de gestion, chaque entité métier (client, produit,
commande) devient une classe. Les données restent privées et seules les
méthodes publiques les modifient, ce qui rend le code testable.

PIÈGES À ÉVITER
- écrire son constructeur : Java ne fournit plus celui par défaut
- laisser les champs publics : plus aucune validation n'est possible

À RETENIR
- une classe décrit un quoi, ses méthodes décrivent le comportement
- encapsulez les champs, exposez le comportement
""",
            "Héritage": """OBJECTIFS
- créer une hiérarchie de classes avec extends
- redéfinir une méthode avec @Override
- raisonner en polymorphisme

POINTS CLÉS
- extends réutilise champs et méthodes du parent
- super(...) appelle le constructeur du parent, en première ligne
- une méthode redéfinie est choisie selon l'objet réel, pas selon la variable
- classe finale : final empêche l'héritage
- une classe abstraite ne s'instancie pas
- protected est visible dans la classe et ses dérivées
- instanceof teste le type réel avant un éventuel cast

EXEMPLE
class Animal {
  void parle() { System.out.println("..."); }
}
class Chat extends Animal {
  @Override void parle() { System.out.println("miaou"); }
}
Animal a = new Chat();
a.parle();                              // miaou : décision à l'exécution
System.out.println(a instanceof Chat);  // true

EN PRATIQUE
L'héritage sert quand la relation est un vrai « est-un » : un Chat est un
Animal. Pour partager un comportement entre classes sans lien de parenté,
préférez une interface ou la composition.

PIÈGES À ÉVITER
- appeler super() trop tard : la première ligne doit le contenir
- redéfinir sans @Override : une faute de frappe passe inaperçue
- caster aveuglément une référence de base : vérifiez avec instanceof

À RETENIR
- hériter pour réutiliser, redéfinir pour spécialiser
- une interface suffit souvent : l'héritage imbriqué se paie cher
""",
            "Interfaces": """OBJECTIFS
- décrire un contrat avec interface
- implémenter plusieurs interfaces
- utiliser les méthodes par défaut

POINTS CLÉS
- interface : méthodes abstraites, sans corps, publiques par défaut
- classe : implements Nom, Nom2 (héritage simple + interfaces multiples)
- default : méthode fournie directement dans l'interface
- une interface peut contenir constantes et méthodes statiques
- Comparable et Serializable sont des interfaces de la bibliothèque standard

EXEMPLE
interface Serializable {
  String serialiser();
}
interface Temporaire {
  default void journal() { System.out.println("événement enregistré"); }
}
class Produit implements Serializable, Temporaire {
  public String serialiser() { return "{...}"; }
}
Serializable s = new Produit();
s.serialiser();                    // la classe impose le comportement

EN PRATIQUE
Les grandes bibliothèques s'articulent presque toutes autour
d'interfaces : stockage, journalisation, persistance. Programmer contre
une interface permet de remplacer une implémentation sans y toucher.

PIÈGES À ÉVITER
- écrire une méthode sans default ni corps : la classe devra l'implémenter
- oublier public : les méthodes d'interface sont publiques d'office
- conserver des champs modifiables dans une interface

À RETENIR
- l'interface décrit un QUOI, la classe abstraite un COMMENT commun
- plusieurs interfaces oui, plusieurs classes héritées non
""",
            "Collections": """OBJECTIFS
- choisir entre List, Set et Map
- parcourir et modifier des collections en sécurité
- connaître les implémentations courantes
- trier et rechercher dans une collection

POINTS CLÉS
- List : ordonné, doublons autorisés (ArrayList, LinkedList)
- Set : sans doublons (HashSet, TreeSet)
- Map : association clé vers valeur (HashMap, TreeMap)
- itérateur : for (Type x : collection)
- ArrayList accède vite par index, LinkedList insère vite au milieu
- List.of(...) crée une liste immuable, idéale en lecture seule

EXEMPLE
List<String> noms = new ArrayList<>();
noms.add("Babi");
noms.add("Alice");
noms.remove("Alice");
System.out.println(noms.size());         // 1
System.out.println(noms.contains("Babi"));  // true
noms.stream().filter(s -> s.startsWith("B"))
     .forEach(System.out::println);

EN PRATIQUE
Toute application de gestion manipule des listes de clients, des ensembles
de permissions ou des dictionnaires de traduction. Choisir la bonne
structure évite les boucles de recherche inutiles et les bugs de doublons.

PIÈGES À ÉVITER
- modifier une collection pendant le for-each : ConcurrentModificationException
- appeler contains sur une grande List : préférez un HashSet
- se tromper de généricité : Map exige deux paramètres, Map<K, V>

À RETENIR
- l'ordre et les doublons d'abord, la structure ensuite
- programmer contre l'interface laisse le choix de l'implémentation
""",
            "Génériques": """OBJECTIFS
- paramétrer les classes et méthodes d'un type
- éviter les casts manuels et les erreurs à l'exécution
- poser des contraintes avec extends
- écrire un utilitaire générique réutilisable

POINTS CLÉS
- class Boîte<T> { T valeur; }
- méthode : static <T> T premier(List<T> l)
- contrainte : <T extends Comparable<T>> impose un type comparable
- l'inférence déduit T à l'appel : new Boîte<>() suffit
- plusieurs paramètres : Map<K, V>, Paire<A, B>
- les génériques sont élagués à l'exécution : pas de new T()

EXEMPLE
class Paire<A, B> {
  A premier;
  B second;
}
Paire<String, Integer> p = new Paire<>();
p.premier = "Babi";
p.second = 42;

static <T extends Comparable<T>> T minimum(List<T> liste) {
  T min = liste.get(0);
  for (T x : liste) if (x.compareTo(min) < 0) min = x;
  return min;
}

EN PRATIQUE
Les génériques apparaissent partout : List<String>, Map<String, Integer>,
Optional<User>. Le compilateur vérifie que la bonne donnée circule au
bon endroit et vous évite une ClassCastException en production.

PIÈGES À ÉVITER
- caster une List<Object> en List<String> : refusé à l'exécution
- écrire new ArrayList() sans type : préférez le diamant new ArrayList<>()
- créer un tableau de type générique : new T[] est refusé

À RETENIR
- le type erroné est signalé à la compilation, pas à l'exécution
- contraindre avec extends rend l'utilitaire réutilisable partout
""",
            "Entrées / sorties": """OBJECTIFS
- lire et écrire des fichiers avec les flux
- utiliser BufferedReader / PrintWriter
- sérialiser des objets en texte
- distinguer java.io et java.nio

POINTS CLÉS
- try-with-resources ferme automatiquement les ressources
- BufferedReader.readLine() lit ligne à ligne et renvoie null à la fin
- Paths / Files (java.nio) simplifient la lecture complète
- encodage : StandardCharsets.UTF_8, sinon le système impose le sien
- Files.write(path, lignes) écrit une liste de chaînes d'un seul coup
- une IOException oblige à traiter l'erreur

EXEMPLE
Path p = Paths.get("n.txt");
Files.write(p, List.of("ligne 1", "ligne 2"), StandardCharsets.UTF_8);
try (BufferedReader br =
       Files.newBufferedReader(p, StandardCharsets.UTF_8)) {
  String ligne;
  while ((ligne = br.readLine()) != null) System.out.println(ligne);
}

EN PRATIQUE
Lecture de fichiers de configuration, export de rapports, import de
données tabulées : tout passe par ces flux. Le bloc try-with-resources
garantit la fermeture du fichier même si une exception survient au
milieu du traitement.

PIÈGES À ÉVITER
- ouvrir un flux sans le fermer : fuite de descripteurs système
- lire un fichier UTF-8 avec l'encodage par défaut : caractères cassés
- croire qu'une chaîne vide marque la fin : seul null la signale

À RETENIR
- toujours try-with-resources pour un flux
- indiquez l'encodage, ne le laissez jamais deviner
""",
            "Exceptions": """OBJECTIFS
- attraper et relancer des exceptions
- distinguer vérifiées et non vérifiées
- créer ses propres exceptions métier
- choisir le bon niveau de catch

POINTS CLÉS
- vérifiées : IOException, Exception exigent un catch obligatoire
- non vérifiées : NullPointerException, RuntimeException
- try / catch / finally, throw pour lever
- class MonErreur extends Exception {...}
- multi-catch : catch (IOException | SQLException e)
- Error signale une défaillance grave de la JVM, on ne la rattrape pas
- chaîner (message, cause) conserve l'origine du problème

EXEMPLE
try {
  int n = Integer.parseInt(saisie);
  if (n < 0) throw new IllegalArgumentException("negatif");
} catch (NumberFormatException e) {
  System.out.println("nombre invalide : " + saisie);
} finally {
  System.out.println("fin du traitement");
}

EN PRATIQUE
Une exception métier (SoldeInsuffisant, StockVide) transporte une
information utile jusqu'à la couche qui sait quoi en faire : l'interface
utilisateur affiche un message clair, le journal garde la trace pour le
dépannage.

PIÈGES À ÉVITER
- vider le catch silencieusement : prévoyez au moins un log
- attraper Exception trop large : les vraies erreurs passent inaperçues
- relancer une exception sans sa cause : le diagnostic devient impossible

À RETENIR
- lever pour signaler, attraper pour traiter
- finally s'exécute toujours, même après un return
""",
        },
        "exercises": {
            "Affichage console": """ÉNONCÉ
- écrire un programme Java avec main qui affiche un message d'accueil puis la version du runtime utilisé.

ÉTAPES
1. créer la classe public class Main
2. écrire public static void main(String[] args)
3. afficher le message avec System.out.println
4. afficher System.getProperty("java.version")
5. compiler avec javac Main.java, puis exécuter avec java Main

RÉSULTAT ATTENDU
- la première ligne affiche Bonjour Java !
- la seconde ligne affiche la version, par exemple 21.0.4
- aucune erreur ni avertissement à la compilation

POUR TESTER
- lancez le programme deux fois : le message doit être identique
- remplacez la propriété par java.home et vérifiez l'affichage d'un chemin
- cas limite : supprimez le println et constatez qu'aucune sortie n'apparaît

INDICE
- le nom du fichier doit être Main.java pour public class Main.
- placez-vous dans le dossier du fichier avant de lancer javac depuis le terminal.
""",
            "Calculatrice": """ÉNONCÉ
- implémenter une classe Calculatrice avec les quatre opérations et un menu console qui relit le choix de l'utilisateur.

ÉTAPES
1. méthodes additionner, soustraire, multiplier, diviser(double, double)
2. gérer la division par zéro avec une exception ou un message
3. lire le choix avec Scanner(System.in)
4. répéter tant que l'utilisateur ne choisit pas « q »
5. afficher chaque résultat avec le libellé de l'opération

RÉSULTAT ATTENDU
- choix 1 puis 6 puis 2 affiche 3.0
- la division par 0 affiche une erreur et le menu revient
- la saisie « q » termine le programme sans erreur

POUR TESTER
- essayez 7 * 6, 10 - 4, 3 / 0 puis une lettre à la place d'un nombre
- vérifiez que le menu réapparaît après chaque calcul
- cas limite : saisissez deux fois de suite la même opération, le résultat doit rester stable

INDICE
- Scanner.nextLine() puis Integer.parseInt évite l'oublie de saut de ligne.
""",
            "Compte bancaire": """ÉNONCÉ
- modéliser un compte bancaire (titulaire, solde) avec dépôt, retrait et virement, en interdisant un solde négatif.

ÉTAPES
1. classe CompteBancaire avec un solde privé
2. deposer(double) et retirer(double) qui vérifient le solde
3. lever IllegalArgumentException si le retrait est impossible
4. méthode toString() pour l'affichage
5. ajouter un virement vers un second compte

RÉSULTAT ATTENDU
- déposer 100 puis retirer 30 donne un solde de 70
- retirer 500 déclenche une exception avec un message clair
- un virement de 20 débite le premier compte et crédite le second

POUR TESTER
- essayez un dépôt négatif et un retrait exactement égal au solde
- créez deux comptes : la somme des soldes doit se conserver après un virement
- affichez le compte : toString doit montrer titulaire et solde

INDICE
- garder solde en double centimes (ou long) pour éviter les arrondis.
- testez aussi un retrait sur un compte jamais débité auparavant.
""",
            "Gestion de notes": """ÉNONCÉ
- pour une classe d'élèves (nom et notes), calculer la moyenne de chaque élève et sa mention, puis la moyenne de la classe.

ÉTAPES
1. classe Élève avec List<Double> notes
2. méthode moyenne() et mention() (>= 16 Excellent, >= 10 Admis)
3. parcourir la classe et afficher un tableau aligné
4. calculer la moyenne générale
5. afficher l'élève qui obtient la meilleure moyenne

RÉSULTAT ATTENDU
- Alice 14.33 (Admis), Bob 16.5 (Excellent)
- la moyenne de la classe est 15.4
- l'élève en tête est affiché en dernier

POUR TESTER
- ajoutez une note de 20 puis une note de 0 : les deux moyennes doivent bouger
- testez un élève sans aucune note : le programme doit signaler le cas sans planter
- cas limite exact : la mention doit basculer à 10 et non à 9.99

INDICE
- DoubleStream de la liste : notes.stream().mapToDouble(...).average()
- la moyenne de la classe se calcule à partir des moyennes individuelles.
""",
            "Lire un CSV": """ÉNONCÉ
- lire un fichier CSV (nom;prénom;ville) et transformer chaque ligne en objet, en ignorant la ligne d'en-tête.

ÉTAPES
1. ouvrir avec BufferedReader en UTF-8
2. lire la première ligne (en-tête) et l'ignorer
3. découper chaque ligne avec split(";")
4. construire un objet et l'afficher ; signaler les lignes mal formées
5. compter les lignes traitées et les lignes rejetées

RÉSULTAT ATTENDU
- un fichier de 3 lignes (en-tête comprise) produit 2 objets affichés
- une ligne avec une colonne manquante génère un message avec son numéro
- le décompte final sépare lignes traitées et lignes rejetées

POUR TESTER
- retirez une colonne : l'erreur doit citer le numéro de la ligne fautive
- ajoutez une ligne vide : elle ne doit pas faire planter le programme
- mettez un accent dans un prénom et ouvrez en UTF-8 : aucun caractère cassé

INDICE
- ne pas fermer le BufferedReader dans la boucle : try-with-resources autour.
""",
            "Compteur de mots": """ÉNONCÉ
- compter les occurrences de chaque mot d'un texte avec HashMap et afficher les trois plus fréquents.

ÉTAPES
1. découper le texte en mots avec un découpage sur les caractères non alphabétiques
2. mettre en minuscules et ignorer les mots de moins de 3 lettres
3. compter dans HashMap<String, Integer> avec merge ou getOrDefault
4. trier par valeur décroissante et afficher le top 3
5. afficher aussi le nombre de mots distincts

RÉSULTAT ATTENDU
- pour « le chat le chien le » : le:3, chat:1, chien:1
- le top 3 commence par le qui totalise 3 occurrences
- le nombre de mots distincts est 3

POUR TESTER
- répétez un mot en majuscules : il doit fusionner avec la forme en minuscules
- testez un texte vide : aucun résultat, aucune erreur
- vérifiez que la somme des comptes égale le nombre de mots retenus

INDICE
- map.merge(mot, 1, Integer::sum) fait l'incrémentation en une ligne.
- un tri des entrées de la map sur la valeur donne le top 3 directement.
""",
            "Tri personnalisé": """ÉNONCÉ
- trier une liste d'objets Personne par nom puis par âge avec Comparator, puis inverser complètement l'ordre.

ÉTAPES
1. implémenter Comparable<Personne> (tri par nom)
2. construire Comparator.comparing(Personne::getNom)
3. enchaîner thenComparing pour le second critère
4. inverser avec Collections.reverseOrder()
5. afficher la liste avant et après chaque tri

RÉSULTAT ATTENDU
- départ : Alice 30, Bob 25, Alice 22
- tri nom puis âge : Alice 22, Alice 30, Bob 25
- ordre inversé : Bob 25, Alice 30, Alice 22

POUR TESTER
- ajoutez une personne portant le même nom : l'âge doit la départager
- vérifiez que la liste d'origine est bien modifiée sur place
- testez une liste vide et une liste d'un seul élément : aucun plantage

INDICE
- comparator.thenComparing(...).reversed() inverse tout le comparateur.
- comparez les noms avec compareTo, jamais avec le double égal des objets.
- préférez un ArrayList en paramètre plutôt qu'un tableau brut.
""",
        },
    },
    "C++": {
        "lessons": {
            "Types et variables": """OBJECTIFS
- maîtriser les types primitifs et la déclaration
- utiliser const, auto et le namespace std
- comprendre la portée des variables

POINTS CLÉS
- int, float, double, char, bool, std::string
- auto déduit le type à la déclaration
- const empêche la modification ; constexpr évalue à la compilation
- #include <string>, using namespace std; (à réserver aux exemples)
- les entiers ont une taille fixe : <cstdint> fournit int32_t, int64_t
- une variable déclarée dans un bloc n'existe plus hors de ce bloc
- une variable non initialisée contient n'importe quoi : initialisez-la

EXEMPLE
#include <string>
int main() {
  const int AGE = 30;
  auto prix = 9.99;            // double, déduit
  std::string nom = "Babi";
  bool actif = true;
  {
    int doublon = 1;            // portée limitée à ce bloc
  }
  return 0;
}

EN PRATIQUE
C++ se pratique là où la maîtrise de la mémoire compte : périphériques,
moteurs de jeu, outils métiers. Des types précis dès le départ évitent
les conversions silencieuses et les pertes de précision.

PIÈGES À ÉVITER
- comparer deux double avec == : utilisez plutôt une tolérance
- oublier le point flottant : 5 / 2 vaut 2, écrivez 5.0 / 2
- using namespace std; dans un en-tête : risque de collision de noms

À RETENIR
- initialisez à la déclaration, marquez const ce qui ne change pas
- auto devine le type, mais affichez-le quand la lecture en souffre
""",
            "Conditions et boucles": """OBJECTIFS
- écrire des conditions if / switch et des boucles for / while
- parcourir un tableau avec les boucles à plage
- contrôler le flux avec break / continue

POINTS CLÉS
- switch sur entier ou enum, break obligatoire (sinon chute)
- boucle à plage : for (auto x : vecteur)
- do…while teste sa condition à la fin
- opérateurs && || !
- une condition se lit sans double égal : if (x) signifie x non nul
- ++i est légèrement préférable à i++ dans une boucle
- if constexpr élimine une branche à la compilation

EXEMPLE
for (int i = 0; i < 5; ++i) {
  if (i == 3) continue;
  std::cout << i << " ";        // 0 1 2 4
}
switch (choix) {
  case 1: traiter(); break;
  default: std::cout << "inconnu"; break;
}
int n = 0;
do { ++n; } while (n < 3);      // tourne au moins une fois

EN PRATIQUE
Menus console, lecture d'événements et boucles de rendu utilisent ces
constructions au quotidien. Le choix entre for, while et do…while dépend
de ce que l'on sait déjà avant d'entrer dans la boucle.

PIÈGES À ÉVITER
- oublier le break : le switch continue dans le cas suivant
- boucle non bornée : initialisez le compteur et faites-le progresser
- comparer des flottants à == pour sortir d'une boucle

À RETENIR
- chaque boucle doit afficher sa sortie au premier coup d'œil
- la boucle à plage est la façon la plus sûre de parcourir un conteneur
""",
            "Fonctions": """OBJECTIFS
- définir des fonctions avec paramètres et retours
- passer par valeur, référence ou pointeur
- surcharger et donner une valeur par défaut

POINTS CLÉS
- (int a, int b) copie les valeurs ; (int& a) modifie l'appelant
- passage par const référence pour les objets lourds : const std::string&
- surcharge : même nom, signature différente
- valeur par défaut uniquement à la déclaration
- retour : T pour copier, T& pour accéder, const T& pour exposer sans copier

EXEMPLE
int max3(int a, int b, int c = 0) {
  int m = a > b ? a : b;
  return m > c ? m : c;
}
void doubler(int& x) { x *= 2; }
int v = 21;
doubler(v);                       // v vaut maintenant 42
const std::string& plusLong(const std::string& a,
                            const std::string& b) {
  return a.size() >= b.size() ? a : b;
}

EN PRATIQUE
Un projet C++ sépare souvent la déclaration (.h) de la définition
(.cpp). Passer une chaîne ou un conteneur en const référence évite une
copie inutile, une différence nette dès que les objets grossissent.

PIÈGES À ÉVITER
- donner la valeur par défaut dans les deux fichiers : double définition
- retourner une référence sur une variable locale : mémoire invalide
- passer un std::string par valeur dans une boucle serrée

À RETENIR
- par valeur pour les petits types, par const référence pour les gros
- une fonction qui ne modifie rien le prouve avec const
""",
            "Pointeurs et mémoire": """OBJECTIFS
- comprendre l'adresse et le déréférencement
- allouer et libérer la mémoire dynamique
- éviter les fuites et les accès invalides

POINTS CLÉS
- T* p = &v ; *p accède à la valeur, &v donne l'adresse
- new T alloue, delete libère ; new[] et delete[] pour les tableaux
- la portée RAII (objets) évite presque tout new/delete manuel
- jamais delete deux fois, jamais utiliser un pointeur après delete
- nullptr remplace le 0 historique pour « aucun pointeur »
- -> accède à un membre quand on tient un pointeur sur objet

EXEMPLE
int* n = new int(42);
std::cout << *n << std::endl;    // 42
delete n;
n = nullptr;                     // l'adresse libérée n'est plus utilisée
std::vector<int> v = {1, 2, 3};  // libéré automatiquement à la fin
std::cout << v.front();          // 1

EN PRATIQUE
Aujourd'hui on écrit le moins possible de new et de delete : les
conteneurs et les pointeurs intelligents (std::unique_ptr) gèrent la
durée de vie à votre place et suppriment les fuites classiques.

PIÈGES À ÉVITER
- utiliser *n après delete : comportement indéfini
- new[] avec delete simple : les autres destructeurs ne tournent pas
- copier un pointeur brut sans transférer la charge de le libérer

À RETENIR
- fuite = allocation jamais libérée : valgrind la détecte
- RAII d'abord, pointeurs bruts seulement si nécessaire
""",
            "Classes et objets": """OBJECTIFS
- définir une classe (champs privés, méthodes publiques)
- écrire constructeur, destructeur, surcharge d'opérateurs
- appliquer l'encapsulation

POINTS CLÉS
- private par défaut dans class, public dans struct
- constructeur : Rectangle(double l, double h);
- const sur une méthode : elle ne modifie pas l'objet
- règle des 3 ou 5 si la classe gère une ressource
- la liste d'initialisation construit les champs avant le corps
- friend ouvre un accès ponctuel aux membres privés
- une méthode statique n'a pas de this et voit l'état partagé

EXEMPLE
class Compte {
public:
  Compte(double s = 0) : solde(s) {}
  void deposer(double m) { if (m > 0) solde += m; }
  double getSolde() const { return solde; }
private:
  double solde;
};
Compte c(100);
c.deposer(50);
std::cout << c.getSolde();       // 150

EN PRATIQUE
Une classe C++ décrit un objet avec un comportement précis : un fichier
ouvert, une connexion réseau, un compte. L'encapsulation interdit
d'altérer l'état par accident et centralise les vérifications.

PIÈGES À ÉVITER
- oublier le const d'un accesseur : impossible sur un objet constant
- initialiser les champs dans le corps plutôt que dans la liste dédiée
- oublier explicit : Compte c = 100; compile pourtant

À RETENIR
- private pour l'état, public pour le comportement
- const sur chaque méthode qui ne modifie pas l'objet
""",
            "Héritage et virtuel": """OBJECTIFS
- créer des classes dérivées avec public
- redéfinir des méthodes et comprendre le polymorphisme
- utiliser le destructeur virtuel

POINTS CLÉS
- class D : public B { ... };
- virtual = redéfinissable ; override marque la redéfinition
- sans virtual, l'appel dépend du type de la référence ou du pointeur
- destructeur virtuel obligatoire si l'objet part via un pointeur de base
- = 0 rend la méthode pure : la classe devient abstraite
- protected est accessible à la classe et à ses dérivées

EXEMPLE
class Forme {
public:
  virtual double aire() const = 0;   // abstraite
  virtual ~Forme() = default;
};
class Cercle : public Forme {
public:
  Cercle(double rr) : r(rr) {}
  double aire() const override { return 3.14159 * r * r; }
private:
  double r;
};

EN PRATIQUE
On conserve des pointeurs sur Forme pour traiter tous les dessins de la
même façon. Le choix de la méthode se fait à l'exécution : on ajoute une
forme sans modifier le code appelant.

PIÈGES À ÉVITER
- appeler une méthode non virtuelle via un pointeur de base : le corps de la base s'exécute
- oublier ~Forme() = default : suppression incomplète d'un objet dérivé
- masquer une méthode au lieu de la redéfinir : le override manqué passe inaperçu

À RETENIR
- virtual pour le comportement polymorphe, override pour la traçabilité
- une méthode pure rend la classe abstraite, non instanciable
""",
            "STL": """OBJECTIFS
- utiliser vector, map, string et algorithmes
- parcourir avec itérateurs et lambdas
- choisir la conteneur adaptée au besoin

POINTS CLÉS
- std::vector : tableau dynamique, push_back, accès indexé direct
- std::map : triée clé vers valeur ; std::unordered_map : plus rapide
- itérateurs : begin() / end(), l'algorithme s'arrête en [début, fin)
- algorithmes : sort, find_if, count_if avec lambdas
- std::string fournit tout ce que fait vector et gère le texte
- erase-remove : v.erase(std::remove_if(d, f), v.end())

EXEMPLE
#include <vector>
#include <algorithm>
std::vector<int> v = {3, 1, 2};
std::sort(v.begin(), v.end());   // 1 2 3
auto it = std::find_if(v.begin(), v.end(),
                       [](int x) { return x > 1; });
int total = 0;
for (int x : v) total += x;      // 6
v.push_back(4);

EN PRATIQUE
Presque tout un programme C++ manipule des conteneurs standard. vector
par défaut, unordered_map pour une table de hachage et deque pour des
insertions en tête évitent de réinventer des structures maison.

PIÈGES À ÉVITER
- itérer et effacer en même temps : préférez l'idiome erase-remove
- comparer size() à un int : le compilateur avertit sur le signe
- oublier <algorithm> : std::sort ne compile pas

À RETENIR
- vector pour l'ajout en fin fréquent ; deque pour insérer devant
- un algorithme standard est testé et souvent plus rapide qu'une boucle maison
""",
            "Templates": """OBJECTIFS
- écrire des fonctions et des classes génériques
- comprendre l'instanciation à la compilation
- poser des contraintes avec les concepts (C++20)

POINTS CLÉS
- template <typename T> T max(T a, T b)
- le compilateur génère un code distinct par type utilisé
- template <class T> class Boîte { T v; };
- concepts (C++20) : template <typename T> requires std::integral T
- la spécialisation traite un cas particulier
- le nom des paramètres (T, U, Value) sert à la lisibilité

EXEMPLE
template <typename T>
T plusGrand(T a, T b) { return a > b ? a : b; }
int x = plusGrand(3, 7);          // instancié en int
double d = plusGrand(2.5, 1.5);   // instancié en double

template <typename T>
class Boîte {
public:
  T valeur;
};

EN PRATIQUE
Les bibliothèques standard et le code de performance vivent dans les
templates : vector<int> et vector<double> partagent la même source mais
produisent deux fonctions distinctes, sans coût à l'exécution.

PIÈGES À ÉVITER
- placer un template dans un .cpp séparé : erreur à l'instanciation
- mélanger int et double dans un même appel : le déducteur refuse
- oublier typename devant un type dépendant : refus du compilateur

À RETENIR
- un code template vit souvent dans l'en-tête (instanciation visible)
- un concept rend l'erreur de template compréhensible
""",
        },
        "exercises": {
            "Bonjour C++": """ÉNONCÉ
- compiler et exécuter un premier programme qui affiche un message d'accueil puis la date du jour.

ÉTAPES
1. écrire bonjour.cpp avec #include <iostream>
2. afficher via std::cout << ... << std::endl
3. compiler : g++ -std=c++17 -Wall bonjour.cpp -o bonjour
4. exécuter : ./bonjour (bonjour.exe sous Windows)
5. afficher la date avec <chrono> ou <ctime>
6. vérifier le code de retour du programme

RÉSULTAT ATTENDU
- la première ligne affiche Bonjour C++ !
- la seconde ligne affiche la date du jour sous forme lisible
- la compilation ne produit aucun avertissement avec -Wall

POUR TESTER
- retirez un point-virgule : le compilateur doit localiser l'erreur exacte
- relancez le programme à deux moments différents : la date change
- cas limite : testez le code de retour après une erreur de syntaxe

INDICE
- le retour 0 de main signale le succès du programme.
- affichez la date avec std::time puis std::ctime pour rester simple.
""",
            "Calculatrice": """ÉNONCÉ
- surcharger les opérateurs + - * / dans une classe Nombre pour écrire naturellement a + b.

ÉTAPES
1. classe Nombre avec un champ double valeur
2. friend Nombre operator+(const Nombre&, const Nombre&)
3. surcharger les quatre opérateurs arithmétiques
4. afficher avec operator<<
5. prévenir la division par zéro (valeur nulle ou exception)

RÉSULTAT ATTENDU
- Nombre(3) + Nombre(4) donne 7
- Nombre(6) * Nombre(7) donne 42
- std::cout << Nombre(5) affiche 5 sans code supplémentaire

POUR TESTER
- vérifiez que a + b et b + a donnent le même résultat
- composez les opérations : (Nombre(1) + Nombre(2)) * Nombre(3) donne 9
- cas limite : la division par zéro doit être refusée de façon annoncée

INDICE
- les opérateurs binaires en free function (friend) gardent l'ordre des opérandes.
- l'opérateur d'affichage prend toujours un std::ostream& en premier paramètre.
- conservez le dernier résultat dans un champ pour enchaîner les calculs.
""",
            "Tableau trié": """ÉNONCÉ
- trier un tableau d'entiers par tri à bulles, puis comparer le nombre d'échanges avec std::sort.

ÉTAPES
1. écrire la boucle double : pour i, puis pour j de 0 à n-i-1
2. échanger tab[j] et tab[j+1] si le premier est le plus grand
3. compter chaque échange réalisé
4. trier une seconde copie avec std::sort
5. afficher les tableaux et les deux compteurs

RÉSULTAT ATTENDU
- au départ : 5, 2, 8, 1
- à l'arrivée : 1, 2, 5, 8 pour les deux méthodes
- le compteur du tri maison est supérieur ou égal à celui de std::sort

POUR TESTER
- testez un tableau déjà trié : les échanges doivent être nuls
- testez l'ordre inverse et un tableau d'un seul élément
- comparez les deux tableaux élément par élément : ils doivent coïncider

INDICE
- std::swap(a, b) évite d'écrire l'échange manuellement.
- retenez le nombre d'échanges dans un entier plutôt que dans un booléen.
- commencez par 4 éléments : la double boucle reste facile à déboguer.
""",
            "Compteur de mots": """ÉNONCÉ
- lire un texte au clavier et compter chaque mot avec std::map<std::string, int>, puis afficher les mots triés.

ÉTAPES
1. lire une ligne complète avec std::getline
2. construire un stringstream et en extraire les mots
3. faire compteur[mot]++ dans la map
4. afficher mot : compte (la map est déjà triée)
5. afficher le nombre total de mots lus

RÉSULTAT ATTENDU
- pour « baba le le » : baba:1 puis le:2, par ordre alphabétique
- le total de mots lus vaut 3
- le nombre de mots distincts vaut 2

POUR TESTER
- saisissez les mêmes mots en majuscules après les avoir normalisés : les comptes doivent se cumuler
- laissez la ligne vide : aucun mot affiché, aucune erreur
- vérifiez que la somme des comptes égale le total de mots lus

INDICE
- passez tout en minuscules avant de compter pour fusionner les doublons.
- un std::map trie déjà les clés : aucun tri supplémentaire pour afficher.
- extraire les mots avec un stringstream reste plus lisible qu'un index manuel.
""",
            "Classe Rectangle": """ÉNONCÉ
- écrire une classe Rectangle (largeur, hauteur) avec aire, périmètre, comparaison et affichage.

ÉTAPES
1. constructeur validant des dimensions strictement positives (throw sinon)
2. méthodes aire() et perimetre()
3. surcharge de operator== et comparaison avec un autre rectangle
4. operator<< pour std::cout
5. ajouter un redimensionnement qui passe par la même validation

RÉSULTAT ATTENDU
- Rectangle(4, 5) donne une aire de 20 et un périmètre de 18
- un rectangle 4 × 5 est plus grand qu'un rectangle 3 × 3
- une dimension négative déclenche une exception à la construction

POUR TESTER
- testez Rectangle(0, 5) : la validation doit refuser la création
- affichez deux rectangles : largeur et hauteur doivent apparaître
- cas limite : comparez un rectangle avec lui-même, l'égalité est vraie

INDICE
- les accesseurs sont const : double aire() const;
- validez dans le constructeur avant même d'affecter les champs.
""",
            "Fibonacci récursif": """ÉNONCÉ
- écrire fib(n) récursivement, mesurer son coût, puis écrire la version itérative et comparer les temps.

ÉTAPES
1. poser les cas de base : fib(0) = 0 et fib(1) = 1
2. écrire la recursion fib(n) = fib(n-1) + fib(n-2)
3. écrire la version itérative avec deux variables d'appui
4. mesurer les temps avec chrono pour n = 30, 35, 40
5. afficher les deux résultats et les deux durées

RÉSULTAT ATTENDU
- fib(10) vaut 55 dans les deux versions
- les deux versions donnent exactement le même résultat pour chaque n
- la version récursive ralentit nettement au-delà de 35, l'itérative reste instantanée

POUR TESTER
- comparez les deux versions pour n de 0 à 20 : les valeurs doivent coïncider
- chronométrez n = 40 : l'écart de temps doit sauter aux yeux
- cas limite : n = 0 et n = 1 doivent répondre sans débordement

INDICE
- la récursion naîve recalcule tout : la mémoïsation résout le problème.
""",
            "Devinette console": """ÉNONCÉ
- trouver un nombre choisi au hasard entre 1 et 100 en sept essais au maximum, avec des indices et un taux de réussite affiché en fin de partie.

ÉTAPES
1. générer la cible : rand() % 100 + 1 (srand(time(0)) en tête)
2. lire les essais avec std::cin
3. afficher « plus grand » ou « plus petit » après chaque essai
4. annoncer la victoire ou la défaite, puis le taux de réussite
5. proposer de rejouer tant que l'utilisateur le souhaite

RÉSULTAT ATTENDU
- cible 42 : essais 50, 30, 45, 41, 42 donnent « trouvé en 5 essais »
- le taux s'affiche en pourcentage, par exemple 71 %
- sept essais ratés : défaite avec affichage de la cible

POUR TESTER
- relancez la partie : la cible doit changer d'une partie à l'autre
- saisissez 0, 101 puis une lettre : chaque saisie doit être refusée proprement
- cas limite : trouver en un seul essai doit afficher 100 %

INDICE
- une boucle for de sept itérations gère le décompte d'essais proprement.
""",
        },
    },
    "C#": {
        "lessons": {
            "Types et variables": """OBJECTIFS
- déclarer avec var et les types forts
- utiliser les types nullable et les chaînes interpolées
- distinguer valeur et référence
- choisir le type numérique adapté au besoin

POINTS CLÉS
- int, double, string, bool ; var déduit à la compilation
- int? : nullable ; x ?? valeur de défaut
- chaînes verbatim @ "chemin\\file" et interpolée $"{}"
- struct = valeur, class = référence
- decimal pour l'argent : précision décimale exacte
- string est immuable : chaque opération crée une nouvelle instance
- const pour les constantes de compilation, readonly au constructeur

EXEMPLE
int age = 30;
int? sansAge = null;
string msg = $"Babi a {age} ans";
double? note = sansAge ?? 0;
bool estVrai = true;
Console.WriteLine(msg);
Console.WriteLine($"{age} en hexa : {age:X}");

EN PRATIQUE
Les applications .NET manipulent partout des chaînes (noms, adresses,
chemins de fichiers) et des nombres (ages, prix, compteurs). var allège
la déclaration quand le type est évident, mais le type explicite reste
préférable quand la lecture du code en dépend.

PIÈGES À ÉVITER
- utiliser double pour de l'argent : préférez decimal
- oublier le ?? sur un nullable : NullReferenceException
- croire que var rend le code non typé : le type reste fixe à la compilation

À RETENIR
- le type suit la valeur, var ne change rien à cela
- string est immuable : chaque opération crée une nouvelle instance
""",
            "Conditions et boucles": """OBJECTIFS
- écrire if et switch, y compris les switch expressions
- boucler avec for, foreach, while
- utiliser les patrons de comparaison modernes

POINTS CLÉS
- switch expression : var r = x switch { 1 => "un", _ => "autre" };
- foreach (var n in liste) pour parcourir une collection
- is / or / and dans les patrons
- break / continue comme en C
- une condition se lit sans double égal : if (x) signifie x vrai
- for quand le compte est connu, foreach pour parcourir
- la switch expression doit couvrir tous les cas possibles

EXEMPLE
var jour = (int)DateTime.Now.DayOfWeek;
var type = jour switch {
  0 or 6 => "week-end",
  _ => "semaine"
};
for (int i = 0; i < 3; i++) Console.Write(i + " ");
foreach (var n in new[] { 4, 5 }) Console.Write(n + " ");

EN PRATIQUE
Menus d'application, validation de formulaires et traitement d'événements
reposent sur ces structures. La switch expression remplace avantageusement
une pile de if/else quand les cas sont simples et que la lecture doit
rester immédiate.

PIÈGES À ÉVITER
- oublier le cas _ : la switch expression doit être exhaustive
- oublier break dans un switch classique : le code chute dans le cas suivant
- modifier une collection pendant un foreach : exception à l'exécution

À RETENIR
- privilégiez foreach pour parcourir et for pour compter
- la switch expression doit être exhaustive : pensez au cas _
""",
            "Fonctions": """OBJECTIFS
- définir des méthodes avec paramètres nommés et valeurs par défaut
- utiliser out, ref et les retours multiples
- écrire des fonctions expression-bodied

POINTS CLÉS
- out : la méthode remplit le paramètre (TryParse)
- ref : passé à l'appel et renvoyé modifié
- (bool ok, string err) comme tuple de retour
- défauts : void f(int a, int b = 10)
- params accepte un nombre variable d'arguments
- les paramètres nommés rendent l'appel lisible : f(b: 3)
- expression-bodied : int Carre(int x) => x * x;

EXEMPLE
bool ok = int.TryParse(saisie, out int n);
if (ok) Console.WriteLine(n * 2);

(int min, int max) Extremes(IEnumerable<int> v)
  => (v.Min(), v.Max());

var r = Extremes(new[] { 3, 9, 1 });
Console.WriteLine($"{r.min} {r.max}");   // 1 9

EN PRATIQUE
TryParse revient sans cesse pour lire une saisie clavier ou un champ de
configuration. Renvoyer un tuple évite de créer une classe de résultat
pour deux ou trois valeurs qui vont toujours ensemble.

PIÈGES À ÉVITER
- Convert.ToInt32 sur du texte invalide : FormatException
- oublier d'affecter un paramètre ref : erreur à la compilation
- surcharger en changeant seulement le nom des paramètres : ambiguïté

À RETENIR
- TryParse renvoie un booléen et ne lève jamais d'exception
- out pour produire un résultat, ref pour le transformer
""",
            "Classes et objets": """OBJECTIFS
- créer des classes avec propriétés et constructeurs
- maîtriser static, readonly et les membres expression-bodied
- appliquer l'encapsulation

POINTS CLÉS
- propriété : public string Nom { get; set; } avec un champ privé en appui
- get; private set; : lecture seule depuis l'extérieur
- readonly : affecté au constructeur seulement
- constructeur chaîné : this(...) pour réutiliser un autre constructeur
- init-only : propriété fixée une seule fois à l'initialisation
- static porte l'état partagé par toutes les instances

EXEMPLE
class Compte {
  public string Titulaire { get; }
  public decimal Solde { get; private set; }
  public Compte(string t, decimal s = 0) {
    Titulaire = t; Solde = s;
  }
  public void Deposer(decimal m) {
    if (m > 0) Solde += m;
  }
}
var c = new Compte("Babi", 100);
c.Deposer(50);
Console.WriteLine(c.Solde);       // 150

EN PRATIQUE
Les entités d'une application (Client, Produit, Commande) sont des classes
à propriétés validées. decimal protège les montants et l'encapsulation
centralise les règles de gestion au même endroit.

PIÈGES À ÉVITER
- exposer un champ public : toute la validation disparaît
- oublier d'affecter une propriété obligatoire : le constructeur refuse
- utiliser double pour l'argent : les arrondis s'accumulent

À RETENIR
- propriété pour l'état, méthode pour le comportement
- decimal pour l'argent, jamais double
""",
            "Collections": """OBJECTIFS
- choisir List, Dictionary ou HashSet selon le besoin
- parcourir et transformer avec foreach
- connaître les méthodes courantes de chaque conteneur

POINTS CLÉS
- List<T> : Add, Count, accédeur d'index [i]
- Dictionary<K,V> : TryGetValue, accédeur d'index
- HashSet<T> : sans doublons, Contains en temps constant
- IReadOnlyList<T> pour exposer une liste en lecture seule
- AddRange ajoute une séquence, Insert cible un index précis
- Remove renvoie un booléen : vérifiez s'il a trouvé
- Queue<T> et Stack<T> pour les files et les piles

EXEMPLE
var notes = new Dictionary<string, int> {
  ["alice"] = 15, ["bob"] = 12
};
if (notes.TryGetValue("alice", out int v))
  Console.WriteLine(v);
var uniques = new HashSet<string> { "a", "a", "b" };
Console.WriteLine(uniques.Count);          // 2

EN PRATIQUE
Formulaire, stock, scores, index de recherche : presque tout se traduit
par une List pour conserver l'ordre, un Dictionary pour accéder par clé
et un HashSet pour tester l'appartenance sans doublons.

PIÈGES À ÉVITER
- indexer un dictionnaire sans test : KeyNotFoundException
- modifier une List pendant un foreach : InvalidOperationException
- trier la liste à chaque affichage : triez une fois et réutilisez

À RETENIR
- List.Remove ne renvoie que true ou false : vérifiez le résultat
- choisissez la structure selon l'opération dominante
""",
            "Héritage et interfaces": """OBJECTIFS
- hériter d'une classe de base
- redéfinir avec virtual et override
- implémenter une ou plusieurs interfaces
- créer un type léger avec record

POINTS CLÉS
- virtual n'est pas la valeur par défaut : il faut le déclarer
- abstract : classe ou méthode à implémenter par les dérivés
- : IComparable<Produit> impose la méthode CompareTo
- record : type valeur avec égalité structurelle
- sealed empêche la redéfinition, base(...) appelle le constructeur du parent
- is et as testent ou convertissent une référence

EXEMPLE
abstract class Forme {
  public abstract double Aire();
}
class Cercle : Forme {
  private readonly double r;
  public Cercle(double r) { this.r = r; }
  public override double Aire() => Math.PI * r * r;
}
Forme f = new Cercle(2);
Console.WriteLine(f.Aire());   // méthode choisie à l'exécution

EN PRATIQUE
Les bibliothèques séparent souvent une classe abstraite (code commun) et
des interfaces (capacités : comparable, sérialisable, triable). Combiner
les deux donne des architectures souples et faciles à tester.

PIÈGES À ÉVITER
- oublier virtual : override est refusé à la compilation
- implémenter une interface sans public : erreur de visibilité
- attendre d'une classe abstraite qu'elle s'instancie : impossible

À RETENIR
- interface = contrat de capacité ; héritage = relation est-un
- abstract impose, virtual autorise
""",
            "LINQ": """OBJECTIFS
- interroger des collections de façon déclarative
- enchaîner Where, Select, OrderBy, GroupBy
- distinguer les requêtes sur objets des requêtes sur base de données

POINTS CLÉS
- Where filtre, Select projette, OrderBy trie
- ToList() matérialise (attention aux requêtes différées)
- GroupBy pour les regroupements, Any et All pour les tests
- syntaxe méthodes recommandée plutôt que la requête query {}
- First renvoie un élément et lève, FirstOrDefault renvoie null
- Take et Skip permettent de paginer les résultats
- agrégats : Count, Sum, Min, Max, Average

EXEMPLE
var admis = notes
  .Where(n => n.Value >= 10)
  .OrderByDescending(n => n.Value)
  .Select(n => n.Key)
  .ToList();
int total = notes.Count();
bool doublon = notes.Any(n => n.Key == "bob");

EN PRATIQUE
Rapports, filtres d'écran et exports utilisent LINQ : la requête s'écrit
comme une phrase et reste lisible même plusieurs mois plus tard.
Matérialisez avec ToList() avant de modifier la collection d'origine.

PIÈGES À ÉVITER
- modifier la liste pendant l'énumération : InvalidOperationException
- ré-exécuter une requête non matérialisée : pensez à ToList()
- confondre Any et Count > 0 : Any s'arrête au premier élément

À RETENIR
- une requête LINQ s'exécute à l'énumération, pas à la déclaration
- Where filtre les éléments, Select transforme leur forme
""",
        },
        "exercises": {
            "Console .NET": """ÉNONCÉ
- créer un projet console avec le SDK et afficher un message puis quelques informations sur l'environnement d'exécution.

ÉTAPES
1. créer le projet : dotnet new console -n MonProg
2. écrire un Console.WriteLine dans Program.cs
3. afficher Environment.Version et le nom de la machine
4. exécuter avec dotnet run
5. vérifier la compilation seule avec dotnet build

RÉSULTAT ATTENDU
- la première ligne affiche Bonjour .NET !
- la version du runtime apparaît, par exemple 8.0.4
- le nom de la machine est affiché en dernier

POUR TESTER
- relancez dotnet run : le message est identique à chaque exécution
- modifiez le texte puis rebuild : la nouvelle valeur doit s'afficher
- cas limite : terminez par Environment.Exit(1) et vérifiez le code retour

INDICE
- le fichier Program.cs utilise les « top-level statements » : pas de classe Main obligatoire.
- Environment.MachineName fournit le nom de la machine en une ligne.
""",
            "Calculatrice": """ÉNONCÉ
- créer une classe Opérations avec des méthodes statiques et un menu console qui recommence après chaque calcul.

ÉTAPES
1. écrire static double Addition(double a, double b) et les trois autres
2. lire les deux nombres avec int.TryParse ou double.TryParse
3. demander l'opérateur et le traiter avec un switch
4. boucler tant que l'utilisateur n'écrit pas « q »
5. afficher le résultat formaté avec deux décimales

RÉSULTAT ATTENDU
- 7 * 6 donne 42
- une saisie invalide affiche un message puis redemande
- le menu réapparaît après chaque calcul

POUR TESTER
- essayez 3 / 0 : le programme refuse sans planter
- tapez une lettre à la place d'un nombre : TryParse relance la saisie
- cas limite : saisissez l'opérateur en majuscule ou en minuscule, les deux doivent passer

INDICE
- un switch sur char (opérateur) rend le menu très lisible.
- double.TryParse convient mieux que int.TryParse pour accepter les décimaux.
""",
            "Liste de courses": """ÉNONCÉ
- gérer une liste de courses : ajouter, supprimer, cocher comme acheté et sauvegarder le résultat dans un fichier.

ÉTAPES
1. déclarer le record Article(string Nom, bool Acheté)
2. manipuler une List<Article> avec Add et Remove
3. marquer un article acheté via son index ou un prédicat
4. File.WriteAllLines pour écrire, File.ReadAllLines au démarrage
5. proposer un menu numéroté avec sortie sur « q »

RÉSULTAT ATTENDU
- l'ajout de « pain » le fait apparaître dans la liste
- l'article coché est marqué acheté à l'affichage
- après redémarrage, la liste est conservée à l'identique

POUR TESTER
- supprimez un article puis quittez : il ne doit pas revenir au démarrage
- ajoutez deux fois le même article : le comportement doit être annoncé
- cas limite : fichier absent au premier lancement, la liste démarre vide

INDICE
- sérialisez « nom|acheté » par ligne pour un format texte simple.
- séparez les champs avec String.Split puis reconstruisez le record.
""",
            "Gestion d'étudiants": """ÉNONCÉ
- à partir d'une liste d'étudiants (nom et notes), produire le classement, les moyennes individuelles et la moyenne de la promotion avec LINQ.

ÉTAPES
1. déclarer la classe Etudiant { string Nom; List<double> Notes; }
2. calculer la moyenne par étudiant avec Notes.Average()
3. ordonner le classement avec OrderByDescending sur la moyenne
4. afficher le top 3 puis les admis (moyenne >= 10)
5. afficher la moyenne générale de la promotion

RÉSULTAT ATTENDU
- Bob 16.5 en premier, Alice 14.3, Carla 9.8
- seuls Bob et Alice sont admis
- la moyenne de la promotion s'affiche sous le classement

POUR TESTER
- ajoutez une note de 20 à Carla : elle doit basculer dans les admis
- testez un étudiant sans aucune note : le programme doit signaler le cas au lieu de planter
- vérifiez que les moyennes du classement sont bien décroissantes

INDICE
- Select(n => new { n.Nom, Moy = n.Notes.Average() }) crée une vue calculée.
""",
            "Sérialiser JSON": """ÉNONCÉ
- sérialiser puis désérialiser un objet avec System.Text.Json, en traitant proprement les erreurs de format.

ÉTAPES
1. définir la classe avec des propriétés publiques
2. produire le texte avec JsonSerializer.Serialize(obj)
3. relire avec Deserialize<T>(json) dans un try/catch JsonException
4. afficher les champs relus côte à côte
5. écrire puis relire un fichier sur le disque

RÉSULTAT ATTENDU
- l'objet produit un JSON propre et relisible
- un JSON cassé affiche « format invalide » sans planter
- les champs relus sont identiques aux valeurs de départ

POUR TESTER
- supprimez une accolade : le catch doit se déclencher
- remplacez une valeur numérique par du texte : l'erreur doit être signalée
- cas limite : un JSON vide doit être refusé avec le même message

INDICE
- JsonSerializerOptions { WriteIndented = true } rend le fichier lisible.
- affichez l'exception capturée pour comprendre où se situe l'erreur.
""",
            "FizzBuzz": """ÉNONCÉ
- générer la séquence FizzBuzz de 1 à 100 dans une List<string>, puis l'afficher dix valeurs par ligne.

ÉTAPES
1. boucler de 1 à 100 inclus
2. appliquer les divisibilités : par 15, puis par 3, puis par 5, sinon le nombre
3. ajouter chaque chaîne obtenue à la List<string>
4. afficher avec un index pour provoquer le retour à la ligne
5. vérifier la longueur de la liste produite

RÉSULTAT ATTENDU
- début : 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz
- autour de 15 : 14, FizzBuzz, 16
- la liste contient exactement 100 éléments

POUR TESTER
- contrôlez les positions 3, 5 et 15 : Fizz, Buzz, FizzBuzz
- comptez les éléments par ligne : dix partout, sauf peut-être la dernière
- cas limite : 90 doit afficher FizzBuzz car divisible par 3 et par 5

INDICE
- une expression switch sur (i % 3, i % 5) condense tout le choix.
- ajoutez l'élément avec Add puis contrôlez Count à la fin de la boucle.
""",
            "Compte bancaire": """ÉNONCÉ
- implémenter un compte bancaire en decimal avec dépôt, retrait, virement et journal horodaté des opérations.

ÉTAPES
1. définir decimal Solde { get; private set; }
2. écrire Depositer et Retirer avec contrôle du signe et du solde
3. lever InvalidOperationException quand le retrait est impossible
4. conserver une List<string> journal de chaque opération
5. permettre un virement entre deux comptes

RÉSULTAT ATTENDU
- dépôt de 100 puis retrait de 30 : solde 70 et 2 entrées au journal
- retrait de 500 : exception avec un message explicite
- chaque ligne du journal contient la date et le montant

POUR TESTER
- après un virement, la somme des soldes des deux comptes doit rester stable
- un dépôt négatif doit être refusé avant toute modification
- cas limite : retrait exactement égal au solde doit réussir et laisser 0

INDICE
- decimal.Parse/euro : culture fr-FR pour l'affichage (ToString("0.00 €")).
""",
        },
    },
}
