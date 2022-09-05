from math import atan, atan2, sin, cos, pi, sqrt, pow

def get_elipse_size(size_x, size_y, angle):
    angle = angle * (pi / 180)
    radius = (size_x * size_y) / (sqrt((pow(size_x, 2) * pow(sin(angle), 2)) + (pow(size_y, 2) * pow(cos(angle), 2))))
    return (abs(radius * cos(angle)), abs(radius * sin(angle)))

def get_rectangle_size(size_x, size_y, angle):

    center_base = size_x / 2
    center_hight = size_y / 2

    vertex_angle = atan(center_hight / center_base) * 180 / pi

    if((angle > vertex_angle and angle < 180 - vertex_angle) or (angle < -vertex_angle and angle > vertex_angle - 180)):
        return (abs(center_base * cos(angle * (pi / 180))), center_hight)
    else:
        return (center_base, abs(center_hight * sin(angle * (pi / 180))))

def get_octogon_size(size_x, size_y, angle):

    angle = abs(angle)

    if (angle < 22.5 or angle > 157.5):
        return (size_x, abs(size_y * sin(angle * (pi / 180))))
    elif (angle > 67.5 and angle < 112.5):
        return (abs(size_x * cos(angle * (pi / 180))), size_y)
    else:
        return (abs(size_x * cos(angle * (pi / 180))), abs(size_y * sin(angle * (pi / 180))))

def get_angle_line(origin, destination):
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    return atan2(y_delta, x_delta) * 180 / pi

def get_distance(point_1, point_2):
    return sqrt(pow(point_1[0] - point_2[0], 2) + pow(point_1[1] - point_2[1], 2))

def get_transformation(element):
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
