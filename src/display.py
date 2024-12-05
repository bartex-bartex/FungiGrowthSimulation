import numpy as np
import pygame

def render_frame(screen: pygame.Surface, frame, scale):
    frame = np.where(frame, 255, 0).astype(np.uint8)
    frame_surface = pygame.surfarray.make_surface(frame)
    
    target_size = (frame.shape[1] * scale, frame.shape[0] * scale)
    scaled_frame_surface = pygame.transform.scale(frame_surface, target_size)
    screen.blit(scaled_frame_surface, (0, 0))
    pygame.display.flip()

def render_text(screen: pygame.Surface, lines, x, y, color=(255, 255, 255)):
    rect_to_clear = pygame.Rect(x, y, screen.get_width(), screen.get_height() - y)
    screen.fill((0, 0, 0), rect_to_clear)

    fontSize = 20
    spaceBetweenLines = 5
    font = pygame.font.SysFont('monospace', fontSize)
    for line in lines:
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y))
        y += fontSize + spaceBetweenLines
    
    pygame.display.flip()

def render_final_message(screen: pygame.Surface, message, x, y, color=(255, 255, 255)):

    fontSize = 30
    spaceBetweenLines = 5
    font = pygame.font.SysFont('Space Mono', fontSize)
    line_surface = font.render(message, True, color)
    screen.blit(line_surface, (x, y - fontSize - spaceBetweenLines))
    
    pygame.display.flip()