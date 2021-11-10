
### INTERPRETER FOR OBJECT-ORIENTED LANGUAGE

"""The interpreter processes parse trees of this format:

PTREE ::=  [DLIST, CLIST]

DLIST ::=  [ DTREE* ]
           where  DTREE*  means zero or more DTREEs
DTREE ::=  ["int", ID, ETREE]  |  ["proc", ID, ILIST, [], CLIST]
           (note: the [] in the "proc" operator tree will be used in Part B)

CLIST ::=  [ CTREE* ]
CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]  |  ["call", LTREE, ELIST]

ELIST ::=   [ ETREE* ]
ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]  
      where  OP ::=  "+"  | "-"

LTREE ::=  ID

ILIST ::= [ ID* ]
ID    ::=  a nonempty string of letters

NUM   ::=  a nonempty string of digits


The interpreter computes the meaning of the parse tree, which is
a sequence of updates to heap storage.

You will extend the above to include declarations and calls of parameterized
procedures.
"""


from heapmodule import *   # import the contents of the  heapmodule.py  module 


### INTERPRETER FUNCTIONS, one for each class of parse tree listed above.
#   See the end of program for the driver function,  interpretPTREE


def interpretPTREE(tree) :
    """interprets a complete program tree
       pre: tree is a  PTREE ::= [ DLIST, CLIST ]
       post: heap holds all updates commanded by the  tree
    """
    initializeHeap()
    interpretDLIST(tree[0])
    interpretCLIST(tree[1])
    print("Successful termination.")
    printHeap()


def interpretDLIST(dlist) :
    """pre: dlist  is a list of declarations,  DLIST ::=  [ DTREE+ ]
       post:  memory  holds all the declarations in  dlist
    """
    for dec in dlist :
        interpretDTREE(dec)


def interpretDTREE(d) :
    """pre: d  is a declaration represented as a DTREE:
       DTREE ::=  ["int", ID, ETREE]  |  ["proc", ID, ILIST, [], CLIST] (WRITE ME)
       post:  heap is updated with  d
    """
    ### WRITE ME
    active_ns = ....
    
    # ["int", ID, ETREE]  |  ["proc", ID, ILIST, [], CLIST]
    # ["int", "x", "2"]  |  ["proc", "p", ['y', 'z'], [], [...]]
    if d[0] == 'int': # d = ["int", ID, ETREE] 
        var = d[1]
        val = interpretETREE(...)
        declare(active_ns, var, val)
    # ["proc", ID, ILIST, [], CLIST]
    if d[0] == 'proc': 
        proc_name = d[1]
        param_list = ...
        cmd_list = ...
        handle = allocNS() # heap[handle] = {}
        declare(....) # heap = {active_ns: {..., proc_name:handle, ...}}
        heap[handle]['type'] = 'proc'
        heap[handle]['params'] = ...
        heap[handle]['local'] = []
        heap[handle]['body'] = ...
        heap[handle]['parentns'] = ...
    


def interpretCLIST(clist) :
    """pre: clist  is a list of commands,  CLIST ::=  [ CTREE+ ]
                  where  CTREE+  means  one or more CTREEs
       post:  memory  holds all the updates commanded by program  p
    """
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
       CTREE ::=  (WRITE ME) ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]  |  ["call", LTREE, ELIST]
       post:  heap  holds the updates commanded by  c
    """
    operator = c[0]
    if operator == "=" :   # , ["=", LTREE, ETREE]
        handle, field = interpretLTREE(c[1])  # returns (handle,field) pair
        rval = interpretETREE(c[2])
        update(handle, field, rval)
    elif operator == "print" :   # ["print", LTREE]
        print(interpretETREE(c[1]))
        printHeap()
    elif operator == "if" :   # ["if", ETREE, CLIST1, CLIST2]
        test = interpretETREE(c[1])
        if test != 0 :
            interpretCLIST(c[2])
        else :
            interpretCLIST(c[3]) 
    # WRITE ME 
    # interpret ["call", LTREE, ELIST] # ["call", "p", ['1', '2']] if proc p(x, y):...
    elif operator == "call":
        # 1. find where proc closure, extract params, body, parentns...
        handle, proc_name = interpretLTREE(...)
        # 2. look up all the following from p's handle
        param_list = lookup(handle, 'params')
        ...
        ....
        cmd_list = lookup(handle, 'body')


        # 4.
        newNS = ...
        pushHandle(newNS) # for example activation_stack = ['h0', 'h2']
        heap[newNS]['parentns'] = ...
        #evaluate EL=c[2] to a list of values
        if len(param_list) == len(c[2]):
            for param, e in zip(param_list, c[2]):
                v = interpretETREE(...)
                heap[newNS][param] = ...  # heap = {..., 'h2': {'a': 1, 'b':2}} if proc p(a, b):...end p (1, 2)

        interpretCLIST(...)
        popHandle()

    else :  crash(c, "invalid command")


def interpretETREE(etree) :
    """interpretETREE computes the meaning of an expression operator tree.
         ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE] 
         OP ::= "+" | "-"
        post: updates the heap as needed and returns the  etree's value
    """
    if isinstance(etree, str) and etree.isdigit() :  # NUM  -- string of digits
      ans = int(etree) 
    elif  etree[0] in ("+", "-") :    # [OP, ETREE, ETREE]
        ans1 = interpretETREE(etree[1])
        ans2 = interpretETREE(etree[2])
        if isinstance(ans1,int) and isinstance(ans2, int) :
            if etree[0] == "+" :
                ans = ans1 + ans2
            elif etree[0] == "-" :
                ans = ans1 - ans2
        else : crash(etree, "addition error --- nonint value used")
    elif  etree[0] == "deref" :    # ["deref", LTREE]
        handle, field = interpretLTREE(etree[1])
        ans = lookup(handle,field)
    else :  crash(etree, "invalid expression form")
    return ans


def interpretLTREE(ltree) :
    """interpretLTREE computes the meaning of a lefthandside operator tree.
          LTREE ::=  ID
       post: returns a pair,  (handle,varname),  the L-value of  ltree
    """
    # WRITE ME: MODIFY THE FUCNTION 
    if isinstance(ltree, str) and  ltree[0].isalpha()  :  #  ID 
        ans = (activeNS(), ltree)   # use the handle to the active namespace
    else :
        crash(ltree, "illegal L-value")
    return ans


def crash(tree, message) :
    """pre: tree is a parse tree,  and  message is a string
       post: tree and message are printed and interpreter stopped
    """
    print("Error evaluating tree:", tree)
    print(message)
    print("Crash!")
    printHeap()
    raise Exception   # stops the interpreter




