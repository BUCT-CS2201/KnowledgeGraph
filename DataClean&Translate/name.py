import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

#API
API_KEY = "sk-6cfc266025c046b3a9168c5d709c1f84"
API_URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 读取CSV文件
input_csv = "1号博物馆21-25.csv"
output_csv = "named_data_21-25.csv"
df = pd.read_csv(input_csv)

# 描述列
column_to_name = ['description']

# 翻译函数
def add_name(text):
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": f"给出的是一段文物的描述，请根据文物的描述为文物取名，要求：专业化命名，只要名字，不要有补充说明和注释，严禁添加书名号，用汉字，不要用阿拉伯数字：{text}"
            }
        ],
        "temperature":1.2
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        translated = response.json()["choices"][0]["message"]["content"]
        print(f"Name: {translated}")
        # 去除所有单双引号  # 去除可能的引号
        return translated.replace("'", "").replace('"', "")
    else:
        print(f"失败（状态码 {response.status_code}）: {text}")
        return None

# 多线程翻译
def translate_column(column_name, start_row, end_row):
    df.loc[start_row:end_row, 'name'] = df.loc[start_row:end_row, column_name].apply(add_name)

def main():
    with ThreadPoolExecutor(max_workers=16) as executor:
        # 每400行保存一次
        for i in range(0, len(df), 400):
            end_row = min(i + 399, len(df) - 1)  # 确保不超过数据框的长度
            print(f"正在翻译第 {i+1} 到 {end_row+1} 行...")
            futures = {executor.submit(translate_column, col, i, end_row): col for col in column_to_name}
            for future in as_completed(futures):
                column_name = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"翻译列 {column_name} 时出错: {e}")
            # 保存临时结果
            df[:end_row+1].to_csv(f"output_{i//400}.csv", index=False, encoding="utf_8_sig")
            print(f"已保存前 {end_row+1} 行到 output_{i//400}.csv")

    # 最终保存全部结果
    df.to_csv(output_csv, index=False, encoding="utf_8_sig")
    print(f"翻译完成！结果已保存到 {output_csv}")

if __name__ == "__main__":
    main()


