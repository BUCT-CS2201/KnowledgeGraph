import numpy as np
import pandas as pd

# 读取文件
df = pd.read_csv("merged_file_museum3.csv")

# 选择需要的列并重命名
column_need = [
    '标题',
    'Period',
    'Classification',
    'Medium',
    'Accession Year',
    'People',
    'Dimensions',
    '图片URL'
]

df_filtered = df[column_need].copy().rename(columns={
    '标题': 'name',
    'Period': 'dynasty',
    'Classification': 'type',
    'Medium': 'description',
    'Accession Year': 'entry_time',
    'Dimensions': 'size',
    'People': 'Author',
})

# 删除重复项和空值
df_filtered = df_filtered.fillna('NULL')

# 添加一列 museum_id，内容全部为 3
df_filtered['museum_id'] = 3



# 替换 NULL 值
df_filtered['Author'] = df_filtered['Author'].replace('NULL', '不明')
df_filtered['entry_time'] = df_filtered['entry_time'].replace('NULL', '暂无')
df_filtered['type'] = df_filtered['type'].replace('NULL', '暂无')
df_filtered['description'] = df_filtered['description'].replace('NULL', '暂无')

# 去除 dynasty 和 size 列为 'NULL' 的数据项
df_filtered = df_filtered[(df_filtered['dynasty'] != 'NULL') &
                          (df_filtered['size'] != 'NULL') ]

def remove_after_comma(text):
    if isinstance(text, str):  # 确保处理的是字符串
        return text.split(', ')[0]  # 按 ", " 分割，取第一部分
    return text  # 非字符串（如 NaN）原样返回）

column_name = "name"
df_filtered[column_name] = df_filtered[column_name].apply(remove_after_comma)
column_name = "dynasty"
df_filtered[column_name] = df_filtered[column_name].apply(remove_after_comma)
column_name = "Author"
df_filtered[column_name] = df_filtered[column_name].apply(remove_after_comma)


# 添加一列 materials，内容全部为 '暂无'
df_filtered['materials'] = '暂无'
# 保存最终结果
df_filtered.to_csv('final_processed_data_3.csv', index=False, encoding='utf-8-sig')