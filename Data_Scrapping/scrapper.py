from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up the WebDriver (adjust the path to the location of your WebDriver)
driver = webdriver.Chrome()

def scrape_amazon(url):
    # Navigate to Amazon
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
                product_link = product.find_element(By.TAG_NAME, "a").get_attribute('href')
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


def scrape_information(url):
    # Navigate to the URL
    driver.get(url)
    product_info = []

    try:
        # Wait for the necessary elements to load
        wait = WebDriverWait(driver, 10)
        products = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-xs-4')))
        image = products.find_element(By.CLASS_NAME, 'card-cover')
        image_url = image.find_element(By.TAG_NAME, 'img').get_attribute('src')
        card_desc = products.find_element(By.CLASS_NAME, 'card-desc').text
        price = products.find_element(By.CLASS_NAME, 'service_price').text
        desc = card_desc.split('\n')
        title = desc[0]
        description = desc[1]

        product_info.append(title)
        product_info.append(description)
        product_info.append(price)
        product_info.append(image_url)
        product_info.append(url)
    except Exception as e:
        print(f"An error occurred for URL: {url}")
        print(str(e))

    return product_info

# base_url = 'https://www.togetherv.com/indore/balloon-decoration-for-birthday'
# base_url = 'https://www.togetherv.com/indore/balloon-bouquet'
# base_url = 'https://www.togetherv.com/indore/valentines-bouquet'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations-for-anniversary'
# base_url = 'https://www.togetherv.com/indore/ring-decorations'
# base_url = 'https://www.togetherv.com/indore/sequin-decorations'
# base_url = 'https://www.togetherv.com/indore/valentines-decor'
# base_url = 'https://www.togetherv.com/indore/womens-day-decoration'
# base_url = 'https://www.togetherv.com/indore/childrens-day'
# base_url = 'https://www.togetherv.com/indore/lohri-and-sankranti-decors'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations/office-decorations'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations/balloon-wall-decorations'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations/proposal-decor'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations/car-boot-decoration'
# base_url = 'https://www.togetherv.com/indore/balloon-decorations/bachelorette-theme-decorations'
base_url = 'https://www.togetherv.com/indore/balloon-decorations/pet-decoration'

# List of URLs
list_url = scrape_amazon(base_url)
print(len(list_url))
master_list = []
for url in list_url:
    product_info = scrape_information(url)
    if product_info:  # Only add if product_info is not empty
        master_list.append(product_info)

# Define the CSV file headers
headers = ['Title', 'Description', 'Price', 'Image URL', 'URL']

# Write the master list to a CSV file
filename = base_url.split('/')[-1]
with open(f'media/{filename}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(master_list)

print(f"Data has been written to {filename}.csv")

# Close the WebDriver
driver.quit()
