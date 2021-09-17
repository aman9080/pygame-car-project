import pygame, math, sys
from pygame.locals import *
import time
pygame.font.init()

pygame.display.set_caption("car driving")


TURN_SPEED = 7
ACCELERATION = 10
MAX_FORWARD_SPEED = 3
MAX_REVERSE_SPEED = 2


BG = (0, 0, 190)
disp_x=1200
disp_y=600
screen = pygame.display.set_mode((disp_x,disp_y))



car = pygame.image.load('car.png')
import random

car1 = pygame.image.load('car 3.png')
car1X=(random.randint(20,disp_x-200))
car1Y=(random.randint(20,disp_y))
car1Y_change=20

car2 = pygame.image.load('ball.png')
car2X=(random.randint(20,disp_x-400))
car2Y=(random.randint(20,disp_y))
car2Y_change=30

car3 = pygame.image.load('star.png')
car3X=(random.randint(20,disp_x-300))
car3Y=(random.randint(20,disp_y))
car3Y_change=30



pygame.mixer.init()
horn = pygame.mixer.Sound('car-horn.wav')
blast =pygame.mixer.Sound('massenger.mp3')


clock = pygame.time.Clock()  # load clock
k_up = k_down = k_left = k_right = 0  # init key values
speed = direction = 0  # start speed & direction
position = (100, 100)  # start position

over_font=pygame.font.SysFont("SFNT",100)

play = True
while play:
    # USER INPUT
    clock.tick(30)
    # get events from the user
    for event in pygame.event.get():
        # not a key event
        if not hasattr(event, 'key'):
            continue
        # check if presses a key or left it
        down = event.type == KEYDOWN
        up = event.type == KEYUP # key down or up?

        if event.key == K_RIGHT:
            k_right = up * TURN_SPEED
        elif event.key == K_LEFT:
            k_left = up * TURN_SPEED
        elif event.key == K_UP:
            MAX_FORWARD_SPEED += 2
            k_up = up * MAX_FORWARD_SPEED

        elif event.key == K_DOWN:
            MAX_FORWARD_SPEED -=MAX_REVERSE_SPEED
            k_up = up * MAX_FORWARD_SPEED

        elif event.key == K_RETURN:
            horn.play()
        elif event.key == K_ESCAPE:
            play = False


    screen.fill(BG)
    # SIMULATION
    # .. new speed and direction based on acceleration and turn
    speed += (k_up + k_down)
    if speed > MAX_FORWARD_SPEED:
        speed = MAX_FORWARD_SPEED
    if speed < MAX_REVERSE_SPEED:
        speed = MAX_REVERSE_SPEED
    direction += (k_right - k_left)  # TODO is this the right direction?
    # .. new position based on current position, speed and direction
    x, y = position
    rad = direction * math.pi / 180

    x += speed * math.sin(rad)
    y += speed * math.cos(rad)
    # make sure the car doesn't exit the screen
    if y < 0:
        y = 0  # TODO is there another way to treat this?
    elif y > 600:
        y = 600
    if x < 0:
        x = 0
    elif x > 1200:
        x = 1200
    position = (x, y)
    # RENDERING
    # .. rotate the car image for direction
    rotated = pygame.transform.rotate(car, direction)
    # .. position the car on screen
    rect = rotated.get_rect()
    rect.center = position
    print(position)
    screen.blit(rotated, rect)

    distance1 = math.sqrt(((x)-(car1X+32))**2+((y)-(car1Y+32))**2)
    distance2 = math.sqrt(((x) - (car2X + 32)) ** 2 + ((y) - (car2Y + 32)) ** 2)

    if distance1 < 35 or distance2 < 35:
        car1Y_change=0
        car2Y_change=0
        car3Y_change = 0
        distance1 = 0
        distance2 =0

        horn.play()
        over = over_font.render("GAME OVER ", True, (255, 255, 0))
        screen.blit(over, (400, 200))
    for i in range(0,10):
        distance = math.sqrt(((x+32)-(car3X+32))**2+((y+32)-(car3Y+32))**2)
        if distance <40:
            car3X=random.randint(20,disp_x)
            car3Y=random.randint(20,disp_y)
            blast.play()



    screen.blit(car1,(car1X,car1Y))
    screen.blit(car2, (car2X, car2Y))
    screen.blit(car3, (car3X, car3Y))


    car1Y += car1Y_change
    car1X += 0
    car2Y += car2Y_change
    car2X += 0
    car3Y +=0
    car3X += 0

    print()



    if car1Y > 600:
        car1Y = -10
    if car1X > 1200:
        car1X = -10

    if car2Y > 600:
        car2Y = -30
    if car2X > 1200:
        car2X = -30



    pygame.display.flip()

sys.exit(0)
# quit the game
