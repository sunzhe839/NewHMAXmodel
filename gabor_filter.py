__author__ = 'yuki'
#coding UTF-8

import numpy as np
from filter import Filter
from MPrintIMG import Print


class GaborFilter(Filter):
    def __init__(self, filter_size, aspect, lamb, sigma, orientations):
        self.filter_size = filter_size  
        self.aspect = aspect  # parameters
        self.lamb = lamb
        self.sigma = sigma
        self.orientations = orientations

        self.gabor_filter = np.zeros([self.orientations, self.filter_size, self.filter_size])
        ptr = np.zeros([self.filter_size, self.filter_size])

        start = int(0.5 * (1 - self.filter_size))

        # make gabor filter kernel
        for o in range(self.orientations):
            for x in range(start, start + self.filter_size):
                for y in range(start, start + self.filter_size):
                    theta = 1.0 * o / self.orientations * np.pi
                    Y = x * np.sin(theta) + y * np.cos(theta)
                    X = x * np.cos(theta) - y * np.sin(theta)
                    if np.sqrt(X * X + Y * Y) <= -start:
                        e = np.exp(-(X * X + self.aspect * self.aspect * Y * Y) / (2.0 * self.sigma * self.sigma))

                        #12/10 change this
                        #before cos
                        #after sin
                        e *= np.sin(2.0 * np.pi * X / self.lamb)
                    else:
                        e = 0.0

                    #12/2 change ptr[x, y]
                    #before x:-5 ~ 5 , y:-5 ~ 5
                    #after x:0 ~ 10 , y:0 ~ 10
                    ptr[x - start, y - start] = e

            self.gabor_filter[o, :, :] = ptr
        #Print().PrintGaborFilter(self.gabor_filter, 1)


    def compute_unit(self, input_layer, scale, feature, x, y, orientation):
        # "feature" is not used
        gabor = self.gabor_filter[orientation, :, :].T
        patch = input_layer.get_array(scale)[0, x:x + self.filter_size, y:y + self.filter_size].T

        r = gabor * patch
        res = r.sum()
        l = patch * patch
        lenc = l.sum()

        res = abs(res)
        if lenc > 0:
            res /= np.sqrt(lenc)
        return res
