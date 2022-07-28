import inkex, re, math
from shared.Add_Element import add_metabolic_building_block, add_elemental_reaction, add_reaction, add_inverse_reaction, add_component

def format_num(string):
    separator = string.find(',')
    if(separator != -1):
        string = string[:separator-1] + '.' + string[separator+1:]
        return float(string)
    return float(string)

def string_to_list(string):
    s_list = string.split(' ')
    f_list = []
    for s in s_list:
        s = s.split(",")
        x = float(s[0])
        y = float(s[1])
        f_list.append((x, y))
    return f_list

class Constructor(inkex.EffectExtension):
    
    #def add_arguments(self, pars):
    
    def effect(self):

        pattern1 = re.compile("graph*")
        pattern2 = re.compile("R[0-9][0-9][0-9][0-9][0-9]_rev")
        pattern3 = re.compile("R[0-9][0-9][0-9][0-9][0-9]")
        pattern4 = re.compile("[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+\.[0-9,\-]+")
        pattern5 = re.compile("[0-9]+")
        pattern6 = re.compile("C[0-9][0-9][0-9][0-9][0-9]")

        ids = []
        for id in self.svg.get_ids():
            ids.append(id)

        # Obtains all mbb in the svg.
        for id in ids:
            texts = []
            figures = []

            # get element by ID and if is a group and it isn't a graph then get all child elements.
            element = self.svg.getElementById(id)
            if(element.tag_name == 'g' and not pattern1.match(element.get_id())):
                for child in element.descendants():
                    if(child.tag_name == 'text'):
                        texts.append(child.text)
                
                    if(child.tag_name == 'ellipse' or child.tag_name == 'polygon'):
                        figures.append(child.get_id())
                    
            if(not texts and figures):
                # It is a path.
                None     
            elif(texts and figures):
                # It is a element.

                # Information for the element.
                reactions = []
                id_element = ""
                type_element = ""
                enzime = ""
                position = []
                size = 0
                name = ""

                # Obtains the texts inside the element and gets the type of element from it.
                for text in texts:
                    if(text == 'MBB'):
                        type_element = 'MBB'
                    elif(pattern2.match(text)):
                        type_element = 'Inverse'
                        reactions.append(text)
                    elif(pattern3.match(text)):
                        type_element = 'Reaction'
                        reactions.append(text)
                    elif(pattern4.match(text)):
                        enzime = text
                    elif(pattern5.match(text)):
                        id_element = text
                    elif(pattern6.match(text)):
                        type_element = 'Compound'
                        name = text
                    else:
                        name = text

                # Obtains the position of the element from the figures that the group contains.
                for figure in figures:
                    figure = self.svg.getElementById(figure)
                    if(figure.tag_name == 'ellipse'):
                        position = (float(figure.get('cx')), float(figure.get('cy')))
                        size = max(format_num(figure.get('rx')), format_num(figure.get('ry')))
                    elif(figure.tag_name == 'polygon'):

                        # If it is a polygon and filled with the color yellow then it is a elemental reaction.
                        if(figure.get('fill') == 'yellow'):
                            type_element = 'Elemental'
                            points = string_to_list(figure.get('points'))
                            x_A = float(points[0][0])
                            y_A = float(points[0][1])
                            x_B = float(points[4][0])
                            y_B = float(points[4][1])
                            position = ((x_A + x_B) / 2, (y_A + y_B) /2)
                            size = math.sqrt(math.pow((x_A - x_B) / 2, 2) + math.pow((y_A - y_B) / 2, 2))
                        else:
                            # it is a compound.
                            points = string_to_list(figure.get('points'))
                            x_A = float(points[0][0])
                            y_A = float(points[0][1])
                            x_B = float(points[2][0])
                            y_B = float(points[2][1])
                            x_C = float(points[1][0])
                            position = ((x_A + x_B) / 2, (y_A + y_B) /2)
                            size = abs(x_A - x_C)
                
                # Debug text.
                """if(type_element == "Inverse" or type_element == "Reaction" or type_element == "Elemental"):
                    inkex.errormsg(type_element + " " + id_element + " " + str(reactions) + " " + enzime + " " + str(position) + " " + str(size))
                elif(type_element == "MBB"):
                    inkex.errormsg(type_element + " " + id_element + " " + str(position) + " " + str(size))"""

                # Proceeds to draw the element.
                if(type_element == 'MBB'):
                    add_metabolic_building_block(self, id_element, position[0], position[1], size)
                elif(type_element == 'Reaction'):
                    add_reaction(self, id_element, reactions[0], enzime,  position[0], position[1], size)
                elif(type_element == 'Elemental'):
                    add_elemental_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size)
                elif(type_element == 'Inverse'):
                    add_inverse_reaction(self, id_element, reactions[0], enzime, position[0], position[1], size)
                elif(type_element == 'Compound'):
                    add_component(self, name, position[0], position[1], size)
                else:
                    None

            else:
                # Element that does not belong to a metabolic path way.
                None

if __name__ == '__main__':
    Constructor().run()