# -*- coding: utf-8 -*-
from pycparser.c_ast import *

def MakeInit():
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

def assist(node):
    typ = type(node)
    if typ == BinaryOp or typ == UnaryOp:
        return node.__class__.__name__+node.op
    return node.__class__.__name__

#------------------------------------------------------------------------------

if __name__ == "__main__":
    pass
