import inkex
from typing import Any
from inkex import BaseElement
from math import sin, cos, pi
from shared.Geometry import get_transformation, get_angle_line, get_circle_size, get_regular_octogon_size, get_component_size
from shared.Boleans import is_component, is_elemental_reaction
from shared.Element import add_triangle, add_line

# Function that using the id decides which function to use to obtain the size in x and y axis.
def get_size(ID: str, size: float, angle: float) -> tuple[float, float]:
    if(is_component(ID)):
        return get_component_size(size, angle)
    if(is_elemental_reaction(ID)):
        return get_regular_octogon_size(size, angle)
    else:
        return get_circle_size(size, angle)

# Function that returns the coordenates from point A and B 
def get_line_coordinates(center_A: tuple[float, float], size_A: tuple[float, float], center_B: tuple[float, float], size_B: tuple[float, float]) -> tuple[tuple[float, float], tuple[float, float]]:

        # For x-axis.
        if(center_A[0] > center_B[0]):
            x_A = center_A[0] - size_A[0]
            x_B = center_B[0] + size_B[0]
        else:
            x_A = center_A[0] + size_A[0]
            x_B = center_B[0] - size_B[0]

        # For y-axis.
        if(center_A[1] > center_B[1]):
            y_A = center_A[1] - size_A[1]
            y_B = center_B[1] + size_B[1]
        else:
            y_A = center_A[1] + size_A[1]
            y_B = center_B[1] - size_B[1]

        return ((x_A, y_A), (x_B, y_B))

def add_straight_arrow(self, origin_id, destiantion_id, origin, destination, direction):

    # Calculate the angle of the arrow to the horizontal axis.
    angle = get_angle_line(origin, destination)

    # Triangle height (sides are 1) and splited into x and y.
    height = 3
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

def add_arrow(self: Any, element_A: Any, element_B: Any, direction: bool) -> None:

    # Obtains the properties of both elements.
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
