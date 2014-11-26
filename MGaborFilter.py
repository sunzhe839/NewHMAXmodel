__author__ = 'yuki'
#coding UTF-8

import numpy
from PIL import Image

class GaborFilter:
    def __init__(self, xyCount, aspect, lamb, sigma, fCount):
        self.m_xyCount = xyCount #length of filter
        self.aspect = aspect #parameters
        self.lamb = lamb
        self.sigma = sigma
        self.m_fCount = fCount #number of scale

        self.m_gabors = numpy.zeros([self.m_fCount,self.m_xyCount,self.m_xyCount])
        ptr = numpy.zeros([self.m_xyCount,self.m_xyCount])
        #ptr_mul=numpy.zeros([self.m_xyCount,self.m_xyCount])

        self.xy_Start = int(0.5*(1-self.m_xyCount))

        #make gabor filter kernel
        for o in range(4): #orientation
            for x in range(self.xy_Start,self.xy_Start+self.m_xyCount):
                for y in range(self.xy_Start,self.xy_Start+self.m_xyCount):
                    theta=1.0*o/4*numpy.pi
                    Y = x*numpy.sin(theta) + y*numpy.cos(theta)
                    X = x*numpy.cos(theta) - y*numpy.sin(theta)
                    if numpy.sqrt(X*X+Y*Y) <= -(self.xy_Start):
                        e = numpy.exp(-(X*X+self.aspect*self.aspect*Y*Y)/(2.0*self.sigma*self.sigma))
                        e = e*numpy.cos(2.0*numpy.pi*X/self.lamb)
                    else:
                        e = 0.0
                    ptr[x, y] = e
                    #ptr_mul[x,y]=e**2

            """
        n=self.m_xyCount**2
        ptr_mean=numpy.mean(ptr)

        ptr_stdv = numpy.sqrt(numpy.sum(ptr_mul)-numpy.sum(ptr)**2/n)
        for iy in range(self.m_xyCount):
            for jx in range(self.m_xyCount):
                ptr[iy,jx] = (ptr[x,y]-ptr_mean)/ptr_stdv
                print ptr[iy,jx]
            """
            self.m_gabors[o, :, :] = ptr
            """
            img = Image.new('RGB', (11, 11))
            for iy in range(self.xy_Start,self.xy_Start+self.m_xyCount):
                for jx in range(self.xy_Start,self.xy_Start+self.m_xyCount):
                    #print self.m_gabors[0,jx,iy]
                    gvalue = (self.m_gabors[0,jx,iy]+1)*128

                    gvalue = int(gvalue)
                    print gvalue
                    img.putpixel((jx-self.xy_Start, iy-self.xy_Start), (gvalue, gvalue, gvalue))
            img.show()
            """


    def FCount(self):
        return self.m_fCount

    def ComputeUnit(self, Inputpatch, orientation):
        res=0.0
        lenc=0.0
        gabor = self.m_gabors[orientation,:,:]

        #convolve
        for xi in range(self.xy_Start, self.xy_Start+self.m_xyCount-1):
            for yi in range(self.xy_Start, self.xy_Start+self.m_xyCount-1):
                w = gabor[xi,yi]
                v = Inputpatch[xi-self.xy_Start, yi-self.xy_Start]
                #print w, v
                res += w*v
                lenc += v*v
                #print res, lenc

        res = abs(res)
        if lenc > 0:
            res /=numpy.sqrt(lenc)
        return res

    def ComputeLayer(self, xySize, InputImage, Output): #make patch
        for o in range(4):
            for x in range(xySize-10):
                for y in range(xySize-10):
                    Output[o, x, y] = self.ComputeUnit(InputImage[x:x+10,y:y+10], o)
