from re import S
import inkex
from inkex import TextElement

# Adds a text label to the given location and size.
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

def svg_format(self, value, unit):
    return self.svg.unittouu(str(value) + unit)

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

class Constructor(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--ID', type=str, default='Inkscape', dest='ID', help="name input")
        pars.add_argument('--KEGG_reaction', type=str, default='Inkscape', dest='KEGG_reaction', help="name input")
        pars.add_argument('--KEGG_enzime', type=str, default='Inkscape', dest='KEGG_enzime', help="name input")
        pars.add_argument('--type_M', type=str, default='Inkscape', dest='type_M', help="name input")
        pars.add_argument('--type_R', type=str, default='Inkscape', dest='type_R', help="name input")
        pars.add_argument('--tab', type=str, default='Inkscape', dest='tab', help="name input")

    def effect(self):
        if self.options.tab == 'DAG':
            if self.options.type_M == 'Reactions':
                add_reaction(self)
            elif self.options.type_M == 'Elemental_Reactions':
                name = 'DAG Elemental Reactions'
            else:
                name = 'DAG Metabolic Building Block'
        else:
            if self.options.type_R == 'Reactions':
                add_reaction(self)
            elif self.options.type_R == 'Component':
                name = 'RC Component'
            else:
                name = 'RC inverse Reactions'

if __name__ == '__main__':
    Constructor().run()