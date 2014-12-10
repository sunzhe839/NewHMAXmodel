__author__ = 'yuki'
#coding UTF-8

import numpy as np
from PIL import Image
from PIL import ImageOps
from MLayer import Layer
from MGaborFilter import GaborFilter
from MLocalInvariance import LocalInvariance
from MPrintIMG import Print

if __name__=="__main__":
    #test s1 to c1
    input_size = 256 #input image size
    n_scale = 2 #number of scale at InputLayer
    c1_n_scale = n_scale - 1 #number of scale at c1
    n_orientation = 4

    #input an image
    Im_name = raw_input()
    image = Image.open(Im_name)

    #fs1 = GaborFilter(11, 0.4, 2.0, 1.0, n_orientation)  :previous parameter
    fs1 = GaborFilter(11, 0.4, 4.0, 1.5, n_orientation)
    fc1 = LocalInvariance(10, n_orientation)

    ImageOps.grayscale(image).resize((input_size, input_size)).save('base.jpg')

    #make layer
    print 'Input Layer'
    InputLayer = Layer(input_size, n_scale, 1, "Input")
    InputLayer.set_layer(image)

    print '\nS1 Layer'
    s1Layer = Layer(input_size, n_scale, 4, "s1")

    print "\nC1 Layer"
    c1Layer = Layer(input_size, c1_n_scale, 4, "c1")

    #conpute layer s1 to c1
    fs1.ComputeS1Layer(InputLayer, s1Layer, n_scale)
    fc1.ComputeC1Layer(s1Layer, c1Layer, c1_n_scale, 5)

    #print orientated image
    Print().PrintIMG(s1Layer.get_size(0), s1Layer.get_array(0), n_orientation, "s1")
    Print().PrintIMG(c1Layer.get_size(0), c1Layer.get_array(0), n_orientation, "c1")




