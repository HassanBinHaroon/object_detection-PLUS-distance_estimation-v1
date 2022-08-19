''' create yaml file '''
# create content of yaml file
dataset_path = "thermal_dataset/"
nc = 14
category_label=['empty', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter']

data = ["train: {0}images/train\n".format(dataset_path),
        "val: {0}images/val\n\n".format(dataset_path),
        "nc: {0}\n\n".format(nc),
        "names: {0}".format(category_label)]
        
# write dataset yaml file
with open("./data/dataset.yaml", "w") as dataset_yaml:
  dataset_yaml.writelines(data)