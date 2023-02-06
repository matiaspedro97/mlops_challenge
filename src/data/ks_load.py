import sys
sys.path.append('..src/')

import pandas as pd
import os
import numpy as np



class KeyStrokeDataLoader:
    def __init__(self, path_or_buf: str) -> None:
        self.path = path_or_buf
    
    def load_df(self):
        return pd.read_csv(self.path)

    def get_aggregates_by_sentence(self):
        df = self.load_df()
        df_merg = pd.DataFrame(columns=['user', 'actions', 'values'])
        for user, (_, row) in zip(df['user'], df.drop(['user'], axis=1).iterrows()):
            aux_df = pd.DataFrame({'user': [user]*len(row), 'actions': list(row.index), 'values': row})
            df_merg = pd.concat([df_merg, aux_df], axis=0)
        return df_merg
        
        

    
