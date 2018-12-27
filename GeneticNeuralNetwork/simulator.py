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
from pygame.locals import *
import sys
import os
import random
import itertools
import NeuralNetwork as nn
import GeneticAlgorithm as ga
import time
import numpy as np



GENERATIONS = ga.GENERATIONS
POPULATION=ga.POPULATION

N_LAYERS=nn.N_LAYERS
N_OUTPUTS=nn.N_OUTPUTS
N_INPUTS=nn.N_INPUTS
N_NEURONS=nn.N_NEURONS
f=open("data.txt","w")
"Constants for the simulator"

"640x480"
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 1000
IMG_DIR = "Images"
MV_CONSTANT= 1
GOAL_X=700
GOAL_Y=700
SPAWN_X=500
SPAWN_Y=300
LIMIT_TIME=2
SPEED=3
"Object parameters"
cell_dim=(25,25)
obj_dim=(75,75)

num_cells=4
#---------------------------------------------------------------
"Loading picture utility"
def load_image(name, dir_image, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_image, name)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
#---------------------------------------------------------------
class Player(pygame.sprite.Sprite):

    def __init__(self,spawnx,spawny,picture,(dim1,dim2)):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(picture, IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image,(dim1,dim2))
        self.rect = self.image.get_rect()
        self.rect.centerx = spawnx
        self.rect.centery = spawny




    "Movement and Boundaries for the Player"
    def move(self,x,y):
        radius=self.radius()

        if self.posX()+x>=radius and self.posX()+x<=SCREEN_WIDTH-radius:
            self.rect.centerx+=x
        else:
            if self.posX()<SCREEN_WIDTH-self.posX():
                self.rect.centerx=radius
            else:
                self.rect.centerx=SCREEN_WIDTH-radius

        if self.posY()+y>=radius and self.posY()+y<=SCREEN_HEIGHT-radius:
            self.rect.centery+=y
        else:
            if self.posY()<SCREEN_HEIGHT-self.posY():
                self.rect.centery=radius
            else:
                self.rect.centery=SCREEN_HEIGHT-radius


    "Getters and setters"
    def radius(self):
        return self.rect.width/2
    def posX(self):
        return self.rect.centerx
    def posY(self):
        return self.rect.centery
    def set_posX(self,x):
        self.rect.centerx=x
    def set_posY(self,y):
        self.rect.centery=y

    def set_pos(self,x,y):
        self.rect.centerx=x
        self.rect.centery=y

    def center(self):
        return (self.posX(),self.posY())
    def new_center(self,x,y):
        return (self.posX()+x,self.posY()+y)
#---------------------------------------------------------------


"FUNCTIONS RELATED TO GAME PHYSICS"
def distance((x,y),(w,z)):
    distance2=(x-w)**2+(y-z)**2
    return distance2**0.5

def collision(tup1,tup2,r1,r2):
    return distance(tup1,tup2)<r1+r2

'''
"Utility to know if one npc is touching the border"
def is_touching_borderX(npc):
    radius=npc.radius()

    return npc.posX()-radius==0 or npc.posX()+radius==SCREEN_WIDTH
def is_touching_borderY(npc):
    radius=npc.radius()
    return npc.posY()-radius==0 or npc.posY()+radius==SCREEN_HEIGHT

"2 npcs would overlap if one is touching the border and the other one is pushing towards that one"
def overlap(npc1,npc2,(x,y)):
    r1=npc1.radius()
    r2=npc2.radius()
    new_center1=npc1.new_center(x,y)
    center2=npc2.center()
    if x==0 and y!=0:
        return collision(new_center1,center2,r1,r2) and is_touching_borderY(npc2)
    elif x!=0 and y==0:
        return collision(new_center1,center2,r1,r2) and is_touching_borderX(npc2)
'''

def sign(x):
    if x==0: return 1
    else:
        return 1-(x<=0)
def will_touch_borderX(npc,xshift):
    radius=npc.radius()
    return npc.posX()+xshift-radius<=0 or npc.posX()+xshift+radius>=SCREEN_WIDTH

def will_touch_borderY(npc,yshift):
    radius=npc.radius()
    return npc.posY()+yshift-radius<=0 or npc.posY()+yshift+radius>=SCREEN_HEIGHT

#-------------------------------------
"FUNCTIONS RELATED TO MOVEMENT"
"""def move(selected,cells,(x,y)):

    "Cells not moving are stored in this array in order to check physical problems"
    nonselected=range(len(cells))[:selected]+range(len(cells))[(selected+1):]

    for i in nonselected:
        col=collision((cells[selected].posX()+x,cells[selected].posY()+y),(cells[i].posX(),cells[i].posY()),cells[selected].radius(),cells[i].radius())
        ol=overlap(cells[selected],cells[i],(x,y))

        if not col:
            cells[selected].move(x,y)
        if col:
            cells[i].move(x,y)

            "The reason to to this is so they bounce back. If 2"
            "Are pushing the same ball, they would overlap with"
            "no collision, and since this are simplle physics I"
            "did not want to propagate movement and pushes, because"
            "it collides so many times it would run out of stack"
            cells[selected].move(-2*x,-2*y)


            if ol:
                if is_touching_borderX(cells[i]) and is_touching_borderY(cells[i]):
                    cells[selected].move(-x,-y)
                    cells[i].move(x,y)

                elif is_touching_borderX(cells[i]):
                    cells[selected].move(-x,-y)
                    cells[i].move(0,y)

                elif is_touching_borderY(cells[i]):
                    cells[selected].move(0,-2*y)
                    cells[i].move(x,0)
"""

"Move decision function. Here the Neural Network will make a decision about the movement"
def sameCuadrant((x1,y1),(x2,y2)):

    return np.sign(x1)==np.sign(x2) and np.sign(y1)==np.sign(y2)


def isInLine((pointX,pointY),(slopeX,slopeY),(originX,originY)):

    if sameCuadrant((pointX-originX,pointY-originY),(slopeX,slopeY)):
        if slopeX != 0:
            m=slopeY/slopeX

            return (pointY-originY)==m*(pointX-originX)
        else:
            minv=slopeX/slopeY
            return (pointY-originY)*minv==(pointX-originX)
    else:
        return False



def beams((posX,posY)):


    beam0=isInLine((GOAL_X,GOAL_Y),(1,0),(posX,posY))
    beam45=isInLine((GOAL_X,GOAL_Y),(1,1),(posX,posY))
    beam90=isInLine((GOAL_X,GOAL_Y),(0,1),(posX,posY))
    beam135=isInLine((GOAL_X,GOAL_Y),(-1,1),(posX,posY))
    beam180=isInLine((GOAL_X,GOAL_Y),(-1,0),(posX,posY))
    beam225=isInLine((GOAL_X,GOAL_Y),(-1,-1),(posX,posY))
    beam270=isInLine((GOAL_X,GOAL_Y),(0,-1),(posX,posY))
    beam315=isInLine((GOAL_X,GOAL_Y),(1,-1),(posX,posY))

    return [beam0,beam45,beam90,beam135,beam180,beam225,beam270,beam315]


def decision_move(selected,cells,nn):

    cellX=cells[selected].posX()
    cellY=cells[selected].posY()
    beam=beams((cellX,cellY))

    nn_input=[]
    for i in range(len(beam)):
        nn_input.append((cellX-GOAL_X)*beam[i])
        nn_input.append((cellY-GOAL_Y)*beam[i])

    out=nn.output(nn_input)

    X_shift=np.sign(out[0])
    Y_shift=np.sign(out[1])

    return (X_shift,Y_shift)

#--------------------------------------
"Functions related to the visualization"
def update_screen(cells,background,screen):
    goal = load_image("goal.png",IMG_DIR,alpha=True)
    screen.blit(background, (0, 0))
    screen.blit(goal, (GOAL_X, GOAL_Y))
    for c in cells:
        screen.blit(c.image,c.rect)
    pygame.display.flip()


def restart(screen):
    cells=[]
    spawns=cellspawns()
    for i in range(num_cells):

        cells.append(Player(spawns[i][0],spawns[i][1],"cell.png",cell_dim))
        screen.blit(cells[i].image, (cells[i].rect.centerx, cells[i].rect.centery))

    objective=Player(SPAWN_X,SPAWN_Y,"object.png",obj_dim)

    cells.append(objective)

    background = load_image("background.jpg",IMG_DIR,alpha=False)
    goal = load_image("goal.png",IMG_DIR,alpha=True)
    screen.blit(goal, (GOAL_X, GOAL_Y))

    screen.blit(background, (0, 0))

    return cells

def cellspawns():
    spawn_radius=obj_dim[0]/2+cell_dim[0]/2
    spawns=[]

    global SPAWN_X
    global SPAWN_Y
    SPAWN_X=np.random.randint(300,SCREEN_WIDTH/2)
    SPAWN_Y=np.random.randint(300,SCREEN_HEIGHT/2)
    for i in range(num_cells):
        angle=np.random.uniform(0,np.pi)
        x=spawn_radius*np.cos(angle)+SPAWN_X-4
        y=spawn_radius*np.sin(angle)+SPAWN_Y-4
        spawns.append((x,y))
    return spawns


"Function made in order to avoid local minimum"
def tweak_params():
    another=0
    if another==0:
        f.write("endsimul\n")
    print("Parameter to change: ")
    print("1. Add a hidden layer")
    print("2. Add a neuron by layer")
    print("3. Change the variance of the mutation")
    print("4. Simulate again with the same parameters\n")
    change = int(input("Press the desired option: \n"))

    if change==1:
        print "Actual number of layers: ",nn.N_LAYERS
        newN_LAYERS=int(input("Number of layers: \n"))
        print "\nN_LAYERS changed from",nn.N_LAYERS,"to",newN_LAYERS
        nn.N_LAYERS=newN_LAYERS
        print ("Wanna change another parameter?\n")
        another=int(input("Enter: 1 (Yes) 0 (No)"))
        if another==1:
            tweak_params()
    elif change==2:
        print "Actual number of neurons: ",nn.N_NEURONS
        newN_NEURONS=int(input("Number of neurons: \n"))
        print "\nN_NEURONS changed from",nn.N_NEURONS,"to",newN_NEURONS
        nn.N_NEURONS=newN_NEURONS
        print ("Wanna change another parameter?\n")
        another=int(input("Enter: 1 (Yes) 0 (No)"))
        if another==1:
            tweak_params()
    elif change==3:
        print "Actual variance: ",ga.STD_VAR
        print("\n The variance will be multiplied by an uniform distribution with:")
        print("Lower boundary: \n")
        newSTD_VAR_INF=float(input(""))
        print("Upper boundary: \n")
        newSTD_VAR_SUP=float(input(""))
        print "STD_VAR changed to",ga.STD_VAR
        ga.STD_VAR*=np.random.uniform(newSTD_VAR_INF,newSTD_VAR_SUP)
        print ("Wanna change another parameter?\n")
        another=int(input("Enter: 1 (Yes) 0 (No)"))
        if another==1:
            tweak_params()
    elif change==4:
        print "\n Simulating again"

    global N_LAYERS
    global N_NEURONS
    N_LAYERS=nn.N_LAYERS
    N_NEURONS=nn.N_NEURONS
    ga.N_LAYERS=N_LAYERS
    ga.N_NEURONS=N_NEURONS


def main():
    pygame.init()



    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Genetic Algorithm Simulator")


    cells=restart(screen)

    "Loading background"
    background = load_image("background.jpg",IMG_DIR,alpha=False)
    screen.blit(background, (0, 0))

    goal = load_image("goal.png",IMG_DIR,alpha=True)
    screen.blit(goal, (GOAL_X, GOAL_Y))

    pygame.display.flip()
    clock = pygame.time.Clock()

    "First generation random weights"

    popu_weights=[]

    '''
    para la pimera capa, necesitamos tantos pesos como N_INPUTS
    para las capas inermedias, necesitamso tantos pesos como N_NEURONS'''

    for i in range(POPULATION):

            layer1_w=np.random.uniform(-1,1,size=(N_INPUTS,N_NEURONS))
            weights = [layer1_w]
            for l in range(N_LAYERS-1):
                weights.append(np.random.uniform(-1,1,size=(N_NEURONS,N_NEURONS)))
            "OUTPUT WEIGHTS"
            weights.append(np.random.uniform(-1,1,size=(N_NEURONS,N_OUTPUTS)))
            b=np.random.uniform(-1,1,size=(1+N_LAYERS))

            popu_weights.append((weights,b))




    individuals = ga.init_individuals(popu_weights)

    neural_network=None
    avgfitmin=100000000000
    notbetter=0
    for generation in xrange(GENERATIONS):
        final_poss=[]
        "Main simulator loop"
        print 'Generation: ', generation
        f.write("g\n"+str(generation)+"\n")
        "For each element in the population, do the simulation in 10 seconds"
        for i in range(POPULATION):
            print "Individual number",i
            "Current element of the population assigned neural_network"
            f.write("i\n"+str(i)+"\n")
            f.write(str(SPAWN_X)+" "+str(SPAWN_Y)+"\n")

            neural_network=individuals[i]
            time1=time.clock()
            time2=0

            while time2<LIMIT_TIME:

                clock.tick(60)
                update_screen(cells,background,screen)

                "Catching all the events in the game. If one happens to be QUIT, exit"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                time2=time.clock()-time1

                mv_buff=[]
                resX=0
                resY=0
                for selected in range(len(cells)-1):
                    mv_buff.append(decision_move(selected,cells,neural_network))

                for j in range(len(cells)-1):
                    resX+=mv_buff[j][0]
                    resY+=mv_buff[j][1]


                cant_x=False
                cant_y=False

                for j in range(len(cells)):
                    cant_x=cant_x or will_touch_borderX(cells[j],resX)
                    cant_y=cant_y or will_touch_borderY(cells[j],resY)

                resX=resX*int(not cant_x)
                resY=resY*int(not cant_y)

                f.write(str(resX)+" "+str(resY)+"\n")

                for j in range(len(cells)):
                    cells[j].move(SPEED*resX,SPEED*resY)
            final_poss.append((cells[-1].posX(),cells[-1].posY()))
            pygame.display.quit()
            '''RESTART'''
            screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
            pygame.display.set_caption("Genetic Algorithm Simulator")
            cells=restart(screen)
            pygame.display.flip()


        print 'End of Generation: ', generation


        individuals = ga.fitness(individuals,(SPAWN_X,SPAWN_Y),(GOAL_X,GOAL_Y),final_poss)
        avgfit=0
        for i in individuals:
            avgfit+=i.getFitness()
        avgfit/=POPULATION


        if avgfit<avgfitmin :
            avgfitmin=avgfit
            notbetter=0
        else:
            notbetter+=1


        if notbetter==4:
            print "Didn't improve for 4 gen"
            return True
            exit()

        print "Average Fitness for Gen ",generation," is ",avgfit


        if any(agent.fitness == 0 for agent in individuals):

            print 'Threshold met!'
            return False
            exit(0)
        fittest =   ga.selection(individuals)
        offspring = ga.crossover(fittest)
        individuals = ga.mutation(offspring)
    return False



while True:
    hasstopped=main()
    if hasstopped:
        tweak_params()

    else:
        exit(0)
