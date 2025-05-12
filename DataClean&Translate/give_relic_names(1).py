import pandas as pd
import requests

#API
API_KEY = "sk-6cfc266025c046b3a9168c5d709c1f84"
API_URL = "https://api.deepseek.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 读取CSV文件
input_csv = ".csv"
output_csv = ".csv"
df = pd.read_csv(input_csv)

# 描述列
column_to_change = ['']

# 翻译函数
def add_name(text):
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": f"给出的是一段文物的描述，请根据文物的描述为文物取名，请专业一点（只要名字，不要有补充说明和注释）：{text}"
            }
        ],
        "temperature":1.3
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

# 翻译
for former_column in column_to_change:
    df[former_column] = df[former_column].apply(
    lambda x: add_name(x) if pd.notnull(x) else None
)

# 保存结果
df.to_csv(output_csv, index=False, encoding="utf_8_sig")
print(f"翻译完成！结果已保存到 {output_csv}")