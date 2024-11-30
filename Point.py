class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.processed = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"