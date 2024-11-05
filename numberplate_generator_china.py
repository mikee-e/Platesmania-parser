import random
import string
import requests
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time
import os
import traceback
regions = [
            '京', '津', '冀',
            '晋', '蒙', '辽', 
            '吉', '黑', '沪', 
            '苏', '浙', '皖', 
            '闽', '赣', '鲁', 
            '豫', '鄂', '湘', 
            '粤', '桂', '琼', 
            '渝', '川', '贵', 
            '云', '藏', '陕', 
            '甘', '青', '宁',
            '新'
            ]



def generate_sequence():
    combinations = [
                "DDDDD", "LDDDD", "LLDDD",
                "DLDDD", "DDLDD", "DDDLD",
                "DDDDL", "LDDDL", "DDDLL",
                "LDLDD", "DLLDD", "LDDLD",
                "DLDLD", "DLDDL", "DDLLD",
                "DDLDL"
                ]
    # Генерируем случайную цифру
    def get_digit():
        return str(random.randint(0, 9))
    
    # Генерируем случайную букву
    def get_letter():
        return random.choice(string.ascii_uppercase)
    
    combination = random.choice(combinations)

    sequence = ""
    for char in combination:
        if char == "D":
            sequence += get_digit()
        elif char == "L":
            sequence += get_letter()
    
    return sequence

def get_html(url):
    browser = webdriver.Chrome()
    browser.get(url)

    return browser


def main():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    pages = 100
    country = "cn"
    base = f"https://platesmania.com/{country}/informer"
    try:
        os.mkdir(f"./images/{country}")
    except FileExistsError:
        pass
    driver.get(base)
    driver.maximize_window()
    
    ctype = driver.find_element(By.ID, value='ctype')
    select_ctype = Select(ctype)
    select_ctype.select_by_index(0)
    region = driver.find_element(By.ID, value='region')
    select_region = Select(region)
    select_region.select_by_value("4003")
    region2 = driver.find_element(By.ID, value='region2')
    select_region2 = Select(region2)
    select_region2.select_by_index(0)
    print(len(select_region.options), len(select_ctype.options), len(select_region2.options))
    for i in range(len(select_ctype.options)):
        try:
            select_ctype.select_by_index(i)
            current_ctype = select_ctype.all_selected_options[0].get_attribute('text')
        except:
            continue
        try:
            os.mkdir(f"images/cn/{current_ctype}")
        except:
            tb = traceback.format_exc()
            print(tb)
        for j in range(len(regions)):
            current_region = regions[j]
            try:
                os.mkdir(f"images/cn/{current_ctype}/{current_region}")
            except:
                pass
            try:
                region = driver.find_element(By.ID, value='region')
                select_region = Select(region)
                select_region.select_by_index(j + 1)

                region2 = driver.find_element(By.ID, value='region2')
                select_region2 = Select(region2)
            except:
                tb = traceback.format_exc()
                print(tb)
                continue
            for k in range(len(select_region2.options)):
                try:
                    select_region2.select_by_index(k)
                    current_region2 = select_region2.all_selected_options[0].get_attribute('text')
                except:
                    tb = traceback.format_exc()
                    print(tb)
                    continue
                try:
                    os.mkdir(f"images/cn/{current_ctype}/{current_region}/{current_region2}")
                except:
                    pass
                for _ in range(1000):
                        if len(os.listdir(f"./images/cn/{current_ctype}/{current_region}/{current_region2}/")) > 300:
                            continue
                        try:
                            ctype = driver.find_element(By.ID, value='ctype')   
                            select_ctype = Select(ctype)
                            
                            select_ctype.select_by_index(i)
                            region = driver.find_element(By.ID, value='region')
                            select_region = Select(region)
                            select_region.select_by_index(j + 1)
                            region2 = driver.find_element(By.ID, value='region2')
                            select_region = Select(region2)
                            select_region.select_by_index(k)
                            text = generate_sequence()
                            driver.find_element(By.ID, value="nomerpl").send_keys(text)
                            driver.find_element(By.NAME, value="Submit").click()
                            img = driver.find_element(By.CSS_SELECTOR, value="html body div.wrapper div.container.content div.row.blog-page div.col-md-9.col-xs-12 div.row.margin-bottom-20.bg-grey div.col-sm-12 img.img-responsive.vcenter")
                            img.screenshot(f"./images/cn/{current_ctype}/{current_region}/{current_region2}/{current_region}{current_region2}{text}.png")
                        except:
                            tb = traceback.format_exc()
                            print(tb)

    time.sleep(10)
    driver.quit()




if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except:
            continue
        break
