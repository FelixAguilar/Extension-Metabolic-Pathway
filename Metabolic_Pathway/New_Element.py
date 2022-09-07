import inkex, re
from shared.Add_Element import add_component, add_elemental_reaction, add_inverse_reaction, add_reaction, add_metabolic_building_block
from shared.Errors import *

# Checks if the id is not used in the svg.
def check_unique_id(self, id, verify):
    if(verify):
        pattern = re.compile("[E|M|I|R] [0-9]+")
    
        # Gets all ids in the svg.
        svg_ids = []
        for svg_id in self.svg.get_ids():
            if(pattern.match(svg_id)):
                svg_ids.append(svg_id)

        # Iterates through all the ids for a equal id.
        for svg_id in svg_ids:
            element = self.svg.getElementById(svg_id)
            if(element.get('code') == id):
                inkex.errormsg(error_id)
                return False
    return True

def check_format_numeric(string, error):
    if(string.isnumeric()):
        return True
    inkex.errormsg(error)
    return False

# Checks that it folows the format of a enzime.
def check_format_enzime(enzime: str) -> bool:
    pattern = re.compile("^[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+$")
    if(pattern.match(enzime)):
        return True
    inkex.errormsg(error_format_enzime)
    return False

# From a list in string format obtains all the reactions inside a list.
def string_to_list(list: str) -> list[str]:
    list = list.split(', ')
    return list

# Checks if all reactions inside a list have the correct format.
def check_format_reactions(reactions: list[str]) -> bool:
    pattern = re.compile("^R[0-9][0-9][0-9][0-9][0-9](_rev)?$")
    for reaction in reactions:
        if(not pattern.match(reaction)):
            inkex.errormsg(error_format_reaction)
            return False
    return True

class Constructor(inkex.EffectExtension):
    
    def add_arguments(self, pars):
        pars.add_argument('--ID_M', type=str, default='undefined', dest='ID_M', help="ID of element MDAG")
        pars.add_argument('--ID_R', type=str, default='undefined', dest='ID_R', help="ID of element RC")
        pars.add_argument('--KEGG_reaction_M', type=str, default='undefined', dest='KEGG_reaction_M', help="KEGG reaction code MDAG")
        pars.add_argument('--KEGG_reaction_R', type=str, default='undefined', dest='KEGG_reaction_R', help="KEGG reaction code RC")
        pars.add_argument('--KEGG_enzime_M', type=str, default='undefined', dest='KEGG_enzime_M', help="KEGG enzime code MDAG")
        pars.add_argument('--KEGG_enzime_R', type=str, default='undefined', dest='KEGG_enzime_R', help="KEGG enzime code RC")
        pars.add_argument('--type_M', type=str, default='undefined', dest='type_M', help="Type of element MDAG")
        pars.add_argument('--type_R', type=str, default='undefined', dest='type_R', help="Type of element RC")
        pars.add_argument('--tab', type=str, default='undefined', dest='tab', help="Type of Metabolic Pathway")
        pars.add_argument('--x_M', type=int, default='30', dest='x_M', help="Position x of the element MDAG")
        pars.add_argument('--x_R', type=int, default='30', dest='x_R', help="Position x of the element RC")
        pars.add_argument('--y_M', type=int, default='30', dest='y_M', help="Position y of the element MDAG")
        pars.add_argument('--y_R', type=int, default='30', dest='y_R', help="Position y of the element RC")
        pars.add_argument('--size_M', type=int, default='20', dest='size_M', help="Size of the element MDAG")
        pars.add_argument('--size_R', type=int, default='20', dest='size_R', help="Size of the element RC")
        pars.add_argument('--unique_M', type=inkex.Boolean, default=False, dest='unique_M', help="If the element id needs to not be unique")
        pars.add_argument('--unique_R', type=inkex.Boolean, default=False, dest='unique_R', help="If the element id needs to not be unique")

    def effect(self):

        if self.options.tab == 'DAG':
            if self.options.type_M == 'Reactions':
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_M)
                    if(check_format_reactions(reactions) and check_format_enzime(self.options.KEGG_enzime_M) and check_unique_id(self, self.options.ID_M, self.options.unique_M)):
                        add_reaction(self, self.options.ID_M, reactions, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            elif self.options.type_M == 'Elemental_Reactions':
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_M)
                    if(check_format_reactions(reactions) and check_unique_id(self, self.options.ID_M, self.options.unique_M) and check_format_enzime(self.options.KEGG_enzime_M)):     
                        add_elemental_reaction(self, self.options.ID_M, reactions, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
            else:
                if(self.options.ID_M == 'undefined'):
                    inkex.errormsg(error_empty_fields_mmb)
                else:
                    if(check_format_numeric(self.options.ID_M, error_format_id) and check_unique_id(self, self.options.ID_M, self.options.unique_M)): 
                        add_metabolic_building_block(self, self.options.ID_M, self.options.x_M, self.options.y_M, self.options.size_M)
        else:
            if self.options.type_R == 'Reactions':
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_R)
                    if(check_format_reactions(reactions) and check_format_enzime(self.options.KEGG_enzime_R) and check_unique_id(self, self.options.ID_R, self.options.unique_R)):
                        add_reaction(self, self.options.ID_R, reactions, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)
            elif self.options.type_R == 'Component':
                if (self.options.KEGG_reaction_R == 'undefined'):
                    inkex.errormsg(error_empty_fields_component)
                else:
                    add_component(self, self.options.KEGG_reaction_R, self.options.x_R, self.options.y_R, self.options.size_R)
            else:
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_R)
                    if(check_format_reactions(reactions) and check_format_enzime(self.options.KEGG_enzime_R) and check_unique_id(self, self.options.ID_R, self.options.unique_R)):
                        add_inverse_reaction(self, self.options.ID_R, reactions, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)

if __name__ == '__main__':
    Constructor().run()