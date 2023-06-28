import subprocess
import numpy as np
import argparse
import os

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Script for blending image files")

# Add command line arguments
parser.add_argument("input_file", help="Input file path")
parser.add_argument("output_file", help="Output file path")

# Parse the command line arguments
args = parser.parse_args()

# Access the input and output file paths
input_filepath = args.input_file
output_filepath =  args.output_file

# Make the output directories if they don't exist yet
for overlay in range (20, 81, 20):
    os.makedirs(output_filepath + "/" + "tiffs_blend_" + str(overlay), exist_ok=True)

# Iterate through input directory, blend each image and save it into corresponding output directory
for filename in os.listdir(input_filepath):
    for overlay in range (20, 81, 20):
        output_filename = output_filepath + "/" + "tiffs_blend_" + str(overlay) + "/" + filename
        command = ["magick", "composite", "-blend", str(overlay), "layer.tif", input_filepath + "/" + filename, output_filename]
        subprocess.run(command)