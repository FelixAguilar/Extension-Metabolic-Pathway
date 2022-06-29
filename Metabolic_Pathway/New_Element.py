from operator import length_hint
from wsgiref.util import request_uri
import inkex
from inkex import TextElement, PathElement
from re import S

font_size = 10

# returns value as svg format.
def svg_format(self, value, unit):
    return self.svg.unittouu(str(value) + unit)

# Adds a text label to the given id, location and size.
def add_text(id, x, y, size, text):
    elem = TextElement(x=str(x), y=str(y), id=id)
    elem.text = str(text)
    elem.style = {
        'font-size': size,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal' }
    return elem

# Adds a elipse to the given center position and radius.
def add_elipse(cx, cy, r, color):
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '0.25px'}
    elem = PathElement.arc((cx, cy), r)
    elem.style = style
    return elem

# Adds a hexagon to the given center position and side.

# Adds a rectangle to the given center position, high and base.

# Generates a new metabolic building block in the current layer.
def add_metabolic_building_block(self, id, x, y, radius):

    # Minimum size of component is 20.
    if(radius < 20):
        radius = 20
    
    # Change variables to svg format.
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, radius, 'pt')
    svg_s = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    mbb = inkex.Group()
    mbb.add(add_elipse(svg_x, svg_y, svg_r, 'lightgray'))
    mbb.add(add_text("mbb" + id, svg_x - 4, svg_y - 1, svg_s, 'MBB'))
    mbb.add(add_text("id" + id, svg_x - len(id), svg_y + 4, svg_s, id))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(mbb)

# Generates a new reaction in the current layer.
def add_reaction(self, id, reaction, enzime, x, y, radius):

    # Minimum size of component is 25.
    if(radius < 25):
        radius = 25
    
    # Change variables to svg format.
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, radius, 'pt')
    svg_s = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    reac = inkex.Group()
    reac.add(add_elipse(svg_x, svg_y, svg_r, 'yellow'))
    reac.add(add_text('id' + id, svg_x - len(id), svg_y - 3, svg_s, id))
    reac.add(add_text('reaction' + id, svg_x - len(reaction) - 1, svg_y + 1, svg_s, 'R' + reaction))
    reac.add(add_text("enzime" + id, svg_x - len(enzime), svg_y + 5, svg_s, enzime))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(reac)

# Generates a new inverse reaction in the current layer.
def add_inverse_reaction(self, id, reaction, enzime, x, y, radius):

    # Minimum size of component is 32.
    if(radius < 32):
        radius = 32
    
    # Change variables to svg format.
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, radius, 'pt')
    svg_s = svg_format(self, font_size, 'pt')

    # Creates a group and adds all components to it.
    reac = inkex.Group()
    reac.add(add_elipse(svg_x, svg_y, svg_r, '#c1b2ff'))
    reac.add(add_text('id' + id, svg_x - len(id), svg_y - 3, svg_s, id))
    reac.add(add_text('reaction' + id, svg_x - len(reaction) - 5, svg_y + 1, svg_s, 'R' + reaction + '_rev'))
    reac.add(add_text("enzime" + id, svg_x - len(enzime), svg_y + 5, svg_s, enzime))

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(reac)

def add_elemental_reaction(self, id, reaction, enzime, x, y, r):
    if(r < 25):
        r = 25
    
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, r, 'pt')
    svg_s = svg_format(self, font_size, 'pt')

    layer = self.svg.get_current_layer()

    reac = inkex.Group()
    reac.add(add_elipse(svg_x, svg_y, svg_r, 'yellow'))
    reac.add(add_text('id' + id, svg_x - len(id), svg_y - 3, svg_s, id))
    reac.add(add_text('reaction' + id, svg_x - len(reaction) - 1, svg_y + 1, svg_s, 'R' + reaction))
    reac.add(add_text("enzime" + id, svg_x - len(enzime), svg_y + 5, svg_s, enzime))
    layer.add(reac)

def add_component(self, component, x, y, r):
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, r, 'pt')
    svg_s = svg_format(self, font_size, 'pt')

    layer = self.svg.get_current_layer()

    reac = inkex.Group()
    reac.add(add_elipse(svg_x, svg_y, svg_r, 'yellow'))
    reac.add(add_text('component' + component, svg_x - len(id), svg_y - 3, svg_s, 'C' + component))
    layer.add(reac)


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
                    add_reaction(self, self.options.ID_M, self.options.KEGG_reaction_M, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            elif self.options.type_M == 'Elemental_Reactions':

                # New elemental reaction for MDAG.
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the elemental reaction.')
                else:
                    add_elemental_reaction(self, self.options.ID_M, self.options.KEGG_reaction_M, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            else:

                # New metabolic building block for MDAG.
                if(self.options.ID_M == 'undefined'):
                    inkex.errormsg('ID for metabolic building block has not been defined.')
                else:
                    add_metabolic_building_block(self, self.options.ID_M, self.options.x_M, self.options.y_M, self.options.size_M)
        else:
            if self.options.type_R == 'Reactions':

                # New reaction for RC.
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg('ID, reaction or enzime code has not been defined for the reaction.')
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
                    add_inverse_reaction(self, self.options.ID_R, self.options.KEGG_reaction_R, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)

if __name__ == '__main__':
    Constructor().run()