from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait


def run_scraper():
    """
    Scraper module. Responsible for extracting listing-level data.
    """
    
    # Chrome configuration
    # detach=True keeps browser open after script finishes
    # useful for debugging scraping behaviour
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_experimental_option("detach", True)


    list_addresses = []
    details = []
    whole_price = []
    titles= []
    web_links = []

    # Determine number of result pages
    driver = webdriver.Chrome(options=chrome_opt)
    driver.get("https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/krakow?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC&limit=72&page=")
    time.sleep(1)
    
    # Get total number of listings displayed on page
    num_of_listenings  = driver.find_element(by= By.CSS_SELECTOR, value=".css-1cwh6ya").text
    pages = num_of_listenings.split(" ")[-1]
    
    #  Determine number of result pages
    pages = math.ceil(int(pages)/72)
    print(pages)
    driver.quit()


    
    def get_data():
        """
        Function responsible for extracting data from
        """
        listenings = driver.find_elements(By.CSS_SELECTOR, value= ".css-1lyza52")
        for item in listenings:
            try:
                title = item.find_element(by=By.CSS_SELECTOR, value=".css-16vl3c1").text
            except:
                title= None
            titles.append(title)
            try:
                address = item.find_element(by=By.CSS_SELECTOR, value=".css-oxb2ca").text
            except:
                address = None
            list_addresses.append(address)
            try:
                flat_price = item.find_element(By.CSS_SELECTOR, value= ".css-1ht00de").text
            except:
                flat_price = None
            whole_price.append(flat_price)
            try:
                rooms_m_price_floor = item.find_element(by=By.CSS_SELECTOR, value=".css-1k6eezo").text
            except:
                rooms_m_price_floor = None
            details.append(rooms_m_price_floor)
            try:
                links = item.find_element(by=By.CSS_SELECTOR, value= ".css-16vl3c1").get_attribute("href")
            except:
                links = None
    
            web_links.append(links)
            time.sleep(2)

    # Mechanism for opening next pages and calling data scraping 
    driver = webdriver.Chrome(options=chrome_opt)
    for i in range(1,pages+1):
        # driver = webdriver.Chrome(options=chrome_opt)
        next_url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/krakow?ownerTypeSingleSelect=ALL&by=LATEST&direction=DESC&limit=72&page={i}"
        driver.get(next_url)
        time.sleep(2)
        if i == 1:
            cookies = driver.find_element(By.CSS_SELECTOR, value = "#onetrust-accept-btn-handler")
            cookies.click()
        time.sleep(1)
        get_data()
        time.sleep(1)
        # driver.quit()
        # print(f"Navigated to: {driver.current_url}")
        
    driver.quit()

    # Brake down details info into separate values. There is 1 sting that is being split into 3 values 
    rooms = []
    living_area = []
    floor = []
    
    # Parse combined details into separate fields
    for i in range(len(details)):
        record = details[i].split("\n")
        rooms.append(record[1]) if len(record) > 1 else rooms.append("n/a") 
        living_area.append(record[3].split(" ")[0]) if len(record) > 1 else living_area.append("n/a") 
        floor.append(record[-1]) if len(record) == 6 else floor.append("n/a")

    whole_price_fin = [price.split("\n")[0].replace("zł", "").replace(" ", "").replace(",", ".") for price in whole_price]

    # Create dictionary
    data = {"Links": web_links, "Title" : titles , "Adress": list_addresses, "Price":whole_price_fin, "Floor":floor, "Living area": living_area, "Rooms" : rooms, }
    # print(len(titles), len(list_addresses),len(whole_price_fin),len(floor), len(web_links),len(living_area), len(rooms))

    # Load to dataframe 
    df = pd.DataFrame(data)
    
    # Remove duplicated listings
    df = df.drop_duplicates(["Title", "Adress"], keep='last')
    
    # Remove rows missing key identifiers
    df = df.dropna(subset=["Title", "Adress"])
    
    # Convert numeric columns
    df["Living area"] = pd.to_numeric(df["Living area"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    
    return df

if __name__ == "__main__":
    df = run_scraper()
    print(df.head())
    
