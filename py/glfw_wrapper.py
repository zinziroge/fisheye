from glfw import *

def glfwSetTime(time):
    return set_time(time)

def glfwGetTime():
    return get_time()

def glfwInit():
    return init()

def glfwTerminate():
    return terminate()

def glfwGetMonitors():
    return get_monitors()

def glfwWindowHint(target, hint):
    window_hint(target, hint)

def glfwGetVideoMode(monitor):
    return get_video_mode(monitor)

def glfwCreateWindow(width, height, title, monitor, share):
    return create_window(width, height, title, monitor, share)

def glfwMakeContextCurrent(window):
    make_context_current(window)

def glfwSetWindowUserPointer(window, pointer):
    return set_window_user_pointer(window, pointer)

def glfwGetWindowUserPointer(window):
    return get_window_user_pointer(window)

def glfwSetKeyCallback(window, cbbun):
    return set_key_callback(window, cbbun)

def glfwSetMouseButtonCallback(window, mouse):
    return set_mouse_button_callback(window, mouse)

def glfwSetScrollCallback(window, wheel):
    return set_scroll_callback(window, wheel)

def glfwSetFramebufferSizeCallback(window, cbfun):
    return set_framebuffer_size_callback(window, cbfun)

def glfwSwapInterval(interval):
    swap_interval(interval)

def glfwDestroyWindow(window):
    destroy_window(window)

#    return _glfw.glfwWindowShouldClose(window)
def glfwWindowShouldClose(window):
    window_should_close(window)

#    return _glfw.glfwGetKey(window, key)
def glfwGetKey(window, key):
    return get_key(window, key)

def glfwPollEvents():
    return poll_events()

#    return xpos_value.value, ypos_value.value
def glfwGetCursorPos(window):
    return get_cursor_pos(window)

def glfwGetMouseButton(window, button):
    return get_mouse_button(window, button)

def glfwSwapBuffers(window):
    swap_buffers(window)
