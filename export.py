import os
import cv2

class Export:
  def __init__(self):
    self.path = os.path.dirname(os.path.realpath(__file__))

    self.frames_path = self.path + "/frames/"
    self.cells_path = self.path + "/cells/"
    self.out_path = self.path + "/out/"
  
  def sort_images(self):
    li = []
    for i in range(len(os.listdir(self.out_path))+1):
      for img in os.listdir(self.out_path):
        if str(img) == f"frame{i}.png":
          li.append(img)
    return li

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

Export().make_video()