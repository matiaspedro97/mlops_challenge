from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from loguru import logger
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

import pickle
import json
import os

from src.utils import get_model_latest_version
from src.constants import MODEL_PATH, RESULTS_PATH


def get_model_results(m_name: str = 'RF', version: int = 0):
    res_path = os.path.join(RESULTS_PATH, f'{m_name}_{version}.csv')
    try:
        res = pd.read_csv(res_path, index_col=0).to_dict()
    except Exception as e:
        res = {'Model not found': e}
    return res


class Trainer:
    def __init__(self) -> None:
        self.clf_d = {'RF': RandomForestClassifier(), 'SVM': SVC(probability=True), 'XGB': XGBClassifier()}

    def fit(self, X_t: pd.DataFrame, y_t: np.ndarray, clf_name: str):
        clf = self.clf_d.get(clf_name, None)
        if clf is not None:
            clf.fit(X_t, y_t)
            clf.feature_names_in_ = list(X_t.columns)
        else:
            logger.debug(f"The predictor '{clf_name}' is not pre-defined by this class."
                         f"Please choose a name which is among the following available: {list(self.clf_d.keys())}"
                         )

    def fit_all(self, X_t: pd.DataFrame, y_t: np.ndarray):
        for k, _ in self.clf_d.items():
            self.fit(X_t, y_t, k)
            logger.debug(f"{k} predictor successfully trained!")

        logger.debug(f"Finished training")

    def eval(self, X_v: pd.DataFrame, y_v: np.ndarray, clf_name: str, to_save: bool = True, **kwargs):
        clf = self.clf_d.get(clf_name, None)

        # Confirm whether the classifier is a valid estimator or not (e.g. None)
        if clf is not None:
            # Evaluation
            y_prob = clf.predict_proba(X_v)  # model confidence
            y_pred = np.argmax(y_prob, axis=-1)  # predictions argmax
            clf_rep = pd.DataFrame(classification_report(y_true=y_v, y_pred=y_pred, output_dict=True, **kwargs))
            
            # Save report and estimator
            if to_save:
                m_name = f"{clf_name}_{get_model_latest_version(clf_name) + 1}"
                self.save_estimator(clf=clf, name=m_name)
                self.save_result(rep=clf_rep, name=m_name)
            return clf_rep

        else:
            logger.debug(f"The predictor '{clf_name}' is not pre-defined by this class."
                         f"Please choose a name which is among the following available: {list(self.clf_d.keys())}"
                         )
            return None

    def eval_all(self, X_v: pd.DataFrame, y_v: np.ndarray, to_save: bool = True, **kwargs):
        rep_d = {}
        for k, _ in self.clf_d.items():
            rep_d[k] = self.eval(X_v, y_v, k, to_save=to_save, **kwargs)
            
            logger.debug(f"{k} predictor successfully trained!")

        logger.debug(f"Finished evaluation")
        return rep_d

    def save_result(self, rep: pd.DataFrame, name: str):
        m_path = os.path.join(RESULTS_PATH, f'{name}.csv')
        try:
            rep.to_csv(m_path, index=True)
            logger.debug("Results successfully dumped")
        except Exception as e:
            logger.debug(f"Error: {e}")

    def save_estimator(self, clf, name: str):
        m_path = os.path.join(MODEL_PATH, f'{name}.pkl')
        try:
            pickle.dump(clf, open(m_path, 'wb'))
            logger.debug("Estimator successfully dumped")
        except Exception as e:
            logger.debug(f"Error: {e}")

