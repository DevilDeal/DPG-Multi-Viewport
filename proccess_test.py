
import dearpygui.dearpygui as dpg
from standard_mem import mem_obj
from standard_mem import *

class own_mem(mem_obj):
    def __init__(self, id, func, arg, identity: str | int, share_all=True):
        super().__init__(id, func, arg, identity, share_all)
        self.test_text = 0
        self.identity = "changer"
        self.TITLE = "changer"
        self.mode = "var"
        self.test_input = "here"
        self.test_input_tag = None
        
TITLE = "changer"


def main(send,recv,own_id,change_mode,parent):
    dpg.create_context()
    dpg.create_viewport(title=TITLE,width=400, height=222,x_pos=444)
    dpg.setup_dearpygui()
    
    
    
    def callback_input_text(user,data):
        
        mem_space.test_text_value = data
        update_var(send,"test_text_value",data,0)
        update_memory(send,memory=mem_space)

    with dpg.window(label="test",no_title_bar=False,pos=(0,0),width=222-1,height=222-1,no_resize=True,no_background=False) as primary_window:
        test_input = dpg.add_input_text(label= "change value",default_value="here",callback=callback_input_text)
        request_memory(parent,0,own_id)
        
        mem_space = receive(recv,awaits=True)
        mem_space.test_input_tag = test_input
        update_memory(send,memory=mem_space)
 

    with dpg.theme( ) as global_theme:
        with dpg.theme_component():
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,(0,0,0,100))
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,(0,0,0,100))
            
    dpg.bind_theme(global_theme)
    dpg.set_primary_window(primary_window,True)
    dpg.show_viewport()
    
    
    

    # below replaces, start_dearpygui()
    
    while dpg.is_dearpygui_running():
        request_memory(parent,0,own_id)
        
        mem_space = receive(recv,awaits=True)
        
        
        dpg.render_dearpygui_frame()
        
    terminate_all(parent_interface=parent)
    dpg.destroy_context()

