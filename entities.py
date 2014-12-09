#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     18/09/2014
# Copyright:   (c) Timothy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pygame.locals import *
import random, math
class Bee:
    xPos = 0.0
    yPos = 0.0
    xVel = 0.0
    yVel = 0.0
    vel = 0.0
    xPosLast = 0.0
    yPosLast = 0.0
    boolSelected = False
    heldPollen = 0
    direction = 0.0
    timeToLive = 0
    turnTime = 0
    actionTime = 0
    colour = (0,0,0)
    favouriteMemory = None
    memoryInQuestion = None
    memoryArray = []
    distanceTravelled = 0.0
    currentAction = "Moving randomly"
    def __init__(self,xPos,yPos,vel):
        self.memoryArray = []
        self.xPos = xPos
        self.yPos = yPos
        self.vel = vel
        self.turnTime = 5
        self.direction = random.randint(0,360)
        self.timeToLive = 5000 + random.randint(0,300)
        self.colour = (random.randint(200,255),random.randint(200,255),0)
        self.favouriteMemory = Memory(0,0,0,0)
    def randomDirection(self):
        self.direction = self.direction + random.randint(-20,20)
        self.turnTime = 3
    def updatePosition(self):
        self.timeToLive = self.timeToLive - 1
        self.xPosLast = self.xPos
        self.yPosLast = self.yPos
        self.xPos = self.xPos + (self.vel * math.cos(math.radians(self.direction)))
        self.yPos = self.yPos + (self.vel * math.sin(math.radians(self.direction)))
        self.distanceTravelled = 0
    def storeMemoryAboutFlower(self,currentFlower):
        flowerRating = (currentFlower.pollenRate * 5) + currentFlower.pollenStored
        newMemory = Memory(currentFlower.xPos,currentFlower.yPos,self.distanceTravelled,flowerRating)
        if newMemory.flowerViability > self.favouriteMemory.flowerViability:
            self.favouriteMemory = newMemory
        self.memoryArray.append(newMemory)
        self.distanceTravelled = 0
    def harvestPollen(self,flower):
        self.currentFlower = flower
        flower.givePollen(self)
    def moveTowards(self,target,accuracy):
        self.turnTime = random.randint(20,50)
        self.direction = math.degrees(math.atan2((target[1] - self.yPos) , (target[0] - self.xPos))) + random.randint(-accuracy,accuracy)
class Beehive:
    xPos = 0.0
    yPos = 0.0
    pollenStore = 0
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
    def collectPollenFromBee(self,bee):
        self.pollenStore = self.pollenStore + bee.heldPollen
        bee.heldPollen = 0
class Memory:
    direction = 0.0
    distance = 0.0
    xPos = 0.0
    yPos = 0.0
    flowerViability = 0
    def __init__(self,xPos,yPos,distance,viability):
        #self.direction = math.degrees(math.asin((yPos - 540)/((yPos * yPos + xPos * xPos)**0.5)))
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.flowerViability = viability
    def updateViability(self,currentFlower):
        self.viability = (currentFlower.pollenRate * 30) + currentFlower.pollenStored
class Flower:
    xPos = 0.0
    yPos = 0.0
    pollenRate = 0
    pollenStored = 0
    pollenMax = 0
    timeToLive = 0
    colour = (0,0,0)
    harvestTimeout = 0
    def __init__(self, xPos, yPos, colour, pollenRate, pollenMax, timeToLive):
        self.xPos = xPos
        self.yPos = yPos
##        self.pollenRate = random.randint(0,6) + random.randint(0,6) + 1 #creates normal-ish distribution for recharge rates
##        self.pollenMax = random.randint(0,30) + random.randint(0,30) + 10
##        self.timeToLive = random.randint(0,60000) + random.randint(0,60000) + 20000
        self.pollenRate = pollenRate
        self.pollenMax = pollenMax
        self.timeToLive = timeToLive
        self.colour = colour
    def makePollen(self):
        if self.pollenStored < self.pollenMax:
            self.pollenStored = self.pollenStored + self.pollenRate
        self.timeToLive = self.timeToLive - 1
    def givePollen(self, bee):
        self.harvestTimeout = 60
        if self.pollenStored < (1000 - bee.heldPollen):
            bee.heldPollen = bee.heldPollen + self.pollenStored
            self.pollenStored = 0
        else:
            self.pollenStored = self.pollenStored - (1000 - bee.heldPollen)
            bee.heldPollen = 1000
            bee.currentAction = "Return to hive"
class Effect:
    xPos = 0.0
    yPos = 0.0
    timeToLive = 0
    def __init__(self,bee):
        self.xPos = bee.xPos
        self.yPos = bee.yPos
        self.timeToLive = 25

class Trail:
    xPos = 0.0
    yPos = 0.0
    timeToLive = 0
    colour = (0,0,0)
    def __init__(self,bee):
        self.xPos = bee.xPos
        self.yPos = bee.yPos
        self.timeToLive = 10
        self.colour = (bee.colour[0],bee.colour[1],bee.colour[2])
    def update(self):
        self.timeToLive = self.timeToLive - 1
        self.colour = (self.colour[0],self.colour[1],self.colour[2])

def distanceBetween(pos1,pos2):
    return (((pos1[0] - pos2[0])**2) + ((pos1[1] - pos2[1])**2))**0.5






