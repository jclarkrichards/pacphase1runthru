import pygame

def getImage(sheet, x, y, width, height):
    sheet.set_clip(pygame.Rect(x, y, width, height))
    return sheet.subsurface(sheet.get_clip())
