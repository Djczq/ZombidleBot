from Point import Point

class Rectangle:
    def __init__(self, topleft, botrigth):
        self.topleft = topleft
        self.botrigth = botrigth

    @classmethod
    def fromArray(cls, arr):
        return Rectangle(Point(arr[0], arr[1]), Point(arr[2], arr[3]))

    @classmethod
    def fromValues(cls, width1, height1, width2, height2):
        wmin = min(width1, width2)
        wmax = max(width1, width2)
        hmin = min(height1, height2)
        hmax = max(height1, height2)
        return Rectangle(Point(wmin, hmin), Point(wmax, hmax))

    def offset(self, off):
        return Rectangle(self.topleft.add(off), self.botrigth.add(off))

    def contains(self, other):
        """check if other is inside self"""
        if other.topleft.width < self.topleft.width or other.topleft.width > self.botrigth.width:
            return False
        if other.botrigth.width < self.topleft.width or other.botrigth.width > self.botrigth.width:
            return False
        if other.topleft.height < self.topleft.height or other.topleft.height > self.botrigth.height:
            return False
        if other.botrigth.height < self.topleft.height or other.botrigth.height > self.botrigth.height:
            return False
        return True

    def getCenterPoint(self):
        return Point((self.topleft.width + self.botrigth.width) / 2, (self.topleft.height + self.botrigth.height) / 2)

    def getSliceNP(self):
        return (slice(self.topleft.height, self.botrigth.height), slice(self.topleft.width, self.botrigth.width))

    def __str__(self):
        return "(" + str(self.topleft) + "," + str(self.botrigth) + ")"
