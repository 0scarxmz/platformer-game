from settings import * 
from sprites import *
from support import *
from timer import Timer
from groups import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Jumping Game')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # load map
        self.load_assests()
        self.setup()

        # timers

    def load_assests(self):
        # graphics
        self.player_frames = import_folder('../images/player')

    def setup(self):
        tmx_data = load_pygame('../data/maps/world.tmx')

        for x, y, image in tmx_data.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_data.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for obj in tmx_data.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames)

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 