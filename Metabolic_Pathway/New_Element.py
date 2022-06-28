from operator import length_hint
from wsgiref.util import request_uri
import inkex
from inkex import TextElement, PathElement
from re import S
from math import pi

# returns value as svg format.
def svg_format(self, value, unit):
    return self.svg.unittouu(str(value) + unit)

# Adds a text label to the given location and size.
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

def add_elipse(cx, cy, r):
    style = {'stroke': 'black', 'fill': 'lightgrey', 'stroke-width': '1px'}
    elem = PathElement.arc((cx, cy), r)
    elem.style = style
    return elem


# creates new reaction.
def add_reaction(self):
    x = 40
    y = x
    size = 10

    # values to SVG format.
    layer = self.svg.get_current_layer()
    svg_size = svg_format(self , size, 'pt')
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')

    layer.add(add_text(svg_x, svg_y, svg_size, self.options.ID))
    y += 15
    svg_y = svg_format(self, y, 'px')
    layer.add(add_text(svg_x, svg_y, svg_size, self.options.KEGG_reaction))
    y += 15
    svg_y = svg_format(self, y, 'px')
    layer.add(add_text(svg_x, svg_y, svg_size, self.options.KEGG_enzime))

def add_metabolic_building_block(self):

    id = self.options.ID_M
    x = 40
    y = 40
    r = 25
    s = 10
    
    svg_x = svg_format(self, x, 'px')
    svg_y = svg_format(self, y, 'px')
    svg_r = svg_format(self, r, 'pt')
    svg_s = svg_format(self, s, 'pt')

    layer = self.svg.get_current_layer()

    mbb = inkex.Group()
    mbb.add(add_elipse(svg_x, svg_y, svg_r))
    mbb.add(add_text("mbb" + id, svg_x - 4, svg_y, svg_s, 'MBB'))
    mbb.add(add_text("id" + id, svg_x - len(id), svg_y + 5, svg_s, id))

    layer.add(mbb)

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

    def effect(self):
        if self.options.tab == 'DAG':
            if self.options.type_M == 'Reactions':
                add_reaction(self)
            elif self.options.type_M == 'Elemental_Reactions':
                name = 'DAG Elemental Reactions'
            else:
                if(self.options.ID_M == 'undefined'):
                    inkex.errormsg('ID for metabolic building block has not been defined.')
                else:
                    add_metabolic_building_block(self)
        else:
            if self.options.type_R == 'Reactions':
                add_reaction(self)
            elif self.options.type_R == 'Component':
                name = 'RC Component'
            else:
                name = 'RC inverse Reactions'

if __name__ == '__main__':
    Constructor().run()