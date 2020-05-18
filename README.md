# stylegan2_scripts
## Create dataset:
1. pbooru_downloader.py
2. remove wrong images
3. fix_jpeg_extensions.py
4. process_to_1024.py
5. 7zip->tar folder

dataset.tar: (images processed with process_to_1024.py and fix_jpeg_extensions.py)
   img1.jpg
   img2.jpg
   img3.jpg
   ...

6. upload to gdrive
gdrive: stylegan2/my_dataset.tar

7. open colab and start training