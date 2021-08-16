import threading
from PIL import Image, ImageOps
import time
import os
import sys
import cv2

# python3 main.py <video> <framerate> <size>

class CellVID:
  def __init__(self, video_path, framerate=0, size=128):
    self.path = os.path.dirname(os.path.realpath(__file__))

    self.video_path = video_path
    self.frames_path = self.path + "/frames/"
    self.cells_path = self.path + "/cells/"
    self.out_path = self.path + "/out/"

    self.video_capture = cv2.VideoCapture(self.video_path)

    self.frame_rate = frame_rate
    if frame_rate == 0:
      self.frame_rate = self.video_capture.get(cv2.CAP_PROP_FPS)

    self.size = size

    self.main()
  
  def make_frames(self):
    success,image = self.video_capture.read()
    while success:
      if count % self.frame_steps == 0:
        cv2.imwrite(self.frames_path + f"frame{count}.png", image)
        if success: print(f"Frame Exported: frame{count}.png")
      success,image = self.video_capture.read()
      if self.frame_count and count >= self.frame_count:
        break
      count += 1

  def render_frame(self):
    if i+1 == len(os.listdir(self.frames_path)):
      return
    frame_image = Image.open(self.frames_path + f"frame{i}.png")
    frame_image = frame_image.resize((int(size * frame_image.width / frame_image.height), size), Image.ANTIALIAS)

    output_image = Image.new("RGBA", (round(size * frame_image.width / frame_image.height * 16), size * 16), (42, 42, 42, 255))

    for y in range(frame_image.height):
      for x in range(frame_image.width):
        pixel = frame_image.getpixel((x, y))

        best_match = [1000*1000, self.cells_path + "BGDefault.png"]
        for cell in [(88, 88, 88, self.cells_path + "immobile.png"), (48, 48, 48, self.cells_path + "BGDefault.png"), (1, 203, 182, self.cells_path + "CCWspinner_alt.png"), (255, 104, 2, self.cells_path + "CWspinner_alt.png"), (208, 12, 33, self.cells_path + "enemy.png"), (3, 205, 113, self.cells_path + "generator.png"), (68, 110, 185, self.cells_path + "mover.png"), (227, 164, 40, self.cells_path + "slide.png"), (210, 158, 94, self.cells_path + "push.png"), (155, 0, 206, self.cells_path + "trash.png")]:
          p1_sum = pixel[0] + pixel[1] + pixel[2]
          p2_sum = cell[0] + cell[1] + cell[2]
          if p1_sum >= p2_sum:
            diff = p1_sum-p2_sum
          else:
            diff = p2_sum-p1_sum
          if diff < best_match[0]:
            best_match = [diff, cell[3]]

        closest_cell = best_match[1]

        cell_img = Image.open(closest_cell)
        output_image.paste(cell_img, (x*16, y*16))
    
      if i == 0:
        print(f"{y}/{size}")
    output_image.save(self.out_path + f"frame{i}.png", "PNG")
    print(f"Frame Rendered: frame{i}.png")

  def render(self):
    for i, frame in enumerate(os.listdir(self.frames_path)):
      if i == len(os.listdir(self.frames_path))-1:
        return
      while threading.activeCount() >= 10:
        pass
      print(f"Rendering frame{i}.png...")
      threading.Thread(target=self.render_frame, args=[i, self.size], daemon=True).start()

  def main(self):
    self.make_frames()
    self.render()

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    cellvid = CellVid(sys.argv[1], sys.argv[2], sys.argv[3])
  elif len(sys.argv) <= 2:
    cellvid = CellVid(sys.argv[1], sys.argv[2])
  elif len(sys.argv) <= 3:
    cellvid = CellVid(sys.argv[1], sys.argv[2], sys.argv[3])
  else:
    prin("python3 main.py <video> <framerate> <size>")
    exit()