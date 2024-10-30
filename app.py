import pygame
from model import Model
import numpy as np
import imageio

def frame_to_surface(frame: np.array) -> pygame.Surface:
    frame = np.where(frame, 255, 0).astype(np.uint8)
    return pygame.surfarray.make_surface(frame)


height = 320
width = 320

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

screen = pygame.display.set_mode((height, width))  # surface that is main window default black
clock = pygame.time.Clock()

model = Model(height, width)
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

    frame_id, frame = model.next_frame()
    print(frame_id)
    screen.blit(frame_to_surface(frame), (0, 0))
    pygame.display.flip()

    frames.append(np.where(frame, 255, 0).astype(np.uint8))

    if frame_id > 400:
        running = False

    # clock.tick(100)

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()