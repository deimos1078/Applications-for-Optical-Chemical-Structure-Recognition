import subprocess
import numpy as np

for i in range(1, 130):
    input_filepath = "tiffs/" + str(i) + ".tif"
    
    for overlay in range (20, 81, 20):
        output_filepath = "tiffs_blend_" + str(overlay) + "/" + str(i) + ".tif"
        command = ["magick", "composite", "-blend", str(overlay), "layer.tif", input_filepath, output_filepath]
        subprocess.run(command)