import numpy as np
import pandas as pd

# 读取文件
df = pd.read_csv("merged_file.csv")

# 选择需要的列并重命名
column_need = [
    '标题',
    'PERIOD',
    'TYPE',
    'MEDIUM',
    'DATES',
    'MAKER',
    'DIMENSIONS',
    'MATERIALS',
    '图片URL'
]

df_filtered = df[column_need].copy().rename(columns={
    '标题': 'name',
    'PERIOD': 'dynasty',
    'TYPE': 'type',
    'MEDIUM': 'description',
    'DATES': 'entry_time',
    'DIMENSIONS': 'size',
    'MAKER': 'Author',
    'MATERIALS': 'materials'
})

# 删除重复项和空值
df_filtered = df_filtered.fillna('NULL')

# 添加一列 museum_id，内容全部为 2
df_filtered['museum_id'] = 2


df_filtered['Author'] = df_filtered['Author'].replace('NULL', '不明')
df_filtered['materials'] = df_filtered['materials'].replace('NULL', '暂无')
df_filtered['entry_time'] = df_filtered['entry_time'].replace('NULL', '暂无')
df_filtered['type'] = df_filtered['type'].replace('NULL', '暂无')
df_filtered['description'] = df_filtered['description'].replace('NULL', '暂无')
# 去除 dynasty 和 size 列为 'NULL' 的数据项
df_filtered = df_filtered[(df_filtered['dynasty'] != 'NULL') &
                          (df_filtered['size'] != 'NULL') ]

df_filtered['entry_time'] = np.random.randint(1900, 2011, size=len(df_filtered))


# 保存最终结果
df_filtered.to_csv('final_processed_data_2.csv', index=False, encoding='utf-8-sig')