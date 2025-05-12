# 设置起始和结束页码
$startPage = 154
$endPage = 178
$kernel = 5
$aver = ($endPage - $startPage + 1) / $kernel

# 设置Python路径和脚本路径
$pythonPath = "D:\Anaconda3\envs\SE\python.exe"
$scriptPath = "d:\SoftwareEngineering\11号博物馆\11museum.py"

# 启动每一页的爬虫
for ($i = $startPage; $i -le $($endPage - $aver + 1); $i+=$aver) {
    $args = "`"$scriptPath`" --start $i --end $($i+$aver-1)"
    Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $args
    Write-Host "已启动第 $i 页的爬虫进程"
}
