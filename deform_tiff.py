from collections import namedtuple
from wand.color import Color
from wand.image import Image
import numpy as np
import random

Point = namedtuple('Point', ['x', 'y', 'i', 'j'])

def distort(img, scale):
    img.background_color = Color('white')
    img.virtual_pixel = 'background'
    img.border('White', 30, 30)
    for j in range(10):
        args = ()
        for i in range(2):
            x = random.randint(int(0.3*img.size[0]), int(0.7*img.size[0]))
            x_new = random.randint(int(x - scale*0.05*img.size[0]), int(x + scale*0.05*img.size[0]))
            y = random.randint(int(0.3*img.size[1]), int(0.7*img.size[1]))
            y_new = random.randint(int(y - scale*0.05*img.size[1]), int(y + scale*0.05*img.size[1]))
            args = args + Point(x, y, x_new, y_new)

        img.distort('shepards', args)
    return img

for i in range(1, 130):
    filepath_in = "data/tiffs/" + str(i) + ".tif"
    for scale in np.arange(0.1, 0.6, 0.1):
        filepath_out = "data/tiffs_distorted_" + str(int(scale*100)) + "/" + str(i) + ".tif"
        img = Image(filename = filepath_in)
        img_distorted = distort(img, scale)
        img_distorted.save(filename = filepath_out)