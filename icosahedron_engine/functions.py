import pygame
import colorsys

def rgb(speed):
    hue = (pygame.time.get_ticks() / (speed * 1000)) % 1

    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

    return int(r * 255), int(g * 255), int(b * 255)