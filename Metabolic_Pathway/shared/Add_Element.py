from typing import Any
import inkex
from inkex import TextElement, PathElement, Rectangle, BaseElement

# Font size for all text created by the extension.
font_size: float = 10

# Adds a text label to the given location.
def add_text(x: float, y: float, text: str) -> Any:
    elem = TextElement(x=str(x), y=str(y))
    elem.text = str(text)
    elem.style = {
        'font-size': font_size,
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal' }
    return elem

# Adds a line between the two given points.
def add_line(origin: tuple[float, float], destination: tuple[float, float]) -> Any:
    elem = inkex.PathElement()
    elem.style = {'stroke': 'black', 'stroke-width': '1px', 'fill': 'none'}
    elem.path = 'M {},{} L {},{}'.format(origin[0], origin[1], destination[0], destination[1])
    return elem

# Adds a triangle of defined size with the center in the given position, and rotation given.
def add_triangle(center: tuple[float, float], rotation: float) -> Any:
    style = {'stroke': 'black', 'fill': 'black', 'stroke-width': '1px'}
    elem = PathElement.star(center, (3, 3), 3)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(' + str(rotation) + ', ' + str(center[0]) + ', ' + str(center[1]) + ')')
    elem.style = style
    return elem

# Adds a elipse to the given center position and radius.
def add_elipse(cx: float, cy: float, radius: float, color: str) -> Any:
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '1px'}
    elem = PathElement.arc((cx, cy), radius)
    elem.style = style
    return elem

# Adds a octogon to the given center position and side.
def add_octogon(cx: float, cy: float, radius: float, color: str) -> Any:
    style = {'stroke': 'black', 'fill': color, 'stroke-width': '1px'}
    elem = PathElement.star((cx, cy), (radius, radius), 8)
    elem.set('sodipodi:arg1', 0)
    elem.set('sodipodi:arg2', 0)
    elem.set('transform', 'rotate(23, ' + str(cx) + ', ' + str(cy) + ')')
    elem.style = style
    return elem

# Adds a rectangle to the given center position, high and base.
def add_rectangle(cx: float, cy: float, base: float, hight: float) -> Any:
    style = {'stroke': 'black', 'fill': 'none', 'stroke-width': '1px'}
    elem = Rectangle()
    elem.set('x', cx)
    elem.set('y', cy)
    elem.set('height', base)
    elem.set('width', hight)
    elem.style = style
    return elem

# Generates a new metabolic building block in the current layer.
def add_metabolic_building_block(self: Any, id: str, x: float, y: float, radius: float) -> Any:
    
    # Change font size format to svg.
    size_y = font_size
    size_x = font_size/3

    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_elipse(x, y, radius, 'lightgray'))
    group.add(add_text(x - len('MBB') * size_x, y, 'MBB'))
    group.add(add_text(x - len(id) * size_x, y + size_y, id))

    # Values for the group.
    group.set('code', id)
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'M ')
    return group

# Generates a new reaction in the current layer.
def add_reaction(self: Any, id: str, reactions: list[str], enzime: str, x: float, y: float, radius: float) -> Any:

    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_elipse(x, y, radius, 'yellow'))
 
    # Change font size format to svg.
    lines = 2 + len(reactions)
    size_x = font_size/3
    size_y = font_size
    index = 1 - lines / 2

    group.add(add_text(x - len(id) * size_x, y + (index * size_y), id))
    index = index + 1
    for reaction in reactions:
        group.add(add_text(x - len(reaction) * size_x, y + (index * size_y), reaction))
        index = index + 1
    group.add(add_text(x - len(enzime) * size_x + 4, y + (index * size_y), enzime))

    # Values for the group.
    group.set('code', id)
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'R ')

    return group

# Generates a new inverse reaction in the current layer.
def add_inverse_reaction(self: Any, id: str, reactions: list[str], enzime: str, x: float, y: float, radius: float) -> Any:

    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_elipse(x, y, radius, '#c1b2ff'))
    
    # Change font size format to svg.
    lines = 2 + len(reactions)
    size_x = font_size/3
    size_y = font_size
    index = 1 - lines / 2

    group.add(add_text(x - len(id) * size_x, y + (index * size_y), id))
    index = index + 1
    for reaction in reactions:
        group.add(add_text(x - len(reaction) * size_x, y + (index * size_y), reaction))
        index = index + 1
    group.add(add_text(x - len(enzime) * size_x + 4, y + (index * size_y), enzime))

    # Values for the group.
    group.set('code', id)
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'I ')
    return group

# Generates a new elemental reaction in the current layer.
def add_elemental_reaction(self: Any, id: str, reactions: list[str], enzime: str, x: float, y: float, radius: float) -> Any:
    
    # Creates a group and adds all components to it.
    group = inkex.Group()
    group.add(add_octogon(x, y, radius, 'yellow'))
    group.add(add_octogon(x, y, radius + 4, 'none'))

    # Change font size format to svg.
    lines = 2 + len(reactions)
    size_x = font_size/3
    size_y = font_size
    index = 1 - lines / 2

    group.add(add_text(x - len(id) * size_x, y + (index * size_y), id))
    index = index + 1
    for reaction in reactions:
        group.add(add_text(x - len(reaction) * size_x, y + (index * size_y), reaction))
        index = index + 1
    group.add(add_text(x - len(enzime) * size_x + 4, y + (index * size_y), enzime))

    # Values for the group.
    group.set('code', id)
    group.set('x', x)
    group.set('y', y)
    group.set('size', radius)

    # Adds it to the current layer.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'E ')
    return group

# Generates a new component in the current layer.
def add_component(self: Any, component: str, x: float, y: float, size: float) -> Any:

    # Creates a group with all the elements inside of it.
    group = inkex.Group()
    group.add(add_rectangle(x - size/2, y - ((font_size + 2)/2), (font_size + 2), size))
    group.add(add_text(x - ((len(component)*(font_size/2))/2), y + (font_size/2) - 1, component))

    # Values for the group.
    group.set('x', x)
    group.set('y', y)
    group.set('size', size)

    # Gets the current layer and adds the group to it.
    layer = self.svg.get_current_layer()
    layer.add(group)
    BaseElement.set_random_id(group, prefix = 'C ')

    return group
