from PIL import Image

for i in range(1, 131):
    filepath_in = "tiffs/" + str(i) + ".tif"
    img = Image.open(filepath_in)
    for compression_pctg in range(20, 81, 20):
        filepath_out = "tiffs_compressed_" + str(compression_pctg) + "/" + str(i) + ".tif"
        img.save(filepath_out, "JPEG", quality=(100-compression_pctg))
    filepath_out = "tiffs_compressed_99/" + str(i) + ".tif"
    img.save(filepath_out, "JPEG", quality=1)