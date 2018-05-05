#---for auto add friends---
#file_author:lhd
#date: 2018-5-4
__author__ = 'ds'

import win32gui
import win32api
import win32con
import re
import time


def get_Resolution():
    '''
    return your Pc's Resolution
    '''
    width = win32api.GetSystemMetrics(0)
    higth = win32api.GetSystemMetrics(1)
    return width, higth

def get_id(hwnd, mouse):
    '''
    get the window that we need,such as "qq" or "yy" or something else
    '''
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and \
        win32gui.IsWindowVisible(hwnd) and win32gui.GetClassName(hwnd) == "TXGuiFoundation":
        if soft_type == win32gui.GetWindowText(hwnd):
            main_id_need.append(hwnd)
        #elif win32gui.GetWindowText(hwnd) == "提示":
        #    win32gui.CloseWindow(hwnd)
        else:
            window_id_need.append(hwnd)

def double_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
def send_message(w_hwnd):
    win32gui.PostMessage(w_hwnd, win32con.WM_PASTE, 0, 0)  #send message from pasteboard  
    time.sleep(0.3)  
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN,0)  #  press the enter key
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN,0) #let the key up 
    win32gui.CloseWindow(w_hwnd)
    
#scroll down
def scroll_down():
    win32api.SetCursorPos((370, 250))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.SetCursorPos((370, 700))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)    

if __name__ == "__main__":
    '''
    main process to process single thread
    '''
    soft_type = "QQ" # qq , yy
    main_id_need = []
    window_id_need = []
    w_x_pos = 0
    c_y_pos = 215    
    win32gui.EnumWindows(get_id, 0)
    main_id_need2 = main_id_need
    
    #Multiple nesting, bad code!!!
    for hwnd in main_id_need2:
        try:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, w_x_pos, 0, 380, 760, win32con.SWP_SHOWWINDOW)
        except Exception as e:
            import sys
            print('Exception! make sure your QQ or YY is loading')
            sys.exit()
        
        soft_window_size = win32gui.GetWindowRect(hwnd)
        print(soft_window_size)
        for _ in range(2):
            for _ in range(3):
                win32api.SetCursorPos((145, c_y_pos))
                double_click()
                c_y_pos += 60
            window_id_need = []
            time.sleep(1)
            win32gui.EnumWindows(get_id, 0)
            print(window_id_need)
            for w_hwnd in window_id_need:
                send_message(w_hwnd)
            scroll_down()        
        w_x_pos += 290
        print('done')
        break