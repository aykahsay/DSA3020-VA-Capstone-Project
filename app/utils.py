import pandas as pd

def prepare_input(year:int, extra_features:dict=None):
    """
    Build DataFrame input for model. Adjust to match trained features.
    """
    d = {"year": year}
    if extra_features:
        d.update(extra_features)
    return pd.DataFrame([d])
