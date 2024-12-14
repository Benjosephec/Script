# CSV-Stock Manager

**CSV-Stock Manager** est un outil en ligne de commande développé en Python pour la gestion et l'analyse des données d'inventaire à partir de fichiers CSV. Il permet de charger, rechercher, trier et résumer les données d'inventaire de manière simple et efficace.

## Prérequis

Avant d'utiliser le programme, assurez-vous que Python est installé sur votre machine.

### Dépendances

- Python 3.x
- pandas
- colorama

## Installation

Clonez le dépôt du projet ou téléchargez-le manuellement.
```bash
git clone https://github.com/VotreUtilisateur/csv-stock-manager.git
cd csv-stock-manager
```

## Utilisation

Une fois le programme installé, vous pouvez l'utiliser directement en ligne de commande. Voici les principales commandes à connaître pour interagir avec l'inventaire.

### 1. Lancer le programme

Pour démarrer l'application, exécutez simplement le script Python, ce qui vous permettra d'interagir avec le programme via la ligne de commande.
```
python main.py
```

### 2. Charger les fichiers CSV

Utilisez la commande `load` pour ajouter des fichiers CSV à l'inventaire. Le programme lira tous les fichiers CSV dans le répertoire spécifié et les fusionnera en une base de données unique.
```
load /data
```
### 3. Rechercher un produit ou une catégorie

Utilisez la commande `search` pour rechercher des produits ou des catégories dans votre inventaire. Vous pouvez effectuer des recherches par nom de produit ou par catégorie.
```
search category=Electronics
search product_name=Laptop
```

### 4. Afficher un résumé des données

La commande `summary` génère un résumé des données de l'inventaire, incluant la quantité totale et le prix moyen par catégorie. Vous pouvez également exporter ce résumé dans un fichier CSV.
```
summary
```

### 5. Afficher les premières lignes de l'inventaire

La commande `show` permet d'afficher les premières lignes de l'inventaire, pour avoir un aperçu rapide des données. Par défaut, elle affiche 5 lignes, mais vous pouvez spécifier un nombre personnalisé.
```
show 10  # Affiche les 10 premières lignes
```

### 6. Quitter le programme

Utilisez la commande `exit` pour quitter l'application.
```
exit
```

## Exemple de fichier CSV

Voici un exemple de fichier CSV pour un inventaire de produits électroniques :

```csv
product_name,quantity,unit_price,category
Laptop,10,800.0,Electronics
Smartphone,15,500.0,Electronics
Wireless Mouse,8,25.0,Electronics
```
