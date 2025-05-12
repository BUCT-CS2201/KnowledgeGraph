# PrincetonUniversityMuseum（第2个）爬取代码运行须知

## 11museum.py：爬虫代码

该代码通过脚本执行，如想仅仅执行单个代码，可通过命令行执行，其中第一个路径为计算机上已配置好的能够用于运行该python程序的虚拟环境的路径，第二个为**11museum.py**所在的路径，--start 1和--end 2分别为开始页码和结束页码

```powershell
& D:/Anaconda3/envs/SE/python.exe d:/SoftwareEngineering/11museum.py --start 1 --end 2     
```

## run_museum.ps1：并行执行脚本

$pythonPath需要修改为计算机上已配置好的能够用于运行python程序的虚拟环境的路径

$scriptPath需要修改为test2.py所在的路径

$startPage和$endPage为起始和结束页码，建议一次不要运行过多页，**内存会过载**

$kernel为线程数，$aver为每线程分配爬取页数

脚本运行命令

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 
.\run_museum.ps1
```
