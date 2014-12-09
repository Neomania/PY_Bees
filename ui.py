#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     08/12/2014
# Copyright:   (c) Timothy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pygame.locals import *
class LineBetweenObjects:
    object1 = None
    object2 = None
    timeToLive = 0
    colour = (0,0,255)
    def __init__(self,object1,object2,timeToLive,colour = (0,0,255)):
        self.object1 = object1
        self.object2 = object2
        self.timeToLive = timeToLive
        if colour != (0,0,255):
            self.colour = colour

class Button:
    topLeft = (0,0)
    bottomRight = (0,0)
