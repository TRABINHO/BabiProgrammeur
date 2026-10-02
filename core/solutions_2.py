"""Corrections commentées — lot 2 : Java, C++, C#.

Une entrée par exercice du curriculum (titre exact, copié-collé depuis
core/curriculum.py, clé "exercises" obligatoire) :

    CONTENT["Java"]["exercises"]["Calculatrice"] = \"\"\"SOLUTION
    ...
    \"\"\"

Fusionnées dans core/solutions.py. Contrôle :
    python tests/check_solutions.py Java "C++" "C#"
"""
CONTENT = {
    "Java": {"exercises": {}},
    "C++": {"exercises": {}},
    "C#": {"exercises": {}},
}

CONTENT["Java"]["exercises"]["Affichage console"] = """SOLUTION

public class Main {
    public static void main(String[] args) {
        System.out.println("Bonjour Java !");
        // la version du runtime vient des propriétés système
        String version = System.getProperty("java.version");
        System.out.println("Runtime : " + version);
    }
}

EXPLICATION

La JVM cherche une méthode main de signature exacte : public static
void main(String[] args). « public » l'autorise à appeler la méthode,
« static » indique qu'aucun objet n'est nécessaire, « void » qu'elle
ne renvoie rien. Le fichier doit s'appeler Main.java, car une classe
publique doit vivre dans un fichier de même nom. println écrit la
chaîne puis un retour à la ligne ; le + assemble le message et la
propriété lue. java.version décrit le runtime qui exécute le
programme, pas le compilateur javac.

POINTS DE VÉRIFICATION

- L'affichage contient « Bonjour Java ! » puis « Runtime : » suivi
  d'un numéro du type 21.0.4.
- Renommer le fichier Programme.java provoque une erreur de
  compilation sur la classe Main.
- Retirer « public » devant main casse le lancement : rien ne
  s'affiche car la JVM ne trouve plus son point d'entrée.
- Remplacer println par print supprime le retour à la ligne.

POUR ALLER PLUS LOIN

- Écrire System.out.printf("Runtime : %s%n", version) pour formater
  l'affichage."""

CONTENT["Java"]["exercises"]["Calculatrice"] = """SOLUTION

import java.util.Scanner;

public class Calculatrice {
    static double calculer(char op, double a, double b) {
        if (op == '+') return a + b;
        if (op == '-') return a - b;
        if (op == '*') return a * b;
        if (op == '/') {
            if (b == 0) throw new IllegalArgumentException("division par zero");
            return a / b;
        }
        throw new IllegalArgumentException("operateur inconnu");
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("op (+ - * /) ou q :");
            String op = sc.next();
            if (op.equals("q")) break;
            double a = sc.nextDouble();
            double b = sc.nextDouble();
            try { System.out.println("= " + Calculatrice.calculer(op.charAt(0), a, b)); }
            catch (IllegalArgumentException e) { System.out.println(e.getMessage()); }
        }
    }
}

EXPLICATION

calculer() est statique : elle prend l'opérateur et les deux opérandes,
renvoie un double et refuse la division par zéro avant le calcul.

POINTS DE VÉRIFICATION

- Saisir +, 6 puis 2 affiche 3.0 : l'ordre est opérateur, a, b.
- Un diviseur 0 affiche « division par zero », le menu reprend.
- Un caractère inconnu affiche « operateur inconnu ».

POUR ALLER PLUS LOIN

- Passer à une expression switch (Java 14)."""

CONTENT["Java"]["exercises"]["Compte bancaire"] = """SOLUTION

public class CompteBancaire {
    private final String titulaire;
    private double solde;

    public CompteBancaire(String titulaire, double solde) {
        this.titulaire = titulaire;
        this.solde = solde;
    }

    public void deposer(double m) {
        if (m <= 0) throw new IllegalArgumentException("montant positif");
        solde += m;
    }

    public void retirer(double m) {
        if (m <= 0 || m > solde) {
            throw new IllegalArgumentException("retrait refuse");
        }
        solde -= m;
    }

    public String toString() {
        return titulaire + " : " + solde + " euros";
    }

    public static void main(String[] args) {
        CompteBancaire c = new CompteBancaire("Alice", 0);
        c.deposer(100);
        c.retirer(30);
        System.out.println(c);
        try { c.retirer(500); }
        catch (IllegalArgumentException e) { System.out.println(e.getMessage()); }
    }
}

EXPLICATION

Le champ solde est privé : tout passe par deposer() et retirer(),
donc chaque mouvement est vérifié et un solde négatif est impossible.

POINTS DE VÉRIFICATION

- Déposer 100 puis retirer 30 laisse un solde de 70.
- Retirer 500 affiche « retrait refuse », le solde reste 70.
- Déposer 0 lève « montant positif ».

POUR ALLER PLUS LOIN

- Stocker les centimes dans un long pour éviter les arrondis."""

CONTENT["Java"]["exercises"]["Gestion de notes"] = """SOLUTION

import java.util.List;

public class Eleve {
    private final String nom;
    private final List<Double> notes;

    public Eleve(String nom, List<Double> notes) {
        this.nom = nom;
        this.notes = notes;
    }

    public double moyenne() {
        return notes.stream().mapToDouble(Double::doubleValue)
                .average().orElse(0);
    }

    public String mention() {
        double m = moyenne();
        if (m >= 16) return "Excellent";
        if (m >= 10) return "Admis";
        return "Refuse";
    }

    public static void main(String[] args) {
        Eleve alice = new Eleve("Alice", List.of(14.0, 15.0, 14.0));
        Eleve bob = new Eleve("Bob", List.of(16.0, 17.0));
        System.out.println(alice.nom + " " + alice.moyenne() + " " + alice.mention());
        System.out.println(bob.nom + " " + bob.moyenne() + " " + bob.mention());
        System.out.println("classe " + (alice.moyenne() + bob.moyenne()) / 2);
    }
}

EXPLICATION

moyenne() transforme la liste en flux de doubles puis calcule la
moyenne ; orElse(0) évite la division par zéro. mention() compare
les seuils du plus grand au plus petit : 16 donne Excellent.

POINTS DE VÉRIFICATION

- Alice : 14.33 et Admis ; Bob : 16.5 et Excellent.
- La moyenne de classe vaut 15.42.
- Une liste vide renvoie 0.0.

POUR ALLER PLUS LOIN

- Formater avec System.out.printf("%.2f", moyenne())."""

CONTENT["Java"]["exercises"]["Lire un CSV"] = """SOLUTION

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class LireCsv {
    public static void main(String[] args) throws IOException {
        try (BufferedReader br = Files.newBufferedReader(
                Paths.get("personnes.csv"), StandardCharsets.UTF_8)) {
            String ligne = br.readLine();        // en-tête ignorée
            while ((ligne = br.readLine()) != null) {
                String[] champs = ligne.split(";");
                if (champs.length < 3) {
                    System.err.println("ligne ignoree : " + ligne);
                    continue;
                }
                System.out.println(champs[0] + " " + champs[1] + " " + champs[2]);
            }
        }
    }
}

EXPLICATION

try-with-resources ferme le BufferedReader automatiquement, même en
cas d'exception. La première readLine() rend l'en-tête, qu'on jette ;
la boucle s'arrête quand readLine() renvoie null. split(";") découpe
chaque ligne, et la taille du tableau révèle les lignes incomplètes.

POINTS DE VÉRIFICATION

- Un fichier de 3 lignes affiche 2 personnes.
- « Alice;Lille » sans troisième colonne est signalée puis ignorée.
- Un fichier absent déclenche IOException depuis main.

POUR ALLER PLUS LOIN

- DécouperCsv() pourrait gérer les champs entre guillemets."""

CONTENT["Java"]["exercises"]["Compteur de mots"] = """SOLUTION

import java.util.HashMap;
import java.util.Map;

public class CompteurMots {
    public static void main(String[] args) {
        String texte = "le chat le chien le";
        Map<String, Integer> compte = new HashMap<>();
        for (String mot : texte.split("[^A-Za-zÀ-ÿ]+")) {
            mot = mot.toLowerCase();
            compte.merge(mot, 1, Integer::sum);
        }
        compte.entrySet().stream()
                .sorted((a, b) -> b.getValue() - a.getValue())
                .limit(3)
                .forEach(e -> System.out.println(e.getKey() + " : " + e.getValue()));
    }
}

EXPLICATION

Le texte est découpé sur tout ce qui n'est pas une lettre, donc la
ponctuation disparaît. Chaque mot passé en minuscules est compté avec
merge : la clé est créée à 0 puis 1 est additionné grâce à
Integer::sum. Les entrées de la map sont ensuite triées par valeur
décroissante, la comparaison b - a plaçant les mots fréquents en
tête, et limit garde le top 3.

POINTS DE VÉRIFICATION

- « le chat le chien le » produit le : 3, chat : 1, chien : 1.
- « Chat » et « chat » partagent la même clé grâce aux minuscules.
- Sans les lettres accentuées dans le motif, « thé » serait coupé :
  la plage À-ÿ les conserve.

POUR ALLER PLUS LOIN

- Remplacer le tri manuel par Comparator.comparingInt(Map.Entry::
  getValue).reversed()."""

CONTENT["Java"]["exercises"]["Tri personnalisé"] = """SOLUTION

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Personne implements Comparable<Personne> {
    String nom;
    int age;

    Personne(String nom, int age) {
        this.nom = nom;
        this.age = age;
    }

    public int compareTo(Personne autre) {
        return nom.compareTo(autre.nom);
    }

    public String toString() {
        return nom + " " + age;
    }

    public static void main(String[] args) {
        List<Personne> liste = new ArrayList<>(List.of(
                new Personne("Alice", 30), new Personne("Bob", 25),
                new Personne("Alice", 22)));
        Comparator<Personne> ordre = Comparator.comparing((Personne p) -> p.nom)
                .thenComparingInt(p -> p.age);
        liste.sort(ordre);
        System.out.println(liste);
        liste.sort(ordre.reversed());
        System.out.println(liste);
    }
}

EXPLICATION

Comparable<Personne> fixe l'ordre naturel ; le Comparator compare le
nom puis l'âge, et reversed() inverse tout le comparateur construit.

POINTS DE VÉRIFICATION

- Le premier affichage est [Alice 22, Alice 30, Bob 25].
- Le second est [Bob 25, Alice 30, Alice 22], l'ordre opposé.
- Sans thenComparingInt, les deux Alice gardent leur ordre.

POUR ALLER PLUS LOIN

- Utiliser Collections.reverseOrder() pour l'ordre inversé."""

CONTENT["C++"]["exercises"]["Bonjour C++"] = """SOLUTION

#include <iostream>
#include <ctime>

int main() {
    std::cout << "Bonjour C++ !" << std::endl;
    std::time_t maintenant = std::time(nullptr);
    std::cout << "Date : " << std::ctime(&maintenant);
    return 0;
}

EXPLICATION

Le préproceseur recolle les fichiers d'en-tête au moment de la
compilation : iostream fournit cout et endl, ctime la gestion de
l'heure. cout << enchaîne les écritures, chaque opérateur renvoyant
le flux pour continuer la chaîne ; endl ajoute un retour à la ligne
et vide le tampon. time(nullptr) renvoie l'heure courante en secondes
depuis 1970, et ctime la convertit en date lisible, saut de ligne
compris. return 0 signale au système que tout s'est bien passé.

POINTS DE VÉRIFICATION

- Compilation : g++ -std=c++17 -Wall bonjour.cpp -o bonjour, sans
  aucun avertissement.
- L'exécution affiche « Bonjour C++ ! » puis « Date : » suivie du
  jour, de l'heure et de l'année.
- Supprimer #include <iostream> provoque une erreur de compilation
  sur cout, le type n'étant pas déclaré.

POUR ALLER PLUS LOIN

- Remplacer endl par un simple saut de ligne pour gagner un flush
  par affichage quand le débit compte.
- Utiliser std::put_time avec un tm passé à localtime pour formater
  la date au format JJ/MM/AAAA."""

CONTENT["C++"]["exercises"]["Calculatrice"] = """SOLUTION

#include <iostream>
#include <stdexcept>

class Nombre {
public:
    double valeur;
    explicit Nombre(double v) : valeur(v) {}

    friend Nombre operator+(const Nombre& a, const Nombre& b) {
        return Nombre(a.valeur + b.valeur);
    }
    friend Nombre operator-(const Nombre& a, const Nombre& b) {
        return Nombre(a.valeur - b.valeur);
    }
    friend Nombre operator*(const Nombre& a, const Nombre& b) {
        return Nombre(a.valeur * b.valeur);
    }
    friend Nombre operator/(const Nombre& a, const Nombre& b) {
        if (b.valeur == 0) throw std::invalid_argument("division par zero");
        return Nombre(a.valeur / b.valeur);
    }
    friend std::ostream& operator<<(std::ostream& os, const Nombre& n) {
        return os << n.valeur;
    }
};

int main() {
    Nombre a(3), b(4);
    std::cout << a + b << " " << a * b << " " << a / b << std::endl;
    return 0;
}

EXPLICATION

Les opérateurs binaires sont des fonctions amies : ils accèdent aux
champs et gardent l'ordre des opérandes, donc on écrit a + b comme
pour un double. operator<< rend l'affichage aussi naturel.

POINTS DE VÉRIFICATION

- a + b affiche 7, a * b affiche 12, a / b affiche 0.75.
- n / n avec n valant 0 lève std::invalid_argument.
- Sans explicit, Nombre n = 5 compile à l'insu du programmeur.

POUR ALLER PLUS LOIN

- Déplacer les définitions hors de la classe."""

CONTENT["C++"]["exercises"]["Tableau trié"] = """SOLUTION

#include <iostream>
#include <algorithm>
#include <utility>

void triABulles(int tab[], int n, int& echanges) {
    echanges = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (tab[j] > tab[j + 1]) {
                std::swap(tab[j], tab[j + 1]);
                echanges++;
            }
        }
    }
}

int main() {
    int tab[] = {5, 2, 8, 1};
    int autre[] = {5, 2, 8, 1};
    int echanges = 0;
    triABulles(tab, 4, echanges);
    for (int v : tab) std::cout << v << " ";
    std::cout << std::endl << "echanges : " << echanges << std::endl;
    std::sort(autre, autre + 4);
    for (int v : autre) std::cout << v << " ";
    std::cout << std::endl;
    return 0;
}

EXPLICATION

La boucle extérieure fait passer les plus grandes valeurs vers la
fin ; la borne n - i - 1 évite de comparer avec ce qui est déjà trié,
donc chaque passage raccourcit la zone de travail. Le compteur
d'échanges est transmis par référence pour être relu dans main.
std::sort, lui, travaille entre deux pointeurs bornes.

POINTS DE VÉRIFICATION

- [5, 2, 8, 1] devient [1, 2, 5, 8] dans les deux cas.
- Le tri à bulles compte des échanges, sort n'en expose aucun : la
  comparaison se fait sur le résultat, pas sur le coût.

POUR ALLER PLUS LOIN

- Ajouter un drapeau échange pour sortir plus tôt sur un tableau
  presque trié."""

CONTENT["C++"]["exercises"]["Compteur de mots"] = """SOLUTION

#include <iostream>
#include <map>
#include <sstream>
#include <string>

int main() {
    std::cout << "texte : ";
    std::string ligne;
    std::getline(std::cin, ligne);
    std::stringstream flux(ligne);
    std::map<std::string, int> compteur;
    std::string mot;
    while (flux >> mot) {
        compteur[mot]++;     // la map crée la clé à 0 si besoin
    }
    for (const auto& entree : compteur) {
        std::cout << entree.first << " : " << entree.second << std::endl;
    }
    return 0;
}

EXPLICATION

getline lit la ligne entière, y compris les espaces, puis le
stringstream rejoue le découpage opérateur par opérateur : flux >> mot
sépare sur les blancs. L'opérateur crochets de map renvoie le
compteur de la clé et l'initialise à 0 à la première rencontre, donc
compteur[mot]++ compte sans test préalable. La map étant un arbre
équilibré, la boucle d'affichage sort les mots par ordre alphabétique.

POINTS DE VÉRIFICATION

- « baba le le » affiche baba : 1 puis le : 2, dans cet ordre.
- Un mot répété plusieurs fois incrémente sa seule clé.
- Saisie vide : aucune ligne affichée, aucune erreur.

POUR ALLER PLUS LOIN

- Passer std::unordered_map pour un accès plus rapide quand l'ordre
  alphabétique n'est plus nécessaire."""

CONTENT["C++"]["exercises"]["Classe Rectangle"] = """SOLUTION

#include <iostream>
#include <stdexcept>

class Rectangle {
    double largeur;
    double hauteur;
public:
    Rectangle(double l, double h) : largeur(l), hauteur(h) {
        if (l <= 0 || h <= 0) throw std::invalid_argument("dimensions positives");
    }
    double aire() const { return largeur * hauteur; }
    double perimetre() const { return 2 * (largeur + hauteur); }
    bool operator==(const Rectangle& autre) const {
        return largeur == autre.largeur && hauteur == autre.hauteur;
    }
    friend std::ostream& operator<<(std::ostream& os, const Rectangle& r) {
        return os << r.largeur << "x" << r.hauteur;
    }
};

int main() {
    Rectangle r(4, 5);
    std::cout << r << " : aire " << r.aire()
              << ", perimetre " << r.perimetre() << std::endl;
    try {
        Rectangle invalide(-1, 2);
    } catch (const std::invalid_argument& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}

EXPLICATION

Le constructeur initialise puis valide : une dimension non positive
lève une exception, donc aucun Rectangle invalide n'existe.

POINTS DE VÉRIFICATION

- Rectangle(4, 5) affiche 4x5 : aire 20, perimetre 18.
- Rectangle(-1, 2) affiche « dimensions positives », sans plantage.
- Oublier const sur aire() interdit l'appel sur une constante.

POUR ALLER PLUS LOIN

- Comparer les surfaces pour classer des rectangles."""

CONTENT["C++"]["exercises"]["Fibonacci récursif"] = """SOLUTION

#include <iostream>
#include <chrono>

long long fibRec(int n) {
    if (n < 2) return n;                 // cas de base
    return fibRec(n - 1) + fibRec(n - 2);
}

long long fibIt(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        long long t = a + b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    auto t0 = std::chrono::steady_clock::now();
    std::cout << "recursif 40 : " << fibRec(40) << std::endl;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "iteratif 40 : " << fibIt(40) << std::endl;
    auto t2 = std::chrono::steady_clock::now();
    auto ms = [](auto d) {
        return std::chrono::duration_cast<std::chrono::milliseconds>(d).count();
    };
    std::cout << ms(t1 - t0) << " ms contre " << ms(t2 - t1) << " ms"
              << std::endl;
    return 0;
}

EXPLICATION

La récursion s'arrête à n égal 0 ou 1, sinon elle s'appelle avec
n-1 et n-2 : chaque niveau double le travail, d'où un coût
exponentiel. L'itératif garde seulement les deux derniers termes.

POINTS DE VÉRIFICATION

- fibRec(10) et fibIt(10) valent tous les deux 55.
- Pour n = 40, les deux affichent 102334155, mais le récursif prend
  plusieurs secondes contre quelques millisecondes.
- Sans cas de base, la récursion déborde la pile et plante.

POUR ALLER PLUS LOIN

- Mémoriser les résultats calculés pour éviter les recalculs."""

CONTENT["C++"]["exercises"]["Devinette console"] = """SOLUTION

#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));
    int cible = std::rand() % 100 + 1;
    int essais = 0;
    bool trouve = false;
    while (essais < 7 && !trouve) {
        essais++;
        std::cout << "essai " << essais << "/7 : ";
        int tentative;
        std::cin >> tentative;
        if (tentative == cible) trouve = true;
        else if (tentative < cible) std::cout << "plus grand" << std::endl;
        else std::cout << "plus petit" << std::endl;
    }
    if (trouve) std::cout << "trouve en " << essais << " essais" << std::endl;
    else std::cout << "perdu, c'etait " << cible << std::endl;
    std::cout << "taux : " << essais << "/7" << std::endl;
    return 0;
}

EXPLICATION

srand n'est appelé qu'une fois : sans graine, la série serait
identique à chaque lancement. Le modulo 100 + 1 donne 1 à 100. Les
indices plus grand et plus petit découpent la plage de recherche,
ce qui garantit la trouvaille en sept coups maximum.

POINTS DE VÉRIFICATION

- Une cible 42 devinée en 5 essais affiche « trouve en 5 essais ».
- Après sept essais ratés, le programme révèle la cible et affiche
  7/7.
- Le même nombre ne se répète pas d'un lancement à l'autre.

POUR ALLER PLUS LOIN

- Remplacer le couple srand et rand par <random> et
  std::mt19937 pour un générateur moderne."""

CONTENT["C#"]["exercises"]["Console .NET"] = """SOLUTION

Console.WriteLine("Bonjour .NET !");
Console.WriteLine("Runtime : " + Environment.Version);
Console.WriteLine("Machine : " + Environment.MachineName);
Console.WriteLine("OS : " + Environment.OSVersion);

foreach (var arg in args)
{
    Console.WriteLine("argument : " + arg);
}

EXPLICATION

Le SDK génère un Programme.cs en « top-level statements » : il n'y a
plus de classe Main à écrire, les instructions sont le programme.
Environment.Version donne la version du runtime .NET exécuté, pas
celle du SDK installé. MachineName et OSVersion décrivent la
machine. Le tableau args contient les mots passés après le nom du
programme lors du lancement.

POINTS DE VÉRIFICATION

- dotnet run affiche « Bonjour .NET ! » puis un numéro 8.0.x.
- dotnet run toto affiche en plus « argument : toto ».
- dotnet build ne signale aucune erreur sur un projet vierge.

POUR ALLER PLUS LOIN

- Lire une valeur au clavier avec Console.ReadLine() puis
  int.TryParse pour saisir un nombre sans planter.
- Ajouter un fichier appsettings.json et le relire avec
  Microsoft.Extensions.Configuration pour paramétrer le programme."""

CONTENT["C#"]["exercises"]["Calculatrice"] = """SOLUTION

while (true)
{
    Console.Write("op (+ - * /) ou q : ");
    string op = Console.ReadLine() ?? "";
    if (op == "q") break;
    double a = Operations.Lire("a ? "), b = Operations.Lire("b ? ");
    double? r = op switch
    {
        "+" => Operations.Addition(a, b),
        "-" => Operations.Soustraction(a, b),
        "*" => Operations.Multiplication(a, b),
        "/" => Operations.Division(a, b),
        _ => null
    };
    Console.WriteLine(r is null ? "operateur inconnu" : "resultat : " + r);
}

class Operations
{
    public static double Addition(double a, double b) => a + b;
    public static double Soustraction(double a, double b) => a - b;
    public static double Multiplication(double a, double b) => a * b;
    public static double Division(double a, double b) => a / b;

    public static double Lire(string invite)
    {
        while (true)
        {
            Console.Write(invite);
            if (double.TryParse(Console.ReadLine(), out double v)) return v;
            Console.WriteLine("saisie invalide");
        }
    }
}

EXPLICATION

Le switch transforme l'opérateur en résultat, la branche _ renvoyant
null si l'opérateur est inconnu ; TryParse refuse un texte.

POINTS DE VÉRIFICATION

- 7 puis * puis 6 affiche 42 ; q termine la boucle.
- Saisir abc affiche « saisie invalide ».

POUR ALLER PLUS LOIN

- Découper la boucle dans AfficherMenu()."""

CONTENT["C#"]["exercises"]["Liste de courses"] = """SOLUTION

string fichier = "courses.txt";
List<Article> articles = new();

if (File.Exists(fichier))
{
    articles = File.ReadAllLines(fichier)
        .Select(l => l.Split('|'))
        .Select(p => new Article(p[0], p.Length > 1 && p[1] == "x"))
        .ToList();
}

articles.Add(new Article("pain", false));
articles.RemoveAll(a => a.Nom == "beurre");
for (int i = 0; i < articles.Count; i++)
{
    if (articles[i].Nom == "lait") articles[i] = articles[i] with { Acheté = true };
}

foreach (var a in articles)
    Console.WriteLine((a.Acheté ? "[x] " : "[ ] ") + a.Nom);

File.WriteAllLines(fichier,
    articles.Select(a => a.Nom + (a.Acheté ? "|x" : "|o")));

record Article(string Nom, bool Acheté);

EXPLICATION

Le record décrit une ligne de la liste ; il est immuable, on remplace
un article pour le cocher grâce à with. Add et RemoveAll gèrent la
liste, et la persistance encode l'état par |x ou |o dans un fichier
texte que la relecture reconstruit au démarrage.

POINTS DE VÉRIFICATION

- Après ajout de « pain », l'affichage montre [ ] pain.
- Après le cocher de « lait », la ligne commence par [x].
- Le fichier courses.txt est réécrit à chaque exécution ; un
  démarrage suivant relit la liste conservée.

POUR ALLER PLUS LOIN

- Sérialiser la liste en JSON avec System.Text.Json pour conserver
  les accents sans format maison."""

CONTENT["C#"]["exercises"]["Gestion d'étudiants"] = """SOLUTION

List<Etudiant> classe = new()
{
    new Etudiant { Nom = "Bob", Notes = new List<double> { 16.0, 17.0 } },
    new Etudiant { Nom = "Alice", Notes = new List<double> { 14.0, 14.5, 14.5 } },
    new Etudiant { Nom = "Carla", Notes = new List<double> { 9.0, 10.5 } }
};

var classement = classe
    .Select(e => new { e.Nom, Moy = e.Notes.Average() })
    .OrderByDescending(x => x.Moy)
    .ToList();

foreach (var e in classement)
    Console.WriteLine($"{e.Nom} {e.Moy:F1} {(e.Moy >= 10 ? "admis" : "refuse")}");

Console.WriteLine("top 3 : " + string.Join(", ",
    classement.Take(3).Select(x => x.Nom)));

class Etudiant
{
    public string Nom { get; set; } = "";
    public List<double> Notes { get; set; } = new();
}

EXPLICATION

Select fabrique une vue avec la moyenne calculée, sans modifier les
étudiants. OrderByDescending classe cette vue du meilleur au moins
bon, et Take garde les trois premiers. L'opérateur conditionnel dans
l'interpolation choisit la mention à partir de la moyenne.

POINTS DE VÉRIFICATION

- Bob 16.5 apparaît en premier, Alice 14.3 ensuite, Carla 9.8 en fin.
- Seuls Bob et Alice sont admis, Carla est refusee avec 9.8.
- L'ordre de la liste d'origine n'est pas modifié par le tri LINQ.

POUR ALLER PLUS LOIN

- Ajouter ThenBy(e => e.Nom) pour départager les ex æquo par nom."""

CONTENT["C#"]["exercises"]["Sérialiser JSON"] = """SOLUTION

using System.Text.Json;

Personne p = new() { Nom = "Alice", Age = 30 };
var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(p, options);
Console.WriteLine(json);

string casse = "{Nom:";                 // JSON volontairement invalide
try
{
    Personne relu = JsonSerializer.Deserialize<Personne>(casse) ?? new();
    Console.WriteLine($"{relu.Nom} {relu.Age}");
}
catch (JsonException)
{
    Console.WriteLine("format invalide");
}

class Personne
{
    public string Nom { get; set; } = "";
    public int Age { get; set; }
}

EXPLICATION

Serialize transforme l'objet en texte ; WriteIndented met un retour
à la ligne par propriété pour rester lisible. Deserialize reconstruit
l'objet depuis le texte, mais un JSON cassé déclenche une JsonException
que le try / catch transforme en message clair au lieu d'un plantage.
Les propriétés publiques sont le contrat de sérialisation.

POINTS DE VÉRIFICATION

- L'affichage montre un objet JSON avec Nom et Age indentés.
- La chaîne tronquée affiche « format invalide », le programme
  continue.
- Une propriété renommée sortirait avec un autre nom dans le JSON.

POUR ALLER PLUS LOIN

- Renseigner JsonPropertyName pour choisir le nom exact de chaque
  champ dans le fichier."""

CONTENT["C#"]["exercises"]["FizzBuzz"] = """SOLUTION

List<string> suite = new();

for (int i = 1; i <= 100; i++)
{
    suite.Add((i % 3, i % 5) switch
    {
        (0, 0) => "FizzBuzz",
        (0, _) => "Fizz",
        (_, 0) => "Buzz",
        _ => i.ToString()
    });
}

for (int i = 0; i < suite.Count; i++)
{
    Console.Write(suite[i].PadRight(9));
    if ((i + 1) % 10 == 0) Console.WriteLine();
}

EXPLICATION

L'expression switch travaille sur le couple des deux restes : le cas
(0, 0) est testé en premier, donc un multiple de 15 affiche
FizzBuzz et les autres branches sont ignorées. Les tirets bas
signifient « indifférent ». La séquence complète est stockée dans une
List<string>, puis affichée dix éléments par ligne en profitant de
l'index de boucle.

POINTS DE VÉRIFICATION

- La liste contient exactement 100 éléments, du 1 au 100.
- L'élément d'indice 14 vaut FizzBuzz, l'élément 0 vaut 1.
- L'affichage comporte 10 lignes de 10 colonnes alignées.

POUR ALLER PLUS LOIN

- Remplacer la List par une chaîne concaténée et string.Join pour
  économiser les allocations."""

CONTENT["C#"]["exercises"]["Compte bancaire"] = """SOLUTION

var c = new CompteBancaire("Alice");
c.Depositer(100m);
c.Retirer(30m);
Console.WriteLine($"{c.Titulaire} : {c.Solde:0.00} euros");
try { c.Retirer(500m); }
catch (InvalidOperationException e) { Console.WriteLine(e.Message); }

class CompteBancaire
{
    public string Titulaire { get; }
    public decimal Solde { get; private set; }
    public List<string> Journal { get; } = new();

    public CompteBancaire(string titulaire)
    {
        Titulaire = titulaire;
    }

    public void Depositer(decimal montant)
    {
        if (montant <= 0) throw new InvalidOperationException("montant positif");
        Solde += montant;
        Journal.Add($"{DateTime.Now:t} depot {montant:0.00}");
    }

    public void Retirer(decimal montant)
    {
        if (montant <= 0 || montant > Solde)
            throw new InvalidOperationException("retrait refuse");
        Solde -= montant;
        Journal.Add($"{DateTime.Now:t} retrait {montant:0.00}");
    }
}

EXPLICATION

decimal évite les imprécisions du double en monnaie. Solde n'a que
private en écriture : Depositer et Retirer valident puis notent tout.

POINTS DE VÉRIFICATION

- Le solde affiché est 70.00, le journal compte deux entrées.
- Un retrait de 500 affiche « retrait refuse », solde inchangé.
- Un dépôt négatif lève « montant positif ».

POUR ALLER PLUS LOIN

- Ajouter un virement entre deux comptes."""
