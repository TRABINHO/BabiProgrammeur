"""Corrections commentées — lot 3 : Go, Rust, SQL.

Une entrée par exercice du curriculum (titre exact, copié-collé depuis
core/curriculum.py, clé "exercises" obligatoire) :

    CONTENT["Go"]["exercises"]["Bonjour Go"] = \"\"\"SOLUTION
    ...
    \"\"\"

Fusionnées dans core/solutions.py. Contrôle :
    python tests/check_solutions.py Go Rust SQL
"""
CONTENT = {
    "Go": {"exercises": {}},
    "Rust": {"exercises": {}},
    "SQL": {"exercises": {}},
}

CONTENT["Go"]["exercises"]["Bonjour Go"] = """SOLUTION

package main

import "fmt"

func main() {
    fmt.Println("Bonjour, Go !")
    nom := "Gophers"
    fmt.Println("Salut", nom, "!")
    somme := 0
    for n := 1; n <= 100; n++ {
        somme += n
    }
    fmt.Println("Somme de 1 à 100 :", somme)
}
// sortie : Bonjour, Go ! / Salut Gophers ! / Somme de 1 à 100 : 5050

EXPLICATION

Un fichier exécutable doit appartenir au package main et contenir la
fonction main. On l'enregistre sous le nom main.go, puis go run main.go
compile et lance le programme en une seule commande. Le raccourci :=
déclare la variable et fait deviner son type : nom devient string,
somme devient int. fmt.Println sépare ses arguments par un espace et
ajoute un saut de ligne. Le point-virgule en fin de ligne est facultatif :
Go l'insère lui-même, c'est une règle de sa syntaxe.

POINTS DE VÉRIFICATION

- go run main.go affiche exactement les trois lignes attendues.
- Sans « package main » ni func main(), la compilation échoue.
- Un identifiant déclaré puis jamais lu provoque une erreur : Go refuse
  le code mort.
- var somme int = 0 remplace utilement := quand le type doit être explicite.

POUR ALLER PLUS LOIN

- go fmt main.go réécrit le fichier avec l'indentation officielle.
- go mod init bonjour crée un module, utile dès qu'on sépare le code en
  plusieurs fichiers.
"""

CONTENT["Go"]["exercises"]["Convertisseur"] = """SOLUTION

package main

import (
    "flag"
    "fmt"
)

func main() {
    metres := flag.Float64("metres", 1.0, "distance en mètres")
    vers := flag.String("vers", "pieds", "cible : pieds ou pouces")
    flag.Parse()
    switch *vers {
    case "pieds":
        fmt.Println(*metres, "m valent", *metres*3.28084, "pieds")
    case "pouces":
        fmt.Println(*metres, "m valent", *metres*39.3701, "pouces")
    default:
        fmt.Println("Unité inconnue :", *vers)
    }
}
// go run convertisseur.go -metres 2.5 -vers pouces

EXPLICATION

Le package flag lit la ligne de commande avant main : chaque drapeau
-nom valeur devient une variable. Float64 et String renvoient un
pointeur, d'où l'étoile *metres ; le deuxième argument sert de défaut.
flag.Parse() doit suivre la déclaration des drapeaux, sinon leurs
valeurs sont ignorées. Le cas default affiche une erreur au lieu de
convertir après une faute de frappe.

POINTS DE VÉRIFICATION

- -metres 2.5 -vers pouces affiche environ 98.429.
- Sans aucun drapeau, la distance vaut 1.0 et la cible est pieds.
- -vers km affiche « Unité inconnue : km » puis le programme sort.

POUR ALLER PLUS LOIN

- flag.Args() renvoie les arguments restants après les drapeaux.
- Ranger les taux dans une map[string]float64 : ajouter une unité ne
  demande plus de modifier le switch.
"""

CONTENT["Go"]["exercises"]["Compteur de mots"] = """SOLUTION

package main

import (
    "fmt"
    "sort"
    "strings"
)

func main() {
    texte := "Le code Go est du code simple, le code Go est lisible"
    compte := make(map[string]int)
    for _, brut := range strings.Fields(texte) {
        mot := strings.TrimSuffix(strings.ToLower(brut), ",")
        compte[mot]++
    }
    var mots []string
    for mot := range compte {
        mots = append(mots, mot)
    }
    sort.Strings(mots)
    for _, mot := range mots {
        fmt.Println(mot, ":", compte[mot])
    }
}
// sortie : code : 3 / du : 1 / est : 2 / go : 2 / le : 3 / lisible : 1

EXPLICATION

strings.Fields découpe la phrase sur les espaces et ignore les blancs
multiples : chaque mot devient une clé. ToLower rassemble « Go » et
« go », TrimSuffix retire la virgule qui sinon créerait une clé à part
pour « simple, ». compte[mot]++ crée la clé manquante avec 0 puis
l'augmente. L'ordre des clés étant aléatoire, les mots sont copiés dans
une slice triée avant d'afficher.

POINTS DE VÉRIFICATION

- « code » et « le » valent 3, « go » et « est » valent 2.
- strings.Fields("") renvoie une slice vide : aucune ligne affichée.
- Sans sort.Strings, l'ordre des lignes change à chaque exécution.

POUR ALLER PLUS LOIN

- Garder les trois mots les plus fréquents avec un tri sur les valeurs.
"""

CONTENT["Go"]["exercises"]["Liste de tâches"] = """SOLUTION

package main

import "fmt"

type Tache struct {
    titre string
    faite bool
}

type ListeTaches struct{ items []Tache }

func (l *ListeTaches) Ajouter(titre string) {
    l.items = append(l.items, Tache{titre: titre})
}

func (l *ListeTaches) Terminer(titre string) bool {
    for i := range l.items {
        if l.items[i].titre == titre {
            l.items[i].faite = true
            return true
        }
    }
    return false
}

func main() {
    var l ListeTaches
    l.Ajouter("Lire le cours Go")
    l.Ajouter("Réussir l'exercice")
    fmt.Println("Terminer :", l.Terminer("Lire le cours Go"))
    fmt.Println("Encore :", l.Terminer("Lire le cours Go"))
    for _, t := range l.items {
        fmt.Println("-", t.titre, t.faite)
    }
}
// Terminer : true / Encore : true / - Lire le cours Go true /
// - Réussir l'exercice false

EXPLICATION

Le receiver *ListeTaches est un pointeur : Ajouter et Terminer
modifient la slice partagée. Sans l'étoile, on travaillerait sur une
copie et la tâche ajoutée disparaîtrait. for i := range l.items donne
les index, seul moyen de modifier l'élément en place.

POINTS DE VÉRIFICATION

- Le second appel renvoie aussi true : la tâche existe et reste faite.
- Un titre inconnu fait revenir false : ce booléen ne doit pas être
  ignoré.

POUR ALLER PLUS LOIN

- Écrire Supprimer(titre) qui recolle la slice avec l.items[i+1:].
"""

CONTENT["Go"]["exercises"]["Serveur HTTP"] = """SOLUTION

package main

import (
    "fmt"
    "net/http"
)

func accueil(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Essaie /bonjour?nom=Alice")
}

func bonjour(w http.ResponseWriter, r *http.Request) {
    nom := r.URL.Query().Get("nom")
    if nom == "" {
        nom = "toi"
    }
    fmt.Fprintf(w, "Bonjour %s !", nom)
}

func main() {
    http.HandleFunc("/", accueil)
    http.HandleFunc("/bonjour", bonjour)
    fmt.Println("Serveur sur http://localhost:8080")
    http.ListenAndServe(":8080", nil)
}
// curl "http://localhost:8080/bonjour?nom=Alice" affiche : Bonjour Alice !

EXPLICATION

HandleFunc associe un chemin à une fonction. Chaque handler reçoit w, le
flux de réponse vers le client, et r, la requête : on écrit avec
Fprintln ou Fprintf plutôt que Println. ListenAndServe bloque ensuite,
une goroutine par requête, d'où des handlers courts. Query().Get lit un
paramètre d'URL ; s'il manque, on pose un défaut avant d'afficher.

POINTS DE VÉRIFICATION

- /bonjour?nom=Alice renvoie Bonjour Alice !.
- /bonjour sans paramètre renvoie Bonjour toi !.
- Le chemin / reçoit aussi les adresses inconnues : c'est le repli.
- Le programme ne se termine jamais tout seul ; Ctrl+C l'arrête.

POUR ALLER PLUS LOIN

- Lire r.Method pour refuser un GET sur une route réservée au POST.
- Servir des fichiers avec http.FileServer(http.Dir("static")).
"""

CONTENT["Go"]["exercises"]["Pool de workers"] = """SOLUTION

package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    taches := make(chan int)
    var wg sync.WaitGroup
    for id := 1; id <= 3; id++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for t := range taches {
                fmt.Println("worker", id, "traite", t)
                time.Sleep(5 * time.Millisecond)
            }
        }(id)
    }
    for i := 1; i <= 9; i++ {
        taches <- i
    }
    close(taches)
    wg.Wait()
    fmt.Println("fin : toutes les tâches sont traitées")
}

EXPLICATION

Le canal n'a pas de tampon : chaque envoi attend un worker disponible,
ce qui répartit le travail. wg.Add(1) précède le lancement, defer
wg.Done() garantit le décompte et wg.Wait() bloque jusqu'au dernier
worker. L'id est passé en argument : sans lui, toutes les goroutines
liraient la même variable de boucle. close avant Wait libère le range.

POINTS DE VÉRIFICATION

- Les 9 tâches sont partagées entre les 3 workers, l'ordre varie.
- Sans close(taches), les workers attendent éternellement et wg.Wait
  ne revient jamais.
- Le même id affiché plusieurs fois trahit la capture par erreur.

POUR ALLER PLUS LOIN

- Noter la signature du canal en entrée et en sortie pour verrouiller
  les rôles.
- Remplacer le Sleep par un calcul mesuré et comparer les durées.
"""

CONTENT["Go"]["exercises"]["Dépenses CSV"] = """SOLUTION

package main

import (
    "encoding/csv"
    "fmt"
    "io"
    "os"
    "strconv"
)

func main() {
    donnees := `date,categorie,montant
2024-03-05,transport,12.50
2024-03-06,alimentation,23.99
2024-03-07,transport,9.80`
    os.WriteFile("depenses.csv", []byte(donnees), 0644)
    f, err := os.Open("depenses.csv")
    if err != nil { panic(err) }
    defer f.Close()
    r := csv.NewReader(f)
    total := 0.0
    lignes := 0
    for {
        ligne, err := r.Read()
        if err == io.EOF { break }
        if err != nil { panic(err) }
        if ligne[0] == "date" { continue }
        m, _ := strconv.ParseFloat(ligne[2], 64)
        total += m
        lignes++
    }
    fmt.Println(lignes, "dépenses,", total, "euros")
}
// 3 dépenses, 46.29 euros

EXPLICATION

Le fichier d'exemple est écrit avec un littéral brut entre accents
graves, qui accepte les vraies coupures de ligne, puis relu : le
programme fonctionne seul. csv.Reader livre une ligne à la fois et
io.EOF marque la fin, ce qui n'est pas une erreur. L'en-tête est sauté
avec continue, puis ParseFloat convertit le montant.

POINTS DE VÉRIFICATION

- Le total affiché vaut 46.29 pour 3 lignes de données.
- L'en-tête ne compte pas : sans continue, le total serait faux.
- Une virgule en trop fait échouer la lecture (voir err).

POUR ALLER PLUS LOIN

- Accumuler le total par catégorie dans une map[string]float64.
"""

CONTENT["Rust"]["exercises"]["Bonjour cargo"] = """SOLUTION

// Créé avec : cargo new bonjour   puis lancé : cargo run
fn main() {
    println!("Bonjour, Rust !");
    let nom = "Rustace";
    println!("Salut {} !", nom);
    let mut total = 0;
    for n in 1..=100 {
        total += n;
    }
    println!("Somme de 1 à 100 : {}", total);
}
// sortie : Bonjour, Rust ! / Salut Rustace ! / Somme de 1 à 100 : 5050

EXPLICATION

cargo new bonjour crée un dossier avec Cargo.toml et src/main.rs, seul
endroit où doit se trouver fn main. cargo run compile puis lance en une
seule commande. println! est une macro, d'où le point d'exclamation : elle
accepte les emplacements {} remplacés par les arguments suivants. let
déclare sans autoriser le changement, let mut l'autorise. La plage
1..=100 inclut 100, tandis que 1..100 s'arrêterait à 99.

POINTS DE VÉRIFICATION

- cargo run affiche les trois lignes attendues.
- Changer total en let sans mut déclenche une erreur d'emprunt mutable.
- Retirer la virgule après {} dans println! casse la macro.
- La somme vaut 5050, soit 100 × 101 ÷ 2.

POUR ALLER PLUS LOIN

- cargo build --release produit un binaire plus rapide, utile pour ce
  qui sera distribué.
- cargo fmt applique le formatage officiel du projet.
"""

CONTENT["Rust"]["exercises"]["Calculatrice"] = """SOLUTION

#[derive(Debug)]
enum Opération { Addition, Soustraction, Multiplication, Division }

fn calculer(a: f64, op: Opération, b: f64) -> Option<f64> {
    match op {
        Opération::Addition => Some(a + b),
        Opération::Soustraction => Some(a - b),
        Opération::Multiplication => Some(a * b),
        Opération::Division => {
            if b == 0.0 { None } else { Some(a / b) }
        }
    }
}

fn main() {
    println!("{:?}", calculer(7.0, Opération::Division, 2.0));
    println!("{:?}", calculer(7.0, Opération::Division, 0.0));
    println!("{:?}", calculer(7.0, Opération::Soustraction, 9.0));
}
// Some(3.5) / None / Some(-2.0)

EXPLICATION

L'énumération porte les quatre opérations, et match oblige à traiter
chacune : un bras manquant casse la compilation. Chaque bras renvoie
Option<f64>, car la division par zéro n'a pas de résultat : Some(valeur)
ou None. Le main appelle avec le chemin complet Opération::Addition, et
b == 0.0 se compare sans risque ici.

POINTS DE VÉRIFICATION

- calculer(7.0, Division, 2.0) vaut Some(3.5).
- calculer(7.0, Division, 0.0) vaut None et ne panique pas.
- {:?} affiche le contenu de Option, {} exigerait un Display.

POUR ALLER PLUS LOIN

- Ajouter PartialEq pour comparer deux résultats avec assert_eq!.
"""

CONTENT["Rust"]["exercises"]["FizzBuzz"] = """SOLUTION

fn main() {
    let lignes = (1..=100).map(|n| match (n % 3, n % 5) {
        (0, 0) => "FizzBuzz".to_string(),
        (0, _) => "Fizz".to_string(),
        (_, 0) => "Buzz".to_string(),
        _ => format!("{}", n),
    });
    for texte in lignes {
        println!("{}", texte);
    }
}
// 1 / 2 / Fizz / 4 / Buzz / Fizz / 7 / ... / FizzBuzz / ... / 100

EXPLICATION

Le tuple (n % 3, n % 5) condense les deux tests en un seul match. Le
bras (0, 0) doit venir en premier : il réunit les deux règles, sinon les
bras suivants le captureraient. Les traits _ signifient « n'importe
quoi », ils complètent les autres combinaisons. map transforme chaque
nombre en texte sans boucle explicite, format! et to_string convertissent
en String. L'ordre des bras est donc le cœur de l'exercice.

POINTS DE VÉRIFICATION

- 15 et 45 affichent FizzBuzz, 3 affiche Fizz et 5 affiche Buzz.
- 100 affiche Buzz, 101 affiche 101.
- Si (0, 0) est placé après (0, _), FizzBuzz n'apparaît jamais.
- Inverser les restes en (n % 5, n % 3) exige d'égaler (0, 0) aussi.

POUR ALLER PLUS LOIN

- Afficher avec un seul println! et join sur une Vec pour limiter les
  appels système.
- Lire une plage de nombres dans un fichier et appliquer la règle.
"""

CONTENT["Rust"]["exercises"]["Lecture de fichier"] = """SOLUTION

use std::fs;
use std::io::Error;

fn derniere(chemin: &str) -> Result<String, Error> {
    let texte = fs::read_to_string(chemin)?;
    Ok(texte.lines().last().unwrap_or("").to_string())
}

fn main() -> Result<(), Error> {
    fs::write("notes.txt", "Alice : 15\\nBob : 12")?;
    println!("Dernière ligne : {}", derniere("notes.txt")?);
    println!("Fichier absent : {}", derniere("absent.txt").is_err());
    Ok(())
}
// Dernière ligne : Bob : 12 / Fichier absent : true

EXPLICATION

read_to_string renvoie un Result : Ok avec le contenu, Err avec la
raison. L'opérateur ? propage l'erreur vers l'appelant immédiatement,
ce qui évite un match à chaque étape. Pour cela la fonction doit annoncer
Result comme type de retour. main lui-même peut renvoyer Result : il
suffit d'écrire Ok(()) à la fin. lines() itère sur les lignes sans
retour à la ligne, et unwrap_or évite un panic sur un fichier vide.

POINTS DE VÉRIFICATION

- La dernière ligne de notes.txt est Bob : 12, sans le saut de ligne.
- Lire un fichier absent renvoie true pour is_err() et ne plante pas.
- Enlever le ? après read_to_string empêche la compilation.
- lines() traite aussi les fins de ligne Windows.

POUR ALLER PLUS LOIN

- Distinguer les erreurs avec err.kind() == ErrorKind::NotFound.
- Accepter le chemin en argument avec std::env::args.
"""

CONTENT["Rust"]["exercises"]["Bibliothèque"] = """SOLUTION

struct Livre {
    titre: String,
    auteur: String,
    pages: u32,
    emprunte: bool,
}

impl std::fmt::Display for Livre {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let etat = if self.emprunte { " (emprunté)" } else { "" };
        write!(f, "« {} » de {} - {} pages{}", self.titre, self.auteur,
               self.pages, etat)
    }
}

fn main() {
    let l = Livre {
        titre: "Les Fourmis".to_string(),
        auteur: "Bernard Werber".to_string(),
        pages: 180,
        emprunte: false,
    };
    println!("{}", l);
}
// « Les Fourmis » de Bernard Werber - 180 pages

EXPLICATION

La structure range les quatre informations d'un livre. Impl Display
permet d'afficher l'objet avec {}, sans appeler champ par champ. fmt
reçoit le formatter de sortie et write! renvoie un Result que l'on
transmet tel quel. &self est un emprunt immutable : afficher ne change
rien. String et u32 garantissent la propriété des données.

POINTS DE VÉRIFICATION

- println!("{}", l) affiche la ligne complète en une seule passe.
- Changer emprunte en true ajoute la mention entre parenthètheses.
- Tenter println!("{:?}", l) échoue tant que Debug n'est pas dérivé.

POUR ALLER PLUS LOIN

- Ajouter #[derive(Debug)] pour le débogage au format {:?}.
- Implémenter From<(String, String, u32)> pour construire plus vite.
"""

CONTENT["Rust"]["exercises"]["Itérateur personnel"] = """SOLUTION

#[derive(Clone)]
struct Compteur {
    etape: u32,
    max: u32,
    courant: u32,
}

impl Iterator for Compteur {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.courant + self.etape > self.max {
            return None;
        }
        self.courant += self.etape;
        Some(self.courant)
    }
}

fn main() {
    let c = Compteur { etape: 2, max: 10, courant: 0 };
    let valeurs: Vec<u32> = c.clone().collect();
    println!("{:?}", valeurs);
    println!("somme = {}", valeurs.iter().sum::<u32>());
}
// [2, 4, 6, 8, 10] / somme = 30

EXPLICATION

Impl Iterator demande un seul type associé Item et une seule méthode,
next. Tant que la suite tient dans la plage, on avance le curseur et on
rend Some(valeur), sinon None : collect et for cessent alors d'appeler.
&mut self est obligatoire, l'itérateur retient son état. Le curseur
démarre à 0 et la garde self.courant + self.etape > self.max évite de
dépasser le maximum. clone permet de réutiliser l'objet une fois
consommé.

POINTS DE VÉRIFICATION

- Le vecteur obtenu vaut [2, 4, 6, 8, 10] et sa somme 30.
- Une étape de 0 bouclerait sans fin : toujours valider l'étape.
- Un max plus petit que l'étape rend un vecteur vide, sans panic.

POUR ALLER PLUS LOIN

- Implémenter DoubleEndedIterator pour itérer à l'envers.
- Surcharger nth pour sauter directement une position.
"""

CONTENT["Rust"]["exercises"]["Analyse de texte"] = """SOLUTION

use std::collections::HashMap;

fn main() {
    let texte = "le chat noir dort et le chat blanc joue";
    let mut compte: HashMap<&str, u32> = HashMap::new();
    for mot in texte.split_whitespace() {
        *compte.entry(mot).or_insert(0) += 1;
    }
    let mut rang: Vec<(&str, &u32)> = compte.iter().collect();
    rang.sort_by(|a, b| b.1.cmp(a.1).then(a.0.cmp(b.0)));
    for (mot, nombre) in &rang {
        println!("{} : {}", mot, nombre);
    }
}
// le : 2 / chat : 2 / blanc : 1 / dort : 1 / et : 1 ...

EXPLICATION

split_whitespace découpe sur tous les espaces, les retours à la ligne
compris. entry(mot) cherche la clé : or_insert(0) y pose 0 si elle
manque, et le déréférencement * permet d'ajouter 1 à la valeur pointée.
L'annotation HashMap<&str, u32> fixe le type des valeurs. Comme les maps
sont désordonnées, on les copie dans une Vec de paires, puis on trie par
fréquence décroissante et par ordre alphabétique pour un résultat stable.

POINTS DE VÉRIFICATION

- le et chat comptent 2, tous les autres mots 1.
- Sans l'astérisque devant compte.entry, le code ne compile pas.
- Un mot écrit avec une majuscule forme une clé distincte.

POUR ALLER PLUS LOIN

- Mettre les mots en minuscules avec to_lowercase avant le comptage.
- Afficher seulement les cinq premiers mots du classement.
"""

CONTENT["SQL"]["exercises"]["Créer un schéma"] = """SOLUTION

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(120) NOT NULL,
    categorie VARCHAR(50),
    prix DECIMAL(8, 2) NOT NULL CHECK (prix >= 0)
);

CREATE TABLE commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients (id),
    montant_total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    statut VARCHAR(20) NOT NULL DEFAULT 'en_attente',
    date_commande DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lignes_commande (
    commande_id INT NOT NULL REFERENCES commandes (id),
    produit_id INT NOT NULL REFERENCES produits (id),
    quantite INT NOT NULL CHECK (quantite > 0),
    prix_unitaire DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY (commande_id, produit_id)
);

EXPLICATION

Les tables suivent l'ordre des dépendances : clients et produits avant
les autres. NOT NULL, UNIQUE et CHECK interdisent les valeurs
absentes, DEFAULT comble les champs oubliés, DECIMAL garde l'argent
exact là où un float arrondirait.

POINTS DE VÉRIFICATION

- INSERT INTO clients (nom, email) passe sans id.
- Deux clients au même email sont refusés (UNIQUE).
- Un prix négatif est refusé, comme une clé étrangère inconnue.

POUR ALLER PLUS LOIN

- Dessiner les cardinalités avant d'écrire le SQL.
"""

CONTENT["SQL"]["exercises"]["Clients actifs"] = """SOLUTION

SELECT c.id,
       c.nom,
       c.email,
       COUNT(cm.id) AS nombre_commandes,
       MAX(cm.date_commande) AS derniere_commande
FROM clients c
JOIN commandes cm ON cm.client_id = c.id
WHERE cm.date_commande >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY c.id, c.nom, c.email
ORDER BY derniere_commande DESC;

EXPLICATION

La jointure relie chaque client à ses commandes grâce à la clé
étrangère. WHERE filtre les lignes AVANT le regroupement : seules les
commandes des douze derniers mois sont prises en compte, puis GROUP BY
résume le reste par client. MAX donne la date de la plus récente et
COUNT(cm.id) le nombre de commandes. Toute colonne affichée sans
fonction d'agrégation doit figurer dans GROUP BY, d'où les trois
colonnes de c. L'alias permet de trier sur le résultat.

POINTS DE VÉRIFICATION

- Un client sans commande ne paraît pas : c'est une jointure interne.
- Placer la date dans le WHERE avec un LEFT JOIN transforme celui-ci en
  INNER JOIN, erreur classique.
- Commander deux fois le même jour compte deux commandes.

POUR ALLER PLUS LOIN

- Utiliser DATE_ADD(CURDATE(), INTERVAL 1 YEAR), équivalent exact.
- Ajouter HAVING COUNT(cm.id) >= 2 pour ne garder que les habitués.
"""

CONTENT["SQL"]["exercises"]["Top des ventes"] = """SOLUTION

SELECT p.nom,
       p.categorie,
       SUM(l.quantite) AS unites_vendues,
       SUM(l.quantite * l.prix_unitaire) AS chiffre_affaires
FROM lignes_commande l
JOIN produits p ON p.id = l.produit_id
JOIN commandes cm ON cm.id = l.commande_id
WHERE cm.statut = 'payee'
GROUP BY p.id, p.nom, p.categorie
HAVING SUM(l.quantite) >= 5
ORDER BY chiffre_affaires DESC
LIMIT 10;

EXPLICATION

On part des lignes de commande, puis on remonte au produit et à la
commande. WHERE écarte les commandes non payées avant tout calcul, ce
qui coûte moins cher que de filtrer après. GROUP BY regroupe toutes les
ventes d'un même produit, SUM additionne alors les quantités et le
montant. HAVING filtre les groupes déjà formés : il répond à une
valeur agrégée, là où WHERE répond à une ligne. ORDER BY utilise
l'alias, puis LIMIT ne garde que les dix meilleures lignes.

POINTS DE VÉRIFICATION

- Un produit jamais vendu n'apparaît pas, la jointure est interne.
- Sans HAVING, les produits peu vendus entrent dans le classement.
- Sans ORDER BY, LIMIT prend dix lignes au hasard.
- Retirer p.nom de GROUP BY fait échouer la requête avec ONLY_FULL_GROUP_BY.

POUR ALLER PLUS LOIN

- Ajouter ROLLUP pour obtenir un total général en plus des sous-totaux.
- Comparer avec AVG(l.prix_unitaire) et le prix catalogue.
"""

CONTENT["SQL"]["exercises"]["Rapport mensuel"] = """SOLUTION

SELECT DATE_FORMAT(cm.date_commande, '%Y-%m') AS mois,
       COUNT(DISTINCT cm.id) AS commandes,
       SUM(CASE WHEN cm.statut = 'annulee' THEN 1 ELSE 0 END) AS annulees,
       SUM(CASE WHEN cm.statut <> 'annulee'
                THEN cm.montant_total ELSE 0 END) AS chiffre_affaires,
       ROUND(100 * SUM(CASE WHEN cm.statut = 'payee'
                            THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_payees
FROM commandes cm
GROUP BY mois
ORDER BY mois;

EXPLICATION

DATE_FORMAT regroupe les dates par mois, %Y-%m donnant 2024-05. Chaque
CASE agit comme une colonne calculée ligne par ligne : il teste une
condition et rend une valeur, sinon ELSE 0 évite les NULL qui fuiraient
dans SUM. COUNT(DISTINCT cm.id) compte chaque commande une fois, utile
dès qu'une jointure duplique des lignes. La division par COUNT(*) puis
ROUND(..., 1) produit un pourcentage à une décimale. GROUP BY accepte
ici l'alias mois.

POINTS DE VÉRIFICATION

- Une commande annulée n'apporte rien au chiffre d'affaires mais reste
  au dénominateur du pourcentage.
- Un mois sans commande n'apparaît pas dans le rapport.
- pct_payees reste entre 0 et 100.
- Sans ELSE, SUM ignore les lignes et le total baisse silencieusement.

POUR ALLER PLUS LOIN

- Ajouter une colonne par catégorie avec d'autres CASE.
- Regrouper par trimestre avec QUARTER(cm.date_commande).
"""

CONTENT["SQL"]["exercises"]["Transaction"] = """SOLUTION

CREATE TABLE comptes (
    id INT PRIMARY KEY,
    nom VARCHAR(40) NOT NULL,
    solde DECIMAL(10, 2) NOT NULL
);
INSERT INTO comptes VALUES (1, 'Alice', 500.00), (2, 'Bob', 100.00);

BEGIN;
UPDATE comptes SET solde = solde - 100 WHERE id = 1;
UPDATE comptes SET solde = solde + 100 WHERE id = 2;
-- contrôle avant de trancher :
SELECT id, nom, solde FROM comptes ORDER BY id;
COMMIT;

-- En cas de problème, à la place de COMMIT :
-- ROLLBACK;

EXPLICATION

BEGIN ouvre une transaction : les deux UPDATE forment un seul bloc.
Jusqu'à COMMIT, les changements ne sont visibles que dans cette session
et peuvent être annulés. ROLLBACK les efface entièrement, la base
revient à l'état d'avant BEGIN. Le SELECT de contrôle s'insère
naturellement dans le bloc pour vérifier les soldes avant de valider.
Si une requête échoue au milieu, il faut absolument ROLLBACK, sans quoi
la base reste à mi-chemin : la somme des deux comptes ne serait plus
égale.

POINTS DE VÉRIFICATION

- Après COMMIT, Alice a 400.00 et Bob 200.00, la somme reste 600.00.
- Après ROLLBACK à la place de COMMIT, tout est revenu à l'état initial.
- Une transaction se termine toujours par COMMIT ou ROLLBACK.
- Les autres sessions ne voient rien avant COMMIT.

POUR ALLER PLUS LOIN

- Déclencher une erreur volontaire entre les deux UPDATE et observer le
  ROLLBACK.
"""

CONTENT["SQL"]["exercises"]["Vue de rapport"] = """SOLUTION

CREATE OR REPLACE VIEW v_ventes_par_client AS
SELECT c.id AS client_id,
       c.nom,
       COUNT(cm.id) AS nombre_commandes,
       COALESCE(SUM(cm.montant_total), 0) AS total_achete
FROM clients c
LEFT JOIN commandes cm
       ON cm.client_id = c.id AND cm.statut <> 'annulee'
GROUP BY c.id, c.nom;

SELECT *
FROM v_ventes_par_client
WHERE total_achete > 500
ORDER BY total_achete DESC;

EXPLICATION

Une vue est une requête nommée, enregistrée dans le dictionnaire : elle
ne stocke aucune donnée, elle rejoue le SELECT quand on l'ouvre. Le LEFT
JOIN fait apparaître les clients sans commande. COALESCE remplace alors
le NULL du total par 0 pour que le tri fonctionne. La condition sur le
statut est placée dans le ON et non dans WHERE, sinon les clients sans
commande resteraient masqués. Le WHERE extérieur filtre les groupes de
la même façon qu'un HAVING.

POINTS DE VÉRIFICATION

- Chaque client apparaît une seule ligne, même sans commande.
- Un client sans commande affiche 0 pour les deux colonnes.
- DROP VIEW v_ventes_par_client; supprime la vue sans toucher aux tables.

POUR ALLER PLUS LOIN

- Utiliser CREATE OR REPLACE VIEW pour corriger la vue sans la
  supprimer d'abord.
- Créer un index sur commandes (client_id, statut) pour accélérer.
"""

CONTENT["SQL"]["exercises"]["Requête lente"] = """SOLUTION

-- Requête d'origine, lente sur une grosse table :
EXPLAIN SELECT c.nom, cm.montant_total
FROM commandes cm
JOIN clients c ON c.id = cm.client_id
WHERE cm.statut = 'payee'
  AND cm.date_commande >= '2024-01-01'
ORDER BY cm.date_commande DESC;

-- Piste d'optimisation, dans l'ordre des colonnes utilisées :
CREATE INDEX idx_commandes_statut_date
    ON commandes (statut, date_commande);

-- Puis EXPLAIN de nouveau pour comparer les deux plans.

EXPLICATION

EXPLAIN affiche le plan d'exécution : type, key, rows, Extra. Sans
index, la table est lue en entier : type vaut ALL, key est NULL et les
lignes estimées valent la taille de la table. L'index composite se lit
de gauche à droite : statut reçoit l'égalité, puis date_commande sert
au filtre et au tri, ce qui évite le tri coûteux. L'ordre des colonnes
n'est donc pas arbitraire.

POINTS DE VÉRIFICATION

- Avant : type ALL, key NULL, rows proche de la taille de la table.
- Après : type ref, key idx_commandes_statut_date, rows très réduit.
- Extra mentionne Using filesort tant que l'index ne couvre pas le tri.
- Créer un index sur date_commande seul ne filtre pas statut.

POUR ALLER PLUS LOIN

- Étendre l'index à montant_total pour éviter toute relecture de table.
- Surveiller les lentes requêtes avec le slow query log.
"""
