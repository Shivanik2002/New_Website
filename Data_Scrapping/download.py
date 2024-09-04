from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import requests
from io import BytesIO
import os
import time

# Set up Selenium with headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

def download_image(image_url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'https://www.togetherv.com/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(image_url, headers=headers, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content)).convert("RGB")
            jpeg_save_path = save_path.replace('.webp', '.jpg')
            os.makedirs(os.path.dirname(jpeg_save_path), exist_ok=True)
            image.save(jpeg_save_path, "JPEG")
            print(f"Image successfully downloaded and converted: {jpeg_save_path}")
        else:
            print(f"Failed to download {image_url}: {response.status_code} {response.reason}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def fetch_image_urls(url):
    driver.get(url)

    product_list = []

    while True:
        # Wait for the products container to load
        wait = WebDriverWait(driver, 10)
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "category-cards")))
        products = container.find_elements(By.CLASS_NAME, 'col-md-6')

        # Extract product links
        for product in products:
            try:
                product_link = product.find_element(By.TAG_NAME, "img").get_attribute('src')
            except:
                product_link = "N/A"
            if product_link not in product_list:
                product_list.append(product_link)
        
        try:
            # Check if the "See More" button is available and click it
            see_more_button = driver.find_element(By.ID, "see_more")
            see_more_button.click()
            
            # Wait for new products to load
            time.sleep(1)
        except:
            # No more "See More" button, break the loop
            break
    
    return product_list

# URL to fetch image URLs from
page_url = 'https://www.togetherv.com/indore/balloon-decoration-for-birthday'
image_urls = fetch_image_urls(page_url)

# Download each image
for url in image_urls:
    # Extract image name from the URL
    image_name = url.split("/")[-1]
    # Set the save path
    save_path = os.path.join('images', image_name)
    # Download and convert the image
    download_image(url, save_path)

# Close the Selenium driver
driver.quit()
