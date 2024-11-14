import numpy as np

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_interpolated_value(x, data):
        return np.interp(x, list(data.keys()), list(data.values()))