import pygame
import numpy as np
import imageio
import time

from src.display import render_frame, render_text, render_final_message
from src.conversions import surface_to_frame, frame_to_surface
from src.model import Model

from params import Params
from config import Config

start = time.time()

frame_scale = 2
frame_height, frame_width = 300, 300
stats_height, stats_width = 150, 300

MAX_GENERATIONS = 250
config = Config()
params = Params()

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

frames = []
screen = pygame.display.set_mode((frame_width * frame_scale, frame_height * frame_scale + stats_height))  # surface that is main window default black
clock = pygame.time.Clock()
model = Model(frame_height, frame_width, config, params)

frame = model.saw_spore()

running = True

while running and model.is_alive():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_id = model.get_generation()
    radius_mm = model.get_radius_in_mm()
    mass = model.get_mass()
    density = model.get_density()
    time_elapsed = model.get_time_elapsed()

    stats = [
        f"NUTRIENTS: {Params.NUTRIENTS}, TEMP: {Params.TEMP}°C, RH: {Params.RH}%, AW: {Params.AW}",
        f"Generation: {frame_id}",
        f"Time elapsed (h): {time_elapsed}",
        f"Radius (mm): {round(radius_mm, 2)}",
        f"Mass: {mass}",
        f"Density: {round(density, 3)}"
    ]
    render_text(screen, stats, 0, frame_height * frame_scale)
    render_frame(screen, frame, frame_scale)

    frame_and_stats = surface_to_frame(screen)
    frames.append(np.where(frame_and_stats, 255, 0).astype(np.uint8))
    frame = model.next_frame()

    if frame_id >= MAX_GENERATIONS:
        running = False

    # clock.tick(100)

message = "Fungi died - saving..." if not model.is_alive() else "Simulation finished - saving..."
render_final_message(screen, message, 0, frame_height * frame_scale, (255, 0, 0))

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()

end = time.time()
print(f"Time elapsed: {end - start} seconds")