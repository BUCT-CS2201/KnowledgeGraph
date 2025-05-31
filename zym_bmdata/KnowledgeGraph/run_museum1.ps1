# 运行须知：
# 并行脚本
# $pythonPath需要修改为计算机上已配置好的能够用于运行python程序的虚拟环境的路径
# $scriptPath需要修改为test2.py所在的路径

# 脚本运行命令
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 
# .\run_museum3.ps1


# 设置起始和结束页码
$startPage = 60
$endPage = 65

# 设置Python路径和脚本路径
$pythonPath = "D:/anaconda/envs/DL/python.exe"
$scriptPath = "d:/ruanjian/zym_bmdata/KnowledgeGraph/output/British_Museum_Data_Crawling.py"

# 启动每一页的爬虫
for ($i = $startPage; $i -le $endPage; $i++) {
    $args = "`"$scriptPath`" --page $i"
    Start-Process -NoNewWindow -FilePath $pythonPath -ArgumentList $args
    Write-Host "execute process page $i "
    Start-Sleep -Seconds 15
}
