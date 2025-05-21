import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups): # player image imput and background update
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 400  # pixels per second

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0  # seconds
        self.cooldown_duration = 200  # miliseconds

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() # get the current time in milliseconds since pygame was initialized
            print(current_time)
            if current_time - self.laser_shoot_time >= self.cooldown_duration: # can shoot again after *this amount of time* has passed
                self.can_shoot = True
                print('can shoot again')

    def update(self, dt):   # update the player
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self_direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        self.rect.center += self_direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed() # fire laser from space key
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)  # create a laser at the player's position
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = (self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))))


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)   # laser fire_position 
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(300, 450)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()

class SpriteCollision(pygame.sprite.Sprite):
    pass

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# import

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()

# sprites

all_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)  # every 500ms

### imports
### [if image has transparent pixels use* .convert_alpha()]
### [if image has no transparent pixels use* .convert()]

# rect

test_rect = pygame.FRect(0, 0, 300, 600)

# GAME LOOP

while running:
    dt = clock.tick(144) / 1000  # 144 frames per second
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)
    
    all_sprites.update(dt)  # update all sprites in the group

    # draw the game
    display_surface.fill(('black'))
    all_sprites.draw(display_surface)  

    # test collision

    print(player.rect.colliderect(test_rect))
    # print(player.rect.collidepoint(pygame.mouse.get_pos()))

    ### rect.cent += direction * speed * dt

    # display_surface.blit(meteor_surf, meteor_rect)
    # display_surface.blit(laser_surf, laser_rect)
  


    pygame.display.update()


pygame.quit()