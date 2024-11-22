import pygame
import time
import math
from Utils import scale_image, blit_rotate_center

# Load images with scaling
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60

# Base class for all cars
class Car:
    def __init__(self, max_vel, rotation_vel, img, start_pos):
        self.img = img  # Image for the car
        self.max_vel = max_vel  # Maximum velocity
        self.vel = 0  # Current velocity
        self.rotation_vel = rotation_vel  # Rotation speed
        self.angle = 0  # Current angle of the car
        self.x, self.y = start_pos  # Starting position of the car
        self.acceleration = 0.1  # Acceleration rate

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel  # Reverse velocity direction
        self.move()

    def check_collision(self, track_border_mask, track_border_pos):
        # Create a mask for the car at its current position
        car_mask = pygame.mask.from_surface(self.img)
        car_offset = (self.x - track_border_pos[0], self.y - track_border_pos[1])

        # Check for collision by using the mask overlap function
        overlap = track_border_mask.overlap(car_mask, car_offset)
        if overlap:
            return True  # Collision detected
        return False

# Player car class, inheriting from the Car class
class PlayerCar(Car):
    def __init__(self, max_vel, rotation_vel):
        # Call the parent class constructor with the specific parameters
        super().__init__(max_vel, rotation_vel, GREEN_CAR, (180, 200))

# Function to draw the game elements
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

# Function to move the player car based on key presses
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

# Main game loop
run = True
clock = pygame.time.Clock()

# Images and their positions on the screen
images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    (FINISH, FINISH_POSITION),
    (TRACK_BORDER, (0, 0))
]

# Create the player car with specified max velocity and rotation velocity
player_car = PlayerCar(4, 4)

# Game loop
while run:
    clock.tick(FPS)

    # Check for collisions with the track border and make the car bounce
    if player_car.check_collision(TRACK_BORDER_MASK, (0, 0)):  # Assuming the border starts at (0, 0)
        player_car.bounce()

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    move_player(player_car)

pygame.quit()
