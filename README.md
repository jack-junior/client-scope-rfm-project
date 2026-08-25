# ClientScope

Segmentation client **RFM** (Récence · Fréquence · Montant) sur 1,07 M de transactions
e-commerce, avec clustering K-means et recommandations marketing par segment.

<p>
<img alt="Python" src="https://img.shields.io/badge/python-3.11-blue">
<img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.5-orange">
<img alt="statut" src="https://img.shields.io/badge/statut-en%20cours-yellow">
</p>

TAISS 2026 · Togo AI Summer School · Filière Data Science · TP2

---

## Aperçu

| | |
|---|---|
| Source | [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) |
| Période | déc. 2009 → déc. 2011 |
| Transactions | 1 067 371 brutes → 776 582 nettoyées |
| Clients | 5 852 · 41 pays · 17,1 M£ |

## Installation

```bash
git clone https://github.com/jack-junior/client-scope-rfm-project.git
cd client-scope-rfm-project

python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt

pip install nbstripout && nbstripout --install    # voir CONTRIBUTING.md
```

## Données

Le dataset (45 Mo) n'est pas versionné.

```bash
curl -L -o retail.zip https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip
unzip retail.zip -d data/raw/
```

Attendu : `data/raw/online_retail_II.xlsx`

## Utilisation

```bash
jupyter lab
```

Exécuter les notebooks dans l'ordre — chacun lit les sorties du précédent dans
`data/processed/`, aucun ne relit l'Excel brut.

| Notebook | Contenu |
|---|---|
| `01_nettoyage.ipynb` | doublons, écritures non-produit, annulations, lignes sans client |
| `02_features_rfm.ipynb` | agrégation par client, transformation log + standardisation |
| `03_clustering.ipynb` | K-means, choix de *k* (coude, silhouette, stabilité) |
| `04_caracterisation.ipynb` | nommage des segments, tableau de synthèse, recommandations |

Dashboard interactif (après `04`) :

```bash
streamlit run app/dashboard.py
```

## Structure

```
data/raw/          dataset brut (non versionné)
data/processed/    transactions nettoyées + features RFM (non versionné)
notebooks/         01 → 04 + 05_avance/ (CLV, robustesse, RAG)
figures/           coude, silhouette, distributions
report/            rapport 2-3 pages
app/               dashboard Streamlit
rag/               index vectoriel de l'assistant
```

## Choix méthodologiques

Les décisions structurantes — snapshot figé au 10/12/2011, Fréquence comptée en factures
distinctes, conservation des montants extrêmes, transformation `log1p` avant
standardisation, traitement de la corrélation Fréquence/Montant — sont argumentées dans les
notebooks et synthétisées dans [`report/`](report/).

## Reproductibilité

Graines fixées (`random_state=42`) · journal de nettoyage exporté en CSV ·
`StandardScaler` sérialisé pour retransformer les centroïdes en unités métier.

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Équipe

| Nom | Partie |
|---|---|
| *à compléter* | |

## Licence

Données : UCI Machine Learning Repository (Dr Daqing Chen). Code sous licence MIT.
