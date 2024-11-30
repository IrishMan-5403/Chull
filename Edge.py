class Edge:
    def __init__(self, p1, p2):
        self.endpoints = [p1, p2]
        self.adjface1 = None
        self.adjface2 = None
        self.remove = False

    def link_adj_face(self, face):
        if not self.adjface1:
            self.adjface1 = face
        elif not self.adjface2:
            self.adjface2 = face

    def erase(self, face):
        if self.adjface1 == face:
            self.adjface1 = None
        elif self.adjface2 == face:
            self.adjface2 = None

    def get_vertices(self):
        return self.endpoints