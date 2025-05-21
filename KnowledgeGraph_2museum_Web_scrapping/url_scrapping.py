#zx:用于爬取文物url
#仅仅需修改80和81行的参数

import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException

def wait_and_find_element(driver, by, value, timeout=20):
    """安全地等待和查找元素，处理 StaleElementReferenceException"""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(3):  # 最多重试3次
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except StaleElementReferenceException:
            if attempt == 2:  # 最后一次尝试
                raise
            time.sleep(2)
            continue
        except TimeoutException:
            print(f"超时：未找到元素 {value}")
            return None
    return None

def wait_and_find_elements(driver, by, value, timeout=20):
    """安全地等待和查找多个元素，处理 StaleElementReferenceException"""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(3):  # 最多重试3次
        try:
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return elements
        except StaleElementReferenceException:
            if attempt == 2:  # 最后一次尝试
                raise
            time.sleep(2)
            continue
        except TimeoutException:
            print(f"超时：未找到元素集合 {value}")
            return []
    return []

def safe_get_text(element, default=""):
    """安全地获取元素文本"""
    try:
        return element.text.strip() if element else default
    except (StaleElementReferenceException, AttributeError):
        return default
    except Exception as e:
        print(f"获取文本时出错: {str(e)}")
        return default
    
def scrape_british_museum():
    print("初始化无检测Chrome浏览器...")
    # 用于记录所有遇到的字段
    driver = None

    try:
        # 设置浏览器选项
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--headless')
        
        # 启动无检测Chrome浏览器
        driver = uc.Chrome(options=options)
        print("浏览器初始化成功")
        
        base_url = "https://artmuseum.princeton.edu/search/collections?mainSearch=%22Chinese%22&resultssortOption=%22Best+Match%22&results=1"
        
        #爬取{start_page}到{end_page}之间所有文物的url
        start_page = 180
        end_page = 305

        try:
            driver.get(base_url)

            page_num = 1 #当前翻到的页码

            #该循环用于将页数翻到开始页面
            while page_num < start_page:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']") #按钮css格式需要明确
                    next_button.click()
                    time.sleep(2)  # 等待页面加载
                    page_num += 1
                except:
                    print("找不到下一页按钮，或者已到最后一页")
                    break
            print(f"已翻到第{page_num}页")

            item_links = []
            while page_num <= end_page:
                try:
                    items = wait_and_find_elements(driver, By.CSS_SELECTOR, ".result-item")
                    if not items:
                        print("没有找到展品项目，跳过这一页。")
                        page_num += 1
                        continue

                    # 收集当前页面所有物品的链接
                    for item in items:
                        try:
                            title_elem = item.find_element(By.CSS_SELECTOR, "a")
                            if title_elem:
                                link = title_elem.get_attribute("href")
                                if link and link not in item_links:
                                    item_links.append(link)
                        except Exception as e:
                            print(f"获取链接时出错: {str(e)}")
                            continue
                
                    next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']") #按钮css格式需要明确
                    next_button.click()
                    time.sleep(2)  # 等待页面加载
                    page_num += 1
                except:
                    print("找不到下一页按钮，或者已到最后一页")
                    break

            print(f"成功获取 {len(item_links)} 个链接")

            #链接保存下来
            with open(".\item_links.txt", "w", encoding="utf-8") as f:
                for link in item_links:
                    f.write(link + "\n")


        except Exception as e:
            print(f"爬取url出错: {str(e)}")
                
            

    except Exception as e:
        print(f"浏览器初始化失败: {str(e)}")

    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    scrape_british_museum()
    print("爬虫程序执行完毕")
