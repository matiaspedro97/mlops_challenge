# MLOPS Challenge
This challenge consists of building a ML solution from scratch and serve the it as a REST API. 

Check out the repository structure and content, below:

```
Project structure
|   .gitignore
|   README.md
|   LICENSE
|___data
|   |   Train_keystroke.csv
|   docs
|   |   aws_diagram.pdf
|___models
|   |   <model_name>_<version>.pkl
|___notebooks
|   |   run_ks_train_models.ipynb
|___reports
|   |   keystroke_features_eda.html
|___requirements
|   |   requirements-dev.txt
|   |   requirements-prod.txt
|___results
|   |   <model_name>_<version>.csv
|___src
|   |   constants.py
|   |   utils.py
|   |___api
|   |   |   __init__.py
|   |   |   api.py
|   |
|   |___data
|   |   |   __init__.py
|   |   |   ks_load.py
|   |
|   |___model
|   |   |   __init__.py
|   |   |   predict.py
|   |   |   classifier.py
|   |
|   |___process
|   |   |   __init__.py
|   |   |   ks_process.py
|   |
|   |___runs
|   |   |   __init__.py
|   |   |   run_ks_train_models.py
```

<br>

----------------
# Build environment
Before start testing the implemented pipeline, we should build the environments.

To build the development environment:
```bash 
python3 -m virtualenv -p /path/to/python3.7 .pipenv-dev 

. .pipenv-dev/bin/activate

pip install -r requirements/requirements-dev.txt
```

To build the production environment:
```bash 
python3 -m virtualenv -p /path/to/python3.7 .pipenv-prod 

. .pipenv-prod/bin/activate

pip install -r requirements/requirements-prod.txt
```

Activate the desired environment by doing:
```bash
. .pipenv-{your env}/bin/activate
```

In case you are on Windows Powershell, do:

```bash
.pipenv-{your env}/Scripts/Activate.ps1
```
<br>

----------------
# Modules
The pipeline comprises of 5 main modules 

## Data
It loads and parses data into a maneagable format. 

*Classes names: KeyStrokeDataLoader*

## Process
It processes the parsed data by manipulating the dataframes and extracting features of interest from it. 

*Classes names: KeyStrokeExtractor*

## Model
It has 2 scripts: classifier.py and predict.py

The script **classifier.py** will conduct the models training and evaluation based on the features extracted in the previous step.

*Classes names: Trainer*

The script **predict.py** assures the model inference stage, given a model name and version (v0 by default).

*Classes names: KeyStrokeInference*

## Runs
This module conducts the experiments' running. For now, one single script makes use of all the previous modules capabilities and generates different ML models from a dataset CSV file.

To execute the current training pipeline, do:

```bash
python src/runs/run_ks_train_models.py
```

Note: Don't forget to activate your **dev** environment (generated through *requirements/requirements-prod.txt* file)

## API
A simple REST API has been implemented on **api.py** script. It opens up the possibility of inference from any trained model given a set of features.

```bash
python uvicorn src.api.api:app --workers 4
```

Note: Don't forget to activate your **prod** environment (generated through *requirements/requirements-prod.txt* file)

<br>

---
# AWS EC2

In case you want to run this on a public instance and serve the API through a public url, follow the **README_VM.md** step guide

<br>

---
# Deliverables
Please take a look at the deliverables:

- **README.md**: a comprehensive description of the whole set of modules of this project;
- **README_VM.md**: a step-by-step guide for running the API inside an AWS Cloud instance;
- **docs/aws_diagram.pdf**: a diagram explaining the API workflow on the cloud server;
- **notebook/run_ks_tran_models.ipynb**: a notebook containing some visualization of the provided dataset and some observations over the extracted features.

