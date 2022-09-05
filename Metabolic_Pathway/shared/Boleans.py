import re

# Check if the ID belongs to a component.
def is_component(ID: str) -> bool:
    pattern = re.compile("C [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Check if the ID belongs to a elemental reaction.
def is_elemental_reaction(ID: str) -> bool:
    pattern = re.compile("E [0-9]+")
    if(pattern.match(ID)):
        return True
    return False

# Check if the ID belongs to a element of a metabolic pathway.
def is_metabolic_pathway_element(ID: str) -> bool:
    pattern = re.compile("[E|I|M|C|R] [0-9]+")
    if(pattern.match(ID)):
        return True
    return False
