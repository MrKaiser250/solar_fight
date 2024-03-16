import pygame

global WIDTH, HEIGHT, FPS, BLACK, WHITE

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1280, 720
FPS = 30
BLACK = (0,0,0)
WHITE = (255,255,255)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cursor-Battle")

def nframe():
	global mouse_coords, client_mouse_coords, GREEN, BLACK, WHITE, draw_white, draw_green
	win.fill(BLACK)
	pygame.draw.rect(win, WHITE, pygame.Rect(0, 0, 20, 20))
	pygame.display.flip()

while True:
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			
		nframe()
		clock.tick(FPS)