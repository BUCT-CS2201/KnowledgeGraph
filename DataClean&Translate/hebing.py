import os
import pandas as pd

# 定义存放多个CSV文件的文件夹路径，可根据实际情况修改
csv_folder_path = "D:\\PythonProject\\PythonScripts\\MuseumDatabase\\11号博物馆中国文物105-152\\11号博物馆中国文物105-152"

# 定义合并后输出的CSV文件路径及文件名
output_csv_path = "merged_file_105-152.csv"

# 用于存储读取的各个CSV文件的数据框
data_frames = []

# 遍历文件夹中的所有文件
for root, dirs, files in os.walk(csv_folder_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            # 使用pandas的read_csv函数读取每个CSV文件为数据框
            df = pd.read_csv(file_path)
            data_frames.append(df)

# 使用concat函数将所有数据框按行方向进行合并
merged_df = pd.concat(data_frames, ignore_index=True)

# 将合并后的数据框写入到新的CSV文件中
merged_df.to_csv(output_csv_path, index=False)