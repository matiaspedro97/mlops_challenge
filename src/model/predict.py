import pickle
import os
import pandas as pd

from src.constants import MODEL_PATH

class KeyStrokeInference:
    def __init__(self) -> None:
        self.pred = []
        
    def get_model_from_dict(self, config: dict):
        m_name = config.get('Model')
        m_vers = config.get('Version', 0)
        model = pickle.load(open(os.path.join(MODEL_PATH, f'{m_name}_{m_vers}.pkl'), 'rb')) if m_name is not None else None
        
        return model
    
    def get_features_from_dict(self, config: dict):
        model = self.get_model_from_dict(config)
        features = {}
        for k1, it1 in config.items():
            if isinstance(it1, dict):
                for k2, it2 in it1.items():
                    features[f"{k1.lower()}_{k2.lower()}"] = [it2]
        features = pd.DataFrame(features).reindex(model.feature_names_in_, axis=1)
        return model, features
    
    def get_inference_from_dict(self, config: dict):
        model, features = self.get_features_from_dict(config)
        self.pred.append(model.predict(features))
        return {'UserID': self.pred[-1]}

        


            
            
