# 网站本地真实速度测速工具  

一个基于Python和Selenium的网站加载速度测试工具，能够精确测量网页完整加载所需时间。  

## 🚀 功能特性  

- ✅ 精确测量网站完整加载时间  
- ✅ 支持缓存控制（可禁用或启用本地缓存）  
- ✅ 实时显示加载耗时  
- ✅ 自动定位chromedriver  
- ✅ 彩色终端输出(Win10可能不支持)  

> [!WARNING]
> 使用前请确保已安装 [Google Chrome](https://www.google.com/chrome/) 浏览器，这是Selenium自动化测试的必要依赖  

## 📦 依赖安装(仅限于你想使用py文件)  

**pip install -r requirements.txt**

## 🎯 使用示例  

[+] 欢迎使用网站加载计时器 (外置chromedriver版)  
[+] 请确保chromedriver.exe位于程序目录下的chromedriver-win64文件夹中  
[+] 请输入待检测网站的网址: example.com  

请选择缓存模式:  
1. 不使用本地缓存(第一次加载较慢)  
2. 使用本地缓存(需要两次加载)  
[+] 请输入选项数字(1/2): 2  

>**(这步骤测量完成后可能会报错，但不要紧，等一小会就可以正常显示最终加载时间了)**   

[+] 最终加载时间: 3.45 秒  

## ⚙️ 技术细节
 - 使用document.readyState确保页面完全加载
 - 多线程实现实时计时显示
 - 自动添加https协议前缀
 - 完善的错误处理机制

## 📜 许可证
MIT License

>作者: Mete0r | 博客: https://www.xscnet.cn/