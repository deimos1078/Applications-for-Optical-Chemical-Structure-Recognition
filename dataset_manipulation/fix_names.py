from PIL import Image
import os

for dir_name in os.listdir("data"):
    for i in range(1, 130):
        src = "data/" + dir_name + "/" + str(i) + ".tif"
        dest = "data/" + dir_name + "/" + str(i) + ".png"
        try:
            im = Image.open(src)
            im.save(dest, 'PNG')
        except:
            pass