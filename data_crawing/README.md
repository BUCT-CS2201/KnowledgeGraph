# 爬取代码运行须知（Harvard Art Museum为例）

## txt_split.py:地址数组分割代码

将爬取下来的url集合（**item_links.txt**）按以100为一组，分割为61组，命名为**item_links_{x}**,x为组序号

## Harvard_Art_Museum_Data_Crawling.py：爬虫代码

166-233行的被注释掉的代码的功能为仅爬取文物url，并将爬取到的url集合保存到**item_links.txt**中



237行附近 D:\SoftwareEngineering\museum3\ 需要改为**item_links_1.txt**所在前缀路径

```python
with open(r"D:\SoftwareEngineering\museum3\item_links_" + str(p4ge) + ".txt", "r", encoding="utf-8") as f:
    item_links = [line.strip() for line in f.readlines()]
```



该代码通过脚本执行，如想仅仅执行单个代码，可通过命令行执行，其中第一个路径为计算机上已配置好的能够用于运行该python程序的虚拟环境的路径，第二个为**Harvard_Art_Museum_Data_Crawling.py**所在的路径，--page 3的3可改为指定的组序号

```powershell
& D:\Anaconda3\envs\SE\python.exe d:\SoftwareEngineering\museum3\fast_crawler.py --page 3
```

## run_museum.ps1：并行执行脚本

$pythonPath需要修改为计算机上已配置好的能够用于运行python程序的虚拟环境的路径

$scriptPath需要修改为Harvard_Art_Museum_Data_Crawling.py所在的路径

脚本运行命令

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 
.\run_museum3.ps1
```

$startPage和$endPage为起始和结束组序号，建议一次不要运行过多页，**内存会过载**