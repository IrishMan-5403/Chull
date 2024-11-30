from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *


class ConvexHullViewer(QOpenGLWidget):
    def __init__(self, faces, points, edges):
        super().__init__()
        self.faces = faces  # List of triangular faces (from the convex hull algorithm)
        self.points = points  # Original points
        self.edges= edges 
        
        # Variables to control the view
        self.x_rot = 0
        self.y_rot = 0
        self.zoom = -5.0
        
        # Mouse tracking
        self.last_mouse_pos = None
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, self.zoom)

        # centroid = self.calculate_centroid()

        # glTranslatef(-centroid[0], -centroid[1], -centroid[2])

        glRotatef(self.x_rot, 1, 0, 0)
        glRotatef(self.y_rot, 0, 1, 0)

        # glTranslatef(centroid[0], centroid[1], centroid[2])

        self.draw_convex_hull()
    
    

    def draw_convex_hull(self):
        # Draw the points
        glColor3f(1.0, 1.0, 0.0)  # Yellow points
        glPointSize(5)
        glBegin(GL_POINTS)
        for point in self.points:
            glVertex3f(point.x, point.y, point.z)
        glEnd()



        # Draw the triangular faces of the convex hull
        glColor4f(0.0, 0.5, 1.0,0.5)  # Blue faces
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            vertices=face.get_vertices()
            glVertex3f(vertices[0].x, vertices[0].y, vertices[0].z)
            glVertex3f(vertices[1].x, vertices[1].y, vertices[1].z)
            glVertex3f(vertices[2].x, vertices[2].y, vertices[2].z)
        glEnd()

        glColor3f(1.0, 1.0, 1.0)  # White edges
        glLineWidth(1)
        glBegin(GL_LINES)
        for edge in self.edges:
            vertices = edge.get_vertices()
            glVertex3f(vertices[0].x, vertices[0].y, vertices[0].z)
            glVertex3f(vertices[1].x, vertices[1].y, vertices[1].z)

        glEnd()

    def mousePressEvent(self, event):
        """Capture mouse position on press."""
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Handle mouse movement for rotation."""
        if self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            
            # Update rotation based on mouse movement
            self.x_rot += dy
            self.y_rot += dx
            
            # Save the new mouse position for the next movement
            self.last_mouse_pos = event.pos()
            
            # Trigger a redraw
            self.update()

    def wheelEvent(self, event):
        """Handle zoom with mouse wheel."""
        delta = event.angleDelta().y() / 120  # A single wheel step is 120
        self.zoom += delta * 0.2  # Adjust zoom speed
        
        # Trigger a redraw
        self.update()

