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
        if (self.rect.x > screen_width - 50):
            self.rect.x = screen_width - 50
        if (self.rect.y < 0):
            self.rect.y = 0
        if (self.rect.y > screen_height - 50):
            self.rect.y = screen_height - 50
        
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
gotten_cow_number = False
reel_win = False
gotten_score = False
ufo_front = pygame.image.load("ufo_new_front.png")
ufo_back = pygame.image.load("ufo_new_back.png")
ufo_left = pygame.image.load("ufo_new_left.png")
ufo_right = pygame.image.load("ufo_new_right.png")
brown_cow = pygame.image.load("brown_cow.png")
golden_cow = pygame.image.load("golden_cow.png")
brown_spotted_cow = pygame.image.load("brown_spotted_cow.png")
black_cow = pygame.image.load("black_cow.png")
suited_cow = pygame.image.load("suited_cow.png")
background = pygame.image.load("background.jpg")
sell_unlit = pygame.image.load("sell_unlit.png")
sell_lit = pygame.image.load("sell_lit.png")
wait_time = 0
index = 0
reel_bar_height = 100
reel_height_change = 1
cow_height = 100
cow_height_change = 0
progress_bar_length = 50
win_status = 0
reel_win_time = 0
total_score = 0
score = 0
sell_counter = 0
hidden_score = 0


cow = {
    "type": ["Brown", "Brown Spotted", "Black", "Suited", "Golden"],
    "description": ["This milk is brown and tastes like dirt.", "This brown cow has some spots!", "Black cow haha", "Cow of Wall Street", "The milk is made out of gold- very heavy."],
    "difficulty": [50, 75, 30, 85, 100],
    "base_score": [50, 75, 30, 120, 150]
}

def fps_counter():
    fps = clock.get_fps()
    my_font = pygame.font.SysFont('Calibri', 30)
    text_surface = my_font.render(str(round(fps)) + " fps", False, (255, 255, 255))
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
        #print("index: " + str(index))

def reel_game():
    global reel_bar_height
    global reel_height_change
    changing_direction = False
    global cow_height
    global cow_height_change
    global win_status
    global progress_bar_length

    #---------win logic------------

    if (progress_bar_length > 200):
        #win
        win_status = 2
    elif (progress_bar_length <= 0):
        #lose
        win_status = 1
    else:
        #currently playing
        win_status = 0

    #---------logic for player---------

    if (reel_bar_height >= player.rect.y + 150):
        if (reel_height_change > 2):
            reel_height_change = reel_height_change * -0.75
            #print("CHANGING DIRECTIon")
            changing_direction = True
        else:
            reel_bar_height = player.rect.y + 150
            #print("resetting height")
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

    #print("reel_height_change: " + str(reel_height_change))
    
    #-----------cow time------------
    
    big_brown_cow = pygame.transform.scale(brown_cow, (50, 50))
    #print("player y", player.rect.y)
    
    #reset cow position because im lazy to properly spawn in cow correctly
    if (cow_height < player.rect.y - 125 or cow_height > player.rect.y + 80):
        cow_height = player.rect.y

    #every frame, cow approaches zero change
    if (cow_height_change > 0):
        cow_height_change -= 0.03
    else:
        cow_height_change += 0.03
    """
    if (cow_height_change < 0.03 or cow_height_change > -0.03):
        cow_height_change = 0
    """

    move_randomness = random.randint(1, cow["difficulty"][0])
    up_or_down = random.randint(1, 2)
    if (move_randomness == 1):
        if (up_or_down == 1):
            cow_height_change = 2.5
        else:
            cow_height_change = -2.5

    #cow height limit
    if (cow_height <= player.rect.y - 112):
        cow_height = player.rect.y - 112
    elif (cow_height >= player.rect.y + 63):
        cow_height = player.rect.y + 63

    cow_height += cow_height_change

    #---------progress bar logic--------

    if (cow_height + 33 > reel_bar_height - 100  and cow_height + 17 < reel_bar_height - 50):
        progress_bar_length += 0.5
    elif progress_bar_length > 0:
        progress_bar_length -= 0.5

    #-----------visuals------------

    #surrounding
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(player.rect.x + 100, player.rect.y - 100, 100, 200))
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(player.rect.x + 180, player.rect.y - 100, 20, 200))
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(player.rect.x + 140, player.rect.y - 100, 20, 200))

    #reeling bar
    pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x + 160, reel_bar_height - 100, 20, 50))

    #cow
    screen.blit(big_brown_cow, (player.rect.x + 145, cow_height))

    #progress bar
    pygame.draw.rect(screen, GREEN, pygame.Rect(player.rect.x + 100, player.rect.y - progress_bar_length + 100, 20, progress_bar_length))

    #guidelines for adjusting
    """
    pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x, reel_bar_height - 100, 100, 1))
    pygame.draw.rect(screen, RED, pygame.Rect(player.rect.x, reel_bar_height - 50, 100, 1))
    pygame.draw.rect(screen, GREEN, pygame.Rect(player.rect.x, cow_height + 25, 100, 1))
    """

brown_cow = pygame.transform.scale(brown_cow, (100, 100))
brown_spotted_cow = pygame.transform.scale(brown_spotted_cow, (100, 100))
black_cow = pygame.transform.scale(black_cow, (100, 100))
suited_cow = pygame.transform.scale(suited_cow, (50, 50))
golden_cow = pygame.transform.scale(golden_cow, (100, 100))

def update_score():
    global total_score
    global hidden_score
    total_score += hidden_score
    hidden_score = 0


def reel_win_textbox():
    global reeling
    global gotten_cow_number
    global reel_win
    global cow_number
    global reel_win_time
    global total_score
    global gotten_score
    global score
    global hidden_score
    reeling = False
    reel_win = True

    if (not gotten_cow_number):
        cow_number = random.randint(0, 4)
        gotten_cow_number = True

    reel_win_time += 1

    if (gotten_score == False):
        score = cow["base_score"][cow_number] + random.randint(0, 30)
        hidden_score += score
        gotten_score = True

    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(player.rect.x, player.rect.y - 200, 200, 200))
    my_font = pygame.font.SysFont('Calibri', 24)
    total_text = "Congrats! You caught a " + cow["type"][cow_number] + " cow. " + cow["description"][cow_number] + ". It has a difficulty of " + str(cow["difficulty"][cow_number]) + ". It is worth " + str(score) + " points."
    textbox_box = pygame.Rect(player.rect.x, player.rect.y - 200, 200, 200)
    drawText(screen, total_text, BLACK, textbox_box, my_font)

    if (cow_number == 0):
        screen.blit(brown_cow, (player.rect.x + 110, player.rect.y - 80))
    elif (cow_number == 1):
        screen.blit(brown_spotted_cow, (player.rect.x + 110, player.rect.y - 80))
    elif (cow_number == 2):
        screen.blit(black_cow, (player.rect.x + 110, player.rect.y - 80))
    elif (cow_number == 3):
        screen.blit(suited_cow, (player.rect.x + 135, player.rect.y - 55))
    else:
        screen.blit(golden_cow, (player.rect.x + 110, player.rect.y - 80))


def reel_lose():
    global reeling
    print("You lost the cow.")
    reeling = False

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def reset_parameters():
    global index
    global click_hold_counter
    global bobber_down
    global caught_cow
    global reeling
    global reel_height_change
    global progress_bar_length
    global gotten_cow_number
    global win_status
    global reel_win_time
    global gotten_score

    index = 0
    click_hold_counter = 0
    print("reset")
    bobber_down = False
    caught_cow = False
    reeling = False
    reel_height_change = 1
    progress_bar_length = 50
    gotten_cow_number = False
    reeling = False
    win_status = 0
    bobber_down = False
    caught_cow = False
    reel_win_time = 0
    gotten_score = False
    
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    screen.fill(WHITE)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        if (not click and not reeling):
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
                elif event.key == pygame.K_t:
                    progress_bar_length = 100
                elif event.key == pygame.K_r:
                    index = 0
                    click_hold_counter = 0
                    print("reset")
                    bobber_down = False
                    caught_cow = False
                    reeling = False
                    reel_height_change = 1
                    progress_bar_length = 50
                    gotten_cow_number = False

                    
            if event.type == pygame.KEYUP:
                if (not player.change_x == 0 or not player.change_y == 0):
                    if event.key == pygame.K_a:
                        player.changespeed(2, 0)
                    elif event.key == pygame.K_d:
                        player.changespeed(-2, 0)
                    elif event.key == pygame.K_s:
                        player.changespeed(0, -2)
                    elif event.key == pygame.K_w:
                        player.changespeed(0, 2)

    background = pygame.transform.scale(background, (1280, 720))
    screen.blit(background, (0, 0))

    fps_counter()

    my_font = pygame.font.SysFont('Calibri', 30)
    text_surface = my_font.render("Score: " + (str(total_score)), False, (255, 255, 255))
    screen.blit(text_surface, (0, 40))

    sell_unlit = pygame.transform.scale(sell_unlit, (195, 150))
    sell_lit = pygame.transform.scale(sell_lit, (195, 150))

    if (sell_counter < 60):
        screen.blit(sell_lit, (1050, 50))
    elif(sell_counter >= 120):
        sell_counter = 0
        screen.blit(sell_unlit, (1050, 50))
    else:
        screen.blit(sell_unlit, (1050, 50))
    sell_counter += 1

    screen.blit(ufo_right, (player.rect.x,player.rect.y))

    if event.type == pygame.MOUSEBUTTONDOWN:
        player.change_x = 0
        player.change_y = 0
        
        click = True
        gotten_wait = False
 
        #print("mouse clicked")
        
        #pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_blocked(pygame.K_w)
        

    if event.type == pygame.MOUSEBUTTONUP:
        if (not caught_cow and not reeling):
            cast_line(click_hold_counter)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            if (not gotten_wait):
                wait_time = get_wait()
                gotten_wait = True
            wait_time -= 1
            if (wait_time <= 0):
                #index = 0
                catch_alert()
            #print("wait time: " + str(wait_time))
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

            #print(click_hold_counter)
            cast_distance(click_hold_counter)

    if (bobber_down and click and wait_time < 0 and wait_time > -100):
        #print("YOU caught THE COW")
        caught_cow = True
        reeling = True
        
    if (reeling and not win_status == 2):
        reel_game()
        #pygame.event.set_allowed(pygame.MOUSEMOTION)

    if (win_status == 2):
        reel_win_textbox()
        if (click and reel_win_time > 60):
            reset_parameters()
    elif (win_status == 1):
        reset_parameters()
        
    if (player.rect.x > 1000 and player.rect.y < 180):
        update_score()
    

    if (event.type == pygame.MOUSEBUTTONDOWN):
        cast_distance(click_hold_counter)

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

    pygame.display.flip()
 
    clock.tick(60)

pygame.quit()
