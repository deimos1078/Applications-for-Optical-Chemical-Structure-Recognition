
import subprocess
import numpy as np

# Loop over all the TIFF files in the input directory
for i in range(1, 130):
    input_filepath = "tiffs/" + str(i) + ".tif"

    for attenuation in np.arange(0.5, 2.6, 0.5):
        output_filepath = "tiffs_convert_" + str(int(attenuation * 10)) + "/" + str(i) + ".tif"
        command = ["magick", "convert", input_filepath, "-colorspace", "gray","-attenuate", str(attenuation), "+noise", "Gaussian",  output_filepath]
        subprocess.run(command)