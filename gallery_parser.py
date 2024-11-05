from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import os
def get_html(url):
    browser = webdriver.Firefox()
    browser.get(url)

    return browser


def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Firefox(options=chrome_options)
    pages = 100
    country = "by"
    base = f"https://platesmania.com/{country}/gallery"
    try:
        os.mkdir(f"./images/{country}")
    except FileExistsError:
        pass
    for i in tqdm(range(30, pages), desc="pages:"):
        if i == 0:
            url = base
        else:
            url = base + f"-{i}"
        driver.get(url)
        numbers = driver.find_elements(By.CLASS_NAME, value='col-xs-offset-3')
        numbers = [number.get_attribute('innerHTML') for number in numbers]
        for number in numbers:
            # print(number)
            soup = BeautifulSoup(number, "html.parser")
            link = soup.find("a").get("href").replace("nomer", "foto")
            driver.get("https://platesmania.com" + link)

            image = driver.find_element(By.CLASS_NAME, value='wrapper')
            image = BeautifulSoup(image.get_attribute('innerHTML'), "html.parser")
            image_link = image.find("img").get("src")
            text = soup.find("img").get("alt")
            # print(image_link, text)
            driver.get(image_link)
            image = driver.find_element(By.XPATH, value="/html/body/img")
            image.screenshot(f"./images/{country}/{text}.png")
            # driver.get(url)
        

    driver.quit()




if __name__ == "__main__":
    main()
