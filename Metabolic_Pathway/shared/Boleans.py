import re
from typing import Any, List

# Checks if the ID belongs to a path.
def is_path(ID: str) -> bool:
    pattern = re.compile("P [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Checks if the ID belongs to a component.
def is_component(ID: str) -> bool:
    pattern = re.compile("C [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Checks if the ID belongs to a elemental reaction.
def is_elemental_reaction(ID: str) -> bool:
    pattern = re.compile("E [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Checks if the ID belongs to a element of a metabolic pathway.
def is_metabolic_pathway_element(ID: str) -> bool:
    pattern = re.compile("[E|I|M|C|R] [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Checks if the reaction have the correct format.
def check_format_reaction(reaction: str) -> bool:
    pattern = re.compile("^R[0-9][0-9][0-9][0-9][0-9](_rev)?$")
    if(pattern.match(reaction)):
            return True
    return False

# Checks if all reactions inside a list have the correct format.
def check_format_reactions(reactions: List[str]) -> bool:
    for reaction in reactions:
        if(not check_format_reaction(reaction)):
            return False
    return True

# Checks that it folows the format of a enzime.
def check_format_enzime(enzime: str) -> bool:
    pattern = re.compile("^([0-9]+|\-)\.([0-9]+|\-)\.([0-9]+|\-)\.([0-9]+|\-)$")
    if(pattern.match(enzime)):
        return True
    return False

# Checks if it is a number.
def is_numeric(string: str) -> bool:
    if(string.isnumeric()):
        return True
    return False

# Checks if the id is not used in the svg.
def is_unique_id(self: Any, id: str, verify: bool) -> bool:
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
                return False
    return True
