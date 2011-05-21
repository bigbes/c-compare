#/usr/bin/python
# -*- coding: utf-8 -*-
#
from pycparser import parse_file, c_parser
import time,argparse,sys
from pprint import pprint
from pycparser.c_ast import *
from copy import copy

from ctoc import translate_to_c, print_file
from genccfg import MakeInit
from expand import expand_decl, expand_init

class func_count:
    """Функтор-счетчик"""
    count = 0
    def __call__(self):
        self.count += 1
        return self.count

varr_arr = {}
fc_var = func_count()
fc_func = func_count()
fc_type = func_count()

def assist(node):
    typ = type(node)
    if typ == BinaryOp or typ == UnaryOp:
        return node.__class__.__name__+node.op
    return node.__class__.__name__

def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        pprint("Execution Time: %f" % (time.time()-t))
        return res

    return tmp

def comp_subtrees(self, other, hash1 = None, hash2 = None):
    if hash1 == None:
        hash1 = {}
    if hash2 == None:
        hash2 = {}
    if type(other) == type(self):
        if type(other) in (ID, Decl) and (self.id != None) and (other.id != None):
            if (self.id not in hash1) and (other.id not in hash2) and\
               (varr_arr[self.id]==varr_arr[other.id]):
                hash1[self.id] = [other.id, 1, other.coord.file, other.coord.line]
                hash2[other.id] = [self.id, 1, self.coord.file, self.coord.line]
            elif (self.id in hash1) and (other.id in hash2) and\
                 (hash1[self.id][0]==other.id):
                hash1[self.id][1] += 1
                hash2[other.id][1] += 1
            else:
                return False

        elif type(other) == FuncDef:

            temp_list1 = [self.body]
            temp_list2 = [other.body]
            if (other.decl != None and other.decl.type != None) and\
               (self.decl != None and self.decl.type != None):
                temp_list1.extend([self.decl.type.args, self.decl.type.type])
                temp_list2.extend([other.decl.type.args, other.decl.type.type])
            elif (other.decl != None and other.decl.type != None) ^\
                 (self.decl != None and self.decl.type != None):
                return False
            
            for i in range(0, len(temp_list1)):
                if not strange_check_1(temp_list1[i], temp_list2[i], hash1, hash2):
                    return False
        #TODO сравнение того, какая функция вызывается
        elif type(other) == FuncCall:
            return True

        else:
            tmp1 = self.children()
            tmp2 = other.children()
            for i in range(0, len(tmp1)):
                if not comp_subtrees(tmp1[i], tmp2[i], hash1, hash2):
                    return False
        return True
    return False

def get_number_of_children(node):
    if node == None:
        return 0
    child = node.children()
    return sum([get_number_of_children(i) for i in child]) + 1


def hashes_func(obj, h_array):
    substr = ""
    stri = assist(obj)
    for subobj in obj.children():
        stri += hashes_func(subobj, h_array)
    if stri is not "":
        if hash(stri) in h_array:
            h_array[hash(stri)] += [obj]
        else:
            h_array[hash(stri)] = [obj]
    return stri

def UncryptDecl(node, var_arr = None, type_arr = None,
                type_undone_arr = None, func_arr = None):
    if var_arr == None:
        var_arr = {}
    if type_arr == None:
        type_arr = {}
    if type_undone_arr == None:
        type_undone_arr = {}
    if func_arr == None:
        func_arr = {}

    types = []
    typ = type(node)
    if typ == ID:
        if not node.name in var_arr.keys():
            node.id = 'smth'
        else:
            node.id = copy(var_arr[node.name][0])

    #TODO возможны зацикливания из-за неверных и рассистких высказываний. fuck lol
    elif typ == FuncCall:
        if node.name.name in func_arr.keys():
            node.name.id = func_arr[node.name.name][0]
        else:
            node.name.id = 'StandartFunction'
        if not node.args is None:
            for i in node.args.exprs:
                UncryptDecl(i, copy(var_arr), copy(type_arr),
                            copy(type_undone_arr), copy(func_arr))
    elif typ == Decl:
        if node.name != None:
            node.id=fc_var()
            var_arr[node.name]=[node.id, expand_decl(node, type_arr)]
            if node.id not in varr_arr.keys():
                varr_arr[node.id] = [expand_decl(node, type_arr)]
            else:
                varr_arr[node.id] += [expand_decl(node, type_arr)]
        if node.init != None:
            UncryptDecl(node.init, var_arr, type_arr,
                        type_undone_arr, func_arr)
        if type(node.type) in [Struct, Union, Enum] and\
           node.type.name != None:
            type_undone_arr[node.type.name]=[fc_type(),
                                             expand_decl(node, type_arr)[2]]
#            pprint(type_undone_arr)

    elif typ == Typedef:
        if type(node.type) in [Struct, Union, Enum] and\
           node.type.decls == None:
            type_arr[node.name] = type_undone_arr[node.type.name]
        else:
            type_arr[node.name] = [fc_type, expand_decl(node.type, type_arr)]

    elif typ == FuncDef:
        arr = {}
        if node.decl.type.args != None:
            for i in node.decl.type.args.params:
                UncryptDecl(i, var_arr, type_arr, type_undone_arr, func_arr)

        if not node.decl.name in func_arr.keys():
            func_arr[node.decl.name]=[fc_func() ,
                                      expand_init(node.decl.type.type), arr]
            node.decl.id = func_arr[node.decl.name][0]
        else:
            raise(Exception("{0} repeated twice".format(node.decl.name)))
        var_arr_updated = copy(var_arr)
        var_arr_updated.update(arr)
        UncryptDecl(node.body, var_arr_updated, copy(type_arr),
                    copy(type_undone_arr), copy(func_arr))

    else:
        for i in node.children():
            if type(i) in [Decl, FuncDef, DeclList, Typedef]:
                UncryptDecl(i, var_arr, type_arr, type_undone_arr, func_arr)
            else:
                UncryptDecl(i, copy(var_arr), copy(type_arr), copy(type_undone_arr), copy(func_arr))

#@timer
def parsing_file(filename, ans, debug=None):
    if debug == None:
        debug = False
    node = parse_file(filename)
    hashes_func(node, ans)
    UncryptDecl(node)
    if debug:
        node.show()
    return node

def strange_check_1(a, b, hash1, hash2):
    if not(a is None or b is None):
        return comp_subtrees(a, b, hash1, hash2)
    return a is None and b is None

def Complain1(node, array, answer = None):
    if answer is None:
        answer = []
    if node in array:
#        pprint(node)
        answer.append(node)
        return answer
    else:
        for i in node.children():
            Complain1(i, array, answer)
    return answer

def Complain(node1, node2, array1, array2, matching):
    h1 = Complain1(node1, array1)
    h2 = Complain1(node2, array2)
    filter(lambda x: matching[x] in h2, h1)
    h2 = [matching[i] for i in h1]
#    pprint([h1, h2])
    return [h1, h2]

def AddParsingArguments():
    parser = argparse.ArgumentParser(description='Process input files,\
    output files and max number of coincidences')

    parser.add_argument('-f', '--first', help='first input file'
                        , default='examples/main1.c')
    parser.add_argument('-s', '--second', help='second input file'
                        ,  default='examples/main2.c')
    parser.add_argument('-o', '--output', help='output file'
                        ,  default=sys.stdout)
    parser.add_argument('-n', '--number', help='max number of coincidences'
                        , default=10)

    args = parser.parse_args()
    if args.output != sys.stdout:
        sys.stdout = open(args.output, 'a')
    return (args.first, args.second, args.number)

if __name__ == "__main__":
    filename1, filename2, number = AddParsingArguments()
    MakeInit()
    ans1 = {}
    ans2 = {}
    t1 = parsing_file(filename1, ans1)
    t2 = parsing_file(filename2, ans2)
    first = {}
    second = {}
    third = []
    fourth = []
    for i in ans1:
        if i in ans2:
            for j in ans1[i]:
                for k in ans2[i]:
                    if type(j) not in (ID, Constant) and\
                       comp_subtrees(j, k, first, second):
                        if first != {}:
                            third.append([copy(first), copy(second), j, k])
                            first = {}
                            second = {}
            if third != []:
                fourth.append(copy(third))
                third = []

    array1 = []
    array2 = []
    temp_dict1 = {}
    temp_dict2 = {}

    for i in fourth:
        for j in i:
            array1.append(j[2])
            array2.append(j[3])
            temp_dict1[j[2]]=j[3]
    
    array3 = Complain(t1, t2, array1, array2, temp_dict1)

    for i in array3[0]:
        temp_dict2[get_number_of_children(i)] = i
    fragment_number = 1
    for key in sorted(temp_dict2.keys(), key=lambda x:-x):
        if number > 0:
            print("Fragment Number: {0}".format(fragment_number))
            print('#----------------------------------------')
            print_file(temp_dict2[key], 0)
            print('')
            print_file(temp_dict1[temp_dict2[key]], 1)
            print('#----------------------------------------')
            number -= 1
            fragment_number += 1

    