from re import I, T
from turtle import back
import pygame
import math
import copy
import random

global WIDTH, HEIGHT, FPS, BACKGROUND, WHITE, SPEED, running
global characters, sounds, textures

pygame.init()
pygame.mixer.init()

font_name = pygame.font.SysFont("Impact", 37)

class Character:
    def __init__(self, ids=0, name="", image=["", 100, 100, 0], coord=[0, 0], speed=3, AI=[False, 0, 0], flip=0, direct=[0, 0], acc=[0, 0]):
        self.ids = ids
        self.name = name
        # Assuming font_name and WHITE are defined elsewhere
        self.name_render = font_name.render(name, True, WHITE)
        self.image = list(image)  # Assigning image as an attribute
        img = pygame.image.load(image[0])
        img = pygame.transform.scale(img, (image[1], image[2]))
        self.texture = img
        self.width = image[1]
        self.height = image[2]
        self.curr_flip = image[3]
        self.coord = list(coord)
        self.speed = speed
        self.AI = list(AI)
        self.flip = flip
        self.direct = list(direct)
        self.acc = list(acc)
        
    def __deepcopy__(self, memo=None):
        memo = memo or {}
        new_char = Character(
            ids=copy.deepcopy(self.ids, memo),
            name=copy.deepcopy(self.name, memo),
            image=copy.deepcopy(self.image, memo),
            coord=copy.deepcopy(self.coord, memo),
            speed=copy.deepcopy(self.speed, memo),
            AI=copy.deepcopy(self.AI, memo),
            flip=copy.deepcopy(self.flip, memo),
            direct=copy.deepcopy(self.direct, memo),
            acc=copy.deepcopy(self.acc, memo)
        )
        # Assuming font_name and WHITE are defined elsewhere
        new_char.name_render = font_name.render(new_char.name, True, WHITE)
        return new_char

clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
FPS = 60
BACKGROUND = [0,0,10,0]
WHITE = (255,255,255)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Fight v0.2")
pygame.display.set_icon(pygame.image.load("images\\icon.png"))
ANIM_X = 10
ANIM_Y = 25

# Characters and textures
imgt = "images\\"
characters_data = [
    Character(8, "Mr.Black", [imgt+"andr.png", 100, 100, 0], [100,100], 4),
    Character(1, "Sun", [imgt+"sun.png", 200, 200, 0], [500,500], 3, [True, 600, 600]),
    Character(4, "Skufislav", [imgt+"neStas.png", 100, 100, 0], [250,100], 4)
    ]

characters = copy.deepcopy(characters_data)

# Textures
textures = [
    pygame.transform.scale(pygame.image.load(imgt+"background2.png"), (WIDTH+2*ANIM_X, HEIGHT+2*ANIM_Y))
    ]

# Sounds
sd = "sounds\\"
sounds = [
    pygame.mixer.Sound(sd+"music.mp3"),
    pygame.mixer.Sound(sd+"eaten.mp3")
    ]

def nframe():
    global BACKGROUND
    global characters, textures
    win.fill((BACKGROUND[0], BACKGROUND[1], BACKGROUND[2]))
    vert_anim = ANIM_Y*math.sin( (timer_curr[1] - timer_last[1])/1000*math.pi*2 )
    hor_anim = ANIM_X*math.sin( (timer_curr[1] - timer_last[1])/2000*math.pi*2 )
    win.blit(textures[0], (hor_anim-ANIM_X, vert_anim-ANIM_Y))
    for char in characters:
        win.blit(char.texture, ( char.coord[0]+hor_anim, char.coord[1]+vert_anim) )
    for char in characters:
        win.blit(char.name_render, ( char.coord[0]+char.width//2-char.name_render.get_width()//2+hor_anim, char.coord[1]-char.name_render.get_height()+vert_anim ))
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
      
def distanceCHAR(char1, char2):
    return ((char1.coord[0]+char1.width/2-char2.coord[0]-char2.width/2)**2 + (char1.coord[1]+char1.height/2-char2.coord[1]-char2.height/2)**2)**0.5

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def distanceTO(char1, x2, y1):
    return ((char1.coord[0]+char1.width/2-x2)**2 + (char1.coord[1]+char1.height/2-y2)**2)**0.5

# --=Game~Code=-- #

sounds[0].play()

timer_last = [pygame.time.get_ticks(), pygame.time.get_ticks()]
timer_interval = [(sounds[0].get_length()+1)*1000, 2000]
running = True
while running:
    timer_curr = [pygame.time.get_ticks(), pygame.time.get_ticks()]
    # Background animation
    if timer_curr[1] - timer_last[1] > timer_interval[1]:
        timer_last[1] = timer_curr[1]

    # Music
    if timer_curr[0] - timer_last[0] > timer_interval[0]:
        sounds[0].play()
        timer_last[0] = timer_curr[0]

    exit_func()
    nframe()
    clock.tick(FPS)
    
    characters = sorted(characters, key= lambda x: x.coord[1]+x.height)

    # Background color animation
    if BACKGROUND[3] == 0:
        BACKGROUND[2] += 1
    elif BACKGROUND[3] == 1:
        BACKGROUND[2] -= 1  
    if BACKGROUND[3] == 0 and BACKGROUND[2] >= 30:
        BACKGROUND[3] = 1
    elif BACKGROUND[3] == 1 and BACKGROUND[2] <= 10:
        BACKGROUND[3] = 0

    # Character in-game processing
    for char in characters:     
        
        char.acc = [0, 0]
        control_check = False

        # Mr.Black control exclusive
        if char.ids == 8:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                char.acc[1]= -0.05
                control_check = True
            if keys[pygame.K_s]:
                char.acc[1]= 0.05
                control_check = True
            if keys[pygame.K_a]:
                char.acc[0]= -0.05
                control_check = True
            if keys[pygame.K_d]:
                char.acc[0]= 0.05
                control_check = True
        
        # Skufislav control exclusive
        if char.ids == 4:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                char.acc[1]= -0.05
                control_check = True
            if keys[pygame.K_DOWN]:
                char.acc[1]= 0.05
                control_check = True
            if keys[pygame.K_LEFT]:
                char.acc[0]= -0.05
                control_check = True
            if keys[pygame.K_RIGHT]:
                char.acc[0]= 0.05
                control_check = True

        # Flip
        if char.flip == 0 and char.acc[0] > 0:
            char.flip = 1
        elif char.flip == 1 and char.acc[0] < 0:
            char.flip = 0
        if char.curr_flip != char.flip:
            char.curr_flip = char.flip
            char.texture = pygame.transform.flip(char.texture, True, False)
        
        # AI
        if char.AI[0]==True:
            
            if distanceTO(char, char.AI[1], char.AI[2])<=10:
                char.AI[1] = random.randint(char.width//2, WIDTH-char.width//2)
                char.AI[2] = random.randint(char.height//2, HEIGHT-char.height//2)
                
            x2 = char.coord[0]+char.width/2
            y2 = char.coord[1]+char.height/2
            x1 = char.AI[1]
            y1 = char.AI[2]
            modulo3 = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if modulo3 != 0:
                char.acc[0] += 0.05*(x1-x2)/(modulo3)
                char.acc[1] += 0.05*(y1-y2)/(modulo3)
        

        # Char self movement
        char.direct[0] += char.acc[0]
        char.direct[1] += char.acc[1]

        modulo = ( char.direct[0]**2 + char.direct[1]**2 )**0.5
        if char.acc==[0,0] and modulo > 0:
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



        # Sun influence
        if char.ids != 1:
            for char2 in characters:
                if char2.ids == 1:
                    x2 = char2.coord[0]+char2.width/2
                    y2 = char2.coord[1]+char2.height/2
                    x1 = char.coord[0]+char.width/2
                    y1 = char.coord[1]+char.height/2
                    modulo2 = ((x2-x1)**2 + (y2-y1)**2)**0.5
                    if modulo2 > 1 and modulo2 < 250:
                        char.acc[0] += 1.2*(x2-x1)/(modulo2**1.5)
                        char.acc[1] += 1.2*(y2-y1)/(modulo2**1.5)
                    elif modulo2 <= 1:
                        char.acc[0] += 1.2*(x2-x1)/(1)
                        char.acc[1] += 1.2*(y2-y1)/(1)
                    
        char.direct[0] += char.acc[0]
        char.direct[1] += char.acc[1]

        char.coord[0] += char.direct[0] * char.speed
        char.coord[1] += char.direct[1] * char.speed
        
        if char.coord[0]+char.width>WIDTH:
            char.coord[0] = WIDTH - char.width
            if char.direct[0]>0: char.direct[0]=0
        elif char.coord[0] < 0:
            char.coord[0] = 0
            if char.direct[0]<0: char.direct[0]=0
            
        if char.coord[1]+char.height>HEIGHT:
            char.coord[1] = HEIGHT - char.height
            if char.direct[1]>0: char.direct[1]=0
        elif char.coord[1] < 0:
            char.coord[1] = 0
            if char.direct[1]<0: char.direct[1]=0
            
        if char.ids != 1:
            for char2 in characters:
                if char2.ids == 1:
                    if distanceCHAR(char, char2) < 5:
                        characters.remove(char)
                        sounds[1].play()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        characters = copy.deepcopy(characters_data)

pygame.quit()