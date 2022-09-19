import inkex
from typing import List
from shared.Element import add_component, add_elemental_reaction, add_inverse_reaction, add_reaction, add_metabolic_building_block
from shared.Boleans import is_numeric, is_unique_id, check_format_reactions, check_format_enzime
from shared.Errors import *

# From a list in string format obtains all the reactions inside a list.
def string_to_list(list: str) -> List[str]:
    list = list.split(', ')
    return list

class Constructor(inkex.EffectExtension):
    
    # Arguments from the menu.
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

        # Selects which element draw using the current page of the menu and the current selected element in the drop down option. Before allowing, it checks if the information is correct.
        if self.options.tab == 'DAG':
            if self.options.type_M == 'Reactions':
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_M)
                    if(check_format_reactions(reactions)):
                        if(check_format_enzime(self.options.KEGG_enzime_M)):
                            if(is_unique_id(self, self.options.ID_M, self.options.unique_M)):
                                add_reaction(self, self.options.ID_M, reactions, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
                            else:
                                inkex.errormsg(error_id)
                        else:
                            inkex.errormsg(error_format_enzime)
                    else:
                        inkex.errormsg(error_format_reaction)

            elif self.options.type_M == 'Elemental_Reactions':
                if (self.options.ID_M == 'undefined' or self.options.KEGG_reaction_M == 'undefined' or self.options.KEGG_enzime_M == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_M)
                    if(check_format_reactions(reactions)):
                        if(check_format_enzime(self.options.KEGG_enzime_M)):   
                            if(is_unique_id(self, self.options.ID_M, self.options.unique_M)):  
                                add_elemental_reaction(self, self.options.ID_M, reactions, self.options.KEGG_enzime_M, self.options.x_M, self.options.y_M, self.options.size_M)
                            else:
                                inkex.errormsg(error_id)
                        else:
                            inkex.errormsg(error_format_enzime)
                    else:
                        inkex.errormsg(error_format_reaction)
            else:
                if(self.options.ID_M == 'undefined'):
                    inkex.errormsg(error_empty_fields_mmb)
                else:
                    if(is_numeric(self.options.ID_M)):
                        if(is_unique_id(self, self.options.ID_M, self.options.unique_M)): 
                            add_metabolic_building_block(self, self.options.ID_M, self.options.x_M, self.options.y_M, self.options.size_M)
                        else:
                            inkex.errormsg(error_id)
                    else:
                        inkex.errormsg(error_numeric)
        else:
            if self.options.type_R == 'Reactions':
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_R)
                    if(check_format_reactions(reactions)):
                        if(check_format_enzime(self.options.KEGG_enzime_R)):
                            if(is_unique_id(self, self.options.ID_R, self.options.unique_R)):
                                add_reaction(self, self.options.ID_R, reactions, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)
                            else:
                                inkex.errormsg(error_id)
                        else:
                            inkex.errormsg(error_format_enzime)
                    else:
                        inkex.errormsg(error_format_reaction)
            elif self.options.type_R == 'Component':
                if (self.options.ID_R == 'undefined'):
                    inkex.errormsg(error_empty_fields_component)
                else:
                    add_component(self, self.options.ID_R, self.options.x_R, self.options.y_R, self.options.size_R)
            else:
                if (self.options.ID_R == 'undefined' or self.options.KEGG_reaction_R == 'undefined' or self.options.KEGG_enzime_R == 'undefined'):
                    inkex.errormsg(error_empty_fields)
                else:
                    reactions = string_to_list(self.options.KEGG_reaction_R)
                    if(check_format_reactions(reactions)):
                        if(check_format_enzime(self.options.KEGG_enzime_R)):
                            if(is_unique_id(self, self.options.ID_R, self.options.unique_R)):
                                add_inverse_reaction(self, self.options.ID_R, reactions, self.options.KEGG_enzime_R, self.options.x_R, self.options.y_R, self.options.size_R)
                            else:
                                inkex.errormsg(error_id)
                        else:
                            inkex.errormsg(error_format_enzime)
                    else:
                        inkex.errormsg(error_format_reaction)

if __name__ == '__main__':
    Constructor().run()