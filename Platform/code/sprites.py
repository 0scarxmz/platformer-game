from settings import *
from timer import *



class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func = self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey("black")

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()

class Snake(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = 100
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]


class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(frames, pos, groups)
        self.flip = False

        # movement & collision
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 200
        self.gravity = 25
        self.on_floor = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = - 10

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

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        self.on_floor = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_floor else self.frame_index

        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)