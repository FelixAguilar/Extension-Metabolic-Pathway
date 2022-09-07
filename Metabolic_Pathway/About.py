import inkex

class Constructor(inkex.EffectExtension):
    
    # Obtains the arguments in the pop up menu.
    def add_arguments(self, pars):
        pars.add_argument('--tab', type=str, default='undefined', dest='tab', help="Type of Metabolic Pathway")

    # Execution of the extension.
    def effect(self):
        None

if __name__ == '__main__':
    Constructor().run()