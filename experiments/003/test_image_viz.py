import cv2
import json


# Define your colors
DOT_COLORS =  [
    ((0, 0, 255), 'rgb(255, 0, 0)'),       # red
    ((0, 255, 0), 'rgb(0, 255, 0)'),       # green
    ((255, 0, 0), 'rgb(0, 0, 255)'),       # blue
    ((255, 0, 255), 'rgb(255, 0, 255)'),   # magenta
    ((192, 255, 0), 'rgb(0, 255, 192)'),   # mint green
    ((64, 0, 255), 'rgb(255, 0, 64)'),     # deep pink
    ((128, 255, 255), 'rgb(255, 255, 128)'), # pastel yellow
    ((128, 255, 128), 'rgb(128, 255, 128)'), # pastel green
    ((255, 255, 128), 'rgb(128, 255, 255)'), # pastel cyan
    ((255, 255, 0), 'rgb(0, 255, 255)'),   # cyan
    ((255, 165, 0), 'rgb(0, 165, 255)'),   # orange
    ((255, 105, 180), 'rgb(180, 105, 255)'), # hot pink
    ((255, 64, 0), 'rgb(0, 64, 255)'),     # deep orange
    ((0, 165, 255), 'rgb(255, 165, 0)'),   # light blue
    ((60, 179, 113), 'rgb(113, 179, 60)'), # medium sea green
    ((238, 130, 238), 'rgb(238, 130, 238)'), # violet
    ((245, 222, 179), 'rgb(179, 222, 245)'), # wheat
    ((210, 105, 30), 'rgb(30, 105, 210)'), # chocolate
    ((127, 255, 0), 'rgb(0, 255, 127)'),   # chartreuse
    ((255, 140, 0), 'rgb(0, 140, 255)'),   # dark orange
    ((32, 178, 170), 'rgb(170, 178, 32)'), # light sea green
]

def draw_lines(image_path, data):
    # Load image
    img = cv2.imread(image_path)

    print("Ocr Output \n")

    print(data["ocr_ouptut"])
    
    # Draw lines based on OCR output
    for line in data["ocr_ouptut"]:
        x, y, w, h = line["x"], line["y"], line["w"], line["h"]
        top_left = (int(x), int(y))
        bottom_right = (int(x + w), int(y + h))
        cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

    # Map cluster labels to colors
    color_map = {i: color[0] for i, color in enumerate(DOT_COLORS)}

    # Draw a dot for each cluster label
    if "ir_algo_output_indented_lines" in data:
      for line in data["ir_algo_output_indented_lines"]:
          x, y = line["x"], line["y"]
          cluster_label = line["cluster_label"]
          cv2.circle(img, (int(x), int(y)), 10, color_map[cluster_label], -1)

    return img

# Testing the function
with open('output/lm_post_processed.json', 'r') as f:
    data = json.load(f)
    
    
target_image = data[1500]

image_path = f"../images/{target_image['image_id']}.jpg"
print(target_image['image_id'])

img = draw_lines(image_path, target_image)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()