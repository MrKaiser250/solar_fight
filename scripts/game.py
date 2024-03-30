from dataclasses import dataclass
from re import I, T
from turtle import back
import pygame
import math
import copy
import random
import os

global WIDTH, HEIGHT, FPS, BACKGROUND, WHITE, SPEED, running
global characters, sounds, textures

pygame.init()
pygame.mixer.init()

font_name = pygame.font.SysFont("Impact", 37)


def split_folder_into_frames(folder_path, target_width, target_height):
    frames = []
    # Get a list of all files in the folder
    file_names = os.listdir(folder_path)
    # Sort the file names alphabetically
    sorted_file_names = sorted(file_names)
    # Loop through sorted file names
    for file_name in sorted_file_names:
        # Check if the file is a PNG
        if file_name.endswith('.png'):
            # Construct the full path to the image file
            file_path = os.path.join(folder_path, file_name)
            # Load the image file
            frame_surface = pygame.image.load(file_path).convert_alpha()
            # Transform the frame to the target width and height
            frame_surface = pygame.transform.scale(frame_surface, (target_width, target_height))
            # Append the frame to the list of frames
            frames.append(frame_surface)
    return frames


class Character:
    def __init__(self, ids=0, name="", image=["", 100, 100, 0], coord=[0, 0], speed=3, AI=[False, 0, 0], flip=0, direct=[0, 0], acc=[0, 0]):
        self.ids = ids
        self.name = name
        self.name_render = font_name.render(name, True, WHITE)
        self.image = list(image)
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
        new_char.name_render = font_name.render(new_char.name, True, WHITE)
        return new_char


class Projectile:
    def __init__(self, ids=0, name="", image=["", 100, 100], coord=[0, 0], speed=3, direct=[0, 0], rotation = 0, acc=[0, 0], death_timer = 100):
        self.ids = ids
        self.name = name
        self.image = list(image)
        if os.path.isdir(image[0]):  # Check if the path is a directory
            self.frames = split_folder_into_frames(image[0], image[1], image[2])  # Load frames from folder
            self.current_frame_index = 0
            self.texture = self.frames[self.current_frame_index] if self.frames else None
        else:  # If not a directory, assume it's a single image
            img = pygame.image.load(image[0])
            img = pygame.transform.scale(img, (image[1], image[2]))
            self.texture = img
        self.width = image[1]
        self.height = image[2]
        self.coord = list(coord)
        self.speed = speed
        self.direct = list(direct)
        self.acc = list(acc)
        self.death_timer = death_timer
        self.rotation = rotation
        self.birth_time = pygame.time.get_ticks()
        
    def __deepcopy__(self, memo=None):
        memo = memo or {}
        new_proj = Projectile(
            ids=copy.deepcopy(self.ids, memo),
            name=copy.deepcopy(self.name, memo),
            image=copy.deepcopy(self.image, memo),
            coord=copy.deepcopy(self.coord, memo),
            speed=copy.deepcopy(self.speed, memo),
            direct=copy.deepcopy(self.direct, memo),
            rotation=copy.deepcopy(self.rotation, memo),
            acc=copy.deepcopy(self.acc, memo),
            death_timer=copy.deepcopy(self.death_timer, memo)
        )
        return new_proj

    def direct_with_rotation(self):
        self.direct[0] = math.cos(math.radians(self.rotation))
        self.direct[1] = math.sin(math.radians(self.rotation))
        
    def update_animation(self):
        if hasattr(self, 'frames'):  # Check if frames exist (i.e., if it's a GIF)
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame_index]

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
    Character(8, "Mr.Black", [imgt+"andr.png", 120, 120, 0], [100,100], 4),
    Character(1, "Sun", [imgt+"sun.png", 200, 200, 0], [500,500], 3, [True, 600, 600]),
    Character(4, "Skufislav", [imgt+"stas.png", 80, 80, 0], [250,100], 4)
    ]

projectiles_data = [
    Projectile(1, "Wave", [imgt+"wave\\", 40, 20], [0,0], 10, [0,0], 0, [0,0], 10000),
    Projectile(1, "Wave", [imgt+"wave\\", 40, 20], [0,0], 13, [0,0], 0, [0,0], 10000)
    ]

attack_data_data = [
    [1,100,3,3,2000,7],
    [2,50,100,100,5000,1],
    [3,100,100,100,5000,1]
    ]

characters = copy.deepcopy(characters_data)
projectiles = []

# Textures
textures = [
    pygame.transform.scale(pygame.image.load(imgt+"background2.png"), (WIDTH+2*ANIM_X, HEIGHT+2*ANIM_Y))
    ]

# Sounds
sd = "sounds\\"
sounds = [
    pygame.mixer.Sound(sd+"music.mp3"),
    pygame.mixer.Sound(sd+"eaten.mp3"),
    pygame.mixer.Sound(sd+"shot1.mp3"),
    pygame.mixer.Sound(sd+"shot2.mp3")
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
    for proj in projectiles:
        proj.update_animation()
        proj.texture = pygame.transform.rotate(proj.texture, -proj.rotation)
        win.blit(proj.texture, ( proj.coord[0]+hor_anim, proj.coord[1]+vert_anim ) )
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

def closestEnemy(characters, char):
    min_distance = float('inf')
    closest_enemy = None
    
    for char2 in characters:
        if char2.ids != char.ids:  # Ensure char2 is not the same character
            distance = distanceCHAR(char2, char)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = char2
                
    return closest_enemy

def angle(x, y):
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360
    return angle_deg


ROTATION_ATTACK = 0

def attack(data, char):
    global projectiles, ROTATION_ATTACK
    if data[0]==1:
        if len(characters)>1:
            target = closestEnemy(characters, char)
            deltaX = target.coord[0] + target.width / 2 - char.coord[0] - char.width / 2
            deltaY = target.coord[1] + target.height / 2 - char.coord[1] - char.height / 2
            proj = copy.deepcopy(projectiles_data[0])
            proj.rotation = angle(deltaX, deltaY)
            proj.direct_with_rotation()
            proj.texture = pygame.transform.rotate(proj.texture, -proj.rotation)
            proj.coord[0] = char.coord[0] - proj.texture.get_width()/2 + char.width/2
            proj.coord[1] = char.coord[1] - proj.texture.get_height()/2 + char.height/2
            projectiles.append(proj)
            sounds[2].play()
    elif data[0]==2:
        target = closestEnemy(characters, char)
        deltaX = target.coord[0] + target.width / 2 - char.coord[0] - char.width / 2
        deltaY = target.coord[1] + target.height / 2 - char.coord[1] - char.height / 2
        proj = copy.deepcopy(projectiles_data[1])
        proj.rotation = angle(deltaX, deltaY)
        proj.direct_with_rotation()
        proj.texture = pygame.transform.rotate(proj.texture, -proj.rotation)
        proj.coord[0] = char.coord[0] - proj.texture.get_width()/2 + char.width/2
        proj.coord[1] = char.coord[1] - proj.texture.get_height()/2 + char.height/2
        projectiles.append(proj)
    elif data[0]==3:
        proj = copy.deepcopy(projectiles_data[1])
        proj.rotation = ROTATION_ATTACK
        ROTATION_ATTACK = (ROTATION_ATTACK + 5) % 360
        proj.direct_with_rotation()
        proj.texture = pygame.transform.rotate(proj.texture, -proj.rotation)
        proj.coord[0] = char.coord[0] - proj.texture.get_width()/2 + char.width/2
        proj.coord[1] = char.coord[1] - proj.texture.get_height()/2 + char.height/2
        projectiles.append(proj)
        
        

def attack_interval(data, char):
    global attack_data_data, ROTATION_ATTACK
    if data[5] <= 0:
        ROTATION_ATTACK = random.randint(0, 359)

        data2 = random.choice(attack_data_data)
        for i in range(len(data2)):
            data[i]=data2[i]
        if data[0]==2:
            sounds[3].play()
        return data[1]
    elif data[3] <= 0:
        data[3] = data[2]
        data[5] -= 1
        return data[4]
    else:
        data[3] -= 1
        attack(data, char)
        return data[1]


# --=Game~Code=-- #

sounds[0].play()

timer_last = [pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()]
timer_interval = [(sounds[0].get_length()+1)*1000, 2000, 0]
attack_data = [0, 0, 0, 0, 0, 0] # Attack type, time between units, number of units, number of units (curr), time between attacks, number of attacks
attack_data2 = []
running = True
while running:
    timer_curr = [pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()]
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
        BACKGROUND[2] += 2
    elif BACKGROUND[3] == 1:
        BACKGROUND[2] -= 2  
    if BACKGROUND[3] == 0 and BACKGROUND[2] >= 80:
        BACKGROUND[3] = 1
    elif BACKGROUND[3] == 1 and BACKGROUND[2] <= 40:
        BACKGROUND[3] = 0

    # Character in-game processing
    for char in characters:     
        
        if char.ids == 1 and timer_curr[2] - timer_last[2] > timer_interval[2]:
            timer_last[2] = timer_curr[2]
            timer_interval[2] = attack_interval(attack_data, char)

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
    
    for proj in projectiles:
        if pygame.time.get_ticks() - proj.birth_time > proj.death_timer:
            projectiles.remove(proj)
        else:            
            proj.direct[0] += proj.acc[0]
            proj.direct[1] += proj.acc[1]
            proj.coord[0] += proj.direct[0] * proj.speed
            proj.coord[1] += proj.direct[1] * proj.speed
            
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        characters = copy.deepcopy(characters_data)
        projectiles = []
        attack_data = [0,0,0,0,0,0]

pygame.quit()