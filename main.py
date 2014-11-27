#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     buzz buzz
#
# Author:      Timothy
#
# Created:     18/09/2014
# Copyright:   (c) Timothy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import pygame, sys, os, random
    import pygame.freetype
    import entities
    FPS = 60
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    flowerColour = (0,0,0)
    patchLocation = [0,0] #x, y
    intTimeScale = 1.0
    xOffset = 0
    yOffset = 0
    drawTrails = True
    beeExplosions = False
    explosionSprite = pygame.image.load('explosion-spritesheet.png')
    fpsClock = pygame.time.Clock()
    windowWidth = 1366
    windowHeight = 768

    #GUI
    pygame.freetype.init()
    debugFont = pygame.freetype.SysFont('Arial',24)

    #MUSIC
    pygame.mixer.init()
    pygame.mixer.music.load('resources\Sunny Day Sky.ogg')
    pygame.mixer.music.play(loops=-1)

    #GAME OBJECTS
    beeArray = []
    trailArray = []
    flowerArray = []
    explosionArray = []
    explosionSpriteArray = []
    hive = entities.Beehive(windowWidth / 2, windowHeight / 2)
    hiveRect = pygame.Rect((windowWidth / 2) - 50, (windowHeight / 2) - 50,100,100)
    for i in range (0,25):
        explosionSpriteArray.append(pygame.Rect(i*192,0,192,195))
    soundArray = []
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    soundArray.append(pygame.mixer.Sound('pew-01.ogg'))
    soundArray.append(pygame.mixer.Sound('pew-02.ogg'))
    soundArray.append(pygame.mixer.Sound('pew-03.ogg'))
    miscArray = [] #used for general structure things

    pygame.init()
    iconSurface = pygame.image.load('resources\icon.png')
    pygame.display.set_icon(iconSurface)
    screenSurface = pygame.display.set_mode((1366,768))
    pygame.display.set_caption('hello bees')
    #initial flower generation
##    for i in range (3,10):
##        flowerColour = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
##        patchLocation[0] = random.randint(0,1366)
##        patchLocation[1] = random.randint(0,768)
##        for flowerNo in range (1,random.randint(1,6)):
##            flowerArray.append(entities.Flower(patchLocation[0] + random.randint(-50,50),patchLocation[1] + random.randint(-50,50),flowerColour))

    while True:
        screenSurface.fill((0,0,0))
        #surfaceArray = pygame.PixelArray(screenSurface)
        #EVENT HANDLING
        if random.random() < 0.01:
            beeArray.append(entities.Bee(683,384,2))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if random.random() > 0.99:
            if len(flowerArray) < 25:
            #create flowerpatch with same characteristics for each flower
                flowerColour = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
                pollenRate = random.randint(0,6) + random.randint(0,6) + 1 #creates normal-ish distribution for recharge rates
                pollenMax = random.randint(0,30) + random.randint(0,30) + 600
                flowerTimeToLive = random.randint(0,60000) + random.randint(0,60000) + 20000
                patchLocation[0] = random.randint(0,1366)
                patchLocation[1] = random.randint(0,768)
                for flowerNo in range (1,random.randint(1,6)):
                    flowerArray.append(entities.Flower(patchLocation[0] + random.randint(-50,50),patchLocation[1] + random.randint(-50,50),flowerColour,pollenRate,pollenMax,flowerTimeToLive))
        #UPDATES POSITION AND HANDLES COLLISIONS
##        for trail in trailArray:
##            trail.update()
##            if trail.timeToLive == 0:
##                trailArray.remove(trail)
        for currentBee in beeArray:
            #trailArray.append(entities.Trail(currentBee))
            currentBee.updatePosition()
            currentBee.turnTime = currentBee.turnTime - 1
            if currentBee.turnTime <= 0:
                currentBee.randomDirection()
                #currentBee.direction = currentBee.direction + 1
            if currentBee.timeToLive <= 0:
                if beeExplosions == True:
                    explosionArray.append(entities.Effect(currentBee))
                    soundArray[random.randint(0,2)].play()
                beeArray.remove(currentBee) #RIP bee
        #UPDATES FLOWER STATES
        for flower in flowerArray:
            flower.makePollen()
            if flower.timeToLive == 0:
                flowerArray.remove(flower)

        #COLLECTS POLLEN FROM NEARBY FLOWERS
        for bee in beeArray:
            shortestDistance = 99999
            for flower in flowerArray:
                if distanceBetween(bee,flower) < shortestDistance:
                    shortestDistance = distanceBetween(bee,flower)
                if shortestDistance < 10:
                    bee.harvestPollen(flower)
                    shortestDistance = 99999

        for bee in beeArray:
            if hiveRect.collidepoint(bee.xPos,bee.yPos):
                hive.collectPollenFromBee(bee)

        #Final two lines, updates screen and ticks for frame (according to timescale)

        #DRAWS HIVE
        pygame.draw.rect(screenSurface, (125,125,0),hiveRect,0)

        #DRAWS EACH FLOWER

        for flowa in flowerArray:
            if flowa.pollenStored < 300:
                pygame.draw.circle(screenSurface,RED,(flowa.xPos, flowa.yPos),5,0)
            else:
                pygame.draw.circle(screenSurface,flowa.colour,(flowa.xPos, flowa.yPos),5,0)

##        #DRAWS EACH TRAIL
##        if drawTrails == True:
##            for trail in trailArray:
##                pygame.draw.circle(screenSurface,trail.colour,(round(trail.xPos) + xOffset, round(trail.yPos) + yOffset),2,0)
        #DRAWS EACH BEE
        for bee in beeArray:
            if bee.boolSelected == True:
                pygame.draw.circle(screenSurface,DEVPINK,(round(bee.xPos) + xOffset,round(bee.yPos) + yOffset),2,0)
            elif bee.heldPollen > 999:
                pygame.draw.circle(screenSurface,RED,(round(bee.xPos) + xOffset,round(bee.yPos) + yOffset),2,0)
            else:
                pygame.draw.circle(screenSurface,bee.colour,(round(bee.xPos) + xOffset, round(bee.yPos) + yOffset),2,0)
            #pygame.draw.line(screenSurface,RED,pygame.mouse.get_pos(),(round(bee.xPos),round(bee.yPos)),1)
        if beeExplosions == True:
            for explosion in explosionArray:
                screenSurface.blit(explosionSprite,(explosion.xPos - 98,explosion.yPos - 96),explosionSpriteArray[25-explosion.timeToLive])
                explosion.timeToLive = explosion.timeToLive - 1
                if explosion.timeToLive == 0:
                    explosionArray.remove(explosion)
        #DEBUG TEXT

        debugFont.render_to(screenSurface,(0,0),"Pollen in hive: " + str(hive.pollenStore),WHITE,None,0,0)
        #Final two lines, updates screen and ticks for frame (according to timescale)
        pygame.display.update()
        print(len(beeArray))
        fpsClock.tick(FPS * intTimeScale)
def distanceBetween(entity1,entity2):
    return (((entity1.xPos - entity2.xPos)**2) + ((entity1.yPos - entity2.yPos)**2))**0.5
if __name__ == '__main__':
    from pygame.locals import *
    main()
