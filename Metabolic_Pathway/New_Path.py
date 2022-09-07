import inkex, re
from shared.Add_Arrow import add_arrow
from shared.Boleans import is_metabolic_pathway_element
from shared.Errors import *

class Constructor(inkex.EffectExtension):
    
    # Obtains the arguments in the pop up menu.
    def add_arguments(self, pars):
        pars.add_argument('--direction', type=inkex.Boolean, default='False', dest='Direction', help="placement of the arrow head")

    # Execution of the extension.
    def effect(self):

        # Verifies that only two items are selected and they are elements of a metabolic pathway.
        if(len(self.svg.selection) != 2):
            inkex.errormsg(error_input_size + str(len(self.svg.selection)) + '.')
            return
        
        # Verifies that the two selected elements are from a metabolic pathway.
        for element in self.svg.selection:
            if(not is_metabolic_pathway_element(element.get_id())):
                inkex.errormsg(error_metabolic_element)
                return

        # Obtains the elements from the selections.
        element_A = self.svg.selection[0]
        element_B = self.svg.selection[1]

        # Verifies that there is not another path between these two.
        paths = []
        all_ids = self.svg.get_ids()
        pattern = re.compile("P [0-9]+")
        for id in all_ids:
            if(pattern.match(id)):
                paths.append(id)

        for path_id in paths:
            path = self.svg.getElementById(path_id)
            if(path.get('id_dest') == element_A.get_id() and path.get('id_orig') == element_B.get_id()):
                inkex.errormsg("Path exist between " + element_B.get_id() + " and " + element_A.get_id() + " in this direction.")
                return

        # Draws an arrow between elements.
        add_arrow(self, element_B, element_A, self.options.Direction)

if __name__ == '__main__':
    Constructor().run()