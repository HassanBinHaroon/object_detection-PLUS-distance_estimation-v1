from pathlib import Path
import cv2
import torch
import torchvision
import matplotlib.pyplot as plt

def load_image(img_path: Path, resize=True):
  img = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
  img = cv2.resize(img, (128, 256), interpolation = cv2.INTER_AREA)
  return img

def show_grid(image_paths, figh):
  images = [load_image(img) for img in image_paths]
  images = torch.as_tensor(images)
  images = images.permute(0, 3, 1, 2)
  grid_img = torchvision.utils.make_grid(images, nrow=3)
  plt.figure(figsize=(figh, 12))
  plt.imshow(grid_img.permute(1, 2, 0))
  plt.axis('off')
  

# display detected examples from test set
img_paths = list(Path("/content/Graduation-Project/object-detector/results/frames").glob("*.png"))[:9]
show_grid(img_paths, 420)

# display unannotated image from validation set, its anotated version, our model output's version
outputImg = list(Path("results/frames").glob("*.png"))[1]
unannotatedImg = Path('FLIR_ADAS_1_3/val/thermal_8_bit/{0}'.format(outputImg.name))
annotatedImg = Path('FLIR_ADAS_1_3/val/Annotated_thermal_8_bit/{0}'.format(outputImg.name))
show_grid([unannotatedImg, annotatedImg, outputImg], 24)
