import pygame
import numpy as np
import imageio

from src.display import render_frame, render_text, render_final_message
from src.conversions import surface_to_frame, frame_to_surface
from src.model import Model

from params import Params
from config import Config

frame_scale = 2
frame_height, frame_width = 300, 300
stats_height, stats_width = 300, 300

MAX_GENERATIONS = 250
config = Config()
params = Params()

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

frames = []
screen = pygame.display.set_mode(((frame_width + stats_width) * frame_scale, frame_height * frame_scale))  # surface that is main window default black
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

    nutrients_str = [f"{key}: {float(value):.2f}" for key, value in params.NUTRIENTS.items()]
    formatted_nutrients = "[" + ", ".join(nutrients_str) + "]"
    stats = [
        f"NUTRIENTS:        {formatted_nutrients}",
        f"TEMP:             {Params.TEMP}°C",
        f"RH:               {Params.RH}%",
        f"AW:               {Params.AW}",
        "",
        f"Generation:       {frame_id} / {MAX_GENERATIONS}",
        f"Time elapsed (h): {time_elapsed}",
        f"Radius (mm):      {round(radius_mm, 2)}",
        f"Mass (g):         {round(mass, 2)}",
        f"Density (g/mm^2): {round(density, 4)}"
    ]
    render_text(screen, stats, frame_scale, frame_width * frame_scale, 5 + 5 + 15 * frame_scale)
    render_frame(screen, frame, frame_scale)

    frame_and_stats = surface_to_frame(screen)
    frames.append(np.where(frame_and_stats, 255, 0).astype(np.uint8))
    frame = model.next_frame()

    if frame_id >= MAX_GENERATIONS:
        running = False

    # clock.tick(100)

message = "Fungi died..." if not model.is_alive() else "Simulation ended."
render_final_message(screen, message, frame_scale, frame_width * frame_scale, 5, (255, 0, 0))

frame_and_stats = surface_to_frame(screen)
frames.append(np.where(frame_and_stats, 255, 0).astype(np.uint8))

# Clever idea to show saving info to user, but don't save it in the final gif
render_final_message(screen, message + " |   Wait, simulation is being saved", frame_scale, frame_width * frame_scale, 5, (255, 0, 0))

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()