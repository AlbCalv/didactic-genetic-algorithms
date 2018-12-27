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
from NeuralNetwork import *
import NeuralNetwork as nn


GENERATIONS = 100
POPULATION=30
N_GEN=10000
N_NEURONS=nn.N_NEURONS
N_LAYERS=nn.N_LAYERS
STD_VAR=10

class Individual(NeuralNetwork):
    def __init__(self,(weights,b)):

        NeuralNetwork.__init__(self,(weights,b))
        self.fitness=0

    def setFitness(self,f):
        self.fitness=f

    def getFitness(self):
        return self.fitness




"inputs  =Vector of inputs"
"weights[i]=Vector of i weight vectors"

def init_individuals(weights):

    nns=[]

    for i in range(POPULATION):

        new_individual=Individual(weights[i])
        nns.append(new_individual)

    return nns


"How well did the individual do "
"In this case, the criteria will be how much distance is yet to be covered"
def fitness(individuals,(spawnx,spawny),(goalx,goaly),fps):

    for i in range(len(individuals)):
        distance_to_goal=distance(fps[i],(goalx,goaly))
        print distance_to_goal
        individuals[i].setFitness(distance_to_goal)
    return individuals


def selection(individuals):
    individuals.sort(key=lambda x: x.fitness, reverse=False)
    individuals=individuals[:int(len(individuals)/3)]
    for f in individuals:
        print "ind fitness",f.fitness
    return individuals

def crossover(individuals):

    offspring = []
    for i in range(len(individuals)):
        parent1 = random.choice(individuals)
        parent2 = random.choice(individuals)
        while parent2==parent1:
            parent2 = random.choice(individuals)

        c1w=[]
        c2w=[]
        c3w=parent1.getW()
        p1w=parent1.getW()
        p2w=parent2.getW()

        for l in range(1+N_LAYERS):
            rlength=p1w[l].shape[0]
            clength=p1w[l].shape[1]

            mutated_matrix1=np.zeros((rlength,clength))
            mutated_matrix2=np.zeros((rlength,clength))
            sample = np.random.choice((rlength*clength)-1,(rlength*clength)/2)
            for num in range((rlength*clength)-1):
                i=num/clength
                j=num%clength-1
                if num in sample:
                    mutated_matrix1[i,j]=p1w[l][i,j]
                    mutated_matrix2[i,j]=p2w[l][i,j]
                else:
                    mutated_matrix1[i,j]=p2w[l][i,j]
                    mutated_matrix2[i,j]=p1w[l][i,j]

            c1w.append(mutated_matrix1)
            c2w.append(mutated_matrix2)

        child1=Individual((c1w,parent1.getB()))
        child2=Individual((c2w,parent2.getB()))
        child3=Individual((c3w,parent1.getB()))
        offspring.append(child1)
        offspring.append(child2)
        offspring.append(child3)

    "Now we replace one child with a random one in order to avoid local minimum"
    offspring.pop()
    layer1_w=np.random.uniform(-10,10,size=(N_INPUTS,N_NEURONS))
    weights = [layer1_w]
    for l in range(N_LAYERS-1):
        weights.append(np.random.uniform(-10,10,size=(N_NEURONS,N_NEURONS)))
    "OUTPUT WEIGHTS"
    weights.append(np.random.uniform(-10,10,size=(N_NEURONS,N_OUTPUTS)))
    "Randomize b"
    b=np.random.uniform(-1,1,size=(1+N_LAYERS))
    random_offspring=Individual((weights,b))


    offspring.append(random_offspring)

    return offspring

"Mutation following a normal distribution"
def mutation(offspring):
    for child in offspring:
            mutated=map(mutate,child.getW())
            child.setW(mutated)
    return offspring

"Euclidean distance between two points"
def distance((x,y),(w,z)):
    distance2=(x-w)**2+(y-z)**2
    return distance2**0.5

def mutate(x):
    return x*(1+np.random.normal(0,STD_VAR)/100)
