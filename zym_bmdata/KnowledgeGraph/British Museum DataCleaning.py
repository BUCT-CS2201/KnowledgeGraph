# 129和130行为爬取其实页和一共爬多少页
# #朱一鸣：写爬取代码能爬取每个主网页，从主网页查看该页中物品信息，进入物品详细页面进行爬取,自动获取每个商品自己的信息，爬完后以此类推直至爬到本页最后一个物品跳转到下一页。
# #朱一鸣：爬取每个物品自己的信息和物品图片链接,打印爬取进度。
# #知乎狗
# #解决重复爬取第一个文物的问题
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

def get_all_fields(driver):
    """获取页面上所有可用的字段和值，保持原始字段名"""
    fields_data = {}
    try:
        # 获取所有数据项
        data_items = driver.find_elements(By.CSS_SELECTOR, "div.object-detail__data-item")
        print(f"找到 {len(data_items)} 个数据项")
        
        for item in data_items:
            try:
                # 获取标签名
                label = item.find_element(By.CSS_SELECTOR, "dt.object-detail__data-term")
                label_text = label.text.strip()
                
                # 获取该标签对应的所有描述
                descriptions = item.find_elements(By.CSS_SELECTOR, "dd.object-detail__data-description")
                description_texts = [desc.text.strip() for desc in descriptions if desc.text.strip()]
                
                # 将字段和值添加到字典中，使用原始字段名
                if description_texts:
                    fields_data[label_text] = " | ".join(description_texts)
                    # print(f"发现字段: {label_text} = {fields_data[label_text][:100]}...")
                    
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"处理数据项时出错: {str(e)}")
                continue
                
        return fields_data
    except Exception as e:
        print(f"获取字段数据时出错: {str(e)}")
        return {}
def print_item_fields(item_data, page_num, item_index):
    """打印物品的所有字段信息"""
    print(f"\n{'='*50}")
    print(f"第 {page_num} 页，第 {item_index} 个物品字段详情")
    print(f"标题: {item_data.get('标题', '无标题')}")
    print(f"链接: {item_data.get('链接', '无链接')}")
    print('-'*50)
    print("字段列表:")
    
    # 遍历所有字段（除了标题、图片URL和链接）
    for field, value in sorted(item_data.items()):
        if field not in ['标题', '图片URL', '链接']:
            # 如果值太长，截断显示
            value_display = value[:100] + '...' if len(str(value)) > 100 else value
            print(f"{field}: {value_display}")
    
    print(f"{'='*50}\n")
def scrape_british_museum(p4ge):
    print("初始化无检测Chrome浏览器...")
    all_items = []
    # 用于记录所有遇到的字段
    all_encountered_fields = set()
    driver = None

    try:
        # 设置浏览器选项
        import undetected_chromedriver as uc
        options = uc.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")
        
        # 启动无检测Chrome浏览器
        driver = uc.Chrome(options=options)
        print("浏览器初始化成功")
        
        base_url = "https://www.britishmuseum.org/collection/search?keyword=chinese&place=China&view=grid&sort=object_name__asc&page="
        # 爬取其实页和一共爬多少页
        page_num = p4ge
        max_pages = p4ge

        while page_num <= max_pages:
            try:
                url = base_url + str(page_num)
                driver.get(url)
                time.sleep(random.uniform(8, 12))
                print(f"第 {page_num} 页加载完成，开始提取数据...")

                # 获取展品列表
                items = wait_and_find_elements(driver, By.CSS_SELECTOR, ".teaser__wrapper")

                if not items:
                    print("没有找到展品项目，跳过这一页。")
                    page_num += 1
                    continue
                
                print(f"找到 {len(items)} 个展品项目。")
                
                # 收集当前页面所有物品的链接
                item_links = []
                for item in items:
                    try:
                        title_elem = item.find_element(By.CSS_SELECTOR, ".teaser__title a")
                        if title_elem:
                            link = title_elem.get_attribute("href")
                            if link and link not in item_links:
                                item_links.append(link)
                    except Exception as e:
                        print(f"获取链接时出错: {str(e)}")
                        continue
                
                print(f"成功获取 {len(item_links)} 个链接")
                
                # 处理每个物品
                for item_index, link in enumerate(item_links, start=1):
                    try:
                        print(f"\n处理第 {page_num} 页，第 {item_index} 个物品: {link}")
                        driver.get(link)
                        time.sleep(random.uniform(8, 12))

                        # 获取基本信息
                        title_element = wait_and_find_element(driver, By.CSS_SELECTOR, "h2 .vterm, h1.h2")
                        title = safe_get_text(title_element, "无标题")
                        
                        img_elem = wait_and_find_element(driver, By.CSS_SELECTOR, "div.object-detail__image img")
                        image = img_elem.get_attribute("src") if img_elem else "无图片"

                        # 初始化物品数据
                        item_data = {
                            "标题": title,
                            "图片URL": image,
                            "链接": link
                        }

                        # 动态获取所有字段数据
                        fields_data = get_all_fields(driver)
                        
                        # 更新遇到的所有字段集合
                        all_encountered_fields.update(fields_data.keys())
                        
                        # 将字段数据添加到物品数据中
                        item_data.update(fields_data)
                        # print_item_fields(item_data, page_num, item_index)
                        all_items.append(item_data)
                        print(f"第 {page_num} 页，第 {item_index} 个物品数据已添加: {title}")
                        print(f"该物品包含 {len(fields_data)} 个字段")

                    except Exception as e:
                        print(f"处理物品时出错: {str(e)}")
                        continue

                page_num += 1
                time.sleep(random.uniform(8, 12))

            except Exception as e:
                print(f"处理第 {page_num} 页时出错: {str(e)}")
                page_num += 1
                time.sleep(random.uniform(12, 15))

    except Exception as e:
        print(f"浏览器初始化失败: {str(e)}")

    finally:
        # 保存数据
        if all_items:
            # 创建DataFrame时使用所有遇到过的字段
            df = pd.DataFrame(all_items)
            
            # 保存完整版本
            df.to_csv(f"大英博物馆中国文物_完整版{max_pages}.csv", index=False, encoding="utf-8-sig")
            
            # 保存简化版本（去除空值）
            df_no_empty = df.dropna(how='all', axis=1)
            df_no_empty.to_csv(f"大英博物馆中国文物_简化版{max_pages}.csv", index=False, encoding="utf-8-sig")
            
            print(f"\n数据已保存到CSV文件")
            print(f"总共抓取了 {len(all_items)} 个展品")
            print(f"遇到的所有字段: {', '.join(sorted(all_encountered_fields))}")
        
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", type=int, default=1, help="页数")
    args = parser.parse_args()
    scrape_british_museum(args.page)
    print("爬虫程序执行完毕")

