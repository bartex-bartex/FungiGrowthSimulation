import numpy as np
import random
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class HyphaeEnd:
    x: int = 0
    y: int = 0

class Model:
    def __init__(self, height, width, growth_probability):
        self.height = height
        self.width = width
        self.growth_probability = growth_probability
        self.frame_id = 0
        self.frame = np.zeros((height, width), dtype=np.int8)
        self.hyphae_ends = deque()

    def saw_spore(self) -> np.array:
        self.frame_id += 1
        self.frame[self.height//2, self.width//2] = 1
        self.hyphae_ends.append(HyphaeEnd(self.height//2, self.width//2))

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

                if (self._check_probability(growth_probability)):
                    cells_to_append.append(cell)
                    has_grown = True

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
    
    def _check_probability(self, probability: float) -> bool:
        return random.random() < probability
    
    def _get_growth_probability(self, cell_neighbors_cnt: int) -> float:
        return self.growth_probability.get(cell_neighbors_cnt, 0)  # Return 0 if value is not in the dictionary

    def get_radius(self) -> np.float64:
        center_x = self.height // 2
        center_y = self.width // 2

        min_x = center_x - min(self.hyphae_ends, key=lambda h: h.x).x
        max_x = max(self.hyphae_ends, key=lambda h: h.x).x - center_x
        min_y = center_y - min(self.hyphae_ends, key=lambda h: h.y).y
        max_y = max(self.hyphae_ends, key=lambda h: h.y).y - center_y

        return np.mean([min_x, max_x, min_y, max_y])
 
    def get_density(self) -> np.float64:
        return np.sum(self.frame) / (np.pi * self.get_radius() ** 2)

    def get_mass(self) -> np.float64:
        return np.sum(self.frame)

    def get_generation(self) -> int:
        return self.frame_id