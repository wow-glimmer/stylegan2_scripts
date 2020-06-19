import urllib.request
import json
import pathlib
import time


# ----------------------------------------------
# Config
# ----------------------------------------------

# TAGS SEARCH

api_url = 'https://derpibooru.org/api/v1/json/search/images?page={0}&sf=score&q={1}'

ban_list = ' -eqg, -anthro, -sketch, -screencap, -3d, -traditional art, -animated, -pixel art, -id card, -pony town, -fat, -meme, -derped, -tumblr'
ocs = 'oc, solo, pony,' + ban_list #-eqg, -anthro, -sketch, -screencap, -traditional art, -animated, -pixel art, -id card, -pony town, -fat, -meme, -derped'
pony_test = 'pony' #history is name of dataset

# configure this
twi_tags = 'twilight sparkle, upvotes.lt:400, -humanized, -3d, -anthro, solo, -eqg, -animated, -plushie, -meme, -sketch'

# filter things like captions and screenshots
filter_bad = ', -edit, -sketch, -caption, -fat, -derped, -tumblr, -animated, -pixel art, -traditional art'

# pony / starlight glimmer
twi_and_star_2_tags = 'starlight glimmer || twilight sparkle, -humanized, -3d, -anthro, solo, -eqg, -plushie, -meme, -sketch'
#starlight glimmer, twilight sparkle, -humanized, -3d, -anthro, solo, -eqg, -plushie, -meme, -sketch, -edit, -sketch, -caption, -fat, -derped, -tumblr, -animated, -pixel art, -traditional art

# CONFIG ------------------------

# set tags here
tags = twi_and_star_2_tags + filter_bad

save_folder = 'glimmy_twi_3'

# download img to hdd
download = True
# 0.5 is ok (sometimes web error), .77 now 
sleep_time = 1
# start from page X    
start_page = 1         

# images to download (converts to pages) you need 10-100k images
image_count = 100000     

#derpi api sizes https://derpibooru.org/api/v1/json/search/images?page=1&sf=score&q=pony
size = 'medium'             
file_formats = ["image/jpeg", "image/png"]


# ----------------------------------------------
# Code below
# ----------------------------------------------

pages = image_count // 15

est_time = (pages * sleep_time * 15) / 60

print('estimated time:', est_time , 'min')


output_dir = pathlib.Path.cwd() / save_folder

#process = True

start_time = time.time()
ctr = 0
for page_idx in range(start_page, pages+1):
    print('request page:', page_idx)
    time.sleep(sleep_time) # sleep

    # get page request
    req = urllib.request.urlopen(api_url.format(str(page_idx), tags).replace(' ', '%20'))

    data = req.read()
    json_object = json.loads(data.decode('utf8'))

    for image_idx, image in enumerate(json_object['images']):
        end_time = time.time()
        print('page>', str(page_idx) + '/' + str(pages), 'index>', str(image_idx)+'/15', 'dl>', ctr, '|| time left:', est_time-((end_time - start_time) / 60), 'min') # metrics
        
        if not image['mime_type'] in file_formats: continue
        image_url = image['representations'][size]
        image_url_parts = pathlib.PurePath(image_url).parts # https, derpicdn.net, img, 2020 ...

        # save with this file name
        image_filename_id = image_url_parts[6] + '.' + image_url_parts[7].split('.')[1] # id + extension 4013041350 + .png
        print('| source', image_url, '\n|    writing to:', output_dir / pathlib.Path(image_filename_id))
        if download:
            # download image request
            urllib.request.urlretrieve(image_url, output_dir / pathlib.Path(image_filename_id))
            time.sleep(sleep_time) # sleep
            ctr += 1

