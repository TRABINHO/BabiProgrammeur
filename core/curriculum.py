"""Parcours prédéfini de BabiProgrammeur : cours et exercices par langage.

Contenu déclaratif (titres + résumés courts) pour chaque langage de
``LANGUAGES``. L'avancement de l'utilisateur ne vit pas ici mais dans le
stockage (``SessionStore.learning``) ; les identifiants d'éléments sont
dérivés des titres (slug), stables tant que les listes ci-dessous ne sont
pas réécrites (ajouts en fin de liste sans effet sur l'existant).
"""
from __future__ import annotations

import re
import unicodedata
from typing import Dict, List, Tuple

# (titre, résumé court affiché sous le titre)
Item = Tuple[str, str]

LANGUAGES: List[str] = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
    "SQL", "HTML/CSS", "PHP", "Swift", "Kotlin", "Flutter", "Autre",
]

CURRICULUM: Dict[str, Dict[str, List[Item]]] = {
    "Python": {
        "lessons": [
            ("Variables et types", "Nombres, chaînes, booléens, conversions"),
            ("Conditions", "if / elif / else et opérateurs"),
            ("Boucles", "for, while, break et continue"),
            ("Fonctions", "Paramètres, retour, portée des variables"),
            ("Listes et dictionnaires", "Parcours et compréhensions"),
            ("Fichiers", "Lecture et écriture avec open()"),
            ("Erreurs", "try / except et exceptions"),
            ("Modules et paquets", "import, pip, bibliothèque standard"),
        ],
        "exercises": [
            ("Salut le monde", "Afficher un message à l'écran"),
            ("Calculatrice", "Les quatre opérations en console"),
            ("FizzBuzz", "Multiples de 3, de 5 et de 15"),
            ("Moyenne d'une liste", "Somme divisée par la longueur"),
            ("Compteur de mots", "Occurrences d'un mot dans un texte"),
            ("Convertisseur", "Celsius ↔ Fahrenheit"),
            ("Nombre mystère", "Deviner un nombre avec indices"),
        ],
    },
    "JavaScript": {
        "lessons": [
            ("Variables et portée", "let, const et la portée des blocs"),
            ("Conditions et boucles", "if, switch, for, forEach"),
            ("Fonctions", "Function, flèche, paramètres par défaut"),
            ("Tableaux et objets", "map, filter, reduce, décomposition"),
            ("Le DOM", "Sélection, événements, modification"),
            ("Asynchrone", "Promesses, async / await, fetch"),
            ("Modules", "import / export et organisation"),
        ],
        "exercises": [
            ("Message d'accueil", "Afficher du texte dans la page"),
            ("Compteur de clics", "Bouton +1 avec gestion d'événement"),
            ("FizzBuzz", "Version JavaScript du classique"),
            ("Statistiques de notes", "Min, max, moyenne d'un tableau"),
            ("Liste de tâches", "Ajouter et supprimer des éléments"),
            ("Recherche produit", "Filtrer un tableau d'objets"),
            ("Mini-jeu", "Devinette avec essais limités"),
        ],
    },
    "TypeScript": {
        "lessons": [
            ("Types de base", "string, number, boolean, tableaux"),
            ("Interfaces et objets", "Formes de données et littéraux"),
            ("Fonctions typées", "Paramètres, retour, surcharges"),
            ("Union et réduction", "Unions discriminées, narrowing"),
            ("Génériques", "Réutiliser un type avec paramètre"),
            ("Classes et visibilité", "readonly, private, implements"),
            ("Modules de types", "import, export, tsconfig"),
        ],
        "exercises": [
            ("Typer une fonction", "Ajouter des types à du JavaScript"),
            ("Profil utilisateur", "Modéliser un objet avec interface"),
            ("Convertisseur JSON", "Transformer et valider des données"),
            ("Cache générique", "Une Map<K, V> typée"),
            ("États d'une commande", "Union de statuts sans if imbriqués"),
            ("Corriger un bug", "Résoudre une erreur de compilation"),
            ("Réponse d'API", "Typer un objet JSON distant"),
        ],
    },
    "Java": {
        "lessons": [
            ("Classes et objets", "Champs, méthodes, constructeur"),
            ("Héritage", "extends, override, polymorphisme"),
            ("Interfaces", "Contrats et méthodes par défaut"),
            ("Collections", "List, Set, Map et parcours"),
            ("Génériques", "Classes et méthodes paramétrées"),
            ("Entrées / sorties", "Fichiers, lecteurs et flux"),
            ("Exceptions", "try / catch, exceptions vérifiées"),
        ],
        "exercises": [
            ("Affichage console", "Premier programme avec main"),
            ("Calculatrice", "Classe avec méthode calculer()"),
            ("Compte bancaire", "Dépôt, retrait, solde"),
            ("Gestion de notes", "Moyenne et mention d'une classe"),
            ("Lire un CSV", "Parser un fichier avec BufferedReader"),
            ("Compteur de mots", "HashMap des occurrences"),
            ("Tri personnalisé", "Comparator sur une liste d'objets"),
        ],
    },
    "C++": {
        "lessons": [
            ("Types et variables", "int, float, string, const"),
            ("Conditions et boucles", "if, switch, for, while"),
            ("Fonctions", "Paramètres, surcharge, portée"),
            ("Pointeurs et mémoire", "*, &, new / delete"),
            ("Classes et objets", "Constructeurs, méthodes, encapsulation"),
            ("Héritage et virtuel", "Classes dérivées, méthodes virtuelles"),
            ("STL", "vector, map et algorithmes"),
            ("Templates", "Fonctions et classes génériques"),
        ],
        "exercises": [
            ("Bonjour C++", "Premier programme compilé"),
            ("Calculatrice", "Surcharge des opérateurs"),
            ("Tableau trié", "Tri à bulles sur un tableau"),
            ("Compteur de mots", "std::map et flux d'entrée"),
            ("Classe Rectangle", "Aire, périmètre, constructeur"),
            ("Fibonacci récursif", "Récursion et profondeur"),
            ("Devinette console", "Boucle avec indices"),
        ],
    },
    "C#": {
        "lessons": [
            ("Types et variables", "var, string, types nullable"),
            ("Conditions et boucles", "if, expression switch, foreach"),
            ("Fonctions", "Paramètres out / ref, valeurs par défaut"),
            ("Classes et objets", "Propriétés, constructeurs, static"),
            ("Collections", "List<T>, Dictionary<K, V>"),
            ("Héritage et interfaces", "override, implémentation"),
            ("LINQ", "Where, Select, OrderBy"),
        ],
        "exercises": [
            ("Console .NET", "Premier programme SDK"),
            ("Calculatrice", "Classe d'opérations"),
            ("Liste de courses", "Ajout, suppression, persistance"),
            ("Gestion d'étudiants", "Moyennes avec LINQ"),
            ("Sérialiser JSON", "System.Text.Json"),
            ("FizzBuzz", "Version C# idiomatique"),
            ("Compte bancaire", "Encapsulation et validation"),
        ],
    },
    "Go": {
        "lessons": [
            ("Variables et types", "var, :=, const, valeurs zéro"),
            ("Structures et méthodes", "struct, receivers, tags"),
            ("Fonctions et erreurs", "Retours multiples, error"),
            ("Slices et maps", "make, append, itération"),
            ("Interfaces", "Résolution implicite"),
            ("Goroutines et channels", "concurrence, select"),
            ("Packages et modules", "go mod, visibilité"),
        ],
        "exercises": [
            ("Bonjour Go", "go run avec un package main"),
            ("Convertisseur", "Gestion des drapeaux de commande"),
            ("Compteur de mots", "maps et strings.Fields"),
            ("Liste de tâches", "struct + méthodes"),
            ("Serveur HTTP", "net/http et handlers"),
            ("Pool de workers", "goroutines + WaitGroup"),
            ("Dépenses CSV", "encoding/csv"),
        ],
    },
    "Rust": {
        "lessons": [
            ("Variables et mutabilité", "let, shadowing, const"),
            ("Ownership", "move, emprunts, durées de vie (intro)"),
            ("Structures et énumérés", "struct, enum, match"),
            ("Traits", "impl, dérivation, dyn"),
            ("Result et erreurs", "?, Option, panic"),
            ("Collections", "Vec, HashMap, itérateurs"),
            ("Modules et crates", "mod, Cargo, dépendances"),
        ],
        "exercises": [
            ("Bonjour cargo", "cargo new puis cargo run"),
            ("Calculatrice", "match sur un enum Opération"),
            ("FizzBuzz", "Itérateurs et format!"),
            ("Lecture de fichier", "fs + Result + ?"),
            ("Bibliothèque", "struct Livre + affichage Display"),
            ("Itérateur personnel", "impl Iterator sur un type"),
            ("Analyse de texte", "Compte de mots avec HashMap"),
        ],
    },
    "SQL": {
        "lessons": [
            ("SELECT et WHERE", "Filtrer, trier, LIMIT"),
            ("Jointures", "INNER, LEFT, alias de tables"),
            ("Agrégats", "COUNT, SUM, GROUP BY"),
            ("Sous-requêtes", "IN, EXISTS, requêtes dérivées"),
            ("Vues et index", "CREATE VIEW, CREATE INDEX"),
            ("Manipulation", "INSERT, UPDATE, DELETE"),
            ("Modélisation", "Clés, cardinalités, schéma"),
        ],
        "exercises": [
            ("Créer un schéma", "Tables d'une boutique en ligne"),
            ("Clients actifs", "Jointure + filtre sur la date"),
            ("Top des ventes", "GROUP BY + ORDER BY"),
            ("Rapport mensuel", "Agrégats + CASE"),
            ("Transaction", "BEGIN, COMMIT, rollback"),
            ("Vue de rapport", "CREATE VIEW réutilisable"),
            ("Requête lente", "EXPLAIN et optimisation"),
        ],
    },
    "HTML/CSS": {
        "lessons": [
            ("Structure HTML", "head, body, sémantique"),
            ("Texte et liens", "Titres, paragraphes, ancres"),
            ("Images et médias", "img, video, attributs"),
            ("Formulaires", "input, labels, validation native"),
            ("Sélecteurs et cascade", "Spécificité, héritage"),
            ("Flexbox", "Alignement en lignes et colonnes"),
            ("Grid", "Grilles, areas, gap"),
            ("Responsive", "Media queries, unités relatives"),
        ],
        "exercises": [
            ("Page CV", "Structure complète en HTML"),
            ("Menu responsive", "Barre de navigation adaptative"),
            ("Galerie en grille", "Mise en page CSS Grid"),
            ("Formulaire contact", "Validation côté navigateur"),
            ("Carte produit", "flex + ombres + arrondis"),
            ("Section hero", "Dégradé et typographie"),
            ("Thème sombre", "Variables CSS + prefers-color-scheme"),
        ],
    },
    "PHP": {
        "lessons": [
            ("Syntaxe et variables", "$var, écho, types"),
            ("Conditions et boucles", "if, switch, foreach"),
            ("Tableaux", "Indexés, associatifs, parcours"),
            ("Fonctions", "Paramètres, portée, return"),
            ("Formulaires", "GET, POST, assainissement"),
            ("Bases de données", "PDO, requêtes préparées"),
            ("Sessions et cookies", "session_start, authentification"),
        ],
        "exercises": [
            ("Première page", "php -S localhost:8000"),
            ("Calculatrice web", "Formulaire + résultats"),
            ("Validation d'inscription", "Contrôles côté serveur"),
            ("Mini CMS", "Articles gardés en mémoire"),
            ("Compteur de visiteurs", "Fichier ou session"),
            ("Lecture JSON", "json_decode et parcours"),
            ("Connexion PDO", "Connexion simple"),
        ],
    },
    "Swift": {
        "lessons": [
            ("Variables et optionnels", "var / let, ?, guard"),
            ("Conditions et boucles", "if, switch, for-in"),
            ("Fonctions", "Paramètres, tuples, retours"),
            ("Structures et classes", "Valeur vs référence, init"),
            ("Tableaux et dictionnaires", "map, filter, reduce"),
            ("Protocoles", "protocol, conformité, extensions"),
            ("Erreurs", "throws, do / catch"),
        ],
        "exercises": [
            ("Premier playground", "Premiers pas en Swift"),
            ("Convertisseur", "struct + fonction pure"),
            ("Compteur pas à pas", "struct avec méthode mutating"),
            ("FizzBuzz", "switch et chemins multiples"),
            ("Compte bancaire", "classe et références"),
            ("Décodage JSON", "protocole Codable"),
            ("Tri de personnes", "sorted et closures"),
        ],
    },
    "Kotlin": {
        "lessons": [
            ("val et var", "Types, inférence, constantes"),
            ("Conditions et boucles", "if expression, when, ranges"),
            ("Fonctions", "Arguments nommés, corps expression"),
            ("Nullabilité", "?, !!, opérateur elvis"),
            ("Classes et data class", "Constructeur primaire, copy"),
            ("Collections", "listOf, map, filter, sumBy"),
            ("Coroutines", "launch, suspend, Dispatchers"),
        ],
        "exercises": [
            ("Bonjour main", "fun main() et println"),
            ("Calculatrice", "when comme expression"),
            ("Liste de tâches", "data class + liste mutable"),
            ("FizzBuzz", "Règles de progression"),
            ("Statistiques", "Fonctions d'agrégation"),
            ("Extension utile", "String avec une extension"),
            ("Compteur asynchrone", "Job, delay, scope"),
        ],
    },
    "Flutter": {
        "lessons": [
            ("Dart pour Flutter", "Types, fonctions, async en bref"),
            ("Widgets et arbre", "StatelessWidget, StatefulWidget, composition"),
            ("Mise en page", "Row, Column, Stack, Expanded"),
            ("Gestion d'état", "setState et cycle de vie du State"),
            ("Boutons et champs", "TextField, GestureDetector, validation"),
            ("Listes défilantes", "ListView, éléments dynamiques"),
            ("Navigation", "Navigator, routes, arguments"),
            ("Réseau et données", "http, JSON, Future / await"),
        ],
        "exercises": [
            ("Bonjour Flutter", "Compteur par défaut à personnaliser"),
            ("Compteur de clics", "ElevatedButton + setState"),
            ("Liste de tâches", "ListView + ajout / suppression"),
            ("Convertisseur", "Celsius ↔ Fahrenheit avec champs"),
            ("Quiz", "Questions, score, écran de résultat"),
            ("Fil d'actualité", "ListView.builder + images réseau"),
            ("ToDo persistant", "Sauvegarde locale JSON"),
        ],
    },
    "Autre": {
        "lessons": [
            ("Mise en place", "Éditeur, compilateur / interpréteur"),
            ("Syntaxe de base", "Commentaires, ponctuation"),
            ("Variables et types", "Déclaration et conversions"),
            ("Contrôle de flux", "Conditions et boucles"),
            ("Fonctions", "Paramètres et retour"),
            ("Structures de données", "Listes, dictionnaires, ensembles"),
            ("Gestion des erreurs", "Exceptions et cas limites"),
            ("Bonnes pratiques", "Nommage, formatage, versions"),
        ],
        "exercises": [
            ("Bonjour le monde", "Afficher un message"),
            ("Calculatrice", "Quatre opérations"),
            ("Suite numérique", "De 1 à 100 par pas de 5"),
            ("Inverser une chaîne", "Boucle ou méthode dédiée"),
            ("Compteur", "Incrément et affichage"),
            ("Lecture de fichier", "Lire et afficher un fichier"),
            ("Mini-projet", "Un petit outil personnel au choix"),
        ],
    },
}


def slugify(text: str) -> str:
    """Identifiant stable dérivé d'un titre : « Moyenne d'une liste » →
    « moyenne-d-une-liste ». Les accents sont retirés."""
    norm = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in norm if not unicodedata.combining(c))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "item"


def langs() -> List[str]:
    """Langages disposant d'un parcours (dans l'ordre d'affichage)."""
    return [name for name in LANGUAGES if name in CURRICULUM]


def has_lang(name: str) -> bool:
    return name in CURRICULUM


def items(name: str, kind: str) -> List[Tuple[str, str, str]]:
    """[(slug, titre, résumé)] pour un langage — slugs uniques dans la liste."""
    out: List[Tuple[str, str, str]] = []
    seen: Dict[str, int] = {}
    for title, desc in CURRICULUM.get(name, {}).get(kind, []):
        slug = slugify(title)
        n = seen.get(slug, 0) + 1
        seen[slug] = n
        if n > 1:
            slug = f"{slug}-{n}"
        out.append((slug, title, desc))
    return out


def total(name: str, kind: str = "") -> int:
    """Nombre d'éléments d'un langage (kind vide = cours + exercices)."""
    spec = CURRICULUM.get(name, {})
    if kind:
        return len(spec.get(kind, []))
    return sum(len(v) for v in spec.values())


def grand_total() -> int:
    """Tous les éléments de tous les langages (contrôle de cohérence)."""
    return sum(total(name) for name in CURRICULUM)
