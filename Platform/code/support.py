from settings import *

def import_image(*path, format = "png", alpha = True):
    full_path = join + f".{format}"
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])): # 0.png
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames