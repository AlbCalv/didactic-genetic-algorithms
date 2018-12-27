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


import random
import numpy as np

N_OUTPUTS=2
N_LAYERS=2
"8 beams that comes from the food abs"
"2 values (X,Y) if the beam passes through the goal"
N_INPUTS=8*2
N_NEURONS=36

def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

def act_f(x):
    return sigmoid(x)

class NeuralNetwork:
    def __init__(self,(w,b)):

        self.weights=w
        self.b=b

    def set_input(self,input):
        self.input=input

    "Input= 2x1 vector"
    "Weights= N_NEURONSxN_PREVIOUS_LAYER_OUTPUT matrixes"

    def output(self,input):

        prev_layer_output =input
        for l in range(1+N_LAYERS-1):

            wx=np.dot(prev_layer_output,self.weights[l])+self.b[l]
            prev_layer_output=map(act_f,wx)


        "For the output layer, we use the tanh function"
        wx=np.dot(prev_layer_output,self.weights[-1])+self.b[-1]
        prev_layer_output=map(np.tanh,wx)



        return prev_layer_output

    "Setters and getters"
    def setW(self,w):
        self.weights=w

    def getW(self):
        return self.weights

    def getB(self):
        return self.b
    def setB(self,b):
        self.b=b
