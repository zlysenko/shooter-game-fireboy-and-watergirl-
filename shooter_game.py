#Створи власний Шутер!
from pygame import *
from random import*

img_back = 'backfround.jpg' # фон гри
img_hero = 'hero_duet.png' # ігрок
img_monster1 = 'fire_ball.png' # монстр
img_monster2 = 'ice.png' # монстр
img_monster3 = 'rock.png' # монстр
img_ball1 = 'fire.png' # снаряд
img_ball2 = 'drop_water.png' # снаряд
img_bonus = 'bonus.png' # приз


font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)


mixer.init()
mixer.music.load('fireboy_watergirl.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')


win_width = 1300
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter(Fireboy and Watergirl)')
background = transform.scale(image.load(img_back), (win_width, win_height))

score = 0
lost = 0

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

        self.bullet_turn = True     # перемикач куль, true-вогонь,   false-вода
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 160:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

    def fire(self):
        if self.bullet_turn:
            bullet = Bullet(img_ball1, self.rect.centerx - 40, self.rect.top, 50, 60, 10)
        else:
            bullet = Bullet(img_ball2, self.rect.centerx + 10, self.rect.top, 50, 60, 10)
        self.bullet_turn = not self.bullet_turn  # Перемикаємо стан
        bullets.add(bullet)

class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed  
        
        global lost

        if self.rect.y > win_height:
            lost += 1
            self.rect.y = 0 
            self.rect.x = randint(0, win_width-80)

# Куля (снаряд)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()  # Видалити кулю, якщо вона вийшла за верх межі екрану


player = Player(img_hero, 500, win_height - 140, 160, 140, 10)

bullets = sprite.Group()


monsters = sprite.Group()
for i in range (1, 3):
    monster1 = Enemy(img_monster1, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
    monsters.add(monster1)

for i in range (1, 3):
    monster2 = Enemy(img_monster2, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
    monsters.add(monster2)

for i in range (1, 6):
    monster3 = Enemy(img_monster3, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
    monsters.add(monster3)

run = True
finish = False
clock = time.Clock()
FPS = 60
last_shot_time = 0
shoot_delay = 200  # мілісекунд (0.2 секунди)

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        # elif e.type == KEYDOWN:
        #     if e.key == K_SPACE:
        #         player.fire()
        #         fire_sound.play()


    # щоб стріляти на зажатому пробілі
    keys = key.get_pressed()
    current_time = time.get_ticks()

    if keys[K_SPACE]:
        if current_time - last_shot_time > shoot_delay:
            player.fire()
            fire_sound.play()
            last_shot_time = current_time

    if not finish:
        window.blit(background, (0, 0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score = score + 1

            monster_random = randint(1, 3)
            if monster_random == 1:
                monster1 = Enemy(img_monster1, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
                monsters.add(monster1)
            elif monster_random == 2:
                monster2 = Enemy(img_monster2, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
                monsters.add(monster2)
            else:
                monster3 = Enemy(img_monster3, randint(80, win_width-80), randint(-100, -40), 80, 80, randint(1, 3))
                monsters.add(monster3)
            

        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)


        text_lose = font1.render(
        'Пропущено: ' + str(lost), True, (0, 0, 0))
        window.blit(text_lose, (10, 80))

        text_score = font1.render(
        'Рахунок: ' + str(score), True, (0, 0, 0))
        window.blit(text_score, (10, 50))


        if lost >= 5 or sprite.spritecollide(player, monsters, True):
            finish = True
            text_finish = font2.render(
            'Ти програв :[' , False, (250, 250, 240))
            text_rect = text_finish.get_rect(center=(win_width // 2, win_height // 2))
            window.blit(text_finish, text_rect)

        if score >= 15:
            finish = True
            text_finish = font2.render(
            'Ти виграв :]' , True, 	(250, 250, 240))
            text_rect = text_finish.get_rect(center=(win_width // 2, win_height // 2))
            window.blit(text_finish, text_rect)



    else:
        window.blit(background, (0, 0))
        text_rect = text_finish.get_rect(center=(win_width // 2, win_height // 2))
        window.blit(text_finish, text_rect)
        display.update()

    display.update()

    time.delay(20)