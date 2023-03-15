from typing import Any, Tuple
from shared.Element import font_size
from math import atan2, sin, cos, pi, sqrt, pow, tan, acos

# Gets the distance from the center of the ellipse to the edge of it, this is indicated by the angle.
def get_elipse_size(size_x: float, size_y: float, angle: float) -> float:
    return 1 / sqrt(pow(cos(angle)/size_x, 2) + pow(sin(angle)/size_y, 2))

# Gets the distance from the center of the rectangle to the edge of it, this is indicated by the angle.
def get_rectangle_size(size_x: float, size_y: float, angle: float) -> float:

    center_base = size_x / 2
    center_hight = size_y / 2

    vertex_angle = atan2(center_hight, center_base)

    if(angle <= vertex_angle):
        return center_base / cos(angle)
    if(angle > vertex_angle):
        return center_hight / cos(1.5708 - angle)
    
# Gets the distance from the center of the compound rectangle to the edge of it, this is indicated by the angle. 
def get_component_size(size: float, angle: float) -> float:
    return get_rectangle_size(size, (font_size + 2), angle)

# Gets the distance from the center of the octogon to the edge of it, this is indicated by the angle.
def get_octogon_size(distances, radius, angle: float) -> float:

    # extracts the distances.
    h1 = distances[0] # horizontal
    h2 = distances[1] # vertical
    r1 = radius[0]    # first diagonal from base
    r2 = radius[1]    # second diagonal
    
    # extracts angles in radians for the divisions inside the segment of octogon
    vertex1 = acos(h1/r1)   # first angle from base
    vertex3 = acos(h2/r2)   # third angle from base
    vertex2 = 1.5708 - (vertex3 + vertex1) # second angle from base

    if(angle <= vertex1):
        return h1 / cos(angle)
    
    if(angle < vertex1 + vertex2):
        p1 = (cos(vertex1) * r1, sin(vertex1) * r1)
        p2 = (cos(vertex1 + vertex2) * r2, sin(vertex1 + vertex2) * r2)

        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        t = tan(angle)
        
        x = (p1[1] - (m * p1[0])) / (t - m)
        y = t * x
        return sqrt(pow(x, 2) + pow(y, 2))
    
    return h2 / cos(1.5708 - angle)

# Same as the above one but this time is for a regular octogon.
def get_regular_octogon_size(size: float, angle: float) -> float:
    hight = size * 0.9239
    return get_octogon_size((hight, hight), (size, size), angle)

# Separates the size in x and y vectors.
def get_separate_size(size: float, angle: float) -> Tuple[float, float]:
    return (size * cos(angle), size * sin(angle))

# Gets the angle between the line and x-axis.
def get_angle_line(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    angle = atan2(y_delta, x_delta)
    return angle

# Returns the first quadrant angle equivalent with the angle passed.
def get_equivalent_angle(angle: float) -> float:
    if (angle < 0):
        angle = angle + pi
    if (angle > 1.5708):
        angle = pi - angle
    return angle

# Gets the distance between two points.
def get_distance(point_1: Tuple[float, float], point_2: Tuple[float, float]) -> float:
    return sqrt(pow(point_1[0] - point_2[0], 2) + pow(point_1[1] - point_2[1], 2))

# From the element inside the graph, obtains the coordinates for the transformation inside the canvas.
def get_transformation(element: Any) -> Tuple[float, float]:
    t = str(element.get('transform'))

    if(t == "None"):
        return (0, 0)
    else:
        start = t.find('(')
        middle = t.find(',')
        end = t.find(')')

        if(middle == -1):
            x = float(t[start + 1:end])
            y = float(0)
        else:
            x = float(t[start + 1:middle])
            y = float(t[middle + 2:end])
        return (x, y)
