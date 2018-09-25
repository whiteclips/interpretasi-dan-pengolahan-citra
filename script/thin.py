import numpy as np
from PIL import Image


def zhangSuen(imageArr):
    # Convert to 0 and 1 array (1 black, 0 white)
    BLACK = 0
    arr = (imageArr == BLACK).astype(int)

    def getNeighboursValue(i, j):
        return [
            arr[i-1, j], arr[i-1, j+1], arr[i, j+1], arr[i+1, j+1],
            arr[i+1, j], arr[i+1, j-1], arr[i, j-1], arr[i-1, j-1]
        ]

    def transitions(list):
        l = list + list[0:1]
        return sum((n1, n2) == (0, 1) for n1, n2 in zip(l, l[1:]))

    marked_1, marked_2 = 1, 1
    while marked_1 or marked_2:
        row, col = arr.shape

        # Step 1
        marked_1 = []
        for i in range(1, row - 1):
            for j in range(1, col - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = getNeighboursValue(i, j)
                if (
                    arr[i, j] == 1 and  # condition 0
                    2 <= sum(n) <= 6 and  # condition 1
                    transitions(n) == 1 and  # condition 2
                    P2 * P4 * P6 == 0 and  # condition 3
                    P4 * P6 * P8 == 0  # condition 3
                ):
                    marked_1.append((i, j))
        # Apply marked pixel if exists
        for (r, c) in marked_1:
            arr[r, c] = 0

        # Step 2
        marked_2 = []
        for i in range(1, row - 1):
            for j in range(1, col - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = getNeighboursValue(i, j)
                if (
                    arr[i, j] == 1 and  # condition 0
                    2 <= sum(n) <= 6 and  # condition 1
                    transitions(n) == 1 and  # condition 2
                    P2 * P4 * P8 == 0 and  # condition 3
                    P2 * P6 * P8 == 0  # condition 3
                ):
                    marked_2.append((i, j))
        # Apply marked pixel if exists
        for (r, c) in marked_2:
            arr[r, c] = 0

    # Convert back to original black and white
    res = ((arr == 0).astype(int) * 255)
    return res


def getSegmentedImageArray(imgPath):
    res = np.array(Image.open(imgPath).convert('L'))
    res = ((res == 255) * 255).astype(int)
    return res


def showImage(arrImage):
    Image.fromarray(np.uint8(arrImage)).show()

def skeletonizedImage(arrImage):
  newImg = zhangSuen(arrImage)
  return ((arrImage == newImg) * 255).astype(int)

if __name__ == "__main__":
    arr = getSegmentedImageArray("./res/arial.png")
    skeletonized = skeletonizedImage(arr)
    # showImage(arr)
    # showImage(newImg)
    showImage(skeletonized)
