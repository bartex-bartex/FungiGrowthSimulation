import pygame
from model import Model
import numpy as np
import imageio
import growth_probabilities

def frame_to_surface(frame: np.array) -> pygame.Surface:
    frame = np.where(frame, 255, 0).astype(np.uint8)
    return pygame.surfarray.make_surface(frame)

def display_frame(frame):
    frame_surface = frame_to_surface(frame)
    scaled_frame_surface = pygame.transform.scale(frame_surface, (display_width, display_height))
    screen.blit(scaled_frame_surface, (0, 0))
    pygame.display.flip()

height, width = 300, 300
display_height, display_width = 600, 600
MAX_GENERATIONS = 4000

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

screen = pygame.display.set_mode((display_height, display_width))  # surface that is main window default black
clock = pygame.time.Clock()
model = Model(height, width, growth_probabilities.probability_1)

frame = model.saw_spore()
display_frame(frame)

frames = []
frames.append(np.where(frame, 255, 0).astype(np.uint8))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = model.next_frame()
    display_frame(frame)

    frame_id = model.get_generation()
    radius = model.get_radius()
    mass = model.get_mass()
    density = model.get_density()

    print(frame_id, radius, mass, density)

    if frame_id > MAX_GENERATIONS:
        running = False

    frames.append(np.where(frame, 255, 0).astype(np.uint8))

    # clock.tick(100)

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()