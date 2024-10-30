import pygame
from model import Model
import numpy as np
import imageio
import growth_probabilities

def frame_to_surface(frame: np.array) -> pygame.Surface:
    frame = np.where(frame, 255, 0).astype(np.uint8)
    return pygame.surfarray.make_surface(frame)


height = 320
width = 320
MAX_GENERATIONS = 400

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

screen = pygame.display.set_mode((height, width))  # surface that is main window default black
clock = pygame.time.Clock()

model = Model(height, width, growth_probabilities.probability_2)
frame = model.saw_spore()

screen.blit(frame_to_surface(frame), (0, 0))
pygame.display.flip()

frames = []
frames.append(np.where(frame, 255, 0).astype(np.uint8))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = model.next_frame()
    screen.blit(frame_to_surface(frame), (0, 0))
    pygame.display.flip()
    frames.append(np.where(frame, 255, 0).astype(np.uint8))

    frame_id = model.get_generation()
    print(frame_id)


    if frame_id > MAX_GENERATIONS:
        running = False

    # clock.tick(100)

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()