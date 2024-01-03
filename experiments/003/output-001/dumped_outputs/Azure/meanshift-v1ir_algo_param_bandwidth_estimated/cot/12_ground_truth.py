from graphics import Canvas
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CIRCLE_SIZE = 20
DELAY = 0.01

def main:
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    while TRUE
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        if mouse_x >= 0 and mouse_x <= CANVAS_WIDTH and mouse_y >=0 and mouse_y <= CANVAS_HEIGHT
