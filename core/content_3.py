"""Fiches de contenu — lot 3 : Go, Rust, SQL."""
from __future__ import annotations

CONTENT = {
    "Go": {
        "lessons": {
            "Variables et types": """OBJECTIFS
- déclarer des variables avec var, := et const
- connaître les types de base et le typage fort
- convertir explicitement d'un type à l'autre
- afficher des valeurs formatées avec fmt

POINTS CLÉS
- := déclare et affecte à l'intérieur d'une fonction
- var x int = 0 force le type, var x = 0 le déduit
- const TVA = 0.2 : constante évaluée à la compilation
- Go refuse toute conversion implicite : float64(n) avant de diviser
- types de base : string, int, float64, bool, rune, byte
- fmt.Printf("%d ans", age) formate, %v affiche n'importe quoi

EXEMPLE
nom := "Babi"
age := 30
const TVA = 0.2
fmt.Println(nom, age)          # Babi 30
fmt.Println(float64(7) / 2)    # 3.5 : sans float64, ce serait 3
fmt.Printf("%s a %d ans\\n", nom, age)
total := int(19.9) + 1
fmt.Println(total, TVA*100)    # 20 20

EN PRATIQUE
Les saisies clavier arrivent en texte : on les convertit en nombre avant de
calculer, puis en texte pour afficher. Les montants d'argent sont souvent
gardés en entiers, en centimes, pour éviter les erreurs d'arrondi.

PIÈGES À ÉVITER
- 7 / 2 vaut 3 en Go : deux entiers produisent un entier
- strconv.Atoi renvoie une erreur : vérifiez-la avant le calcul

À RETENIR
- typage fort : rien ne se convertit tout seul
- := en local, var pour les globales, const pour les valeurs figées
- %d pour les entiers, %s pour le texte, %f pour les décimaux
""",
            "Structures et méthodes": """OBJECTIFS
- définir des struct et leurs méthodes
- choisir entre récepteur valeur et récepteur pointeur
- appliquer les tags JSON à une structure

POINTS CLÉS
- type Compte struct { Titulaire string `json:"titulaire"` } pour JSON
- func (c Compte) afficher() : récepteur valeur, copie de la structure
- func (c *Compte) deposer(m float64) : pointeur, modifie l'original
- une méthode qui écrit dans un champ exige le récepteur pointeur
- embedding : une struct contenant une autre hérite de ses méthodes

EXEMPLE
type Point struct{ X, Y int }

func (p Point) norme() int { return p.X*p.X + p.Y*p.Y }

func (p *Point) deplacer(dx, dy int) {
  p.X += dx
  p.Y += dy
}

p := Point{X: 3, Y: 4}
fmt.Println(p.norme())    # 25
p.deplacer(1, 1)
fmt.Println(p.X, p.Y)     # 4 5

EN PRATIQUE
Une API Go renvoie presque toujours des struct taguées json : les champs
repris avec leur clé json deviennent les champs de la réponse HTTP. Les
méthodes sur pointeur servent aux opérations qui modifient l'état.

PIÈGES À ÉVITER
- appeler une méthode modifiante sur une valeur copiée : la modification
  est perdue, Go a copié la structure avant l'appel
- oublier le pointeur alors que la méthode écrit : le code ne compile pas

À RETENIR
- récepteur valeur pour lire, récepteur pointeur pour modifier
- le tag json relie la structure à la réponse HTTP
- gofmt aligne les champs : gardez le style du langage
""",
            "Fonctions et erreurs": """OBJECTIFS
- écrire des fonctions avec plusieurs retours
- gérer les erreurs à la go, comme des valeurs
- propager l'erreur jusqu'au main

POINTS CLÉS
- func div(a, b int) (int, error) : deux retours, pas d'exception
- convention : nil = pas d'erreur, sinon on retourne tout de suite
- if _, err := f(); err != nil { return err } : le réflexe quotidien
- _ absorbe une valeur inutile sans déclarer de variable morte
- variadiques : func somme(nombres ...int) reçoit une liste libre
- fmt.Errorf("config : %w", err) conserve la cause d'origine

EXEMPLE
func div(a, b int) (int, error) {
  if b == 0 {
    return 0, errors.New("division par zéro")
  }
  return a / b, nil
}

func main() {
  q, err := div(10, 2)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println("quotient", q)
}

EN PRATIQUE
Dans un serveur, chaque appel base de données ou fichier renvoie une erreur :
on la traite sur place ou on la remonte jusqu'au main, qui affiche le message
final puis quitte avec un code d'échec.

PIÈGES À ÉVITER
- ignorer l'erreur renvoyée (comme _ = f()) masque les pannes silencieusement
- mélanger plusieurs erreurs dans un même message sans dire laquelle est
  survenue

À RETENIR
- l'erreur est une valeur comme une autre : on la retourne, on ne la cache pas
- traiter l'erreur sur place ou la remonter, jamais les deux à moitié
- le message indique OÙ l'erreur s'est produite
""",
            "Slices et maps": """OBJECTIFS
- manipuler les slices, tableaux dynamiques
- utiliser les maps clé vers valeur
- distinguer une copie d'une vue sur les données

POINTS CLÉS
- make([]int, 0, 5) fixe la longueur et la capacité séparément
- append ajoute un élément et réalloue si la capacité manque
- map[string]int : lire m["bob"] renvoie 0 si la clé manque
- v, ok := m["bob"] : ok signale si la clé existe vraiment
- deux copies de slice partagent le tableau sous-jacent, jusqu'à append
- copie indépendante : s2 := append([]int(nil), s1...)
- len(), cap(), range et delete() servent sur ces deux structures

EXEMPLE
m := map[string]int{"alice": 15}
v, ok := m["bob"]          // ok vaut false, v vaut 0
fmt.Println(v, ok)

s := append([]int{1, 2}, 3)
fmt.Println(s, len(s))     // [1 2 3] 3

delete(m, "alice")         // retire la clé
fmt.Println(len(m))        // 0

EN PRATIQUE
Une liste de tâches ou un panier d'achat est une slice de struct. Un compte
rendu vit dans une map : des identifiants en clé, un compteur ou un solde en
valeur.

PIÈGES À ÉVITER
- lire m[k] sans second retour : impossible de distinguer 0 d'une clé absente
- réutiliser une sous-slice après avoir modifié la slice d'origine

À RETENIR
- la valeur zéro (0, "", nil) distingue une absence d'une vraie valeur
- append peut changer le tableau : surveillez le partage
- range sur une map rend clé et valeur en une seule expression
""",
            "Interfaces": """OBJECTIFS
- définir des interfaces implicitement satisfaites
- raisonner par composition plutôt que par héritage
- connaître io.Reader et io.Writer

POINTS CLÉS
- une interface est satisfaite SANS le mot implements
- petite interface = bon design : fmt.Stringer = String() string
- interface{} (ou any) accepte n'importe quel type de valeur
- une interface vaut nil seulement si valeur ET type sont nil
- une méthode à récepteur pointeur ne satisfait l'interface que par *T
- on compose des interfaces réduites plutôt qu'une interface géante

EXEMPLE
type Affichable interface{ Afficher() string }

func print(a Affichable) {
  fmt.Println(a.Afficher())
}

type Duree int

func (d Duree) Afficher() string {
  return fmt.Sprintf("%d min", int(d))
}

print(Duree(42))           // 42 min

EN PRATIQUE
Les bibliothèques Go attendent des comportements, pas des types : un handler
HTTP écrit dans un io.Writer, un décodeur lit depuis un io.Reader. Des
fonctions sur ces interfaces se testent avec des buffers en mémoire.

PIÈGES À ÉVITER
- déclarer l'interface dans le paquet qui l'implémente : elle appartient au
  consommateur, pas à celui qui la satisfait
- ajouter une méthode avec un mauvais récepteur : le compilateur refuse

À RETENIR
- Go détecte les interfaces à la compilation, sans aucune inscription
- petite interface, grand pouvoir : demandez seulement ce dont vous avez besoin
""",
            "Goroutines et channels": """OBJECTIFS
- lancer des tâches concurrentes avec go
- communiquer par channels
- attendre la fin des tâches avec WaitGroup

POINTS CLÉS
- go f() lance une goroutine, bien plus légère qu'un thread
- ch := make(chan int) ; ch <- v pour envoyer, <-ch pour recevoir
- un channel fermé reste lisible jusqu'à la fin, l'envoi après panique
- range ch se termine quand le channel est fermé
- sync.WaitGroup : Add avant, Done à la fin, Wait au point d'entrée
- go test -race détecte les accès concurrents non protégés

EXEMPLE
ch := make(chan string, len(taches))   // tampon assez grand pour tout
var wg sync.WaitGroup
for _, t := range taches {
  wg.Add(1)
  go func(n string) {
    defer wg.Done()
    ch <- traite(n)
  }(t)
}
wg.Wait()
close(ch)
for r := range ch {
  fmt.Println(r)
}

EN PRATIQUE
Un service web appelle plusieurs API en parallèle puis fusionne les réponses :
chaque appel part dans sa goroutine et WaitGroup garantit qu'aucune réponse
n'est perdue avant l'envoi au client.

PIÈGES À ÉVITER
- envoyer sur un channel non tamponné sans lecteur : le programme bloque
- lire et écrire la même variable sans mutex, même avec peu de goroutines

À RETENIR
- goroutine légère, channel sûr : deux piliers de la concurrence Go
- celui qui crée le channel décide de qui le ferme
- go test -race avant de conclure qu'un code est sûr
""",
            "Packages et modules": """OBJECTIFS
- organiser le code en packages cohérents
- gérer les dépendances avec go mod
- importer et publier proprement

POINTS CLÉS
- package main avec func main() : le seul moyen de produire un binaire
- un dossier = un package ; une majuscule rend le nom exporté
- go mod init monprojet crée le module, go get ajoute une dépendance
- les imports se groupent en trois blocs : standard, externes, locaux
- gofmt -w . formate, go vet . remarque les doutes, go test . teste

EXEMPLE
// dossier geom/geom.go
package geom

// Aire est exportée car la majuscule est visible de l'extérieur.
func Aire(l, h float64) float64 { return l * h }

// aireInterne reste cachée dans ce paquet.
func aireInterne(l, h float64) float64 { return l * h }

// main.go
package main

import "monprojet/geom"

func main() {
  fmt.Println(geom.Aire(3, 4))   // 12
}

EN PRATIQUE
Un projet Go réel sépare les paquets métier, stockage et API : chaque dossier
devient une brique réutilisable et testable isolément. go.mod fige les
versions exactes des dépendances de toute l'équipe.

PIÈGES À ÉVITER
- importer un paquet pour ses effets de bord : écrivez _ « nom/du/paquet »
- tout mettre dans package main : plus aucune réutilisation possible

À RETENIR
- un dossier, un paquet, un test : l'unité de travail de Go
- majuscule exportée, minuscule cachée
- go mod, gofmt, go vet : trois commandes du quotidien
""",
        },
        "exercises": {
            "Bonjour Go": """ÉNONCÉ
- initialiser un module Go dans un dossier vide
- afficher « Bonjour Go ! » puis la version du compilateur utilisée
- vérifier le code avec les outils officiels avant de le rendre

ÉTAPES
1. créer le dossier bonjour et lancer go mod init bonjour
2. écrire main.go : package main, func main(), import fmt
3. fmt.Println("Bonjour Go !")
4. afficher la version avec runtime.Version() dans un second Println
5. lancer go run . pour exécuter puis go vet . pour contrôler
6. gofmt -w . pour formater au standard du langage

RÉSULTAT ATTENDU
- deux lignes affichées : le message de bienvenue puis go1 suivi du numéro
  de version, par exemple go1.22.1
- aucun message d'avertissement de go vet, fichier déjà bien formaté
- le dossier contient main.go et go.mod qui nomme le module bonjour

POUR TESTER
- go run . affiche bien les deux lignes attendues à chaque exécution
- modifiez volontairement une accolade : go vet doit signaler le défaut
- relancez gofmt -w . : le fichier ne doit plus changer, signe qu'il est
  conforme

INDICE
- go run . compile en mémoire et exécute dans le répertoire courant ; sans
  ligne package main, le compilateur refuse le binaire
""",
            "Convertisseur": """ÉNONCÉ
- construire un convertisseur de température en ligne de commande, avec le
  paquet flag : l'option -c convertit des Celsius vers Fahrenheit et l'option
  -f fait l'inverse
- si aucune option n'est donnée, le programme affiche son aide

ÉTAPES
1. déclarer deux drapeaux : flag.Float64("c", 0, "Celsius") et flag.Float64("f", 0, "Fahrenheit")
2. appeler flag.Parse() avant toute lecture de valeur
3. détecter le sens de conversion selon le drapeau réellement utilisé
4. appliquer C×9/5+32 et (F-32)×5/9
5. afficher avec fmt.Printf("%.1f degrés ...", v)
6. si aucun drapeau est fourni, afficher l'aide puis quitter avec code 2

RÉSULTAT ATTENDU
- -c 0 affiche 32.0 degrés Fahrenheit
- -c 100 affiche 212.0 et -f 77 affiche 25.0 degrés Celsius
- -f 40 affiche 4.4 degrés Celsius, arrondi à une décimale
- sans argument, le message d'aide listant -c et -f s'affiche

POUR TESTER
- essayez les valeurs repères 0, 32, 100 et 212 : la conversion doit être
  symétrique, un aller-retour redonne la valeur de départ
- testez -c 0 -f 77 ensemble : le programme doit choisir un seul sens ou
  refuser poliment, jamais afficher deux résultats
- un nombre invalide comme -c abc doit produire une erreur de flag lisible

INDICE
- flag.Parse() est indispensable avant de lire les valeurs, et flag.Usage
  affiche l'aide standard du programme
""",
            "Compteur de mots": """ÉNONCÉ
- lire un texte tapé au clavier et compter combien de fois chaque mot apparaît
- afficher ensuite les mots dans l'ordre alphabétique avec leur compte
- les mots doivent être comparés sans tenir compte de la casse

ÉTAPES
1. lire os.Stdin avec bufio.NewReader ou bufio.Scanner
2. découper le texte avec strings.Fields, qui ignore les espaces multiples
3. passer chaque mot en minuscules avec strings.ToLower avant de compter
4. incrémenter un compteur de type map[string]int
5. extraire les clés dans une slice et les trier avec sort.Strings
6. afficher chaque ligne au format mot espace compte

RÉSULTAT ATTENDU
- si l'utilisateur tape « Le le chat », l'affichage contient chat 1 puis
  le 2, une ligne par mot distinct, dans l'ordre alphabétique
- les mots identiques à la casse près sont fusionnés en un seul

POUR TESTER
- saisissez une phrase répétée deux fois : les comptes doivent doubler sans
  que le nombre de lignes augmente
- testez une ligne vide, une ligne d'espaces et une ponctuation collée :
  le programme ne doit jamais planter et doit simplement afficher ce qui a
  été saisi
- vérifiez que l'ordre est bien alphabétique et pas celui de la saisie

INDICE
- range sur une map produit (clé, valeur) et les clés sont déjà uniques :
  il ne reste qu'à les trier avant l'affichage
""",
            "Liste de tâches": """ÉNONCÉ
- réaliser une liste de tâches en mémoire, sans base de données, utilisable
  depuis la ligne de commande
- trois opérations : ajouter une tâche, la marquer comme faite, la supprimer
- l'affichage numérote chaque tâche et montre son état avec une case

ÉTAPES
1. définir type Tache struct { Texte string; Faite bool }
2. garder une slice []Tache dans la fonction main ou une struct Liste
3. écrire ajouter(texte) qui fait append sur la slice
4. écrire completer(i) qui passe Faite à true à l'index i
5. écrire supprimer(i) qui reconstruit la slice avec append(t[:i], t[i+1:]...)
6. afficher chaque ligne : numéro, case [ ] ou [x], puis le texte

RÉSULTAT ATTENDU
- après ajout de « coder » puis « lire » : 1. [ ] coder puis 2. [ ] lire
- après completions : 1. [x] coder et 2. [ ] lire
- après suppression de la tâche 1 : il ne reste qu'une seule ligne, affichée
  comme 1. [ ] lire, la numérotation repartant de 1

POUR TESTER
- ajoutez trois tâches, en complétez une, puis supprimez celle du milieu et
  vérifiez que la suite conserve son ordre et que la numérotation est continue
- essayez de compléter un index hors bornes : le programme doit afficher un
  message d'erreur au lieu de panic
- supprimez tout : la liste affichée doit être vide, sans ligne fantôme

INDICE
- supprimer sans doublon : append(t[:i], t[i+1:]...) décale les éléments
  restants sur la place de celui qui part
""",
            "Serveur HTTP": """ÉNONCÉ
- monter un petit serveur HTTP local avec deux routes distinctes
- la route / répond en texte brut avec le message de bienvenue
- la route /time répond au format JSON avec la date et l'heure courantes
- le serveur doit s'arrêter proprement avec Ctrl+C

ÉTAPES
1. importer net/http, encoding/json, fmt et log
2. écrire un handler pour "/" avec http.HandleFunc qui écrit l'en-tête texte
3. écrire un handler pour "/time" qui prépare une structure reponse
4. fixer Content-Type avec w.Header().Set("Content-Type", "application/json")
5. encoder la valeur avec json.NewEncoder(w).Encode(...)
6. démarrer avec log.Fatal(http.ListenAndServe(":8080", nil))

RÉSULTAT ATTENDU
- GET http://localhost:8080/ renvoie le texte de bienvenue en texte brut
- GET http://localhost:8080/time renvoie un objet JSON contenant une clé
  heure dont la valeur suit le format 2006-01-02 15:04:05
- une route inconnue renvoie la page 404 par défaut

POUR TESTER
- ouvrez les deux adresses dans un navigateur et observez bien les deux
  formats différents, texte d'un côté, JSON de l'autre
- testez une troisième adresse : la réponse doit être 404, le serveur reste
  vivant
- avec curl, vérifiez l'en-tête Content-Type renvoyé par /time

INDICE
- httptest.NewRecorder permet d'exécuter un handler en mémoire et de relire
  la réponse, sans ouvrir de port pendant les tests
""",
            "Pool de workers": """ÉNONCÉ
- traiter 100 tâches numérotées de 1 à 100 avec un pool limité à 5
  goroutines seulement, pour limiter la concurrence réelle
- chaque tâche envoyée doit produire un résultat, dans n'importe quel ordre
  mais sans qu'aucun résultat ne se perde

ÉTAPES
1. créer jobs := make(chan int, 100) et results := make(chan int, 100)
2. lancer exactement 5 workers : for j := range jobs { results <- traiter(j) }
3. envoyer les 100 jobs dans la boucle for i := 1; i <= 100; i++
4. fermer(jobs) après le dernier envoi, depuis l'émetteur
5. collecter les 100 résultats avec une boucle for de compteur
6. fermer(results) puis afficher la somme des résultats pour contrôle

RÉSULTAT ATTENDU
- 100 lignes de résultats produites par seulement 5 goroutines
- aucun blocage : le programme arrive au bout et affiche sa somme finale
- traiter(i) peut renvoyer i*i, la somme des carrés de 1 à 100 vaut 338350

POUR TESTER
- ajoutez un print du numéro de goroutine : vous ne devez jamais voir plus
  de 5 identifiants distincts
- retirez close(jobs) : le programme bloquera à la fin, preuve que la
  fermeture signale bien la fin du flux
- lancez avec go run -race : aucune course détectée doit apparaître

INDICE
- on ferme un channel juste après le DERNIER envoi, jamais avant, et
  uniquement du côté qui envoie ; close(ch) est le signal de fin
""",
            "Dépenses CSV": """ÉNONCÉ
- lire un fichier CSV de dépenses dont les colonnes sont date, libellé et
  montant, séparées par des points-virgules
- calculer le total dépensé pour chaque mois, puis repérer le mois le plus
  dépensier de l'année
- afficher un bilan lisible, prêt à être copié dans un compte rendu

ÉTAPES
1. ouvrir le fichier avec os.Open et le lire via csv.NewReader (point-virgule)
2. passer le délimiteur à r.Comma = ';' et lire les en-têtes
3. convertir le montant avec strconv.ParseFloat, en signalant les lignes fautives
4. extraire le mois des 7 premiers caractères de la date (AAAA-MM)
5. additionner dans une map[string]float64
6. parcourir la map pour trouver la clé du maximum
7. afficher chaque mois trié, puis la ligne de bilan

RÉSULTAT ATTENDU
- un fichier de 12 lignes réparties sur 3 mois affiche 3 totaux mensuels
  puis une ligne précisant le mois le plus élevé, par exemple 2026-03
- le total global est égal à la somme des totaux mensuels

POUR TESTER
- comparez le total affiché avec la somme de la calculatrice sur toutes les
  lignes : les deux doivent être identiques
- testez un fichier sans ligne, un montant vide et un montant non
  numérique : le programme signale la ligne fautive sans s'arrêter

INDICE
- csv.Reader s'occupe déjà des guillemets et des virgules internes aux
  champs : ne découpez jamais la ligne vous-même avec strings.Split
""",
        },
    },
    "Rust": {
        "lessons": {
            "Variables et mutabilité": """OBJECTIFS
- déclarer avec let et let mut
- comprendre l'immuabilité par défaut
- utiliser le shadowing et les constantes
- lire le type attendu dans le message d'erreur

POINTS CLÉS
- let x = 5 ; la réaffectation x = 6 est refusée sans mut
- shadowing : redéclaration qui masque la précédente, conversion y compris
- const : valeur évaluée à la compilation, jamais modifiable
- types usuels i32, f64, bool, char, &str, usize pour les index
- les constantes portent souvent des majuscules, par convention

EXEMPLE
let n = "42";
let n: i32 = n.parse().unwrap();   // shadowing + conversion
let mut somme = n + 8;
println!("{}", somme);             // 50

const MAX: i32 = 100;
let croissance = MAX + 1;
println!("{}", croissance);        // 101

EN PRATIQUE
Dans une application, la plupart des valeurs restent immuables : on lit une
configuration, on la transforme, on obtient une nouvelle valeur. mut apparaît
seulement pour un compteur ou une liste que l'on remplit.

PIÈGES À ÉVITER
- mut partout dès le départ : vous perdez la protection par défaut de Rust
- shadowings successifs qui changent de type sans raison lisible

À RETENIR
- immuabilité par défaut : les bugs d'aliasing sont impossibles par construction
- mut pour modifier, shadowing pour convertir en un nouveau type
- const pour toute valeur figée partagée par tout le module
""",
            "Ownership": """OBJECTIFS
- comprendre propriétaire, emprunt et transfert
- éviter les doubles libérations sans ramasse-miettes
- choisir &T pour lire et &mut T pour écrire

POINTS CLÉS
- chaque valeur a UN propriétaire ; l'assignation TRANSFÈRE la propriété
- quand l'ancien propriétaire sort de portée, sa valeur est libérée (Drop)
- emprunt en lecture : autant de &x simultanés que vous voulez
- emprunt en écriture : un seul &mut x, jamais mêlé à un lecteur
- String est propriétaire, &str est une vue sur du texte existant
- retourner une chaîne construite : String, pas &str emprunté

EXEMPLE
let s = String::from("hi");
let r = &s;              // emprunt en lecture
println!("{}", r);
let s2 = s;              // transfert : s n'est plus utilisable

EN PRATIQUE
Une fonction qui transforme une donnée la reçoit en &mut pour ne pas vider la
variable de l'appelant. Les bibliothèques renvoient des &str quand elles le
peuvent, afin de ne rien recopier pour rien.

PIÈGES À ÉVITER
- utiliser une variable après transfert : le compilateur l'arrête, ce message
  d'erreur est votre allié, pas un obstacle
- un emprunt en écriture pendant qu'un lecteur existe : refusé, par sécurité

À RETENIR
- un propriétaire, un seul ; les emprunts suivent des règles strictes
- la mémoire est libérée à la fin de la portée, sans ramasse-miettes
- « zero-cost abstractions » : la sécurité mémoire sans coût à l'exécution
""",
            "Structures et énumérés": """OBJECTIFS
- modéliser des données avec struct et enum
- associer des données aux variantes d'une énumération
- implémenter des méthodes avec impl
- faire le tri avec match de façon exhaustive

POINTS CLÉS
- struct Point { x: f64, y: f64 } regroupe des champs nommés
- enum Commande { Quitter, Deplacer { x: i32, y: i32 } } : chaque variante
  porte ses propres données
- match doit être exhaustif : le compilateur refuse un cas oublié
- impl Point { fn norme(&self) -> f64 } ajoute des méthodes au type
- #[derive(PartialEq, Debug, Clone)] fournit les comparaisons standards

EXEMPLE
enum Commande {
  Quitter,
  Deplacer { x: i32, y: i32 },
}

let c = Commande::Deplacer { x: 3, y: 4 };
match c {
  Commande::Quitter => println!("fin"),
  Commande::Deplacer { x, y } => println!("x {} y {}", x, y),
}

EN PRATIQUE
Les messages d'une interface (cliquer, fermer, envoyer) deviennent des
variantes d'une enum : une seule fonction reçoit le type entier et match le
décrit, au lieu d'une cascade de types disparates.

PIÈGES À ÉVITER
- oublier une variante dans match : le code ne compile pas, c'est voulu
- comparer deux struct sans #[derive(PartialEq)] : le compilateur refuse

À RETENIR
- struct pour les données qui vont ensemble, enum pour les choix possibles
- les énumérés Rust portent des données : le union type complet
- impl() ajoute les méthodes, derive() ajoute les comportements standards
""",
            "Traits": """OBJECTIFS
- définir un comportement partagé avec trait
- implémenter un trait pour un type existant
- utiliser les traits bornés dans les génériques

POINTS CLÉS
- trait Affichable { fn afficher(&self) -> String; }
- impl Affichable for Point { ... } : l'implémentation se fait à l'extérieur
- <T: Display> ou impl Trait dans les paramètres de fonction
- traits usuels : Display, Debug, Clone, Copy, PartialEq, Iterator
- &dyn Affichable pour le dispatch dynamique, T: Affichable pour le statique

EXEMPLE
trait Affichable {
  fn afficher(&self) -> String;
}

impl Affichable for i32 {
  fn afficher(&self) -> String {
    format!("{} points", self)
  }
}

fn affiche<T: Affichable>(v: T) {
  println!("{}", v.afficher());
}

EN PRATIQUE
Un tri, un sérialiseur ou un rendu HTML attendent un comportement, pas un type
 précis : la fonction reçoit T: Ord, T: Serialize ou T: Affichable et devient
réutilisable avec n'importe quelle structure qui joue le jeu.

PIÈGES À ÉVITER
- implémenter un trait de la bibliothèque pour un type de la bibliothèque :
  la règle du cohérence l'interdit, passez par un nouveau type
- oublier une méthode sans corps par défaut : le code ne compile pas

À RETENIR
- le polymorphisme de trait est monomorphisé : zéro coût à l'exécution
- une petite interface décrit exactement ce dont la fonction a besoin
""",
            "Result et erreurs": """OBJECTIFS
- gérer les erreurs avec Result au lieu de panics
- propager l'erreur avec l'opérateur ?
- distinguer une erreur attendue d'un vrai bug

POINTS CLÉS
- Result<T, E> : Ok(valeur) ou Err(erreur), jamais les deux à la fois
- ? renvoie l'erreur automatiquement si le contexte le permet
- unwrap() panique si Err : réservé aux exemples dont on est sûr
- Option<T> gère l'absence ; on la transforme avec ok_or
- thiserror pour les bibliothèques, anyhow pour les applications

EXEMPLE
fn lire(path: &str) -> Result<String, io::Error> {
  let contenu = fs::read_to_string(path)?;
  Ok(contenu.trim().to_string())
}

match lire("config.txt") {
  Ok(t) => println!("{} lignes", t.lines().count()),
  Err(e) => eprintln!("lecture impossible : {}", e),
}

EN PRATIQUE
Un service web renvoie son résultat dans un Result : l'erreur remonte jusqu'au
point d'entrée, qui la traduit en message clair. Le bug, lui, mérite un panic :
on ne poursuit jamais dans un état inconnu.

PIÈGES À ÉVITER
- unwrap() dans le code produit : un fichier absent fait paniquer le service
- utiliser ? dans une fonction dont le type de retour ne correspond pas

À RETENIR
- Result est une valeur : traitez-le, ne l'ignorez pas
- l'opérateur ? écrit la propagation en un seul caractère
- panic pour un bug, Err pour une situation prévue
""",
            "Collections": """OBJECTIFS
- utiliser Vec, HashMap et String
- itérer avec for et les itérateurs
- gérer l'absence avec Option

POINTS CLÉS
- Vec<T> : push, len, iter ; un index hors bornes provoque une panique
- get(i) renvoie Option<&T> : sûr, aucune panique possible
- HashMap : lecture avec get() qui renvoie Option, insertion avec entry()
- iter(), map(), filter(), collect() composent les traitements
- String est propriétaire, &str est une vue : push_str complète String

EXEMPLE
let mut compteur = HashMap::new();
for mot in texte.split_whitespace() {
  *compteur.entry(mot).or_insert(0) += 1;
}

let mut nombres = vec![3, 1, 2];
nombres.sort();
let total: i32 = nombres.iter().sum();
println!("{:?} {}", nombres, total);

EN PRATIQUE
Un journal d'événements est un Vec de structures, un tableau de bord regroupe
les compteurs dans une HashMap. Les itérateurs enchaînés remplacent les boucles
imbriquées et se lisent presque comme une phrase.

PIÈGES À ÉVITER
- accéder avec v[i] alors que l'élément peut manquer : préférez v.get(i)
- emprunter une référence pendant une mutation : le compilateur refuse

À RETENIR
- préférez get() aux index quand l'absence est possible
- entry().or_insert(0) est la façon idiomatique de compter
- les itérateurs sont paresseux : collect() les déclenche
""",
            "Modules et crates": """OBJECTIFS
- structurer un projet avec mod et pub
- gérer Cargo et les dépendances
- écrire et exécuter des tests unitaires

POINTS CLÉS
- dossier src/ = module racine ; pub expose un élément à l'extérieur
- use chemins::du::module importe un élément d'un autre module
- Cargo.toml : [dependencies] déclare les crates et leurs versions
- cargo build, cargo run, cargo test : le trio du quotidien
- tests : #[cfg(test)] mod tests { use super::*; ... }

EXEMPLE
// src/lib.rs
pub fn double(n: i32) -> i32 { n * 2 }

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn double_2() { assert_eq!(double(2), 4); }

  #[test]
  fn double_negatif() { assert_eq!(double(-3), -6); }
}

EN PRATIQUE
Une bibliothèque sépare ses modules métier, stockage et web. Chacun garde une
visibilité minimale : tout reste privé tant que pub n'a pas été écrit, et le
fichier Cargo.lock se versionne pour une construction identique à l'équipe.

PIÈGES À ÉVITER
- tout marquer pub : vous perdez le contrôle de ce qui est exposé
- oublier #[cfg(test)] : les fonctions de test voyagent dans le binaire

À RETENIR
- cargo new lib puis cargo test : des tests dès la première minute
- pub est une décision de conception, pas un réflexe
""",
        },
        "exercises": {
            "Bonjour cargo": """ÉNONCÉ
- créer un premier projet Rust avec Cargo dans un dossier vide
- afficher « Bonjour Rust ! » puis la version du crate utilisée
- passer les contrôles de qualité avant de rendre le travail

ÉTAPES
1. lancer cargo new bonjour puis entrer dans le dossier créé
2. ouvrir src/main.rs et écrire les deux println!
3. afficher la version avec env!("CARGO_PKG_VERSION")
4. lancer cargo run, qui compile puis exécute
5. lancer cargo clippy et corriger ses recommandations
6. lancer cargo fmt pour formater au standard du langage

RÉSULTAT ATTENDU
- le terminal affiche le message de bienvenue, puis le numéro de version du
  crate, par exemple 0.1.0, puis la ligne indiquant le binaire exécuté
- cargo clippy ne remonte aucun avertissement

POUR TESTER
- relancez cargo run : la seconde exécution doit être immédiate, le binaire
  est déjà compilé
- cassez un caractère du texte : le compilateur doit indiquer le numéro de
  ligne et refuser de produire le binaire
- modifiez le message et vérifiez qu'il apparaît bien à l'exécution

INDICE
- println! est une macro, reconnaissable à son point d'exclamation : elle
  formate la chaîne à la compilation, d'où sa vitesse
""",
            "Calculatrice": """ÉNONCÉ
- construire une calculatrice sûre avec une énumération Operation qui porte
  les quatre opérations Add, Sub, Mul et Div
- une fonction appliquer reçoit l'opération et deux nombres et renvoie un
  Result<f64, String> : la division par zéro devient une erreur, jamais une
  panique qui ferait tomber le programme

ÉTAPES
1. définir enum Operation { Add, Sub, Mul, Div }
2. écrire fn appliquer(op: Operation, a: f64, b: f64) -> Result<f64, String>
3. traiter les quatre cas avec match
4. pour Div, vérifier b et renvoyer Err avec un message explicite
5. dans main, afficher le résultat avec if let Ok(v) = ...
6. tester les quatre opérations puis le cas interdit

RÉSULTAT ATTENDU
- Add(3, 4) donne Ok(7.0), Mul(6, 7) donne Ok(42.0)
- Sub(3, 4) donne Ok(-1.0), Div(7, 2) donne Ok(3.5)
- Div(7, 0) donne Err dont le message parle de division par zéro

POUR TESTER
- appelez Div par 0.0 : le programme doit afficher l'erreur au lieu de planter
- vérifiez une division à décimal, 7 par 2 doit afficher 3.5 et non 3
- ajoutez une opération Mod : le compilateur réclame le cas manquant dans le
  match, preuve que l'énumération vous protège

INDICE
- le Result doit être traité avant affichage : if let Ok(v) = resultat ou
  resultat.unwrap_or(0.0), jamais un unwrap() risqué
""",
            "FizzBuzz": """ÉNONCÉ
- générer la suite FizzBuzz de 1 à 100 dans un Vec<String>, puis l'afficher
  dix éléments par ligne, comme au tableau
- les multiples de 3 donnent « Fizz », ceux de 5 donnent « Buzz », ceux des
  deux donnent « FizzBuzz », les autres gardent leur numéro

ÉTAPES
1. écrire une fonction fizzbuzz(n: usize) -> String
2. traiter d'abord les multiples de 15, puis de 3, puis de 5
3. construire la suite avec (1..=100).map(fizzbuzz)
4. collecter le résultat dans un Vec<String>
5. découper par paquets de dix avec chunks(10)
6. joindre chaque paquet avec join(" ") avant d'afficher

RÉSULTAT ATTENDU
- dix lignes de dix éléments, séparés par un espace
- la suite commence par 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz
- le rang 15 affiche FizzBuzz, le rang 100 affiche Buzz

POUR TESTER
- comptez les éléments du vecteur : ils doivent être exactement 100
- vérifiez les rangs 15, 30, 45 et 90 : tous affichent FizzBuzz
- testez votre fonction sur 3, 5 et 7 isolément avant de lancer la boucle

INDICE
- match (n % 3, n % 5) traite les paires de restes en une seule expression,
  sans if imbriqué ni conditions en cascade
""",
            "Lecture de fichier": """ÉNONCÉ
- lire un fichier texte et afficher ses lignes numérotées à partir de 1
- le chemin du fichier vient de la ligne de commande, après cargo run
- si le fichier est absent, afficher une erreur lisible : le programme ne
  doit jamais s'arrêter avec un panic

ÉTAPES
1. écrire fn main() -> Result<(), Box<dyn Error>>
2. récupérer le premier argument avec std::env::args()
3. lire le contenu avec fs::read_to_string(chemin)?
4. parcourir texte.lines().enumerate()
5. afficher chaque ligne au format numéro deux-points texte
6. lancer avec cargo run -- nom-du-fichier.txt

RÉSULTAT ATTENDU
- un fichier de 3 lignes affiche exactement 3 lignes numérotées de 1 à 3
- un chemin absent affiche une erreur contenant ce chemin, avec un code de
  sortie non nul et aucune trace de panique

POUR TESTER
- testez avec un fichier existant puis avec un chemin inventé : les deux
  exécutions doivent se terminer proprement
- insérez une ligne vide au milieu : elle doit apparaître avec son numéro
- essayez avec un dossier à la place d'un fichier : le message d'erreur doit
  rester compréhensible

INDICE
- Box<dyn Error> accepte dans un même Result des erreurs de types différents :
  c'est la signature la plus pratique pour une fonction main
""",
            "Bibliothèque": """ÉNONCÉ
- créer une bibliothèque Rust avec cargo new --lib modélisant un rayon de
  livres : la structure Livre porte un titre, un auteur et un état lu
- une structure Bibliotheque retient les livres dans un Vec et propose des
  méthodes pour en ajouter, en marquer un comme lu et lister les livres lus
- chaque méthode est couverte par des tests unitaires

ÉTAPES
1. lancer cargo new --lib ma_biblio puis ouvrir src/lib.rs
2. déclarer pub struct Livre { titre: String, auteur: String, lu: bool }
3. impl Livre : new(), marquer_lu(&mut self), resume(&self) -> String
4. struct Bibliotheque { livres: Vec<Livre> } avec ajouter et livres_lus
5. écrire les tests dans #[cfg(test)] mod tests avec use super::*
6. exécuter cargo test

RÉSULTAT ATTENDU
- cargo test affiche au moins trois tests réussis
- livres_lus ne retourne que les livres dont l'état lu vaut vrai
- resume contient à la fois le titre et l'auteur du livre

POUR TESTER
- ajoutez un test qui marque un livre comme lu puis le retrouve dans
  livres_lus : il doit passer en vert
- cassez volontairement une assertion : un test doit passer en échec, preuve
  que les tests s'exécutent réellement
- vérifiez cargo doc --no-deps sans erreur

INDICE
- les tests vivent dans #[cfg(test)] mod tests ; super::* importe tout le
  module parent, y compris ce qui est privé
""",
            "Itérateur personnel": """ÉNONCÉ
- implémenter un itérateur Fibonacci personnel : une structure Fib qui
  produit le nombre suivant à chaque appel de next
- l'utiliser comme un itérateur standard : take, sum, collect, boucle for
- la suite commence par 0 et 1 et ne s'arrête jamais d'elle-même

ÉTAPES
1. struct Fib { a: u64, b: u64 }
2. impl Iterator for Fib avec type Item = u64 et fn next(&mut self)
3. à chaque appel, avancer les valeurs (a, b) = (b, a + b) et rendre l'ancien a
4. construire Fib { a: 0, b: 1 } comme point de départ
5. extraire les dix premiers termes avec take(10)
6. sommer avec sum::<u64>() et collecter un vecteur pour l'affichage

RÉSULTAT ATTENDU
- les dix premiers termes valent 0 1 1 2 3 5 8 13 21 34
- la somme de ces dix termes vaut 88
- collect::<Vec<_>>() renvoie un vecteur de dix éléments

POUR TESTER
- prenez vingt termes : la suite doit continuer et rester strictement
  croissante à partir du troisième terme
- affichez le septième terme et vérifiez-le à la main
- poussez jusqu'à la capacité de u64 : en mode debug, Rust signale le
  débordement au lieu de produire un nombre faux

INDICE
- next() renvoie Option<u64> : Some(valeur) pour continuer, None pour dire
  que la suite est terminée
""",
            "Analyse de texte": """ÉNONCÉ
- analyser un texte multi-lignes : nombre total de mots, mot le plus fréquent
  avec son nombre d'occurrences, et ligne la plus longue
- le texte est lu dans un fichier ou déclaré en constante, sans interaction
- les trois résultats s'affichent sur une seule ligne facile à relire

ÉTAPES
1. découper les mots avec texte.split_whitespace()
2. compter avec une HashMap<&str, usize> et entry().or_insert(0)
3. trouver le mot le plus fréquent avec max_by_key
4. découper les lignes avec texte.lines()
5. choisir la plus longue avec lines().max_by_key(|l| l.len())
6. afficher les trois résultats avec println!

RÉSULTAT ATTENDU
- pour un exemple donné : 42 mots, mot le plus fréquent « le » avec 7
  occurrences, puis la ligne la plus longue affichée en entier
- la ponctuation collée au mot ne crée pas un mot supplémentaire

POUR TESTER
- testez un texte d'une seule ligne : les trois résultats doivent rester
  cohérents, la ligne la plus longue étant cette unique ligne
- testez un texte vide : le programme affiche 0 mot sans paniquer
- comparez le total de mots avec celui donné par votre éditeur de texte

INDICE
- les itérateurs se chaînent : lines().map(str::trim).filter(|l| !l.is_empty())
  ignore les lignes blanches avant la mesure
""",
        },
    },
    "SQL": {
        "lessons": {
            "SELECT et WHERE": """OBJECTIFS
- sélectionner des colonnes et filtrer des lignes
- trier et limiter les résultats
- manipuler les expressions simples et les alias

POINTS CLÉS
- SELECT colonnes FROM table WHERE condition ORDER BY ... LIMIT n
- opérateurs : = <> < > <= >=, BETWEEN, LIKE, IN, IS NULL
- ORDER BY colonne ASC par défaut, DESC pour l'ordre décroissant
- alias : SELECT prix AS p, utile pour une colonne de calcul
- les textes se délimitent par des apostrophes, les chiffres non
- DISTINCT élimine les doublons sur les colonnes retenues

EXEMPLE
SELECT nom, prix
FROM produits
WHERE prix BETWEEN 10 AND 50
  AND categorie IN ('outils', 'livres')
ORDER BY prix DESC
LIMIT 10;

EN PRATIQUE
Toute application avec un catalogue, un journal ou un tableau de bord écrit
ce genre de requête : filtre par date, tri par pertinence, page de résultats.
C'est la première chose à valider avant d'ajouter une jointure.

PIÈGES À ÉVITER
- WHERE prix < 10 OR 100 : sur certains SGBD, 100 vaut vrai et tout passe,
  écrivez BETWEEN 10 AND 100
- WHERE nom = null ne fonctionne jamais : écrivez IS NULL
- ORDER BY et LIMIT se placent après WHERE, pas avant

À RETENIR
- LIKE 'a%' cherche ce qui commence par a, % signifiant n'importe quoi
- le tri s'applique avant la coupe : ORDER BY puis LIMIT
- testez la condition en SELECT d'abord, la colonne ensuite
""",
            "Jointures": """OBJECTIFS
- relier plusieurs tables avec JOIN
- distinguer INNER, LEFT, RIGHT et FULL
- éviter les doublons et les lignes orphelines

POINTS CLÉS
- INNER JOIN : seulement les correspondances des deux côtés
- LEFT JOIN : tout le côté gauche, même sans correspondance à droite
- ON précise la clé de liaison ; WHERE filtre après la jointure
- alias obligatoires quand une table revient deux fois (auto-jointure)
- une colonne de droite qui vaut NULL signale une absence
- JOIN seul équivaut à INNER JOIN

EXEMPLE
SELECT c.nom, COUNT(*) AS commandes
FROM clients c
JOIN commandes cm ON cm.client_id = c.id
GROUP BY c.nom;

SELECT c.nom, cm.id
FROM clients c
LEFT JOIN commandes cm ON cm.client_id = c.id;

EN PRATIQUE
Une fiche client affiche ses commandes, un produit ses avis : chaque écran
combine deux tables. LEFT JOIN sert quand la présence n'est pas garantie,
comme un client sans aucune commande.

PIÈGES À ÉVITER
- oublier ON : le moteur produit un cartésien et renvoie des millions de lignes
- filtrer une colonne de droite dans WHERE après un LEFT JOIN : la jointure
  redevient INNER, placez ce filtre dans ON

À RETENIR
- INNER pour l'intersection, LEFT pour conserver tout le côté gauche
- COUNT(*) compte les lignes réelles, y compris celles complétées à droite
- toujours écrire ON avant de penser à WHERE
""",
            "Agrégats": """OBJECTIFS
- résumer avec COUNT, SUM, AVG, MIN, MAX
- regrouper avec GROUP BY
- filtrer les groupes avec HAVING

POINTS CLÉS
- GROUP BY regroupe les lignes avant de les agréger
- HAVING filtre APRÈS agrégation, WHERE filtre avant
- COUNT(*) compte les lignes, COUNT(colonne) ignore les NULL
- toute colonne non agrégée doit figurer dans GROUP BY
- ROUND(AVG(prix), 2) arrondit le résultat à deux décimales
- MIN et MAX marchent aussi sur les textes, en ordre alphabétique

EXEMPLE
SELECT categorie, ROUND(AVG(prix), 2) AS prix_moyen, COUNT(*)
FROM produits
GROUP BY categorie
HAVING COUNT(*) >= 3
ORDER BY prix_moyen DESC;

EN PRATIQUE
Un tableau de bord affiche le chiffre d'affaires par mois, le panier moyen
par magasin ou le nombre d'incidents par service : une ligne par groupe,
une colonne par mesure.

PIÈGES À ÉVITER
- WHERE AVG(prix) > 20 : l'agrégat n'existe pas encore, utilisez HAVING
- oublier GROUP BY : les moteurs exigeants refusent la colonne libre

À RETENIR
- WHERE sur les lignes, HAVING sur les groupes : l'ordre est fixe
- AVG ignore les NULL, tout comme COUNT(colonne)
- un agrégat résume : la sortie compte exactement une ligne par groupe
""",
            "Sous-requêtes": """OBJECTIFS
- imbriquer une requête dans une autre
- utiliser IN, EXISTS et la comparaison scalaire
- savoir quand une sous-requête corrélée coûte cher

POINTS CLÉS
- WHERE prix > (SELECT AVG(prix) FROM produits) : comparaison scalaire
- IN (SELECT ...) pour une liste calculée à la volée
- EXISTS s'arrête dès le premier résultat trouvé
- NOT IN se trompe dès qu'une valeur vaut NULL, préférez NOT EXISTS
- sous-requête corrélée : elle référence la ligne externe, exécutée par ligne

EXEMPLE
SELECT nom FROM clients c
WHERE EXISTS (
  SELECT 1 FROM commandes cm
  WHERE cm.client_id = c.id AND cm.montant > 1000
);

EN PRATIQUE
« Les produits jamais commandés » ou « les clients au-dessus de la moyenne »
demandent une valeur calculée avant le filtre : la sous-requête la produit,
la requête externe l'utilise.

PIÈGES À ÉVITER
- imbriquer sans avoir testé la sous-requête seule : le message d'erreur
  porte alors sur toute la phrase
- NOT IN avec une sous-requête contenant NULL : zéro ligne, sans erreur

À RETENIR
- écrivez d'abord la sous-requête, puis entourez-la de la requête externe
- une sous-requête corrélée s'exécute par ligne : pensez à l'index
""",
            "Vues et index": """OBJECTIFS
- créer des vues pour réutiliser une requête
- accélérer les recherches avec des index
- mesurer l'effet avec EXPLAIN

POINTS CLÉS
- CREATE VIEW v AS SELECT ... puis SELECT * FROM v, comme une table
- vue matérialisée : résultat stocké, à rafraîchir (selon le SGBD)
- CREATE INDEX idx ON table(colonne) accélère filtres et jointures
- l'index utile porte sur les clés de jointure et les colonnes filtrées
- DROP VIEW ou DROP INDEX retirent l'objet créé

EXEMPLE
CREATE VIEW ventes_par_mois AS
SELECT DATE_FORMAT(date, '%Y-%m') AS mois, SUM(total) AS total
FROM commandes GROUP BY mois;

EXPLAIN SELECT * FROM commandes WHERE client_id = 7;

EN PRATIQUE
Une vue porte un rapport partagé par toute l'équipe : la requête complexe
s'écrit une fois. L'index, lui, se pose sur les colonnes que WHERE et JOIN
utilisent le plus souvent.

PIÈGES À ÉVITER
- indexer toutes les colonnes : les insertions ralentissent sans gain
- indexer une expression, YEAR(date) par exemple : la colonne brute reste
  seule exploitable, filtrez directement sur elle

À RETENIR
- trop d'index pèse sur les écritures : visez la lecture la plus fréquente
- EXPLAIN avant et après pour mesurer, jamais à l'aveugle
""",
            "Manipulation": """OBJECTIFS
- insérer, mettre à jour et supprimer des lignes
- gérer les clés auto-incrémentées
- travailler dans une transaction

POINTS CLÉS
- INSERT INTO t (col1, col2) VALUES (v1, v2), plusieurs lignes à la suite
- UPDATE t SET col = v WHERE id = 5
- DELETE FROM t WHERE ... ; sans WHERE, toute la table part
- transaction : BEGIN, COMMIT, ROLLBACK pour des écritures groupées
- le nombre de lignes touchées indique si l'écriture a bien agi

EXEMPLE
BEGIN;
UPDATE comptes SET solde = solde - 100 WHERE id = 1;
UPDATE comptes SET solde = solde + 100 WHERE id = 2;
COMMIT;

INSERT INTO produits (nom, prix) VALUES ('Cable', 9.9);
DELETE FROM produits WHERE prix < 1;

EN PRATIQUE
Un virement, une commande annulée, un stock décrémenté : chaque écriture
importante passe par une transaction pour ne jamais garder la moitié d'une
opération en base.

PIÈGES À ÉVITER
- UPDATE sans WHERE : toute la table prend la même valeur, testez d'abord
  avec SELECT en changeant seulement le mot clé
- oublier COMMIT : la session suivante ne voit pas l'écriture

À RETENIR
- tester TOUJOURS une UPDATE ou un DELETE en SELECT avant
- BEGIN puis COMMIT : rien n'est définitif tant que tout n'a pas réussi
""",
            "Modélisation": """OBJECTIFS
- concevoir un schéma relationnel normalisé
- choisir clés primaires et clés étrangères
- poser contraintes et index au bon endroit

POINTS CLÉS
- 1NF : plus de colonnes composées ; 2NF/3NF : pas de dépendance partielle
- clé primaire unique, clé étrangère qui référence une clé primaire
- contraintes : NOT NULL, UNIQUE, FOREIGN KEY, CHECK
- table de jonction pour une relation plusieurs à plusieurs
- nommer les tables au pluriel et les clés id, pour toute l'équipe

EXEMPLE
CREATE TABLE produits (
  id INTEGER PRIMARY KEY,
  nom TEXT NOT NULL,
  prix NUMERIC(10,2) CHECK (prix >= 0)
);

CREATE TABLE commandes_produits (
  commande_id INTEGER REFERENCES commandes(id),
  produit_id INTEGER REFERENCES produits(id),
  quantite INTEGER NOT NULL CHECK (quantite > 0)
);

EN PRATIQUE
Un magasin sépare produits, commandes et lignes de commande : chaque entité
devient une table, chaque relation une clé étrangère. Le schéma se dessine
sur le papier avant le premier CREATE TABLE.

PIÈGES À ÉVITER
- stocker une liste de produits dans un texte : impossible à filtrer, à
  compter et à indexer proprement
- une clé étrangère sans index : les jointures ralentissent

À RETENIR
- normaliser d'abord, dénormaliser ensuite seulement si c'est mesuré
- une contrainte posée en base protège mieux qu'un contrôle dans le code
""",
        },
        "exercises": {
            "Créer un schéma": """ÉNONCÉ
- concevoir la base d'une librairie avec trois tables : auteurs, livres et
  emprunts, reliées entre elles par des clés étrangères
- poser les contraintes qui empêchent les données incohérentes : noms
  obligatoires, années plausibles, dates de prêt qui se suivent

ÉTAPES
1. CREATE TABLE auteurs (id INTEGER PRIMARY KEY, nom TEXT NOT NULL)
2. CREATE TABLE livres avec titre NOT NULL, annee et auteur_id référençant auteurs
3. CREATE TABLE emprunts avec livre_id référençant livres, date_emprunt, date_retour
4. ajouter des CHECK pour l'année et l'ordre des deux dates
5. créer un index sur chaque clé étrangère
6. insérer un auteur, deux livres et un emprunt pour vérifier

RÉSULTAT ATTENDU
- les trois tables existent et apparaissent dans la liste des tables
- l'insertion d'un livre dont l'auteur_id est inconnu est refusée
- un emprunt pointant vers un livre absent est refusé également

POUR TESTER
- tentez l'insertion invalide : le moteur doit répondre par une erreur de clé
  étrangère, pas par un message incompréhensible
- essayez de supprimer un auteur qui possède des livres : cela doit être refusé
- inspectez le schéma avec .schema en SQLite ou SHOW CREATE TABLE

INDICE
- id INTEGER PRIMARY KEY AUTOINCREMENT donne une clé simple auto-incrémentée
""",
            "Clients actifs": """ÉNONCÉ
- lister les clients ayant passé au moins 3 commandes dans les 6 derniers
  mois, avec pour chacun le nombre de commandes et le montant total cumulé
- le classement va du client le plus important au moins important

ÉTAPES
1. filtrer les commandes récentes avec WHERE date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
2. regrouper par identifiant avec GROUP BY client_id
3. poser le seuil avec HAVING COUNT(*) >= 3
4. joindre la table clients pour afficher le nom, avec JOIN
5. agréger les montants avec SUM(total) AS total
6. trier avec ORDER BY total DESC

RÉSULTAT ATTENDU
- une ligne par client éligible, contenant nom, nombre de commandes et total
- les lignes sont classées du montant décroissant au plus petit
- un client ayant seulement 2 commandes n'apparaît pas dans la liste

POUR TESTER
- comparez le nombre de lignes rendues avec un décompte fait à la main
- relevez le seuil à 5 : la liste doit se restreindre
- vérifiez qu'aucun nom n'est dupliqué et qu'aucun client absent ne traîne

INDICE
- la date appartient à WHERE, le seuil de nombre appartient à HAVING : ces
  deux filtres ne se remplacent pas
""",
            "Top des ventes": """ÉNONCÉ
- pour chaque catégorie de produits, afficher le produit le plus vendu avec
  sa quantité totale, en ignorant les produits jamais vendus
- une seule ligne doit sortir par catégorie, même en cas d'égalité

ÉTAPES
1. agréger les ventes : SUM(quantite) AS total GROUP BY produit_id
2. joindre la table produits pour le nom du produit
3. joindre ensuite la table categories pour le nom de catégorie
4. classer avec ROW_NUMBER() OVER (PARTITION BY categorie ORDER BY total DESC)
5. donner un alias à cette fenêtre via une sous-requête ou une CTE WITH
6. ne garder que les lignes de rang 1 puis trier par catégorie

RÉSULTAT ATTENDU
- une ligne par catégorie, avec le nom du produit et sa quantité vendue
- aucune catégorie vide ni aucun produit jamais vendu n'apparaît

POUR TESTER
- vérifiez qu'une catégorie ne comptant qu'un seul produit le rend bien
- comparez la quantité affichée avec un SELECT SUM fait à part sur ce produit
- ajoutez une vente fictive importante : le produit tête de liste doit changer

INDICE
- la fenêtre s'écrit ROW_NUMBER() OVER (PARTITION BY categorie ORDER BY
  total DESC) et une CTE WITH ventes AS (...) rend la lecture plus simple
""",
            "Rapport mensuel": """ÉNONCÉ
- produire le rapport annuel : chiffre d'affaires mois par mois, nombre de
  commandes et panier moyen, de janvier à décembre
- les mois sans commande doivent apparaître avec des zéros et non être absents

ÉTAPES
1. regrouper avec GROUP BY YEAR(date), MONTH(date)
2. agréger SUM(total) AS ca, COUNT(*) AS commandes, AVG(total) AS panier
3. fabriquer un calendrier de 12 mois, table de dates ou requête récursive
4. LEFT JOIN les commandes sur ce calendrier
5. remplacer les vides avec COALESCE(SUM(total), 0)
6. trier avec ORDER BY mois

RÉSULTAT ATTENDU
- 12 lignes, de janvier à décembre, chacune avec CA, commandes et panier moyen
- les mois vides affichent 0 pour le CA et 0 pour le nombre de commandes
- le panier moyen vaut CA divisé par nombre de commandes

POUR TESTER
- additionnez les CA mensuels : le total doit égaler le CA de l'année entière
- comparez le nombre total de commandes avec un COUNT(*) sans GROUP BY
- vérifiez qu'aucun mois ne manque et qu'aucun n'est dupliqué

INDICE
- AVG ignore les lignes NULL : contrôlez que la colonne total est bien remplie
""",
            "Transaction": """ÉNONCÉ
- réaliser un virement bancaire atomique : débiter le compte 1 de 500 et
  créditer le compte 2 de la même somme
- si l'une des deux écritures échoue, aucune ne s'applique : jamais de
  transfert à moitié appliqué

ÉTAPES
1. ouvrir la transaction avec BEGIN
2. UPDATE comptes SET solde = solde - 500 WHERE id = 1 AND solde >= 500
3. vérifier que 1 ligne a été touchée, sinon ROLLBACK immédiat
4. UPDATE comptes SET solde = solde + 500 WHERE id = 2
5. vérifier à nouveau puis conclure par COMMIT
6. relire les deux soldes pour contrôle

RÉSULTAT ATTENDU
- la somme des deux soldes est identique avant et après le virement
- un compte sans solde suffisant laisse la base intacte, sans débit partiel
- le compte 1 perd exactement 500, le compte 2 en gagne 500

POUR TESTER
- relevez les deux soldes avant et après : les écarts doivent être -500 et +500
- testez avec un solde insuffisant : rien ne doit changer du tout
- commentez le COMMIT puis relisez les soldes : ils doivent être revenus à
  leur valeur initiale

INDICE
- le solde suffisant se teste dans le WHERE (solde >= 500), pas dans le
  langage applicatif après coup
""",
            "Vue de rapport": """ÉNONCÉ
- créer une vue Produits_ventes qui, pour chaque produit, donne la quantité
  vendue et le chiffre d'affaires correspondant
- ensuite interroger la vue comme une table, pour classer les produits par
  chiffre d'affaires décroissant

ÉTAPES
1. CREATE VIEW Produits_ventes AS SELECT p.nom, SUM(l.quantite),
   SUM(l.prix_unitaire * l.quantite) AS ca
2. FROM lignes l JOIN produits p ON p.id = l.produit_id
3. GROUP BY p.nom
4. SELECT * FROM Produits_ventes ORDER BY ca DESC
5. réutiliser la vue dans une seconde requête filtrée par un WHERE
6. DROP VIEW Produits_ventes si la vue doit être corrigée ou retirée

RÉSULTAT ATTENDU
- la vue existe et répond à des requêtes simples, comme une table
- chaque ligne contient un produit, sa quantité totale et son CA
- le classement par CA décroissant part du premier produit

POUR TESTER
- interrogez la vue puis la requête complète équivalente : les deux
  résultats doivent être identiques ligne à ligne
- additionnez le CA de la vue : il doit égaler le total de la table des lignes
- essayez d'insérer dans la vue : le SGBD refuse, ou répercute l'opération
  sur la table de base

INDICE
- DROP VIEW puis CREATE VIEW permet de corriger la définition proprement
""",
            "Requête lente": """ÉNONCÉ
- diagnostiquer une requête lente avec EXPLAIN et la corriger, soit par un
  index adapté, soit par une réécriture plus simple
- le gain doit être mesuré avant et après, puis noté pour l'équipe

ÉTAPES
1. chronométrer la requête d'origine avec EXPLAIN ANALYZE
2. repérer un full table scan ou un tri coûteux dans le plan affiché
3. créer l'index sur la colonne filtrée ou la clé de jointure
4. relancer la mesure et comparer les deux durées
5. si l'index ne change rien, réécrire la sous-requête en JOIN
6. conserver le plan obtenu avec la nouvelle durée

RÉSULTAT ATTENDU
- le plan d'exécution montre un accès par index au lieu d'une lecture complète
- le temps d'exécution baisse de façon nette et mesurable
- les résultats renvoyés restent strictement identiques

POUR TESTER
- comparez EXPLAIN avant et après : le type d'accès doit avoir changé
- ajoutez des lignes dans la table puis relancez : l'écart doit grandir
- comparez les deux jeux de résultats, ligne à ligne, pour rester tranquille

INDICE
- une fonction sur la colonne filtrée, YEAR(date) = 2026 par exemple, empêche
  l'usage de l'index : filtrez sur la colonne brute
""",
        },
    },
}
