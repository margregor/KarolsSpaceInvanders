from os import walk
import pygame as pg


def import_folder(path):
    """Function loading graphics folders"""
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path)
            surface_list.append(image_surf)

    return surface_list


enemies_images = import_folder('./graphics/enemy')
player_images = import_folder('./graphics/player')
