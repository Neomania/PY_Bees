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
    import entities, ui
    FPS = 60
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    SOL_GREEN = (133,153,0)
    SOL_DARK = (7,54,66)
    flowerColour = (0,0,0)
    patchLocation = [0,0] #x, y
    intTimeScale = 1.0
    xOffset = 0
    yOffset = 0
    scrollAmount = 0
    drawTrails = True
    beeExplosions = False
    explosionSprite = pygame.image.load('explosion-spritesheet.png')
    fpsClock = pygame.time.Clock()
    windowWidth = 1080
    windowHeight = 1080
    beeMax = 50

    selectionStart = (0,0)
    selectionSize = (0,0)
    selectionEnd = (0,0)
    selecting = False

    #GUI
    pygame.freetype.init()
    debugFont = pygame.freetype.SysFont('Arial',12)

    #MUSIC
##    pygame.mixer.init()
##    pygame.mixer.music.load('resources\Sunny Day Sky.ogg')
##    pygame.mixer.music.play(loops=-1)

    #GAME OBJECTS
    beeArray = []
    selectedBeeArray = []
    trailArray = []
    flowerArray = []
    explosionArray = []
    explosionSpriteArray = []
    idlingArray = []
    lineArray = []

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
    screenSurface = pygame.Surface((windowWidth,windowHeight))
    mainSurface = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption('hello bees')
    #initial flower generation
##    for i in range (3,10):
##        flowerColour = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
##        patchLocation[0] = random.randint(0,1366)
##        patchLocation[1] = random.randint(0,768)
##        for flowerNo in range (1,random.randint(1,6)):
##            flowerArray.append(entities.Flower(patchLocation[0] + random.randint(-50,50),patchLocation[1] + random.randint(-50,50),flowerColour))

    while True:
        screenSurface.fill(BLACK)
        mainSurface.fill(SOL_DARK)
        #surfaceArray = pygame.PixelArray(screenSurface)
        #EVENT HANDLING
        if random.random() < 0.2:
            if len(beeArray) < beeMax:
                beeArray.append(entities.Bee(hive.xPos,hive.yPos,2))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                scrollAmount = 0
                for bee in selectedBeeArray:
                    bee.boolSelected = False
                selectedBeeArray = []
                selecting = True
                selectionStart = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                selectionSize = (pygame.mouse.get_pos()[0] - selectionStart[0],pygame.mouse.get_pos()[1] - selectionStart[1])
                selectionEnd = pygame.mouse.get_pos()
                selectionRect = pygame.Rect(selectionStart,selectionSize)
                selecting = False
                for bee in beeArray:
                    if betweenVertices(selectionStart,selectionEnd,bee):
                        bee.boolSelected = True
                        selectedBeeArray.append(bee)
                for flower in flowerArray:
                    if betweenVertices(selectionStart,selectionEnd,flower):
                        selectedBeeArray.append(flower)
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    pass
                    #scrollAmount = scrollAmount - 10
                elif event.key == K_UP:
                    pass
                elif event.key == K_DELETE:
                    for entity in selectedBeeArray:
                        entity.timeToLive = 0
                    selectedBeeArray = []
                    #scrollAmount = scrollAmount + 10
        if pygame.key.get_pressed()[K_UP]:
            scrollAmount = scrollAmount + 5
        if pygame.key.get_pressed()[K_DOWN]:
            scrollAmount = scrollAmount - 5

    ##                if selectionRect.collidepoint(bee.xPos,bee.yPos):
    ##                    bee.boolSelected = True
    ##                    selectedBeeArray.append(bee)
        if random.random() > 0.9:
            if len(flowerArray) < 25:
            #create flowerpatch with same characteristics for each flower
                flowerColour = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
                pollenRate = random.randint(0,6) + random.randint(0,6) + 1 #creates normal-ish distribution for recharge rates
                pollenMax = random.randint(0,30) + random.randint(0,30) + 600
                flowerTimeToLive = random.randint(0,60000) + random.randint(0,60000) + 20000
                patchLocation[0] = random.randint(0,windowWidth)
                patchLocation[1] = random.randint(0,windowHeight)
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
            if betweenVertices((0,0),(windowWidth,windowHeight),currentBee) == False:
                currentBee.xPos = currentBee.xPosLast
                currentBee.yPos = currentBee.yPosLast
                currentBee.direction = currentBee.direction + 180
            currentBee.turnTime = currentBee.turnTime - 1
            if currentBee.turnTime <= 0:
                if currentBee.currentAction == "Moving randomly":
                    currentBee.actionTime = currentBee.actionTime - 1
                    if currentBee.actionTime <= 0:
                        currentBee.currentAction = "Return to hive"
                    else:
                        currentBee.randomDirection()
                elif currentBee.currentAction == "Return to hive":
                    currentBee.moveTowards((hive.xPos,hive.yPos),20)
                elif currentBee.currentAction == "Idling":
                    idlingArray.remove(currentBee)
                    currentBee.vel = 2
                    if currentBee.memoryArray == []:
                        currentBee.randomDirection()
                        currentBee.movingRandomly()
                    else:
                        if random.random() < 0.8:
                            print("lucky")
                            currentBee.currentAction = "Moving to memory"
                            currentBee.actionTime = 10
                            #currentBee.direction = currentBee.favouriteMemory.direction
                            #currentBee.memoryInQuestion = currentBee.favouriteMemory #TESTING TO FIX CRASH
                            currentBee.memoryInQuestion = entities.Memory(0,0,0,0)
                            for memory in currentBee.memoryArray:
                                if currentBee.memoryInQuestion.flowerViability < memory.flowerViability:
                                    currentBee.memoryInQuestion = memory
                        else:
                            print("unlucky")
                            currentBee.randomDirection()
                            currentBee.movingRandomly()
                    #currentBee.currentAction = "Moving randomly"
                elif currentBee.currentAction == "Moving to memory":
                    if currentBee.actionTime >= 0:
                        currentBee.moveTowards((currentBee.memoryInQuestion.xPos,currentBee.memoryInQuestion.yPos),10)
                        currentBee.actionTime = currentBee.actionTime - 1
                    else:
                        currentBee.currentAction = "Return to hive"
                        if currentBee.heldPollen < 200:
                            currentBee.memoryArray.remove(currentBee.memoryInQuestion)
                        else:
                            currentBee.memoryInQuestion.flowerViability = currentBee.memoryInQuestion.flowerViability * (0.8 + (0.2 * (currentBee.heldPollen / 1000)))
##                        if currentBee.heldPollen < 200:
##                            currentBee.memoryArray.remove(currentBee.memoryInQuestion) #CAUSING CRASHES
                        for memory in currentBee.memoryArray:
                            if memory.flowerViability > currentBee.favouriteMemory.flowerViability:
                                currentBee.favouriteMemory = memory
                #currentBee.direction = currentBee.direction + 1
            if currentBee.timeToLive <= 0:
                if beeExplosions == True:
                    explosionArray.append(entities.Effect(currentBee))
                    soundArray[random.randint(0,2)].play()
                #beeArray.remove(currentBee) #RIP bee
        #UPDATES FLOWER STATES
        for flower in flowerArray:
            flower.makePollen()
            flower.harvestTimeout = flower.harvestTimeout - 1
            if flower.timeToLive <= 0:
                flowerArray.remove(flower)

        #COLLECTS POLLEN FROM NEARBY FLOWERS
        for bee in beeArray:
            if bee.currentAction == "Moving randomly":
                shortestDistance = 99999
                for flower in flowerArray:
                    if distanceBetween(bee,flower) < shortestDistance:
                        shortestDistance = distanceBetween(bee,flower)
                    if shortestDistance < 25:
                        if bee.currentAction == "Moving randomly" and flower.harvestTimeout <= 0:
                            bee.storeMemoryAboutFlower(flower)
                            bee.harvestPollen(flower)
                        shortestDistance = 99999
            elif bee.currentAction == "Moving to memory":
                if distanceBetween(bee.memoryInQuestion,bee) < 250: #max distance to memory:
                    for flower in flowerArray:
                        if distanceBetween(bee,flower) < 25:
                            if flower.harvestTimeout <= 0:
                                bee.memoryInQuestion.updateViability(flower)
                                for memory in bee.memoryArray:
                                    if memory.flowerViability > bee.favouriteMemory.flowerViability:
                                        bee.favouriteMemory = memory
                                bee.harvestPollen(flower)
            elif bee.currentAction == "Idling": #chance to broadcast
                if random.random() < 0.01:
                    for idlebee in idlingArray:
                        #print(bee.favouriteMemory in idlebee.memoryArray)
                        if idlebee != bee and ((bee.favouriteMemory in idlebee.memoryArray) == False):
                            if idlebee.favouriteMemory.flowerViability < bee.favouriteMemory.flowerViability and random.random() < 0.1:
                                #print("tellinsomeone")
                                idlebee.memoryArray.append(bee.favouriteMemory)
                                idlebee.favouriteMemory = bee.favouriteMemory
                                lineArray.append(ui.LineBetweenObjects(bee,idlebee,60))
                    lineArray.append(ui.LineBetweenObjects(bee,bee.favouriteMemory,10,(GREEN)))
        for bee in beeArray:
            if hiveRect.collidepoint(bee.xPos,bee.yPos) and bee.currentAction == "Return to hive":
                hive.collectPollenFromBee(bee)
                bee.currentAction = "Idling"
                idlingArray.append(bee)
                bee.moveTowards((hive.xPos,hive.yPos),30)
                bee.vel = 0.25
                bee.turnTime = random.randint(60,600)

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
        for line in lineArray:
            pygame.draw.line(screenSurface,line.colour,(line.object1.xPos,line.object1.yPos),(line.object2.xPos,line.object2.yPos),2)
            line.timeToLive = line.timeToLive - 1
            if line.timeToLive == 0:
                lineArray.remove(line)
        for i in range(0,len(selectedBeeArray)):
            if (30 * (i + 1) + scrollAmount) > 0: #This line stops things crashing, please don't ignore it
                if isinstance(selectedBeeArray[i],entities.Bee):
                    debugFont.render_to(mainSurface,
                    (windowWidth + 5,30 * (i + 1) + scrollAmount),
                    selectedBeeArray[i].name + ": "
                     +"currentAction: " + selectedBeeArray[i].currentAction
                     + ", favMem: " + str(selectedBeeArray[i].favouriteMemory)
                     + ", memories: " + str(len(selectedBeeArray[i].memoryArray))
                     + ", dir: " + str(selectedBeeArray[i].direction).zfill(3)
                     + ", xPos: " + str(selectedBeeArray[i].xPos).zfill(6)
                     + ", yPos: " + str(selectedBeeArray[i].yPos).zfill(6),
                     SOL_GREEN,None,0,0)
                elif isinstance(selectedBeeArray[i],entities.Flower):
                    debugFont.render_to(mainSurface,
                    (windowWidth + 5,30 * (i + 1) + scrollAmount),
                     "pollenStored: " + str(selectedBeeArray[i].pollenStored)
                     + ", pollenRate: " + str(selectedBeeArray[i].pollenRate)
                     + ", pollenMax: " + str(selectedBeeArray[i].pollenMax),
                     selectedBeeArray[i].colour,None,0,0)
        if selecting == True:
            selectionSize = (pygame.mouse.get_pos()[0] - selectionStart[0],pygame.mouse.get_pos()[1] - selectionStart[1])
            selectionRect = pygame.Rect(selectionStart,selectionSize)
            pygame.draw.rect(screenSurface,RED,selectionRect,2)
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

        debugFont.render_to(mainSurface,(windowWidth + 5,0),"Pollen in hive: " + str(hive.pollenStore),SOL_GREEN,None,0,0)
        #Final two lines, updates screen and ticks for frame (according to timescale)
        mainSurface.blit(screenSurface,(0,0))
        pygame.display.update()
        #print(len(beeArray))
        fpsClock.tick(FPS * intTimeScale)
def betweenVertices(selectionStart,selectionEnd,entity):
    inX = False
    inY = False
    if entity.xPos > selectionStart[0]:
        if entity.xPos < selectionEnd[0]:
            inX = True
    elif entity.xPos > selectionEnd[0]:
        inX = True
    if entity.yPos > selectionStart[1]:
        if entity.yPos < selectionEnd[1]:
            inY = True
    elif entity.yPos > selectionEnd[1]:
        inY = True
    if inX and inY:
        return True
    else:
        return False


def distanceBetween(entity1,entity2):
    return (((entity1.xPos - entity2.xPos)**2) + ((entity1.yPos - entity2.yPos)**2))**0.5
if __name__ == '__main__':
    from pygame.locals import *
    main()
