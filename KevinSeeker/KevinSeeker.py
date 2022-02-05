from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
import os
import numpy as np


def height(col, bounds, transposed_matrix):
    interruption = 0
    total_sum = 0
    chopped_list = np.array([np.max(x) for x in transposed_matrix[col][bounds[1]:]])

    while interruption < max_interruption and total_sum + bounds[1] < image_two.size[1]:
        index = np.where(chopped_list[:][total_sum:] == 0)[0][0]
        if index == 0:
            total_sum += 1
            interruption += 1
        else:
            interruption = 1
            total_sum += index
            
    return total_sum


def cutbackground(image1, image2, area):
    first = image1.crop(area)
    second = image2.crop(area)
    first_picture_array = np.asarray(first)
    second_picture_array = np.asarray(second)

    for index, column in enumerate(second_picture_array):
        chopped_column = np.array([np.max(x) for x in column])
        cut = np.where(chopped_column == 0)[0]
        first_picture_array[index][cut] = 0

    im = Image.fromarray(first_picture_array)
    return im


def objectfinder(image):
    picture = np.asarray(image)
    disruption = np.where(picture < 40, 0, picture)
    im = Image.fromarray(disruption)
    values = im.getbbox()
    mosaic = []

    while values is not None:
        picture = np.asarray(im)
        rotated = picture.transpose(1, 0, 2)
        column = np.where(picture[values[1]] > 0)[0][0]

        high = height(column, values, rotated)
        half_distance = int(high + max_interruption) / 2

        area = (column - half_distance, values[1] - max_interruption, column + half_distance, values[1] + high)
        object_full_image = im.crop(area)

        quality_values = object_full_image.getbbox()

        new_area = [area[0] + quality_values[0], area[1] + quality_values[1],
                    area[0] + quality_values[2], area[1] + quality_values[3]]

        no_background = cutbackground(image_two, im, new_area)
        mosaic.append(no_background)
        no_background.show()
        draw = ImageDraw.Draw(image_two)
        draw.rectangle(new_area, outline='red', width=4)

        wipe = ImageDraw.Draw(im)
        wipe.rectangle(new_area, fill=0)
        values = im.getbbox()


dirname = os.path.dirname(__file__)
firstfile = os.path.join(dirname, 'dublin.jpg')
secondfile = os.path.join(dirname, 'dublin_edited.jpg')
#firstfile = os.path.join(dirname, 'org.jpg')
#secondfile = os.path.join(dirname, 'edited.jpg')

image_one = Image.open(firstfile)
image_two = Image.open(secondfile)

max_interruption = int(0.05 * image_one.size[1])
diff = ImageChops.difference(image_one, image_two)

objectfinder(diff)

image_two.show()

