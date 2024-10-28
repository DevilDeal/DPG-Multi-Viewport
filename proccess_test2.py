import dearpygui.dearpygui as dpg
from standard_mem import mem_obj
from standard_mem import *

class own_mem2(mem_obj):
    def __init__(self, id, func, arg, identity: str | int, share_all=True):
        super().__init__(id, func, arg, identity, share_all)
        self.test_text = 0
        self.identity = "debug_window"
        self.TITLE = "debug_window"
        self.mode = "var"
        self.test_text_value = "here"
        self.test_text_tag = None
        
TITLE = "debug_window"


def main2(send,recv,own_id,change_mode,parent):
    dpg.create_context()
    dpg.create_viewport(title=TITLE, decorated=False,clear_color=[0,0,0,100],always_on_top=False,vsync=True,width=400, height=222,x_pos=-10)
    dpg.setup_dearpygui()
    is_menu_bar_clicked = True
    
    def mouse_drag_callback(_, app_data):
        if is_menu_bar_clicked:
            _, drag_delta_x, drag_delta_y = app_data
            viewport_pos_x, viewport_pos_y = dpg.get_viewport_pos()
            new_pos_x = viewport_pos_x + drag_delta_x
            new_pos_y = max(viewport_pos_y + drag_delta_y, 0)
            
            dpg.set_viewport_pos([new_pos_x, new_pos_y])

    def mouse_click_callback():
        global is_menu_bar_clicked
        is_menu_bar_clicked = True if dpg.get_mouse_pos(local=False)[1] < 40 else False

    with dpg.handler_registry():
        dpg.add_mouse_drag_handler(button=0, threshold=0, callback=mouse_drag_callback)
        
   
            

    with dpg.window(label="test",no_title_bar=True,pos=(0,0),width=222-1,height=222-1,no_resize=True,no_background=True) as primary_window:
        test_text =dpg.add_text("here")
        request_memory(parent,0,own_id)
        
        mem_space = receive(recv,awaits=True)
        mem_space.test_text_tag = test_text
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
        
        if mem_space!= None:
            if mem_space.test_text_tag!= None:
                dpg.set_value(mem_space.test_text_tag,mem_space.test_text_value)
        
        
        dpg.render_dearpygui_frame()
    terminate_all(parent_interface=parent)
    dpg.destroy_context()
