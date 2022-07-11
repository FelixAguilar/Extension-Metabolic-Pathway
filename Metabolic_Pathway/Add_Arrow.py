import inkex, re
from inkex import PathElement, BaseElement
from math import atan, atan2, sin, cos, pi

def is_component(ID):
    pattern = re.compile("C [0-9]+")
    if(pattern.match(ID)):
        return True
    return False
def is_elemental_reaction(string):
    pattern = re.compile("E [0-9]+")
    if(pattern.match(string)):
            return True
    return False
def get_component_center(ID, center, size):
    if(is_component(ID)):
        return (center[0] + (size / 2), center[1] + (size / 6))
    return center
def get_transformation(element):
    t = str(element.get('transform'))

    if(t == "None"):
        return (0,0)
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
        return (x,y)
def add_line(origin, destination):
    line = inkex.PathElement()
    line.style = {'stroke': 'black', 'stroke-width': '0.25px', 'fill': 'none'}
    line.path = 'M {},{} L {},{}'.format(origin[0], origin[1], destination[0], destination[1])
    return line
def add_triangle(center, rotation):
    style = {'stroke': 'black', 'fill': 'black', 'stroke-width': '0.25px'}
    elem = PathElement.star(center, (1, 1), 3)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(' + str(rotation) + ', ' + str(center[0]) + ', ' + str(center[1]) + ')')
    elem.style = style
    return elem
def get_angle_line(origin, destination):
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    return atan2(y_delta, x_delta) * 180 / pi
def add_straight_arrow(self, origin_id, destiantion_id, origin, destination, direction):

    # Calculate the angle of the arrow to the horizontal axis.
    angle = get_angle_line(origin, destination)

    # Triangle height (sides are 1) and splited into x and y.
    height = 1.2
    x_height = height * cos(angle * (pi / 180))
    y_height = height * sin(angle * (pi / 180))
    
    # Creates the group and adds the elements depending on the direction.
    group = inkex.Group()
    group.add(add_line(origin, destination))
    if(direction == True):
        group.add(add_triangle((destination[0] - x_height, destination[1] - y_height), angle))
        group.set('id_dest', destiantion_id)
        group.set('id_orig', origin_id)
    else:
        group.add(add_triangle((origin[0] + x_height, origin[1] + y_height), angle + 180))
        group.set('id_orig', destiantion_id)
        group.set('id_dest', origin_id)
        
    # Adds the group to the layer and assigns a unique id.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'P ')
def get_circle_size(size, angle):
    return (abs(size * cos(angle * (pi / 180))), abs(size * sin(angle * (pi / 180))))
def get_rectangle_size(size, angle):

    center_base = size / 2
    center_hight = size / 6 

    vertex_angle = atan(center_hight / center_base) * 180 / pi

    if((angle > vertex_angle and angle < 180 - vertex_angle) or (angle < -vertex_angle and angle > vertex_angle - 180)):
        return (abs(center_base * cos(angle * (pi / 180))), center_hight)
    else:
        return (center_base, abs(center_hight * sin(angle * (pi / 180))))
def get_octogon_size(size, angle):
    
    size += 1
    angle = abs(angle)
    hight = size * cos(22.5 * (pi / 180))

    if (angle < 22.5 or angle > 157.5):
        return (hight, abs(hight * sin(angle * (pi / 180))))
    elif (angle > 67.5 and angle < 112.5):
        return (abs(hight * cos(angle * (pi / 180))), hight)
    else:
        return (abs(hight * cos(angle * (pi / 180))), abs(hight * sin(angle * (pi / 180))))
def get_size(ID, size, angle):
    if(is_component(ID)):
        return get_rectangle_size(size, angle)
    if(is_elemental_reaction(ID)):
        return get_octogon_size(size, angle)
    else:
        return get_circle_size(size, angle)
def get_line_coordinates(center_A, size_A, center_B, size_B):
        if(center_A[0] > center_B[0]):
            x_A = center_A[0] - size_A[0]
            x_B = center_B[0] + size_B[0]
        else:
            x_A = center_A[0] + size_A[0]
            x_B = center_B[0] - size_B[0]

        if(center_A[1] > center_B[1]):
            y_A = center_A[1] - size_A[1]
            y_B = center_B[1] + size_B[1]
        else:
            y_A = center_A[1] + size_A[1]
            y_B = center_B[1] - size_B[1]

        return ((x_A, y_A), (x_B, y_B))
def add_arrow(self, element_A, element_B, direction):
    # Obtains the properties of the elements.
    center_A = (float(element_A.get('x')), float(element_A.get('y')))
    size_A = float(element_A.get('size'))
    id_A = element_A.get_id()

    center_B = (float(element_B.get('x')), float(element_B.get('y')))
    size_B = float(element_B.get('size'))
    id_B = element_B.get_id()

        # Gets the transformations of the elements if there are, and applies them.
    t = get_transformation(element_A)
    center_A = (center_A[0] + t[0], center_A[1] + t[1])
    t = get_transformation(element_B)
    center_B = (center_B[0] + t[0], center_B[1] + t[1])

    # If it is a component, get the center of it.
    center_A = get_component_center(id_A, center_A, size_A)
    center_B = get_component_center(id_B, center_B, size_B)
        
    # Gets the angle of the line between the two elements.
    angle = get_angle_line(center_B, center_A)

    # Gets the size to add or remove from the elements according to the type of it.
    size_A = get_size(id_A, size_A, angle)
    size_B = get_size(id_B, size_B, angle)

    # Obtains the coordinates of the two points of the line.
    coordinates = get_line_coordinates(center_A, size_A, center_B, size_B)
    coordinates_A = coordinates[0]
    coordinates_B = coordinates[1]

    # Adds the arrow, this one doesn't take into account the elements in his path.
    add_straight_arrow(self, id_B, id_A, coordinates_B, coordinates_A, direction)
