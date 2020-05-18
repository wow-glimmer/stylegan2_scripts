# stylegan2_scripts
## Create dataset:
1. pbooru_downloader.py
2. fix_jpeg_extensions.py
3. process_to_1024.py
4. 7zip->tar folder

dataset.tar: (images processed with process_to_1024.py and fix_jpeg_extensions.py)
   img1.jpg
   img2.jpg
   img3.jpg
   ...

5. upload to gdrive
gdrive: stylegan2/my_dataset.tar

6. open colab and start training