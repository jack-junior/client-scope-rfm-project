# syntax=docker/dockerfile:1
FROM continuumio/miniconda3:24.9.2-0

LABEL maintainer="TAISS 2026 - CLIENT SCOPE RFM"
LABEL description="Environnement reproductible pour le TP2 - Segmentation clients RFM (Online Retail II)"

# Dossier de travail dans le conteneur
WORKDIR /home/jovyan/work

# Copier uniquement les fichiers de définition d'environnement d'abord
# (permet de mettre en cache la couche conda si le code change mais pas les dépendances)
COPY environment.yml /tmp/environment.yml

# Créer l'environnement conda à partir de environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Activer l'environnement par défaut pour tous les processus du conteneur
ENV CONDA_DEFAULT_ENV=client-scope-rfm
ENV PATH=/opt/conda/envs/client-scope-rfm/bin:$PATH

# Créer un utilisateur non-root (bonne pratique de sécurité)
RUN useradd -m -s /bin/bash jovyan && \
    chown -R jovyan:jovyan /home/jovyan
USER jovyan

# Copier le reste du projet (notebooks, src, README, etc.)
COPY --chown=jovyan:jovyan . /home/jovyan/work

# Port par défaut de Jupyter
EXPOSE 8888

# Healthcheck simple : vérifie que le serveur Jupyter répond
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8888/api || exit 1

# Lancement de JupyterLab sans authentification par défaut à l'intérieur du conteneur
# (l'authentification/le token est géré via variable d'environnement, voir DEPLOYMENT.md)
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--notebook-dir=/home/jovyan/work"]
