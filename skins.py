import csv
import io
from lcu_driver import Connector
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math
from tqdm import tqdm

connector = Connector()

@connector.ready
async def connect(connection):
    response_inventory = await connection.request('get', '/lol-inventory/v2/inventory/CHAMPION_SKIN')
    inventory_data = await response_inventory.json()

    inventory_data.sort(key=lambda x: datetime.strptime(x['purchaseDate'], '%Y%m%dT%H%M%S.%fZ'), reverse=True)
    
    response_skins = await connection.request('get', '/lol-game-data/assets/v1/skins.json')
    skins_data = await response_skins.json()
    
    combined_data = []
    load_screen_images = []

    for item in tqdm(inventory_data, desc="Processing skins"):
        item_id = str(item['itemId'])
        if item_id in skins_data:
            skin_name = skins_data[item_id]['name']
            splash_path = skins_data[item_id]['splashPath']
            load_screen_path = skins_data[item_id].get('loadScreenPath')
            
            champion_name = splash_path.split('/')[5]

            obtained_date = datetime.strptime(item['purchaseDate'], '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
            
            combined_entry = {
                'itemId': item['itemId'],
                'name': skin_name,
                'championName': champion_name,
                'obtained': obtained_date,
            }
            combined_data.append(combined_entry)

            if load_screen_path:
                response_image = await connection.request('GET', load_screen_path)
                if response_image.status == 200:
                    image_data = await response_image.read()
                    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
                    load_screen_images.append((image, skin_name))
    
    csv_filename = 'list.csv'
    collage_filename = 'collage.jpg'

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['itemId', 'name', 'championName', 'obtained'])
        writer.writeheader()
        writer.writerows(combined_data)
        print(f"CSV saved as {csv_filename}")

    if load_screen_images:
        collage = create_collage(load_screen_images)
        collage.save('collage.jpg')
        print(f"Collage saved as {collage_filename}")

def create_collage(images):
    img_width, img_height = 308, 560
    target_aspect_ratio = 16 / 9
    max_aspect_ratio_diff = 0.15
    text_height = 60

    num_images = len(images)

    best_columns = 1
    best_rows = num_images
    smallest_diff = float('inf')
    minimal_empty_space = float('inf')

    for columns in range(1, num_images + 1):
        rows = math.ceil(num_images / columns)
        collage_width = columns * img_width
        collage_height = rows * (img_height + text_height)
        collage_aspect_ratio = collage_width / collage_height

        aspect_ratio_diff = abs(collage_aspect_ratio - target_aspect_ratio)

        empty_space = (columns * rows) - num_images

        if aspect_ratio_diff <= max_aspect_ratio_diff:
            if empty_space < minimal_empty_space or (empty_space == minimal_empty_space and aspect_ratio_diff < smallest_diff):
                smallest_diff = aspect_ratio_diff
                minimal_empty_space = empty_space
                best_columns = columns
                best_rows = rows

    collage_width = best_columns * img_width
    collage_height = best_rows * (img_height + text_height)

    collage = Image.new('RGBA', (collage_width, collage_height), 'black')
    draw = ImageDraw.Draw(collage)

    font_size = 32
    font = ImageFont.truetype("arial.ttf", font_size)

    for idx, (image, name) in enumerate(images):
        x = (idx % best_columns) * img_width
        y = (idx // best_columns) * (img_height + text_height)
        collage.paste(image, (x, y))
        
        lines = []
        words = name.split(' ')
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width <= img_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line.strip())

        for i, line in enumerate(lines):
            text_x = x + img_width // 2
            text_y = y + img_height + 5 + i * (font_size + 5)
            draw.text((text_x, text_y), line, font=font, fill="white", anchor="mm")

    return collage.convert("RGB")

connector.start()