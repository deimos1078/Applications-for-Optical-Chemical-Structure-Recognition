from DECIMER import predict_SMILES
from rdkit import Chem
import os
from PIL import Image

def binarize_image(input_image_path):
    image = Image.open(input_image_path)
    grayscale_image = image.convert("L")

    pixel_values = list(grayscale_image.getdata())
    average_pixel_value = sum(pixel_values) // len(pixel_values)

    binarized_image = grayscale_image.point(lambda pixel: 0 if pixel < average_pixel_value else 255, "1")


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

path = 'data'
for dir_name in os.listdir(path):
    os.makedirs('generated_molfiles/decimer_filter/' + dir_name, exist_ok = True)
    for i in range(1, 130):
        image_path = 'data/' + dir_name + '/' + str(i) + '.tif'
        image_path = binarize_image(image_path)

        SMILES = predict_SMILES(image_path)

        os.remove(image_path)

        mol = Chem.MolFromSmiles(SMILES)
        if (mol is None):
            mol = Chem.MolFromSmiles('C1NCN1.C1NCN1') #structure indicating failure to parse smiles
        print(str(i) + " -> " + SMILES)
        try:
            molfile = Chem.MolToMolBlock(mol)
        except:
            molfile = Chem.MolToMolBlock(Chem.MolFromSmiles('C1NCN1.C1NCN1'))
        output_file = 'generated_molfiles/decimer_filter/' + dir_name + '/' + str(i) + '.mol'
        with open(output_file, "w") as f:
            f.write(molfile)
