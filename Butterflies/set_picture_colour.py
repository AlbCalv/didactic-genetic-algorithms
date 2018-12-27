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

from PIL import Image
import numpy as np
import sys


"INPUTS"


def changeColourTo(image_route,colour):
    "Creating an Image object from the test file"
    img = Image.open(image_route,'r')
    #img.show()
    "List with all pixel values (R,G,B)"
    pix_list = list(img.getdata())

    n_pix= len(pix_list)
    "Converting tuples (R,G,B) to lists [R,G,B] for sklearn"
    Pixels=[]

    "Change white pixels for colour"
    for i in range(n_pix):
        if sum(pix_list[i])>=255*2:
            pix_list[i]=colour

    "Loading the picture"
    recover = Image.new(img.mode,img.size)
    recover.putdata(pix_list)
    recover.save('coloured_butterfly.png')
    #recover.show()

    return recover
