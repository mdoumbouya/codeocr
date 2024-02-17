from graphics import Canvas
canvas_width = 300
canvas_height = 300
circle_size = 20
delay = 0.01

def main:
canvas = Canvas(canvas_width, canvas_height)
while True
mouse_x = canvas.get_mouse_x()
mouse_y = canvas.get_mouse_y()
if mouse_x >= 0 and mouse_x <= canvas_width and mouse_y >= 0 and mouse_y <= canvas_height
