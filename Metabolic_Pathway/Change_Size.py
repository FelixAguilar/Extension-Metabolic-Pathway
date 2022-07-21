import inkex, re, Add_Element, Move_Arrows
from re import S, T
from Add_Element import add_component, add_elemental_reaction, add_inverse_reaction, add_reaction, add_metabolic_building_block
from Move_Arrows import move_arrows

# Checks is the element given is a metabolic path way.
def is_metabolic_pathway_element(svg_element):
    pattern = re.compile("[E|I|M|C|R] [0-9]+")
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

class Constructor(inkex.EffectExtension):
    
    def add_arguments(self, pars):
        pars.add_argument('--size', type=int, default='0', dest='difference', help="Size change to the selected element.")
        
    def effect(self):

        # Size diference should be different of zero.
        if(self.options.difference == 0):
            return

        # Verifies that only one item is selected.
        if(len(self.svg.selection) != 1):
            inkex.errormsg('To change size there must be one elements selected. There are currently ' + str(len(self.svg.selection)) + ' items selected.')
            return

        # Verifies that the selected element is from a metabolic pathway.
        if(not is_metabolic_pathway_element(self.svg.selection[0])):
            inkex.errormsg('The selected element does not belong to a metabolic pathway or it is a pathway of it.')
            return

        # Obtains the element and extracts the data.
        element = self.svg.selection[0]
        position = (float(element.get('x')), float(element.get('y')))
        transform = get_transformation(element)
        size = int(element.get('size'))
        id = element.get_id()

        # Obtains the current position and size for the element.
        x = position[0] + transform[0]
        y = position[1] + transform[1]
        size = size + self.options.difference

        # Extracts the text of the element and formats it for next use.
        texts = []
        childs = element.descendants()
        for child in childs:
            if(child.get_id().find('text') != -1):
                pattern1 = re.compile("[E|I|M|C|R][0-9]+")
                pattern2 = re.compile("R[0-9]+_rev")
                if(pattern2.match(child.text)):
                    text = child.text[1:-4]
                    texts.append(text)
                elif(pattern1.match(child.text)):
                    text = child.text[1:]
                    texts.append(text)
                else:    
                    texts.append(child.text)

        # Deletes the element.
        element.delete()

        # Creates the element.
        if(id.find('R') != -1):
            add_reaction(self, texts[0], texts[1], texts[2], x, y, size)
        elif(id.find('E') != -1):
            add_elemental_reaction(self, texts[0], texts[1], texts[2], x, y, size)
        elif(id.find('M') != -1):
            add_metabolic_building_block(self,  texts[0], x, y, size)
        elif(id.find('I') != -1):
            add_inverse_reaction(self, texts[0], texts[1], texts[2], x, y, size)
        elif(id.find('C') != -1):
            id = id[2:]
            add_component(self, texts[0], x, y, size, id)

        # Restructures the arrows for this element.
        move_arrows(self)

if __name__ == '__main__':
    Constructor().run()