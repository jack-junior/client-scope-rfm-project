# DEPLOYMENT.md — Déploiement du projet via Docker

Ce document décrit comment déployer l'environnement du TP2 (Segmentation clients RFM) dans un conteneur Docker, en local ou sur un serveur distant, afin de fournir un environnement Jupyter reproductible et isolé pour la revue et l'exécution du projet.

> Ce document complète `README.md` (installation locale via conda) sans le remplacer. Docker est recommandé pour la **revue du projet par un tiers** (relecteur, jury) ou pour un **déploiement sur serveur**, indépendamment de la machine hôte.

---

## 1. Architecture de déploiement

```
                    ┌───────────────────────────────┐
                    │        Hôte / Serveur          │
                    │                                 │
   navigateur ───►  │  Conteneur Docker               │
   :8888 (ou 443     │  ┌──────────────────────────┐  │
   via reverse proxy)│  │ miniconda3                │  │
                    │  │  └─ env conda "client-scope-rfm"    │  │
                    │  │      └─ JupyterLab :8888   │  │
                    │  └──────────────────────────┘  │
                    │                                 │
                    │  Volumes persistants :           │
                    │   data_raw / data_interim /      │
                    │   data_processed / outputs /      │
                    │   reports / figures               │
                    └───────────────────────────────┘
```

- Le conteneur embarque **l'environnement conda exact** défini par `environment.yml`, garantissant que le relecteur exécute le projet dans les mêmes conditions que l'équipe.
- Les **données et résultats** sont stockés dans des volumes Docker nommés, séparés de l'image, pour persister entre redémarrages et mises à jour du conteneur.
- Le code (`notebooks/`, `src/`) est monté en volume pour permettre l'édition sans reconstruire l'image à chaque changement.

---

## 2. Fichiers de déploiement du dépôt

| Fichier | Rôle |
|---|---|
| `Dockerfile` | Construit l'image : base `miniconda3`, environnement conda `client-scope-rfm`, utilisateur non-root, lancement de JupyterLab. |
| `docker-compose.yml` | Orchestration : port exposé, token d'authentification, volumes de données, healthcheck. |
| `.dockerignore` | Exclut du build les données brutes, le cache Python et les fichiers sensibles/locaux. |
| `.env` *(à créer localement, non versionné)* | Variables sensibles : `JUPYTER_TOKEN`, `JUPYTER_HOST_PORT`. |

---

## 3. Prérequis

| Outil | Version recommandée |
|---|---|
| Docker Engine | 24.0+ |
| Docker Compose (plugin) | v2+ (`docker compose`, pas `docker-compose`) |
| OS hôte | Linux (Ubuntu 22.04+ recommandé) |
| Accès réseau sortant | requis au premier build (installation des paquets conda) |

Vérifier l'installation :
```bash
docker --version
docker compose version
```

---

## 4. Configuration avant déploiement

### 4.1 Créer le fichier `.env` (non versionné)

À la racine du projet :
```bash
cat > .env <<'EOF'
JUPYTER_TOKEN=change_moi_avec_un_token_fort
JUPYTER_HOST_PORT=8888
EOF
```

> ⚠️ **Ne jamais versionner `.env`** — il doit figurer dans `.gitignore`. Le token protège l'accès à Jupyter ; sans lui, toute personne atteignant le port exposé peut exécuter du code arbitraire dans le conteneur.

### 4.2 Préparer les dossiers de données (si non existants)

```bash
mkdir -p data/raw data/interim data/processed outputs reports figures
```

Les données brutes (`data/raw/`) doivent être déposées manuellement ou récupérées via le script de téléchargement décrit dans `README.md` — elles ne sont pas incluses dans l'image Docker.

---

## 5. Construction et lancement

### 5.1 Build de l'image

```bash
docker compose build
```

### 5.2 Lancement en arrière-plan

```bash
docker compose up -d
```

### 5.3 Vérifier que le conteneur est opérationnel

```bash
docker compose ps
docker compose logs -f jupyter
```

Le log affiche l'URL Jupyter avec le token si celui-ci n'a pas été correctement pris en compte — sinon, accéder directement à :

```
http://<adresse-du-serveur>:8888/?token=<JUPYTER_TOKEN défini dans .env>
```

### 5.4 Copier les données brutes dans le volume (si nécessaire)

Si les données ne sont pas déjà présentes localement dans `data/raw/` avant le premier `up`, elles peuvent être copiées directement dans le conteneur :
```bash
docker cp data/raw/online_retail_ii.xlsx client-scope-rfm-jupyter:/home/jovyan/work/data/raw/
```

### 5.5 Arrêter / redémarrer

```bash
docker compose stop        # arrête sans supprimer les volumes
docker compose down        # arrête et supprime le conteneur (volumes conservés)
docker compose down -v     # ⚠️ supprime aussi les volumes (perte des données/résultats)
```

---

## 6. Déploiement sur un serveur distant

### 6.1 Transfert du projet

```bash
rsync -avz --exclude 'data/raw' --exclude '.git' \
    ./client-scope-rfm/ user@serveur:/opt/client-scope-rfm/
```

Puis, sur le serveur :
```bash
cd /opt/client-scope-rfm
docker compose build
docker compose up -d
```

### 6.2 Exposition sécurisée via reverse proxy (recommandé)

Ne **jamais exposer directement le port 8888 sur Internet** sans HTTPS. Utiliser un reverse proxy (nginx, Traefik ou Caddy) devant le conteneur.

Exemple minimal avec **nginx** + **Let's Encrypt (certbot)** :

```nginx
server {
    listen 443 ssl;
    server_name client-scope-rfm.exemple.org;

    ssl_certificate     /etc/letsencrypt/live/client-scope-rfm.exemple.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/client-scope-rfm.exemple.org/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}

server {
    listen 80;
    server_name client-scope-rfm.exemple.org;
    return 301 https://$host$request_uri;
}
```

Le `JUPYTER_TOKEN` reste actif **en plus** du HTTPS — les deux mécanismes sont complémentaires, pas substituables l'un à l'autre.

---

## 7. Gestion des données et persistance

| Volume | Contenu | Persistance |
|---|---|---|
| `data_raw` | Données sources (Online Retail II) | Conservé entre redéploiements |
| `data_interim` | Sorties du nettoyage (Partie 1) | Conservé |
| `data_processed` | Features RFM finales (Partie 2) | Conservé |
| `outputs` | Jeu de clients segmenté (Partie 3-4) | Conservé |
| `reports` | Rapport final, tableau de synthèse | Conservé |
| `figures` | Graphiques exportés (coude, silhouette) | Conservé |

Sauvegarde d'un volume (exemple pour `outputs`) :
```bash
docker run --rm -v tp2-segmentation-rfm_outputs:/data -v "$PWD":/backup \
    alpine tar czf /backup/outputs_backup.tar.gz -C /data .
```

---

## 8. Mise à jour du déploiement

Après modification du code, de l'`environment.yml` ou du `Dockerfile` :
```bash
git pull
docker compose build --no-cache
docker compose up -d
```

`--no-cache` est recommandé après une modification de `environment.yml`, pour garantir que l'environnement conda est bien reconstruit et non servi depuis le cache Docker.

---

## 9. Dépannage courant

| Symptôme | Cause probable | Solution |
|---|---|---|
| `docker compose up` échoue avec une erreur de port | Port 8888 déjà utilisé sur l'hôte | Modifier `JUPYTER_HOST_PORT` dans `.env` |
| Page Jupyter demande un mot de passe/token inconnu | `JUPYTER_TOKEN` non défini ou `.env` non chargé | Vérifier `docker compose config` pour confirmer la variable résolue |
| Build très long ou échoue au téléchargement des paquets | Pas d'accès réseau sortant depuis le conteneur | Vérifier la connectivité du serveur / proxy réseau |
| Données absentes dans le conteneur | Volumes non montés ou données non copiées | Revoir §5.4, vérifier `docker compose config` |
| Résultats perdus après `docker compose down` | Utilisation erronée de `-v` | Ne jamais utiliser `-v` sauf réinitialisation volontaire |

---

## 10. Bonnes pratiques de sécurité

- Ne jamais commiter `.env` ni de token en clair dans le dépôt Git.
- Toujours utiliser un `JUPYTER_TOKEN` fort et unique par déploiement.
- Restreindre l'accès réseau au port 8888 au reverse proxy uniquement (pas d'exposition directe).
- Exécuter le conteneur avec un utilisateur non-root (déjà configuré dans le `Dockerfile` — utilisateur `jovyan`).
- Limiter la durée de vie du déploiement « live » à la période de revue/évaluation du projet, puis arrêter le conteneur.
