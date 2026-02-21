from pygame import *
from random import randint


font.init()
font2  = font.Font(None, 36)

mixer.init()
mixer.music.load('M5/L4-8/space.ogg')
mixer.music.play()

fire_sound = mixer.Sound("M5/L4-8/fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 5:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("M5/L4/bullet.png",self.rect.x + 40 , win_height - 100, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width - 80)
            self.rect.y = -40
            self.speed = int(self.speed* randint(8,13)/10)
            global lost
            lost += 1


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

bg_im = image.load("M5/L4/galaxy.jpg")
background = transform.scale(bg_im, (win_width, win_height))

player = Player("M5/L4/rocket.png", 300, win_height - 100 , 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("M5/L4/ufo.png", randint(0, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

lost  = 0
run = True
FPS = 20
clock = time.Clock()

while run: 
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()

    window.blit(background, (0,0))

    player.update()
    player.draw()

    monsters.update()
    monsters.draw(window)

    bullets.update()
    bullets.draw(window)

    collide = sprite.groupcollide(monsters, bullets, True, True)
    if collide:
        monster = Enemy("M5/L4/ufo.png", randint(0, win_width - 80), -40, 80, 50, randint(1,5))
        monsters.add(monster)

    text_lose = font2.render("Missed: " + str(lost), 1, (255, 255,255))
    window.blit(text_lose, (10, 50))
    display.update()
    clock.tick(FPS)