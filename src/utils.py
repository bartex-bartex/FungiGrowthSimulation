import numpy as np
import random

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_interpolated_value(x, data):
        return np.interp(x, list(data.keys()), list(data.values()))
    
    @staticmethod
    def simulate_probability(probability: float) -> bool:
        return random.random() < probability

    @staticmethod
    def get_random_value_from_range(value, deviation):
        return random.uniform((1 - deviation) * value, (1 + deviation) * value)