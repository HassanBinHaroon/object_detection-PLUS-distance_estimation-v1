nc = 14

# configure yolov5s
with open('models/yolov5s.yaml', 'r') as yolo_yaml:
    # read a list of lines into data
    data = yolo_yaml.readlines()

# change number of classes (nc)
for i in range(len(data)):
  if data[i].startswith("nc"):
    data[i] = "nc: {0} # number of classes\n\n".format(nc)
    break

# write everything back
with open('models/yolov5s.yaml', 'w') as yolo_yaml:
    yolo_yaml.writelines(data)