from re import T
from turtle import back
import pygame
import math
import copy
import math

global WIDTH, HEIGHT, FPS, BACKGROUND, WHITE, SPEED, running
global characters

pygame.init()
pygame.mixer.init()

class Character:
    def __init__(self, ids=0, name="", image=["", 100, 100, 0], coord = [0, 0], speed = 3, flip = 0, direct = [0, 0], acc = [0, 0]):
        self.ids = ids
        self.name = name
        img = pygame.image.load(image[0])
        img = pygame.transform.scale(img, (image[1], image[2]))
        self.texture = img
        self.width = image[1]
        self.height = image[2]
        self.curr_flip = image[3]
        self.coord = coord
        self.speed = speed
        self.flip = flip
        self.direct = direct
        self.acc = acc

    def __deepcopy__(self, memo=None):
        new_char = Character(
            ids=copy.deepcopy(self.ids, memo),
            name=copy.deepcopy(self.name, memo),
            texture=copy.deepcopy(self.texture, memo),
            width=copy.deepcopy(self.width, memo),
            height=copy.deepcopy(self.height, memo),
            curr_flip=copy.deepcopy(self.curr_flip, memo),
            coord=copy.deepcopy(self.coord, memo),
            speed=copy.deepcopy(self.speed, memo),
            flip=copy.deepcopy(self.flip, memo),
            direct=copy.deepcopy(self.direct, memo),
            acc=copy.deepcopy(self.acc, memo)
        )
        return new_char

clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
FPS = 60
BACKGROUND = [0,0,50,0]
WHITE = (255,255,255)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Fight v0.2")


# Characters and textures
imgt = "images\\"
characters = [
    Character(8, "Mr.Black", [imgt+"andr.png", 100, 100, 0], [100,100], 4),
    Character(1, "Sun", [imgt+"sun.png", 200, 200, 0], [500,500], 3)
    ]

# Sounds
sd = "sounds\\"
sounds = [
    pygame.mixer.Sound(sd+"music.mp3")
    ]

def nframe():
    global BACKGROUND
    global characters
    win.fill((BACKGROUND[0], BACKGROUND[1], BACKGROUND[2]))
    vert_anim = 25*math.sin( (timer_curr[1] - timer_last[1])/1000*math.pi*2 )
    hor_anim = 10*math.sin( (timer_curr[1] - timer_last[1])/2000*math.pi*2 )
    for char in characters:
        win.blit(char.texture, ( char.coord[0]+hor_anim, char.coord[1]+vert_anim) )
    pygame.display.flip()

def custom_delay(duration):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration and running == True:
        pygame.display.flip()
        clock.tick(FPS)
        exit_func()

def exit_func():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
      


# --=Game~Code=--

sounds[0].play()

timer_last = [pygame.time.get_ticks(), pygame.time.get_ticks()]
timer_interval = [(sounds[0].get_length()+1)*1000, 2000]
running = True
while running:
    timer_curr = [pygame.time.get_ticks(), pygame.time.get_ticks()]
    # Background animation
    if timer_curr[1] - timer_last[1] > timer_interval[1]:
        timer_last[1] = timer_curr[1]

    exit_func()
    nframe()
    clock.tick(FPS)
    
    # Music
    if timer_curr[0] - timer_last[0] > timer_interval[0]:
        sounds[0].play()
        timer_last[0] = timer_curr[0]

    # Background color animation
    if BACKGROUND[3] == 0:
        BACKGROUND[2] += 1
    elif BACKGROUND[3] == 1:
        BACKGROUND[2] -= 1  
    if BACKGROUND[3] == 0 and BACKGROUND[2] >= 120:
        BACKGROUND[3] = 1
    elif BACKGROUND[3] == 1 and BACKGROUND[2] <= 30:
        BACKGROUND[3] = 0

    # Character in-game processing
    for char in characters:     
        
        char.acc = [0, 0]


        # Mr.Black control exclusive
        if char.ids == 8:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                char.acc[1]= -0.05
            if keys[pygame.K_s]:
                char.acc[1]= 0.05
            if keys[pygame.K_a]:
                char.acc[0]= -0.05
            if keys[pygame.K_d]:
                char.acc[0]= 0.05
        
        

        # Char movement
        char.direct[0] += char.acc[0]
        char.direct[1] += char.acc[1]
        modulo = ( char.direct[0]**2 + char.direct[1]**2 )**0.5
        if (char.ids == 8 and not(keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]) and modulo > 0) or (char.ids != 8 and modulo > 0):
            if modulo <= 0.075:
                char.direct = [0, 0]
            else:
                if char.direct[0] != 0:
                    char.direct[0] -= char.direct[0]/abs(char.direct[0])*0.05
                if char.direct[1] != 0:
                    char.direct[1] -= char.direct[1]/abs(char.direct[1])*0.05
    
        if modulo > 1:
            char.direct[0] /= modulo
            char.direct[1] /= modulo
        
        if char.direct[0]>=0:
            char.coord[0] += char.direct[0] * char.speed
        else:
            char.coord[0] += char.direct[0] * char.speed
        if char.direct[1]>=0:
            char.coord[1] += char.direct[1] * char.speed
        else:
            char.coord[1] += char.direct[1] * char.speed
        
        if char.coord[0]+char.width>WIDTH:
            char.coord[0] = WIDTH - char.width
        elif char.coord[0] < 0:
            char.coord[0] = 0
        if char.coord[1]+char.height>HEIGHT:
            char.coord[1] = HEIGHT - char.height
        elif char.coord[1] < 0:
            char.coord[1] = 0

        if char.flip == 0 and char.acc[0] > 0:
            char.flip = 1
        elif char.flip == 1 and char.acc[0] < 0:
            char.flip = 0
        if char.curr_flip != char.flip:
            char.curr_flip = char.flip
            char.texture = pygame.transform.flip(char.texture, True, False)

pygame.quit()