import os
import pathlib
from PIL import Image
from argparse import ArgumentParser
import glob

def expand2square(pil_img, background_color): #  nkmk / python-tools 
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        print('w>h')
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


# config
scan_dir = pathlib.Path.cwd() / 'derpibooru_page_downloader' #\All\pinkie pAI-20200514T175116Z-001\pinkie pAI\other_ponies'
sub_dir = 'all'
output_dir = pathlib.Path.cwd() / 'dataset_twi_and_glim_fixed/'
target_size = 1024
write_mode = True # false means debug mode (print paths only)

# main loop
scan_dir_len = len(os.listdir(scan_dir / sub_dir))
ctr = 0
invalid = 0
for file_name in os.listdir(scan_dir / sub_dir): ##os.listdir(scan_dir):
    print('iter')
    if not file_name.endswith(('.jpeg', '.jpg', '.png')):
        continue

    # open
    png = Image.open(scan_dir / sub_dir / file_name)
    png.load() # required for png.split()
    
    # make transparency white
    if (len(png.split()) == 4):
        # remove transparency
        im = Image.new("RGB", png.size, (255, 255, 255))
        im.paste(png, mask=png.split()[3]) # 3 is the alpha channel
    else:
        print('no transparency')
        im = png

    # resize to square
    try:
        im = expand2square(im, (255, 255, 255))
    except Exception as e:
        invalid += 1
    # make rgb only
    im = im.convert('RGB')

    # resize to 2048
    im = im.resize((target_size, target_size), resample=3)

    # save
    
    if write_mode:
        im.save(output_dir / file_name, 'JPEG', quality=96)
    else:
        print('test> write ', output_dir / file_name)
    # progress bar
    print(str(ctr), '/', str(scan_dir_len), file_name, 'done')
    ctr += 1

print(invalid)