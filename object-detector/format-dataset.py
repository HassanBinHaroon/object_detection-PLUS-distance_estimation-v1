import json
import os
from pathlib import Path
from tqdm import tqdm
import PIL.Image as Image


# load dataset
train_data = []
val_data = []
train_annotations = []
val_annotations = []
categories = []

with open("FLIR_ADAS_1_3/train/thermal_annotations.json") as f:
    train_data = json.loads(f.read())
    for annotation in train_data["annotations"]:
       train_annotations.append(annotation)

with open("FLIR_ADAS_1_3/val/thermal_annotations.json") as f:
    val_data = json.loads(f.read())
    for annotation in val_data["annotations"]:
       val_annotations.append(annotation)

# handle first nc classes
nc = 14
category_label = [0]*nc
for category in train_data["categories"]:
  categories.append(category)
  if(category["id"] < nc):
    category_label[category["id"]] = category["name"]

categories = [d for d in train_annotations if d["id"] < nc]
train_annotations = [d for d in train_annotations if d["category_id"] < nc]
val_annotations = [d for d in val_annotations if d["category_id"] < nc]

def count_number_of_images(folder_path):
    import os
    initial_count = 0
    dir = folder_path
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1

    return initial_count

def create_dataset(thermal_dataset, dataset_type):
  
  images_path = Path(f"thermal_dataset/images/{dataset_type}")
  images_path.mkdir(parents=True, exist_ok=True)
  labels_path = Path(f"thermal_dataset/labels/{dataset_type}")
  labels_path.mkdir(parents=True, exist_ok=True)
  initial_count=count_number_of_images("FLIR_ADAS_1_3/train/thermal_8_bit")

  for coun, row in enumerate(tqdm(thermal_dataset)):

    image_name=''
    label_name=''
    if dataset_type == "train":
        image_name = "{}.jpeg".format(str(row["image_id"]+1).zfill(5))
        imgPath = "FLIR_ADAS_1_3/{}/thermal_8_bit/FLIR_{}.jpeg".format(dataset_type,str(row["image_id"]+1).zfill(5))
        label_name = "{}.txt".format(str(row["image_id"]+1).zfill(5))
    else:
        image_name = "{}.jpeg".format(str(row["image_id"]+initial_count+1).zfill(5))
        imgPath = "FLIR_ADAS_1_3/{}/thermal_8_bit/FLIR_{}.jpeg".format(dataset_type,str(row["image_id"]+initial_count+1).zfill(5))
        label_name = "{}.txt".format(str(row["image_id"]+initial_count+1).zfill(5))

    if os.path.exists(str(images_path / image_name)) == False:
      img = Image.open(imgPath)
      width, height = img.size
      img = img.convert("RGB")
      img.show() # ?
      img.save(str(images_path / image_name), "JPEG")
    
    with (labels_path / label_name).open(mode="a") as label_file:

          min_x, min_y, bbox_width, bbox_height = row["bbox"]
          category_idx = row["category_id"]
          center_x = min_x + bbox_width*0.5
          center_y = min_y + bbox_height*0.5

          label_file.write(
            f"{category_idx} {center_x/width} {center_y/height} {bbox_width/width} {bbox_height/height}\n"
          )


create_dataset(train_annotations , "train")
create_dataset(val_annotations , "val")
