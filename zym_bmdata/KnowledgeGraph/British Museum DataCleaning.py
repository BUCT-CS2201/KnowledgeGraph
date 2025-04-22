import pandas as pd

# 读取文件
df = pd.read_csv("大英博物馆中国文物_完整版.csv")

# 选择需要的列并重命名
column_need = [
    'Museum number',
    '标题',
    'Object Type',
    'Description',
    'Materials',
    'Dimensions',
    'Acquisition date',
    '链接',
    '图片URL',
    'Production date'
]

df_filtered = df[column_need].copy().rename(columns={
    'Museum number': '博物馆编号',
    'Object Type': '类型',
    'Description': '描述',
    'Materials': '材料',
    'Dimensions': '尺寸',
    'Acquisition date': '收录日期',
    '链接': '链接',
    '图片URL': '图片地址',
    'Production date': '制作时间'
})

# 修改正则表达式模式 - 使用非捕获组(?:)替代捕获组()
pattern = r'^\d+,\d+,\d+\.\d+(?:-\d+)?\.?\w*$'

# 过滤博物馆编号格式
df_filtered = df_filtered[
    df_filtered['博物馆编号'].str.contains(pattern, na=False, regex=True)
].copy()

# 填充制作时间为空的值为'不明'
df_filtered['制作时间'] = df_filtered['制作时间'].fillna('不明')

# 删除制作时间中的所有形如（）（）的内容
df_filtered['制作时间'] = df_filtered['制作时间'].str.replace(r'\(\s*.*?\)\s*', '', regex=True).str.strip()

# 替换图片地址为空的数据为‘暂无’
df_filtered['图片地址'] = df_filtered['图片地址'].fillna('暂无')

# 删除重复项和空值
df_filtered = df_filtered.drop_duplicates(subset=['博物馆编号'])
df_filtered = df_filtered.dropna(subset=['类型', '尺寸', '描述', '材料', '收录日期', '链接'])

# 保存最终结果
df_filtered.to_csv('final_processed_data.csv', index=False, encoding='utf-8-sig')
