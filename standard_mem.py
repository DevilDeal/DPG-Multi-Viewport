class mem_obj():
    def __init__(self,id,func,arg,identity :str|int,share_all = True , ):
        self.id = id
        self.func = func
        self.arg = arg
        
        self.share_all = share_all
        self.identity = identity
        self.mode = "var"
        self.received = False
        self.send = False
        self.thread_active = True

def recv_memory(receiver,memory:int = None):
    ### mem_obj.mode needs to be "all" instead of "var" ###
    if not receiver.empty():
        if memory != None:
            item = receiver.get()[memory]
        else:
            item = receiver.get()
        return item

def request_memory(parent_interface,memory_space:int = 0,to_process:int=0,):
    variable_str = ""
    parent_interface.recv_variable_from_share("all",to_process,memory_space,variable_str)

def request_var(parent_interface,variable_str:str = "",memory_space:int = 0,to_process:int=0,):
    
    parent_interface.recv_variable_from_share("var",to_process,memory_space,variable_str)

def receive(receiver,awaits:bool = True):
    if awaits:
        while receiver.empty():
            
            pass
    if not receiver.empty():
        value = receiver.get()
        return value

def update_var(sender_interface,variable_str:str ,value,memory_space:int = 0,):
    
    sender_interface.put(["var",memory_space,variable_str,value])
    
def update_var_identity(sender_interface,variable_str:str ,value,memory_space:int|str = 0,):
    
    sender_interface.put(["var2",memory_space,variable_str,value])
    
def update_memory(sender_interface,memory):
    sender_interface.put([memory])

def terminate_all(parent_interface):
    parent_interface.recv_variable_from_share("terminate",0,0,0)