from operator import length_hint
from tokenize import group
from wsgiref.util import request_uri
import inkex, re
from inkex import PathElement, BaseElement
from re import S, T
from math import atan2, sin, cos, pi

def is_metabolic_pathway_element(svg_element):
    pattern = re.compile("[E|M|C|R] [0-9]+")
    if(pattern.match(svg_element.get_id())):
            return True
    return False

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

def add_straight_arrow(self, o_id, d_id, ox, oy, dx, dy, dir):

    # Calculate the angle of the arrow to the horizontal axis.
    angle = get_angle_line(ox, oy, dx, dy)

    # Triangle height (sides are 1) and splited into x and y.
    height = 1.2
    x_height = height * cos(angle * (pi / 180))
    y_height = height * sin(angle * (pi / 180))
    
    # Creates the group and adds the elements depending on the direction.
    group = inkex.Group()
    group.add(add_line(ox, oy, dx, dy))
    if(dir == True):
        group.add(add_triangle(dx - x_height, dy - y_height, angle))
        group.set('id_dest', d_id)
        group.set('id_orig', o_id)
    else:
        group.add(add_triangle(ox + x_height, oy + y_height, angle + 180))
        group.set('id_orig', d_id)
        group.set('id_dest', o_id)
        
    # Adds the group to the layer and assigns a unique id.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'P ')
    
class Constructor(inkex.EffectExtension):
    
    def add_arguments(self, pars):
        pars.add_argument('--direction', type=inkex.Boolean, default='False', dest='Direction', help="placement of the arrow head")

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

        # Obtains the elements.
        element_A = self.svg.selection[0]
        element_B = self.svg.selection[1]

        # Obtains the properties of the elements.
        xd = float(element_A.get('x'))
        yd = float(element_A.get('y'))
        sd = float(element_A.get('size'))
        idd = element_A.get_id()

        xo = float(element_B.get('x'))
        yo = float(element_B.get('y'))
        so = float(element_B.get('size'))
        ido = element_B.get_id()

        # Gets the transformations of the elements if there are, and applies them.
        t = get_transformation(element_A)
        xd = xd + t[0]
        yd = yd + t[1]
        t = get_transformation(element_B)
        xo = xo + t[0]
        yo = yo + t[1]

        #The next section is only for circles.

        # Gets the angle of the line between the two elements.
        angle = get_angle_line(xo, yo, xd, yd)

        # Gets the size of the element splitted into coordinates.
        sox = so * cos(angle * (pi / 180))
        soy = so * sin(angle * (pi / 180))
        sdx = sd * cos(angle * (pi / 180))
        sdy = sd * sin(angle * (pi / 180))

        # Eliminates the line inside the element.
        xo = xo + sox
        yo = yo + soy
        xd = xd - sdx
        yd = yd - sdy

        # Adds the arrow, this one doesn't take into account the elements in his path.
        add_straight_arrow(self, ido, idd, xo, yo, xd, yd, self.options.Direction)

if __name__ == '__main__':
    Constructor().run()