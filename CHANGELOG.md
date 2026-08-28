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

### Previous updates

- Updated the README project status badge from “en cours” to “terminé”.
- Refined README formatting and documentation, including the dependency table and data-download command.
- Corrected the contributor roles listed in the README.

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

## [v0.2.0] - 2026-08-27

Second project release, promoting the RFM customer-segmentation workflow to a documented, reproducible, and reviewable project deliverable.

### Summary

- Finalized the cleaning, RFM feature engineering, standardization, K-Means clustering, segment characterization, and marketing recommendation workflow.
- Added the recommendations notebook with actions for high-value, at-risk, promising, and inactive customer segments.
- Documented the natural-language querying layer using ChromaDB, sentence-transformers, semantic retrieval, re-ranking, and an external Groq LLM through the OpenMind RAG integration.
- Added the OpenMind RAG guide, README documentation, final reports, presentation, and reusable source modules.
- Added notebook-output protection and GitHub Actions validation with `nbstripout`.

### Validation

- Notebooks were manually tested and their JSON structure validated.
- Python source compilation, notebook sanitization, and CI checks passed.
- No automated unit-test suite is currently configured.

## [v0.1.0] - 2026-08-27

### First working release

Delivered the first tested version of the customer-segmentation project based on RFM analysis.

### Summary

- Added retail transaction cleaning and preparation.
- Added Recency, Frequency, and Monetary feature engineering, log transformation, and standardization.
- Added K-Means clustering, elbow-method analysis, customer segment characterization, and recommendations.
- Established the reproducible notebook workflow from data cleaning through recommendations.
- Added project dependency management through `pyproject.toml` and `uv.lock`.
- Added notebook-output and generated-file protection through `nbstripout` and GitHub Actions.

### Validation

- All notebooks were manually tested successfully.
- Python source compilation and notebook JSON validation completed successfully.
- `main` was synchronized with `origin/main`.
