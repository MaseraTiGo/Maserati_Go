import win32gui
import win32con
import win32api
import time
'''
what's more:change to multiprocess to improve efficient
            coding more pretty and observe the standard
'''    

titles = set()
search = set()
add_friends = []


def get_all_window(hwnd, mouse): 
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and \
        win32gui.IsWindowVisible(hwnd):
        titles.add(win32gui.GetWindowText(hwnd))
        if win32gui.GetWindowText(hwnd) == "查找":
            search.add(hwnd)
        if "添加好友" in win32gui.GetWindowText(hwnd):
            add_friends.append([hwnd, win32gui.GetWindowRect(hwnd)])
            print('CurrentHwnd', hwnd)
            
def send_message(af):
    w_hwnd = af[0]
    w1, h1, w2, h2 = af[1]
    w = w2 - w1
    h = h2 - h1
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB,0)
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYUP, win32con.VK_TAB,0)
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB,0)
    win32gui.PostMessage(w_hwnd, win32con.WM_KEYUP, win32con.VK_TAB,0)
    win32gui.PostMessage(w_hwnd, win32con.WM_PASTE, 0, 0)  #send message from pasteboard  
    time.sleep(0.3)  
    #win32gui.PostMessage(w_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN,0)  #  press the enter key
    #win32gui.PostMessage(w_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN,0) #let the key up 
    #win32gui.PostMessage(w_hwnd, win32con.WM_CLOSE, 0, 0)
    #print('why', w_hwnd)
    win32gui.SetWindowPos(w_hwnd, 0, 380, 0, w, h, win32con.SWP_SHOWWINDOW)
    time.sleep(0.1)
    win32api.SetCursorPos((w+360, 15))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    #win32gui.CloseWindow(w_hwnd)

def add():
    if add_friends:
        send_message(add_friends.pop())
        #time.sleep(1)

win32gui.EnumWindows(get_all_window, 0)
win32api.SetCursorPos((50, 730))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
time.sleep(1)
win32gui.EnumWindows(get_all_window, 0)        
ss = list(search)
if search:
    win32gui.SetWindowPos(ss[0], 0, 380, 0, 1000, 600, win32con.SWP_SHOWWINDOW)
    #print('move')
    time.sleep(2)     
    for _ in range(2):
        win32api.SetCursorPos((1070, 110))
        #time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)
        y_pos = 270
        for _ in range(4):
            x_pos = 550
            for _ in range(4):
                win32api.SetCursorPos((x_pos, y_pos))
                #time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                time.sleep(0.3)
                win32gui.EnumWindows(get_all_window, 0)
                add()
                x_pos += 220
            y_pos += 90
        
        #break
    
# lt = [t for t in titles if t] 
# lt.sort() 
# for t in lt:  
    # print(t) 

    

# import win32con,win32gui,time  
# hwnd = 66996   ### window handle, decimal 
  
# win32gui.PostMessage(hwnd,win32con.WM_PASTE, 0, 0)  # send message from the pasteboard
  
# time.sleep(0.3)  
  
# win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,win32con.VK_RETURN,0)  #  press enter key    
  
# win32gui.PostMessage(hwnd,win32con.WM_KEYUP,win32con.VK_RETURN,0)     #release enter key


#Test_Infomation