import numpy as np
from collections import deque
from dataclasses import dataclass
from src.utils import Utils
from config import Config
from params import Params


@dataclass(frozen=True, eq=True)
class HyphaeEnd:
    x: int = 0
    y: int = 0

@dataclass(eq=True)
class BoundingBox:
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

    def mean_radius(self):
        return (self.bottom - self.top + self.right - self.left) / 4

@dataclass(frozen=True, eq=True)
class Point:
    x: int = 0
    y: int = 0

class Model:
    def __init__(self, height, width, config: Config, params: Params):
        self.height = height
        self.width = width
        self.center = Point(height // 2, width // 2)
        self.frame_id = 0
        self.frame = np.zeros((height, width), dtype=np.int8)
        self.hyphae_ends = deque()

        self.config = config
        self.params = params

        # set rules simulating nutrients availability
        self.nutrients = params.NUTRIENTS

        # estimate lifespan based on WATER availability
        water_availability = self.params.AW * 100 + self.params.RH
        self.estimated_lifespan = Utils.get_interpolated_value(water_availability, self.config.SURVIVAL_TIME_WATER)
        self.estimated_lifespan = Utils.get_random_value_from_range(self.estimated_lifespan, 0.1)

        # alter growth rate based on TEMPERATURE
        self.growth_rate = Utils.get_interpolated_value(self.params.TEMP, self.config.GROWTH_RATE_TEMP)
        for key in self.nutrients.keys():
            self.nutrients[key] *= self.growth_rate

    def saw_spore(self) -> np.array:
        self.frame_id += 1
        self.frame[self.center.x, self.center.y] = 1
        self.hyphae_ends.append(HyphaeEnd(self.center.x, self.center.y))
        self.bounding_box = BoundingBox(self.center.x, self.center.y, self.center.x, self.center.y)

        return self.frame

    def next_frame(self) -> np.array:
        cells_to_append = []

        while self.hyphae_ends:
            hyphae_end = self.hyphae_ends.popleft()
            hyphae_end_neighbors = self._get_neighbours(hyphae_end)

            has_grown = False
            for cell in hyphae_end_neighbors:
                cell_neighbors = self._get_neighbours(cell)
        
                cell_neighbors_cnt = 0
                for cell_neighbor in cell_neighbors:
                    if self.frame[cell_neighbor.x, cell_neighbor.y] == 1:
                        cell_neighbors_cnt += 1

                # determine growth based on probability
                growth_probability = self._get_growth_probability(cell_neighbors_cnt)

                if (Utils.simulate_probability(growth_probability)):
                    cells_to_append.append(cell)
                    has_grown = True

                    self.bounding_box.top = min(self.bounding_box.top, cell.x)
                    self.bounding_box.bottom = max(self.bounding_box.bottom, cell.x)
                    self.bounding_box.left = min(self.bounding_box.left, cell.y)
                    self.bounding_box.right = max(self.bounding_box.right, cell.y)


            # if haven't grown in the generation might grow in the next
            if not has_grown:
                cells_to_append.append(hyphae_end)

        for cell in set(cells_to_append):
            self.frame[cell.x, cell.y] = 1
            self.hyphae_ends.append(cell)

        self.frame_id += 1

        return self.frame
    
    def _get_neighbours(self, hyphae_end: HyphaeEnd) -> list:
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        neighbours = [
            HyphaeEnd(hyphae_end.x + dx, hyphae_end.y + dy)
            for dx, dy in offsets
            if 0 <= hyphae_end.x + dx < self.height and 0 <= hyphae_end.y + dy < self.width
        ]
        
        return neighbours
    
    def _get_growth_probability(self, cell_neighbors_cnt: int) -> float:
        return self.nutrients.get(cell_neighbors_cnt, 0)  # Return 0 if value is not in the dictionary

    def get_radius_in_pixels(self) -> np.float64:  # ok
        return self.bounding_box.mean_radius()
 
    def get_radius_in_mm(self) -> float:  # ok
        return self.get_radius_in_pixels() * self.config.GROWTH_RATE_MM_PER_DAY / 24 * self.config.GROWTH_TIME_HOURS_PER_PIXEL
    
    def get_time_elapsed(self) -> int:  # ok
        return self.frame_id * self.config.GROWTH_TIME_HOURS_PER_PIXEL

    def get_mass(self) -> np.float64:  # ok
        # gdy teraz 2px = 1 mm, to 4pixele mieszczą się w 1mm^2
        px2_to_mm2 = (self.config.GROWTH_RATE_MM_PER_DAY / 24 * self.config.GROWTH_TIME_HOURS_PER_PIXEL) ** 2
        return np.sum(self.frame) * self.config.BIOMASS_DENSITY_GRAMS_PER_MM2 * px2_to_mm2
    
    def get_density(self) -> np.float64:  # ok
        radius = self.get_radius_in_mm()

        if radius == 0:
            return 0

        return self.get_mass() / (np.pi * (radius ** 2))

    def get_generation(self) -> int:
        return self.frame_id
    
    def is_alive(self) -> bool:
        return self.get_time_elapsed() < self.estimated_lifespan
    