import numpy as np

class Config:
    """
    Configuration class holding constant values related to growth rate and survival time.
    """

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
    """
    Dict[int, float]: Temperature-to-growth rate mapping.
    
    This dictionary represents the normalized growth rate of an organism at various temperatures (°C).
    
    Values range from `0` (no growth) to `1` (max growth rate).
    """

    SURVIVAL_TIME_WATER = {
        0: 0,
        11: 4 * 24,
        33: 7 * 24,
        51: 10 * 24,
        75: 13 * 24,
        80 - np.finfo(np.float64).min: 16 * 24, 
        80: 20 * 365 * 24  # TODO: find a better solution for this
    }
    """
    Dict[float, float]: Water availability-to-survival time mapping.
    
    This dictionary shows the survival time (in hours) of an fungi at different water availability levels (%).
    """

    GROWTH_RATE_MM_PER_DAY = 4
    """
    Fungi growth rate in millimeters per day.
    """

    GROWTH_TIME_HOURS_PER_PIXEL = 3
    """
    Time (in hours) needed for fungi to grow by 1 pixel in the simulation.
    """