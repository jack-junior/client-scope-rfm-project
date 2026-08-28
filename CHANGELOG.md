# Changelog

All notable changes to this project will be documented in this file.

## [v0.2.1] - 2026-08-28

Patch release (from v0.2.0): completed project release.

### Summary
- Completed the segmentation project using RFM analysis and K-Means clustering on the UCI Online Retail II dataset.
- Finalized Jupyter notebooks delivering the data cleaning, feature engineering, RFM scoring, clustering, cluster analysis, and visualizations.
- Included a Dockerfile to reproduce the environment and run the notebooks in a containerized setup.
- Updated documentation in README with usage instructions and reproduction steps.
- Minor bug fixes and formatting improvements in notebooks.

### Files / notable artifacts
- Jupyter notebooks (analysis and results)
- Dockerfile for reproducible environment
- README with instructions to run and reproduce results

### How to reproduce locally
1. Clone the repository:
   git clone https://github.com/jack-junior/client-scope-rfm-project.git
2. (Optional) Build the Docker image and run the container:
   docker build -t client-scope-rfm-project .
   docker run --rm -p 8888:8888 client-scope-rfm-project
3. Or install dependencies locally and run notebooks:
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   jupyter lab

### Notes
This is a patch release (incrementing the patch version from v0.2.0 -> v0.2.1) and contains finalization of the analysis and packaging for reproducibility.

