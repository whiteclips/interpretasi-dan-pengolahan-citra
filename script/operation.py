import numpy as np
from PIL import Image
import sys
import uuid

GRADIENT = 0
MEDIAN = 1
DIFFERENCE = 2

def get_median_of_array(array):
    array.sort()
    num_of_element = len(array)
    if num_of_element % 2 == 0:
        return int((array[int(num_of_element / 2)] + array[int(num_of_element / 2) + 1]) / 2)
    else:
        return array[int((num_of_element - 1) / 2) + 1]

def normalize_point_in_array(point_x, point_y, array):
    width = len(array)
    height = len(array[0])
    if (point_x < 0 or point_x >= width or point_y < 0 or point_y >= height):
        return 0
    else:
        return array[point_x][point_y]

def get_difference_of_point_in_array(point_1_x, point_1_y, point_2_x, point_2_y, array):
    width = len(array)
    height = len(array[0])
    if (point_1_x < 0 or point_1_x >= width or point_1_y < 0 or point_1_y >= height):
        point_1 = 0
    else:
        point_1 = array[point_1_x][point_1_y]
    if (point_2_x < 0 or point_2_x >= width or point_2_y < 0 or point_2_y >= height):
        point_2 = 0
    else:
        point_2 = array[point_2_x][point_2_y]
    return abs(point_1 - point_2)

def do_operation_gradient(array):
    width = len(array)
    height = len(array[0])
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(array[i][j]) + " "
    #     print line
    # print "-----"
    result_array = [[None for y in range(height) ] for x in range(width)]
    for i in range(width):
        for j in range(height):
            gradient_1 = get_difference_of_point_in_array(i - 1, j - 1, i + 1, j + 1, array)
            gradient_2 = get_difference_of_point_in_array(i, j - 1, i, j + 1, array)
            gradient_3 = get_difference_of_point_in_array(i + 1, j - 1, i - 1, j + 1, array)
            gradient_4 = get_difference_of_point_in_array(i + 1, j, i - 1, j, array)
            result_array[i][j] = max(gradient_1, gradient_2, gradient_3, gradient_4)
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(result_array[i][j]) + " "
    #     print line
    return result_array

def do_operation_median(array):
    width = len(array)
    height = len(array[0])
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(array[i][j]) + " "
    #     print line
    # print "-----"
    result_array = [[None for y in range(height) ] for x in range(width)]
    for i in range(width):
        for j in range(height):
            point_1 = normalize_point_in_array(i - 1, j - 1, array)
            point_2 = normalize_point_in_array(i, j - 1, array)
            point_3 = normalize_point_in_array(i + 1, j - 1, array)
            point_4 = normalize_point_in_array(i - 1, j, array)
            point_5 = normalize_point_in_array(i + 1, j, array)
            point_6 = normalize_point_in_array(i - 1, j + 1, array)
            point_7 = normalize_point_in_array(i, j + 1, array)
            point_8 = normalize_point_in_array(i + 1, j + 1, array)
            values = [point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8]
            # print values
            # print get_median_of_array(values)
            # sys.exit()
            result_array[i][j] = get_median_of_array(values)
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(result_array[i][j]) + " "
    #     print line
    return result_array

def do_operation_difference(array):
    width = len(array)
    height = len(array[0])
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(array[i][j]) + " "
    #     print line
    # print "-----"
    result_array = [[None for y in range(height) ] for x in range(width)]
    for i in range(width):
        for j in range(height):
            difference_1 = get_difference_of_point_in_array(i, j, i - 1, j - 1, array)
            difference_2 = get_difference_of_point_in_array(i, j, i, j - 1, array)
            difference_3 = get_difference_of_point_in_array(i, j, i + 1, j - 1, array)
            difference_4 = get_difference_of_point_in_array(i, j, i + 1, j, array)
            difference_5 = get_difference_of_point_in_array(i, j, i + 1, j + 1, array)
            difference_6 = get_difference_of_point_in_array(i, j, i, j + 1, array)
            difference_7 = get_difference_of_point_in_array(i, j, i - 1, j + 1, array)
            difference_8 = get_difference_of_point_in_array(i, j, i - 1, j, array)
            result_array[i][j] = max(difference_1, difference_2, difference_3, difference_4, difference_5, difference_6, difference_7, difference_8)
    # for j in range(10):
    #     line = ""
    #     for i in range(10):
    #         line = line + str(result_array[i][j]) + " "
    #     print line
    return result_array

def do_operation(array, type_of_operation):
    if type_of_operation == GRADIENT:
        return do_operation_gradient(array)
    elif type_of_operation == MEDIAN:
        return do_operation_median(array)
    elif type_of_operation == DIFFERENCE:
        return do_operation_difference(array)

def preprocess_image(input_image, type_of_operation):
    # if (len(sys.argv) < 3):
    #     print "Please provide the arguments."
    #     print "RUN INSTRUCTION"
    #     print "python operation.py file_name_of_image type_of_operation"
    #     print "file_name_of_image, for example, is image_bird.jpg"
    #     print "type_of_operation is either 0, 1, or 2. 0: GRADIENT, 1: MEDIAN, 2: DIFFERENCE" 
    #     sys.exit()

    # file_name = sys.argv[1]
    # type_of_operation = int(sys.argv[2])
    
    # type_of_operation = operation

    image = input_image
    pixel = image.load()
    width = image.size[0]
    height = image.size[1]
    
    try:
        value = int(pixel[0, 0])
        gray_array = [[None for y in range(height) ] for x in range(width)]    
        for i in range(width):
            for j in range(height):
                gray = pixel[i,j]
                gray_array[i][j] = gray
        if type_of_operation == GRADIENT:
            result_gray_array = do_operation_gradient(gray_array)
        elif type_of_operation == MEDIAN:
            result_gray_array = do_operation_median(gray_array)
        elif type_of_operation == DIFFERENCE:
            result_gray_array = do_operation_difference(gray_array)
        else:
            print("Type of operation not recognized.", file=sys.stdout)
            # sys.exit()
        for i in range(width):
            for j in range(height):
                image.putpixel((i, j), result_gray_array[i][j])
    except:
        red_array = [[None for y in range(height) ] for x in range(width)]
        green_array = [[None for y in range(height) ] for x in range(width)]
        blue_array = [[None for y in range(height) ] for x in range(width)]
        for i in range(width):
            for j in range(height):
                red = pixel[i,j][0]
                red_array[i][j] = red
                green = pixel[i,j][1]
                green_array[i][j] = green
                blue = pixel[i,j][2]
                blue_array[i][j] = blue
        if type_of_operation == GRADIENT:
            result_red_array = do_operation_gradient(red_array)
            result_green_array = do_operation_gradient(green_array)
            result_blue_array = do_operation_gradient(blue_array)
        elif type_of_operation == MEDIAN:
            result_red_array = do_operation_median(red_array)
            result_green_array = do_operation_median(green_array)
            result_blue_array = do_operation_median(blue_array)
        elif type_of_operation == DIFFERENCE:
            result_red_array = do_operation_difference(red_array)
            result_green_array = do_operation_difference(green_array)
            result_blue_array = do_operation_difference(blue_array)
        else:
            print("Type of operation not recognized.", file=sys.stdout)
            # sys.exit()
        for i in range(width):
            for j in range(height):
                image.putpixel((i, j), (result_red_array[i][j], result_green_array[i][j], result_blue_array[i][j]))
    
    unique_filename = str(uuid.uuid4()) + '.' + image.format
    print(unique_filename, file=sys.stdout)
    path = 'static/dump/' + unique_filename
    image.save(path)

    return path