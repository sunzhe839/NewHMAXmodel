__author__ = 'yuki'
#coding UTF-8
from PIL import Image

Im_name = raw_input()

image = Image.open(Im_name).resize((480, 360))
size = image.size
print image.format, size, image.mode

#image.show()

#make gray scale
ax = size[0]
ay = size[1]
gIm = Image.new("RGB", (ax, ay))
gIm2 = Image.new("RGB", (ax, ay))

for i in range(0, ax):
 for j in range(0, ay):
  px = image.getpixel((i, j))
  gpx = (px[0] + px[1] + px[2])/3
  gIm.putpixel((i, j), (gpx, gpx, gpx)) #grayscale1
  gpx2 = max(px)
  gIm2.putpixel((i, j), (gpx2, gpx2, gpx2)) #grayscale2

gIm.save("gray_image1.jpg")
gIm2.save("gray_image2.jpg")
