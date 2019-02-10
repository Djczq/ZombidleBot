class Point:
    # coord : (width = left-->rigth (x), heigh = top-->bottom (y))
    # box : (top-left width, top-left heigh, bottom-rigth width, bottom-rigth heigh)
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @classmethod
    def fromArray(cls, arr):
        return cls(arr[0], arr[1])

    def add(self, width, height):
        return Point(self.width + width, self.height + height)

    def asArray(self):
        return [self.width, self.height]

    def asArrayReverse(self):
        return [self.height, self.width]

    def __str__(self):
        return "<width: " + str(self.width) + ", height: " + str(self.height) + ">"
