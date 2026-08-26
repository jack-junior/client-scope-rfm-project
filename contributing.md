# Contribuer

Ce guide complète `README.md` (installation et structure générales) et `DEPLOYMENT.md`
(déploiement Docker) : il décrit le **flux de travail Git au quotidien** pour l'équipe.

---

## Mise en place

Le projet utilise **conda** (Anaconda ou Miniconda), pas `venv`/`pip` seul — voir
`README.md` §2-3 si conda n'est pas encore installé.

```bash
git clone https://github.com/jack-junior/client-scope-rfm-project.git
cd client-scope-rfm-project

conda env create -f environment.yml
conda activate client-scope-rfm

# nbstripout est déjà installé via environment.yml — reste à l'activer pour ce dépôt :
nbstripout --install
```

> Si `environment.yml` n'existe pas encore localement, suivre la procédure de secours
> décrite dans `README.md` §3.3 (`conda create` + `pip install -r requirements.txt` +
> `conda env export`).

## nbstripout est obligatoire

Un `.ipynb` est un JSON qui embarque **les résultats d'exécution**, images en base64
comprises. Une simple ré-exécution réécrit des milliers de lignes : sans filtre, deux
personnes travaillant sur des notebooks différents produisent quand même des conflits
illisibles.

`nbstripout` installe un filtre Git qui retire les outputs au moment du `git add` : le code
est versionné, les résultats non. Les figures utiles sont écrites dans `figures/` par les
notebooks eux-mêmes (voir `README.md` §5).

Le filtre est local à chaque poste — il ne se transmet pas avec le dépôt. **Chaque membre
doit lancer `nbstripout --install` après son clone**, dans l'environnement conda `client-scope-rfm`
activé.

## Règles

1. **Un notebook = un responsable.** Les notebooks communiquent par les fichiers de
   `data/interim/` et `data/processed/` (voir le pipeline documenté dans `README.md` §6),
   jamais par la mémoire : chacun avance sur le sien dès que l'amont a produit ses sorties.
2. **Une branche par membre et par partie**, au format `type/prenom-nom` défini dans
   `README.md` §7.3 : `john-doe`, `feat/01-nettoyage`, `feat/02-features-rfm`,
   `feat/03-clustering-choix-k`, `feat/04-caracterisation`, `feat/05-rapport`.
   Fusion dans `master` par Pull Request, relue par un autre membre.
3. **Aucune donnée committée.** `data/`, `outputs/`, `figures/`, `.env` sont exclus par
   `.gitignore` — si vous avez besoin des sorties d'un coéquipier, ré-exécutez son
   notebook : c'est le test de reproductibilité du projet (voir `DEPLOYMENT.md` §9).
4. **`git status` avant chaque commit** — ni `.xlsx`, ni `.parquet`, ni `.conda/`,
   ni `.env`. En cas de doute, `git status --ignored` doit confirmer que ces fichiers
   sont bien listés comme ignorés, pas comme prêts à être committés.
5. **Conventions de nommage respectées** (voir `README.md` §7.1) : `snake_case` partout,
   colonnes sans accent, noms de segments strictement identiques entre notebooks, tableau
   de synthèse et rapport (`Champions`, `Fidèles`, `À risque`, `Endormis`, `Nouveaux`,
   `Perdus`).
6. **`random_state=42`** fixé dans tout code utilisant un algorithme stochastique
   (K-means, ré-échantillonnage) — voir `README.md` §7.2.
7. **

## Répartition

La répartition détaillée par pôle (effectifs, phases, dépendances) est documentée dans
`REPARTITION_EQUIPE.md`. Ce tableau assigne un responsable nominatif par livrable :

| Partie | Livrable | Responsable |
|---|---|---|
| P1 — Nettoyage | `notebooks/01_nettoyage.ipynb` | |
| P2 — Features RFM | `notebooks/02_features_rfm.ipynb` | |
| P3 — Clustering & choix de k | `notebooks/03_clustering_choix_k.ipynb` | |
| P4 — Caractérisation | `notebooks/04_caracterisation_segments.ipynb` | |
| P5 — Discussion & rapport | `reports/rapport_tp2.pdf` | |
| Infra & déploiement | `Dockerfile`, `docker-compose.yml`, `DEPLOYMENT.md` | |
| Coordination & QA | remise finale, relecture croisée | |

## Messages de commit

Format : préfixe de partie (optionnel) + **verbe à l'infinitif** (convention fixée dans
`README.md` §7.3), en français, cohérent sur tout le projet.

```
P2: ajoute le calcul du panier moyen
P3: ajoute la figure silhouette pour k=2..10
docs: précise le choix du snapshot
fix: corrige le dédoublonnage sur colonnes métier
```

Éviter les formulations au participe passé (« ajout de », « correction de ») ou au passé
composé (« a ajouté ») — un seul style doit être utilisé par toute l'équipe pour que
l'historique Git reste lisible.
