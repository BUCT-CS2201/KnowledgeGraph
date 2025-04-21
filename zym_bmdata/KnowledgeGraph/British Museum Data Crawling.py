

# #朱一鸣：写爬取代码能爬取每个主网页，从主网页查看该页中物品信息，进入物品详细页面进行爬取，爬完后以此类推直至爬到本页最后一个物品跳转到下一页。
# #朱一鸣：爬取每个物品共有的信息和物品图片链接,打印爬取进度。
# #知乎狗
# #解决重复爬取第一个文物的问题
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

def get_field_by_label(driver, label_text, default="未找到"):
    """通过标签文本查找对应的数据字段"""
    print(f"正在查找字段: '{label_text}'")
    try:
        # 寻找包含指定标签的数据项
        data_items = driver.find_elements(By.CSS_SELECTOR, "div.object-detail__data-item")
        print(f"找到 {len(data_items)} 个数据项")
        
        if not data_items:
            print(f"警告: 未找到任何数据项，字段 '{label_text}' 查找失败")
            return default
            
        for i, item in enumerate(data_items):
            try:
                # 在每个数据项中查找标签
                label = item.find_element(By.CSS_SELECTOR, "dt.object-detail__data-term")
                label_content = label.text.strip() if label else ""
                print(f"  数据项 #{i+1} 标签: '{label_content}'")
                
                if label and label_text.lower() in label_content.lower():
                    print(f"  找到匹配的标签: '{label_content}'")
                    # 找到匹配的标签，获取所有对应的描述
                    descriptions = item.find_elements(By.CSS_SELECTOR, "dd.object-detail__data-description")
                    print(f"  该标签下找到 {len(descriptions)} 个描述项")
                    
                    if descriptions:
                        # 将所有描述文本合并
                        texts = [desc.text.strip() for desc in descriptions if desc.text.strip()]
                        for j, text in enumerate(texts):
                            print(f"    描述 #{j+1}: '{text}'")
                        
                        result = " | ".join(texts) if texts else default
                        print(f"  合并结果: '{result}'")
                        return result
                    else:
                        print(f"  警告: 标签 '{label_content}' 下未找到描述项")
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"  处理数据项 #{i+1} 时出错: {str(e)}")
                continue
        
        print(f"未找到标签为 '{label_text}' 的数据项，返回默认值")
    except Exception as e:
        print(f"查找字段 '{label_text}' 时出错: {str(e)}")
    
    return default


def scrape_british_museum():
    print("初始化无检测Chrome浏览器...")
    all_items = []
    driver = None

    try:
        # 设置浏览器选项
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
        #输入爬取的开始页数和爬取总页数的页数
        # 例如：page_num = 1，max_pages = 1：从第一页开始爬数据，一共爬一页。
        page_num = 1
        max_pages = 1

        while page_num <= max_pages:
            try:
                url = base_url + str(page_num)
                driver.get(url)
                time.sleep(random.uniform(8, 12))
                print(f"第 {page_num} 页加载完成，开始提取数据...")

                # 使用新的等待函数获取展品列表
                items = wait_and_find_elements(driver, By.CSS_SELECTOR, ".teaser__wrapper")

                if not items:
                    print("没有找到展品项目，跳过这一页。")
                    page_num += 1
                    continue
                
                print(f"找到 {len(items)} 个展品项目。")
                
                # 存储当前页面的链接以便稍后处理
                item_links = []
                for item_index, item in enumerate(items, start=1):
                    try:
                        title_elem = item.find_element(By.CSS_SELECTOR, ".teaser__title a")
                        if title_elem:
                            link = title_elem.get_attribute("href")
                            if link and link not in item_links:  # 避免重复链接
                                item_links.append(link)
                    except Exception as e:
                        print(f"第 {page_num} 页，第 {item_index} 个物品获取链接时出错: {str(e)}")
                        continue
                
                print(f"成功获取 {len(item_links)} 个链接")
                
                # 遍历所有获取到的链接
                for item_index, link in enumerate(item_links, start=1):
                    try:
                        print(f"第 {page_num} 页，第 {item_index} 个物品，进入物品页面: {link}")
                        driver.get(link)
                        # 使用随机等待减轻服务器负担
                        time.sleep(random.uniform(8, 12))

                        # 提取信息
                        try:
                            # 获取标题
                            title_element = wait_and_find_element(driver, By.CSS_SELECTOR, "h2 .vterm, h1.h2")
                            title = safe_get_text(title_element, "无标题")
                            print(f"第 {page_num} 页，第 {item_index} 个物品，标题: {title}")

                            # 获取图片URL
                            try:
                                img_elem = wait_and_find_element(driver, By.CSS_SELECTOR, "div.object-detail__image img")
                                image = img_elem.get_attribute("src") if img_elem else "无图片"
                                print(f"第 {page_num} 页，第 {item_index} 个物品，图片URL: {image}")
                            except Exception as e1:
                                print(f"第 {page_num} 页，第 {item_index} 个物品，获取图片失败: {str(e1)}")
                                image = "无法获取图片"

                            # 使用新函数获取各个字段
                            fields = [
                                ("物品类型", "Object Type"),
                                ("博物馆编号", "Museum number"),
                                ("描述", "Description"),
                                ("发现地点", "Findspot"),
                                ("材料", "Materials"),
                                ("尺寸", "Dimensions"),
                                ("位置", "Location"),
                                ("获取名称", "Acquisition name"),
                                ("获取日期", "Acquisition date"),
                                ("部门", "Department"),
                                ("登记号", "Registration number"),
                            ]
                            item_data = {"标题": title, "图片URL": image, "链接": link}

                            for field_name, label_text in fields:
                                try:
                                    value = get_field_by_label(driver, label_text)
                                    item_data[field_name] = value
                                    print(f"第 {page_num} 页，第 {item_index} 个物品，{field_name}: {value}")
                                except Exception as e:
                                    print(f"第 {page_num} 页，第 {item_index} 个物品，获取 {field_name} 时出错: {str(e)}")
                                    item_data[field_name] = "获取失败"

                            all_items.append(item_data)
                            print(f"第 {page_num} 页，第 {item_index} 个物品，数据已添加: {title}")
                            # 添加一个短暂的随机暂停，避免频繁请求
                            time.sleep(random.uniform(1, 3))

                        except Exception as e:
                            print(f"第 {page_num} 页，第 {item_index} 个物品，提取信息时出错: {str(e)}")
                            continue

                    except (StaleElementReferenceException, TimeoutException) as e:
                        print(f"第 {page_num} 页，第 {item_index} 个物品，处理元素时出错: {str(e)}")
                        continue

                page_num += 1
                # 页面间随机等待，减轻服务器负担
                time.sleep(random.uniform(8, 12))

            except Exception as e:
                print(f"爬取第 {page_num} 页时出错: {str(e)}")
                page_num += 1
                time.sleep(random.uniform(12, 15))

    except Exception as e:
        print(f"浏览器初始化失败: {str(e)}")

    finally:
        # 保存数据
        if all_items:
            df = pd.DataFrame(all_items)
            # 保存两个版本的文件，一个完整的
            df.to_csv("大英博物馆中国文物_完整版.csv", index=False, encoding="utf-8-sig")
            # 尝试保存一个不包含空值的简化版本
            df_no_empty = df.applymap(lambda x: x if x not in ["无描述", "未找到", "无图片", "", "无材料", "无标题"] else None).dropna(how='all', axis=1)
            df_no_empty.to_csv("大英博物馆中国文物_简化版.csv", index=False, encoding="utf-8-sig")
            print(f"数据已保存到 CSV 文件，总共抓取了 {len(all_items)} 个展品。")
        
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    scrape_british_museum()
    print("爬虫程序执行完毕")

