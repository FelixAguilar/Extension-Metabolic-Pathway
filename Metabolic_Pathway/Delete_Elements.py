import inkex, re
from shared.Boleans import is_metabolic_pathway_element
from shared.Errors import *

class Constructor(inkex.EffectExtension):
    
    #def add_arguments(self, pars):
        
    def effect(self):

        # Verifies that at least one item is selected.
        if(len(self.svg.selection) < 1):
            inkex.errormsg(error_delete_none)
            return

        # Obtains the element and extracts the data.
        ids = []
        for element in self.svg.selection:
            if (is_metabolic_pathway_element(element.get_id())):
                ids.append(element.get_id())
            element.delete()

        all_ids = self.svg.get_ids()
        pattern = re.compile("P [0-9]+")
        for g_id in all_ids:
            if(pattern.match(g_id)):
                path = self.svg.getElementById(g_id)
                for id in ids:
                    if(path.get('id_dest') == id or path.get('id_orig') == id):
                        path.delete()

if __name__ == '__main__':
    Constructor().run()