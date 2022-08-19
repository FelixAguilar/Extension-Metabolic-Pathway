import inkex, math
from inkex import TextElement, PathElement, Rectangle, BaseElement

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
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '1px'}
    elem = PathElement.arc((cx, cy), radius)
    elem.style = style
    return elem

# Adds a octogon to the given center position and side.
def add_octogon(cx, cy, radius, color):
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '1px'}
    elem = PathElement.star((cx, cy), (radius, radius), 8)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(23, ' + str(cx) + ', ' + str(cy) + ')')
    elem.style = style
    return elem

# Adds a rectangle to the given center position, high and base.
def add_rectangle(cx, cy, base, hight):
    style = {'stroke': 'black', 'fill': 'none', 'stroke-width': '1px'}
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
    size_y = font_size
    size_x = font_size/3

    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_elipse(x, y, radius, 'lightgray'))
    group.add(add_text(x - len('MBB') * size_x, y, svg_font_size, 'MBB'))
    group.add(add_text(x - len(id) * size_x, y + size_y, svg_font_size, id))

    # Values for the group.
    group.set('id', 'M ' + str(id))
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    return group

# Generates a new reaction in the current layer.
def add_reaction(self, id, reactions, enzime, x, y, radius, unique = True, g_id = None):

    # Creates a group and adds all components to it.
    group = inkex.Group(id = id)
    group.add(add_elipse(x, y, radius, 'yellow'))

        
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')
    lines = 2 + len(reactions)
    size_x = font_size/3
    size_y = font_size
    index = 1 - lines / 2

    group.add(add_text(x - len(id) * size_x, y + (index * size_y), svg_font_size, id))
    index = index + 1
    for reaction in reactions:
        group.add(add_text(x - len(reaction) * size_x, y + (index * size_y), svg_font_size, reaction))
        index = index + 1
    group.add(add_text(x - len(enzime) * size_x + 4, y + (index * size_y), svg_font_size, enzime))

    # Values for the group.
    if(unique and g_id == None):
        group.set('id', 'R ' + str(id))
    if(g_id != None):
        group.set('id', 'R ' + str(g_id))
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    if(not unique):
        BaseElement.set_random_id(group, prefix = 'R ')
    return group


# Generates a new inverse reaction in the current layer.
def add_inverse_reaction(self, id, reaction, enzime, x, y, radius, unique = True, g_id = None):

    # Minimum size of component is 11.
    if(radius < 11):
        radius = 11

    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_elipse(x, y, radius, '#c1b2ff'))
    
    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')
    size_y = font_size
    size_x = font_size/3
    group.add(add_text(x - len(id) * size_x, y - size_y, svg_font_size, id))
    group.add(add_text(x - len(reaction) * size_x, y , svg_font_size, reaction))
    group.add(add_text(x - len(enzime) * size_x + 4, y + size_y, svg_font_size, enzime))

    # Values for the group.
    if(unique and g_id == None):
        group.set('id', 'I ' + str(id))
    if(g_id != None):
        group.set('id', 'I ' + str(g_id))
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    if(not unique):
        BaseElement.set_random_id(group, prefix = 'I ')
    return group


# Generates a new elemental reaction in the current layer.
def add_elemental_reaction(self, id, reaction, enzime, x, y, radius):
    
    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_octogon(x, y, radius, 'yellow'))
    group.add(add_octogon(x, y, radius + 4, 'none'))

    # Change font size format to svg.
    svg_font_size = svg_format(self, font_size, 'pt')
    size_y = font_size
    size_x = font_size/3
    group.add(add_text(x - len(id) * size_x, y - size_y, svg_font_size, id))
    group.add(add_text(x - len(reaction) * size_x, y , svg_font_size, reaction))
    group.add(add_text(x - len(enzime) * size_x + 4, y + size_y, svg_font_size, enzime))

    # Values for the group.
    group.set('id', 'E ' + str(id))
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    return group


# Generates a new component in the current layer.
def add_component(self, component, x, y, size, id = None):

    # Minimum size for a component.
    if(size < 13):
        size = 13
    
    # Format of the font size.
    svg_font_size = svg_format(self, font_size, 'pt')

    # Creates a group with all the elements inside of it.
    group = inkex.Group()
    group.add(add_rectangle(x - size/2, y - ((font_size + 2)/2), (font_size + 2), size))
    group.add(add_text(x - ((len(component)*(font_size/2))/2), y + (font_size/2) - 1 , svg_font_size, component))

    # Values for the group.
    if(id != None):
        group.set('id', 'C ' + str(id))
    group.set('x', x)
    group.set('y', y)
    group.set('size', size)

    """ (font_size/1.5) * len(component) + 2"""
    """(font_size/1.5) * len(component) + 2"""

    # Gets the current layer and adds the group to it.
    layer = self.svg.get_current_layer()
    layer.add(group)

    if(id == None):
        BaseElement.set_random_id(group, prefix = 'C ')

    return group
