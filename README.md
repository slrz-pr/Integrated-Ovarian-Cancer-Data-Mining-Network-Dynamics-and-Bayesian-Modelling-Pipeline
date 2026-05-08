# Integrated-Ovarian-Cancer-Data-Mining-Network-Dynamics-and-Bayesian-Modelling-Pipeline

# Ovarian Cancer Pipeline: From Mining to Bayesian Inference

## Project Overview
This repository hosts a bioinformatics pipeline designed to analyze Ovarian Cancer genomic signatures. It utilizes public data to identify high-risk patient groups and gene interaction networks.

## Dataset Reference
* **Name:** TCGA-OV (Ovarian Serous Cystadenocarcinoma)
* **Source:** [GDC Data Portal](https://portal.gdc.cancer.gov/projects/TCGA-OV)
* **Access Date:** May 2026
* **Scope:** Transcriptomic profiles focusing on High-Grade Serous Ovarian Cancer (HGSOC).

## Pipeline Steps
1. **Data Mining:** Cleaning RNA-Seq data and handling clinical stage metadata[cite: 3].
2. **Machine Learning:** Training a Random Forest to classify "High Risk" vs "Low Risk" based on FIGO staging[cite: 3].
3. **Network Dynamics:** Constructing a Protein-Protein Interaction (PPI) map of top-ranked features[cite: 3].
4. **Bayesian Modeling:** Estimating the probability of stage progression given specific gene mutations[cite: 3].
