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

"Constants for the simulator"
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 1000
IMG_DIR = "Images"
MV_CONSTANT= 1
GOAL_X=700
GOAL_Y=700
SPAWN_X=500
SPAWN_Y=300
LIMIT_TIME=1
SPEED=3

"Object parameters"
cell_dim=(25,25)
obj_dim=(75,75)
num_cells=4

"Prueba"
F=open("data.txt","w")


#---------------------------------------------------------------

class Cell():

    def __init__(self,spawnx,spawny,width):

        self.centerx = spawnx
        self.centery = spawny
        self.width = width



    "Movement and Boundaries for the Cell"
    def move(self,x,y):
        radius=self.radius()

        if self.posX()+x>=radius and self.posX()+x<=SCREEN_WIDTH-radius:
            self.centerx+=x
        else:
            if self.posX()<SCREEN_WIDTH-self.posX():
                self.centerx=radius
            else:
                self.centerx=SCREEN_WIDTH-radius

        if self.posY()+y>=radius and self.posY()+y<=SCREEN_HEIGHT-radius:
            self.centery+=y
        else:
            if self.posY()<SCREEN_HEIGHT-self.posY():
                self.centery=radius
            else:
                self.centery=SCREEN_HEIGHT-radius


    "Getters and setters"
    def radius(self):
        return self.width/2
    def posX(self):
        return self.centerx
    def posY(self):
        return self.centery
    def set_posX(self,x):
        self.centerx=x
    def set_posY(self,y):
        self.centery=y

    def set_pos(self,x,y):
        self.centerx=x
        self.centery=y

    def center(self):
        return (self.posX(),self.posY())
    def new_center(self,x,y):
        return (self.posX()+x,self.posY()+y)

#-------------------------------------
"Functions related to game physics"
def distance((x,y),(w,z)):
    distance2=(x-w)**2+(y-z)**2
    return distance2**0.5

def collision(tup1,tup2,r1,r2):
    return distance(tup1,tup2)<r1+r2

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
"Functions related to the beams treatment"
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

#-------------------------------------
"Funtions relate to the movement"
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
def restart():
    cells=[]
    spawns=cellspawns()
    for i in range(num_cells):
        cells.append(Cell(spawns[i][0],spawns[i][1],cell_dim[0]))
    objective=Cell(SPAWN_X,SPAWN_Y,obj_dim[0])

    cells.append(objective)
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

#--------------------------------------

"Function made in order to avoid local minimum"
def tweak_params():
    another=0
    print("Parameter to change: ")
    print("1. Add a hidden layer")
    print("2. Add a neuron by layer")
    print("3. Change the variance of the mutation")
    print("4. Simulate again with the same parameters\n")
    change = int(input("Press the desired option: \n"))

    if change==1:
        print "Actual number of layers: ",nn.N_LAYERS
        newN_LAYERS=int(input("Number of layers: \n"))
        while(newN_LAYERS<=0):
            print "Enter a valid number\n"
            print "Actual number of layers: ",nn.N_LAYERS
            newN_LAYERS=int(input("Number of layers: \n"))

        print "\nN_LAYERS changed from",nn.N_LAYERS,"to",newN_LAYERS
        nn.N_LAYERS=newN_LAYERS
        print ("Wanna change another parameter?\n")
        another=int(input("Enter: 1 (Yes) 0 (No)"))
        if another==1:
            tweak_params()
        else:
            F.write("endsimul\n")

    elif change==2:
        print "Actual number of neurons: ",nn.N_NEURONS
        newN_NEURONS=int(input("Number of neurons: \n"))
        while(newN_NEURONS<=0):
            print "Enter a valid number\n"
            print "Actual number of neurons: ",nn.N_NEURONS
            newN_NEURONS=int(input("Number of layers: \n"))
        print "\nN_NEURONS changed from",nn.N_NEURONS,"to",newN_NEURONS
        nn.N_NEURONS=newN_NEURONS
        print ("Wanna change another parameter?\n")
        another=int(input("Enter: 1 (Yes) 0 (No)"))
        if another==1:
            tweak_params()
        else:
            F.write("endsimul\n")

    elif change==3:
        print "Actual variance: ",ga.STD_VAR
        print("The variance will be multiplied by an uniform distribution with:")
        print("Lower boundary: \n")
        newSTD_VAR_INF=float(input(""))
        print("Upper boundary: \n")
        newSTD_VAR_SUP=float(input(""))
        while(newSTD_VAR_INF<=0 or newSTD_VAR_SUP<=0):
            print "Enter a valid number\n"
            print "Actual variance: ",ga.STD_VAR
            print("The variance will be multiplied by an uniform distribution with:")
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
        else:
            F.write("endsimul\n")

    elif change==4:
        print "Simulating again"
        F.write("endsimul\n")

    global N_LAYERS
    global N_NEURONS
    N_LAYERS=nn.N_LAYERS
    N_NEURONS=nn.N_NEURONS
    ga.N_LAYERS=N_LAYERS
    ga.N_NEURONS=N_NEURONS


def main():

    pygame.init()

    #f=open("datos.txt","w")

    cells=restart()

    "First generation random weights"

    popu_weights=[]

    '''
    For the first layer, we need as many weights as N_INPUTS
    for the intermediate layers, we need as many weights as N_NEURONS'''

    for i in range(POPULATION):

            layer1_w=np.random.uniform(-10,10,size=(N_INPUTS,N_NEURONS))
            weights = [layer1_w]
            for l in range(N_LAYERS-1):
                weights.append(np.random.uniform(-10,10,size=(N_NEURONS,N_NEURONS)))
            "OUTPUT WEIGHTS"
            weights.append(np.random.uniform(-10,10,size=(N_NEURONS,N_OUTPUTS)))
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
        F.write("g\n"+str(generation)+"\n")


        "For each element in the population, do the simulation in 10 seconds"
        for i in range(POPULATION):
            print "Individual number",i
            F.write("i\n"+str(i)+"\n")
            F.write(str(SPAWN_X)+" "+str(SPAWN_Y)+"\n")

            "Current element of the population assigned neural_network"
            neural_network=individuals[i]
            time1=time.clock()
            time2=0

            while time2<LIMIT_TIME:


                "Catching all the events in the game. If one happens to be QUIT, exit"
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




                for j in range(len(cells)):
                    cells[j].move(SPEED*resX,SPEED*resY)

                F.write(str(cells[-1].posX())+" "+str(cells[-1].posY())+"\n")

            final_poss.append((cells[-1].posX(),cells[-1].posY()))
            cells=restart()


        print 'End of Generation: ', generation


        individuals = ga.fitness(individuals,(SPAWN_X,SPAWN_Y),(GOAL_X,GOAL_Y),final_poss)
        avgfit=0
        "Calculus of the fitness"
        for i in individuals:
            avgfit+=i.getFitness()
        avgfit/=POPULATION

        "Check of block in a local minimum"
        if avgfit<avgfitmin :
            avgfitmin=avgfit
            notbetter=0
        else:
            notbetter+=1


        if notbetter==1:
            print notbetter,"generations without performing better"
            return True
            exit()


        if any(agent.fitness == 0 for agent in individuals):

            print 'Threshold met!'
            return False
            exit(0)
        fittest =   ga.selection(individuals)
        offspring = ga.crossover(fittest)
        individuals = ga.mutation(offspring)
        print "\nAverage Fitness for Gen ",generation," is ",avgfit,"\n"
    return False

    "Lecture in the format needed"
    gen=F.read(1)
    ind=F.read(1)
    spawn=F.read(7)
    print gen, ind, spawn


"""While the avg fitness is improving, the program doesn't stop,
when its needed, the parameters are tweaked"""
while True:
    hasstopped=main()
    if hasstopped:
        tweak_params()

    else:
        exit(0)
