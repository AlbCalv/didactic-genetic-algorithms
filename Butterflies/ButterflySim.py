#This file is part of Didactic Genetic Algorithms.

#    Didactic Genetic Algorithms  is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Voluntary Project for ALGC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Didactic Genetic Algorithms.  If not, see <https://www.gnu.org/licenses/>.


import pygame
import sys
import os
import set_picture_colour as setcol
import geneticbutterfly as ga
import numpy as np
import time

"Constants"
SCREEN_WIDTH=1620
SCREEN_HEIGHT=900
IMG_DIR = ""
POPULATION = 20
GENERATIONS=200
MARGIN=200
LIMIT_TIME=2
BACKGROUNDCOLOUR =[73,70,28]

#---------------------------------------------------------------
"Loading picture utility"
def load_image(name, dir_image, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_image, name)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, can't load image: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def setImages(screen,individuals,positions):


    for i in range(len(individuals)):

        setcol.changeColourTo("Butterfly.png",individuals[i].getColour())
        but = load_image("coloured_butterfly.png",IMG_DIR,alpha=True)
        screen.blit(but,positions[i])

    pygame.display.flip()

def main():
    pygame.init()

    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Butterfly Color Evolution")

    col=(255,0,0,255)
    pygame.font.init() # you have to call this at the start,
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    "Loading background"
    screen.fill(BACKGROUNDCOLOUR)

    clock = pygame.time.Clock()

    pygame.display.flip()

    run = True

    colours=[]
    '''
    for i in range(POPULATION):
        randomrgb=list(np.random.randint(255,size=3))
        randomrgb.append(255)
        randomrgb=tuple(randomrgb)
        colours.append(randomrgb)
    individuals=ga.init_individuals(colours)
    '''

    for i in range(POPULATION):
        colours.append([255,255,255,255])
    individuals=ga.init_individuals(colours)
    positions=[(np.random.randint(0,SCREEN_WIDTH-2*MARGIN),np.random.randint(0,SCREEN_HEIGHT-2*MARGIN)) for i in range(len(individuals))]


    wing_status=0
    for i in range(GENERATIONS):
        print "Generacion :"+str(i)
        time1=time.clock()
        time2=0

        textsurface = myfont.render("Generation "+str(i), False, (255,255,255))

        while time2<LIMIT_TIME:
            pygame.time.delay(1)
            screen.fill(BACKGROUNDCOLOUR)
            screen.blit(textsurface,(SCREEN_WIDTH-MARGIN/1.5,SCREEN_HEIGHT-MARGIN/1.7))
            setImages(screen,individuals,positions)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            time2=time.clock()-time1


        individuals=ga.fitness(individuals,BACKGROUNDCOLOUR)
        fittest =   ga.selection(individuals)
        individuals= ga.crossover(fittest)
        individuals = ga.mutation(individuals)


    for final in individuals:
        print "color "+str(final.getColour())
    pygame.quit()

main()
