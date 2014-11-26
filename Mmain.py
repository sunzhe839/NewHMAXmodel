__author__ = 'yuki'
#coding UTF-8
import numpy
from PIL import Image
from PIL import ImageOps
from Layer import *
from MGaborFilter import *

nsii=12
ns1i=12
nc1i=11
ns2i=11
nc2i=2
s1SStep=1
c1SStep=1
s2SStep=1
c2SStep=4
targetid=1
fnum=35

def Maxrun():


    #fs_gabor=fs1()
    #print fs_gabor
#    nsci=12
    #ns1=[]
    #Nsilay=Layer()
    #smi=si
    nsi=[]
    nsi.append(Layer(256, 1, -127.5000000000000000, 1.0000000000000000))
    nsi.append(Layer(214, 1, -126.6505577477897901, 1.1892071150027210))
    nsi.append(Layer(180, 1, -126.572113832391991, 1.4142135623730949))
    nsi.append(Layer(152, 1, -126.9753587033108744, 1.6817928305074288))
    nsi.append(Layer(128, 1, -126.9999999999999858, 1.9999999999999998))
    nsi.append(Layer(106, 1, -124.8667470752856872, 2.3784142300054416))
    nsi.append(Layer(90, 1, -125.8650070512054242, 3.363585661014857))
    nsi.append(Layer(76, 1, -126.1344622880571649, 3.9999999999999991))
    nsi.append(Layer(64, 1, -125.9999999999999716, 4.7568284600108832))
    nsi.append(Layer(52, 1, -121.2991257302775239, 4.7568284600108832))
    nsi.append(Layer(44, 1, -121.6223663640861190, 5.6568542494923779))
    nsi.append(Layer(38, 1, -124.4526694575497032, 6.7271713220297134))


    ns1=[]
    ns1.append(Layer(246, fs1.FCount(), -122.5000000000000000, 1.0000000000000000))
    ns1.append(Layer(204, fs1.FCount(), -120.7045221727761799, 1.1892071150027210))
    ns1.append(Layer(170, fs1.FCount(), -119.5010460205265161, 1.4142135623730949))
    ns1.append(Layer(142, fs1.FCount(), -118.5663945507737225, 1.6817928305074288))
    ns1.append(Layer(118, fs1.FCount(), -116.9999999999999858, 1.9999999999999998))
    ns1.append(Layer(96, fs1.FCount(), -112.9746759252584809, 2.3784142300054416))
    ns1.append(Layer(80, fs1.FCount(), -111.7228714274744874, 2.8284271247461894))
    ns1.append(Layer(66, fs1.FCount(), -109.3165339829828753, 3.3635856610148576))
    ns1.append(Layer(54, fs1.FCount(), -105.9999999999999716, 3.9999999999999991))
    ns1.append(Layer(42, fs1.FCount(), -97.5149834302231113, 4.7568284600108832))
    ns1.append(Layer(34, fs1.FCount(), -93.3380951166242312, 5.6568542494923779))
    ns1.append(Layer(28, fs1.FCount(), -90.8168128474011240, 6.7271713220297134))
    '''
    nc1=[]
    nc1.append(Layer(47, fs1.FCount(), -115.0000000000000000,   5.0000000000000000))
    nc1.append(Layer(39, fs1.FCount(), -112.9746759252584951,   5.9460355750136049))
    nc1.append(Layer(33, fs1.FCount(), -113.1370849898475939,   7.0710678118654746))
    nc1.append(Layer(27, fs1.FCount(), -109.3165339829828895,   8.4089641525371448))
    nc1.append(Layer(21, fs1.FCount(),  -99.9999999999999858,   9.9999999999999982))
    nc1.append(Layer(17, fs1.FCount(),  -95.1365692002176644,  11.8920711500272080))
    nc1.append(Layer(15, fs1.FCount(),  -98.9949493661166287,  14.1421356237309475))
    nc1.append(Layer(11, fs1.FCount(),  -84.0896415253714480,  16.8179283050742896))
    nc1.append(Layer(9, fs1.FCount(),  -79.9999999999999858,  19.9999999999999964))
    nc1.append(Layer(7, fs1.FCount(),  -71.3524269001632518,  23.7841423000544161))
    nc1.append(Layer(5, fs1.FCount(),  -56.5685424949237756,  28.2842712474618878))

    ns2=[]
    ns2.append(Layer(44, fs2.FCount(), -107.5000000000000000,   5.0000000000000000))
    ns2.append(Layer(36, fs2.FCount(), -104.0556225627380798,   5.9460355750136049))
    ns2.append(Layer(30, fs2.FCount(), -102.5304832720493806,   7.0710678118654746))
    ns2.append(Layer(24, fs2.FCount(),  -96.7030877541771616,   8.4089641525371448))
    ns2.append(Layer(18, fs2.FCount(),  -84.9999999999999858,   9.9999999999999982))
    ns2.append(Layer(14, fs2.FCount(),  -77.2984624751768479,  11.8920711500272080))
    ns2.append(Layer(12, fs2.FCount(),  -77.7817459305202163,  14.1421356237309475))
    ns2.append(Layer(8, fs2.FCount(),  -58.8627490677600136,  16.8179283050742896))
    ns2.append(Layer(6, fs2.FCount(),  -49.9999999999999929,  19.9999999999999964))
    ns2.append(Layer(4, fs2.FCount(),  -35.6762134500816259,  23.7841423000544161))
    ns2.append(Layer(2, fs2.FCount(),  -14.1421356237309439,  28.2842712474618878))
    print "fs2"
    print fs2.FCount()

    nc2=[]
    nc2.append(Layer(1, fs2.FCount(),    0.0000000000000000,   1.0000000000000000))
    nc2.append(Layer(1, fs2.FCount(),    0.0000000000000000,   1.0000000000000000))
'''


    #print ns1
    #return (nsi,ns1,nc1,ns2,nc2)
    return (nsi, ns1)


if __name__=="__main__":
    Im_name = raw_input()

    image = Image.open(Im_name)

    #fs1=GaborFilter(11, 0.3, 5.641, 4.5128, 12)
    fs1=GaborFilter(11, 0.4, 2.0, 1.0, 12)
    """
    si = []
    si.append(ImageOps.grayscale(image).resize((256, 256)))
    si.append(ImageOps.grayscale(image).resize((214, 214)))
    si.append(ImageOps.grayscale(image).resize((180, 180)))
    si.append(ImageOps.grayscale(image).resize((152, 152)))
    si.append(ImageOps.grayscale(image).resize((128, 128)))
    si.append(ImageOps.grayscale(image).resize((106, 106)))
    si.append(ImageOps.grayscale(image).resize((90, 90)))
    si.append(ImageOps.grayscale(image).resize((76, 76)))
    si.append(ImageOps.grayscale(image).resize((64, 64)))
    si.append(ImageOps.grayscale(image).resize((52, 52)))
    si.append(ImageOps.grayscale(image).resize((44, 44)))
    si.append(ImageOps.grayscale(image).resize((38, 38)))
    sii=numpy.array(si) #Convert list to numpy array



    nsi, ns1 = Maxrun()

    for nn in range(nsii):
        nsi[nn].SetLayer(sii[nn])

    for ns1nn in range(ns1i):
        fs1.ComputeLayer(nsi[ns1nn].xySize, nsi[ns1nn], ns1[ns1nn])
    """

    #test gabor filter
    o = 90 #output image size
    i = 100 #input image size

    Output = numpy.zeros((4, o, o), dtype=float)
    Outputsum = numpy.zeros((o, o), dtype=float)
    gimg = ImageOps.grayscale(image).resize((i, i))
    gimg.save('base.jpg')
    imgArray = numpy.asarray(gimg).T*1.0/255

    fs1.ComputeLayer(i, imgArray, Output)

    img = Image.new('RGB', (o, o))
    for orient in range(4):
        for x in range(o):
            for y in range(o):
                gvalue = int(Output[orient, x, y]*255)
                Outputsum[x, y] += gvalue
                img.putpixel((x, y), (gvalue, gvalue, gvalue))
        img.save(str(orient)+'.jpg')

    #sum of 4 orientations
    sumimg = Image.new('RGB', (o, o))
    for sx in range(o):
        for sy in range(o):
            svalue = int(Outputsum[sx, sy])
            sumimg.putpixel((sx, sy), (svalue, svalue, svalue))
    sumimg.show()

