from Point import Point
from Edge import Edge
from Face import Face


class ConvexHull:
    def __init__(self):
        self.faces = []
        self.edges = []
        self.map_edges = {}
        self.exterior_points = []

    def key_to_edge(self, a, b):
        return hash(a) ^ hash(b)

    def volume_sign(self, face, p):
        ax, ay, az = face.vertices[0].x - p.x, face.vertices[0].y - p.y, face.vertices[0].z - p.z
        bx, by, bz = face.vertices[1].x - p.x, face.vertices[1].y - p.y, face.vertices[1].z - p.z
        cx, cy, cz = face.vertices[2].x - p.x, face.vertices[2].y - p.y, face.vertices[2].z - p.z

        vol = ax * (by * cz - bz * cy) + ay * (bz * cx - bx * cz) + az * (bx * cy - by * cx)
        return 0 if vol == 0 else (-1 if vol < 0 else 1)

    def add_one_face(self, a, b, c, inner_pt):
        new_face = Face(a, b, c)
        if self.volume_sign(new_face, inner_pt) < 0:
            new_face.reverse()
        self.faces.append(new_face)

        def create_edge(p1, p2):
            key = self.key_to_edge(p1, p2)
            if key not in self.map_edges:
                self.edges.append(Edge(p1, p2))
                self.map_edges[key] = self.edges[-1]
            self.map_edges[key].link_adj_face(new_face)

        create_edge(a, b)
        create_edge(a, c)
        create_edge(b, c)

    def colinear(self, a, b, c):
        return ((c.z - a.z) * (b.y - a.y) - (b.z - a.z) * (c.y - a.y)) == 0 and \
               ((b.z - a.z) * (c.x - a.x) - (b.x - a.x) * (c.z - a.z)) == 0 and \
               ((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)) == 0

    def build_first_hull(self, pointcloud):
        n = len(pointcloud)
        if n <= 3:
            print("Tetrahedron: points.size() < 4")
            return False

        i = 2
        while self.colinear(pointcloud[i], pointcloud[i-1], pointcloud[i-2]):
            if i == n - 1:
                print("Tetrahedron: All points are colinear!")
                return False
            i += 1

        face = Face(pointcloud[i], pointcloud[i-1], pointcloud[i-2])
        j = i
        while not self.volume_sign(face, pointcloud[j]):
            if j == n - 1:
                print("Tetrahedron: All points are coplanar!")
                return False
            j += 1

        p1, p2, p3, p4 = pointcloud[i], pointcloud[i-1], pointcloud[i-2], pointcloud[j]
        p1.processed = p2.processed = p3.processed = p4.processed = True
        self.add_one_face(p1, p2, p3, p4)
        self.add_one_face(p1, p2, p4, p3)
        self.add_one_face(p1, p3, p4, p2)
        self.add_one_face(p2, p3, p4, p1)
        return True

    def find_inner_point(self, face, edge):
        for vertex in face.vertices:
            if vertex != edge.endpoints[0] and vertex != edge.endpoints[1]:
                return vertex

    def incre_hull(self, pt):
        visible_faces = []
        for face in self.faces: # this will run in the magnitude O(n)
            if self.volume_sign(face, pt) < 0:
                face.visible = True
                visible_faces.append(face)

        if not visible_faces:
            return

        for edge in self.edges:
            face1, face2 = edge.adjface1, edge.adjface2
            if face1 is None or face2 is None:
                continue
            if face1.visible and face2.visible:
                edge.remove = True
            elif face1.visible or face2.visible:
                if face1.visible:
                    face1, face2 = face2, face1
                inner_pt = self.find_inner_point(face2, edge)
                edge.erase(face2)
                self.add_one_face(edge.endpoints[0], edge.endpoints[1], pt, inner_pt)

    def construct_hull(self, pointcloud):
        if not self.build_first_hull(pointcloud): 
            return
        for pt in pointcloud:  ## This for loop run n times
            if not pt.processed:
                self.incre_hull(pt) ## This will take O(n)
                self.clean_up() ## This will also take O(n)
        self.extract_exterior_points()

    def clean_up(self):  ## Each for loop runs in range of n
        self.edges = [edge for edge in self.edges if not edge.remove]
        self.map_edges = {self.key_to_edge(edge.endpoints[0], edge.endpoints[1]): edge for edge in self.edges}
        self.faces = [face for face in self.faces if not face.visible]

    def extract_exterior_points(self):
        exterior_set = set()
        for face in self.faces:
            for vertex in face.vertices:
                exterior_set.add(vertex)
        self.exterior_points = list(exterior_set)
    
    def get_faces(self):
        return self.faces
    def get_edges(self):
        return self.edges
