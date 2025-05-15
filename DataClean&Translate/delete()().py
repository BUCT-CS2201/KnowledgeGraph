import pandas as pd
import re

# 文件路径配置
input_csv = "named_data_21-25.csv"  # 输入文件路径
output_csv = "named_data_final_21-25.csv"  # 输出文件路径


def clean_brackets(text):
    """
    清理重复括号的函数
    示例输入："铜合金钱币：开元通宝。（正面）（正面）| 单字。（背面）（背面）"
    示例输出："铜合金钱币：开元通宝。（正面）| 单字。（背面）"
    """
    if pd.isna(text):
        return text

    # 使用正则表达式匹配连续重复的括号内容
    pattern = r'([（(][^）)]+[）)])(\1)+'

    # 替换为单个括号内容
    cleaned_text = re.sub(pattern, r'\1', str(text))
    return cleaned_text


def main():
    # 读取CSV文件
    try:
        df = pd.read_csv(input_csv)
        print(f"成功读取文件：{input_csv}")
    except FileNotFoundError:
        print(f"错误：输入文件 {input_csv} 未找到")
        return
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return

    # 处理description列
    if 'description' in df.columns:
        # 应用清洗函数
        df['description'] = df['description'].apply(clean_brackets)
        print("已完成重复括号清理")
    else:
        print("错误：CSV文件中不存在 description 列")
        return

    # 保存结果
    try:
        df.to_csv(output_csv, index=False, encoding="utf_8_sig")
        print(f"处理结果已保存至：{output_csv}")
    except Exception as e:
        print(f"保存文件时发生错误：{str(e)}")


if __name__ == "__main__":
    main()