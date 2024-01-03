from graphics import Canvas
Canvas_width = 300
Canvas_height = 300
circle_size = 20
delay = 0.01

def main():
Canvas = Canvas(Canvas_width, Canvas_height)
while True:
mouse_x = Canvas.get_mouse_x()
mouse_y = Canvas.get_mouse_y()
if mouse_x >= 0 and mouse_x <= Canvas_width and mouse_y >= 0 and mouse_y <= Canvas_height:
