

###  HEAP-STORAGE MODULE

"""The program's heap is currently a dictionary that maps handles to namespaces.

      heap : { (HANDLE : NAMESPACE)+ }
             where  HANDLE = a string of digits
                    NAMESPACE = a dictionary that maps var names to ints:
                                { (ID : INT)* }
   Example:
     heap = { "h0": {"x":7, "y":1, "z":2} }
     heap_count = 1
        is an example heap, where handle "0" names a namespace
        whose  "x"  field holds int 7, "y" field holds int 1,
        and "z" holds int 2.

===========================================================================
   You will extend this simple definition when you implement closures,
   the activation stack, and objects:

      heap : { (HANDLE : (NAMESPACE | CLOSURE))+ }
          where  HANDLE = a string, e.g.,  'h1'
                 NAMESPACE = a dictionary that maps var names to ints or to handles.  Also contains a "parentns" link to more-global vars.
                 CLOSURE = a dictionary containing a procedure's formal parameters, local decls, code body, and handle to the proc's global namespace
   Example:
     heap = { "h0": {"x":7, "y":1, "z":2, "p": 'h1', "parentns":'nil'},
              "h1": {"type":'proc', "params":['a'], "locals":[], "code":[['print', 'a']], "link":'h0'}
            }

        is an example heap, where handle "h0" names a namespace
        whose  "x"  field holds int 7, "y" field holds int 1,
        "z" holds int 2, and 'p' holds a handle to a closure saved at 'h1'. 
"""

heap = {}

heap_count = 0  # how many objects stored in the heap

# 1.
activation_stack = []  # This is the handle to the namespace in the heap that holds the
         # program's global variables.  See  initializeHeap  below.

### Maintenance functions for  heap  and  heap_count:


def isEmpty():
  """check whether activation stack is empty or not"""
  global activation_stack
  # WRITE ME


def pushHandle(handle):
  """ push handle on the activation_stack"""
  global activation_stack
  # WRITE ME
  activation_stack.append(...)

def popHandle():
  """ pop a handle from stack """
  global activation_stack
  # if  activation state is not empty 
  # WRITE ME
  if not isEmpty:
     ....

def topHandle():
  """ return the top handel on the activation_stack"""
  global activation_stack
  # WRITE ME


def activeNS():
    """returns the handle of the namespace that holds the currently visible
       program variables
    """
    # WRITE ME write this function

    pass
    #return top handle on the activation stack

def declare(handle, field, rval) :
    """creates a new definition in the heap at (handle, field) and initializes
       it with rval, provided that  heap[handle][field] does not already exist!
       (else crashes with a "redeclaration error")

       params: handle, field, as described above
               rval -- an int or a handle
    """
    ## WRITE ME: # int x = 1 ["int", "x" ,"1"] heap[handle][field] = rval #heap = {handle:{field:rval}}
    pass
    
def initializeHeap():
    """resets the heap for a new program"""
    global heap_count, heap, activation_stack
    handle = allocateNS()  # create namespace in  heap  for global variables heap={'h0':{}}
    heap[handle]['parentns'] = 'nil'
    # WRITE ME
    pushHandle(...)
    


def printHeap(): 
    """prints contents of  ns  and  heap"""
    print("activation stack =", activation_stack)

    print("heap = {")
    handles = sorted(heap.keys())
    for h in handles: 
        print(" ", h, ":", heap[h])
    print("}")
    

def allocateNS() :
    """allocates a new, empty namespace in the heap and returns its handle"""
    global heap_count
    newloc = "h" + str(heap_count)  # generate handle of form,  hn,  where  n  is an int
    heap[newloc] = {} # heap = {....'h4': {}}
    heap_count = heap_count + 1
    return newloc


def isLValid(handle, field):
    """checks if  (handle, field)  is a valid L-value, that is, checks
       that  heap[handle]  is a namespace  and   field  is found in it.
       returns  True  if the above holds true; returns  False  otherwise.
    """
    return (handle in heap) and (field in heap[handle])


def lookup(handle, field) :
    """looks up the value of  (handle,field)  in the heap
       param: handle,field -- such that  isLValid(handle, field)
       returns: The function extracts the object at  heap[handle],
                indexes it with field,  and returns  (heap[handle])[field]
    """
    if isLValid(handle, field) :
        return  heap[handle][field]
    else :
        crash("invalid lookup address: " + handle + " " + field)


def update(handle, field, rval) :
    """updates  rval  at heap[handle][field], provided that
         (i)  isLValid(handle,field)
         (ii) the type of  rval  matches the type of what's already stored at
              heap[handle][field]
       (else crashes with a type-error message)

       params:  handle, field, as described above
                rval -- an int or a handle
    """
    ## REVISE THE FOLLOWING CODE TO MATCH THE ABOVE DOCUMENTATION:
    heap[handle][field] = rval


def crash(message) :
    """prints message and stops execution"""
    print("Heap error: ", message, " Crash!")
    printHeap()
    raise Exception   # stops the interpreter
