import glob
import os

from src.constants import MODEL_PATH

def get_model_latest_version(name: str):
    avail_estim = glob.glob(os.path.join(MODEL_PATH, f'{name}_*.pkl'))
    versions = list(map(lambda x: int(x.split('.')[-2].split('_')[-1]), avail_estim)) + [-1]
    return max(versions)

