import sys
sys.path.extend('..src/')

import os

from sklearn.model_selection import train_test_split

from src.data.ks_load import KeyStrokeDataLoader
from src.process.ks_process import KeyStrokeExtractor
from src.model.classifier import Trainer
from src.constants import DATA_PATH

# Settings
train_prop = 0.8
y_lbl = 'user'
seed = 9

# Fetch dataset
loader = KeyStrokeDataLoader(path_or_buf=os.path.join(DATA_PATH, 'Train_keystroke.csv'))
ks_df = loader.load_df()  # data

# Extract Features
extractor = KeyStrokeExtractor(df=ks_df, y_lbl=y_lbl)
feat_df = extractor.build_feature_dataframe()
X_total, y_total = feat_df.drop([y_lbl], axis=1), feat_df[y_lbl]

# Splitting
X_train, X_val, y_train, y_val = train_test_split(X_total, y_total, train_size=train_prop, random_state=seed, stratify=y_total)

# Fine-tune estimators (RF, SVM, XGBoost by default)
predictor = Trainer()
predictor.fit_all(X_t=X_train, y_t=y_train)

rep = predictor.eval_all(X_v=X_val, y_v=y_val, to_save=True)

