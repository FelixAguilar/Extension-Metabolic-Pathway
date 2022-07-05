from operator import length_hint
from tokenize import group
from wsgiref.util import request_uri
import inkex, re
from inkex import PathElement, BaseElement
from re import S
from math import atan2, sin, cos, pi

def is_metabolic_pathway_element(svg_element):
    pattern = re.compile("[E|M|C|R] [0-9]+")
    if(pattern.match(svg_element.get_id())):
            return True
    return False

def add_line(x1, y1, x2, y2):
    line = inkex.PathElement()
    line.style = {'stroke': 'black', 'stroke-width': '0.25px', 'fill': 'none'}
    line.path = 'M {},{} L {},{}'.format(x1, y1, x2, y2)
    #line.label = name
    return line

def add_triangle(cx, cy, rotation):
    style = {'stroke': 'black', 'fill': 'black', 'stroke-width': '0.25px'}
    elem = PathElement.star((cx, cy), (1, 1), 3)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(' + str(rotation) + ', ' + str(cx) + ', ' + str(cy) + ')')
    elem.style = style
    return elem

def get_angle_line(ox, oy, dx, dy):
    x_delta = dx - ox
    y_delta = dy - oy
    return atan2(y_delta, x_delta) * 180 / pi

def add_straight_arrow(self, o_id, d_id, ox, oy, dx, dy):

    # Calculate the angle of the arrow to the horizontal axis.
    angle = get_angle_line(ox, oy, dx, dy)

    # Triangle half height (sides are 1) and splited into x and y.
    height = 0.433
    x_height = height * sin(angle * 180 / pi)
    y_height = height * cos(angle * 180 / pi)
    
    # Creates the group and adds the elements depending on the direction.
    group = inkex.Group()
    group.add(add_line(ox - x_height, oy - y_height, dx, dy))
    group.add(add_triangle(dx - x_height, dy - y_height, angle))
    group.set('id_orig', d_id)
    group.set('id_dest', o_id)
        
    # Adds the group to the layer and assigns a unique id.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'P ')
    
class Constructor(inkex.EffectExtension):
    
    def add_arguments(self, pars):
        pars.add_argument('--direction', type=bool, default='False', dest='Direction', help="placement of the arrow head")

    def effect(self):

        # Verifies that only two items are selected and they are elements of a metabolic pathway.
        if(len(self.svg.selection) != 2):
            inkex.errormsg('To create a path there must be two elements selected. There are currently ' + str(len(self.svg.selection)) + ' items selected.')
            return
        
        # Verifies that the two selected elements are from a metabolic pathway.
        for element in self.svg.selection:
            if(not is_metabolic_pathway_element(element)):
                inkex.errormsg('The selected elements do not belong to a metabolic pathway or it is a pathway of it.')
                return

        # Creates a path between them.
        element_A = self.svg.selection[0]
        element_B = self.svg.selection[1]

        if(self.options.Direction):
            x_d = float(element_A.get('x'))
            y_d = float(element_A.get('y'))
            s_d = float(element_A.get('size'))
            id_d = element_A.get_id()

            x_o = float(element_B.get('x'))
            y_o = float(element_B.get('y'))
            s_o = float(element_B.get('size'))
            id_o = element_B.get_id()
        else:
            x_o = float(element_A.get('x'))
            y_o = float(element_A.get('y'))
            s_o = float(element_A.get('size'))
            id_o = element_A.get_id()

            x_d = float(element_B.get('x'))
            y_d = float(element_B.get('y'))
            s_d = float(element_B.get('size'))
            id_d = element_B.get_id()
        
        angle = get_angle_line(x_o, y_o, x_d, y_d)
        x_s_o = s_o * sin(angle)
        y_s_o = s_o * cos(angle)
        x_s_d = s_d * sin(angle)
        y_s_d = s_d * cos(angle)

        if(x_o < x_d):
            x_o += x_s_o
            x_d -= x_s_d
        else:
            x_o -= x_s_o
            x_d += x_s_d
        if(y_o < y_d):
            y_o += y_s_o
            y_d -= y_s_d
        else:
            y_o -= y_s_o
            y_d += y_s_d

        add_straight_arrow(self, id_o, id_d, x_o, y_o, x_d, y_d)
       
        

if __name__ == '__main__':
    Constructor().run()