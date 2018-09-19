from PIL import Image
import numpy as np
from queue import Queue

MAGIC = 77


class Direction:
    def __init__(self):
        self.N = self.W = self.E = self.S = 0
        self.NW = self.NE = self.SE = self.SW = 0

    def __str__(self):
        s = "N({}) E({}) S({}) W({})".format(self.N, self.E, self.S, self.W)
        s += "\nNE({}) SE({}) SW({}) NW({})".format(self.NE,
                                                    self.SE, self.SW, self.NW)
        return s

    def addPoint(self, r1, c1, r2, c2):
        if (r1-r2 < 0):
            if (c1-c2 < 0):
                self.add("NW")
            elif (c1-c2 == 0):
                self.add("N")
            else:
                self.add("NE")
        elif (r1-r2 == 0):
            if (c1-c2 < 0):
                self.add("W")
            elif (c1-c2 > 0):
                self.add("E")
        else:
            if (c1-c2 < 0):
                self.add("SW")
            elif (c1-c2 == 0):
                self.add("S")
            else:
                self.add("SE")

    def add(self, c):
            # print(c, end=" ")
        if (c == "N" or c == "n"):
            self.N += 1
        elif (c == "E" or c == "e"):
            self.E += 1
        elif (c == "S" or c == "s"):
            self.S += 1
        elif (c == "W" or c == "w"):
            self.W += 1
        elif (c == "NE" or c == "ne"):
            self.NE += 1
        elif (c == "NW" or c == "nw"):
            self.NW += 1
        elif (c == "SE" or c == "se"):
            self.SE += 1
        elif (c == "SW" or c == "sw"):
            self.SW += 1


def getSegmentedImageArray(imgPath):
    res = np.array(Image.open(imgPath).convert('L'))
    res = ((res == 255) * 255).astype(int)
    return res


def getDirectionFromArray(imgArr):
    # === Helper function ===
    def isValid(r, c):
        return (0 <= r and r < imgArr.shape[0] and 0 <= c and c < imgArr.shape[1])

    def isBorder(r, c):
        if (imgArr[r, c] == 255):
            return False
        sibling = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1),
                   (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]
        for (s_i, s_j) in sibling:
            if (isValid(s_i, s_j) and imgArr[s_i, s_j] == 255):
                return True
        return False

    def getPosition(s_i, s_j):
        found = False
        i, j = s_i, s_j
        while (j < imgArr.shape[1] and not found):
            i = 0
            while (i < imgArr.shape[0] and not found):
                if (imgArr[i, j] == 0):
                    found = True
                else:
                    i += 1
            if (not found):
                j += 1
        if (not found):
            return -1, -1
        else:
            return i, j
    # === End Helper function ===

    newArr = imgArr.copy()
    dir = Direction()
    rightmost = 0

    while(1):
        i, j = getPosition(0, rightmost)
        if (i == -1 and j == -1):
            break

        visited = {(i, j)}
        while (1):
            # Find Sibling clock wise
            next = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]
            got = False
            for (r, c) in next:
                if (isValid(r, c) and (r, c) not in visited and isBorder(r, c)):
                    if (c > rightmost):
                        rightmost = c
                    newArr[r, c] = MAGIC
                    visited.add((r, c))
                    dir.addPoint(i, j, r, c)
                    got = True
                    i, j = r, c
                    break
            if (not got):
                break
        rightmost += 1

    return dir, newArr


if __name__ == "__main__":
    arr = getSegmentedImageArray("./res/arial.png")
    dir, newArr = getDirectionFromArray(arr)
    # Before anti flooded
    Image.fromarray(np.uint8(arr)).show()

    # After anti flooded
    newArr = (newArr == MAGIC) * 255
    newArr.astype(int)
    Image.fromarray(np.uint8(newArr)).show()
