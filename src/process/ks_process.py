import pandas as pd
import numpy as np


class KeyStrokeExtractor:
    def __init__(self, df: pd.DataFrame, y_lbl: str) -> None:
        # Data and Labels
        self.df = df
        self.y_lbl = y_lbl  # groundtruth

        # Checkpoint
        ##############################
        assert self.validate_labels()  # check if both column labels exist in the provided dataframe
        ##############################

        self.classes = self.df[self.y_lbl].unique()

    def validate_labels(self):
        return self.y_lbl in self.df.columns

    def get_stat_aggregates(self, feature: np.ndarray, name: str, axis=1):
        mean, std = np.mean(feature, axis=axis), np.std(feature, axis=axis)
        return pd.DataFrame({f'{name}_mean': mean, f'{name}_std': std})

    def extract_features(self):
        aux_df = self.df.copy(deep=True)
        aux_data, y_true = aux_df.drop([self.y_lbl], axis=1), aux_df[self.y_lbl]

        # In case the columns doesn't come in the correct order
        aux_data = aux_data.reindex(sorted(aux_data.columns, key=lambda x: int(x.split('-')[1])), axis=1)

        # Compute all time differences
        time_diffs = aux_data.diff(axis=1).to_numpy()[:, 1:]

        # Hold time (grab time every 2 keystrokes starting from the 1st diff), 
        # Release-Press time (grab time every 2 keystrokes starting from the 2nd diff)
        ht, rpt = time_diffs[:, ::2], time_diffs[:, 1::2]
        
        # Press-Press time (sum even HT indices and RPT), Release-Release time (sum odd HT indices and RPT)
        ppt, rrt = np.sum([ht[:, :-1], rpt], axis=0), np.sum([ht[:, 1:], rpt], axis=0)

        return y_true, (ht, rpt, ppt, rrt)

    def build_feature_dataframe(self):
        y_true, (ht, rpt, ppt, rrt) = self.extract_features()

        # Mean and STD aggregates
        ht_agg = self.get_stat_aggregates(feature=ht, name='ht', axis=1)  # hold time
        rpt_agg = self.get_stat_aggregates(feature=rpt, name='rpt', axis=1)  # release-to-press time
        ppt_agg = self.get_stat_aggregates(feature=ppt, name='ppt', axis=1)  # press-to-press time
        rrt_agg = self.get_stat_aggregates(feature=rrt, name='rrt', axis=1)  # release-to-release time

        # Build feature dataset
        feat_df = pd.concat([ht_agg, ppt_agg, rrt_agg, rpt_agg], axis=1)
        feat_df[self.y_lbl] = y_true

        return feat_df

