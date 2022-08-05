import pygame, sys, random
from pygame.locals import *

pygame.init()

MARGIN = 90
WHITE = (255,255,255)
BLACK = (0,0,0)


SCREEN = pygame.display.set_mode((480,480))
CLOCK = pygame.time.Clock()


class ColorBrick:
    def __init__(self, pos, image):
        self.rect = pygame.Rect(MARGIN + pos[0] * 50 + 2, MARGIN + pos[1] * 50 + 2, 50, 50)
        self.state = False
        self.image = image
        self.open_side = pygame.transform.scale(pygame.image.load(image), (48,48))
        self.close_side = pygame.transform.scale(pygame.image.load("Sprite/sprite_0.png"), (48,48))
        self.state_clock = 0
        self.find = False

    def draw(self, screen):
        if self.state:
            SCREEN.blit(self.open_side, self.rect)

            if self.state_clock > 0 and not self.find:
                self.state_clock -= 1

                if self.state_clock == 0:
                    self.state = False

        else:
            SCREEN.blit(self.close_side, self.rect)

    def collide_control(self, pos):
        if self.rect.collidepoint(pos):
            self.state = True
            return True
        return False

    def set_state_clock(self):
        self.state_clock = 60

def draw_line():
    for x in range(MARGIN,391,50):
        pygame.draw.line(SCREEN, BLACK, (MARGIN, x), (390,x), 2)

    for y in range(MARGIN,391,50):
        pygame.draw.line(SCREEN, BLACK, (y,MARGIN), (y,390), 2)

def create_image():
    path = "Sprite/sprite_"
    surfs = []
    for i in range(1,19):
        surfs.append(f"{path}{i}.png")
    
    return surfs

def create_pos():
    pos = []
    for x in range(6):
        for y in range(6):
            pos.append([x,y])
            
    return pos

def create_color_brick():
    colors = create_image()
    pos = create_pos()
    random.shuffle(pos)

    rect_list = []

    while colors:
        color = colors[0]
        for i in range(2):
            select_pos = random.choice(pos)
            rect_list.append(ColorBrick(select_pos, color))
            pos.remove(select_pos)

        colors.remove(color)

    return rect_list

bricks = create_color_brick()

first_select = None

while True:
    SCREEN.fill((0,0,0))

    for brick in bricks:
        brick.draw(SCREEN)

    draw_line()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for brick in bricks:
                if brick.collide_control(mouse_pos):
                    if not first_select:
                        first_select = brick
                    else:
                        if brick != first_select and brick.image == first_select.image:
                            first_select.find = True
                            brick.find = True
                            print(True)
                        else:
                            brick.set_state_clock()
                            first_select.set_state_clock()
                        
                        first_select = None

    pygame.display.update()
    CLOCK.tick(60)
