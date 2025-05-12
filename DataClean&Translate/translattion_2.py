import pandas as pd
import requests
import time

# 配置 DeepSeek API
API_KEY = "sk-6cfc266025c046b3a9168c5d709c1f84"  # 替换成你的API Key
API_URL = "https://api.deepseek.com/v1/chat/completions"  # 确认API地址
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 读取CSV文件
input_csv = "final_processed_data_2.csv"  # 输入文件路径
output_csv = "final_translated_data_2.csv"  # 输出文件路径
df = pd.read_csv(input_csv)

# 选择要翻译的列（'）
column_to_translate = ["dynasty","type","description","Author","size","materials"]
#translated_column = ["Dimensions"]  # 新列存储翻译结果

# 翻译函数
def translate_text(text):
    data = {
        "model": "deepseek-chat",  # 确认模型名称
        "messages": [
            {
                "role": "system",
                "content": f"将下面这一段文物信息翻译成中文，要求在翻译前先规范化每个英文单词对应的翻译，并且除了翻译内容请不要有多余部分（比如注解和说明等）"},
            {
                "role": "user",
                "content": f"Translate this precisely: {text}"
            }
        ],
        "temperature":1
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        translated = response.json()["choices"][0]["message"]["content"]
        print(f"Translated: {translated}")
        return translated.replace("'", "").replace('"', "")  # 去除所有单双引号  # 去除可能的引号
    else:
        print(f"翻译失败（状态码 {response.status_code}）: {text}")
        return None

# 逐行翻译（加入延迟避免速率限制）
for former_column in column_to_translate:
    df[former_column] = df[former_column].apply(
    lambda x: translate_text(x) if pd.notnull(x) else None
)

# 保存结果
df.to_csv(output_csv, index=False, encoding="utf_8_sig")  # 保证中文不乱码
print(f"翻译完成！结果已保存到 {output_csv}")