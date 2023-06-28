import subprocess
import numpy as np
import argparse
import os

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
for attenuation in np.arange(0.5, 2.6, 0.5):
    os.makedirs(output_filepath + "/" + "tiffs_convert_" + str(int(attenuation * 10)), exist_ok=True)

# Iterate through input directory, blend each image and save it into corresponding output directory
for filename in os.listdir(input_filepath):
    for attenuation in np.arange(0.5, 2.6, 0.5):
        output_filename = output_filepath + "/"  + "tiffs_convert_" + str(int(attenuation * 10)) + "/" + filename
        command = ["magick", "convert", input_filepath + "/" + filename, "-colorspace", "gray","-attenuate", str(attenuation), "+noise", "Gaussian",  output_filename]
        subprocess.run(command)