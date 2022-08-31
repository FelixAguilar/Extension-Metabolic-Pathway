from cmath import sqrt
from xmlrpc.client import boolean
import inkex, re, math
from math import atan, atan2, sin, cos, pi, sqrt, pow
from shared.Add_Element import add_metabolic_building_block, add_elemental_reaction, add_reaction, add_inverse_reaction, add_component, font_size
from shared.Add_Arrow import add_arrow

def format_num(string) -> float:
    separator = string.find(',')
    if(separator != -1):
        string = string[:separator-1] + '.' + string[separator+1:]
        return float(string)
    return float(string)
def is_metabolic_pathway_element(svg_element) -> bool:
    pattern = re.compile("[E|I|M|C|R] [0-9]+")
    if(pattern.match(svg_element.get_id())):
        return True
    return False
def string_to_list(string) -> list:
    s_list = string.split(' ')
    f_list = []
    for s in s_list:
        s = s.split(",")
        x = float(s[0])
        y = float(s[1])
        f_list.append((x, y))
    return f_list
def is_component(ID) -> bool:
    pattern = re.compile("C [0-9]+")
    if(pattern.match(ID)):
        return True
    return False
def is_elemental_reaction(string) -> bool:
    pattern = re.compile("E [0-9]+")
    if(pattern.match(string)):
        return True
    return False
def get_elipse_size(size_x, size_y, angle):
    angle = angle * (pi / 180)
    radius = (size_x * size_y) / (sqrt((pow(size_x, 2) * pow(sin(angle), 2)) + (pow(size_y, 2) * pow(cos(angle), 2))))
    return (abs(radius * cos(angle)), abs(radius * sin(angle)))

def get_rectangle_size(size_x, size_y, angle):

    center_base = size_x / 2
    center_hight = size_y / 2

    vertex_angle = atan(center_hight / center_base) * 180 / pi

    if((angle > vertex_angle and angle < 180 - vertex_angle) or (angle < -vertex_angle and angle > vertex_angle - 180)):
        inkex.errormsg((abs(center_base * cos(angle * (pi / 180))), center_hight))
        return (abs(center_base * cos(angle * (pi / 180))), center_hight)
    else:
        inkex.errormsg((center_base, abs(center_hight * sin(angle * (pi / 180)))))
        return (center_base, abs(center_hight * sin(angle * (pi / 180))))

def get_octogon_size(size, size_y, angle):

    size += 1
    angle = abs(angle)
    hight = size * cos(22.5 * (pi / 180))

    if (angle < 22.5 or angle > 157.5):
        return (hight, abs(hight * sin(angle * (pi / 180))))
    elif (angle > 67.5 and angle < 112.5):
        return (abs(hight * cos(angle * (pi / 180))), hight)
    else:
        return (abs(hight * cos(angle * (pi / 180))), abs(hight * sin(angle * (pi / 180))))

def get_size(ID, size_x, size_y, angle):
    if(is_component(ID)):
        return get_rectangle_size(size_x, size_y, angle)
    if(is_elemental_reaction(ID)):
        return get_octogon_size(size_x, size_y, angle)
    else:
        return get_elipse_size(size_x, size_y, angle)

def get_angle_line(origin, destination):
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    return atan2(y_delta, x_delta) * 180 / pi
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
def get_distance(point_1, point_2):
    return math.sqrt(math.pow(point_1[0] - point_2[0], 2) + math.pow(point_1[1] - point_2[1], 2))

# Class for the paths.
class Path:
    def __init__(self, o, d, p) -> None:
        self.o = o  # Tupple origin.
        self.d = d  # Tupple destiny.
        self.p = p  # Tupple point of the arrow.

    def get_o(path):
        return path.o
    def get_d(path):
        return path.d
    def get_p(path):
        return path.p

    # Changes the direction of the arrow depending on the point of the arrow.
    def change_direction(path):
        distance_oh = get_distance(path.p, path.o)
        distance_dh = get_distance(path.p, path.d)
        if(distance_oh > distance_dh):
            path.d = path.o
            path.o = path.p
        else:
            path.o = path.p

    # Applies the transformation on the origin, destiny and point of the path.
    def apply_transformation(path, transformation):
        path.o = (path.o[0] + transformation[0], path.o[1] + transformation[1])
        path.d = (path.d[0] + transformation[0], path.d[1] + transformation[1])
        path.p = (path.p[0] + transformation[0], path.p[1] + transformation[1])

    def __str__(self) -> str:
        return str(self.o) + " " + str(self.d) + " " + str(self.p)

class Group_info:
    def __init__(self, group, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.group = group

    def get_size_x(group_info):
        return group_info.size_x

    def get_size_y(group_info):
        return group_info.size_y

    def get_group(group_info):
        return group_info.group

class Constructor(inkex.EffectExtension):

    # def add_arguments(self, pars):

    def effect(self):

        # Patterns for the text and elements.
        pattern1 = re.compile("graph*")
        pattern2 = re.compile("R[0-9][0-9][0-9][0-9][0-9]_rev")
        pattern3 = re.compile("R[0-9][0-9][0-9][0-9][0-9]")
        pattern4 = re.compile("[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+")
        pattern5 = re.compile("^([0-9]+)$")
        pattern6 = re.compile("C[0-9][0-9][0-9][0-9][0-9]")
        pattern7 = re.compile("E *")
        pattern8 = re.compile("^([0-9]+)_r$")
        pattern9 = re.compile("^([0-9]+)\-([0-9]+)_r$")

        # Lists for the elements in the graph.
        lines = []
        groups_info = []
        transform = []

        # Gets a editable list of all ids.
        ids = []
        for id in self.svg.get_ids():
            ids.append(id)

        for id in ids:

            # if the id is from  a graph gets the transformation.
            if(pattern1.match(id)):
                element = self.svg.getElementById(id)
                transform = get_transformation(element)
            else:

                # Lists used for each id element separated in text and figures.
                texts = []
                figures = []

                # get element by ID and if it is a group gets all his child elements divided in text and figures.
                element = self.svg.getElementById(id)
                if(element.tag_name == 'g'):
                    for child in element.descendants():
                        if(child.tag_name == 'text'):
                            texts.append(child.text)
                        if(child.tag_name == 'ellipse' or child.tag_name == 'polygon' or child.tag_name == 'path'):
                            figures.append(child.get_id())

                # If there is no text but has figures it is a path.
                if(not texts and figures):

                    # Variables used to define a path.
                    points = "" # String of data extracted.
                    point = 0   # Farthedst point in the arrow.
                    origin = 0  # Origin of the path.
                    destiny = 0 # Destiny of the path.

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

                            # Gets the greatest hight and the vertex of it.
                            if(distance_AB > distance_BC and distance_AC > distance_BC):
                                point = point_A
                            if(distance_BC > distance_AC and distance_AB > distance_AC):
                                point = point_B
                            else:
                                point = point_C

                    # Adds the path to the list.
                    lines.append(Path(origin, destiny, point))

                # line tranformation before change direction.

                # It is a element of the Pathway.
                elif(texts and figures):

                    # Variables used to define a element.
                    reactions = []    # All code reaction in the element.
                    id_element = ""   # ID of the element.
                    type_element = "" # Type of element.
                    enzime = ""       # Code of the enzime.
                    position = []     # Center of the element.
                    size = 0          # Size of the element.
                    size_x = 0        # Size of the element in the x axis.
                    size_y = 0        # Size of the element in the y axis.
                    name = ""         # Used for compounds if it is not using codes.

                    # Filters the text setting the type of element with it if it can. Also saves the text in the correct variable.
                    for text in texts:
                        if(text == 'MBB'):
                            type_element = 'MBB'
                        elif(pattern2.match(text)):
                            type_element = 'Inverse'
                            reactions.append(text)
                        elif(pattern3.match(text)):
                            type_element = 'Reaction'
                            reactions.append(text)
                        elif(pattern4.match(text)):
                            enzime = text
                        elif(pattern5.match(text) or pattern8.match(text) or pattern9.match(text)):
                            if(pattern9.match(text)):
                                id_element = text
                                #text[:text.find('-')]
                            elif(pattern8.match(text)):
                                id_element = text[:-2]
                            else:
                                id_element = text
                        elif(pattern6.match(text)):
                            type_element = 'Compound'
                            name = text
                        else:
                            type_element = 'Compound'
                            name = text

                    # Iterates inside the figures and filters the data extracted.
                    for figure in figures:
                        figure = self.svg.getElementById(figure)

                        # If it is an ellipse gets the center of it and the smallest size.
                        if(figure.tag_name == 'ellipse'):
                            position = (float(figure.get('cx')), float(figure.get('cy')))
                            size_x = format_num(figure.get('rx'))
                            size_y = format_num(figure.get('ry'))
                            size = min(size_x, size_y)

                        # If it is a poligon then gets the points.
                        elif(figure.tag_name == 'polygon'):
                            points = string_to_list(figure.get('points'))

                            # If it is filled with yellow then it will be an elemental reaction.
                            if(figure.get('fill') == 'yellow'):
                                type_element = 'Elemental'

                                # Gets the first to the fourth point of the octagon.
                                x_A = float(points[0][0])
                                y_A = float(points[0][1])
                                x_B = float(points[1][0])
                                y_B = float(points[1][1])
                                x_C = float(points[2][0])
                                y_C = float(points[2][1])
                                x_D = float(points[3][0])
                                y_D = float(points[3][1])
                                x_E = float(points[4][0])
                                y_E = float(points[4][1])

                                # With this points calculates the center and size of the element.
                                position = ((x_A + x_E) / 2, (y_A + y_E) / 2)
                                size_x = math.sqrt(math.pow(((x_D + x_C) / 2) - x_B, 2))
                                size_y = math.sqrt(math.pow(((y_A + y_B) / 2) - y_C, 2))
                                size = min(size_x, size_y)

                            # If it has less or equal points than 5 it is a compound.
                            elif(len(points) <= 5):
                                type_element = 'Compound'

                                # Gets 2 diagonal points and the middle coordentate x.
                                x_A = float(points[0][0])
                                y_A = float(points[0][1])
                                x_B = float(points[2][0])
                                y_B = float(points[2][1])
                                x_C = float(points[1][0])
                                y_C = float(points[1][1])

                                # gets the center of the compound and x size.
                                position = ((x_A + x_B) / 2, (y_A + y_B) / 2)
                                size_x = abs(x_A - x_C)
                                size_y = abs(y_A - y_B)
                                size = size_x
                                
                    # Proceeds to set the element with the information obtained inside the list.
                    if(type_element == 'MBB'):
                        groups_info.append(Group_info(add_metabolic_building_block(self, id_element, position[0], position[1], size), size_x, size_y))
                    elif(type_element == 'Reaction'):
                        groups_info.append(Group_info(add_reaction(self, id_element, reactions, enzime,  position[0], position[1], size), size_x, size_y))
                    elif(type_element == 'Elemental'):
                        groups_info.append(Group_info(add_elemental_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size), size_x, size_y))
                    elif(type_element == 'Inverse'):
                        groups_info.append(Group_info(add_inverse_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size), size_x, size_y))
                    elif(type_element == 'Compound'):
                        groups_info.append(Group_info(add_component(self, name, position[0], position[1], size), size_x, size_y))

        # For each group created, applies the transformation of the graph so it will me draw in the correct spot.
        layer = self.svg.get_current_layer()
        for group_info in groups_info:

            group = group_info.get_group()
            # Iterates trough the childs in the group and changes the center coordinates with the transformation.
            for child in group.descendants():

                if(child.tag_name == 'path'):

                    # For all the path elements.
                    child.set('sodipodi:cx', float(child.get('sodipodi:cx')) + transform[0])
                    child.set('sodipodi:cy', float(child.get('sodipodi:cy')) + transform[1])

                    # For the polygons inside a elemental reaction.
                    if(pattern7.match(group.get_id())):
                        child.set('transform', 'rotate(23, ' + str(child.get('sodipodi:cx')) + ', ' + str(child.get('sodipodi:cy')) + ')')
                else:

                    # For text and rectangles.
                    child.set('x', float(child.get('x')) + transform[0])
                    child.set('y', float(child.get('y')) + transform[1])

            # Adds the group to the layer.
            layer.add(group)

        for line in lines:

            # Variables for the paths.
            nearest_orig = "" # ID of the nearest element to origin.
            nearest_dest = "" # ID of the nearest element to destiny.
            distance_orig = float("inf") # Distance to the nearest element to origin.
            distance_dest = float("inf") # Distance to the nearest element to destiny.

            # Applies the transformation, changes the direction of the arrow and gets the angle of the line to the x-axis.
            line.apply_transformation(transform)
            line.change_direction()
            angle = get_angle_line(line.d, line.o)

            # Iterates trought all elements in groups for which the path interconects them.
            for group_info in groups_info:

                group = group_info.get_group()
                size_x = group_info.get_size_x()
                size_y = group_info.get_size_y()
                
                # It must be an metabolic_path_way.
                if(is_metabolic_pathway_element(group)):

                    # Gets the center of the group.
                    group_center = (float(group.get('x')), float(group.get('y')))

                    # Gets the distance to the origin and destiny of this group.
                    distance_o = math.sqrt(math.pow(group_center[0] - line.o[0], 2) + math.pow(group_center[1] - line.o[1], 2))
                    distance_d = math.sqrt(math.pow(group_center[0] - line.d[0], 2) + math.pow(group_center[1] - line.d[1], 2))

                    # Gets the size of the element and the corrected distance to the line.
                    size_o = get_size(group.get_id(), size_x, size_y, angle)
                    distance_o = distance_o - math.sqrt(math.pow(size_o[0], 2) + math.pow(size_o[1], 2))
                    size_d = get_size(group.get_id(), size_x, size_y, angle)
                    distance_d = distance_d - math.sqrt(math.pow(size_d[0], 2) + math.pow(size_d[1], 2))

                    # Checks if the distance to the destiny is smaller, if it is then updates it.
                    if(distance_dest >= distance_d):
                        distance_dest = distance_d
                        nearest_dest = group

                    # Checks if the distance to the origin is smaller, if it is then updates it.
                    if(distance_orig >= distance_o):
                        distance_orig = distance_o
                        nearest_orig = group
            
            # If neither of them is empty then draw the arrow.
            if(nearest_dest != "" and nearest_orig != ""):
                add_arrow(self, nearest_dest, nearest_orig, False)

        # Deletes old graph.
        self.svg.getElementById('graph0').delete()

if __name__ == '__main__':
    Constructor().run()
