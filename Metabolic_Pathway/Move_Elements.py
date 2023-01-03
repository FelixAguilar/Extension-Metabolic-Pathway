import inkex
from operator import contains
from shared.Arrow import add_arrow_image
from shared.Boleans import is_path, is_metabolic_pathway_element, is_image
from shared.Errors import *

def redraw_paths(self, paths) -> None:
    for path in paths:
        add_arrow_image(self, self.svg.getElementById(path.get('id_orig')), self.svg.getElementById(path.get('id_dest')))
        path.delete()

class Constructor(inkex.EffectExtension):
    
    #def add_arguments(self, pars):
    
    def effect(self):

        # Verifies that at least one item is selected.
        if(len(self.svg.selection) < 1):
            inkex.errormsg(error_move_path)
            return

        # Obteins all the elements selected.
        def check_element(element) -> bool: return is_metabolic_pathway_element(element.get_id()) or is_image(element.tag_name)
        elements = list(filter(check_element, self.svg.selection))

        # If there is elements selected, it works as intended, if there is no 
        # elements selected and all are paths then they are drawed again.
        if(elements):

            # Obteins all the path ids in the svg.
            paths = list(filter(is_path, self.svg.get_ids()))

            # Obtains all the paths that connects the selected elements between them and with the rest of the svg.
            inter_paths = []
            for path_id in paths:
                path = self.svg.getElementById(path_id)
                for element in elements:
                    element_id = element.get_id()
                    if(not contains(inter_paths, path) and (path.get('id_dest') == element_id or (path.get('id_orig') == element_id))):
                        inter_paths.append(path)

            # For the path list between the selection and the rest redraw the line and deletes the old one.
            redraw_paths(self, inter_paths)

        else:

            # Obteins all the path in the selection.
            def check_path(path) -> bool: return is_path(path.get_id())
            paths = list(filter(check_path, self.svg.selection))

            # Redraws paths.
            if(paths):
                redraw_paths(self, paths)
            else:
                inkex.errormsg(error_move_path)


if __name__ == '__main__':
    Constructor().run()