
# http://richard.cgpublisher.com/product/pub.84/prod.11
# INTIALISATION
import pygame, math, sys
from pygame.locals import *

TURN_SPEED = 6
ACCELERATION = 3
MAX_FORWARD_SPEED = 0
MAX_REVERSE_SPEED =5

BG = (0, 75, 100)


# initialize the screen with size (MAX_X, MAX_Y)
screen = pygame.display.set_mode((1200, 600))

car = pygame.image.load('car.png')
# initialize the sound mixer
pygame.mixer.init()

horn = pygame.mixer.Sound('car horror horn.mp3')
clock = pygame.time.Clock()  # load clock
k_up = k_down = k_left = k_right = 0  # init key values
speed = direction = 0  # start speed & direction
position = (100, 100)  # start position

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
        # key events: http://pygame.org/docs/ref/key.html
        if event.key == K_RIGHT:
            k_right = up * TURN_SPEED
        elif event.key == K_LEFT:
            k_left = up * TURN_SPEED
        elif event.key == K_UP:
            k_up = up * MAX_FORWARD_SPEED
        elif event.key == K_DOWN:
            k_down = up * 0
        elif event.key == K_RETURN:
            horn.play()  # TODO honk twice if you feel nice
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
    elif y > MAX_Y:
        y = MAX_Y
    if x < 0:
        x = 0
    elif x > MAX_X:
        x = MAX_X
    position = (x, y)
    # RENDERING
    # .. rotate the car image for direction
    rotated = pygame.transform.rotate(car, direction)
    # .. position the car on screen
    rect = rotated.get_rect()
    rect.center = position
    print(position)
    # .. render the car to screen
    screen.blit(rotated, rect)
    pygame.display.flip()

sys.exit(0)  # quit the game

