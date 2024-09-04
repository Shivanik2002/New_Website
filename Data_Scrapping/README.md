# Web Scraping and Image Downloader

This project contains two Python scripts:
1. A web scraping script to extract product information from a webpage.
2. An image downloading script to download images from the extracted URLs and convert them from `.webp` format to `.jpg` format.

## Prerequisites

- Python 3.x
- Chrome WebDriver (compatible with your Chrome browser version)
- The following Python libraries:
  - `selenium`
  - `pillow`
  - `requests`

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/web-scraping-image-downloader.git
    cd web-scraping-image-downloader
    ```

2. **Set up a virtual environment:**
    ```sh
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    ```

3. **Install the required libraries:**
    ```sh
    pip install selenium pillow requests
    ```

4. **Download and set up Chrome WebDriver:**
    - Download Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - Make sure to download the version that matches your installed Chrome browser version.
    - Place the WebDriver executable in a directory that is in your system's PATH, or specify the path in the script.

## Usage

### Web Scraping Script

1. **Update the URL:**
   - Open the `scrape_products.py` file.
   - Update the `url` variable with the URL of the page you want to scrape.

2. **Run the script:**
    ```sh
    python scrape_products.py
    ```

3. **Check the CSV file:**
   - The scraped product information will be saved in the `product_info.csv` file.

### Image Downloader Script

1. **Update the URL:**
   - Open the `download_images.py` file.
   - Update the `page_url` variable with the URL of the page you want to scrape images from.

2. **Run the script:**
    ```sh
    python download_images.py
    ```

3. **Check the downloaded images:**
   - The downloaded images will be saved in the `images` directory.
   - Images will be converted to `.jpg` format.

## Scripts Overview

### scrape_products.py

The script performs the following steps:
1. **Set up Selenium with Chrome:**
   - This allows the script to navigate web pages and extract data.
2. **Scrape Product Information:**
   - Navigates to the specified URL and extracts product links, titles, descriptions, prices, and image URLs.
3. **Save to CSV:**
   - Saves the extracted product information into `product_info.csv`.

### download_images.py

The script performs the following steps:
1. **Set up Selenium with headless Chrome:**
   - This allows the script to simulate real browser behavior without opening a visible browser window.
2. **Fetch Image URLs:**
   - Navigates to the specified page URL and fetches all image URLs that match a specific pattern (images hosted on `cdn.togetherv.com`).
3. **Download and Convert Images:**
   - Downloads each image using the `requests` library.
   - Converts images from `.webp` to `.jpg` format using the `Pillow` library.
   - Saves the converted images in the `images` directory.

## Error Handling

- The scripts handle potential errors such as connection issues and invalid responses.
- If an image fails to download, the script prints an error message with the URL and reason for the failure.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or suggestions, please contact [your email address].
