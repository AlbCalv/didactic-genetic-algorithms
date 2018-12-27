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

import matplotlib.pyplot as plt
import numpy as np
from colour import Color


POS_X=0
POS_Y=0
COL=Color("yellow")
COLOURS=[]
GEN=0

plt.axis([0, 1750, 0, 1000])
plt.plot(POS_X,POS_Y,"ro")

f=open("data.txt","r")
with open("data.txt") as f:
    lines=f.readlines()

lines =[line.rstrip("\n") for line in open("data.txt")]

"Fix data file last line problems"
print lines[-1]
if(len(lines[-1])>2 and lines[-1]!="endsimul"):
    lines.pop()
    print lines[-1]
    lines.append("endsimul")
print lines[-1]
f.close()


"Fix problems with rgb code length"
def fixColours(COLOURS):
    c=0
    for i in COLOURS:
        s=str(i)
        if (s[0]=="#" and len(s)<7):
                snew="#"+s[1]+s[1]+s[2]+s[2]+s[3]+s[3]
                COLOURS[c]=snew
        c+=1
    return COLOURS

gensets=[]
"Total of generations"
for i in lines:
    if i!="endsimul":
        if i[0]=="g":
            GEN+=1
    else:
        gensets.append(GEN)
        GEN=0

"Conclusion of the entire simulation"
gensets.append(100)

"Create gradiant with as colours as generations"
COLOURS = list(COL.range_to(Color("red"),gensets[0]))
fixColours(COLOURS)


split=[]
movX=[]
movY=[]
gencount=0
nombre=0
for i in lines:
    if not(i=="endsimul"):
        if not(i =="i" or i=="g" or len(i)<4):
            "Format of the data file"
            split=i.split(" ")
            POS_X=int(float(split[0]))
            POS_Y=int(float(split[1]))
            movX.append(POS_X)
            movY.append(POS_Y)
        else:

            if i == "g":
                gencount+=1
                COL=COLOURS[gencount-1]

            plt.plot(movX,movY,color=str(COL),linestyle="solid")

            if len(movX)>0 : plt.plot(movX[0],movY[0],color=str(COL),marker="s",linestyle="solid")

            movX=[]
            movY=[]

    else:
        plt.plot(700,700,"bx")
        #plt.show()
        plt.savefig("graphsim"+str(nombre+1)+".png")
        plt.clf()
        plt.axis([0, 1750, 0, 1000])
        movX=[]
        movY=[]
        gencount=0
        nombre+=1
        COL=Color("yellow")
        COLOURS = list(COL.range_to(Color("red"),gensets[nombre]))
        fixColours(COLOURS)
