from pathlib import Path
import inkex, re, math
from math import atan, atan2, sin, cos, pi
from shared.Add_Element import add_metabolic_building_block, add_elemental_reaction, add_reaction, add_inverse_reaction, add_component
from shared.Add_Arrow import add_arrow

def format_num(string):
    separator = string.find(',')
    if(separator != -1):
        string = string[:separator-1] + '.' + string[separator+1:]
        return float(string)
    return float(string)
def is_metabolic_pathway_element(svg_element):
    pattern = re.compile("[E|I|M|C|R] [0-9]+")
    if(pattern.match(svg_element.get_id())):
            return True
    return False
def string_to_list(string):
    s_list = string.split(' ')
    f_list = []
    for s in s_list:
        s = s.split(",")
        x = float(s[0])
        y = float(s[1])
        f_list.append((x, y))
    return f_list

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
def get_angle_line(origin, destination):
    x_delta = destination[0] - origin[0]
    y_delta = destination[1] - origin[1]
    return atan2(y_delta, x_delta) * 180 / pi

class path:
    def __init__(self, o, d) -> None:
        self.o = o
        self.d = d

    def get_o(path):
        return path.o

    def get_d(path):
        return path.d

    def change_direction(path, head):
        distance_oh = math.sqrt(math.pow(head[0] - path.o[0], 2) +  math.pow(head[1] - path.o[1], 2))
        distance_dh = math.sqrt(math.pow(head[0] - path.d[0], 2) +  math.pow(head[1] - path.d[1], 2))

        if(distance_oh < distance_dh):
            aux = path.o
            path.o = path.d
            path.d = aux

    def __str__(self) -> str:
        return str(self.o) + " " + str(self.d)

class Constructor(inkex.EffectExtension):
    
    #def add_arguments(self, pars):
    
    def effect(self):

        pattern1 = re.compile("graph*")
        pattern2 = re.compile("R[0-9][0-9][0-9][0-9][0-9]_rev")
        pattern3 = re.compile("R[0-9][0-9][0-9][0-9][0-9]")
        pattern4 = re.compile("[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+")
        pattern5 = re.compile("[0-9]+")
        pattern6 = re.compile("C[0-9][0-9][0-9][0-9][0-9]")

        lines = []
        groups = []

        ids = []
        for id in self.svg.get_ids():
            ids.append(id)

        # Obtains all mbb in the svg.
        for id in ids:
            texts = []
            figures = []

            # get element by ID and if is a group and it isn't a graph then get all child elements.
            element = self.svg.getElementById(id)
            if(not pattern1.match(element.get_id()) and element.tag_name == 'g'):
                for child in element.descendants():
                    if(child.tag_name == 'text'):
                        texts.append(child.text)
                
                    if(child.tag_name == 'ellipse' or child.tag_name == 'polygon' or child.tag_name == 'path'):
                        figures.append(child.get_id())
                    
            if(not texts and figures):
                # It is a path.
                for figure in figures:
                    figure = self.svg.getElementById(figure)
                    if(figure.tag_name == 'path'):
                        line = figure.get('d')
                        if (line.find('C') != -1):
                            y_o = line[line.find(',') + 1:line.find('C')]
                        else:
                            y_o = line[line.find(',') + 1:line.find(' ')]
                        o = (float(line[line.find('M') + 1:line.find(',')]), float(y_o))  
                        d = (float(line[line.rfind(' ') + 1: line.rfind(',')]), float(line[line.rfind(',') + 1:]))
                        lines.append(path(o,d))
                    else:
                        points = figure.get('points')
                        point = (float(points[0:points.find(',')]), float(points[points.find(',') + 1: points.find(' ')]))
                        lines[-1].change_direction(point)

            elif(texts and figures):
                # It is a element.

                # Information for the element.
                reactions = []
                id_element = ""
                type_element = ""
                enzime = ""
                position = []
                size = 0
                name = ""

                # Obtains the texts inside the element and gets the type of element from it.
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
                    elif(pattern5.match(text)):
                        id_element = text
                    elif(pattern6.match(text)):
                        type_element = 'Compound'
                        name = text
                    else:
                        name = text

                # Obtains the position of the element from the figures that the group contains.
                for figure in figures:
                    figure = self.svg.getElementById(figure)
                    if(figure.tag_name == 'ellipse'):
                        position = (float(figure.get('cx')), float(figure.get('cy')))
                        size = max(format_num(figure.get('rx')), format_num(figure.get('ry')))
                    elif(figure.tag_name == 'polygon'):
                        
                        points = string_to_list(figure.get('points'))

                        # If it is a polygon and filled with the color yellow then it is a elemental reaction.
                        if(figure.get('fill') == 'yellow'):
                            type_element = 'Elemental'   
                            x_A = float(points[0][0])
                            y_A = float(points[0][1])
                            x_B = float(points[4][0])
                            y_B = float(points[4][1])
                            position = ((x_A + x_B) / 2, (y_A + y_B) /2)
                            size = math.sqrt(math.pow((x_A - x_B) / 2, 2) + math.pow((y_A - y_B) / 2, 2))
                        elif(len(points) <= 5):
                            # it is a compound.
                            type_element = 'Compound'
                            x_A = float(points[0][0])
                            y_A = float(points[0][1])
                            x_B = float(points[2][0])
                            y_B = float(points[2][1])
                            x_C = float(points[1][0])
                            position = ((x_A + x_B) / 2, (y_A + y_B) /2)
                            size = abs(x_A - x_C)

                # Proceeds to draw the element.
                if(type_element == 'MBB'):
                    groups.append(add_metabolic_building_block(self, id_element, position[0], position[1], size))
                elif(type_element == 'Reaction'):
                    groups.append(add_reaction(self, id_element, reactions[0], enzime,  position[0], position[1], size))
                elif(type_element == 'Elemental'):
                    groups.append(add_elemental_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size))
                elif(type_element == 'Inverse'):
                    groups.append(add_inverse_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size))
                elif(type_element == 'Compound'):
                    groups.append(add_component(self, name, position[0], position[1], size))

        layer = self.svg.get_current_layer()
        for group in groups:
           layer.add(group)

        for line in lines:
            nearest_orig = ""
            nearest_dest = ""
            distance_orig = float("inf")
            distance_dest = float("inf")

            for group in groups:
                if(is_metabolic_pathway_element(group)):
                    group_center = (float(group.get('x')), float(group.get('y')))

                    distance_o = math.sqrt(math.pow(group_center[0] - line.o[0], 2) + math.pow(group_center[1] - line.o[1], 2))
                    distance_d = math.sqrt(math.pow(group_center[0] - line.d[0], 2) + math.pow(group_center[1] - line.d[1], 2))

                    size_o = get_size(group.get_id(), float(group.get('size')), get_angle_line(line.o, group_center))
                    distance_o = distance_o - math.sqrt(math.pow(size_o[0],2) + math.pow(size_o[1],2))

                    size_d = get_size(group.get_id(), float(group.get('size')), get_angle_line(line.d, group_center))
                    distance_o = distance_o - math.sqrt(math.pow(size_d[0],2) + math.pow(size_d[1],2))

                    if(distance_dest >= distance_d):
                        distance_dest = distance_d
                        nearest_dest = group

                    if(distance_orig >= distance_o):
                        distance_orig = distance_o
                        nearest_orig = group

            if(nearest_dest != "" and nearest_orig != ""):
                add_arrow(self, nearest_orig, nearest_dest, False)
        
        self.svg.getElementById('graph0').delete()
            
if __name__ == '__main__':
    Constructor().run()