import inkex, re, Add_Arrow
from re import S, T
from Add_Arrow import add_arrow

def move_arrows(self):

    # Obteins all the path ids in the svg.
    paths = []
    all_ids = self.svg.get_ids()
    pattern = re.compile("P [0-9]+")
    for id in all_ids:
        if(pattern.match(id)):
            paths.append(id)

    # Removes all paths inside the selection.
    for element in self.svg.selection:
        if(pattern.match(element.get_id())):
            paths.remove(element.get_id())

    # Obtains all the paths that connects the selection with the rest of the svg.
    inter_path = []
    for element in self.svg.selection:
        id = element.get_id()
        if(not pattern.match(element.get_id())):
            for path_id in paths:
                path = self.svg.getElementById(path_id)
                if(path.get('id_dest') == id or (path.get('id_orig') == id)):
                    inter_path.append(path)

    # For each path between the selection and the rest redraw the line and deletes the arrow.
    for path in inter_path:
        add_arrow(self, self.svg.getElementById(path.get('id_orig')), self.svg.getElementById(path.get('id_dest')), False)
        path.delete()