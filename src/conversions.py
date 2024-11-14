import numpy as np
import pygame

def frame_to_surface(frame: np.array) -> pygame.Surface:
    frame = np.where(frame, 255, 0).astype(np.uint8)
    return pygame.surfarray.make_surface(frame)

def surface_to_frame(surface: pygame.Surface) -> np.array:
    frame = pygame.surfarray.array3d(surface)
    frame = np.transpose(frame, (1, 0, 2))  # transpose for correct orientation
    return frame