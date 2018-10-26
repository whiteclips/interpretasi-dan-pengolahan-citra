import numpy as np
from PIL import Image
import sys

def zhangSuen(imageArr, noise_threshold_percent):
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
        straight_neighbors = []
        n = 0
        while (n < 8):
            if ((n % 2 == 0) and neighbors[n]):
                straight_neighbors.append(n)
            if (n < 7):
                if (neighbors[n] and neighbors[n+1]):
                    isStick = True
            else:
                if (neighbors[n] and neighbors[0]):
                    isStick = True
            n += 1

        if (len(straight_neighbors) > 2):
            return True
        elif (len(straight_neighbors) == 2):
            if (0 in straight_neighbors and 2 in straight_neighbors and neighbors[5]):
                return False
            elif (2 in straight_neighbors and 4 in straight_neighbors and neighbors[7]):
                return False
            elif (4 in straight_neighbors and 6 in straight_neighbors and neighbors[1]):
                return False
            elif (6 in straight_neighbors and 0 in straight_neighbors and neighbors[3]):
                return False
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
    # noise_threshold_percent = 0.07
    visited = []
    cross_candidate = []
    max_len_branch_global = 0
    total_len_path = 0
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
                    # print('', file=sys.stdout)
                    # print(current_cross, file=sys.stdout)
                    cross_candidate.append(current_cross)
                    # cari awal percabangan
                    init_branch = get_init_branch(i, j)
                    # print(init_branch, file=sys.stdout)
                    branches = []
                    max_len_branch = 0
                    
                    for b in init_branch:
                        # telusuri semua cabang
                        # print("====", file=sys.stdout)
                        current_pixel = b
                        branch_path = []
                        branch_path.append(current_pixel)
                        stop = False
                        while not stop:
                            # print(current_pixel, file=sys.stdout)
                            neighbors_val = getNeighboursValue(current_pixel[0], current_pixel[1])
                            neighbors_coord = getNeighboursCoordinat(current_pixel[0], current_pixel[1])
                            if (sum(neighbors_val) == 1) :
                                stop = True
                                # print("stop1", file=sys.stdout)
                            elif (sum(neighbors_val) >= 4):
                                stop = True
                                # print("stop2", file=sys.stdout)
                            else:
                                n = 0
                                isNextExist = False
                                while not isNextExist and n < 8:
                                    if (
                                        neighbors_val[n] and
                                        neighbors_coord[n] not in init_branch and
                                        neighbors_coord[n] not in branch_path and
                                        neighbors_coord[n] != current_cross
                                    ):
                                        current_pixel = neighbors_coord[n]
                                        isNextExist = True
                                    else:
                                        n += 1

                                if (isNextExist):
                                    branch_path.append(current_pixel)
                                else:
                                    stop = True
                        
                        branches.append(branch_path)

                        if (max_len_branch < len(branch_path)):
                            max_len_branch = len(branch_path)

                        if (max_len_branch_global < len(branch_path)):
                            max_len_branch_global = len(branch_path)

                        total_len_path += len(branch_path)

                    noise_threshold = int(round(noise_threshold_percent * max_len_branch))
                    # print("threshold: " + str(noise_threshold), file=sys.stdout)
                    for branch in branches:
                        if (len(branch) < noise_threshold):
                            # print("Noise", file=sys.stdout)
                            # print(branch, file=sys.stdout)
                            # hapus branch dari arr
                            for b in branch:
                                arr[b[0], b[1]] = 0
                        
                visited.append((i, j))

    # search tip (ujung)
    tip_candidate = []
    for i in range(1, row - 1):
        for j in range(1, col - 1):
            neighbors = getNeighboursValue(i, j)
            if ((arr[i, j] == 1) and (sum(neighbors) == 1)):
                tip_candidate.append((i, j))
    
    # print("tip", file=sys.stdout)
    # print(tip_candidate, file=sys.stdout)

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
    
    # print("cross", file=sys.stdout)
    # print(cross_candidate, file=sys.stdout)

    # Convert back to original black and white
    res = ((arr == 0).astype(int) * 255)
    # print("total : " + str(total_len_path), file=sys.stdout)

    return (res, tip_candidate, cross_candidate)


def predict(tips, cross):
    t = len(tips)
    c = len(cross)
    print("Tips: ",tips)
    print("Cross: ",cross)
    print("Tips({}), Cross({})".format(t,c))
    if (c == 1):
        if (t == 1):  return "a, b, d, e, g, p, q"
        elif (t == 2): return "l, n, r"
        elif (t == 3): return "f, h, m, w, y"
        elif (t == 4): return "k, x, z"
        else: return "UKNOWN"
    elif (t == 0):
        if (t == 0): return "o"
        elif (t == 2): return "c, s, u, v"
        elif (t == 3): return "i, j, t"
        else: return "UKNOWN"
    else: return "UKNOWN"


def getSegmentedImageArray(imgPath, treshold ):
    res = np.array(Image.open(imgPath).convert('L'))
    res = ((res >= int(treshold)) * 255).astype(int)
    return res


def showImage(arrImage):
    Image.fromarray(np.uint8(arrImage)).show()

def skeletonizedImage(arrImage, noise_threshold_percent):
  (newImg, tips, cross) = zhangSuen(arrImage, noise_threshold_percent)
  res = ((arrImage == newImg) * 255).astype(int)
  return (res, tips, cross)


if __name__ == "__main__":
    arr = getSegmentedImageArray("./res/hand_written/a.png")
    skeletonized, tips, cross = skeletonizedImage(arr, 0.08)
    print("Tips : {} .  Cross : {}".format(tips,cross))
    # showImage(arr)
    # showImage(newImg)
    showImage(skeletonized)
