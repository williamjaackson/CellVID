# Imports
from PIL import Image, ImageOps
import os
import sys
import cv2
import threading
import time

class CellVid:
  def __init__(self, video_path, frame_rate, frame_steps, frame_count, size, step):
    self.video_path = video_path
    self.frame_steps = frame_steps
    self.frame_count = int(frame_count)
    
    self.path = os.path.dirname(os.path.realpath(__file__))

    self.vidcap = cv2.VideoCapture(video_path)

    self.frame_rate = frame_rate
    if frame_rate == 0:
      self.frame_rate = self.vidcap.get(cv2.CAP_PROP_FPS)

    self.frames_path = self.path + "/frames/"
    self.cells_path = self.path + "/cells/"
    self.out_path = self.path + "/out/"

    self.main(step, size)
  
  def sort_images(self):
    li = []
    for i in range(len(os.listdir(self.out_path))+1):
      for img in os.listdir(self.out_path):
        if str(img) == f"frame{i}.png":
          li.append(img)
    return li

  def make_frames(self, count=0):
    success,image = self.vidcap.read()
    while success:
      if count % self.frame_steps == 0:
        cv2.imwrite(self.frames_path + f"frame{count}.png", image)
        if success: print(f"Frame Exported: frame{count}.png")
      success,image = self.vidcap.read()
      if self.frame_count and count >= self.frame_count:
        break
      count += 1
  
  def render_frame(self, i, size):
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
  def render(self, size=128):
    for i, frame in enumerate(os.listdir(self.frames_path)):
      if i == len(os.listdir(self.frames_path))-1:
        return
      print("Rendering...")
      threading.Thread(target=self.render_frame, args=[i, size]).start()
  
  def make_video(self):
    self.images = self.sort_images()
    frame = cv2.imread(os.path.join(self.out_path, self.images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'MP4V'), self.frame_rate, (width,height))

    for i, image in enumerate(self.images): 
      print(f"Exporting Video: {i}/{len(self.images)}")
      video.write(cv2.imread(os.path.join(self.out_path, image)))

    cv2.destroyAllWindows()
    video.release()
  
  def main(self, s, size):
    if s == "frames":
      self.make_frames()
    elif s == "render":
      self.render(size)
    elif s == "export":
      self.make_video()
    else:
      self.make_frames()
      self.render(size)
      while len(os.listdir(self.out_path)) != len(os.listdir(self.frames_path)):
        pass
      time.sleep(0.25*(len(os.listdir(self.out_path))))
      self.make_video()
  

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    raise SyntaxError("python3 main.py <video_path> <frame_rate=24> <frame_steps=1> <frame_count=0> <size=128> <step=0>")
  elif len(sys.argv) == 2:
    video_path = sys.argv[1]
    frame_rate = 0
    frame_steps = 1
    frame_count = 0
    size = 128
    step = 0
  elif len(sys.argv) == 3:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = 1
    frame_count = 0
    size = 128
    step = 0
  elif len(sys.argv) == 4:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = int(sys.argv[3])
    frame_count = 0
    size = 128
    step = 0
  elif len(sys.argv) == 5:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = int(sys.argv[3])
    size = int(sys.argv[4])
    frame_count = 0
    step = 0
  elif len(sys.argv) == 6:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = int(sys.argv[3])
    size = int(sys.argv[4])
    frame_count = int(sys.argv[5])-1
    step = 0
  elif len(sys.argv) == 7:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = int(sys.argv[3])
    size = int(sys.argv[4])
    frame_count = int(sys.argv[5])-1
    step = sys.argv[6]
  cellvid = CellVid(video_path, frame_rate, frame_steps, frame_count, size, step)