# League of Legends Skin Collage Generator

This project is a Python script that connects to the League of Legends client, retrieves information about the champion skins you own, and generates a visual collage of those skins along with a CSV file containing details about each skin.

## Features

- **Retrieve Skin Data:** The script connects to the League of Legends client and retrieves information about all the champion skins in your inventory.
- **Sort by Acquisition Date:** The skins are sorted by the date they were obtained, from newest to oldest.
- **Generate Collage:** A collage of the skin splash arts is created, with the skin names displayed below each image.
- **Export Data:** The skin data is exported to a CSV file (`list.csv`), containing details such as item ID, skin name, champion name, and the date the skin was obtained.

## Requirements

To run this project, you need Python installed on your machine. You can install the required Python packages using `pip` and the provided `requirements.txt` file.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies

- `lcu-driver`: A Python library to interact with the League of Legends client.
- `Pillow`: A Python Imaging Library used to create and manipulate images.
- `tqdm`: A library used to show a progress bar in the console while processing the skins.

## Usage

1. **Ensure League Client is Running:** The script requires the League of Legends client to be open and running.

2. **Run the Script:**

   ```bash
   python skins.py
   ```

   This will connect to your League of Legends client, retrieve the skin data, and generate a collage as well as a CSV file with the details.

3. **Output Files:**
   - `collage.jpg`: The generated collage of your champion skins.
   - `list.csv`: A CSV file containing detailed information about each skin in your inventory.

### Example Output

- **Collage Example:** 

   ![Example Collage](example_collage.jpg)

- **CSV Example:** 

   | itemId  | name                  | championName | obtained           |
   |---------|-----------------------|--------------|--------------------|
   | 63008   | Eternal Dragon Brand  | Brand        | 2024-07-28 15:29:15|
   | 131047  | Winterblessed Diana   | Diana        | 2024-07-24 18:15:12|
   | ...     | ...                   | ...          | ...                |

## Customization

- **Change Collage Dimensions:** You can adjust the dimensions of the collage by modifying the variables `img_width`, `img_height`, and `text_height` in the `create_collage` function.
- **Font and Text Settings:** Customize the font size, style, and colors by adjusting the `font_size`, `font`, and `fill` parameters in the text drawing section of the `create_collage` function.
- **CSV and Collage Filenames:** The script can be easily modified to save the CSV and collage files with custom names or to include timestamps.

## Contributing

If you have suggestions for improving this project or find any issues, feel free to create a pull request or open an issue on GitHub.

## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE.md) file for more details.
