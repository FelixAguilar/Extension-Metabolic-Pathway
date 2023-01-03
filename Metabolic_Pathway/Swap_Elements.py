import inkex
from operator import contains
from shared.Arrow import add_arrow_image
from shared.Boleans import is_path, is_metabolic_pathway_element, is_image
from shared.Errors import *

class Constructor(inkex.EffectExtension):
    
    #def add_arguments(self, pars):
    
    def effect(self):

        # Verifies that at least two items are selected and they are a image and a element.
        if(len(self.svg.selection) != 2):
            inkex.errormsg(error_selection_size)
            return

        image = -1
        element = -1
        for component in self.svg.selection:
            if(is_image(component.tag_name)):
                image = component
            elif(is_metabolic_pathway_element(component.get_id())):
                element = component

        if(image != -1 and element != -1):
            # Obteins all the path in the svg.
            paths = list(filter(is_path, self.svg.get_ids()))

            element_id = element.get_id()
            swap_paths = []
            for path_id in paths:
                path = self.svg.getElementById(path_id)
                if(path.get('id_dest') == element_id or path.get('id_orig') == element_id):
                    swap_paths.append(path)

            # Redraws paths.
            if(swap_paths):
                for path in swap_paths:
                    if (path.get('id_orig') == element_id):
                        add_arrow_image(self, image, self.svg.getElementById(path.get('id_dest')))
                    elif (path.get('id_dest') == element_id):
                        add_arrow_image(self, self.svg.getElementById(path.get('id_orig')), image)
                    path.delete()
            element.delete()
        else:
            inkex.errormsg(error_selection_size)

if __name__ == '__main__':
    Constructor().run()