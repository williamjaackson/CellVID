# Imports
from PIL import Image, ImageOps
import os
import sys
import cv2

class CellVid:
  def __init__(self, video_path, frame_rate, frame_steps):
    self.video_path = video_path
    self.frame_rate = frame_rate
    self.frame_steps = frame_steps
    
    self.path = os.path.dirname(os.path.realpath(__file__))

    self.vidcap = cv2.VideoCapture(video_path)
    self.frames_path = self.path + "/frames/"
    self.cells_path = self.path + "/cells/"
    self.out_path = self.path + "/out/"

    self.main()
  
  def make_frames(self, count=0):
    success,image = self.vidcap.read()
    while success:
      if count % self.frame_steps == 0:
        cv2.imwrite(self.frames_path + f"frame{count}.png", image)
        if success: print(f"Frame Exported: frame{count}.png")
      success,image = self.vidcap.read()
      #if count >= amount and amount:
      #  break
      count += 1
  
  def render(self):
    for i, frame in enumerate(os.listdir(self.frames_path)):
      
      frame_image = Image.open(self.frames_path + f"frame{frame}.png")
      frame_image = frame_image.resize((int(size * frame_image.width / frame_image.height), size), Image.ANTIALIAS)

      output_image = Image.new("RGBA", (round(size * frame_image.width / frame_image.height * 16), size * 16), (42, 42, 42, 255))

      for y in range(frame_image.height):
        for x in range(frame_image.width):
          pixel = frame_image.getpixel((x, y))

          p1_sum = p1[0] + p1[1] + p1[2]
          p2_sum = p2[0] + p2[1] + p2[2]
          if p1_sum >= p2_sum:
            diff = p1_sum-p2_sum
          else:
            diff = p2_sum-p1_sum

          best_match = [1000*1000, self.cells_path + "BGDefault.png"]
          for cell in [(88, 88, 88, self.cells_path + "immobile.png"), (48, 48, 48, self.cells_path + "BGDefault.png"), (1, 203, 182, self.cells_pat + "CCWspinner_alt.png"), (255, 104, 2, self.cells_pat + "CWspinner_alt.png"), (208, 12, 33, self.cells_pat + "enemy.png"), (3, 205, 113, self.cells_pat + "generator.png"), (68, 110, 185, self.cells_pat + "mover.png"), (227, 164, 40, self.cells_pat + "slide.png"), (210, 158, 94, self.cells_pat + "push.png"), (155, 0, 206, self.cells_pat + "trash.png")]:
            if diff < best_match[0]:
              best_match = [diff, cell[3]]

          closest_cell = best_match[1]

          cell_img = Image.open(closest_cell)
          output_image.paste(cell_img, (x*16, y*16))
      
      output_image.save(self.out_path + f"frame{frame}.png", "PNG")

      print(f"Frame Rendered: frame{i}.png")
  
  def make_video(self):
    images = sort_images()
    frame = cv2.imread(os.path.join(self.out_path, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'MP4V'), self.frame_rate, (width,height))

    for i, image in enumerate(images): 
      print(f"Exporting Video: {i}/{len(images)}")
      video.write(cv2.imread(os.path.join(self.out_path, image)))

    cv2.destroyAllWindows()
    video.release()
  
  def main(self):
    self.make_frames()
    self.render()
    self.make_video()
  

if __name__ == "__main__":
  if len(sys.argv) <= 1:
    raise SyntaxError("python3 main.py <video_path> <frame_rate=24> <frame_steps=1>")
  elif len(sys.argv) == 2:
    video_path = sys.argv[1]
    frame_rate = 24
    frame_steps = 1
  elif len(sys.argv) == 3:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = 1
  elif len(sys.argv) == 4:
    video_path = sys.argv[1]
    frame_rate = int(sys.argv[2])
    frame_steps = int(sys.argv[3])
  cellvid = CellVid(video_path, frame_rate, frame_steps)