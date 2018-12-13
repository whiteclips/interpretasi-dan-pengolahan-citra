from PIL import Image, ImageDraw
import math
import uuid


def get_hsv_from_rgb(red, green, blue):
    red, green, blue = red / 255.0, green / 255.0, blue / 255.0
    mx = max(red, green, blue)
    mn = min(red, green, blue)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == red:
        h = (60 * ((green - blue) / df) + 360) % 360
    elif mx == green:
        h = (60 * ((blue - red) / df) + 120) % 360
    elif mx == blue:
        h = (60 * ((red - green) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return h, s, v


def get_ycbcr_from_rgb(red, green, blue):
    y = math.trunc((0.257 * red) + (0.504 * green) + (0.098 * blue) + 16)
    cb = math.trunc(((-0.148) * red) - (0.291 * green) + (0.439 * blue) + 128)
    cr = math.trunc((0.439 * red) - (0.368 * green) - (0.071 * blue) + 128)
    return y, cb, cr


def get_hsv_matrix_from_rgb_matrix(width, height, rgb_matrix):
    hsv_matrix = [[0 for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            red = rgb_matrix[j, i][0]
            green = rgb_matrix[j, i][1]
            blue = rgb_matrix[j, i][2]
            hsv_matrix[i][j] = get_hsv_from_rgb(red, green, blue)
    return hsv_matrix


def get_ycbcr_matrix_from_rgb_matrix(width, height, rgb_matrix):
    ycbcr_matrix = [[0 for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            red = rgb_matrix[j, i][0]
            green = rgb_matrix[j, i][1]
            blue = rgb_matrix[j, i][2]
            ycbcr_matrix[i][j] = get_ycbcr_from_rgb(red, green, blue)
    return ycbcr_matrix


def is_skin_pixel(i, j, rgb_matrix, hsv_matrix):
    red = rgb_matrix[j, i][0]
    green = rgb_matrix[j, i][1]
    blue = rgb_matrix[j, i][2]
    hue = hsv_matrix[i][j][0]
    saturation = hsv_matrix[i][j][1]

    return 0 <= hue <= 50 and 23 <= saturation <= 68 and red > 95 and green > 40 and blue > 20 and red > green and red > blue and abs(
        red - green) > 15


def is_skin_pixel(i, j, rgb_matrix, ycbcr_matrix):
    red = rgb_matrix[j, i][0]
    green = rgb_matrix[j, i][1]
    blue = rgb_matrix[j, i][2]
    y = ycbcr_matrix[i][j][0]
    cb = ycbcr_matrix[i][j][1]
    cr = ycbcr_matrix[i][j][2]

    cond_1 = cr <= (1.5862 * cb) + 20
    cond_2 = cr >= (0.3448 * cb) + 76.2069
    cond_3 = cr >= (-4.5652 * cb) + 234.5652
    cond_4 = cr <= (-1.15 * cb) + 301.75
    cond_5 = cr <= (-2.2857 * cb) + 432.85

    return red > 95 and green > 20 and blue > 20 and red > green and red > blue and abs(
        red - green) > 15 and cr > 135 and cb > 85 and y > 80 and cond_1 and cond_2 and cond_3 and cond_4 and cond_5


def mask_image_to_get_face(image, outer_color, inner_color=None):
    for i in range(image.height):
        for j in range(image.width):
            if is_skin_pixel(i, j, image.rgb_matrix, image.hsv_matrix) or is_skin_pixel(i, j, image.rgb_matrix,
                                                                                        image.ycbcr_matrix):
                if inner_color is not None:
                    image.rgb_matrix[j, i] = inner_color
            else:
                image.rgb_matrix[j, i] = outer_color
    return image.output_image


def is_boundary(image, point):
    x = point[0]
    y = point[1]
    if x < 0 or y < 0 or x >= image.width or y >= image.height:
        return False
    if image.rgb_matrix[x, y] == image.outer_color:
        return False
    if x == 0 or y == 0 or x == image.width - 1 or y == image.height - 1:
        return True
    if image.rgb_matrix[x - 1, y - 1] != image.outer_color and image.rgb_matrix[x + 1, y + 1] == image.outer_color:
        return True
    if image.rgb_matrix[x - 1, y - 1] == image.outer_color and image.rgb_matrix[x + 1, y + 1] != image.outer_color:
        return True
    if image.rgb_matrix[x, y - 1] != image.outer_color and image.rgb_matrix[x, y + 1] == image.outer_color:
        return True
    if image.rgb_matrix[x, y - 1] == image.outer_color and image.rgb_matrix[x, y + 1] != image.outer_color:
        return True
    if image.rgb_matrix[x + 1, y - 1] != image.outer_color and image.rgb_matrix[x - 1, y + 1] == image.outer_color:
        return True
    if image.rgb_matrix[x + 1, y - 1] == image.outer_color and image.rgb_matrix[x - 1, y + 1] != image.outer_color:
        return True
    if image.rgb_matrix[x + 1, y] != image.outer_color and image.rgb_matrix[x - 1, y] == image.outer_color:
        return True
    if image.rgb_matrix[x + 1, y] == image.outer_color and image.rgb_matrix[x - 1, y] != image.outer_color:
        return True
    return False


def find_min_max_region(region):
    min_x, min_y, max_x, max_y = 1000000, 1000000, 0, 0
    for point in region:
        x = point[0]
        y = point[1]
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    min_point = (min_x, min_y)
    max_point = (max_x, max_y)
    distance_x = max_x - min_x
    distance_y = max_y - min_y
    distance = math.sqrt((distance_x * distance_x) + (distance_y * distance_y))
    return min_point, max_point, distance, len(region)


def is_point_inside_image(image, point):
    return 0 <= point[0] < image.width and 0 <= point[1] < image.height


def evaluate_region_flood_fill(image):
    regions = []
    visited = [[0 for j in range(image.width)] for i in range(image.height)]
    for i in range(image.height):
        for j in range(image.width):
            if is_point_inside_image(image, (j, i)) and visited[i][j] == 0 and image.rgb_matrix[
                j, i] != image.outer_color:
                region = []
                potential_points = [(j, i)]
                visited[i][j] = 1
                while len(potential_points) != 0:
                    point = potential_points.pop(0)
                    region.append(point)
                    point1 = (point[0] - 1, point[1] - 1)
                    if is_point_inside_image(image, point1) and visited[point1[1]][point1[0]] == 0 and image.rgb_matrix[
                        point1] != image.outer_color:
                        visited[point1[1]][point1[0]] = 1
                        potential_points.append(point1)
                    point2 = (point[0], point[1] - 1)
                    if is_point_inside_image(image, point2) and visited[point2[1]][point2[0]] == 0 and image.rgb_matrix[
                        point2] != image.outer_color:
                        visited[point2[1]][point2[0]] = 1
                        potential_points.append(point2)
                    point3 = (point[0] + 1, point[1] - 1)
                    if is_point_inside_image(image, point3) and visited[point3[1]][point3[0]] == 0 and image.rgb_matrix[
                        point3] != image.outer_color:
                        visited[point3[1]][point3[0]] = 1
                        potential_points.append(point3)
                    point4 = (point[0] + 1, point[1])
                    if is_point_inside_image(image, point4) and visited[point4[1]][point4[0]] == 0 and image.rgb_matrix[
                        point4] != image.outer_color:
                        visited[point4[1]][point4[0]] = 1
                        potential_points.append(point4)
                    point5 = (point[0] + 1, point[1] + 1)
                    if is_point_inside_image(image, point5) and visited[point5[1]][point5[0]] == 0 and image.rgb_matrix[
                        point5] != image.outer_color:
                        visited[point5[1]][point5[0]] = 1
                        potential_points.append(point5)
                    point6 = (point[0], point[1] + 1)
                    if is_point_inside_image(image, point6) and visited[point6[1]][point6[0]] == 0 and image.rgb_matrix[
                        point6] != image.outer_color:
                        visited[point6[1]][point6[0]] = 1
                        potential_points.append(point6)
                    point7 = (point[0] - 1, point[1] + 1)
                    if is_point_inside_image(image, point7) and visited[point7[1]][point7[0]] == 0 and image.rgb_matrix[
                        point7] != image.outer_color:
                        visited[point7[1]][point7[0]] = 1
                        potential_points.append(point7)
                    point8 = (point[0] - 1, point[1])
                    if is_point_inside_image(image, point8) and visited[point8[1]][point8[0]] == 0 and image.rgb_matrix[
                        point8] != image.outer_color:
                        visited[point8[1]][point8[0]] = 1
                        potential_points.append(point8)
                regions.append(region)
    return regions


def find_unwanted_region(image, region, region_info):
    unwanted_region = [[0 for j in range(image.width)] for i in range(image.height)]
    x_min, y_min = region_info["min_point"][0], region_info["min_point"][1]
    x_max, y_max = region_info["max_point"][0], region_info["max_point"][1]
    # for i in range(y_min, y_max + 1):
    #     for j in range(x_min, x_max + 1):
    #         if (j, i) not in region:
    #             unwanted_region[i][j] = 1
    #         else:
    #             break
    #     for j in range(x_max, x_min - 1, -1):
    #         if (j, i) not in region:
    #             unwanted_region[i][j] = 1
    #         else:
    #             break
    # for j in range(x_min, x_max + 1):
    #     for i in range(y_min, y_max + 1):
    #         if unwanted_region[i][j] == 0:
    #             if (j, i) not in region:
    #                 unwanted_region[i][j] = 1
    #             else:
    #                 break
    #     for i in range(y_max, y_min - 1, -1):
    #         if unwanted_region[i][j] == 0:
    #             if (j, i) not in region:
    #                 unwanted_region[i][j] = 1
    #             else:
    #                 break
    for i in range(y_min, y_max + 1):
        for j in range(x_min - 1, -1, -1):
            unwanted_region[i][j] = 1
        for j in range(x_max + 1, image.width):
            unwanted_region[i][j] = 1

    return unwanted_region


def is_point_inside_region(point, x_value, y_value):
    return x_value[0] <= point[0] <= x_value[1] and y_value[0] <= point[1] <= y_value[1]


def is_point_valid(image, point):
    return 0 <= point[0] <= image.width - 1 and 0 <= point[1] <= image.height - 1


def select_valid_subregion_eye(region_info, subregions, subregions_info):
    new_subregions = []
    new_subregions_info = []
    x_min, y_min = region_info["min_point"][0], region_info["min_point"][1]
    x_max, y_max = region_info["max_point"][0], region_info["max_point"][1]
    x_min_face, y_min_face = x_min, y_min
    x_max_face, y_max_face = x_max, y_max
    height_of_face = y_max - y_min
    width_of_face = x_max - x_min
    for i in range(len(subregions)):
        subregion = subregions[i]
        subregion_info = subregions_info[i]
        x_min, y_min = subregion_info["min_point"][0], subregion_info["min_point"][1]
        x_max, y_max = subregion_info["max_point"][0], subregion_info["max_point"][1]
        height_of_subregion = y_max - y_min
        width_of_subregion = x_max - x_min

        validity = 1.2 * height_of_subregion <= width_of_subregion <= 3.2 * height_of_subregion and \
                   0.125 * width_of_face <= width_of_subregion <= 0.3 * width_of_face and \
                   0.25 * height_of_face <= y_min - y_min_face and y_max - y_min_face <= 0.5 * height_of_face

        if validity:
            new_subregions.append(subregion)
            new_subregions_info.append(subregion_info)

    return new_subregions, new_subregions_info


def select_valid_subregion_mouth(region_info, subregions, subregions_info):
    new_subregions = []
    new_subregions_info = []
    x_min, y_min = region_info["min_point"][0], region_info["min_point"][1]
    x_max, y_max = region_info["max_point"][0], region_info["max_point"][1]
    x_min_mouth, y_min_mouth = x_min, y_min
    x_max_mouth, y_max_mouth = x_max, y_max
    height_of_face = y_max - y_min
    width_of_face = x_max - x_min
    for i in range(len(subregions)):
        subregion = subregions[i]
        subregion_info = subregions_info[i]
        x_min, y_min = subregion_info["min_point"][0], subregion_info["min_point"][1]
        x_max, y_max = subregion_info["max_point"][0], subregion_info["max_point"][1]
        height_of_subregion = y_max - y_min
        width_of_subregion = x_max - x_min

        validity = height_of_subregion <= width_of_subregion <= 6 * height_of_subregion and \
                   0.2 * width_of_face <= width_of_subregion <= 0.6 * width_of_face and \
                   0.5 * height_of_face <= y_min - y_min_mouth and y_max - y_min_mouth <= 0.75 * height_of_face

        if validity:
            new_subregions.append(subregion)
            new_subregions_info.append(subregion_info)

    return new_subregions, new_subregions_info


def select_valid_subregion_nose(eye_subregion, eye_subregion_info, mouth_subregion, mouth_subregion_info):
    new_subregions_info = {}

    y_max_eye = eye_subregion_info["max_point"][1]
    y_min_mouth = mouth_subregion_info["max_point"][1]
    distance_eye_mouth = y_min_mouth - y_max_eye
    width_mouth = mouth_subregion_info["max_point"][0] - mouth_subregion_info["min_point"][0]
    center_mouth = (mouth_subregion_info["max_point"][0] + mouth_subregion_info["min_point"][0]) / 2

    width_nose = width_mouth * 0.75
    x_min_nose = center_mouth - (width_nose / 2)
    x_max_nose = center_mouth + (width_nose / 2)

    y_max_nose = y_max_eye + 0.60 * distance_eye_mouth
    y_min_nose = y_max_nose - width_nose

    new_subregions_info["min_point"] = (x_min_nose, y_min_nose)
    new_subregions_info["max_point"] = (x_max_nose, y_max_nose)
    new_subregions_info["area"] = 100

    return new_subregions_info


def get_constrained_region(image, region_info):
    x_min, y_min = region_info["min_point"][0], region_info["min_point"][1]
    x_max, y_max = region_info["max_point"][0], region_info["max_point"][1]
    x_values = [(0, 0) for i in range(image.height)]
    y_values = [(0, 0) for j in range(image.width)]
    for i in range(y_min, y_max + 1):
        x_min_local = x_min
        x_max_local = x_max
        for j in range(x_min, x_max + 1):
            if image.rgb_matrix[j, i] != image.outer_color:
                x_min_local = j
                break
        for j in range(x_max, x_min - 1, -1):
            if image.rgb_matrix[j, i] != image.outer_color:
                x_max_local = j
                break
        x_values[i] = (x_min_local, x_max_local)

    for j in range(x_min, x_max + 1):
        y_min_local = y_min
        y_max_local = y_max
        for i in range(y_min, y_max + 1):
            if image.rgb_matrix[j, i] != image.outer_color:
                y_min_local = i
                break
        for i in range(y_max, y_min - 1, -1):
            if image.rgb_matrix[j, i] != image.outer_color:
                y_max_local = i
                break
        y_values[j] = (y_min_local, y_max_local)

    return x_values, y_values


def find_subregions_inside_region(image, region, region_info):
    subregions = []
    visited = [[0 for j in range(image.width)] for i in range(image.height)]
    x_values, y_values = get_constrained_region(image, region_info)
    x_min, y_min = region_info["min_point"][0], region_info["min_point"][1]
    x_max, y_max = region_info["max_point"][0], region_info["max_point"][1]
    for i in range(y_min, y_max + 1):
        for j in range(x_min, x_max + 1):
            x_value = x_values[i]
            y_value = y_values[j]
            # print x_value, y_value, (j, i)
            if is_point_inside_region((j, i), x_value, y_value) and visited[i][j] == 0 and image.rgb_matrix[
                j, i] == image.outer_color:
                subregion = []
                potential_points = [(j, i)]
                visited[i][j] = 1
                while len(potential_points) != 0:
                    point = potential_points.pop(0)
                    subregion.append(point)
                    point1 = (point[0] - 1, point[1] - 1)
                    x_value = x_values[point1[1]]
                    y_value = y_values[point1[0]]
                    if is_point_inside_region(point1, x_value, y_value) and \
                                    visited[point1[1]][point1[0]] == 0 and \
                                    image.rgb_matrix[
                                        point1] == image.outer_color:
                        visited[point1[1]][point1[0]] = 1
                        potential_points.append(point1)
                    point2 = (point[0], point[1] - 1)
                    x_value = x_values[point2[1]]
                    y_value = y_values[point2[0]]
                    if is_point_inside_region(point2, x_value, y_value) and \
                                    visited[point2[1]][point2[0]] == 0 and \
                                    image.rgb_matrix[
                                        point2] == image.outer_color:
                        visited[point2[1]][point2[0]] = 1
                        potential_points.append(point2)
                    point3 = (point[0] + 1, point[1] - 1)
                    x_value = x_values[point3[1]]
                    y_value = y_values[point3[0]]
                    if is_point_inside_region(point3, x_value, y_value) and \
                                    visited[point3[1]][point3[0]] == 0 and \
                                    image.rgb_matrix[
                                        point3] == image.outer_color:
                        visited[point3[1]][point3[0]] = 1
                        potential_points.append(point3)
                    point4 = (point[0] + 1, point[1])
                    x_value = x_values[point4[1]]
                    y_value = y_values[point4[0]]
                    if is_point_inside_region(point4, x_value, y_value) and \
                                    visited[point4[1]][point4[0]] == 0 and \
                                    image.rgb_matrix[
                                        point4] == image.outer_color:
                        visited[point4[1]][point4[0]] = 1
                        potential_points.append(point4)
                    point5 = (point[0] + 1, point[1] + 1)
                    x_value = x_values[point5[1]]
                    y_value = y_values[point5[0]]
                    if is_point_inside_region(point5, x_value, y_value) and \
                                    visited[point5[1]][point5[0]] == 0 and \
                                    image.rgb_matrix[
                                        point5] == image.outer_color:
                        visited[point5[1]][point5[0]] = 1
                        potential_points.append(point5)
                    point6 = (point[0], point[1] + 1)
                    x_value = x_values[point6[1]]
                    y_value = y_values[point6[0]]
                    if is_point_inside_region(point6, x_value, y_value) and \
                                    visited[point6[1]][point6[0]] == 0 and \
                                    image.rgb_matrix[
                                        point6] == image.outer_color:
                        visited[point6[1]][point6[0]] = 1
                        potential_points.append(point6)
                    point7 = (point[0] - 1, point[1] + 1)
                    x_value = x_values[point7[1]]
                    y_value = y_values[point7[0]]
                    if is_point_inside_region(point7, x_value, y_value) and \
                                    visited[point7[1]][point7[0]] == 0 and \
                                    image.rgb_matrix[
                                        point7] == image.outer_color:
                        visited[point7[1]][point7[0]] = 1
                        potential_points.append(point7)
                    point8 = (point[0] - 1, point[1])
                    x_value = x_values[point8[1]]
                    y_value = y_values[point8[0]]
                    if is_point_inside_region(point8, x_value, y_value) and \
                                    visited[point8[1]][point8[0]] == 0 and \
                                    image.rgb_matrix[
                                        point8] == image.outer_color:
                        visited[point8[1]][point8[0]] = 1
                        potential_points.append(point8)
                subregions.append(subregion)
    return subregions


class ImageObject:
    def __init__(self, image):
        self.original_image = image
        self.output_image = self.original_image.copy()
        self.width = self.output_image.size[0]
        self.height = self.output_image.size[1]
        self.rgb_matrix = self.output_image.load()
        self.hsv_matrix = get_hsv_matrix_from_rgb_matrix(self.width, self.height, self.rgb_matrix)
        self.ycbcr_matrix = get_ycbcr_matrix_from_rgb_matrix(self.width, self.height, self.rgb_matrix)
        self.outer_color = (0, 0, 0)
        self.inner_color = (255, 255, 255)

    def mask_image(self):
        self.output_image = mask_image_to_get_face(self, self.outer_color, self.inner_color)

    def box_image(self, regions_info, threshold):
        for info in regions_info:
            if info["area"] >= threshold:
                ImageDraw.Draw(self.original_image).rectangle((info["min_point"], info["max_point"]), outline="#FF0000")

    def fill_image(self, regions, regions_info, threshold, color):
        temp_rgb = self.original_image.load()
        total = 0
        for i in range(len(regions)):
            info = regions_info[i]
            if info["area"] >= threshold:
                total = total + 1
                for point in regions[i]:
                    temp_rgb[point] = color

    def find_and_box_region(self, threshold):
        regions = evaluate_region_flood_fill(self)
        regions_info = []
        for region in regions:
            min_max = find_min_max_region(region)
            info = {"min_point": min_max[0], "max_point": min_max[1],
                    "distance": min_max[2], "area": min_max[3]}
            regions_info.append(info)

        # largest_region = regions[0]
        # largest_region_info = regions_info[0]
        # for i in range(1, len(regions)):
        #     region = regions[i]
        #     region_info = regions_info[i]
        #     if region_info["area"] > largest_region_info["area"]:
        #         largest_region = region
        #         largest_region_info = region_info

        # self.fill_image(regions, regions_info, threshold, color)

        for i in range(len(regions)):
            largest_region = regions[i]
            largest_region_info = regions_info[i]

            subregions = find_subregions_inside_region(self, largest_region, largest_region_info)
            subregions_info = []
            for subregion in subregions:
                min_max = find_min_max_region(subregion)
                info = {"min_point": min_max[0], "max_point": min_max[1],
                        "distance": min_max[2], "area": min_max[3]}
                subregions_info.append(info)
            subregions, subregions_info = select_valid_subregion(largest_region_info, subregions, subregions_info)

            threshold = threshold * largest_region_info["area"]
            self.box_image(subregions_info, threshold)

            # self.fill_image([largest_region], [largest_region_info], threshold, color)

    def find_and_fill_region(self, threshold, color):
        regions = evaluate_region_flood_fill(self)
        regions_info = []
        for region in regions:
            min_max = find_min_max_region(region)
            info = {"min_point": min_max[0], "max_point": min_max[1],
                    "distance": min_max[2], "area": min_max[3]}
            regions_info.append(info)

        # largest_region = regions[0]
        # largest_region_info = regions_info[0]
        # for i in range(1, len(regions)):
        #     region = regions[i]
        #     region_info = regions_info[i]
        #     if region_info["area"] > largest_region_info["area"]:
        #         largest_region = region
        #         largest_region_info = region_info

        # self.fill_image(regions, regions_info, threshold, color)

        # print len(regions)
        for i in range(len(regions)):

            is_face_by_eye = False
            is_face_by_mouth = False

            largest_region = regions[i]
            largest_region_info = regions_info[i]

            subregions = find_subregions_inside_region(self, largest_region, largest_region_info)
            subregions_info = []
            for subregion in subregions:
                min_max = find_min_max_region(subregion)
                info = {"min_point": min_max[0], "max_point": min_max[1],
                        "distance": min_max[2], "area": min_max[3]}
                subregions_info.append(info)

            threshold = threshold * largest_region_info["area"]

            new_subregions_eye, new_subregions_info_eye = select_valid_subregion_eye(largest_region_info, subregions,
                                                                             subregions_info)
            if len(new_subregions_eye) != 0 and len(new_subregions_info_eye) != 0:
                # print "EYE FOUND"
                self.fill_image(new_subregions_eye, new_subregions_info_eye, threshold, (255, 0, 0))
                is_face_by_eye = True

            new_subregions_mouth, new_subregions_info_mouth = select_valid_subregion_mouth(largest_region_info, subregions,
                                                                               subregions_info)
            if len(new_subregions_mouth) != 0 and len(new_subregions_info_mouth) != 0:
                # print "MOUTH FOUND"
                self.fill_image(new_subregions_mouth, new_subregions_info_mouth, threshold, (0, 255, 0))
                is_face_by_mouth = True

            if is_face_by_eye and is_face_by_mouth:
                # print len(new_subregions_eye)
                # print new_subregions_eye
                new_subregion_info_nose = select_valid_subregion_nose(new_subregions_eye[0], new_subregions_info_eye[0],
                                                                      new_subregions_mouth[0], new_subregions_info_mouth[0])
                # print new_subregion_info_nose
                self.box_image([new_subregion_info_nose], threshold)
                # self.box_image([largest_region_info], threshold)

                # start here dagu
                distance_nose_mouth = new_subregions_info_mouth[0]["min_point"][1] - new_subregion_info_nose["max_point"][1]
                distance_mouth_chin = 2 * distance_nose_mouth
                y_updated = new_subregions_info_mouth[0]["max_point"][1] + distance_mouth_chin

                # start here alis
                height_eye = new_subregions_info_eye[0]["max_point"][1] - new_subregions_info_eye[0]["min_point"][1]
                y_min_alis = new_subregions_info_eye[0]["min_point"][1] - height_eye
                y_max_alis = y_min_alis + 0.75 * height_eye
                x_min_alis = new_subregions_info_eye[0]["min_point"][0]
                x_max_alis = new_subregions_info_eye[0]["max_point"][0]

                new_subregion_info_alis = {}
                new_subregion_info_alis["min_point"] = (x_min_alis, y_min_alis)
                new_subregion_info_alis["max_point"] = (x_max_alis, y_max_alis)
                new_subregion_info_alis["area"] = 100
                self.box_image([new_subregion_info_alis], threshold)

                height_eye = new_subregions_info_eye[1]["max_point"][1] - new_subregions_info_eye[1]["min_point"][1]
                y_min_alis = new_subregions_info_eye[1]["min_point"][1] - height_eye
                y_max_alis = y_min_alis + 0.75 * height_eye
                x_min_alis = new_subregions_info_eye[1]["min_point"][0]
                x_max_alis = new_subregions_info_eye[1]["max_point"][0]

                new_subregion_info_alis = {}
                new_subregion_info_alis["min_point"] = (x_min_alis, y_min_alis)
                new_subregion_info_alis["max_point"] = (x_max_alis, y_max_alis)
                new_subregion_info_alis["area"] = 100
                self.box_image([new_subregion_info_alis], threshold)



                largest_region_info["max_point"] = (largest_region_info["max_point"][0], y_updated)

                self.box_image([largest_region_info], threshold)

                # self.fill_image([largest_region], [largest_region_info], threshold, color)

    def process_image(self, threshold):
        self.mask_image()
        # self.find_and_box_region(threshold)
        # regions = evaluate_region_flood_fill(self)
        # print len(regions)
        # for region in regions:
        #     for each in region:
        #         temp = self.original_image.load()
        #         temp[each] = (255, 0, 0)
        # self.find_and_fill_region(threshold, self.inner_color)
        self.find_and_fill_region(threshold, (0, 255, 0))
        # self.find_and_box_region(threshold)


if __name__ == "__main__":
    image = ImageObject("test_image/image_face_bob.jpg")
    image.process_image(0.000)
    image.original_image.show("Output Image")
    # image.image_output.save("test_image/out.jpg")


def face_detect(image):
    image_input = ImageObject(image)
    image_input.process_image(0.000)

    unique_filename = str(uuid.uuid4()) + '.' + image.format
    path = 'static/dump/' + unique_filename
    image_input.original_image.save(path)
    return path
