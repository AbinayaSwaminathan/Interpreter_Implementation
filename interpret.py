
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
       DTREE ::=  ["int", ID, ETREE]  |  ["proc", ID, ILIST, [], CLIST]
       post:  heap is updated with  d
    """
    ns = activeNS()
    if d[0] == "int": 
        var = d[1]                                       #["int", ID, ETREE]
        #check sanity -- var is declared or not 
        val = interpretETREE(d[2])
        # heap[ns][var] = val
        #printHeap()
        #print(ns, var, val)
        declare(ns, var, val)
        #printHeap()

 
    if d[0] == "proc":  #["proc", ID, ILIST, [], CLIST]
        var = d[1]
        closure_handle = allocateNS()
        #heap[ns][var] = handle   #var exists or not
        declare(ns, var, closure_handle)

        heap[closure_handle]["body"] = d[4]
        heap[closure_handle]["params"] = d[2]
        heap[closure_handle]["type"] = "proc"
        heap[closure_handle]["link"] = ns
    

     ### WRITE ME
    



def interpretCLIST(clist) :
    """pre: clist  is a list of commands,  CLIST ::=  [ CTREE+ ]
                  where  CTREE+  means  one or more CTREEs
       post:  memory  holds all the updates commanded by program  p
    """
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
        CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]  |  ["call", LTREE, ELIST]
       post:  heap  holds the updates commanded by  c

       (i) Compute the meaning of L, verify that the meaning is the handle to a procedure closure, and extract from that closure these parts: IL, CL, and parentns link. (If L is not bound to a handle of a proc closure, it's an error that stops execution.) 
       (ii) evaluate EL to a list of values 
       (iii) Allocate a new namespace.
       (iv) Within the new namespace, bind parentns to the handle extracted from the closure; bind the values from EL to the corresponding names in IL. (Make certain that the number of arguments in EL equals the number of parameters in IL. Otherwise, it's an error that prints a message and stops execution). 
       (v) Push the new namespace's handle onto the activation stack, execute CL, and upon completion pop the activation stack.
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
    # ["call", LTREE, ELIST]
    elif operator == "call":
    # (i) Compute the meaning of L, verify that the meaning is the handle to a procedure closure,
        # and extract from that closure these parts: IL, CL, and parentns link.
        # (If L is not bound to a handle of a proc closure, it's an error that stops execution.) 
      
        ns, proc_name = interpretLTREE(c[1]) # "h0", "p"
        closure_handle = lookup(ns, proc_name)
        
        if isinstance(closure_handle, int):
            crash("....")
        #if closure_handle is string: then proc_name is valid name of a procedure
        if isinstance(closure_handle, str):
            params_list = lookup(closure_handle,"params")   # ["a", "b""] if we have declaured proc p(a, b):...
            proc_body = lookup(closure_handle,"body")
            parentns = lookup(closure_handle,"link")

         # (ii) evaluate EL to a list of values
         # c[2], is ["2", "3"] if p(2, 3)
        actual_params = []
        for e in c[2]:
            temp=interpretETREE(e)
            actual_params.append(temp)


        #(iii) Allocate a new namespace.
        new_ns = allocateNS()



       # (iv) Within the new namespace, bind parentns to the handle extracted from the closure
              # bind the values from EL to the corresponding names in IL.
       # (Make certain that the number of arguments in EL equals the number of parameters in IL. 
       # Otherwise, it's an error that prints a message and stops execution). 
        heap[new_ns]["parentns"]= parentns
        if len(params_list)== len(actual_params):
            for params, actual_params in zip(params_list,actual_params):
                heap[new_ns][params]= actual_params
        else:
            crash("error parameter no. doesn't match")
       # (v) Push the new namespace's handle onto the activation stack, execute CL, 
       # and upon completion pop the activation stack.
        pushHandle(new_ns)
        interpretCLIST(proc_body)
        popHandle()
        del heap[new_ns]
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
    
    if isinstance(ltree, str) and  ltree[0].isalpha()  :  #  ID
        active_ns=activeNS()
            #check if ltree is in current active_ns if not find the parent ns
        if ltree not in heap[active_ns]:
            parentns=heap[active_ns]["parentns"]
        elif ltree in heap['parentns']
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




