import pygame
import random
from pygame import mixer
import math
import time
import random
pygame.font.init()
 
# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0) 

mixer.init()
#bonk = mixer.Sound("bonk.mp3")
#good_hit = mixer.Sound("good_hit.mp3")
#bad_hit = mixer.Sound("bad_hit.mp3")
#mixer.music.set_volume(1)

screen_width = 1280
screen_height = 720

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
 
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if (self.rect.x < 0):
            self.rect.x = 0
        if (self.rect.x > screen_width - 15):
            self.rect.x = screen_width - 15
        if (self.rect.y < 0):
            self.rect.y = 0
        if (self.rect.y > screen_height - 15):
            self.rect.y = screen_height - 15
        

 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen

screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
 
# This is a list of every sprite. 
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
"""
for i in range(50):
    # This represents a block
    block = Block(GREEN, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
    good_block_list.add(block)
    all_sprites_list.add(block)
"""
 
# Create a RED player block
player = Player(20, 15)
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
click_hold_counter = 0 
increase = True
click = False
facing_up = False
facing_down = False
facing_left = False
facing_right = False
bobber_down = False
caught_cow = False
reeling = False
new_reel = False
reel_bar_height = 100
ufo_front = pygame.image.load("ufo_new_front.png")
ufo_back = pygame.image.load("ufo_new_back.png")
ufo_left = pygame.image.load("ufo_new_left.png")
ufo_right = pygame.image.load("ufo_new_right.png")
brown_cow = pygame.image.load("cow1.png")
wait_time = 0
index = 0
reel_height_change = 1

cow = {
    "cow": ["Brown", "Brown Spotted", "Black", "Regular Cow", "Golden"],
    "description": ["brown milk is brown", "this brown cow has some spots!", "black cow haha", "normal cow", "golden milk is heavy"]
}

def fps_counter():
    fps = clock.get_fps()
    my_font = pygame.font.SysFont('Calibri', 30)
    text_surface = my_font.render(str(round(fps)), False, (0, 0, 0))
    screen.blit(text_surface, (0,0))

def cast_distance(length):
    if (not reeling):
        pygame.draw.rect(screen, BLACK, pygame.Rect(player.rect.x + 95, player.rect.y - 10, 20, 60))
        pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x + 100, player.rect.y+50-length, 10, length))

def cast_line(length):
    if (facing_up):
        pygame.draw.rect(screen, BLACK, pygame.Rect(player.rect.x + 25, player.rect.y - (length*2), 5, 5))
    elif (facing_down):
        pygame.draw.rect(screen, BLACK, pygame.Rect(player.rect.x + 25, player.rect.y + 60 + (length*2), 5, 5))
    elif (facing_right):
        pygame.draw.rect(screen, BLACK, pygame.Rect(player.rect.x + 60 + (length*2), player.rect.y + 25, 5, 5))
    else:
        pygame.draw.rect(screen, BLACK, pygame.Rect(player.rect.x - (length*2), player.rect.y + 25, 5, 5))

def get_wait():
    return (random.randint(1, 5) * 60)

def catch_alert():
    global index
    index += 1
    if ((index > 0 and index < 5) or (index > 10 and index < 15)):
        pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x + 40, player.rect.y - 10, 20, 20))
        print("index: " + str(index))

def reel_game():
    #surrounding
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(player.rect.x + 100, player.rect.y - 100, 100, 200))
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(player.rect.x + 180, player.rect.y - 100, 20, 200))
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(player.rect.x + 140, player.rect.y - 100, 20, 200))

    #reeling bar
    pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x + 160, reel_bar_height - 100, 20, 50))

    #cow time
    big_brown_cow = pygame.transform.scale(brown_cow, (50, 50))
    screen.blit(big_brown_cow, (player.rect.x + 150, player.rect.y))


clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    screen.fill(WHITE)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        if (not click):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    facing_left = True
                    facing_right = False
                    facing_up = False
                    facing_down = False
                    player.changespeed(-2, 0)
                elif event.key == pygame.K_d:
                    facing_right = True
                    facing_left = False
                    facing_up = False
                    facing_down = False
                    player.changespeed(2, 0)
                elif event.key == pygame.K_s:
                    facing_down = True
                    facing_up = False
                    facing_left = False
                    facing_right = False
                    player.changespeed(0, 2)
                elif event.key == pygame.K_w:
                    facing_up = True
                    facing_down = False
                    facing_left = False
                    facing_right = False
                    player.changespeed(0, -2)
                elif event.key == pygame.K_r:
                    index = 0
                    click_hold_counter = 0
                    print("spacebar")
                    bobber_down = False
                    caught_cow = False
                    reeling = False
                    reel_height_change = 1

                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.changespeed(2, 0)
                elif event.key == pygame.K_d:
                    player.changespeed(-2, 0)
                elif event.key == pygame.K_s:
                    player.changespeed(0, -2)
                elif event.key == pygame.K_w:
                    player.changespeed(0, 2)

    fps_counter()

    if event.type == pygame.MOUSEBUTTONDOWN:
        
        click = True
        gotten_wait = False
 
        #print("mouse clicked")
        
        #pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_blocked(pygame.K_w)
        

    if event.type == pygame.MOUSEBUTTONUP:
        if (not caught_cow):
            cast_line(click_hold_counter)
            if (not gotten_wait):
                wait_time = get_wait()
                gotten_wait = True
            wait_time -= 1
            if (wait_time <= 0):
                #index = 0
                catch_alert()
            print("wait time: " + str(wait_time))
            bobber_down = True
        click = False
            #click_hold_counter = 0
   
    if (click):
        if (not reeling):
            if (click_hold_counter < 0):
                increase = True
            elif (click_hold_counter > 60):
                increase = False

            if (increase): click_hold_counter += 1
            else: click_hold_counter -= 1

            print(click_hold_counter)
            cast_distance(click_hold_counter)

    if (bobber_down and click and wait_time < 0 and wait_time > -100):
        #print("YOU caught THE COW")
        caught_cow = True
        reeling = True
    
    if (reeling):
        changing_direction = False
        if (reel_bar_height >= player.rect.y + 150):
            if (reel_height_change > 2):
                reel_height_change = reel_height_change * -0.75
                print("CHANGING DIRECTIon")
                changing_direction = True
            else:
                reel_bar_height = player.rect.y + 150
                print("resetting height")
        if (reel_bar_height <= player.rect.y):
            reel_bar_height = player.rect.y

        #if bar is at top or bottom, set change to 1
        if ((reel_bar_height >= player.rect.y + 150 or reel_bar_height <= player.rect.y) and not changing_direction):
            reel_height_change = 0

        if (click):
            reel_height_change -= 0.2
            #limiting max reel height change speed
            if (reel_height_change < -5.00):
                reel_height_change = -5.00
        
            reel_bar_height += reel_height_change
            
        
        if (not click):
            reel_height_change += 0.2
            #limiting max reel fall speed
            if (reel_height_change > 5.0):
                reel_height_change = 5.0
            
            reel_bar_height += reel_height_change

        
                

        print("reel_height_change: " + str(reel_height_change))
        
        reel_game()



    #fish_index = random.randint(0, 2)
    #print(fishdict["fish"][fish_index] + " | Description: " + fishdict["description"][fish_index])
     
    # See if the player block has collided with anything.
    #good_blocks_hit_list = pygame.sprite.spritecollide(player, good_block_list, True)


   
    
    
    if (event.type == pygame.MOUSEBUTTONDOWN):
        cast_distance(click_hold_counter)


    # Draw all the spites
    #all_sprites_list.draw(screen)
    all_sprites_list.update()


    ufo_front = pygame.transform.scale(ufo_front, (50, 50))
    ufo_back = pygame.transform.scale(ufo_back, (50, 50))
    ufo_left = pygame.transform.scale(ufo_left, (50, 50))
    ufo_right = pygame.transform.scale(ufo_right, (50, 50))

    if (facing_up):
        screen.blit(ufo_back, (player.rect.x,player.rect.y))
    if (facing_down):
        screen.blit(ufo_front, (player.rect.x,player.rect.y))
    if (facing_left):
        screen.blit(ufo_left, (player.rect.x,player.rect.y))
    if (facing_right):
        screen.blit(ufo_right, (player.rect.x,player.rect.y))

 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

    #displays average fps
    
 
pygame.quit()
