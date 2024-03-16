from re import T
import pygame

global WIDTH, HEIGHT, FPS, BLACK, WHITE, running

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
FPS = 30
BLACK = (0,0,0)
WHITE = (255,255,255)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar Fight")

def nframe():
	global BLACK, WHITE, x_rec, y_rec
	win.fill(BLACK)
	pygame.draw.rect(win, WHITE, pygame.Rect(x_rec, y_rec, 20, 20))
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
      



x_rec = 0
y_rec = 0
running = True
while running:
    exit_func()
    
    x_rec+=10
    y_rec+=10
    custom_delay(1000)
    
    nframe()
    clock.tick(FPS)

pygame.quit()