import csv
import re
import pandas as pd

# 配置输入输出文件名（根据实际情况修改）
input_filename = 'merged_file_1-178.csv'  # 输入的CSV文件
output_filename = 'merged_file_1-178_final.csv'  # 输出的处理结果文件

def clean_newlines(text):
    """替换所有换行符为空格并统计"""
    cleaned = re.sub(r'\r?\n', ' ', text)
    replaced_count = len(re.findall(r'\r?\n', text))
    cleaned = re.sub(r'[ 　]+', ' ', cleaned)  # 正则匹配半角空格和全角空格
    space_replaced = len(re.findall(r'[ 　]{2,}', cleaned))

    return cleaned.strip(), replaced_count
# 处理CSV文件
with open(input_filename, mode='r', encoding='utf-8-sig') as infile, \
        open(output_filename, mode='w', newline='', encoding='utf-8-sig') as outfile:
    # 创建读写对象
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

    # 写入标题行
    writer.writeheader()

    # 逐行处理数据
    for row in reader:
        for key in row:
            original = row[key]
            # 替换换行符并统计
            cleaned_text, count = clean_newlines(original)
            row[key] = cleaned_text
        if 'name' in row:  # 确保存在name列
            # 删除书名号（同时移除《和》）
            cleaned = row['name'].replace('《', '').replace('》', '')
            # 第二步：删除中文括号及其内容（使用正则表达式）
            cleaned = re.sub(r'（.*?）', '', cleaned)  # 关键修改点

            wall_keywords = ['北墙', '东墙', '南墙', '西墙']
            if any(kw in cleaned for kw in wall_keywords):
                cleaned = '墙砖拓片'
                print(f"替换触发", cleaned)
            if cleaned.strip() == '' or cleaned.strip() == 'RO8' or cleaned.strip() == 'M1和M2' or cleaned.strip() == 'Ram':
                continue  # 跳过当前行
            row['name'] = cleaned
        if 'Author' in row:  # 注意列名大小写
            # 删除中文括号及其内容
            cleaned_author = re.sub(r'（.*?）', '', row['Author'])
            if '，' in cleaned_author:  # 使用中文全角逗号
                cleaned_author = cleaned_author.split('，', 1)[0].strip()
                print(f"分割触发：", cleaned_author)
            if '无法翻译' in cleaned_author:  # 使用中文全角逗号
                cleaned = '匿名'
            if cleaned_author == '无法翻译':
                cleaned_author = '不明'
            row['Author'] = cleaned_author
        if 'materials' in row:  # 注意列名大小写
            # 删除中文括号及其内容
            cleaned_mater = re.sub(r'（.*?）', '', row['materials'])
            row['materials'] = cleaned_mater
        if 'type' in row:  # 注意列名大小写
            # 删除中文括号及其内容
            cleaned_type = re.sub(r'（.*?）', '', row['type'])
            row['type'] = cleaned_type
        if 'size' in row:  # 注意列名需与实际CSV一致
            original_size = row['size']
            if original_size == '见单独记录' or original_size == '见注释/文本输入':
                row['size'] = '不明'
        writer.writerow(row)

print(f"处理完成！清理后的文件已保存至: {output_filename}")