from pycparser.c_ast import *

def makeinit():
    ID.__init__ = init_ID
    ID.attr_names = ('name', 'id')
    Decl.__init__ = init_Decl
    Decl.attr_names = ('name','quals','storage','funcspec', 'id',)



def init_ID(self, name, coord=None, id=None):
    self.name = name
    self.coord = coord
    self.id = id

def init_Decl(self, name, quals, storage, funcspec, type, init, bitsize,\
		coord=None, id=None):
    self.name = name
    self.quals = quals
    self.storage = storage
    self.funcspec = funcspec
    self.type = type
    self.init = init
    self.bitsize = bitsize
    self.coord = coord
    self.id = id

#------------------------------------------------------------------------------

if __name__ == "__main__":
	pass
