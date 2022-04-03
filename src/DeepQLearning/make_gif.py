# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 16:37:46 2022

@author: korte
"""

import imageio
import os
import time

path = "C:/Users/korte/Nextcloud/Cognitive Systems/3. Semester/Intelligent Data Analysis and Machine Learning II/Project/Snake_Korte/src/QLearning/"
folder = "screenshots/"

path = path + folder

image_folder = os.fsencode(path)

filenames = []
images = []

for file in os.listdir(image_folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpeg', '.png', '.gif') ):
        filenames.append(filename)

filenames.sort() # this iteration technique has no built in order, so sort the frames

for filename in filenames:
    im = imageio.imread(str(path) + str(filename))
    images.append(im)

imageio.mimsave(os.path.join(f'gifs/movie{int(time.time())}.gif'), images, duration = 0.22) # modify duration as needed