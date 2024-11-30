from Window import viewer
from CHull import ConvexHull
from Point import Point
import numpy as np

if __name__ == "__main__":
    # Generate some random points
    points = [Point(np.random.rand(), np.random.rand(), np.random.rand()) for _ in range(500)]
    
    # points = [Point(0,0,0),Point(-1,1,-1),Point(1,-1,-1),Point(-1,-1,1),Point(1,1,1),Point(2,2,2)]

    hull = ConvexHull()
    hull.construct_hull(points)
    chull_faces=hull.get_faces()
    chull_edges=hull.get_edges()
    viewer(chull_faces, points,chull_edges)
    
#  To create virtual enironment - python -m venv env
#  To activte venv - .\env\Scripts\activate 
#  To install the dependencies - pip install -r requirements.txt 
#  To run the code - python main.py
#  To deactivate venv- deactivate