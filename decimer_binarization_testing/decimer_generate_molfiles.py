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
    output_path = os.path.splitext(input_image_path)[0] + "_binarized.tif"
    binarized_image.save(str(output_path))
    return output_path

path = 'data_decimer_binarization_test'
for dir_name in os.listdir(path):
    os.makedirs('generated_molfiles/decimer_binarized/' + dir_name, exist_ok = True)
    for i in range(1, 130):
        image_path = 'data_decimer_binarization_test/' + dir_name + '/' + str(i) + '.tif'
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
        output_file = 'generated_molfiles/decimer_binarized/' + dir_name + '/' + str(i) + '.mol'
        with open(output_file, "w") as f:
            f.write(molfile)
