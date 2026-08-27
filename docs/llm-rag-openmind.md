# Interrogation en langage naturel des résultats

> Cette fonctionnalité transforme les résultats de la segmentation RFM en une base de connaissances interrogeable. Un utilisateur peut poser une question en langage naturel sur les segments obtenus sans manipuler directement les fichiers de données, le code Python ou les requêtes SQL.

La couche a été réalisée à partir du projet open source [OpenMind RAG](https://github.com/cherif-tg/openmind), adapté aux résultats de ce projet. Le LLM est un service externe : les utilisateurs le configurent et l'utilisent indépendamment du dépôt de segmentation.

## Architecture RAG

Le fonctionnement repose sur les composants suivants :

1. **Sources analytiques** : résultats RFM, affectations de segments, profils moyens et recommandations produits à l'étape 04.
2. **Documents** : transformation des tableaux et descriptions de profils clients en documents textuels interprétables.
3. **Découpage** : division des documents en fragments afin d'améliorer la recherche de passages pertinents.
4. **Embeddings** : vectorisation des fragments avec `sentence-transformers`.
5. **Base vectorielle** : stockage local des vecteurs et de leurs métadonnées dans ChromaDB.
6. **Recherche sémantique** : sélection des fragments les plus proches de la question utilisateur.
7. **Re-ranking** : réordonnancement des résultats avec les modèles de `sentence-transformers` afin d'améliorer la pertinence du contexte transmis au modèle.
8. **Génération** : transmission du contexte sélectionné à un LLM accessible via Groq.
9. **Réponse justifiée** : génération d'une réponse contextualisée accompagnée de citations ou références vers les documents récupérés.

Le pipeline RAG peut être résumé ainsi :

```text
Résultats RFM + profils segments
            |
            v
Documents -> fragments -> embeddings -> ChromaDB
                                      |
Question utilisateur -> recherche -> re-ranking
                                      |
                                      v
                           contexte + citations
                                      |
                                      v
                              LLM via Groq
                                      |
                                      v
                           réponse conversationnelle
```

## Données indexées

Les informations indexées doivent être produites par le pipeline analytique et correspondre à la version validée des résultats :

- identifiant et effectif de chaque segment ;
- récence, fréquence et montant moyens ;
- part de chiffre d'affaires et indice de valeur ;
- profil métier associé au segment ;
- action marketing recommandée ;
- synthèse des caractéristiques utilisées pour interpréter le segment.

Les fichiers sources recommandés sont les sorties générées par les notebooks 03 et 04, notamment la synthèse des segments et les profils caractérisés. Les données brutes de transaction ne sont pas nécessaires pour poser les questions métier et ne doivent pas être indexées par défaut.

## Étapes d'indexation

Les utilisateurs du LLM exécutent l'indexation dans leur propre environnement OpenMind RAG. Le dépôt fournit les résultats analytiques ; il ne fournit pas de clé API et ne centralise pas le service LLM.

1. **Exécuter le pipeline RFM** dans l'ordre des notebooks 01 à 04.
2. **Vérifier les sorties** : contrôler les colonnes, les noms de segments, les effectifs et les recommandations avant toute indexation.
3. **Préparer les documents** : convertir la synthèse finale et les descriptions de profils en documents texte ou Markdown. Conserver les métadonnées `source`, `segment`, `date_calcul` et `version_donnees`.
4. **Configurer OpenMind RAG** dans un environnement séparé du projet et installer ses dépendances selon sa documentation.
5. **Choisir le modèle d'embeddings** `sentence-transformers` et le modèle de re-ranking adaptés à l'environnement disponible.
6. **Créer ou réinitialiser la collection ChromaDB** correspondant à la version des résultats. Ne pas mélanger plusieurs versions de segmentation dans une même collection sans métadonnées de version.
7. **Découper et vectoriser les documents**, puis enregistrer les fragments et leurs métadonnées dans ChromaDB.
8. **Tester la recherche** avec des questions connues et vérifier que les fragments retournés concernent le bon segment.
9. **Activer le re-ranking** avant l'envoi du contexte au LLM.
10. **Configurer le LLM via Groq** dans l'environnement de l'utilisateur, puis tester les citations et la fidélité des réponses.
11. **Recréer l'index** après toute modification des résultats RFM, des profils ou des recommandations.

## Questions possibles

L'interface conversationnelle permet notamment de demander :

- « Quel segment génère la plus grande part du chiffre d'affaires ? »
- « Quels sont les profils des Champions ? »
- « Quelle stratégie marketing recommander pour les clients Endormis ? »
- « Quel segment doit être contacté en priorité et pourquoi ? »
- « Quels éléments des résultats justifient une campagne de réactivation ? »

Les réponses doivent rester limitées aux informations présentes dans les documents récupérés. Les citations permettent à l'utilisateur de vérifier le segment, le tableau ou le profil utilisé comme source.

## Confidentialité et sécurité

Le LLM étant accessible indépendamment de ce projet, chaque utilisateur est responsable de la configuration de son fournisseur et de son environnement d'exécution.

- Ne jamais transmettre de clé API dans Git, un notebook, un fichier `.env` versionné ou une capture d'écran.
- Ne pas envoyer de données brutes de transaction, d'identifiants personnels, d'adresses ou d'informations sensibles au LLM si une synthèse agrégée suffit.
- Indexer en priorité des statistiques agrégées par segment et des recommandations, plutôt que des lignes individuelles.
- Vérifier les règles de conservation, d'entraînement et de transfert des données du fournisseur LLM choisi.
- Utiliser un fichier `.env` local ou le gestionnaire de secrets du fournisseur ; le dépôt ne contient aucune clé.
- Séparer les collections ChromaDB par projet et par version de données, et protéger les répertoires d'index locaux.
- Vérifier chaque réponse contre les citations et les sorties RFM originales ; le LLM peut produire une interprétation incorrecte ou une information absente du contexte.
- Ne pas utiliser une réponse générée comme unique justification d'une décision commerciale concernant un client.

## Limites connues

Cette couche facilite l'interprétation, mais elle ne remplace pas l'analyse statistique. La qualité des réponses dépend de la qualité des documents indexés, des embeddings, du re-ranking et du contexte transmis au LLM. Une question hors périmètre doit recevoir une réponse indiquant que l'information n'est pas présente dans la base indexée.

## Vérification de l'exigence

| Élément attendu                             | Mise en oeuvre dans le projet                                          |
| --------------------------------------------- | ---------------------------------------------------------------------- |
| Questions en langage naturel sur les segments | Interface conversationnelle OpenMind RAG                               |
| Base vectorielle                              | ChromaDB                                                               |
| Vectorisation des documents                   | `sentence-transformers`                                              |
| Recherche sémantique                         | Récupération des fragments les plus pertinents                       |
| Amélioration de la pertinence                | Re-ranking avant génération                                          |
| Génération par LLM                          | LLM externe accessible via Groq                                        |
| Réponses traçables                          | Citations des documents récupérés                                   |
| Protection des données                       | Indexation agrégée, secrets hors dépôt et note de confidentialité |
| Reproductibilité                             | Réindexation après chaque nouvelle version des résultats            |

## Référence

- Projet OpenMind RAG : [https://github.com/cherif-tg/openmind](https://github.com/cherif-tg/openmind)
