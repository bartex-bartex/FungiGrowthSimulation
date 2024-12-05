import numpy as np

class Config:

    GROWTH_RATE_TEMP = {
        4: 0,
        9: 0.52,
        10: 0.52,
        19: 1,
        20: 1,
        21: 1,
        22: 1,
        30: 0.85,
        35: 0
    }

    SURVIVAL_TIME_WATER = {
        0: 0,
        11: 4 * 24,
        33: 7 * 24,
        51: 10 * 24,
        75: 13 * 24,
        80 - np.finfo(np.float64).min: 16 * 24, 
        80: 20 * 365 * 24
    }

    BIOMASS_DENSITY_GRAMS_PER_MM2 = 0.0094

    # tempo wrostu (mm / dzień)
    GROWTH_RATE_MM_PER_DAY = 4

    # przedstawienie na pixelach (3h = 1 px)
    GROWTH_TIME_HOURS_PER_PIXEL = 3