# Segmentation clients RFM — Online Retail II

TAISS 2026 — Togo AI Summer School · Filière F1 (Data Science) · TP2
Équipe : *[noms à compléter]* — Lomé, août 2026
Dépôt : github.com/jack-junior/client-scope-rfm-project

---

## 1. Contexte

Un e-commerce britannique de cadeaux, opérant majoritairement en gros, cumule plus d'un million
de transactions sur deux ans sans connaissance structurée de sa clientèle. Nous construisons une
segmentation comportementale par la méthode RFM (Récence, Fréquence, Montant) suivie d'un
clustering non supervisé, afin d'obtenir des segments nommés et des recommandations marketing
différenciées. La démarche est reproductible : quatre notebooks séquentiels, chacun repartant des
fichiers produits par le précédent, et un dépôt documenté.

## 2. Nettoyage des transactions

Le jeu brut compte **1 067 371 lignes** issues de deux feuilles Excel (déc. 2009 – déc. 2011).
Cinq filtres successifs, chacun journalisé et exporté :

| Filtre | Lignes retirées | Justification |
|---|---:|---|
| Doublons exacts | 34 335 | Artefacts d'export **et chevauchement des deux feuilles** |
| Écritures non-produit | 5 815 | `POST`, `BANK CHARGES`, `ADJUST`… : pas des ventes |
| Annulations (factures `C…`) | 17 914 | Mises de côté pour analyse, non supprimées |
| `CustomerID` manquant | 232 665 | Non rattachables à un client |
| Quantité ou prix ≤ 0 | 60 | Saisies erronées |

Il reste **776 582 transactions, 5 852 clients et 17,1 M£** sur 41 pays.

**Un piège non documenté par la source.** Les deux feuilles se recouvrent du 1er au 9 décembre
2010 : 1 088 factures y figurent deux fois. Comme nous ajoutons une colonne indiquant la feuille
d'origine, un dédoublonnage naïf ne les détecte pas — les deux copies diffèrent par cette colonne.
Il faut dédoublonner sur les seules colonnes métier. Sans cette précaution, 22 202 transactions
restent comptées double et gonflent la Fréquence et le Montant des clients actifs à cette période,
les déplaçant vers les segments haut de gamme. Ce biais ne provoque aucune erreur d'exécution.

**Choix assumés.** Les écritures non-produit sont exclues car le Montant doit mesurer la valeur des
articles achetés, non des frais de port ni des régularisations comptables — arbitrage discutable
pour `POST`. À l'inverse, **les montants extrêmes sont conservés** (jusqu'à 168 000 £ sur une
ligne) : ce sont de véritables commandes de grossistes, précisément les clients que la segmentation
doit isoler. Écrêter au 99e percentile aurait supprimé nos Champions ; l'asymétrie se traite par
transformation logarithmique, non par troncature.

**(Q1) Les annulations changent-elles les segments ?** Non, et nous l'avons mesuré. Deux jeux ont
été préparés — l'un excluant les annulations, l'autre les déduisant du CA client — puis segmentés
séparément. La comparaison des partitions par Adjusted Rand Index donne **ARI = 0,876** sur les
5 838 clients communs : seuls 289 clients (4,9 %) changent de segment. Trente-sept clients (0,63 %)
présentent un CA net nul ou négatif — ils ont retourné autant qu'ils ont acheté — et sont exclus du
jeu net, le logarithme étant impossible sur ces valeurs. Nous conservons le jeu sans retours en
documentant que ce choix n'est pas structurant. La méthode — refaire tourner et mesurer l'écart —
vaut pour toute décision de nettoyage.

## 3. Features RFM et transformations

Agrégation par client au **snapshot du 10/12/2011**, lendemain de la dernière transaction : la date
du jour aurait attribué quinze ans de récence à tous et privé la variable de pouvoir discriminant.
La Fréquence compte les **factures distinctes**, non les lignes — une commande de quarante articles
reste un acte d'achat.

| | Médiane | Moyenne | Maximum | Asymétrie brute | Après `log1p` |
|---|---:|---:|---:|---:|---:|
| Récence (j) | 95 | 200 | 739 | 0,89 | −0,49 |
| Fréquence | 3 | 6,3 | 373 | 12,04 | 1,00 |
| Montant (£) | 856 | 2 917 | 580 987 | 25,33 | 0,27 |

**(Q2) Pourquoi pas K-means sur les RFM bruts ?** K-means minimise une distance euclidienne : sans
mise à l'échelle, le Montant (des milliers) écrase la Récence (des centaines) et la Fréquence (des
unités), et l'on croirait segmenter sur R, F et M alors qu'on ne segmenterait que sur M. Une
asymétrie de 25 signifie en outre qu'une poignée de grossistes est si éloignée du nuage que
l'algorithme leur consacrerait des micro-clusters, écrasant 95 % des clients dans un groupe
indifférencié. Enfin l'écart pertinent est multiplicatif : en brut, 100 £ → 200 £ et
10 000 £ → 10 100 £ constituent le même écart de 100 £ et pèsent identiquement, alors que le
premier client a doublé sa valeur et le second a bougé de 1 %. Le logarithme corrige l'asymétrie
(25,33 → 0,27 pour le Montant), la standardisation égalise ensuite le poids des trois dimensions :
**deux opérations distinctes pour deux problèmes distincts.** Nous assumons ainsi une pondération
égale de R, F et M — décision d'analyste, non propriété des données.

**(Q3) La redondance Fréquence / Montant.** Après transformation, la corrélation atteint **0,85**
contre 0,62 sur données brutes — la corrélation brute était artificiellement basse, les valeurs
extrêmes cassant la relation linéaire. Deux variables aussi corrélées pointent dans la même
direction : la distance compte « l'intensité d'achat » deux fois et la Récence une seule. Parmi les
options possibles (ne rien faire, supprimer M, utiliser le panier moyen, appliquer une PCA), **nous
retenons la première en la documentant.** Une PCA décorrèle par construction — PC1 capte 76 % de la
variance et forme un axe « valeur client », PC1+PC2 couvrent 95 % — mais exprime les centroïdes en
composantes abstraites. Or l'objectif est une segmentation lisible par le marketing : des
centroïdes en jours et en livres se défendent devant une direction, une combinaison linéaire non.

## 4. Clustering et choix de k

K-means (`random_state=42`, `n_init=20`) est retenu pour son déterminisme et l'interprétabilité de
ses centroïdes.

| k | Silhouette | Davies-Bouldin ↓ | Plus petit groupe | ARI bootstrap |
|---:|---:|---:|---:|---:|
| 2 | **0,437** | 0,874 | 2 312 | — |
| 3 | 0,349 | 1,038 | 1 217 | 0,955 |
| **4** | 0,365 | **0,931** | 1 184 | **0,963** |
| 5 | 0,342 | 0,950 | 450 | 0,928 |
| 6 | 0,335 | 0,962 | 472 | 0,890 |

**(Q4) Pourquoi la silhouette ne suffit pas.** Notre cas l'illustre : elle est **maximale à k = 2**.
En la suivant, nous livrerions « actifs » et « partis » — techniquement optimaux, commercialement
inutiles, aucune campagne différenciée ne s'y construisant. Elle mesure une géométrie, non une
utilité ; elle favorise mécaniquement les petits k ; elle ignore la taille des clusters ; elle
suppose des groupes convexes alors que des données comportementales forment un continuum. Seules
ses **variations** importent : elle chute de k=2 à k=3 puis remonte à k=4. Le coude ne tranche pas
davantage — le gain marginal passe de 2 224 (k=3) à 1 430 (k=4) puis 818 (k=5), sans angle net :
il délimite une zone (3 à 5), pas une valeur.

**Nous retenons k = 4** comme point de convergence de quatre indications indépendantes : rebond de
silhouette, minimum de Davies-Bouldin, plus petit segment supérieur à 1 100 clients, et surtout la
meilleure stabilité. Ce test consiste à tirer vingt sous-échantillons de 80 % des clients, à
re-clusteriser chacun et à comparer à la partition de référence : **ARI moyen de 0,963**, minimum
0,893. La variante k = 5, qui isole 450 grossistes concentrant 55 % du CA, est documentée : elle
sépare deux groupes appelant la même action marketing, au prix d'un segment plus petit et moins
stable.

## 5. Segments et recommandations

Les segments sont nommés à partir de leurs **valeurs relatives** R/F/M, jamais de leur numéro de
cluster — arbitraire et variable d'une exécution à l'autre.

| Segment | Effectif | % clients | % CA | Récence moy. | Fréquence moy. | Montant moy. |
|---|---:|---:|---:|---:|---:|---:|
| Champions | 1 184 | 20,2 % | **73,4 %** | 28 j | 19,2 | 10 581 £ |
| À risque | 1 454 | 24,8 % | 16,8 % | 228 j | 5,1 | 1 974 £ |
| Nouveaux / Prometteurs | 1 246 | 21,3 % | 6,1 % | 28 j | 3,0 | 841 £ |
| Perdus / Dormants | 1 968 | 33,6 % | 3,7 % | 393 j | 1,4 | 317 £ |

*Panier moyen : 556 £, 489 £, 313 £, 249 £. Références distinctes par client : 208, 81, 57, 23.
Top pays : Royaume-Uni de 82 % à 90 % du CA selon les segments, puis EIRE, Allemagne, France.
Top produits communs : Regency Cakestand 3 Tier, White Hanging Heart T-Light Holder.*

**Un cinquième des clients porte près des trois quarts du chiffre d'affaires.** Les 208 références
distinctes achetées en moyenne par un Champion, contre 23 pour un dormant, confirment un profil de
grossiste et valident rétrospectivement la conservation des montants extrêmes.

- **Champions** — Fidélisation premium : accès anticipé, contact commercial dédié, conditions de
  gros négociées. *Indicateur : rétention à 12 mois.* Priorité 1 : leur perte serait immédiatement
  visible au compte de résultat.
- **À risque** — Réactivation ciblée sur leurs références habituelles, offre limitée dans le temps.
  *Indicateur : réachat à 60 jours.* 2,87 M£ de CA sont exposés.
- **Nouveaux / Prometteurs** — Onboarding : recommandations croisées, remise sur la deuxième
  commande. *Indicateur : passage à 3 commandes ou plus.*
- **Perdus / Dormants** — Win-back à coût maîtrisé, sans remise agressive ; sortie de la base active
  si sans réponse. *Indicateur : coût par client réactivé.*

Un contrôle croisé avec la grille RFM par quintiles valide le découpage — les scores moyens
décroissent dans le même ordre que le CA (14,1 / 9,8 / 9,7 / 5,0) — et révèle l'apport du
clustering : « À risque » et « Nouveaux » obtiennent un score agrégé quasi identique alors que
leurs profils sont opposés (bonne fréquence mais 228 jours de récence pour les premiers, achat
récent mais trois commandes pour les seconds). Une grille par score les confondrait ; deux actions
distinctes s'imposent pourtant.

## 6. Discussion critique et éthique

**(Q5) Défendre la qualité des segments sans vérité terrain.** Aucune bonne réponse n'existe contre
laquelle se comparer. Notre défense repose sur quatre piliers convergents : la **cohérence interne**
(plusieurs métriques indépendantes désignent la même plage de k) ; la **stabilité** (ARI de 0,963
sur vingt rééchantillonnages — les segments ne sont pas l'artefact d'un tirage) ; la **robustesse
aux choix de préparation** (ARI de 0,876 entre variantes avec et sans retours) ; la **validité
métier**, chaque segment se décrivant en une phrase et appelant une action distincte. La validation
réellement externe serait un test A/B, hors périmètre de ce TP.

**Ce que nos résultats ne permettent pas de conclure.** Nous ne prétendons pas avoir identifié
« les vrais » segments. La projection en deux dimensions montre des frontières franches mais aucun
vide entre les groupes : les clients forment un **continuum**, et le clustering découpe cet espace
à des seuils utiles plutôt qu'il ne révèle des groupes préexistants. Un autre algorithme, un autre
k ou un autre snapshot produiraient un découpage différent et tout aussi défendable — c'est
d'ailleurs pourquoi la silhouette reste modeste (0,365), ce qui est normal sur des données
comportementales.

**Autres limites.** 21,8 % des lignes n'ont pas d'identifiant client : nos segments décrivent la
clientèle identifiée, non l'ensemble des ventes. La concentration du CA sur 1 184 clients est un
risque commercial que la segmentation révèle sans le résoudre. Le jeu est à plus de 80 %
britannique et orienté grossistes ; la répartition par pays (EIRE à 100 % de Champions) reflète de
faibles effectifs et ne doit pas être sur-interprétée. Le RFM est enfin **rétrospectif** : il décrit
le passé sans prédire qui rachètera, si bien que les gains de réactivation chiffrés sont des ordres
de grandeur servant à hiérarchiser des priorités, non à bâtir un budget.

**(Q6) Personnalisation et tarification différenciée : quels garde-fous ?** La segmentation rend
possible de facturer plus cher les Champions, captifs, en subventionnant l'acquisition des
Nouveaux. Cette pratique est **juridiquement encadrée** — une discrimination tarifaire non
justifiée par un coût réel peut être illicite et reste déloyale quand le consommateur l'ignore ;
**économiquement risquée** — découvrir qu'on paie plus que son voisin détruit la confiance plus
sûrement qu'une remise ne fidélise ; **éthiquement problématique** quand le segment devient un
proxy d'une caractéristique protégée, le pays ou le pouvoir d'achat se substituant à l'origine ou
à la situation sociale.

Nous retenons quatre garde-fous. **Différencier l'attention, pas le prix** : réserver la
personnalisation aux avantages plutôt qu'aux tarifs de base — une remise ciblée est acceptable, une
majoration ciblée ne l'est pas. **Exclure les variables sensibles et leurs proxys** : notre modèle
n'utilise que trois variables comportementales, sans donnée géographique ni démographique, et c'est
un choix à préserver. **Garantir la réversibilité** : l'appartenance à un segment se recalcule à
chaque période et ne doit jamais devenir une étiquette permanente. **Assurer la transparence** :
pouvoir expliquer à un client pourquoi il reçoit telle offre. Le segment « Perdus » appelle une
vigilance particulière : cesser d'y investir est défendable en allocation budgétaire, mais ne doit
pas dégrader le service auquel ces clients ont droit.

---

*Reproductibilité : graines fixées, journal de nettoyage exporté, `StandardScaler` sérialisé, snapshot figé ; notebooks 01 → 04, procédure dans le `README.md`. Données : UCI Machine Learning Repository, Online Retail II (Dr Daqing Chen).*
