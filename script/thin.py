import numpy as np
from PIL import Image
import sys

def zhangSuen(imageArr):
    np.set_printoptions(threshold=np.nan)

    # Convert to 0 and 1 array (1 black, 0 white)
    BLACK = 0
    arr = (imageArr == BLACK).astype(int)

    def getNeighboursValue(i, j):
        return [
            arr[i-1, j], arr[i-1, j+1], arr[i, j+1], arr[i+1, j+1],
            arr[i+1, j], arr[i+1, j-1], arr[i, j-1], arr[i-1, j-1]
        ]
    
    def getNeighboursCoordinat(i, j):
        return [
            (i-1, j), (i-1, j+1), (i, j+1), (i+1, j+1),
            (i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1)
        ]

    def transitions(list):
        l = list + list[0:1]
        return sum((n1, n2) == (0, 1) for n1, n2 in zip(l, l[1:]))

    def isShouldBeDeleted(i, j):
        neighbors = getNeighboursValue(i, j)
        if sum(neighbors) < 3:
            return True
        isStick = False
        countStraightNeighbours = 0
        n = 0
        while (not isStick) and (n < 8):
            if ((n % 2 == 0) and neighbors[n]):
                countStraightNeighbours += 1
            if (n < 7):
                if (neighbors[n] and neighbors[n+1]):
                    isStick = True
            else:
                if (neighbors[n] and neighbors[0]):
                    isStick = True
            n += 1

        if (countStraightNeighbours > 2):
            return True
        return isStick

    def isNeighborInArray(i, j, arr):
        neighborsCoordinat = getNeighboursCoordinat(i, j)
        isInArray = False
        n = 0
        while (not isInArray) and (n < 8):
            if (neighborsCoordinat[n] in arr):
                isInArray = True
            n = n + 1

        return isInArray

    def get_init_branch(i, j):
        neighbor_val_arr = getNeighboursValue(i, j)
        neighbor_coordinate_arr = getNeighboursCoordinat(i, j)
        result = []
        for n in range(len(neighbor_val_arr)):
            if (neighbor_val_arr[n] == 1):
                result.append(neighbor_coordinate_arr[n])
        return result

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

    # remove dual-pixeled line
    row, col = arr.shape
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            P2, P3, P4, P5, P6, P7, P8, P9 = n = getNeighboursValue(i, j)
            if (arr[i, j] == 1):
                if ((P2 and P3) or (P2 and P9)) and (sum(n) > 2):
                    # remove P2
                    if (isShouldBeDeleted(i-1, j)):
                        arr[i-1, j] = 0
                if ((P4 and P3) or (P4 and P5)) and (sum(n) > 2):
                    # remove P4
                    if (isShouldBeDeleted(i, j+1)):
                        arr[i, j+1] = 0
                if ((P6 and P5) or (P6 and P7)) and (sum(n) > 2):
                    # remove P6
                    if (isShouldBeDeleted(i+1, j)):
                        arr[i+1, j] = 0
                if ((P8 and P7) or (P8 and P9)) and (sum(n) > 2):
                    # remove P8
                    if (isShouldBeDeleted(i, j-1)):
                        arr[i, j-1] = 0

    # noise clearance
    visited = []
    cross_candidate = []
    min_len = 9
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            if (arr[i, j] == 1) and (i, j) not in visited:
                # cek apakah persimpangan
                neighbors = getNeighboursValue(i, j)
                if (
                    (arr[i, j] == 1) and
                    (sum(neighbors) > 2) and
                    (not isNeighborInArray(i, j, cross_candidate))
                ):
                    current_cross = (i, j)
                    print('', file=sys.stdout)
                    print(current_cross, file=sys.stdout)
                    cross_candidate.append(current_cross)
                    # # cari awal percabangan
                    init_branch = get_init_branch(i, j)
                    print(init_branch, file=sys.stdout)
                    for b in init_branch:
                        # telusuri semua cabang
                        print("====", file=sys.stdout)
                        current_pixel = b
                        branch_path = []
                        branch_path.append(current_pixel)
                        isNoise = False
                        stop = False
                        while not isNoise and not stop and len(branch_path) < min_len:
                            print(current_pixel, file=sys.stdout)
                            neighbors_val = getNeighboursValue(current_pixel[0], current_pixel[1])
                            neighbors_coord = getNeighboursCoordinat(current_pixel[0], current_pixel[1])
                            if (sum(neighbors_val) == 1) :
                                isNoise = True
                                print("noise", file=sys.stdout)
                            elif (sum(neighbors_val) >= 4):
                                stop = True
                                print("stop", file=sys.stdout)
                            else:
                                for n in range(8):
                                    if (
                                        neighbors_val[n] and
                                        neighbors_coord[n] not in init_branch and
                                        neighbors_coord[n] not in branch_path and
                                        neighbors_coord[n] != current_cross
                                    ):
                                        current_pixel = neighbors_coord[n]
                                branch_path.append(current_pixel)

                        if isNoise:
                            print("Noise", file=sys.stdout)
                            print(branch_path, file=sys.stdout)
                            # hapus branch_path dari arr
                            for bp in branch_path:
                                arr[bp[0], bp[1]] = 0
                        
                visited.append((i, j))

    # telusuri
    # visited = []
    # char_candidate = []
    # char_counter = 0
    # char_length_threshold = 10
    # is_inc = True

    # while is_inc:
    #     is_inc = False
    #     for i in range(1, row - 1):
    #         for j in range(1, col - 1):
    #             if (arr[i, j] == 1) and not in visited:
    #                 is_inc = True
    #                 tip_candidate = []
    #                 cross_candidate = []
    #                 current = {'i' : i, 'j' : j}
    #                 while len(next(i, j)) != 0:
    #                     # cek apakah ujung
    #                     neighbors = getNeighboursValue(i, j)
    #                     if ((arr[i, j] == 1) and (sum(neighbors) == 1)):
    #                         tip_candidate.append((i, j))

    #                     # cek apakah persimpangan
    #                     if (
    #                         (arr[i, j] == 1) and
    #                         (sum(neighbors) > 2) and
    #                         (not isNeighborInArray(i, j, cross_candidate))
    #                     ):
    #                         cross_candidate.append((i, j))
                        
    #                     # tandai visited
    #                     visited.append((i, j))

    #                     # cari next-nya

    #                 char_candidate.append({'tip' : tip_candidate, 'cross' : cross_candidate})

    # search tip (ujung)
    tip_candidate = []
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            neighbors = getNeighboursValue(i, j)
            if ((arr[i, j] == 1) and (sum(neighbors) == 1)):
                tip_candidate.append((i, j))
    
    print(tip_candidate, file=sys.stdout)

    # search cross (persimpangan)
    cross_candidate = []
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            neighbors = getNeighboursValue(i, j)
            if (
                (arr[i, j] == 1) and
                (sum(neighbors) > 2) and
                (not isNeighborInArray(i, j, cross_candidate))
            ):
                cross_candidate.append((i, j))
    
    # print(cross_candidate, file=sys.stdout)

    # Convert back to original black and white
    res = ((arr == 0).astype(int) * 255)

    temp = '  '
    for j in range(1, col - 1):
        temp = temp + str(j%9) + ' '
    print(temp, file=sys.stdout)
    # print to log
    for i in range(1, row - 1):
        temp = str(i%9) + ' '
        for j in range(1, col - 1):
            if (res[i, j] == 0):
                temp = temp + 'x '
            else:
                temp = temp + '- '

        print(temp, file=sys.stdout)

    return (res, tip_candidate, cross_candidate)


def getSegmentedImageArray(imgPath):
    res = np.array(Image.open(imgPath).convert('L'))
    res = ((res == 255) * 255).astype(int)
    return res


def showImage(arrImage):
    Image.fromarray(np.uint8(arrImage)).show()

def skeletonizedImage(arrImage):
  (newImg, tips, cross) = zhangSuen(arrImage)
  res = ((arrImage == newImg) * 255).astype(int)
  return (res, tips, cross)

def predict(tips, cross):
    if (len(tips) == 0):
        if (len(cross) == 0):
            return 0
        else :
            return 8
    elif (tips[0] == (29, 6) and tips[1] == (59, 25)):
        return 1
    elif (tips[0] == (26, 10) and tips[1] == (67, 40)):
        return 2
    elif (tips[0] == (21, 9) and tips[1] == (38, 22) and tips[2] == (58, 11)):
        return 3
    elif (tips[0] == (10, 33) and tips[1] == (49, 40) and tips[2] == (60, 32)):
        return 4
    elif (tips[0] == (11, 36) and tips[1] == (56, 12)):
        return 5
    elif (tips[0] == (13, 36)):
        return 6
    elif (tips[0] == (11, 10) and tips[1] == (61, 16)):
        return 7
    elif (tips[0] == (55, 13)):
        return 9



if __name__ == "__main__":
    arr = getSegmentedImageArray("./res/arial.png")
    skeletonized = skeletonizedImage(arr)
    # showImage(arr)
    # showImage(newImg)
    showImage(skeletonized)
