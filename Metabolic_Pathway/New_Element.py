from operator import length_hint
from tokenize import group
from wsgiref.util import request_uri
import inkex, re
from inkex import TextElement, PathElement, Rectangle
from re import S

# Font size for all text created by the extension.
font_size = 10

# Returns input value and unit as svg format.
def svg_format(self, value, unit):
    return self.svg.unittouu(str(value) + unit)

# Adds a text label to the given id, location and size.
def add_text(x, y, size, text):
    elem = TextElement(x=str(x), y=str(y))
    elem.text = str(text)
    elem.style = {
        'font-size': size,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal' }
    return elem

# Adds a elipse to the given center position and radius.
def add_elipse(cx, cy, radius, color):
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '0.25px'}
    elem = PathElement.arc((cx, cy), radius)
    elem.style = style
    return elem

# Adds a octogon to the given center position and side.
def add_octogon(cx, cy, radius, color):
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '0.25px'}
    elem = PathElement.star((cx, cy), (radius, radius), 8)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(23, ' + str(cx) + ', ' + str(cy) + ')')
    elem.style = style
    return elem

# Adds a rectangle to the given center position, high and base.
def add_rectangle(cx, cy, base, hight):
    style = {'stroke': 'black', 'fill': 'none', 'stroke-width': '0.25px'}
    elem = Rectangle()
    elem.set('x', cx)
    elem.set('y', cy)
    elem.set('height', base)
    elem.set('width', hight)
    elem.style = style
    return elem

# Generates a new metabolic building block in the current layer.
def add_metabolic_building_block(self, id, x, y, radius):

    # Minimum size of component is 6.
    if(radius < 6):
        radius = 6
    
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    group = inkex.Group(id = id)
    group.add(add_elipse(x, y, radius, 'lightgray'))
    group.add(add_text(x - 4, y - 1, svg_font_size, 'MBB'))
    group.add(add_text(x - len(id), y + 4, svg_font_size, id))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)

# Generates a new reaction in the current layer.
def add_reaction(self, id, reaction, enzime, x, y, radius):

    # Minimum size of component is 9.
    if(radius < 9):
       radius = 9
    
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    reac = inkex.Group(id = id)
    reac.add(add_elipse(x, y, radius, 'yellow'))
    reac.add(add_text(x - len(id), y - 3, svg_font_size, id))
    reac.add(add_text(x - len(reaction) - 2, y + 1, svg_font_size, 'R' + reaction))
    reac.add(add_text(x - len(enzime), y + 5, svg_font_size, enzime))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(reac)

# Generates a new inverse reaction in the current layer.
def add_inverse_reaction(self, id, reaction, enzime, x, y, radius):

    # Minimum size of component is 11.
    if(radius < 11):
        radius = 11
    
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    group = inkex.Group(id = id)
    group.add(add_elipse(x, y, radius, '#c1b2ff'))
    group.add(add_text(x - len(id), y - 3, svg_font_size, id))
    group.add(add_text(x - len(reaction) - 5, y + 1, svg_font_size, 'R' + reaction + '_rev'))
    group.add(add_text(x - len(enzime), y + 5, svg_font_size, enzime))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)

# Generates a new elemental reaction in the current layer.
def add_elemental_reaction(self, id, reaction, enzime, x, y, radius):

    # Minimum radius is 10.
    if(radius < 10):
        radius = 10
    
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    group = inkex.Group(id = id)
    group.add(add_octogon(x, y, radius, 'yellow'))
    group.add(add_octogon(x, y, radius + 1, 'none'))
    group.add(add_text(x - len(id), y - 3, svg_font_size, id))
    group.add(add_text(x - len(reaction) - 2, y + 1, svg_font_size, 'R' + reaction))
    group.add(add_text(x - len(enzime), y + 5, svg_font_size, enzime))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)

# Generates a new component in the current layer.
def add_component(self, component, x, y, size):

    # Minimum size for a component.
    if(size < 13):
        size = 13
    
    # Format of the font size.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group with all the elements inside of it.
    group = inkex.Group()
    group.add(add_rectangle(x - (size/2), y - (size/6), size/3, size))
    group.add(add_text(x - len(component) - 2, y + 1 , svg_font_size, 'C' + component))

    # Gets the current layer and adds the group to it.
    layer = self.svg.get_current_layer()
    layer.add(group)

# Checks if the id is not used in the svg.
def check_unique_id(self, id):

    # Patern that verifies it is a number.
    pattern = re.compile("[0-9]+")

    # Gets all ids in the svg.
    svg_ids = self.svg.get_ids()

    # Iterates through all the ids for a equal id.
    for svg_id in svg_ids:
        if(pattern.match(svg_id) and svg_id == id):
            return False
    return True

class Constructor(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--ID_M', type=str, default='undefined', dest='ID_M', help="ID of element MDAG")
        pars.add_argument('--ID_R', type=str, default='undefined', dest='ID_R', help="ID of element RC")
        pars.add_argument('--KEGG_reaction_M', type=str, default='undefined', dest='KEGG_reaction_M', help="KEGG reaction code MDAG")
        pars.add_argument('--KEGG_reaction_R', type=str, default='undefined', dest='KEGG_reaction_R', help="KEGG reaction code RC")
        pars.add_argument('--KEGG_enzime_M', type=str, default='undefined', dest='KEGG_enzime_M', help="KEGG enzime code MDAG")
        pars.add_argument('--KEGG_enzime_R', type=str, default='undefined', dest='KEGG_enzime_R', help="KEGG enzime code RC")
        pars.add_argument('--type_M', type=str, default='undefined', dest='type_M', help="Type of element MDAG")
        pars.add_argument('--type_R', type=str, default='undefined', dest='type_R', help="Type of element RC")
        pars.add_argument('--tab', type=str, default='undefined', dest='tab', help="Type of Metabolic Pathway")
        pars.add_argument('--x_M', type=int, default='30', dest='x_M', help="Position x of the element MDAG")
        pars.add_argument('--x_R', type=int, default='30', dest='x_R', help="Position x of the element RC")
        pars.add_argument('--y_M', type=int, default='30', dest='y_M', help="Position y of the element MDAG")
        pars.add_argument('--y_R', type=int, default='30', dest='y_R', help="Position y of the element RC")
        pars.add_argument('--size_M', type=int, default='20', dest='size_M', help="Size of the element MDAG")
        pars.add_argument('--size_R', type=int, default='20', dest='size_R', help="Size of the element RC")

    def effect(self):

        if self.options.tab == 'DAG':
            if self.options.type_M == 'Reactions':

                # New reaction for MDAG.
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the reaction.')
                else:
                    if(not check_unique_id(self, self.options.ID_M)):
                        inkex.errormsg('The ID is already in use, please change it to another number.')
                    else:    
                        add_reaction(self, self.options.ID_M, self.options.KEGG_reaction_M, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            elif self.options.type_M == 'Elemental_Reactions':

                # New elemental reaction for MDAG.
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the elemental reaction.')
                else:
                    if(not check_unique_id(self, self.options.ID_M)):
                        inkex.errormsg('The ID is already in use, please change it to another number.')
                    else:   
                        add_elemental_reaction(self, self.options.ID_M, self.options.KEGG_reaction_M, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            else:

                # New metabolic building block for MDAG.
                if(self.options.ID_M == 'undefined'):
                    inkex.errormsg('ID for metabolic building block has not been defined.')
                else:
                    if(not check_unique_id(self, self.options.ID_M)):
                        inkex.errormsg('The ID is already in use, please change it to another number.')
                    else:   
                        add_metabolic_building_block(self, self.options.ID_M, self.options.x_M, self.options.y_M, self.options.size_M)
        else:
            if self.options.type_R == 'Reactions':

                # New reaction for RC.
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the reaction.')
                else:
                    if(not check_unique_id(self, self.options.ID_R)):
                        inkex.errormsg('The ID is already in use, please change it to another number.')
                    else:   
                        add_reaction(self, self.options.ID_R, self.options.KEGG_reaction_R, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)
            elif self.options.type_R == 'Component':

                # New component for RC.
                if (self.options.KEGG_reaction_R == 'undefined'):
                    inkex.errormsg('component code has not been defined for the reaction.')
                else:
                    add_component(self, self.options.KEGG_reaction_R, self.options.x_R, self.options.y_R, self.options.size_R)
            else:
                
                # New inverse reaction for RC.
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the inverse reaction.')
                else:
                    if(not check_unique_id(self, self.options.ID_R)):
                        inkex.errormsg('The ID is already in use, please change it to another number.')
                    else: 
                        add_inverse_reaction(self, self.options.ID_R, self.options.KEGG_reaction_R, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)

if __name__ == '__main__':
    Constructor().run()