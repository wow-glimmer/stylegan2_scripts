# Dataset scripts for stylegan2
Scripts:
- Derpibooru downloader
- Dataset generator (Pillow)
- Training colab script
- (in dev) Image Sorter (PyQt5)

update:
+fixed jpeg extension issue
+organized configuration code


## Create dataset:
1. pbooru_downloader.py | downloads images from derpibooru.org, configure this file, you need more around 10k+ images
2. remove wrong images | remove images manually or use image_sorter.py (not finished yet)
3. (skip this step) fix_jpeg_extensions.py 
4. process_to_1024.py | configure this file, converts images to squares with white borders
5. 7zip->tar folder

Tar contents should look like this
dataset.tar: 
   1463463.jpg (images processed with process_to_1024.py)
   145814.jpg
   13891032.jpg
   ...

6. upload to google drive
gdrive: stylegan2/my_dataset.tar

7. open colab and start training
Follow instructions.
- Huge datasets  might fill virtual machine disk space
- Model checkpoints are 330mb each. Make sure you have enough space on your google drive disk, change your training option to reduce snapshot rate.
- Nvidia P100 works great, 40 minutes between ticks. (untested on nvidia k80)
- If you make bigger dataset or change type, then you can reuse your old model.

## Change pretrained model (diffrent image sizes):
Pretrained dataset can be changed to use diffrent image size. (256, 512, 1024)
Just change model file.

# get url for .pkl model
512x512 cars: !wget http://d36zk2xti64re0.cloudfront.net/stylegan2/networks/stylegan2-car-config-f.pkl
256x256 3d horses: !wget http://d36zk2xti64re0.cloudfront.net/stylegan2/networks/stylegan2-horse-config-f.pkl
or
goto https://github.com/NVlabs/stylegan2
scroll down to 'Additional Material' table
(firefox) F12>Network
Click on download url
Copy url from 200 GET http header

# modify colab
In 'install the repo' section:
Change:
   !gdown --id 1UlDmJVLLnBD9SnLSMXeiZRO6g-OMQCA_
   !mv stylegan2-ffhq-config-f.pkl network-snapshot-10000.pkl
To:
   (example, change to 256x256)
   #download pkl:
   !wget http://d36zk2xti64re0.cloudfront.net/stylegan2/networks/stylegan2-horse-config-f.pkl
   #move it:
   !mv stylegan2-horse-config-f.pkl network-snapshot-10000.pkl