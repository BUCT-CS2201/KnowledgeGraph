#zx 并行脚本
# 设置起始和结束页码
$startPage = 42
$endPage = 52

# 设置Python路径和脚本路径
$pythonPath = "C:\ProgramData\anaconda3\python.exe"
$scriptPath = "d:\SoftwareEngineering\museum3\test2.py"

# 启动每一页的爬虫
for ($i = $startPage; $i -le $endPage; $i++) {
    $args = "`"$scriptPath`" --page $i"
    Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $args
    Write-Host "execute process page $i "
    Start-Sleep -Seconds 2
}
