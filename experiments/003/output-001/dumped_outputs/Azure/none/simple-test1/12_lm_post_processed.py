from graphics import Canvas
Canvas_width = 300
Canvas_height = 300
Circle_size = 20
Delay = 0.01

def main():
Canvas = Canvas(Canvas_width, Canvas_height)
while True:
Mouse_x = Canvas.get_mouse_x()
Mouse_y = Canvas.get_mouse_y()
if Mouse_x >= 0 and Mouse_x <= Canvas_width and Mouse_y >= 0 and Mouse_y <= Canvas_height:
