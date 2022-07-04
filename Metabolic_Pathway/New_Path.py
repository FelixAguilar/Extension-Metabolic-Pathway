from operator import length_hint
from tokenize import group
from wsgiref.util import request_uri
import inkex, re
from re import S

class Constructor(inkex.EffectExtension):
    def add_arguments(self, pars):
        inkex.errormsg('The ID is already in use, please change it to another number.')

    def effect(self):
        inkex.errormsg('The ID is already in use, please change it to another number.')
        
if __name__ == '__main__':
    Constructor().run()