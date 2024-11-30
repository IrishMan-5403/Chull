class Face:
    def __init__(self, a, b, c):
        self.vertices = [a, b, c]
        self.visible = False
    
    def get_vertices(self):
        return self.vertices

    def reverse(self):
        self.vertices = [self.vertices[1], self.vertices[0], self.vertices[2]]