import json

import mlflow
import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig

_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_random_forest",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
#    "test_regression_model"
]


# This automatically reads in the configuration
@hydra.main(config_path=".", config_name='config', version_base='1.1')
def go(config: DictConfig):

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Get the path at the root of the MLflow project
    hydra_root_path = hydra.utils.get_original_cwd()

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "download" in active_steps:
            # Download file and load in W&B
            _ = mlflow.run(
                os.path.join(hydra_root_path, "components", "get_data"),
                "main",
                parameters={
                    "sample": os.path.join(hydra_root_path, "components",
                                        "get_data", "data", config["etl"]["sample"]),
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )

        if "basic_cleaning" in active_steps:
            _ = mlflow.run(
                    os.path.join(hydra_root_path, "src", "basic_cleaning"), 
                    "main", 
                    parameters={
                        "input_artifact": "nyc_airbnb/sample.csv:latest",
                        "output_artifact": "clean_data.csv",
                        "output_type": "clean_data",
                        "output_description": "Clean dataset with outliers removed",
                        "min_price": config['etl']['min_price'],
                        "max_price": config['etl']['max_price']
                    },
            )


        if "data_check" in active_steps:
            _ = mlflow.run(
                    os.path.join(hydra_root_path, "src", "data_check"),
                    "main",
                    parameters={
                        "csv": "nyc_airbnb/clean_data.csv:latest",
                        "ref": "nyc_airbnb/clean_data.csv:reference",
                        "kl_threshold": config['data_check']['kl_threshold'],
                        "min_price": config['etl']['min_price'],
                        "max_price": config['etl']['max_price']
                    },
            )

        if "data_split" in active_steps:
            _ = mlflow.run(
                    os.path.join(hydra_root_path, "components", "train_val_test_split"),
                    "main",
                    parameters={
                        "input": "nyc_airbnb/clean_data.csv:latest",
                        "test_size": config['modeling']['test_size'],
                        "random_seed": config['modeling']['random_seed'],
                        "stratify": config['modeling']['stratify_by']
                    },
            )

        if "train_random_forest" in active_steps:

            # NOTE: we need to serialize the random forest configuration into JSON
            rf_config = os.path.abspath("rf_config.json")
            with open(rf_config, "w+") as fp:
                json.dump(dict(config["modeling"]["random_forest"].items()), fp)  # DO NOT TOUCH

            # NOTE: use the rf_config we just created as the rf_config parameter for the train_random_forest
            # step

            ##################
            # Implement here #
            ##################

            pass

        if "test_regression_model" in active_steps:

            ##################
            # Implement here #
            ##################

            pass


if __name__ == "__main__":
    go()
