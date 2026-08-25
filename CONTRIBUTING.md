# Contribuer

## Mise en place

```bash
git clone https://github.com/jack-junior/client-scope-rfm-project.git
cd client-scope-rfm-project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pip install nbstripout
nbstripout --install
```

## nbstripout est obligatoire

Un `.ipynb` est un JSON qui embarque **les résultats d'exécution**, images en base64
comprises. Une simple ré-exécution réécrit des milliers de lignes : sans filtre, deux
personnes travaillant sur des notebooks différents produisent quand même des conflits
illisibles.

`nbstripout` installe un filtre Git qui retire les outputs au moment du `git add` : le code
est versionné, les résultats non. Les figures utiles sont écrites dans `figures/` par les
notebooks eux-mêmes.

Le filtre est local à chaque poste — il ne se transmet pas avec le dépôt. **Chaque membre
doit lancer `nbstripout --install` après son clone.**

## Règles

1. **Un notebook = un responsable.** Les notebooks communiquent par les fichiers de
   `data/processed/`, jamais par la mémoire : chacun avance sur le sien dès que l'amont a
   produit ses sorties.
2. **Une branche par partie** — `feat/01-nettoyage`, `feat/02-features`… Fusion dans `main`
   par Pull Request, relue par un autre membre.
3. **Aucune donnée committée.** Si vous avez besoin des sorties d'un coéquipier,
   ré-exécutez son notebook : c'est le test de reproductibilité du projet.
4. **`git status` avant chaque commit** — ni `.xlsx`, ni `.parquet`, ni `.venv/`.

## Répartition

| Partie | Livrable | Responsable |
|---|---|---|
| P1 — Nettoyage | `notebooks/01_nettoyage.ipynb` | |
| P2 — Features RFM | `notebooks/02_features_rfm.ipynb` | |
| P3 — Clustering | `notebooks/03_clustering.ipynb` | |
| P4 — Caractérisation | `notebooks/04_caracterisation.ipynb` | |
| P5 — Discussion & rapport | `report/` | |

## Messages de commit

```
P2: ajout du calcul du panier moyen
P3: figure silhouette pour k=2..10
docs: précision sur le choix du snapshot
fix: dédoublonnage sur colonnes métier
```
