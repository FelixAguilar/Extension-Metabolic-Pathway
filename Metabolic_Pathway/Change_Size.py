import inkex
from shared.Element import add_component, add_elemental_reaction, add_inverse_reaction, add_reaction, add_metabolic_building_block
from shared.Boleans import is_metabolic_pathway_element, check_format_reaction, check_format_enzime, is_path
from shared.Geometry import get_transformation
from shared.Arrow import add_arrow
from shared.Errors import *

class Constructor(inkex.EffectExtension):
    
    def add_arguments(self, pars):
        pars.add_argument('--size', type=int, default='0', dest='difference', help="Size change to the selected element.")
        
    def effect(self):

        # Size diference should be different of zero.
        if(self.options.difference == 0):
            return

        # Verifies that at least there is one item selected.
        if(len(self.svg.selection) < 1):
            inkex.errormsg(error_size_element)
            return

        # Filters the selection so they are only elements from a metabolic pathway.
        def check_element(element) -> bool: return is_metabolic_pathway_element(element.get_id())
        elements = list(filter(check_element, self.svg.selection))

        if(not elements):
            inkex.errormsg(error_size_element)
            return

        new_element_ids = []
        old_element_ids = []

        for element in elements:
            
            # Obtains the element and extracts the data.
            id = element.get_id()
            transform = get_transformation(element)
            position = (float(element.get('x')), float(element.get('y')))
            size = float(element.get('size'))
        
            # Obtains the current position and size for the element.
            x = position[0] + transform[0]
            y = position[1] + transform[1]
            size = size + self.options.difference

            if(size <= 0):
                inkex.errormsg(error_negative_size_1 + id + error_negative_size_2)
            else:
                if(id.find('C') == -1):
                    # Extracts the text of the element and formats it for next use.
                    code = element.get('code')
                    reactions = []
                    enzime = ""

                    childs = element.descendants()
                    for child in childs:
                        if(child.tag_name == 'text'):
                            if(check_format_reaction(child.text)):
                                reactions.append(child.text)
                            elif(check_format_enzime(child.text)):
                                enzime = child.text
                else:
                    childs = element.descendants()
                    for child in childs:
                        if(child.tag_name == 'text'):
                            code = child.text
                    
                # Deletes the element.
                element.delete()

                # Creates the element.
                if(id.find('R') != -1): group = add_reaction(self, code, reactions, enzime, x, y, size)
                elif(id.find('E') != -1): group =add_elemental_reaction(self, code, reactions, enzime, x, y, size)
                elif(id.find('M') != -1): group = add_metabolic_building_block(self,  code, x, y, size)
                elif(id.find('I') != -1): group = add_inverse_reaction(self, code, reactions, enzime, x, y, size)
                elif(id.find('C') != -1): group = add_component(self, code, x, y, size)
                
                old_element_ids.append(id)
                new_element_ids.append(group.get_id())

        # Filters the svg elements so there are only paths.
        paths = list(filter(is_path, self.svg.get_ids()))

        inter_path = []
        for path_id in paths:
            change = False
            path = self.svg.getElementById(path_id)
            
            for old_id, new_id in zip(old_element_ids, new_element_ids):
                if(path.get('id_dest') == old_id):
                    path.set('id_dest', new_id)
                    change = True
                if(path.get('id_orig') == old_id):
                    path.set('id_orig', new_id)
                    change = True
            if(change):
                inter_path.append(path)

        for path in inter_path:
            add_arrow(self, self.svg.getElementById(path.get('id_orig')), self.svg.getElementById(path.get('id_dest')))
            path.delete()

if __name__ == '__main__':
    Constructor().run()