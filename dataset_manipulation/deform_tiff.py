from collections import namedtuple
from wand.color import Color
from wand.image import Image
import numpy as np
import random
import argparse
import os

Point = namedtuple('Point', ['x', 'y', 'i', 'j'])

# Distorts an image using 10 times (arbitrary choice, it's possible different amount of repeats
# will yield other interesting results, I consider this the sweet spot) repeated Shepard's distortion
# 
# This method can definitely be improved and made much more readable, but I am keeping it as is
# for now to archive the process that created the distorted files used in the bachelor's
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

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Script for adding noise to image files")

# Add command line arguments
parser.add_argument("input_file", help="Input file path")
parser.add_argument("output_file", help="Output file path")

# Parse the command line arguments
args = parser.parse_args()

# Access the input and output file paths
input_filepath = args.input_file
output_filepath =  args.output_file

# Make the output directories if they don't exist yet
for scale in np.arange(0.1, 0.6, 0.1):
    os.makedirs(output_filepath + "/" + "tiffs_distort_" + str(int(scale*100)), exist_ok=True)

for filename in os.listdir(input_filepath):
    for scale in np.arange(0.1, 0.6, 0.1):
        output_filename = output_filepath + "/" + "tiffs_distorted_" + str(int(scale*100)) + "/" + filename
        img = Image(filename = input_filepath + "/" + filename)
        img_distorted = distort(img, scale)
        img_distorted.save(filename = output_filepath + "/" + output_filename)