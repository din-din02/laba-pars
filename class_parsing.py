from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from random import randint
import pandas as pd

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs)
        end_time = time.time()   
        
        execution_time = end_time - start_time
        log_message = f"Функция: {func.__name__} — Время выполнения: {execution_time:.2f} сек.\n"
        print(log_message.strip())

        with open("py_log.txt", "a", encoding="utf-8") as f:
            f.write(log_message)
            
        return result
    return wrapper


class Parser():
    def __init__(self):
        self.path='https://1k.by/'
        options = Options()
        self.driver = webdriver.Firefox(options=options)
        self.links_list=[]
        self.info_list = []
        self.csv_path = "smart_watch.csv"

    def __del__(self):
        print('driver quit')

    @log_execution_time
    def proxy(self):
            with open(r"C:\Users\Home\Desktop\Всё мое\прога\laba parsing\proxy_list.txt", 'r') as proxlist:
                proxy_list = proxlist.read()
            proxy_list1=proxy_list.split('\n')

            print(len(proxy_list1))
            proxy = proxy_list1[randint(0, len(proxy_list1)-1)]
    
            self.profile = FirefoxProfile()
            options = Options()
            options.profile = self.profile
            profile = self.profile
            profile.set_preference("general.useragent.override", "Godzilla/5.0 (Linux Ubuntu 22.04 LTS; x64; rv:22.04) Gecko/20100101 Firebox/121.0")
            ip, port = proxy.split(':')
    
            # Ручная настройка прокси
            profile.set_preference("network.proxy.type", 1)  # 1 = ручная настройка
            profile.set_preference(f"network.proxy.http", f"{ip}")
            profile.set_preference(f"network.proxy.http_port", port)
            profile.set_preference(f"network.proxy.ssl", f"{ip}")
            profile.set_preference(f"network.proxy.ssl_port", port)
            profile.set_preference("network.proxy.no_proxies_on", "localhost, 127.0.0.1")
            options = Options()
            options.profile = profile
            print(ip, port)

    @log_execution_time
    def processing(self):
        self.driver.get(self.path)
        time.sleep(1.3)

        cookie=self.driver.find_element(By.XPATH, '/html/body/div/main/div[3]/div/div[3]/button[4]')
        cookie.click()
        time.sleep(0.6)
        watch_path=self.driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/div/div[10]/nav/a[1]')
        watch_path.click()
        time.sleep(2.5)

    @log_execution_time
    def watch_parametrs(self):
        input1=self.driver.find_element(By.XPATH, '//*[@id="pricemin"]')
        time.sleep(0.6)
        input1.send_keys(111)

        input2=self.driver.find_element(By.XPATH, '//*[@id="pricemax"]')
        time.sleep(0.7)
        input2.send_keys(1234)

        button_watch=self.driver.find_element(By.XPATH, '//*[@id="formchoice"]/div[6]/div[2]/div/label[2]/span/i')
        time.sleep(0.6)
        button_watch.click()

        prog_watc=self.driver.find_element(By.XPATH, '/html/body/div[2]/main/div[3]/div[2]/form/div[11]/div/div/div/label/input')
        time.sleep(0.8)
        prog_watc.click()

        button_itog=self.driver.find_element(By.XPATH, '//*[@id="formchoice"]/div[32]/button[1]/span/span')
        time.sleep(1.3)
        button_itog.click()

    @log_execution_time
    def get_links_on_page(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'prod__head')
        for element in elements:
            link = element.find_element(By.TAG_NAME, 'a')
            self.links_list.append(link.get_attribute('href'))
        print(self.links_list)

    @log_execution_time
    def go_to_the_next_page(self):
        clickable_element=self.driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[1]/div[43]/nav/a")
        time.sleep(0.7)
        clickable_element.click()

    @log_execution_time
    def get_info(self):
        for link in self.links_list:
            self.proxy()
            self.driver.get(link)
            time.sleep(6)
            model_data={}
            model_data['Название модели'] = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/h1').text.strip()
            rows = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'spec-info__main')]//tr")
            print(f"Найдено строк характеристик: {len(rows)}") 

            for row in rows:
                    cells = row.find_elements(By.XPATH, "./th | ./td")
                    if len(cells) == 2:
                        raw_key = self.driver.execute_script("return arguments[0].textContent;", cells[0])
                        val_cell = cells[1]
                        val_text = self.driver.execute_script("return arguments[0].textContent;", val_cell).strip()
                        key = raw_key.replace('?', '').strip()

                        if not val_text:
                            if cells[1].find_elements(By.XPATH, ".//*[contains(@class, 'i-x')]"):
                                model_data[key] = 'No'
                            else:
                                model_data[key] = 'Yes'
                        else:
                            model_data[key] = val_text

            self.info_list.append(model_data)
            print(self.info_list)
        self.driver.quit()

    @log_execution_time
    def save_with_pandas(self):
            df = pd.DataFrame(self.info_list)

            if 'Название модели' in df.columns:
                model_col = df.pop('Название модели')
                df.insert(0, 'Название модели', model_col)
            
            df.to_csv(self.csv_path, index=False, sep=';', encoding='utf-8-sig')
