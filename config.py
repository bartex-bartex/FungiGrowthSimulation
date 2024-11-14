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
        11: 4,
        33: 7,
        51: 10,
        75: 13,
        80: -1
    }
    """
    Dict[int, int]: Water availability-to-survival time mapping.
    
    This dictionary shows the survival time (in days) of an organism at different water activity levels (%).
    
    A value of `-1` indicates that the organism has enough water to survive.
    """

    GROWTH_RATE_MM_PER_DAY = 4
    """
    Fungi growth rate in millimeters per day.
    """

    GROWTH_TIME_HOURS_PER_PIXEL = 3
    """
    Time (in hours) needed for fungi to grow by 1 pixel in the simulation.
    """