# config
dir = 'my_dataset/original_characters/'

# script
import os
for file in os.listdir(dir):
    src = dir + file
    dest = dir + file[:-4] + '.jpeg'
    if src.endswith('jpeg') and src[-5] != '.':
        print(src, dest)
    os.rename(src, dest)
