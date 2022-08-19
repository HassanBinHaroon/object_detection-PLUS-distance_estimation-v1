#!/bin/bash
# format dataset
# kitti-dataset
#    |-- test_images
#    |-- train_annots
#    `-- train_images
mkdir kitti-dataset
mv testing/image_2/ kitti-dataset/test_images
mv training/image_2/ kitti-dataset/train_images
mv training/label_2/ kitti-dataset/train_annots
rm -rf training/ testing/