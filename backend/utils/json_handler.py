import numpy as np


def convert_float32_to_float(obj):
    if isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_float32_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_float32_to_float(item) for item in obj]
    else:
        return obj