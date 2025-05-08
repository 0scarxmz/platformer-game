from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, collision_sprites):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_sprites = collision_sprites

    def update(self, dt):
        # Update logic for the sprite
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Draw the sprite on the surface
