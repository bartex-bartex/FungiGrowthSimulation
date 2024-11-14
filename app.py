import pygame
from model import Model
import numpy as np
import imageio
from params import Params
from config import Config

def frame_to_surface(frame: np.array) -> pygame.Surface:
    frame = np.where(frame, 255, 0).astype(np.uint8)
    return pygame.surfarray.make_surface(frame)

def surface_to_frame(surface: pygame.Surface) -> np.array:
    frame = pygame.surfarray.array3d(surface)  # For color images

    # Transpose the frame (rotate 90 degrees counterclockwise)
    frame = np.transpose(frame, (1, 0, 2))

    # Optionally, you can also flip the array horizontally or vertically if needed
    # frame = np.flipud(frame)  # Flip vertically (optional)
    # frame = np.fliplr(frame)  # Flip horizontally (optional)

    return frame

def display_frame(frame):
    frame = np.where(frame, 255, 0).astype(np.uint8)
    frame_surface = pygame.surfarray.make_surface(frame)

    scaled_frame_surface = pygame.transform.scale(frame_surface, (display_width, display_height))
    screen.blit(scaled_frame_surface, (0, 0))
    pygame.display.flip()

def render_text(text, x, y):
    rect_to_clear = pygame.Rect(x, y, 600, 200)
    screen.fill((0, 0, 0), rect_to_clear)

    font = pygame.font.SysFont('Arial', 20)
    for line in text:
        line_surface = font.render(line, True, (255, 255, 255))
        screen.blit(line_surface, (x, y))
        y += 25
    
    pygame.display.flip()

height, width = 300, 300
display_height, display_width = 600, 600
MAX_GENERATIONS = 500

pygame.init()
pygame.display.set_caption("Fungi Growth Simulation")

screen = pygame.display.set_mode((display_height, display_width + 150))  # surface that is main window default black
clock = pygame.time.Clock()
model = Model(height, width, Config, Params)

frame = model.saw_spore()
display_frame(frame)

frames = []
# frames.append(np.where(frame, 255, 0).astype(np.uint8))

running = True

while running and model.is_alive():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = model.next_frame()

    frame_id = model.get_generation()
    radius_mm = round(model.convert_pixel_to_mm(model.get_radius()), 2)
    mass = model.get_mass()
    density = round(model.get_density(), 3)
    time_elapsed = model.get_time_elapsed()

    text = [f"NUTRIENTS {Params.NUTRIENTS}, TEMP: {Params.TEMP}°C, RH: {Params.RH}%, AW: {Params.AW}", f"Generation: {frame_id}", f"Time elapsed (h): {time_elapsed}", f"Radius (mm): {radius_mm}", f"Mass: {mass}", f"Density: {density}"]
    render_text(text, 0, 601)

    display_frame(frame)

    if frame_id > MAX_GENERATIONS:
        running = False

    whole_frame = surface_to_frame(screen)

    frames.append(np.where(whole_frame, 255, 0).astype(np.uint8))

    # clock.tick(100)

imageio.mimsave('fungi.gif', frames, fps=30)
pygame.quit()