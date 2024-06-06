import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# Читаем картинку как чб
directory = 'venv/img prov'

i = 0
for file in os.listdir(directory):
    filepath = os.path.join(directory, file)
    if os.path.isfile(filepath):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            i = i + 1
            cb_img = cv2.imread(filepath,cv2.IMREAD_COLOR)
            cropped_region = cb_img[2:1060, 2:1885]
            plt.imshow(cropped_region)
            plt.show()
            cv2.imwrite(f"{i}.png", cropped_region)
