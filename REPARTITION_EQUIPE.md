# Répartition de la charge de travail — Équipe TP2 (13-14 membres)

*Segmentation clients RFM — TAISS 2026, filière F1*

Ce document organise le travail en **7 pôles**, alignés sur les parties du sujet et sur le barème (100 pts), afin que la charge soit répartie équitablement et que chaque membre ait une responsabilité claire et traçable pour l'évaluation.

> Hypothèse retenue : équipe de **14 membres**. Pour une équipe de 13, retirer un membre du **Pôle Clustering** (3 → 2) — voir note en fin de document.

---

## 1. Principe de répartition

La répartition suit trois critères :
1. **Le poids au barème** — les pôles les plus lourds en points reçoivent plus de personnes.
2. **Les dépendances du pipeline** — P1 → P2 → P3 → P4 sont séquentielles ; les pôles en aval ne peuvent pas commencer leur livrable final avant que l'amont ne livre ses données, d'où un plan en **phases** plutôt qu'un travail 100 % parallèle.
3. **La transversalité** — un pôle Infra/DevOps et un pôle Rapport/QA travaillent en continu sur toute la durée du projet, en parallèle des pôles techniques.

---

## 2. Les 7 pôles

| # | Pôle | Effectif | Partie(s) couverte(s) | Points au barème |
|---|---|---|---|---|
| 1 | **Nettoyage des données** | 2 | Partie 1 | 20 |
| 2 | **Features RFM** | 2 | Partie 2 | 20 |
| 3 | **Clustering & choix de *k*** | 3 | Partie 3 | 25 |
| 4 | **Caractérisation & recommandations** | 2 | Partie 4 | 20 |
| 5 | **Discussion critique, éthique & rédaction du rapport** | 2 | Partie 5 + rapport final | 10 (+ qualité rédactionnelle transverse) |
| 6 | **Infrastructure & déploiement (Docker, conda, repo)** | 1-2 | Transverse (reproductibilité) | 5 |
| 7 | **Coordination, QA & intégration** | 1-2 | Transverse | — (garantit la note globale) |

**Total : 14 membres.**

---

## 3. Détail des pôles

### Pôle 1 — Nettoyage des données (2 membres)
- Chargement et fusion des deux feuilles Excel.
- Traitement des annulations, retours, `CustomerID` manquants, valeurs aberrantes.
- Documentation de chaque décision de nettoyage (nécessaire pour la Question 1 du rapport).
- **Livrable** : `notebooks/01_nettoyage.ipynb` + `data/interim/transactions_clean.csv`.

### Pôle 2 — Features RFM (2 membres)
- Calcul Récence / Fréquence / Montant par client.
- Analyse des distributions, transformation log + standardisation.
- Analyse de la redondance Fréquence/Montant (Question 3).
- **Livrable** : `notebooks/02_features_rfm.ipynb` + `data/processed/customers_rfm.csv`.
- *Dépend de* : livrable du Pôle 1.

### Pôle 3 — Clustering & choix de *k* (3 membres — pôle le plus chargé, 25 pts)
- Tests K-means pour plusieurs *k*, courbe du coude, score de silhouette.
- Étude de stabilité (ré-échantillonnage / plusieurs `random_state`).
- Justification écrite du *k* retenu, croisée avec la cohérence métier.
- Répond aux Questions 2 et 4 du rapport.
- **Livrable** : `notebooks/03_clustering_choix_k.ipynb` + `outputs/customers_segmented.csv` + figures.
- *Dépend de* : livrable du Pôle 2. Effectif renforcé (3 personnes) car c'est le pôle le plus technique et le plus pondéré.

### Pôle 4 — Caractérisation & recommandations (2 membres)
- Statistiques descriptives par segment (effectif, %CA, moyennes RFM, top pays/produits).
- Nommage des segments, tableau de synthèse.
- Rédaction des recommandations marketing (1-2 lignes/segment).
- Répond à la Question 5 du rapport.
- **Livrable** : `notebooks/04_caracterisation_segments.ipynb` + `reports/tableau_synthese_segments.csv`.
- *Dépend de* : livrable du Pôle 3.

### Pôle 5 — Discussion critique, éthique & rédaction (2 membres)
- Rédaction des limites méthodologiques du clustering (absence de vérité terrain, instabilité).
- Traitement de la Question 6 (garde-fous éthiques, tarification différenciée).
- **Rédaction et assemblage final du rapport de 2-3 pages**, intégrant les contributions de tous les pôles.
- Peut démarrer dès le début du projet (recherche bibliographique sur l'éthique du clustering) sans attendre les données.
- **Livrable** : `reports/rapport_tp2.pdf`.

### Pôle 6 — Infrastructure & déploiement (1-2 membres)
- Mise en place et maintenance de `environment.yml`, `requirements.txt`.
- Rédaction/maintenance de `README.md` et `DEPLOYMENT.md`.
- Construction et test du `Dockerfile` / `docker-compose.yml`.
- Vérifie la **reproductibilité** de bout en bout (critère noté, 5 pts) avant la remise finale.
- Travaille en continu, indépendamment de l'avancement des données.

### Pôle 7 — Coordination, QA & intégration (1-2 membres, éventuellement cumulé avec le Pôle 6 si effectif = 13)
- Anime les points d'avancement, vérifie le respect des conventions de nommage (§6 du README).
- Relit l'ensemble des notebooks avant chaque jalon pour cohérence (noms de segments identiques partout, `random_state` fixé, etc.).
- Responsable de la remise finale (assemblage des livrables, vérification de la checklist §7).
- Interface avec les encadrants TAISS en cas de question sur le sujet.

---

## 4. Plan en phases (dépendances du pipeline)

Le projet ne peut pas être 100 % parallèle : les pôles 2, 3, 4 dépendent chacun du livrable du pôle précédent. Le plan ci-dessous permet à chacun d'avoir du travail à chaque phase.

| Phase | Pôles actifs à pleine charge | Pôles actifs en parallèle (préparation) |
|---|---|---|
| **Phase 1** | Pôle 1 (Nettoyage) | Pôle 5 (recherche éthique/biblio), Pôle 6 (mise en place repo, Docker, conda), Pôle 7 (cadrage, planning) |
| **Phase 2** | Pôle 2 (Features RFM) | Pôle 3 prépare son notebook (code du coude/silhouette sur données factices), Pôle 5 continue la rédaction des sections méthode |
| **Phase 3** | Pôle 3 (Clustering — 3 pers.) | Pôle 4 prépare les templates du tableau de synthèse, Pôle 6 teste le déploiement Docker sur les données intermédiaires |
| **Phase 4** | Pôle 4 (Caractérisation) | Pôle 5 rédige les recommandations et intègre les résultats au rapport |
| **Phase 5 — Intégration finale** | Tous | Pôle 7 pilote la relecture croisée, Pôle 6 valide la reproductibilité complète (build Docker + exécution end-to-end) |

> **Recommandation** : ne laissez jamais un pôle inactif plus d'une phase. Les membres des pôles 1 et 2, une fois leur livrable terminé, peuvent rejoindre en renfort le Pôle 3 (le plus chargé) ou le Pôle 5 (rédaction) pendant la Phase 3.

---

## 5. Tableau récapitulatif des rôles (RACI simplifié)

| Livrable | Responsable (R) | Contributeurs (C) | Validateur (A) |
|---|---|---|---|
| `01_nettoyage.ipynb` | Pôle 1 | — | Pôle 7 |
| `02_features_rfm.ipynb` | Pôle 2 | Pôle 1 (support) | Pôle 7 |
| `03_clustering_choix_k.ipynb` | Pôle 3 | Pôle 2 (support) | Pôle 7 |
| `04_caracterisation_segments.ipynb` | Pôle 4 | Pôle 3 (support) | Pôle 7 |
| `rapport_tp2.pdf` | Pôle 5 | Tous les pôles (contenu de leur partie) | Pôle 7 |
| `Dockerfile`, `docker-compose.yml`, `DEPLOYMENT.md` | Pôle 6 | — | Pôle 7 |
| `README.md`, conventions | Pôle 6 | Pôle 7 | Pôle 7 |
| Remise finale (checklist, cohérence globale) | Pôle 7 | Tous | Encadrants TAISS |

---

## 6. Ajustement pour une équipe de 13 membres

Retirer **1 membre du Pôle 3** (Clustering passe de 3 à 2) *ou* fusionner le **Pôle 6 et le Pôle 7** en un seul pôle de 2 personnes cumulant Infra + Coordination — cette seconde option est recommandée si l'équipe souhaite garder 3 personnes sur le clustering (pôle le plus pondéré, 25 pts).

---

## 7. Checklist de remise finale (portée par le Pôle 7)

- [ ] Les 4 notebooks s'exécutent de bout en bout sans erreur, dans l'ordre.
- [ ] `random_state=42` est fixé partout où nécessaire.
- [ ] Les noms de segments sont identiques dans les notebooks, le tableau de synthèse et le rapport.
- [ ] Le rapport répond explicitement aux 6 questions du sujet.
- [ ] `README.md` et `DEPLOYMENT.md` sont à jour et testés par une personne n'ayant pas écrit le code (test d'onboarding à froid).
- [ ] Le build Docker fonctionne (`docker compose build && docker compose up -d`) sur une machine autre que celle du Pôle 6.
- [ ] Le fichier `.env` n'est pas versionné dans Git.
- [ ] Tableau de synthèse des segments complété (effectif, %CA, RFM moyens, top pays/produits).
