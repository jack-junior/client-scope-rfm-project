# Notes d'équipe — Nettoyage · Features RFM · Clustering (Notebooks 1-3)

*Mise au propre des notes manuscrites — à valider/compléter en équipe avant intégration au rapport.*

---

## 0. Rappel des livrables du projet

| # | Livrable | Contenu |
|---|---|---|
| 1 | Notebook complété | Parties 1 à 4 (nettoyage → features → clustering → caractérisation) |
| 2 | Rapport (2-3 pages) | Méthode, choix, limites, réponses aux 6 questions du sujet |
| 3 | Tableau de synthèse | Un segment par ligne, avec effectif/%CA/RFM moyens/top pays-produits |

---

## 1. Pipeline général

```
[1] Nettoyage
     │  → colonnes propres, doublons/annulations traités, retours identifiés
     ▼
[2] Features RFM
     │  → Récence, Fréquence, Montant par client
     ▼
[3] Clustering & choix de k
     │  → K-means, distance euclidienne, méthode du coude
     ▼
[4] Caractérisation (à venir)
```

---

## 2. Notebook 1 — Nettoyage des données

### Ce que vous avez observé sur les colonnes

- **Lettres dans `StockCode`** (notées P, W, C dans vos notes) — **confirmé par la documentation officielle UCI** : le code produit est un nombre à 5 chiffres pouvant être suivi d'une **lettre majuscule** indiquant une variante du même produit. Exemple donné par UCI : `79323P` = *Pink Cherry Lights* et `79323W` = *White Cherry Lights* — même produit de base (`79323`), variante de couleur différente.
  → **Décision à trancher en équipe** : regrouper ces variantes sous un même « produit parent » (utile pour le top produits en Partie 4), ou les garder distinctes ? Documenter le choix dans `DECISIONS.md`.

- **Annulations** — confirmé par UCI : un identifiant de facture (`Invoice`/`InvoiceNo`) commençant par la lettre **C** indique une annulation. La casse varie selon les sources (majuscule ou minuscule) — utiliser un motif insensible à la casse : `^[Cc]`.

- **Retours / montants négatifs** — vos notes identifient correctement le signal : une **quantité négative** correspond généralement à un retour. À formaliser en une nouvelle colonne (ex. `is_return`), plutôt que de le déduire implicitement à chaque analyse.

### Actions concrètes à coder dans `01_nettoyage.ipynb`

- [ ] Colonne `is_cancellation` — regex `^[Cc]` sur `Invoice`.
- [ ] Colonne `is_return` — `Quantity < 0`.
- [ ] Décision documentée sur le regroupement des variantes `StockCode` (P/W/C…).
- [ ] Rapport chiffré avant/après nettoyage (voir `ds_toolkit.cleaning.cleaning_report_summary`).

---

## 3. Notebook 2 — Features RFM

### Définitions retenues

| Feature | Définition |
|---|---|
| **Récence** | Nombre de jours depuis le dernier achat du client |
| **Fréquence** | Nombre de commandes (factures) distinctes |
| **Montant** | Somme de `Quantity × UnitPrice` par client |

### Objectif métier (reformulé de vos notes)

Prédire quels clients sont susceptibles d'acheter à nouveau, et décrire le profil de chaque client à partir de son historique d'achats — **sans algorithme prédictif à proprement parler** : le RFM est une **description agrégée du comportement passé**, pas un modèle prédictif au sens strict. C'est le clustering (Notebook 3) qui en tire une typologie exploitable.

### Outils
Pas d'implémentation algorithmique complexe à ce stade — uniquement de l'agrégation sur les colonnes existantes (`Quantity`, `UnitPrice`, dates, identifiants de commande).

### ⚠️ Point resté ouvert dans vos notes — à trancher en équipe

> *« quelle date choisir pour la récence et pourquoi ? les quantiles »*

Deux décisions distinctes à documenter :
1. **Date de référence pour la récence** — généralement `max(InvoiceDate) + 1 jour` sur l'ensemble du dataset, mais vérifier si cela reste cohérent avec la fusion des deux feuilles (2009-2010 et 2010-2011).
2. **Usage des quantiles** — si l'intention est de segmenter les distributions RFM par quantiles (ex. quartiles) avant ou en complément du clustering, préciser à quelle étape et dans quel but (ex. validation croisée du nommage des segments, détection d'outliers résiduels).

---

## 4. Notebook 3 — Clustering & choix de k

### Principe (reformulé de vos notes)

- **Structure des données** : une ligne = une observation (un client), une colonne = une feature RFM (transformée/standardisée) → matrice d'observations classique pour K-means.
- **Algorithme** : K-means, avec la **distance euclidienne** entre chaque point et les *k* centres (centroïdes).
- **Choix de k — méthode du coude** : tracer l'inertie (somme des distances au carré entre chaque point et son centroïde) en fonction du nombre de clusters, et repérer le point d'inflexion.

### Rappel important (voir `PROTOCOLE.md` de l'équipe)

La méthode du coude seule est **insuffisante** pour justifier *k* dans le rapport — à croiser avec le score de silhouette et un test de stabilité (voir `ds_toolkit.clustering.choose_k_report`). C'est la partie la plus pondérée du barème (25 pts) : vos notes couvrent bien le principe technique, mais le rapport devra montrer les **trois critères combinés**, pas seulement le coude.

---

## 5. Repères tirés de la documentation officielle UCI Online Retail II

Pour référence, quelques précisions utiles issues de la documentation du dataset :

- Le jeu de données couvre les transactions d'un détaillant britannique de cadeaux, en ligne, non-magasin, entre décembre 2009 et décembre 2011, avec une clientèle mêlant particuliers et grossistes.
- `CustomerID` est un identifiant nominal à 5 chiffres — cohérent avec le choix de l'utiliser comme clé d'agrégation pour le RFM.
- `Country` reflète le pays de résidence du client, utile pour le champ « top pays » du tableau de synthèse en Partie 4.

*(Cette section peut être citée telle quelle dans la partie « Données » de votre rapport, avec renvoi vers la page UCI officielle.)*
