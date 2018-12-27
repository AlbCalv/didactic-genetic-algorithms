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


import numpy as np
import random





class Individual():


    def __init__(self,(R,G,B,A)):
        self.colour=(R,G,B,A)
        self.fitness=0

    def setFitness(self,f):
        self.fitness=f

    def getFitness(self):
        return self.fitness

    def getColour(self):
        return self.colour
    def setColour(self,col):
        self.colour=col



def init_individuals(colours):

    individuals=[]

    for i in range(len(colours)):

        new_individual=Individual(colours[i])
        individuals.append(new_individual)

    return individuals






def rgbdistance((R1,G1,B1,A1),(R2,G2,B2,A2)):

    return (R1-R2)**2+(G1-G2)**2+(B1-B2)**2

def fitness(individuals,background):

    backcopy=[i for i in background]
    backcopy.append(255)
    backcopy=tuple(backcopy)
    for i in individuals:
        print backcopy, i.getColour()

        i.setFitness(rgbdistance(backcopy,i.getColour()))

    return individuals


def selection(individuals):

    individuals.sort(key=lambda x: x.fitness, reverse=False)
    individuals=individuals[:int(0.5*len(individuals))]
    for f in individuals:
        print "ind fitness",f.fitness
    return individuals


def crossover(individuals):
    offspring=[]

    for __ in range(len(individuals)):
        parent1 = random.choice(individuals)
        parent2 = random.choice(individuals)
        while parent2==parent1:
            parent2 = random.choice(individuals)

        print "Parent 1, fitness =",parent1.fitness
        print "Parent 2, fitness =",parent2.fitness


        colour1=[(parent1.getColour()[i]+parent2.getColour()[i])/2 for i in range(len(parent1.getColour()))]
        colour1=tuple(colour1)
        colour2=parent2.getColour()


        child1=Individual(colour1)
        child2=Individual(colour2)

        offspring.append(child1)
        offspring.append(child2)


    randomrgb=list(np.random.randint(255,size=3))
    randomrgb.append(255)
    randomrgb=tuple(randomrgb)

    offspring.pop()
    offspring.append(Individual(randomrgb))
    return offspring

def mutation(individuals):
    for ind in individuals:
        mutatedcol=list(ind.getColour())
        for i in range(len(mutatedcol)-1):
            mutatedcol[i]=mutatedcol[i]*np.random.normal(1,0.1,size=1)
        ind.setColour(tuple(mutatedcol))
    return individuals
