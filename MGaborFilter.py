__author__ = 'yuki'
#coding UTF-8

import numpy
from PIL import Image
from MFilter import Filter

class GaborFilter(Filter):
    def __init__(self, xyCount, aspect, lamb, sigma, oCount):
        self.xyCount = xyCount #size of filter
        self.aspect = aspect #parameters
        self.lamb = lamb
        self.sigma = sigma
        self.oCount = oCount #number of orientation

        self.m_gabors = numpy.zeros([self.oCount,self.xyCount,self.xyCount])
        ptr = numpy.zeros([self.xyCount,self.xyCount])

        self.xyStart = int(0.5*(1-self.xyCount))

        #make gabor filter kernel
        for o in range(self.oCount): #orientation
            for x in range(self.xyStart,self.xyStart+self.xyCount):
                for y in range(self.xyStart,self.xyStart+self.xyCount):
                    theta=1.0*o/self.oCount*numpy.pi
                    Y = x*numpy.sin(theta) + y*numpy.cos(theta)
                    X = x*numpy.cos(theta) - y*numpy.sin(theta)
                    if numpy.sqrt(X*X+Y*Y) <= -(self.xyStart):
                        e = numpy.exp(-(X*X+self.aspect*self.aspect*Y*Y)/(2.0*self.sigma*self.sigma))
                        e = e*numpy.cos(2.0*numpy.pi*X/self.lamb)
                    else:
                        e = 0.0

                    #12/2 change ptr[x, y]
                    #before x:-5 ~ 5 , y:-5 ~ 5
                    #after x:0 ~ 10 , y:0 ~ 10
                    ptr[x - self.xyStart, y - self.xyStart] = e

            self.m_gabors[o, :, :] = ptr

            """
            img = Image.new('RGB', (11, 11))
            for iy in range(self.xyCount):
                for jx in range(self.xyCount):
                    #print self.m_gabors[0,jx,iy]
                    gvalue = (self.m_gabors[1,jx,iy]+1)*128

                    gvalue = int(gvalue)
                    print gvalue
                    img.putpixel((jx, iy), (gvalue, gvalue, gvalue))
            img.save('gaborfilter.jpg')
            """

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
            res /=numpy.sqrt(lenc)
        return res

