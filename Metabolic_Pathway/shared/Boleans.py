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

def check_format_enzime(code: str) -> bool:
    
    # Patern that verifies it is a enxime.
    pattern = re.compile("[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+")
    if(pattern.match(code)):
        return True
    return False

def check_format_numeric(string: str) -> bool:
    if(string.isnumeric()):
        return True
    return False

# Checks if the id is not used in the svg.
def check_unique_id(id: str, ids: list[str]):

    # Patern that verifies it is a number.
    pattern = re.compile("[E|I|M|C|R] [0-9]+")

    # Iterates through all the ids for a equal id.
    for svg_id in ids:
        svg_id = svg_id[2:]
        if(svg_id == id):
            return False
    return True