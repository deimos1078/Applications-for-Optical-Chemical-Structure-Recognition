from PIL import Image
import argparse
import os

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Script for compressing image files")

# Add command line arguments
parser.add_argument("input_file", help="Input file path")
parser.add_argument("output_file", help="Output file path")

# Parse the command line arguments
args = parser.parse_args()

# Access the input and output file paths
input_filepath = args.input_file
output_filepath =  args.output_file

# Make the output directories if they don't exist yet
for compression_pctg in range (20, 81, 20):
    os.makedirs(output_filepath + "/" + "tiffs_compressed_" + str(compression_pctg), exist_ok=True)
os.makedirs(output_filepath + "/" + "tiffs_compressed_99", exist_ok=True)

for filename in os.listdir(input_filepath):
    img = Image.open(input_filepath + "/" + filename)
    for compression_pctg in range(20, 81, 20):
        output_filename = output_filepath + "/" + "tiffs_compressed_" + str(compression_pctg) + "/" + filename
        img.save(output_filename, "JPEG", quality=(100-compression_pctg))
    output_filename = output_filepath + "/" + "tiffs_compressed_99" + "/" + filename
    img.save(output_filename, "JPEG", quality=1)