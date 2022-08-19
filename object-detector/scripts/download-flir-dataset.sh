#!/bin/bash
pip install -q kaggle
pip install gdown
gdown 1Q_KA7l5j3j7A4xn4UjJ2-Kw3EA-cYlxN
mkdir ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d deepnewbie/flir-thermal-images-dataset
unzip flir-thermal-images-dataset.zip
rm -rf flir-thermal-images-dataset.zip