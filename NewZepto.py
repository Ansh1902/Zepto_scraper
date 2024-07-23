import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import re

class ZeptoProcessor:
    def __init__(self, base_url, driver_location, folder_location):
        self.base_url = base_url
        self.driver_location = driver_location
        self.folder_location = folder_location

        # Set up Chrome options
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-geolocation")

        # Initialize the driver with the options
        service = Service(self.driver_location)
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

        # Disable geolocation via DevTools Protocol
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 0,
            "longitude": 0,
            "accuracy": 1
        })

        # Initialize search box once
        

    def initialize_search_box(self):
        try:
            time.sleep(2)
            print("*******")
            search_box= self.driver.find_elements(By.XPATH,"//span[@class='flex flex-1 items-center gap-x-1 text-md font-extralight text-gray-700']")[1]            
            print("Found search bar")
            search_box.click()
        except Exception as e:
            print(f"Error initializing search box: {e}")

    def set_location(self, location_name):
        # self.driver.get(self.base_url)
        # wait = WebDriverWait(self.driver, 15)

        # # Click on "type manually" button
        # location_button = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//p[@class="font-norms block typography_caption-small__L5leZ   !text-sm !font-medium !tracking-[0.5px]" and text()="Type manually"]')))
        # location_button[1].click()

        # # Input search address
        # search_address = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="input_text-input__u6h6_ bg-transparent input_md__53jg2 !text-sm"]')))
        # search_address.send_keys(location_name)
        # time.sleep(1)
        # # Select the address from the dropdown
        # address_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ml-4 w-full undefined undefined border-b border-skin-primary-void/10 pb-4"]')))
        # address_option.click()
        # time.sleep(2)

        # # Confirm the address
        # confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class=" py-1 px-7 text-base button_btn-contained__tVXyZ w-full border-skin-primary border !py-3.5 font-bold false "]')))
        # confirm_button.click()
        # time.sleep(1)
        # pincode = self..get_pincode(location_name)
        # print("OBTAINED PINCODE:", pincode)
       
        start_time = time.time()
        try:
            # lat, lon = self.selenium.get_coordinates(location)
            # print(lat,lon)
            # if lat is not None and lon is not None:
            #     self.selenium.set_geolocation(lat,lon)
            # else:
            #     print("Failed to get coordinates for the location")
            
            print("---------setting the delivery location--------")
            print(f"Opening Zepto page: {self.base_url}")
            self.driver.get(self.base_url)
            wait=WebDriverWait(self.driver,10)
            print("clicking the delivery area")
            # Click on "type manually" button
            
            location_button = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//p[contains(@class,"typography_caption-small__L5leZ") and text()="Type manually"]')))
            print("Found type manually button")
            location_button[1].click()
            print("Clicked on type manually button")

            # Input search address
            search_address = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "input_text-input__u6h6_")]')))
            print("found search address bar")
            search_address.send_keys(location_name)
            print("Entered pincode")
            time.sleep(1)
            # Select the address from the dropdown
            address_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ml-4 w-full undefined undefined border-b border-skin-primary-void/10 pb-4"]')))
            address_option.click()
            time.sleep(2)

            # Confirm the address
            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class=" py-1 px-7 text-base button_btn-contained__tVXyZ w-full border-skin-primary border !py-3.5 font-bold false "]')))
            confirm_button.click()
            time.sleep(1)
            address=wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,'/html/body/div/div/div/header[1]/div[1]/div/button/span')
                )
            ).text
            print("-------------")
            print(f"location set to: {address}")

            print(
                f"Time taken to set delivery location: {time.time()-start_time} seconds"
            )
        except Exception as e:
            print(f"Error occurred while setting delivery location: {e}")
        self.initialize_search_box()

    def load_products(self, csv_path):
        df = pd.read_csv(csv_path)
        return df['Name'].tolist()

    def search_product(self, item_name: str, Name, Price):
        try:
            wait = WebDriverWait(self.driver, 10)

            print(f"Searching for: {item_name}")
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@id,":--input")]')))
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)
            search_input.send_keys(item_name)
            search_input.send_keys(Keys.RETURN)

            time.sleep(3)  # Wait for search results to load

            self._extract_search_results(wait, Name, Price)
            return True

        except Exception as e:
            print(f"Error occurred during search: {e}")
            return False

    def _extract_search_results(self, wait: WebDriverWait, Name, Price):
        try:
            print("Finding item")
            items = self.driver.find_elements(By.XPATH, './/a[@class="!p-2 relative my-3 mb-9 rounded-t-xl rounded-b-md product-card_product-card-wrap__Wo0Nb"]')

            if items:
                item = items[0]
                print("Item found")

                time.sleep(2)
                name = item.find_element(By.XPATH, ".//h5[@class='font-norms block typography_h5__UTaxj  typography_line-clamp-2__oj8Jo !text-base !font-semibold !h-9 !tracking-normal px-1.5']").text
                print(name)
                Name.append(name)

                price = item.find_element(By.XPATH, ".//h4[@class='font-norms block typography_h4__XDrlA  typography_line-clamp-1__diiAn !font-semibold !text-md !leading-4 !m-0']").text
                price = re.sub(r'[^\d.]', '', price)
                print(price)
                Price.append(float(price))

            else:
                print("No items found")

        except Exception as e:
            print(f"Error occurred during result extraction: {e}")

    def write_to_csv(self, Name, Price, csv_file):
        df = pd.DataFrame({'Name': Name, 'Price': Price})
        df.to_csv(csv_file, index=False)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    base_url = r"https://www.zeptonow.com/"
    driver_location = r'C:\Users\ANSH\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    folder_location = r'C:\Users\ANSH\Downloads'
    csv_path = 'grocery.csv'
    location_name = "Whitefield, Bengaluru, Karnataka, India"

    processor = ZeptoProcessor(base_url, driver_location, folder_location)
    processor.set_location(location_name)
    products = processor.load_products(csv_path)
    
    Name = []
    Price = []

    for product in products:
        success = processor.search_product(product, Name, Price)
        if not success:
            print(f"Failed to search for product: {product}")

    processor.write_to_csv(Name, Price, 'Zepto_data.csv')
    processor.close()
