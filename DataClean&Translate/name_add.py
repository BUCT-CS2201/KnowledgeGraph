import pandas as pd
import re

# 文件路径配置
input_csv = "merged_file_1-55.csv"
output_csv = "merged_file_1-55_final.csv"


def clean_for_name(text):
    """专门用于name列的清洗"""
    if pd.isna(text):
        return text
    # 仅删除中文句号和空白符
    cleaned = re.sub(r'[。\s]+', '', str(text))
    return cleaned.strip()


def count_chinese(text):
    """统计汉字数量（基于原始description）"""
    if pd.isna(text):
        return 0
    return len(re.findall(r'[\u4e00-\u9fff]', str(text)))


def process_row(row):
    """处理单行数据（不修改description）"""
    original_desc = row['description']
    chinese_count = count_chinese(original_desc)

    # 满足条件时用清洗后的desc替换name
    if chinese_count < 3 and pd.notna(row['name']):
        row['name'] = clean_for_name(original_desc)
    return row


def main():
    try:
        df = pd.read_csv(input_csv)
        print(f"成功读取文件：{input_csv}")

        # 验证必要列
        if 'name' not in df.columns or 'description' not in df.columns:
            print("错误：CSV必须包含name和description列")
            return

        # 保留原始description示例
        original_sample = df.iloc[0].copy()

        # 应用处理
        df = df.apply(process_row, axis=1)

        # 显示处理效果
        print("\n处理效果示例：")
        print(f"原始 name: {original_sample['name']} | description: {original_sample['description']}")
        print(f"当前 name: {df.iloc[0]['name']} | description: {df.iloc[0]['description']}")

        # 保存结果
        df.to_csv(output_csv, index=False, encoding="utf_8_sig")
        print(f"\n处理结果已保存至：{output_csv}")

    except Exception as e:
        print(f"处理失败：{str(e)}")


if __name__ == "__main__":
    main()