# ML Pipeline for Short-Term Rental Prices in NYC

![Conda](https://img.shields.io/conda/pn/conda-forge/python)
![licence](https://img.shields.io/badge/language-Python-brightgreen.svg?style=flat-square)


You are working for a property management company renting rooms and properties for short periods of 
time on various rental platforms. You need to estimate the typical price for a given property based 
on the price of similar properties. Your company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project you will build such a pipeline.

- GitHub release 1.0.2: https://github.com/BolivarTech/build-ml-pipeline-for-short-term-rental-prices.git
- wandb project: https://wandb.ai/bolivartech-com/nyc_airbnb

The following tools are used:

- [MLflow](https://www.mlflow.org) for reproduction and management of pipeline processes.
- [Weights and Biases](https://wandb.ai/site) for artifact and execution tracking.
- [Hydra](https://hydra.cc) for configuration management.
- [Conda](https://docs.conda.io/en/latest/) for environment management.
- [Pandas](https://pandas.pydata.org) for data analysis.
- [Scikit-Learn](https://scikit-learn.org/stable/) for data modeling.

The final goal of the pipeline is to produce the optimal inference artifact which is able to regress the price of a rented unit given its features.

## How to Use This Project

1. Install the [dependencies](#dependencies).
2. Run the pipeline as explained in [the dedicated section](#how-to-run-the-pipeline).

### Dependencies

In order to set up the main environment from which everything is launched you need to install [conda](https://docs.conda.io/en/latest/) and the following sets everything up:

```bash
# Clone repository
git clone https://github.com/BolivarTech/build-ml-pipeline-for-short-term-rental-prices.git
cd build-ml-pipeline-for-short-term-rental-prices

# Create new environment
conda env create -f environment.yml

# Activate environment
conda activate nyc_airbnb_dev
```

All step/component dependencies are handled by MLflow using the dedicated `conda.yaml` environment definition files.

### How to Run the Pipeline

There are multiple ways of running this pipeline, for instance:

- Local execution or execution from cloned source code of the complete pipeline.
- Local execution of selected pipeline steps.
- Remote execution of a release.

In the following, some example commands that show how these approaches work are listed:

```bash
# Go to the root project level, where main.py is
cd build-ml-pipeline-for-short-term-rental-prices

# Local execution of the entire pipeline
mlflow run .

# Step execution: data check + segregation
# Step names can be found in main.py
mlflow run . -P steps="data_check,data_split"

# Execution of a remote release 
mlflow run https://github.com/BolivarTech/build-ml-pipeline-for-short-term-rental-prices.git \
-v 1.0.2 \
-P hydra_options="etl.sample='sample2.csv'"
```

## Authorship

[Julian Bolivar](https://www.linkedin.com/in/jbolivarg), 2023.  
