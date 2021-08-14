import PIL
from PIL import Image
from PIL import ImageOps

import cv2

import os

path = os.path.dirname(os.path.realpath(__file__))
video_path = path + "/video.mp4"
frames_path = path + "/frames/"
cells_path = path + "/cells/"
out_path = path + "/out/"
out_video_path = path + "output.mp4"


def make_frames(amount):
  vidcap = cv2.VideoCapture(video_path); count = 0; success,image = vidcap.read()
  while success:
    if count%1 == 0:
      cv2.imwrite(frames_path + "frame%d.png" % count, image)
      if success: print("Frame Exported: frame{count}.png")
    success,image = vidcap.read()
    if count >= amount and amount:
      break
    count += 1

def pixel_difference(p1, p2):
  p1_sum = p1[0] + p1[1] + p1[2]
  p2_sum = p2[0] + p2[1] + p2[2]
  if p1_sum >= p2_sum:
    diff = p1_sum-p2_sum
  else:
    diff = p2_sum-p1_sum
  return diff

def find_closest_cell(p):
  best_match = [1000*1000, ""]
  for cell in [(88, 88, 88, cells_path + "immobile.png"), (48, 48, 48, cells_path + "BGDefault.png"), (1, 203, 182, cells_path + "CCWspinner_alt.png"), (255, 104, 2, cells_path + "CWspinner_alt.png"), (208, 12, 33, cells_path + "enemy.png"), (3, 205, 113, cells_path + "generator.png"), (68, 110, 185, cells_path + "mover.png"), (227, 164, 40, cells_path + "slide.png"), (210, 158, 94, cells_path + "push.png"), (155, 0, 206, cells_path + "trash.png")]:
    diff = pixel_difference(p, cell)
    if diff < best_match[0]:
      best_match = [diff, cell[3]]
  return best_match

def make_frame(frame, size=128):
  frame_image = Image.open(frames_path + f"frame{frame}.png")
  frame_image = frame_image.resize((int(size * frame_image.width / frame_image.height), size), Image.ANTIALIAS)

  output_image = Image.new("RGBA", (round(size * frame_image.width / frame_image.height * 16), size * 16), (42, 42, 42, 255))

  for y in range(frame_image.height):
    for x in range(frame_image.width):
      pixel = frame_image.getpixel((x, y))
      cell_img = Image.open(find_closest_cell(pixel)[1])
      output_image.paste(cell_img, (x*16, y*16))
  
  output_image.save(out_path + f"frame{frame}.png", "PNG")

def main():
  for i, frame in enumerate(os.listdir(frames_path)):
    make_frame(i)
    print(f"Frame Rendered: frame{i}.png")

def sort_images():
  li = []
  for i in range(len(os.listdir(out_path))+1):
    for img in os.listdir(out_path):
      if str(img) == f"frame{i}.png":
        li.append(img)
  return li

make_frames()

main()

images = sort_images()
frame = cv2.imread(os.path.join(out_path, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'MP4V'), 24, (width,height))

for i, image in enumerate(images): 
  print(f"{i}/{len(images)}")
  print(image)
  video.write(cv2.imread(os.path.join(out_path, image)))

cv2.destroyAllWindows()
video.release()
