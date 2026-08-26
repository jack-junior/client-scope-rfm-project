# TP2 — Segmentation clients RFM
## Note de synthèse méthodologique — TAISS 2026, filière F1 (Data Science)

---

## 1. Lexique des notions clés

| Terme | Définition |
|---|---|
| **Segmentation clients** | Regroupement d'une clientèle en sous-ensembles homogènes selon des critères comportementaux ou démographiques, dans le but de personnaliser les actions marketing. |
| **Méthode RFM** | Cadre d'analyse comportementale reposant sur trois indicateurs par client : **R**écence (temps écoulé depuis le dernier achat), **F**réquence (nombre d'achats sur une période donnée) et **M**ontant (valeur monétaire totale ou moyenne dépensée). |
| **Récence** | Nombre de jours entre la date de référence de l'analyse et la date de la dernière transaction du client. Plus la récence est faible, plus le client est « chaud ». |
| **Fréquence** | Nombre de transactions (ou de factures distinctes) réalisées par un client sur la période d'observation. |
| **Montant (Monetary)** | Somme totale (ou moyenne) dépensée par le client, généralement calculée comme `Quantity × UnitPrice` agrégé par client. |
| **Clustering** | Famille de méthodes d'apprentissage non supervisé visant à regrouper des observations similaires sans étiquette préalable (pas de « vérité terrain »). |
| **K-means** | Algorithme de clustering partitionnel qui affecte chaque observation au centroïde le plus proche, en minimisant la variance intra-cluster ; nécessite de fixer *a priori* le nombre de clusters *k*. |
| **Méthode du coude (elbow method)** | Technique heuristique consistant à tracer l'inertie intra-cluster en fonction de *k* et à repérer le point d'inflexion (« coude ») au-delà duquel l'ajout de clusters n'apporte plus de gain significatif. |
| **Score de silhouette** | Indicateur (entre -1 et 1) mesurant à quel point chaque point est bien assigné à son cluster par rapport aux clusters voisins ; sert à comparer objectivement différentes valeurs de *k*. |
| **Standardisation (z-score)** | Transformation qui centre (moyenne = 0) et réduit (écart-type = 1) une variable, indispensable avant K-means car l'algorithme est sensible à l'échelle des variables. |
| **Transformation logarithmique** | Application de `log(1+x)` à une variable pour corriger une distribution fortement asymétrique (skewed), typique des variables monétaires et de fréquence en e-commerce. |
| **Valeurs aberrantes (outliers)** | Observations extrêmes s'écartant fortement de la distribution générale, pouvant fausser les centroïdes de K-means si elles ne sont pas traitées. |
| **Attrition / churn** | Phénomène de perte progressive de clients qui cessent d'acheter ; un objectif central de la segmentation est de le prévenir ou de le détecter précocement. |
| **Stabilité du clustering** | Propriété d'une segmentation à produire des résultats similaires malgré de légères variations dans les données ou l'initialisation de l'algorithme (test par ré-échantillonnage, bootstrap, etc.). |
| **Cohérence métier (business sense)** | Critère qualitatif exigeant que les segments identifiés statistiquement soient interprétables et exploitables par les équipes marketing, au-delà de la seule performance mathématique. |
| **Segment actionnable** | Segment suffisamment distinct et de taille suffisante pour justifier une action marketing différenciée et rentable. |
| **Vérité terrain (ground truth)** | Étiquettes réelles et connues à l'avance, absentes en apprentissage non supervisé — d'où la difficulté à « prouver » objectivement la qualité d'un clustering. |
| **Tarification différenciée** | Pratique consistant à proposer des prix ou offres différents selon le segment client, soulevant des questions éthiques (discrimination, équité, transparence). |
| **Reproductibilité** | Capacité d'un tiers à obtenir les mêmes résultats en réexécutant le notebook/le code, condition de rigueur scientifique en data science. |

---

## 2. Informations connues (données du sujet)

- **Contexte métier** : e-commerce britannique de cadeaux, vente essentiellement en gros (*wholesale*), >1 million de transactions sur 2 ans.
- **Objectif métier** : personnaliser les campagnes marketing et réduire l'attrition.
- **Jeu de données** : *UCI Online Retail II* — téléchargeable en `.zip` ou via `fetch_ucirepo(id=502)`.
- **Structure du fichier source** : fichier Excel à deux feuilles (« Year 2009-2010 » et « Year 2010-2011 ») à concaténer.
- **Variables disponibles** :
  - `InvoiceNo` — n° de facture
  - `StockCode` — code produit
  - `Description` — nom du produit
  - `Quantity` — quantité
  - `InvoiceDate` — date/heure de transaction
  - `UnitPrice` — prix unitaire (£)
  - `CustomerID` — identifiant client
  - `Country` — pays (~91 % Royaume-Uni, ~37 pays au total)
- **Durée indicative du TP** : environ 4 heures (+ 1 h en option pour le bonus).
- **Barème total** : 100 points, répartis sur 6 rubriques (voir tableau ci-dessous).
- **Transposabilité** : la méthode doit être applicable, en discussion, à un contexte ouest-africain (e-commerce local, plateforme de paiement mobile).

---

## 3. Ce qui est attendu / livrables du projet final

### 3.1 Travail à réaliser (5 parties)
1. **Nettoyage des transactions** (annulations, retours, `CustomerID` manquants, valeurs aberrantes).
2. **Construction et transformation des features RFM** (agrégation par client + traitement des asymétries).
3. **Clustering et choix de k** (justifié par silhouette, coude, stabilité, cohérence métier).
4. **Caractérisation et recommandations** (nommer et décrire chaque segment, formuler des actions marketing).
5. **Discussion critique et éthique** (limites du clustering, enjeux de personnalisation/tarification).

### 3.2 Livrables concrets à remettre
1. Un **notebook complété** (parties 1 à 4), avec code reproductible.
2. Un **jeu de clients nettoyé** contenant les features RFM et leurs transformations documentées.
3. Un **choix de k argumenté** (graphique silhouette et/ou coude + justification écrite).
4. Un **tableau de synthèse des segments**, avec au minimum : effectif, % du CA, récence moyenne, fréquence moyenne, montant moyen, top pays/produits.
5. Des **recommandations marketing par segment** (1 à 2 lignes chacune).
6. Un **rapport de 2 à 3 pages** documentant méthode, choix méthodologiques et limites, répondant explicitement aux 6 questions du sujet (§3.7).

### 3.3 Grille d'évaluation (100 points)
| Rubrique | Points |
|---|---|
| Nettoyage des transactions (P1) | 20 |
| Features RFM et transformations (P2) | 20 |
| Choix de k et clustering (P3) | 25 |
| Caractérisation et recommandations (P4) | 20 |
| Discussion critique et éthique (P5) | 10 |
| Qualité du rapport et reproductibilité | 5 |
| **Total** | **100** |

➡️ **Poids le plus lourd : Partie 3 (choix de k et clustering) — 25 points.** C'est la partie sur laquelle il faut être le plus rigoureux et le plus justifié.

### 3.4 Questions à traiter obligatoirement dans le rapport
1. Impact du traitement des annulations/retours sur les segments — comment le vérifier ?
2. Pourquoi ne pas appliquer K-means sur les RFM bruts ? Apport du log + standardisation ?
3. Comment traiter la corrélation Fréquence/Montant ?
4. Pourquoi la silhouette seule ne suffit pas à choisir *k* ?
5. Comment défendre la qualité des segments sans vérité terrain ?
6. Quels garde-fous éthiques face au risque de tarification différenciée ?

### 3.5 Bonus (optionnel, +1h)
Ajouter une couche d'interrogation en langage naturel des résultats (base vectorielle + LLM), permettant de poser des questions en langage naturel sur les segments obtenus.

---

## 4. Proposition de nom pour le projet

Quelques pistes, à choisir selon le ton souhaité (sobre/institutionnel vs. évocateur) :

- **« ClientScope RFM »** — sobre, évoque l'outil d'observation client.
- **« SegmentAfrique »** ou **« RFM-Africa »** — si vous voulez mettre en avant la dimension de transposabilité vers un e-commerce/paiement mobile ouest-africain.
- **« Cibler pour Fidéliser »** — orienté objectif métier (personnalisation + rétention).
- **« Online Retail II — Typologie Client par RFM »** — nom descriptif académique, adapté si le jury attend un intitulé formel et traçable au jeu de données utilisé.
---

## 5. Protocole de résolution étape par étape

### Outils nécessaires
- **Environnement** : Jupyter Notebook / JupyterLab (ou Google Colab).
- **Langage** : Python 3.
- **Bibliothèques** :
  - `pandas`, `numpy` — manipulation de données
  - `openpyxl` — lecture du fichier Excel source
  - `ucimlrepo` (optionnel) — récupération directe du dataset via `fetch_ucirepo(id=502)`
  - `matplotlib`, `seaborn` — visualisation (distributions, coude, silhouette)
  - `scikit-learn` — `StandardScaler`, `KMeans`, `silhouette_score`
  - `scipy` (optionnel) — tests statistiques de stabilité

### Étape 1 — Chargement et exploration initiale
- Charger les deux feuilles Excel et les concaténer en un seul DataFrame.
- Explorer : dimensions, types, valeurs manquantes, doublons, plages de dates.

### Étape 2 — Nettoyage des transactions (Partie 1, 20 pts)
- Identifier et traiter les **annulations** (souvent repérables via un `InvoiceNo` commençant par « C »).
- Décider d'un traitement pour les **retours** (`Quantity` négative) — exclusion ou traitement séparé, à justifier.
- Supprimer ou isoler les lignes avec `CustomerID` manquant (nécessaire pour l'agrégation par client).
- Traiter les **valeurs aberrantes** (`UnitPrice` ≤ 0, quantités extrêmes).
- **Documenter chaque décision** — c'est noté et cela nourrit la Question 1 du rapport.

### Étape 3 — Construction des features RFM (Partie 2, 20 pts)
- Définir une **date de référence** (ex. : dernière date du dataset + 1 jour).
- Agréger par `CustomerID` :
  - Récence = date de référence − date de dernière commande
  - Fréquence = nombre de factures distinctes
  - Montant = somme de `Quantity × UnitPrice`
- Étudier les distributions (histogrammes) → constater l'asymétrie.
- Appliquer une **transformation log** (`log(1+x)`) puis une **standardisation** (`StandardScaler`).
- Gérer la **redondance Fréquence/Montant** (corrélation) : analyse de corrélation, éventuellement ACP ou choix argumenté de conserver les deux variables malgré la redondance.

### Étape 4 — Clustering et choix de k (Partie 3, 25 pts — la plus pondérée)
- Tester plusieurs valeurs de *k* (ex. 2 à 8) avec K-means.
- Tracer la **courbe du coude** (inertie vs *k*).
- Calculer le **score de silhouette** pour chaque *k*.
- Vérifier la **stabilité** (ex. : plusieurs initialisations aléatoires, ré-échantillonnage).
- Croiser ces critères statistiques avec la **cohérence métier** (des segments trop nombreux ou trop petits sont-ils exploitables par le marketing ?).
- Justifier par écrit le *k* final retenu.

### Étape 5 — Caractérisation et recommandations (Partie 4, 20 pts)
- Pour chaque segment : calculer effectif, % du CA, moyennes RFM, top pays/produits.
- **Nommer** chaque segment de façon parlante (ex. : Champions, Fidèles, À risque, Endormis, Nouveaux clients, Perdus).
- Rédiger 1 à 2 lignes de **recommandation marketing actionnable** par segment.
- Remplir le tableau de synthèse fourni dans le sujet.

### Étape 6 — Discussion critique et éthique (Partie 5, 10 pts)
- Discuter des **limites du clustering** (sensibilité au choix de *k*, absence de vérité terrain, instabilité potentielle).
- Répondre aux 6 questions du sujet, en particulier sur les **garde-fous éthiques** face à la tarification différenciée (transparence, non-discrimination, consentement).

### Étape 7 — Rédaction du rapport et finalisation
- Rapport de 2 à 3 pages : contexte, méthode, résultats (tableau de synthèse), réponses aux 6 questions, limites.
- Vérifier la **reproductibilité** du notebook (exécution de bout en bout sans erreur).
- (Optionnel) Implémenter le bonus : interrogation en langage naturel des résultats via base vectorielle + LLM.

---

*Conseil général* : étant donné la pondération du barème, consacrez un temps proportionnellement plus important à la Partie 3 (choix de k) et documentez systématiquement chaque décision méthodologique — c'est ce qui distingue un rapport « correct » d'un rapport « rigoureux » dans une évaluation de ce type.

---

## 6. Conventions d'équipe (structure de fichiers et nommage)

Ces conventions ne sont pas imposées par l'énoncé mais sont fortement recommandées pour un travail de groupe cohérent, reproductible et facile à corriger.

### 6.1 Structure de fichiers du dépôt

```
client-scope-rfm-project/
├── README.md                      # présentation du projet, instructions d'exécution
├── requirements.txt                # dépendances Python figées (versions)
├── data/
│   ├── raw/                        # données brutes, jamais modifiées
│   │   └── online_retail_ii.xlsx
│   ├── interim/                    # étapes intermédiaires (post-nettoyage brut)
│   │   └── transactions_clean.csv
│   └── processed/                  # jeu de données final prêt pour le clustering
│       └── customers_rfm.csv
├── notebooks/
│   ├── 01_nettoyage.ipynb
│   ├── 02_features_rfm.ipynb
│   ├── 03_clustering_choix_k.ipynb
│   └── 04_caracterisation_segments.ipynb
├── src/                             # fonctions réutilisables extraites des notebooks
│   ├── cleaning.py
│   ├── features.py
│   └── clustering.py
├── figures/                         # graphiques exportés (coude, silhouette, distributions)
│   ├── coude_inertie.png
│   └── silhouette_scores.png
├── reports/
│   ├── rapport_tp2.pdf              # rapport final 2-3 pages
│   └── tableau_synthese_segments.csv
└── outputs/
    └── customers_segmented.csv      # jeu de données final avec segment assigné
```

**Principes directeurs :**
- **`data/raw/` est en lecture seule** — on ne modifie jamais les données sources ; toute transformation produit un nouveau fichier dans `interim/` ou `processed/`.
- **Un notebook = une étape du pipeline**, numérotée dans l'ordre d'exécution (`01_`, `02_`, …), pour qu'un correcteur puisse suivre le déroulé sans ambiguïté.
- **Le code réutilisable** (fonctions de nettoyage, calcul RFM, etc.) est extrait dans `src/` plutôt que dupliqué dans chaque notebook.
- **Un seul point d'entrée documenté** : le `README.md` doit indiquer l'ordre d'exécution des notebooks et les commandes d'installation (`pip install -r requirements.txt`).

### 6.2 Conventions de nommage

| Élément | Convention | Exemple |
|---|---|---|
| Fichiers Python / notebooks | `snake_case`, préfixe numérique pour l'ordre | `02_features_rfm.ipynb` |
| Variables Python | `snake_case`, explicite | `df_transactions_clean`, `customer_id` |
| Colonnes calculées (features) | nom métier en minuscules, sans accent | `recence`, `frequence`, `montant`, `montant_log`, `montant_std` |
| Fonctions | verbe + objet, `snake_case` | `clean_cancellations()`, `compute_rfm_features()` |
| Fichiers de données | `snake_case`, suffixe d'étape | `transactions_clean.csv`, `customers_rfm.csv`, `customers_segmented.csv` |
| Figures exportées | descriptif + type de graphique | `coude_inertie_k2_8.png`, `silhouette_scores_par_k.png` |
| Segments clients | nom court, capitalisé, cohérent entre membres de l'équipe | `Champions`, `Fidèles`, `À risque`, `Endormis`, `Nouveaux`, `Perdus` |
| Colonne d'assignation de segment | nom fixe et unique dans tout le pipeline | `segment` (pas `cluster`, `label`, `groupe` mélangés) |
| Branches Git (si travail collaboratif) | `type/description-courte` | `feat/nettoyage-annulations`, `fix/valeurs-aberrantes-prix` |
| Commits Git | verbe à l'infinitif, en français ou anglais mais **cohérent dans tout le projet** | `Ajoute le calcul des features RFM` |

**Règles transversales à faire respecter par toute l'équipe :**
1. **Une seule langue** pour les noms de variables/colonnes/fonctions dans tout le projet (recommandé : anglais pour le code, français pour les commentaires et le rapport — ou l'inverse, mais pas les deux mélangés).
2. **Les noms de segments doivent être identiques** dans le notebook, le tableau de synthèse et le rapport (éviter qu'un membre écrive « À risque » et un autre « Client à risque »).
3. **Fixer un `random_state`** (ex. `random_state=42`) partout où K-means ou un échantillonnage aléatoire est utilisé, pour garantir la reproductibilité entre les machines de l'équipe.
4. **Versionner `requirements.txt`** dès le début du projet pour éviter les divergences d'environnement entre membres.
