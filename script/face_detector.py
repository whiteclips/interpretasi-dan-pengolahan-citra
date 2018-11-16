from PIL import Image
import math


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
            if is_skin_pixel(i, j, image.rgb_matrix, image.hsv_matrix) or is_skin_pixel(i, j, image.rgb_matrix, image.ycbcr_matrix):
                if inner_color is not None:
                    image.rgb_matrix[j, i] = inner_color
            else:
                image.rgb_matrix[j, i] = outer_color
    return image.image


class ImageObject:
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.rgb_matrix = self.image.load()
        self.hsv_matrix = get_hsv_matrix_from_rgb_matrix(self.width, self.height, self.rgb_matrix)
        self.ycbcr_matrix = get_ycbcr_matrix_from_rgb_matrix(self.width, self.height, self.rgb_matrix)
        self.image_output = None

    def process_image(self):
        self.image_output = mask_image_to_get_face(self, (255, 255, 255))


if __name__ == "__main__":
    image = ImageObject("test_image/image_face_2.jpg")
    image.image.show("Original Image")
    image.process_image()
    image.image_output.show("Output Image")
    image.image_output.save("test_image/out.jpg")
