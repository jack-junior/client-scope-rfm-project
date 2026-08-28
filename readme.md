# TP2 — Segmentation clients RFM

**Segmentation RFM des clients — Online Retail II**
*Programme TAISS 2026 — Filière F1 (Data Science)*

Segmentation de la clientèle d'un e-commerce britannique de cadeaux à partir de son historique de transactions (2009-2011), selon la méthode **RFM (Récence, Fréquence, Montant)**, en vue de recommandations marketing actionnables par segment.

<p>
<img alt="Python" src="https://img.shields.io/badge/python-3.11-blue">
<img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.5-orange">
<img alt="statut" src="https://img.shields.io/badge/statut-en%20cours-yellow">
</p>

---

## 1. Contexte et objectif

Un e-commerce cumulant plus d'un million de transactions sur deux ans souhaite personnaliser ses campagnes marketing et réduire son attrition, sans disposer d'une typologie de sa clientèle. Ce projet construit une segmentation basée sur le comportement d'achat (RFM + clustering K-means), caractérise chaque segment et formule des recommandations marketing associées.

Jeu de données : [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) (transactions réelles, ~1M lignes, ~37 pays).

---

## 2. Prérequis

| Outil                        | Version recommandée                 |
| ---------------------------- | ------------------------------------ |
| OS                           | Linux (Ubuntu 22.04+ ou équivalent) |
| Gestionnaire d'environnement | Anaconda ou Miniconda                |
| Python                       | 3.10+                                |
| Interface notebooks          | Jupyter Notebook / JupyterLab        |
| Gestion de version           | Git / GitHub                         |

> Miniconda est suffisant et plus léger qu'Anaconda complet ; les deux fonctionnent indifféremment pour ce projet.

---

## 3. Installation et mise en place de l'environnement

### 3.1 Installer Miniconda (si non déjà installé)

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p "$HOME/miniconda3"
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda init bash
```

### 3.2 Cloner le dépôt

```bash
git clone <url-du-depot>
cd client-scope-rfm-project
```

### 3.3 Créer et activer l'environnement conda

```bash
conda env create -f environment.yml
conda activate client-scope-rfm
```

Si `environment.yml` n'est pas encore généré, créer l'environnement manuellement puis exporter :

```bash
conda create -n client-scope-rfm python=3.10 -y
conda activate client-scope-rfm
pip install -r requirements.txt
conda env export --no-builds > environment.yml
```

### 3.4 Enregistrer le kernel Jupyter du projet

`ipykernel` est inclus dans `environment.yml`. Enregistrer un kernel **dédié au projet**
(plutôt que d'utiliser le kernel `python3` par défaut de Jupyter) évite la cause la plus
fréquente d'erreurs de kernel : un notebook exécuté avec un environnement Python différent
de celui où les dépendances ont été installées.

```bash
python -m ipykernel install --user --name client-scope-rfm --display-name "Python (client-scope-rfm)"
```

> Le nom `client-scope-rfm` est imposé à toute l'équipe : dans Jupyter, sélectionner
> **Kernel → Change Kernel → Python (client-scope-rfm)** avant d'exécuter un notebook. Un nom de
> kernel différent d'un membre à l'autre n'empêche pas l'exécution, mais casse la
> reproductibilité attendue lors de la remise (voir `DEPLOYMENT.md` §9, checklist
> `REPARTITION_EQUIPE.md` §7).

### 3.5 Activer le filtre nbstripout (obligatoire pour contribuer)

`nbstripout` est inclus dans `environment.yml`. Il retire automatiquement les sorties des
notebooks (résultats, images en base64) au moment du `git add`, pour éviter des diffs
Git illisibles entre membres. Il doit être **activé sur chaque poste** après le clone :

```bash
nbstripout --install
```

Voir `CONTRIBUTING.md` pour le détail du flux de travail Git (branches, commits,
répartition par partie).

### 3.6 Lancer Jupyter

```bash
jupyter lab
```

Puis ouvrir les notebooks dans `notebooks/`, dans l'ordre numéroté (voir §5).

---

### 3.7 Dépendances avancées

En plus des bibliothèques cœur (nettoyage, RFM, clustering), `environment.yml` et
`requirements.txt` incluent des paquets liés à des usages spécifiques du projet :

| Paquet                                   | Usage                                                                                                                                                                  |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pyarrow`                              | Lecture/écriture au format`.parquet` pour `data/interim/` et `data/processed/` — plus rapide et plus compact que `.csv` sur des jeux de données volumineux. |
| `lifetimes`                            | Modélisation de la valeur vie client (CLV), extension possible de l'analyse RFM au-delà de la segmentation de base.                                                  |
| `streamlit`                            | Tableau de bord interactif pour présenter les segments, en complément des notebooks (facultatif).                                                                    |
| `chromadb` + `sentence-transformers` | Base vectorielle, embeddings et re-ranking pour l'interrogation en langage naturel des résultats de segmentation. |

Ces dépendances sont installées avec le reste de l'environnement (`conda env create -f environment.yml`) — aucune commande `pip install` séparée n'est nécessaire. Elles ne sont pas utilisées par le pipeline RFM principal, mais sont mobilisées par la couche d'interrogation en langage naturel décrite dans [docs/llm-rag-openmind.md](docs/llm-rag-openmind.md).

### 3.8 Interrogation en langage naturel des résultats (RAG)

Le projet répond à l'exigence d'ajouter une couche d'interrogation en langage naturel des segments obtenus. Les résultats des notebooks 03 et 04 sont transformés en documents, découpés puis vectorisés dans ChromaDB avec `sentence-transformers`. Une recherche sémantique et un re-ranking sélectionnent le contexte pertinent, qui est ensuite transmis à un LLM externe accessible via Groq. Les réponses sont accompagnées de citations pour permettre leur vérification.

Cette fonctionnalité s'appuie sur le projet open source [OpenMind RAG](https://github.com/cherif-tg/openmind). Le LLM est utilisé indépendamment de ce dépôt : aucune clé API n'est fournie ni stockée dans le projet. Les étapes d'indexation, les questions d'exemple, l'architecture, les limites et les règles de confidentialité sont décrites dans le [guide d'intégration OpenMind RAG](docs/llm-rag-openmind.md).

**Pour l'évaluation :** cette section couvre explicitement le besoin « base vectorielle + LLM » : documents issus de la segmentation, embeddings, ChromaDB, recherche sémantique, re-ranking, génération via LLM et citations des sources.

---

## 4. Récupération des données

Les données brutes ne sont **pas versionnées** dans le dépôt (fichier volumineux). Deux options :

**Option A — téléchargement manuel**

```bash
mkdir -p data/raw
wget https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip -O data/raw/online_retail_ii.zip
unzip data/raw/online_retail_ii.zip -d data/raw/
```

**Option B — via `ucimlrepo` (dans un notebook ou script Python)**

```python
from ucimlrepo import fetch_ucirepo
online_retail_ii = fetch_ucirepo(id=502)
```

Le fichier source contient deux feuilles Excel (« Year 2009-2010 » et « Year 2010-2011 ») à concaténer ; cette étape est réalisée dans `notebooks/01_nettoyage.ipynb`.

---

## 5. Structure du projet

```
client-scope-rfm/
├── README.md                       # ce fichier
├── environment.yml                 # environnement conda (reproductible)
├── requirements.txt                # dépendances pip (alternative/complément)
├── data/
│   ├── raw/                        # données brutes, non versionnées, jamais modifiées
│   ├── interim/                    # étapes intermédiaires (post-nettoyage)
│   └── processed/                  # jeu de données final prêt pour le clustering
├── notebooks/
│   ├── 01_nettoyage.ipynb          # Partie 1 — nettoyage des transactions
│   ├── 02_features_rfm.ipynb       # Partie 2 — construction et transformation RFM
│   ├── 03_clustering_choix_k.ipynb # Partie 3 — clustering et choix de k
│   ├── 04_caracterisation_segments.ipynb  # Partie 4 — caractérisation et recommandations
│   └── 05_recommendations.ipynb            # Synthèse des recommandations par segment
├── src/                             # fonctions réutilisables extraites des notebooks
│   ├── cleaning.py
│   ├── features.py
│   └── clustering.py
├── figures/                         # graphiques exportés (coude, silhouette, distributions)
├── docs/
│   └── llm-rag-openmind.md          # Guide d'interrogation RAG et d'indexation
├── reports/
│   ├── rapport_tp2.pdf             # rapport final (2-3 pages) — Partie 5 incluse
│   └── tableau_synthese_segments.csv
└── outputs/
    └── customers_segmented.csv     # jeu de données final avec segment assigné
```

**Principes :**

- `data/raw/` en lecture seule : toute transformation produit un nouveau fichier dans `interim/` ou `processed/`, jamais d'écrasement des données sources.
- Un notebook correspond à une étape du pipeline, exécutée dans l'ordre numéroté.
- Le code réutilisable est centralisé dans `src/` plutôt que dupliqué entre notebooks.

---

## 6. Ordre d'exécution du pipeline

| Étape | Notebook                              | Entrée                                 | Sortie                                                         |
| ------ | ------------------------------------- | --------------------------------------- | -------------------------------------------------------------- |
| 1      | `01_nettoyage.ipynb`                | `data/raw/online_retail_ii.xlsx`      | `data/interim/transactions_clean.csv`                        |
| 2      | `02_features_rfm.ipynb`             | `data/interim/transactions_clean.csv` | `data/processed/customers_rfm.csv`                           |
| 3      | `03_clustering_choix_k.ipynb`       | `data/processed/customers_rfm.csv`    | `outputs/customers_segmented.csv`, figures dans `figures/` |
| 4      | `04_caracterisation_segments.ipynb` | `outputs/customers_segmented.csv`     | `reports/tableau_synthese_segments.csv`                      |

Exécuter les notebooks **dans cet ordre** ; chacun dépend de la sortie du précédent.

---

## 7. Conventions du projet

### 7.1 Nommage

- Fichiers et notebooks : `snake_case`, préfixe numérique pour les notebooks (`01_`, `02_`, …).
- Variables et fonctions Python : `snake_case`, explicites (`compute_rfm_features()`, `df_transactions_clean`).
- Colonnes calculées : minuscules, sans accent (`recence`, `frequence`, `montant`, `montant_log`).
- Colonne d'assignation de segment : nom fixe unique dans tout le pipeline → `segment`.
- Noms de segments (identiques partout : notebook, tableau, rapport) : `Champions`, `Fidèles`, `À risque`, `Endormis`, `Nouveaux`, `Perdus`.

### 7.2 Reproductibilité

- `random_state=42` fixé partout où un algorithme stochastique est utilisé (K-means, split, etc.).
- Environnement figé via `environment.yml` (conda) et/ou `requirements.txt` (pip) — toute mise à jour de dépendance doit être suivie d'une réexportation.
- Aucune modification manuelle des fichiers dans `data/raw/`.

### 7.3 Git

- Branches : `type/description-courte` (ex. `feat/nettoyage-annulations`, `fix/valeurs-aberrantes-prix`).
- Commits : verbe à l'infinitif, langue cohérente sur tout le projet.
- `data/raw/` exclu du versionnement (voir `.gitignore`).

---

## 8. Livrables du projet

- Notebooks complétés (parties 1 à 4) — voir `notebooks/`
- Jeu de clients nettoyé avec features RFM documentées — `data/processed/rfm_data_processed.csv, data/processed/features_rfm_data.csv`
- Choix de *k* argumenté (graphique + justification) — `figures/` et `reports/Rapport_ClientScopeRFM_Complete_Corrige.pdf`
- Tableau de synthèse des segments — `reports/tableau_synthese_segments.csv`
- Rapport de 2 à 3 pages (méthode, choix, limites, réponses aux 6 questions du sujet) — `reports/Rapport_ClientScopeRFM_Complete_Corrige.pdf`

---

## 9. Auteurs

| Nom | Rôle / parties principales |
| --- | --------------------------- |
| GAYI Komi Selassi | Reporting                          |
| ACOTIE Sam | Data cleaning, Features RFM, Reporting|
| ASSI Magnim Boris | Features RFM, Reporting |
| ⁠Clement TETTEH ASIAKOLEY | Data cleaning, Features RFM, Clustering and k-means, reporting|
| TCHEDRE Aboudoul | Data cleaning, Features RFM |
| Leny NAPALA | Features RFM, Clustering and k-means |
| ⁠Esther MOUKPE | Data cleaning, Clustering and k-means |
| Othniel AMADOTO | Data cleaning, Clustering and k-means, Project management, CI, Quality Assurance, Reporting|
| BEGUEDOU Essokila Victoire | Data cleaning, Features RFM |
| POTCHO Maxime | Clustering and k-means|
| DJOGUENOU Kossi Elom Hervé | Data cleaning |
| TENGA Cherif Abdel Azize | Data cleaning, Clustering and k-means, LLM - Rag, Reporting |
| KADANSAO Koboyo Lucien | Data cleaning, Features RFM |
