import inkex, re, Add_Arrow
from re import S, T
from Add_Arrow import add_arrow

# Checks is the element given is a metabolic path way.
def is_metabolic_pathway_element(svg_element):
    pattern = re.compile("[E|M|C|R] [0-9]+")
    if(pattern.match(svg_element.get_id())):
            return True
    return False


class Constructor(inkex.EffectExtension):
    
    # Obtains the arguments in the pop up menu.
    def add_arguments(self, pars):
        pars.add_argument('--direction', type=inkex.Boolean, default='False', dest='Direction', help="placement of the arrow head")

    # Execution of the extension.
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

        # Verifies that there is not another path between these two.
        """ a hacer """

        # Obtains the elements from the selections.
        element_A = self.svg.selection[0]
        element_B = self.svg.selection[1]

        # Draws an arrow between elements.
        add_arrow(self, element_B, element_A, self.options.Direction)

if __name__ == '__main__':
    Constructor().run()