from PIL import Image
import os

# Script will seach for cropped photos and sew them together from lowest to highest number in the filename.
# to create a single long jpg image file. 


dir_path = os.path.dirname(os.path.realpath(__file__))
crop_pics = f"{dir_path}/cropd"
jpgs = os.path.join(dir_path, crop_pics)


# List of filenames
#filenames = []
filenames = os.listdir(jpgs)
#filenames.append(os.listdir(jpgs))

# Sort the filenames list by the number in each filename in ascending order
filenames = sorted(filenames,key=lambda x: int(x.split(".")[0]))
print(filenames)
#print(filenames.sort(key=lambda f: int(f.split('.')[0][5:])))


# Create an empty image with the same width as the first image and a height equal to the sum of all the images' heights
os.chdir(crop_pics)
width, height = Image.open(filenames[0]).size
result = Image.new('RGB', (width, sum(Image.open(f).size[1] for f in filenames)))

# Paste each image into the result image
y_offset = 0
for filename in filenames:
    img = Image.open(filename)
    result.paste(img, (0, y_offset))
    y_offset += img.size[1]

# Save the result image
result.save('combined.jpg')