__author__ = 'yuki'
#coding UTF-8

import numpy as np
from PIL import Image
from PIL import ImageOps

class Layer(object):
    def __init__(self, xySize, n_scale, n_orientation, LayerType):
        self.xySize = xySize #largest image size
        self.n_scale = n_scale #number of scale
        self.n_orientation = n_orientation #number of orientation
        self.LayerType = LayerType #"Input" or "s1" or "c1" or "s2" or "c2"

        self.array = [] #array = [n_scale][size, size, n_orientation]
        print "size of layer:"
        for i in range(n_scale):
            size = int(xySize*(2**(-1.0*i/4)))
            if self.LayerType == "s1":
                size = self.resize_to_s1(size)
            elif self.LayerType == "c1":
                size = self.resize_to_c1(size)
            print size, "*", size
            self.array.append(np.zeros((size, size, self.n_orientation), dtype=float))

    def set_layer(self, image):
        for s in range(self.n_scale):
            size = self.get_size(s)
            gray_img = np.asarray(ImageOps.grayscale(image).resize((size, size))).T*1.0/255
            for x in range(size):
                for y in range(size):
                    self.array[s][x, y, 0] = gray_img[x, y]

    def get_xySpace(self, ScaleNumber):
        return self.xySize*1.0/self.get_size(ScaleNumber)

    def get_array(self, ScaleNumber):
        return self.array[ScaleNumber]

    def get_size(self,ScaleNumber):
        return self.array[ScaleNumber][:,0,0].size

    def get_LayerType(self):
        if self.LayerType == "s1":
            return 1
        elif self.LayerType == "c1":
            return 2
        else:
            return 0

    def resize_to_s1(self, size):
        return size - 10

    def resize_to_c1(self, size):
        size = self.resize_to_s1(size)
        return size/5 - 1


