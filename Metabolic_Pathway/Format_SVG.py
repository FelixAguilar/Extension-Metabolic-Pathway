import inkex, re
from typing import Any, List, Tuple
from math import sqrt, pow
from shared.Arrow import add_arrow
from shared.Boleans import is_component, is_elemental_reaction, is_metabolic_pathway_element
from shared.Geometry import get_rectangle_size, get_octogon_size, get_elipse_size, get_angle_line, get_transformation, get_distance, get_equivalent_angle
from shared.Element import add_metabolic_building_block, add_elemental_reaction, add_reaction, add_inverse_reaction, add_component
from shared.Errors import *

# Obtains from the string the number in float format.
def format_num(number: str) -> float:
    separator = number.find(',')
    if(separator != -1):
        number = number[:separator-1] + '.' + number[separator+1:]
    return float(number)

# From a list in string format obtains all the points inside a list in float form.
def string_to_list(list: str) -> List[Tuple[float, float]]:
    points_list = list.split(' ')
    coordenates_list = []
    for point in points_list:
        point = point.split(",")
        x = float(point[0])
        y = float(point[1])
        coordenates_list.append((x, y))
    return coordenates_list

# Function that using the id decides which function to use to obtain the size in x and y axis.
def get_size(ID: str, value_x: Any, value_y: Any, angle: float) -> Tuple[float, float]:
    if(is_component(ID)):
        return get_rectangle_size(value_x, value_y, angle)
    if(is_elemental_reaction(ID)):
        return get_octogon_size(value_x, value_y, angle)
    else:
        return get_elipse_size(value_x, value_y, angle)

# Class used to define each path.
class Path:

    # Constructor.
    def __init__(self, o: Tuple[float, float], d: Tuple[float, float], p: Tuple[float, float]) -> None:
        self.o: tuple[float, float] = o  # Tuple origin. [x,y]
        self.d: tuple[float, float] = d  # Tuple destiny. [x,y]
        self.p: tuple[float, float] = p  # Tuple arrow head. [x,y]

    # Gets for the atributes.
    def get_o(self) -> Tuple[float, float]:
        return self.o
    def get_d(self) -> Tuple[float, float]:
        return self.d
    def get_p(self) -> Tuple[float, float]:
        return self.p

    # Changes the direction of the arrow depending on the point of the arrow and changes de origin of the line for the head of the arrow.
    def change_direction(self) -> None:
        distance_oh = get_distance(self.p, self.o)
        distance_dh = get_distance(self.p, self.d)
        if(distance_oh > distance_dh):
            self.d = self.o
            self.o = self.p
        else:
            self.o = self.p

    # Applies the transformation on the origin, destiny and head of the path.
    def apply_transformation(self, transformation) -> None:
        self.o = (self.o[0] + transformation[0], self.o[1] + transformation[1])
        self.d = (self.d[0] + transformation[0], self.d[1] + transformation[1])
        self.p = (self.p[0] + transformation[0], self.p[1] + transformation[1])

# Class used to define a element group and his original size. 
class Group_info:

    # Constructor.
    def __init__(self, group, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.group = group          # Group to be drawn on the canvas.

    # Gets for the atributes.
    def get_size_x(self) -> float:
        return self.size_x
    def get_size_y(self) -> float:
        return self.size_y
    def get_group(self) -> Any:
        return self.group

    def set_group(self, group) -> None:
        self.group = group

# Element info and call to generate it.
class Element:

    #Constructor
    def __init__(self: Any, type: str, position: Tuple[float,float], size: float, id_element: str = None, reactions: List[str] = None, enzime: str = None, name: str = None) -> None:
        self.type = type
        self.id_element = id_element
        self.name = name
        self.reactions = reactions
        self.enzime = enzime
        self.position = position
        self.size = size

    def apply_transform(self, transform: Tuple[float, float]) -> None:
        self.position = (self.position[0] + transform[0], self.position[1] + transform[1])

    def generate(self: Any, api: Any) -> Any:
        if(self.type == 'MBB'):
            return add_metabolic_building_block(api, self.id_element, self.position[0], self.position[1], self.size)
        elif(self.type == 'Reaction'):
            return add_reaction(api, self.id_element, self.reactions, self.enzime, self.position[0], self.position[1], self.size)
        elif(self.type == 'Elemental'):
            return add_elemental_reaction(api, self.id_element, self.reactions, self.enzime, self.position[0], self.position[1], self.size)
        elif(self.type == 'Inverse'):
            return add_inverse_reaction(api, self.id_element, self.reactions, self.enzime, self.position[0], self.position[1], self.size)
        elif(self.type == 'Compound'):
            return add_component(api, self.name, self.position[0], self.position[1], self.size)

class Constructor(inkex.EffectExtension):

    # def add_arguments(self, pars):

    def effect(self):

        # Patterns for the text inside the graph.
        pattern1 = re.compile("graph*")                                     # Graph identification pattern.
        pattern2 = re.compile("R[0-9][0-9][0-9][0-9][0-9]_rev")             # Reverse reaction code pattern.
        pattern3 = re.compile("R[0-9][0-9][0-9][0-9][0-9]")                 # Reaction code pattern.
        pattern4 = re.compile("[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+") # Enzime code pattern.
        pattern5 = re.compile("^([0-9]+(\-[0-9]+)?(_r)?)$")                 # ID code pattern.

        graph = None
        lines: list[Path] = []              # List that will contain all the paths of the graph.
        groups_info: list[Group_info] = []  # List that will contain all the groups of the graph.
        transform: tuple[float, float] = [] # Tuple that will indicate which transformation must be applied to the elements of the graph.

        # Get list of all the ids of the graph in the current state.
        processed = False
        ids: list[str] = []
        for id in self.svg.get_ids():
            if(is_metabolic_pathway_element(id)):
                processed = True
            ids.append(id)

        if (processed):
            inkex.errormsg(error_format)
            return

        # Each element of the graph is filtered to generate the new format.
        for id in ids:

            # If the id indicates the graph itself, the transformation is extracted.
            if(pattern1.match(id)):
                graph = self.svg.getElementById(id)
                transform = get_transformation(graph)
            else:
                texts: list[str] = []   # List that contains all text inside a element.
                figures: list[str] = [] # List that contains all figures ids inside a element.

                # Get the element using the id and check that it is a group using the tag.
                element = self.svg.getElementById(id)
                if(element.tag_name == 'g'):

                    # IIterates over its children and separates figures and texts using the tag.
                    for child in element.descendants():
                        if(child.tag_name == 'text'):
                            texts.append(child.text)
                        if(child.tag_name == 'ellipse' or child.tag_name == 'polygon' or child.tag_name == 'path'):
                            figures.append(child.get_id())

                # If there is no text but has figures it has to be a path.
                if(not texts and figures):
                    head: tuple[float, float] = 0    # Furthest point in the arrow.
                    origin: tuple[float, float] = 0  # Origin of the path.
                    destiny: tuple[float, float] = 0 # Destiny of the path.

                    # For each figure checks if is a path o a polygon.
                    for figure in figures:
                        figure = self.svg.getElementById(figure)

                        # If it is a path then gets the origin point and destiny point in no order.
                        if(figure.tag_name == 'path'):
                            line = figure.get('d')
                            if (line.find('C') != -1):
                                y_origin = line[line.find(',') + 1:line.find('C')]
                            else:
                                y_origin = line[line.find(',') + 1:line.find(' ')]
                            origin = (float(line[line.find('M') + 1:line.find(',')]), float(y_origin))
                            destiny = (float(line[line.rfind(' ') + 1: line.rfind(',')]), float(line[line.rfind(',') + 1:]))

                        # If it is the head of the path.
                        else:

                            # It gets the points for the triangle and separates them into tupples.
                            points = figure.get('points')
                            point_list = string_to_list(points)

                            # Triangle points (tupples).
                            point_A = point_list[0]
                            point_B = point_list[1]
                            point_C = point_list[2]

                            # Gets size of the three sides.
                            distance_AB = get_distance(point_A, point_B)
                            distance_BC = get_distance(point_B, point_C)
                            distance_AC = get_distance(point_A, point_C)

                            # Gets the head of the arrow.
                            if(distance_AB > distance_BC and distance_AC > distance_BC):
                                head = point_A
                            if(distance_BC > distance_AC and distance_AB > distance_AC):
                                head = point_B
                            else:
                                head = point_C

                    # Adds the path to the list.
                    lines.append(Path(origin, destiny, head))

                # It is a element of the Pathway.
                elif(texts and figures):
                    reactions: list[str]= []           # All code reaction in the element.
                    id_element: str = ""               # ID of the element.
                    type_element: str = ""             # Type of element.
                    enzime: str = ""                   # Code of the enzime.
                    position: tuple[float, float] = [] # Center of the element.
                    size: float = 0                    # Size of the element.
                    size_x: float = 0                  # Size of the element in the x axis.
                    size_y: float = 0                  # Size of the element in the y axis.
                    name: float = ""                   # Used for compounds if it is not using codes.

                    # Filters the text setting the type of element with it if it can. Also saves the text in the correct variable.
                    for text in texts:
                        if(pattern2.match(text) or pattern3.match(text)):
                            reactions.append(text)
                        elif(pattern4.match(text)):
                            enzime = text
                        elif(pattern5.match(text)):
                            id_element = text
                        else:
                            name = text

                    # Iterates inside the figures and filters the data extracted.
                    for figure in figures:
                        figure = self.svg.getElementById(figure)

                        # If it is an ellipse.
                        if(figure.tag_name == 'ellipse'):
                            if(figure.get('fill') == 'lightgrey'):
                                type_element = 'MBB'
                            elif(figure.get('fill') == 'yellow'):
                                type_element = 'Reaction'
                            else:
                                type_element = 'Inverse'

                            # Obtains the center of it, size in x-axis and y-axis and the smallest size of between them.
                            position = (float(figure.get('cx')), float(figure.get('cy')))
                            size_x = format_num(figure.get('rx'))
                            size_y = format_num(figure.get('ry'))
                            size = min(size_x, size_y)

                        # If it is a poligon.
                        elif(figure.tag_name == 'polygon'):

                            # Obtains a list of all the points that forms it.
                            points = string_to_list(figure.get('points'))

                            # If it is filled with yellow then it will be an elemental reaction.
                            if(figure.get('fill') == 'yellow'):
                                type_element = 'Elemental'

                                # Vertex names for the octogon and extraction of used points
                                #   D___C
                                #  /     \
                                # E       B
                                # |       |
                                # F       A
                                #  \     /
                                #   G___H
                                x_A = float(points[0][0])
                                y_A = float(points[0][1])
                                x_B = float(points[1][0])
                                y_B = float(points[1][1])
                                x_C = float(points[2][0])
                                y_C = float(points[2][1])
                                x_D = float(points[3][0])
                                x_E = float(points[4][0])
                                y_E = float(points[4][1])

                                # With the points, values used for understanding the octogon are calculated.
                                position = ((x_A + x_E) / 2, (y_A + y_E) / 2)  # Center (c)
                                size_x = get_distance(position, (x_A, position[1])) # width (h2)
                                size_y = get_distance(position, (position[0], y_C)) # hight (h1)
                                radius_x = get_distance(position, (x_B, y_B))  # radius_hight (r2)
                                radius_y = get_distance(position, (x_C, y_C))  # radius_width (r1)
                                size = min(radius_x, radius_y)

                            # If it has less or equal points than 5 it is a compound.
                            elif(len(points) <= 5):
                                type_element = 'Compound'

                                # Gets the first to the third point of the rectangle.
                                x_A = float(points[0][0])
                                y_A = float(points[0][1])
                                x_B = float(points[1][0])
                                y_B = float(points[1][1])
                                x_C = float(points[2][0])
                                y_C = float(points[2][1])

                                # Gets the center of the compound, size in x-axis and y-axis.
                                position = ((x_A + x_C) / 2, (y_A + y_C) / 2)
                                size_x = abs(x_A - x_B)
                                size_y = abs(y_A - y_C)
                                size = size_x

                    # Proceeds to set the Group with the information obtained from the scraping.
                    if(type_element == 'MBB'):
                        groups_info.append(Group_info(Element(type_element, position, size, id_element), size_x, size_y))
                    elif(type_element == 'Reaction'):
                        groups_info.append(Group_info(Element(type_element, position, size, id_element, reactions, enzime), size_x, size_y))
                    elif(type_element == 'Elemental'):
                        groups_info.append(Group_info(Element(type_element, position, size, id_element, reactions, enzime), (size_x, size_y), (radius_x, radius_y)))
                    elif(type_element == 'Inverse'):
                        groups_info.append(Group_info(Element(type_element, position, size, id_element, reactions, enzime), size_x, size_y))
                    elif(type_element == 'Compound'):
                        groups_info.append(Group_info(Element(type_element, position, size, name = name), size_x, size_y))

        # Once it has been defined all paths and groups is time to generate the new elements.

        # For each group, applies the transformation of the graph so it will me draw in the correct spot.
        layer = self.svg.get_current_layer()
        for group_info in groups_info:
            group = group_info.get_group()
            group.apply_transform(transform)
            group_created = group.generate(self)
            group_info.set_group(group_created)

            # Adds the group to the layer.
            layer.add(group_created)

        # Here it will draw all path between the elements.
        for line in lines:

            # Variables for the paths.
            nearest_orig: str = "" # ID of the nearest element to origin.
            nearest_dest: str = "" # ID of the nearest element to destiny.
            distance_orig = float("inf") # Distance to the nearest element to origin.
            distance_dest = float("inf") # Distance to the nearest element to destiny.

            # Applies the transformation, changes the direction of the arrow and gets the angle of the line to the x-axis.
            line.apply_transformation(transform)
            line.change_direction()

            # Iterates trought all elements in groups for which the path interconects them.
            for group_info in groups_info:

                group = group_info.get_group()
                size_x = group_info.get_size_x()
                size_y = group_info.get_size_y()
                
                # It must be an metabolic_pathway.
                if(is_metabolic_pathway_element(group.get_id())):

                    # Gets the center of the group.
                    group_center = (float(group.get('x')), float(group.get('y')))

                    # Gets the distance to the origin and destiny of this group.
                    distance_o = sqrt(pow(group_center[0] - line.o[0], 2) + pow(group_center[1] - line.o[1], 2))
                    distance_d = sqrt(pow(group_center[0] - line.d[0], 2) + pow(group_center[1] - line.d[1], 2))

                    angle_o = get_equivalent_angle(get_angle_line(line.get_o(), group_center))
                    angle_d = get_equivalent_angle(get_angle_line(line.get_d(), group_center))

                    # Gets the size of the element and the corrected distance to the line.
                    size_o = get_size(group.get_id(), size_x, size_y, angle_o)
                    size_d = get_size(group.get_id(), size_x, size_y, angle_d)

                    distance_o = distance_o - size_o
                    distance_d = distance_d - size_d

                    if(distance_d < distance_o):
                        # Checks if the distance to the destiny is smaller, if it is then updates it.
                        if(distance_dest > distance_d):

                            distance_dest = distance_d
                            nearest_dest = group
                    else:
                        # Checks if the distance to the origin is smaller, if it is then updates it.
                        if(distance_orig > distance_o):

                            distance_orig = distance_o
                            nearest_orig = group
            
            # If neither of them is empty then draw the arrow.
            if(nearest_dest != "" and nearest_orig != ""):
                add_arrow(self, nearest_dest, nearest_orig)

        # Deletes old graph.
        if(graph != None):
            graph.delete()

if __name__ == '__main__':
    Constructor().run()
