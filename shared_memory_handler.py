import multiprocessing as mp
from standard_mem import mem_obj
import time
import threading

class shared_mem():
    def __init__(self,target_fps :int = None,sleep :float = 0.0) -> None:
       
        self.workers : int = 0
        self.worker_list : list = []
        self.memory_thread_started = False
        self.share_task = []
        self.recv_queues = []
        self.send_queues = []
        self.lock = False
        self.sleep = sleep
        
    def add_worker(self,func,arg = None,identity : str|int = None,standard_mem : bool = None):
        if identity == None:
            identity = self.workers

        if standard_mem == None:
            thread = mem_obj(self.workers,func,arg,identity)
        else:
            thread = standard_mem(self.workers,func,arg,identity)

        self.worker_list.append(thread)
        recv_queue = mp.SimpleQueue()
        send_queue = mp.SimpleQueue()
        self.recv_queues.append(recv_queue)
        self.send_queues.append(send_queue)
        self.workers += 1
        return thread
    
    def start_workers(self,multiprocessing:bool = True,daemon:bool = True):
        for worker in self.worker_list:
            if worker.arg != None:
                queue = mp.SimpleQueue()
                self.share_task.append(queue)
                if multiprocessing:
                    mp.Process(target=worker.func,args=(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id,self.share_task[worker.id],self,worker.arg,),daemon=daemon).start()
                else:
                    
                    threading.Thread(target=worker.func,args=(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id,self.share_task[worker.id],self,worker.arg,),daemon=daemon).start()
                #worker.func(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id,worker.arg,)
                
            else:
                queue = mp.SimpleQueue()
                self.share_task.append(queue)
                if multiprocessing:
                    mp.Process(target=worker.func,args=(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id,self.share_task[worker.id],self),daemon=daemon).start()
                else:
                    threading.Thread(target=worker.func,args=(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id,self.share_task[worker.id],self),daemon=daemon).start()
                #worker.func(self.recv_queues[worker.id],self.send_queues[worker.id],worker.id)
            

    def send_share_on_request(self):
        pass
    def update_own_share(self):
        pass
    def send_all_shares(self):
        pass

    def update_variable_from_share(self,id,message,value):
        setattr(self.worker_list[id],message,value)
        
    
    def recv_variable_from_share(self,mode:str = "var" or "all" ,sender:int = 0,id:int = 0,attr : str = None,):
        if self.share_task[sender].empty():
            self.share_task[sender].put([id,sender,mode,attr])
           
    def update_variable_from_share2(self,receiver,message,value):
        for i in range(len(self.worker_list)):
            if self.worker_list[i].identity == receiver:
                
                setattr(self.worker_list[i],message,value)
                
                break
    
           
    def recv_variable_from_share2(self,mode:str = "var" or "all" ,sender:str = None,receiver:str = None,attr : str = None,):
        for i in range(len(self.worker_list)):
            if self.worker_list[i].identity == receiver:
                if self.share_task[i].empty():
                    for i in range(len(self.worker_list)):
                        if self.worker_list[i].identity == sender:
                            self.share_task[i].put([receiver,sender,mode,attr])
                            break
            
    def start_memory_thread(self):
        self.memory_thread_started = True
        
        while self.memory_thread_started :
            

            for task in self.share_task:
                if not task.empty():
                    task_list = task.get()
                    
                    id ,sender ,mode,attr = task_list
                    
                    match mode:
                        
                        case "var":
                            item = getattr(self.worker_list[id],attr)
                        
                            
                        case "terminate":
                                
                            self.memory_thread_started=False

                        case _ :
                            item = self.worker_list[id]
                        
                    if self.send_queues[sender].empty():
                        self.send_queues[sender].put(item)

            for current_share in self.recv_queues:
                if not current_share.empty():
                    recv_message = current_share.get()
                    
                    for share in [recv_message]:
                        match share[0]:
                            case "var":
                                
                                id = share[1]
                                message = share[2]
                                value = share[3]
                                
                                self.update_variable_from_share(id,message,value)
                                
                            case _ :
                                share = share[0]
                                id = share.id
                                message = share
                                self.worker_list[id] = message
            
            for current_share_index in range(len(self.send_queues)):
                if self.worker_list[current_share_index].mode == "all":
                    if self.send_queues[current_share_index].empty():
                        self.send_queues[current_share_index].put(self.worker_list)
            

            if self.sleep !=0.0:
                time.sleep(self.sleep)