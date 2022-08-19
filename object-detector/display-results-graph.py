import cv2
import matplotlib.pyplot as plt

# display results image
# imread() reads image as grayscale, second argument is one => grayscale, zero => RGB 
img = cv2.imread('training-results/results.png', 0)
plt.imshow(img)
plt.axis('off')
