import csv
import re
import pandas as pd

# 配置输入输出文件名（根据实际情况修改）
input_filename = 'merged_file_1-178.csv'  # 输入的CSV文件
output_filename = 'merged_file_1-178_final.csv'  # 输出的处理结果文件

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
            row['Author'] = cleaned_author
        if 'materials' in row:  # 注意列名大小写
            # 删除中文括号及其内容
            cleaned_mater = re.sub(r'（.*?）', '', row['materials'])
            row['materials'] = cleaned_mater
        if 'type' in row:  # 注意列名大小写
            # 删除中文括号及其内容
            cleaned_type = re.sub(r'（.*?）', '', row['type'])
            row['type'] = cleaned_type
        writer.writerow(row)

print(f"处理完成！清理后的文件已保存至: {output_filename}")