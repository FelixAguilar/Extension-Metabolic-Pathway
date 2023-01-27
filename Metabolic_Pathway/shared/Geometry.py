from typing import Any, Tuple
from shared.Element import font_size
from math import atan, atan2, sin, cos, pi, sqrt, pow, tan, radians, degrees, acos

# Gets the distance from the center of the circle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_circle_size(size: float, angle: float) -> Tuple[float, float]:

    if (angle < 0):
        angle = angle + 180
    if (angle > 90):
        angle = 180 - angle
    angle = radians(angle)
    return (size * cos(angle), size * sin(angle))
    
# Gets the distance from the center of the ellipse to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_elipse_size(size_x: float, size_y: float, angle: float) -> Tuple[float, float]:

    if (angle < 0):
        angle = angle + 180
    if (angle > 90):
        angle = 180 - angle

    angle_rad = radians(angle)
    radius = 1 / sqrt(pow(cos(angle_rad)/size_x, 2) + pow(sin(angle_rad)/size_y, 2))
    return get_circle_size(radius, angle)

# Gets the distance from the center of the rectangle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_rectangle_size(size_x: float, size_y: float, angle: float) -> Tuple[float, float]:

    center_base = size_x / 2
    center_hight = size_y / 2

    if (angle < 0):
        angle = angle + 180
    if (angle > 90):
        angle = 180 - angle

    vertex_angle = degrees(atan(center_hight / center_base))

    if(angle < vertex_angle):
        return (center_base, tan(radians(angle)) * center_base)
    if(angle > vertex_angle):
        return (tan(radians(90 - angle)) * center_hight, center_hight)

# Gets the distance from the center of the compound rectangle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates. 
def get_component_size(size: float, angle: float) -> Tuple[float, float]:
    return get_rectangle_size(size, (font_size + 2), angle)

# Gets the distance from the center of the octogon to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_octogon_size(distances, radius, angle: float) -> Tuple[float, float]:

    if (angle < 0):
        angle = angle + 180
    if (angle > 90):
        angle = 180 - angle

    # extracts the distances.
    h1 = distances[0] # horizontal
    h2 = distances[1] # vertical
    r1 = radius[0]    # first diagonal from base
    r2 = radius[1]    # second diagonal
    
    # extracts angles in radians for the divisions inside the segment of octogon
    vertex1 = acos(h1/r1)   # first angle from base
    vertex3 = acos(h2/r2)   # third angle from base
    vertex2 = pi/2 - (vertex3 + vertex1) # second angle from base
    angle = radians(angle)

    if(angle < vertex1):
        return (h1, sin(angle) * r1)
    if(angle < vertex1 + vertex2):
        p1 = (cos(vertex1) * r1, sin(vertex1) * r1)
        p2 = (cos(vertex1 + vertex2) * r2, sin(vertex1 + vertex2) * r2)

        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        t = tan(angle)
        
        x = (p1[1] - (m * p1[0])) / (t - m)
        y = t * x
        return (x,y)
    else:
        return (sin(pi/2 - angle) * r2, h2)

# Same as the above one but this time is for a regular octogon.
def get_regular_octogon_size(size: float, angle: float) -> Tuple[float, float]:
    hight = size * cos(radians(22.5))
    return get_octogon_size((hight, hight), (size, size), angle)

# Gets the angle between the line and x-axis.
def get_angle_line(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    return atan2(y_delta, x_delta) * 180 / pi

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
