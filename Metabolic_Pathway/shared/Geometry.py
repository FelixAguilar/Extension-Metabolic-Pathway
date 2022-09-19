from typing import Any, Tuple
from shared.Element import font_size
from math import atan, atan2, sin, cos, pi, sqrt, pow

# Gets the distance from the center of the ellipse to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_elipse_size(size_x: float, size_y: float, angle: float) -> Tuple[float, float]:
    angle = angle * (pi / 180)
    radius = (size_x * size_y) / (sqrt((pow(size_x, 2) * pow(sin(angle), 2)) + (pow(size_y, 2) * pow(cos(angle), 2))))
    return (abs(radius * cos(angle)), abs(radius * sin(angle)))

# Gets the distance from the center of the circle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_circle_size(size: float, angle: float) -> Tuple[float, float]:
    return (abs(size * cos(angle * (pi / 180))), abs(size * sin(angle * (pi / 180))))

# Gets the distance from the center of the rectangle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_rectangle_size(size_x: float, size_y: float, angle: float) -> Tuple[float, float]:

    center_base = size_x / 2
    center_hight = size_y / 2

    vertex_angle = atan(center_hight / center_base) * 180 / pi

    if((angle > vertex_angle and angle < 180 - vertex_angle) or (angle < -vertex_angle and angle > vertex_angle - 180)):
        return (abs(center_base * cos(angle * (pi / 180))), center_hight)
    else:
        return (center_base, abs(center_hight * sin(angle * (pi / 180))))

# Gets the distance from the center of the compound rectangle to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates. 
def get_component_size(size: float, angle: float) -> Tuple[float, float]:

    center_base = size / 2
    center_hight = (font_size + 2) / 2 

    vertex_angle = atan(center_hight / center_base) * 180 / pi

    if((angle > vertex_angle and angle < 180 - vertex_angle) or (angle < -vertex_angle and angle > vertex_angle - 180)):
        return (abs(center_base * cos(angle * (pi / 180))), center_hight)
    else:
        return (center_base, abs(center_hight * sin(angle * (pi / 180))))

# Gets the distance from the center of the octogon to the edge of it, this is indicated by the angle, the result is separated in x and y coordinates.
def get_octogon_size(size_x: float, size_y: float, angle: float) -> Tuple[float, float]:

    angle = abs(angle)

    if (angle < 22.5 or angle > 157.5):
        return (size_x, abs(size_y * sin(angle * (pi / 180))))
    elif (angle > 67.5 and angle < 112.5):
        return (abs(size_x * cos(angle * (pi / 180))), size_y)
    else:
        return (abs(size_x * cos(angle * (pi / 180))), abs(size_y * sin(angle * (pi / 180))))

# Same as the above one but this time is for a regular octogon.
def get_regular_octogon_size(size: float, angle: float)  -> Tuple[float, float]:
    
    size += 4
    angle = abs(angle)
    hight = size * cos(22.5 * (pi / 180))

    if (angle < 22.5 or angle > 157.5):
        return (hight, abs(hight * sin(angle * (pi / 180))))
    elif (angle > 67.5 and angle < 112.5):
        return (abs(hight * cos(angle * (pi / 180))), hight)
    else:
        return (abs(hight * cos(angle * (pi / 180))), abs(hight * sin(angle * (pi / 180))))

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
