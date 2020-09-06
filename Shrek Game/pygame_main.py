__author__ = 'Lexy'  # put your name here!!!

import pygame, sys, traceback, random
from pygame.locals import *

GAME_MODE_MAIN = 0
GAME_MODE_TITLE_SCREEN = 1
GAME_MODE_GAME_OVER = 2
GAME_MODE_YOU_WON = 3

# import your classFiles here.
from ShrekFile import Shrek
from LordFile import Lord
from PieFile import Pie

# =====================  setup()
def setup():
    """
    This happens once in the program, at the very beginning.
    """
    global buffer, objects_on_screen, objects_to_add, bg_color, game_mode
    global the_shrek, the_lord, the_pie, splat_sound, cork_sound , hits, number_of_pies , misses

    pygame.mixer.init()
    splat_sound = pygame.mixer.Sound("splat.wav")
    cork_sound = pygame.mixer.Sound("cork.wav")

    buffer = pygame.display.set_mode((600, 600))
    objects_on_screen = []  # this is a list of all things that should be drawn on screen.
    objects_to_add = [] #this is a list of things that should be added to the list on screen. Put them here while you
                        #   are in the middle of the loop, and they will be added in later in the loop, when it is safe
                        #   to do so.
    bg_color = pygame.Color("darkgreen")  # you can find a list of color names at https://goo.gl/KR7Pke
    game_mode = GAME_MODE_MAIN
    # Add any other things you would like to have the program do at startup here.
    the_shrek = Shrek()
    objects_on_screen.append(the_shrek)

    the_lord = Lord()
    objects_on_screen.append(the_lord)

    the_pie = Pie()
    objects_on_screen.append(the_pie)
    the_pie.x = 3000

    hits = 0
    misses = 0
    number_of_pies = 5

# =====================  loop()
def loop(delta_T):
    """
     this is what determines what should happen over and over.
     delta_T is the time (in seconds) since the last loop() was called.
    """
    global game_mode
    buffer.fill(bg_color) # wipe the screen with the background color.
    if game_mode == GAME_MODE_MAIN:
        animate_objects(delta_T)

        # place any other code to test interactions between objects here. If you want them to
        # disappear, set them so that they respond True to isDead(), and they will be deleted next. If you want to put
        # more objects on screen, add them to the global variable objects_to_add, and they will be added later in this
        # loop.
        check_for_pie_lord_collisions()


        clear_dead_objects()
        add_new_objects()
        draw_objects()
        show_stats(delta_T) #optional. Comment this out if it annoys you.
        show_hits()
        show_misses()
        show_number_of_pies()

        if number_of_pies == 0 and hits == 5:
            game_mode = GAME_MODE_YOU_WON

        if number_of_pies == 0 and hits < 5:
            game_mode = GAME_MODE_GAME_OVER

    if game_mode == GAME_MODE_GAME_OVER:
        draw_objects()
        display_game_over()

    if game_mode == GAME_MODE_YOU_WON:
        draw_objects()
        display_you_won()

    pygame.display.flip()  # updates the window to show the latest version of the buffer.

# ===================== show_hits()
def show_hits():
    white_color = pygame.Color("white")
    hits_font = pygame.font.SysFont("Impact", 36)
    hits_string = "Hits: {0}".format(hits)
    hits_text_surface = hits_font.render(hits_string, True, white_color)
    hits_rect = hits_text_surface.get_rect()
    hits_rect.top = 10
    hits_rect.left = buffer.get_rect().width /2 - hits_rect.width /2
    buffer.blit(hits_text_surface, hits_rect)

#======================= show_misses()
def show_misses():
    white_color = pygame.Color("white")
    misses_font = pygame.font.SysFont("Impact", 36)
    misses_string = "Misses: {0}".format(misses)
    misses_text_surface = misses_font.render(misses_string, True, white_color)
    misses_rect = misses_text_surface.get_rect()
    misses_rect.top = 50
    misses_rect.left = buffer.get_rect().width /2 - misses_rect.width / 2
    buffer.blit(misses_text_surface, misses_rect)

# ===================== show_number_of_pies()
def show_number_of_pies():
    white_color = pygame.Color("white")
    number_of_pies_font = pygame.font.SysFont("Impact", 36)
    number_of_pies_string = "Remaining Pies: {0}".format(number_of_pies)
    number_of_pies_text_surface = number_of_pies_font.render(number_of_pies_string, True, white_color)
    number_of_pies_rect = number_of_pies_text_surface.get_rect()
    number_of_pies_rect.bottom = 580
    number_of_pies_rect.left = buffer.get_rect().width /2 - number_of_pies_rect.width / 2
    buffer.blit(number_of_pies_text_surface, number_of_pies_rect)
#=====================

def check_for_pie_lord_collisions():
    global hits, number_of_pies, misses

    if abs(the_pie.x - the_lord.x) < 82 and abs(the_pie.y - the_lord.y) < 124:
        the_pie.x = 3000
        splat_sound.play()
        hits = hits + 1
        number_of_pies = number_of_pies - 1

    if abs(the_pie.x - 600) < 5:
        the_pie.x = 3000
        cork_sound.play()
        misses = misses + 1
        number_of_pies = number_of_pies - 1


# =====================  animate_objects()
def animate_objects(delta_T):
    """
    tells each object to "step"...
    """
    global objects_on_screen
    for object in objects_on_screen:
        if object.is_dead(): #   ...but don't bother "stepping" the dead ones.
            continue
        object.step(delta_T)


# =====================  clear_dead_objects()
def clear_dead_objects():
    """
    removes all objects that are dead from the "objectsOnScreen" list
    """
    global objects_on_screen
    i = 0
    for object in objects_on_screen[:]:
        if object.is_dead():
            objects_on_screen.pop(i) # removes the ith object and pulls everything else inwards, so don't advance "i"
                                     #      ... they came back to you.
        else:
            i += 1

# =====================  add_new_objects()
def add_new_objects():
    """
    Adds all the objects in the list "objects to add" to the list of "objects on screen" and then clears the "to add" list.
    :return: None
    """
    global objects_to_add, objects_on_screen
    objects_on_screen.extend(objects_to_add)
    objects_to_add.clear()

# =====================  draw_objects()
def draw_objects():
    """
    Draws each object in the list of objects.
    """
    for object in objects_on_screen:
        object.draw_self(buffer)

#=======================
def display_game_over():
    yellow_color = pygame.Color("Red")
    game_over_font = pygame.font.SysFont('Times', 24)

    game_over_surface = game_over_font.render("YOU LOST", True, yellow_color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.x = buffer.get_rect().width / 2 - game_over_rect.width / 2
    game_over_rect.y = 200

    buffer.blit(game_over_surface, game_over_rect)

#========================
def display_you_won():
    yellow_color = pygame.Color("Red")
    game_over_font = pygame.font.SysFont('Times', 24)

    game_over_surface = game_over_font.render("YOU WON", True, yellow_color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.x = buffer.get_rect().width / 2 - game_over_rect.width / 2
    game_over_rect.y = 200

    buffer.blit(game_over_surface, game_over_rect)

# =====================  show_stats()
def show_stats(delta_T):
    """
    draws the frames-per-second in the lower-left corner and the number of objects on screen in the lower-right corner.
    Note: the number of objects on screen may be a bit misleading. They still count even if they are being drawn off the
    edges of the screen.
    :param delta_T: the time since the last time this loop happened, used to calculate fps.
    :return: None
    """
    white_color = pygame.Color(255,255,255)
    stats_font = pygame.font.SysFont('Arial', 10)

    fps_string = "FPS: {0:3.1f}".format(1.0/delta_T) #build a string with the calculation of FPS.
    fps_text_surface = stats_font.render(fps_string,True,white_color) #this makes a transparent box with text
    fps_text_rect = fps_text_surface.get_rect()   # gets a copy of the bounds of the transparent box
    fps_text_rect.left = 10  # now relocate the box to the lower left corner
    fps_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(fps_text_surface, fps_text_rect) #... and copy it to the buffer at the location of the box

    objects_string = "Objects: {0:5d}".format(len(objects_on_screen)) #build a string with the number of objects
    objects_text_surface = stats_font.render(objects_string,True,white_color)
    objects_text_rect = objects_text_surface.get_rect()
    objects_text_rect.right = buffer.get_rect().right - 10 # move this box to the lower right corner
    objects_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(objects_text_surface, objects_text_rect)

def move_shrek(mouse_loc):
    the_shrek.x = mouse_loc[0]
    the_shrek.y = mouse_loc[1]
    if mouse_loc[0] > 100:
        the_shrek.x = 99

# =====================  read_events()

def read_events():
    """
    checks the list of events and determines whether to respond to one.
    """
    events = pygame.event.get()  # get the list of all events since the last time
    for evt in events:
        if evt.type == QUIT:
            pygame.quit()
            raise Exception("User quit the game")
            # You may decide to check other events, like the mouse
            # or keyboard here.
        if evt.type == MOUSEMOTION:
            move_shrek(evt.pos)
        if evt.type == MOUSEBUTTONDOWN:
            the_pie.x = the_shrek.x
            the_pie.y = the_shrek.y

# program start with game loop - this is what makes the loop() actually loop.
pygame.init()
try:
    setup()
    fpsClock = pygame.time.Clock()  # this will let us pass the deltaT to loop.
    while True:
        time_since_last_loop = fpsClock.tick(60) / 1000.0 # we set this to go up to as much as 60 fps, probably less.
        loop(time_since_last_loop)
        read_events()

except Exception as reason: # If the user quit, exit gracefully. Otherwise, explain what happened.
    if len(reason.args)>0 and reason.args[0] == "User quit the game":
        print ("Game Over.")
    else:
        traceback.print_exc()
