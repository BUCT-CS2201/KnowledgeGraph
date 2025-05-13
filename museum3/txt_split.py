def split_txt_by_lines(file_path, lines_per_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total = len(lines)
    for i in range(0, total, lines_per_file):
        chunk = lines[i:i + lines_per_file]
        with open(f"{file_path.rstrip('.txt')}_{i//lines_per_file + 1}.txt", 'w', encoding='utf-8') as f_out:
            f_out.writelines(chunk)

# 示例用法
split_txt_by_lines('第三个博物馆\item_links.txt', 100)
