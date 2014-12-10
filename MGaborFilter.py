__author__ = 'yuki'
#coding UTF-8

import numpy as np
from MFilter import Filter
from MPrintIMG import Print

class GaborFilter(Filter):
    def __init__(self, xyCount, aspect, lamb, sigma, oCount):
        self.xyCount = xyCount #size of filter
        self.aspect = aspect #parameters
        self.lamb = lamb
        self.sigma = sigma
        self.oCount = oCount #number of orientation

        self.m_gabors = np.zeros([self.oCount, self.xyCount, self.xyCount])
        ptr = np.zeros([self.xyCount, self.xyCount])

        self.xyStart = int(0.5*(1-self.xyCount))

        #make gabor filter kernel
        for o in range(self.oCount): #orientation
            for x in range(self.xyStart,self.xyStart+self.xyCount):
                for y in range(self.xyStart,self.xyStart+self.xyCount):
                    theta=1.0*o/self.oCount*np.pi
                    Y = x*np.sin(theta) + y*np.cos(theta)
                    X = x*np.cos(theta) - y*np.sin(theta)
                    if np.sqrt(X*X+Y*Y) <= -(self.xyStart):
                        e = np.exp(-(X*X+self.aspect*self.aspect*Y*Y)/(2.0*self.sigma*self.sigma))

                        #12/10 change this
                        #before cos
                        #after sin
                        e = e*np.sin(2.0*np.pi*X/self.lamb)
                    else:
                        e = 0.0

                    #12/2 change ptr[x, y]
                    #before x:-5 ~ 5 , y:-5 ~ 5
                    #after x:0 ~ 10 , y:0 ~ 10
                    ptr[x - self.xyStart, y - self.xyStart] = e

            self.m_gabors[o, :, :] = ptr
            #Print().PrintGaborFilter(self.m_gabors, 1)

    def ComputeUnit(self, Inputpatch, orientation):
        res=0.0
        lenc=0.0
        gabor = self.m_gabors[orientation,:,:]

        #convolve
        for xi in range(self.xyCount):
            for yi in range(self.xyCount):
                w = gabor[xi,yi]
                v = Inputpatch[xi, yi]
                res += w*v
                lenc += v*v

        res = abs(res)
        if lenc > 0:
            res /=np.sqrt(lenc)
        return res
