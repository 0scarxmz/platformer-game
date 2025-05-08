from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

    def update(self, dt):
        # Update logic for the sprite
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Draw the sprite on the surface

class AnimatedSprite(Sprite):
    def __init__(self, pos, surf, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
class Player(AnimatedSprite):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.on_floor = False


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = - 20

    def move(self, dt):
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_on_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2).move_to(midtop = self.rect.midbottom))
        self.on_floor = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False
        
            
                                            