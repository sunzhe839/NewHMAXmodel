__author__ = 'yuki'
#coding UTF-8

import numpy as np
from PIL import Image

class Print(object):
    def __init__(self):
        pass

    def PrintIMG(self, Size, ImgArray, n_orientation, Mode):
        Outputsum = np.zeros((Size, Size), dtype=float)
        img = Image.new('RGB', (Size, Size))
        for orient in range(n_orientation):
            for x in range(Size):
                for y in range(Size):
                    gvalue = int(ImgArray[x, y, orient]*255)
                    Outputsum[x, y] += gvalue
                    img.putpixel((x, y), (gvalue, gvalue, gvalue))
            img.save(Mode + '_' + str(orient) + '.jpg')

        #sum of 4 orientations
        sumimg = Image.new('RGB', (Size, Size))
        for sx in range(Size):
            for sy in range(Size):
                svalue = int(Outputsum[sx, sy])
                sumimg.putpixel((sx, sy), (svalue, svalue, svalue))
        sumimg.show()
        sumimg.save(Mode + 'sum.jpg')

    def PrintGaborFilter(self, gabor, orientation):
        img = Image.new('RGB', (11, 11))
        filtersize = gabor[orientation, :, 0].size
        for iy in range(filtersize):
            for jx in range(filtersize):
                gvalue = (gabor[orientation,jx,iy]+1)*128
                gvalue = int(gvalue)
                #print gvalue
                img.putpixel((jx, iy), (gvalue, gvalue, gvalue))
        img.save('gaborfilter.jpg')
