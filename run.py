from shared_memory_handler import shared_mem
from proccess_test2 import main2,own_mem2
from proccess_test import main,own_mem

if __name__ == "__main__":
    mem_handler = shared_mem()
    
    mem_handler.add_worker(main2,standard_mem=own_mem2) # mainthread
    
    
    mem_handler.add_worker(main,standard_mem=own_mem) # debugwindow
    
    
    
    mem_handler.start_workers()
    
    mem_handler.start_memory_thread()
    