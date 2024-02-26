from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from art import tprint
from colorama import init
from colorama import Fore, Style
from selenium.webdriver.common.window import WindowTypes
import re
import os
from pathlib import Path
from shutil import rmtree

init()
driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)

os.system("cls")

tprint("WildImagePars")

with open("Links.txt") as f:
    links = f.read().split("\n")
loading_links = 0

print(Fore.GREEN + "Ссылки загружены в очередь успешно." + Style.RESET_ALL)

for path in Path('Results').glob('*'):
    if path.is_dir():
        rmtree(path)
    else:
        path.unlink()

print("\nЖурнал событий:")

links_number = 1

flag = True


def loading_page():
    print(Fore.GREEN + "\n╔ Начал работать c " + links[loading_links] + Style.RESET_ALL)
    # wait_link = str(input(Fore.GREEN + "Введите ссылку на товар: " + Style.RESET_ALL))

    driver.get(links[loading_links])
    time.sleep(5)

    element = driver.find_element(by=By.XPATH, value='//div[@class="product-page__bottom section-border"]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(5)

    element = driver.find_element(by=By.ID, value='Comments')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(10)

    element = driver.find_element(by=By.XPATH, value='//div[@class="product-page__bottom section-border"]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(5)

    element = driver.find_element(by=By.ID, value='Comments')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(5)

    element = driver.find_element(by=By.XPATH, value='//div[@class="swiper-slide img-plug swiper-slide-active"]')
    element.click()
    time.sleep(5)

    def parser():
        global loading_links
        global links_number
        global flag

        links_name = "Link" + str(links_number)
        os.makedirs(os.path.join("Results", links_name))
        count_image = driver.find_element(by=By.XPATH, value='//h3[@class="gallery-set__title"]').text

        print(Fore.GREEN + "║ Всего фотографий: " + re.sub("[^0-9]", "", count_image) + Style.RESET_ALL)
        print(Fore.GREEN + "║ Фотографии будут сохранятся в папку Link" + str(links_number) + Style.RESET_ALL)

        image_count = 0
        image_count_loading = int(re.sub("[^0-9]", "", count_image))

        while flag:

            image_page = "Results\Link" + str(links_number) + "\img" + str(image_count) + ".png"
            new_image = driver.find_element(by=By.XPATH,
                                            value='//div[@class="swiper-slide img-plug swiper-slide-active"]/img[@class="swiper-lazy swiper-lazy-loaded"]').get_attribute(
                "src")

            driver.switch_to.new_window(WindowTypes.TAB)
            driver.get(new_image)

            time.sleep(1)

            download_image = driver.find_element(by=By.XPATH, value='//body/*').screenshot_as_png
            # new_image = driver.find_element(by=By.XPATH, value='//div[@class="swiper-slide img-plug swiper-slide-active"]/img[@class="swiper-lazy swiper-lazy-loaded"]').screenshot_as_png

            with open(image_page, 'wb') as file:
                file.write(download_image)

            windows = driver.window_handles
            driver.close()
            driver.switch_to.window(windows[0])
            image_count += 1
            image_count_loading = image_count_loading - 1

            if image_count_loading == 0:
                flag = False

            else:
                button = driver.find_element(by=By.XPATH, value='//button[@class="swiper-button-next"]')
                button.click()
                time.sleep(1)

        if not flag:

            save_link = open("Results\Link" + str(links_number) + "\Link.txt", "w")
            save_link.write(links[loading_links])
            save_link.close()

            print(Fore.GREEN + "╚ Завершил парс ссылки." + Style.RESET_ALL)

            loading_links += 1
            links_number += 1

            flag = True

            loading_page()

    parser()


loading_page()
