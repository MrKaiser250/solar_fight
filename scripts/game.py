from re import T
import pygame

global WIDTH, HEIGHT, FPS, BLACK, WHITE, running
global player1_coord

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
FPS = 60
BLACK = (0,0,50)
WHITE = (255,255,255)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Fight v0.1")

# Loading
imgt = "C:\\Users\\Станислав\\Documents\\GitHub\\solar_fight\\images\\"
player1_img = pygame.image.load(imgt+"andr.png")
player1_img = pygame.transform.scale(player1_img, (100, 100))

def nframe():
	global BLACK, WHITE, x_rec, y_rec
	win.fill(BLACK)
	win.blit(player1_img, player1_coord)
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
      



player1_coord = [0, 0]
running = True
while running:
    exit_func()
    nframe()
    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_coord[1]-=5
    elif keys[pygame.K_s]:
        player1_coord[1]+=5
    if keys[pygame.K_a]:
        player1_coord[0]-=5
    elif keys[pygame.K_d]:
        player1_coord[0]+=5

pygame.quit()