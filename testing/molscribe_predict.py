from multiprocessing import freeze_support
import torch
from molscribe import MolScribe
from huggingface_hub import hf_hub_download
import os
import argparse


def main():
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
    
    # Necessary
    freeze_support()

    # download the model
    ckpt_path = hf_hub_download('yujieq/MolScribe', 'swin_base_char_aux_1m.pth')
    model = MolScribe(ckpt_path, device=torch.device('cpu'))


    for dir_name in os.listdir(input_filepath):
        os.makedirs(output_filepath + "/" + dir_name, exist_ok = True)
        for filename in os.listdir(input_filepath + "/" + filename):
            image_path = input_filepath + "/" + dir_name + '/' + filename
            output = model.predict_image_file(image_path)
            molfile = output["molfile"]
            output_file = output_filepath + '/molscribe/' + dir_name + '/' + filename.split(".")[0] + '.mol'
            with open(output_file, "w") as f:
                f.write(molfile)

if __name__ == '__main__':
    main()
    
