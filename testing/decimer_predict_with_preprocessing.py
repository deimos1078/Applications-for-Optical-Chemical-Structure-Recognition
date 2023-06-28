from DECIMER import predict_SMILES
from rdkit import Chem
import os
from PIL import Image
import argparse

# An attached preprocessing step involving the binarization and basic filtering of an image
# before it is recognized by the OCSR engine
def binarize_image(input_image_path):
    image = Image.open(input_image_path)

    # conversion to grayscale
    grayscale_image = image.convert("L")

    # get a threshold, in this case the average pixel value
    pixel_values = list(grayscale_image.getdata())
    average_pixel_value = sum(pixel_values) // len(pixel_values)

    # binarize the image by making all pixel values below the threshold black and all above white
    binarized_image = grayscale_image.point(lambda pixel: 0 if pixel < average_pixel_value else 255, "1")

    # filtering step
    # the idea is to take each pixel and find out how many of its neighboring pixels are black or white
    # based on this amount, the pixel will be either black or white in the filtered picture
    # thresholding is set to 4 again arbitrarily, testing to see which threshold value yields best result can be done 
    filtered_image = binarized_image.copy()
    threshold = 4
    width, height = binarized_image.size


    for y in range (0, height):
        filtered_image.putpixel((0, y), 255)
        filtered_image.putpixel((width-1, y), 255)
    for x in range (0, width):
        filtered_image.putpixel((x, 0), 255)
        filtered_image.putpixel((x, height-1), 255)

    for _ in range(1):
        binarized_image = filtered_image.copy() 
        for x in range(1, width-1):
            for y in range(1, height-1):
                pixel = binarized_image.getpixel((x, y))

                # Count the number of different neighbors
                different_neighbors = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (i != 0 or j != 0):
                            if binarized_image.getpixel((x+i, y+j)) != pixel:
                                different_neighbors += 1
                # Update the pixel value if enough neighbors are different
                if different_neighbors >= threshold:
                    filtered_image.putpixel((x, y), 255)


    output_path = os.path.splitext(input_image_path)[0] + "_binarized.tif"
    filtered_image.save(output_path)
    return output_path


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

for dir_name in os.listdir(input_filepath):
    # Create the dir that the molfiles will be generated to if possible
    os.makedirs(output_filepath + "/" + dir_name, exist_ok = True)
    for filename in os.listdir(input_filepath + "/" + dir_name):
        image_path = output_filepath + "/" + dir_name + '/' + filename
        image_path = binarize_image(image_path)

        SMILES = predict_SMILES(image_path)

        os.remove(image_path)

        mol = Chem.MolFromSmiles(SMILES)
        if (mol is None):
            mol = Chem.MolFromSmiles('C1NCN1.C1NCN1') #structure indicating failure to parse smiles
        try:
            molfile = Chem.MolToMolBlock(mol)
        except:
            molfile = Chem.MolToMolBlock(Chem.MolFromSmiles('C1NCN1.C1NCN1'))
        output_file = output_filepath + "/decimer/" + dir_name + '/' + filename.split(".")[0] + ".mol"
        with open(output_file, "w") as f:
            f.write(molfile)
