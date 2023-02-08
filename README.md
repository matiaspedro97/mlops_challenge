# MLOPS Challenge
This challenge consists of building a ML solution from scratch and serve the features with some REST API endpoints. 

```
Project structure
|   .gitignore
|   README.md
|   LICENSE
|___data
|   |   Train_keystroke.csv
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
|       |   __init__.py
|       |   run_ks_train_models.py