import pandas as pd

# 读取文件
df = pd.read_csv("data.csv")

# 选择需要的列并重命名
column_need = [
    '标题',
    'Cultures/periods',
    'Object Type',
    'Description',
    'Acquisition date',
    'Producer name',
    'Dimensions',
    'Materials',
    '图片URL'
]

df_filtered = df[column_need].copy().rename(columns={
    '标题': 'name',
    'Cultures/periods': 'dynasty',
    'Object Type': 'type',
    'Description': 'description',
    'Acquisition date': 'entry_time',
    'Dimensions': 'size',
    'Producer name': 'Author',
    'Materials': 'materials'
})

# 删除重复项和空值
df_filtered = df_filtered.fillna('NULL')

# 对 type 项进行处理
df_filtered['type'] = df_filtered['type'].str.replace(r'\s*\([^)]*\)', '', regex=True)

# 对 dynasty 列进行处理
df_filtered['dynasty'] = df_filtered['dynasty'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# 对 Author 列进行处理
df_filtered['Author'] = df_filtered['Author'].str.replace(r'\([^)]*\)', '', regex=True).str.strip()

# 对 entry_time 项处理
df_filtered['entry_time'] = df_filtered['entry_time'].fillna('NULL')
df_filtered['entry_time'] = df_filtered['entry_time'].astype(str).str.replace(r'\(.*?\).*', '', regex=True)

# 对 size 项处理
def clean_size_column(series):
    series = series.str.replace(r'(\b\w+:)\s*\1', r'\1', regex=True)
    series = series.str.replace(r'(\s*\(.*?\))\1+', r'\1', regex=True)
    series = series.str.replace(r'\?', '', regex=True)
    series = series.str.replace(r'\s+', ' ', regex=True)
    series = series.str.strip()
    return series

df_filtered['size'] = clean_size_column(df_filtered['size'].astype(str))

# 添加一列 museum_id，内容全部为 1
df_filtered['museum_id'] = 1

# 将 Author 列中值为 'NULL' 的数据替换为 '不明'
df_filtered['Author'] = df_filtered['Author'].replace('NULL', '不明')

#去除数据缺失的文物
df_filtered = df_filtered[(df_filtered['dynasty'] != 'NULL') &
                          (df_filtered['materials'] != 'NULL') &
                          (df_filtered['size'] != 'NULL') &
                          (df_filtered['entry_time'] != 'NULL')]

# 保存最终结果
df_filtered.to_csv('final_processed_data_1.csv', index=False, encoding='utf-8-sig')