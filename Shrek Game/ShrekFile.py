__author__ = 'Lexy'
import pygame

class Shrek:
    def __init__(self):
        """
        This is where we set up the variables for this particular object as soon as it is created.
        """
        self.x = 40
        self.y = 400
        #self.vx = 0
        #self.vy = 0
        self.i_am_alive = True
        self.my_image = pygame.image.load("shrek.png")

    def draw_self(self, surface):
        """
        It is this object's responsibility to draw itself on the surface. It will be told to do this often!
        :param surface:
        :return: None
        """
        my_rect = self.my_image.get_rect()
        my_rect.left = self.x - 30
        my_rect.top = self.y - 5
        surface.blit(self.my_image, my_rect)

    def step(self, delta_T):
        """
        In order to change over time, this method gets called very often. The delta_T variable is the amount of time it
        has been since the last time we called "step()" usually about 1/20 -1/60 of a second.
        :param delta_T:
        :return: None
        """
        pass
        # self.x = self.x + self.vx * delta_T
        # self.y = self.y + self.vy * delta_T
    def is_dead(self):
        """
        lets another object know whether this object is still live and on the board. Used by the main loop to clear objects
        in need of removal.
        :return: True or False - is this object dead?
        """
        if self.i_am_alive:
            return False
        else:
            return True
        # alternative (1-line) version of this function:
        #  "return not self.i_am_alive"
    def die(self):
        """
        change the status of this object so that it is dead.
        :return: None
        """
        self.i_am_alive = False