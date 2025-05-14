import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置 DeepSeek API
API_KEY = "sk-6cfc266025c046b3a9168c5d709c1f84"  # 替换成你的API Key
API_URL = "https://api.deepseek.com/v1/chat/completions"  # 确认API地址
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 读取CSV文件
input_csv = "final_processed_data_3.csv"  # 输入文件路径
output_csv = "3.csv"  # 输出文件路径
df = pd.read_csv(input_csv)

# 选择要翻译的列
column_to_translate = ["name", "dynasty", "type", "description", "Author", "size"]

# 翻译函数
def translate_text(text):
    if pd.isnull(text):
        return None
    data = {
        "model": "deepseek-chat",  # 确认模型名称
        "messages": [
            {
                "role": "system",
                "content": f"将下面这一段文物信息翻译成中文，要求在翻译前先规范化每个英文单词对应的翻译，并且除了翻译内容请不要有多余部分（比如注解和说明等）"
            },
            {
                "role": "user",
                "content": f"Translate this precisely: {text}"
            }
        ],
        "temperature": 1
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        translated = response.json()["choices"][0]["message"]["content"]
        print(f"Translated: {translated}")
        return translated.replace("'", "").replace('"', "")  # 去除所有单双引号
    else:
        print(f"翻译失败（状态码 {response.status_code}）: {text}")
        return None

# 多线程翻译
def translate_column(column_name, start_row, end_row):
    df.loc[start_row:end_row, column_name] = df.loc[start_row:end_row, column_name].apply(translate_text)

def main():
    with ThreadPoolExecutor(max_workers=16) as executor:
        # 每400行保存一次
        for i in range(0, len(df), 400):
            end_row = min(i + 399, len(df) - 1)  # 确保不超过数据框的长度
            print(f"正在翻译第 {i+1} 到 {end_row+1} 行...")
            futures = {executor.submit(translate_column, col, i, end_row): col for col in column_to_translate}
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