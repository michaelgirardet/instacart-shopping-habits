# Analyse des habitudes d'achat Instacart

Exploration du jeu de données [Instacart Market Basket Analysis](https://www.kaggle.com/c/instacart-market-basket-analysis) : profil des clients, évolution des paniers, segmentation et prédiction du réachat.

Ce dépôt est une **version portfolio** du projet pédagogique Epitech **T-DAT-600** (rendu de groupe noté 24/26). Seul le livrable final est conservé. Le projet a été réalisé avec Nadir Ammi Said et Younes Haddad.

## Présentation

L'objectif est de comprendre comment les clients utilisent le service au fil de leurs commandes. L'analyse porte notamment sur le nombre de commandes, la taille des paniers, le délai entre deux achats, le réachat des produits et les rayons les plus représentés.

Le projet répond aux questions suivantes :

- Quel est le profil habituel d'un client ?
- Combien d'articles contient un panier moyen ?
- À quel rythme les clients reviennent-ils ?
- La taille et la composition du panier évoluent-elles avec le temps ?
- Les clients fidèles rachètent-ils davantage les mêmes produits ?
- Quels sont les jours et les heures les plus actifs ?
- Les clients nouveaux et fidèles ont-ils les mêmes habitudes ?
- À partir de quel délai peut-on considérer qu'un client risque de ne plus commander ?

## Résultats principaux

Les résultats ci-dessous sont issus de l'exploration documentée dans le projet :

- un client passe typiquement 10 commandes, avec une moyenne d'environ 16,6 commandes ;
- un panier contient généralement 8 articles, pour une moyenne d'environ 10,1 articles ;
- le délai médian entre deux commandes est de 7 jours, ce qui indique un rythme hebdomadaire dominant ;
- la taille du panier reste proche de 10 articles au fil des commandes ;
- le délai moyen entre deux commandes diminue avec l'expérience, de 15,3 jours au début à 5,1 jours autour de la 50e commande ;
- la part de produits déjà connus atteint environ 53 % à la 5e commande et 82 % à la 50e ;
- les habitudes d'achat commencent à se stabiliser autour de la 15e commande ;
- les clients fidèles représentent environ 17 % des clients et 23 % du volume d'articles ;
- les 20 % de clients les plus actifs représentent environ 60 % du volume d'articles ;
- les nouveaux clients commandent le plus souvent le dimanche à 15 h, tandis que le pic des clients fidèles se situe le lundi à 10 h.

Ces chiffres doivent être interprétés en tenant compte des limites du jeu de données, notamment le plafonnement des délais à 30 jours et l'absence de prix.

## Contenu du dépôt

```text
.
├── datasets/                 # CSV locaux, non versionnés
├── exploration.ipynb         # notebook de référence
├── exploration.html          # export consultable sans Jupyter
├── requirements.txt
├── src/
│   ├── prepare_data.py
│   ├── analysis_helpers.py
│   └── ml_features.py
├── LICENSE
└── README.md
```

Le notebook [`exploration.ipynb`](exploration.ipynb) est le livrable d'analyse. La version HTML [`exploration.html`](exploration.html) permet de parcourir les graphiques et les commentaires sans installer Python.

## Données

Les CSV **ne sont pas inclus** dans ce dépôt. Ils restent soumis aux conditions d'utilisation d'Instacart / Kaggle (usage non commercial).

Source : [Instacart Market Basket Analysis](https://www.kaggle.com/c/instacart-market-basket-analysis/data) (jeu *The Instacart Online Grocery Shopping Dataset 2017*).

Après téléchargement, placer les fichiers dans `datasets/` à la racine du projet :

| Fichier | Contenu |
|---|---|
| `orders.csv` | informations générales sur les commandes et les clients |
| `products.csv` | produits, rayons et départements associés |
| `order_products.csv` | produits présents dans chaque commande |
| `aisles.csv` | liste des rayons |
| `departments.csv` | liste des départements |

Le dataset officiel sépare les articles en `order_products__prior.csv` et `order_products__train.csv`. Les concaténer en un seul `order_products.csv` (en conservant l'en-tête une seule fois) avant de lancer le notebook.

## Installation

### Prérequis

- Python 3.10 ou une version plus récente ;
- `pip` ;
- Jupyter Notebook, JupyterLab ou Visual Studio Code avec les extensions Python et Jupyter.

### Récupération du projet

```bash
git clone git@github.com:michaelgirardet/instacart-shopping-habits.git
cd instacart-shopping-habits
```

### Environnement virtuel

Sous Linux ou macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Dépendances

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Les principales bibliothèques utilisées sont `numpy`, `pandas`, `matplotlib` et `scikit-learn`.

## Utilisation

Après avoir placé les CSV dans `datasets/`, lancer Jupyter depuis la racine du projet :

```bash
jupyter notebook exploration.ipynb
```

ou :

```bash
jupyter lab
```

Ouvrir ensuite `exploration.ipynb` et exécuter les cellules dans l'ordre avec **Run All**. Les chemins utilisés dans le notebook sont relatifs à la racine du projet.

## Préparation et contrôle des données

Le module [`src/prepare_data.py`](src/prepare_data.py) regroupe le chargement, la fusion et le nettoyage des données.

```python
from src.prepare_data import load_cleaned_data, build_order_level_view

df = load_cleaned_data()
df_commandes = build_order_level_view(df)
```

| Fonction | Rôle |
|---|---|
| `load_raw_tables()` | charge `orders.csv`, `products.csv` et `order_products.csv` |
| `merge_tables(...)` | fusionne les commandes avec les produits |
| `clean_analysis_dataframe(df)` | dédoublonne les articles et conserve uniquement les lignes respectant les domaines attendus |
| `load_cleaned_data()` | exécute le pipeline complet de préparation |
| `build_order_level_view(df)` | construit une table avec une ligne par commande |

Le module [`src/analysis_helpers.py`](src/analysis_helpers.py) fournit la fonction `load_departments()` pour charger et préparer les informations sur les départements.

Le module [`src/ml_features.py`](src/ml_features.py) fournit la fonction `build_ml_dataset()`, qui transforme la table des commandes en un jeu de données prêt pour la modélisation : une ligne par client, des variables calculées sur son historique et un label indiquant si sa dernière commande est arrivée en 15 jours ou moins.

Le notebook contrôle les clés, les valeurs manquantes, les types et les bornes métier avant l'analyse :

- `order_number` doit être supérieur ou égal à 1 ;
- `order_dow` doit être compris entre 0 et 6 ;
- `order_hour_of_day` doit être compris entre 0 et 23 ;
- les délais renseignés doivent être compris entre 0 et 30 jours ;
- les valeurs manquantes de `days_since_prior_order` sont conservées, car elles correspondent aux premières commandes ;
- les doublons éventuels de la clé `(order_id, product_id)` sont supprimés avant l'analyse.

Sur les données fournies, aucun doublon ni aucune valeur hors domaine n'a été trouvé : le nettoyage supprime donc zéro ligne. Les valeurs égales à 100 pour `order_number` et à 30 pour `days_since_prior_order` sont conservées, mais documentées comme des plafonds du dataset. Elles sont traitées séparément dans les graphiques Q1 et Q12 pour ne pas déformer les distributions.

## Organisation de l'analyse

### Bloc A : portrait des clients

Cette partie étudie le nombre de commandes par client, la taille des paniers et le délai entre deux commandes. Elle montre que les clients ont des niveaux d'activité différents, que les petits paniers sont majoritaires et que le rythme hebdomadaire est le plus fréquent.

### Bloc B : évolution des habitudes

Les commandes sont regroupées par numéro de commande afin de suivre l'évolution du comportement d'un client au fil du temps. Ce bloc analyse :

- la taille du panier ;
- le délai entre deux commandes ;
- la part de produits déjà connus ;
- la stabilisation des habitudes ;
- la ressemblance entre le premier panier et les suivants.

### Bloc C : comparaison des segments

Les clients sont répartis en trois groupes :

- **nouveaux** : jusqu'à 5 commandes ;
- **transitionnels** : de 6 à 24 commandes ;
- **fidèles** : 25 commandes ou plus.

Les segments sont comparés selon leur volume d'articles, leurs rayons favoris, leurs horaires de commande et leur rythme de retour.

### Analyses complémentaires

Le notebook contient également une analyse des commandes par jour et par heure, ainsi qu'une comparaison de la quantité d'articles achetés dans les principaux rayons.

### Bloc D : modélisation

Un modèle de classification prédit si un client repassera commande dans les 15 jours, seuil de relance identifié pendant l'exploration. Quatre approches sont comparées (baseline, régression logistique, forêt aléatoire, gradient boosting) sur un découpage entraînement/test stratifié de 80/20. Le gradient boosting est retenu avec un ROC-AUC d'environ 0,76, et le modèle produit un score de risque utilisable pour prioriser les relances.

## Export du notebook

Une version HTML du notebook exécuté est fournie à la racine du dépôt : [`exploration.html`](exploration.html).

Pour régénérer la version HTML :

```bash
jupyter nbconvert --to html --execute exploration.ipynb
```

## Limites

Le jeu de données ne contient pas les prix des produits. Le volume est donc mesuré à partir du nombre d'articles et non du chiffre d'affaires.

Les délais entre commandes sont limités à 30 jours dans les données disponibles. Un délai de 30 jours ne correspond donc pas nécessairement à un retour mensuel réel. De la même manière, un délai supérieur à 15 jours est utilisé comme signal de risque, mais ne permet pas de confirmer qu'un client a abandonné le service.

## Équipe

Projet pédagogique Epitech (module T-DAT-600), réalisé par :

- Michaël Girardet
- Nadir Ammi Said
- Younes Haddad

Cette version publique est maintenue par Michaël Girardet à des fins de portfolio.

## Licence

Le code de ce dépôt est publié sous licence [MIT](LICENSE). Les données Instacart ne sont pas redistribuées et restent soumises aux conditions de leur source d'origine.
