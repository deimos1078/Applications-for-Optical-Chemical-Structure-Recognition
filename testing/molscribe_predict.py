from multiprocessing import freeze_support
import torch
from molscribe import MolScribe
from huggingface_hub import hf_hub_download
import os

if __name__ == '__main__':
    freeze_support()
    ckpt_path = hf_hub_download('yujieq/MolScribe', 'swin_base_char_aux_1m.pth')
    model = MolScribe(ckpt_path, device=torch.device('cpu'))

    path = "data"
    for dir_name in os.listdir(path):
        os.makedirs('generated_molfiles/molscribe/' + dir_name, exist_ok = True)
        for i in range(1, 130):
            image_path = 'data/' + dir_name + '/' + str(i) + '.tif'
            output = model.predict_image_file(image_path)
            molfile = output["molfile"]
            output_file = 'generated_molfiles/molscribe/' + dir_name + '/' + str(i) + '.mol'
            with open(output_file, "w") as f:
                f.write(molfile)
