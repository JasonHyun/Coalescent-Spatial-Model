# Spatial Dynamics of Tumor Evolution Using Coalescent Theory

A computational pipeline for analyzing spatial dynamics of tumor evolution in colorectal cancer using coalescent theory. This project processes whole exome sequencing (WES) data from TCGA and HCMI datasets to reconstruct coalescent trees, test for neutral evolution, and generate spatial representations of tumor lineage dynamics.

## Overview

The pipeline integrates population genetics principles with cancer genomics to:
- **Test for neutral evolution** using the 1/f power law framework
- **Reconstruct coalescent trees** from somatic mutation data using Kingman's coalescent
- **Generate spatial mappings** of lineage distributions using Gaussian diffusion
- **Calculate spatial metrics** including Moran's I, within-lineage spread (α), and founder separation (β)

## Quick Start

### Requirements

- Python 3.10+
- Conda (recommended)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd thesis

# Create conda environment
conda env create -f code/environment.yml
conda activate thesis-coalescent
```

### Data Setup

**Note**: This repository does not include MAF data files. Download data using the GDC Data Transfer Tool:

```bash
# Install GDC Data Transfer Tool (see https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)
gdc-client download -m data/gdc_download_20250829_170124.353372/MANIFEST.txt

# Place downloaded .maf.gz files in data/snv maf/
```

### Running the Pipeline

```bash
cd code
bash pipeline.sh
```

Run individual steps:
```bash
bash pipeline.sh --preprocess-only      # Step 1: Preprocessing
bash pipeline.sh --neutrality-only      # Step 2: Neutrality testing
bash pipeline.sh --coalescent-only       # Step 3: Coalescent reconstruction
bash pipeline.sh --spatial-only         # Step 4: Spatial mapping
```

## Pipeline Steps

1. **Preprocessing**: Filters and prepares MAF files
2. **Neutrality Testing**: Tests for neutral evolution using 1/f power law (R² ≥ 0.98 threshold)
3. **Coalescent Tree Reconstruction**: Builds coalescent-compliant trees with VAF-based N_e estimation
4. **Spatial Mapping**: Applies Gaussian diffusion to generate spatial representations and calculate metrics

## Output Structure

```
results/
├── neutrality_tests/          # Neutrality test results and plots
├── coalescent_trees/          # Coalescent tree reconstructions
└── spatial_mapping/          # Spatial mappings and metrics
```

## Key Features

- **Coalescent-compliant tree reconstruction** following Kingman's coalescent principles
- **Deterministic reproducibility** using MD5 hash-based seeding
- **Spatial autocorrelation analysis** via Moran's I
- **Lineage partitioning** and spatial metric calculation
- **Batch processing** of 800+ patient samples

## Project Structure

```
thesis/
├── code/              # Pipeline scripts
├── data/              # MAF data directory (not included in repo)
└── results/           # Analysis outputs
```

## Citation

If you use this code, please cite the relevant methodology papers and datasets (TCGA, HCMI).

## License

[Specify license]
