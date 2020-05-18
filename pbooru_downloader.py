import urllib.request
import json
import pathlib
import time
download = True
sleep_time = .5

#  target data set  5k images 50/50
# glimmy 164 (6th img? from memory)  (2444)
# twily 150 (3rd image)  (2228)
start_page = 150
def img_to_pages(target_image_count):
    print(target_image_count // 15)
api_url = 'https://derpibooru.org/api/v1/json/search/images?page={0}&q={1}'

# configure this
twi_tags = 'twilight sparkle, upvotes.lt:400, -humanized, -3d, -anthro, solo, -eqg, -animated, -plushie, -meme, -sketch'
star_tags = 'starlight glimmer, upvotes.lt:400, -humanized, -3d, -anthro, solo, -eqg, -animated, -plushie, -meme, -sketch'
tags = twi_tags
pages = 10000//15 # images / 15 # 164=~2444 imgs
size = 'medium'
file_formats = ["image/jpeg", "image/png"]

est_time = (pages * sleep_time * 15) / 60

print('estimated time:', est_time , 'min')


output_dir = pathlib.Path.cwd() / 'twily'

#process = True

start_time = time.time()
ctr = 0
for page_idx in range(start_page, pages+1):
    print('request page:', page_idx)
    req = urllib.request.urlopen(api_url.format(str(page_idx), tags).replace(' ', '%20'))
    data = req.read()
    json_object = json.loads(data.decode('utf8'))

    for image_idx, image in enumerate(json_object['images']):
        end_time = time.time()
        print('page>', str(page_idx) + '/' + str(pages), 'index>', str(image_idx)+'/15', 'dl>', ctr, '|| time left:', est_time-((end_time - start_time) / 60), 'min') # metrics
        
        if not image['mime_type'] in file_formats: continue
        image_url = image['representations'][size]
        image_url_parts = pathlib.PurePath(image_url).parts # https, derpicdn.net, img, 2020 ...
        image_filename_id = image_url_parts[6] + image_url[-4:] # id + extension 4013041350 + .png
        print('| source', image_url, '\n|    writing to:', output_dir / pathlib.Path(image_filename_id))
        if download:
            urllib.request.urlretrieve(image_url, output_dir / pathlib.Path(image_filename_id))
            time.sleep(sleep_time)
            ctr += 1

