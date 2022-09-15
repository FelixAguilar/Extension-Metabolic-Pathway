import inkex, re
from shared.Element import add_component, add_elemental_reaction, add_inverse_reaction, add_reaction, add_metabolic_building_block
from shared.Boleans import is_metabolic_pathway_element, check_format_reaction, check_format_enzime
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

        # Verifies that only one item is selected.
        if(len(self.svg.selection) < 1):
            inkex.errormsg('To change size there must be one elements selected. There are currently ' + str(len(self.svg.selection)) + ' items selected.')
            return

        # Verifies that the selected element is from a metabolic pathway.
        for element in self.svg.selection:
            if(not is_metabolic_pathway_element(element.get_id())):
                inkex.errormsg(error_metabolic_element)
                return

        for element in self.svg.selection:
            
            # Obtains the element and extracts the data.
            id = element.get_id()
            transform = get_transformation(element)
            position = (float(element.get('x')), float(element.get('y')))
            size = float(element.get('size'))
        
            # Obtains the current position and size for the element.
            x = position[0] + transform[0]
            y = position[1] + transform[1]
            size = size + self.options.difference

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
            id_new = ""
            if(id.find('R') != -1):
                group = add_reaction(self, code, reactions, enzime, x, y, size)
                id_new = group.get_id()
            elif(id.find('E') != -1):
                group =add_elemental_reaction(self, code, reactions, enzime, x, y, size)
                id_new = group.get_id()
            elif(id.find('M') != -1):
                group = add_metabolic_building_block(self,  code, x, y, size)
                id_new = group.get_id()
            elif(id.find('I') != -1):
                group = add_inverse_reaction(self, code, reactions, enzime, x, y, size)
                id_new = group.get_id()
            elif(id.find('C') != -1):
                group = add_component(self, code, x, y, size)
                id_new = group.get_id()

            # Restructures the arrows for this element.
            paths = []
            all_ids = self.svg.get_ids()
            pattern = re.compile("P [0-9]+")
            for g_id in all_ids:
                if(pattern.match(g_id)):
                    paths.append(g_id)

            inter_path = []
            for path_id in paths:
                path = self.svg.getElementById(path_id)
                if(path.get('id_dest') == id):
                    path.set('id_dest', id_new)
                    inter_path.append(path)
                elif(path.get('id_orig') == id):
                    path.set('id_orig', id_new)
                    inter_path.append(path)

            for path in inter_path:
                add_arrow(self, self.svg.getElementById(path.get('id_orig')), self.svg.getElementById(path.get('id_dest')), False)
                path.delete()

if __name__ == '__main__':
    Constructor().run()