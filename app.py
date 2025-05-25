import os
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from colorama import init, Fore, Style

# ------------------------ 颜色支持双重保障 ------------------------
# 方法1：强制Windows启用ANSI支持
if sys.platform == "win32":
    from ctypes import windll
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# 方法2：初始化Colorama（自动处理跨平台颜色）
init(autoreset=True)

# ------------------------ 主程序代码 ------------------------


def get_chromedriver_path():
    """获取外置chromedriver路径（优先同级目录下的chromedriver-win64文件夹）"""
    try:
        # 获取可执行文件所在目录（打包后）或脚本目录（开发时）
        base_path = os.path.dirname(sys.executable) if getattr(
            sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

        # 尝试查找chromedriver的路径
        possible_paths = [
            # 同级目录下的chromedriver-win64文件夹
            os.path.join(base_path, "chromedriver-win64", "chromedriver.exe"),
            # 直接同级目录
            os.path.join(base_path, "chromedriver.exe"),
            # 系统PATH环境变量中的路径
            "chromedriver.exe"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(
                    f"{Fore.BLUE}[+] 使用chromedriver路径: {path}{Style.RESET_ALL}")
                return path

        raise FileNotFoundError(
            "未找到chromedriver.exe，请确保它在程序目录下的chromedriver-win64文件夹中")

    except Exception as e:
        print(f"{Fore.RED}[错误] 无法定位chromedriver: {e}{Style.RESET_ALL}")
        input("按任意键退出...")
        sys.exit(1)


def load_website(url, use_cache):
    """加载网站并计算加载时间（显示浏览器窗口）"""
    driver = None
    try:
        # 设置Chrome选项
        options = webdriver.ChromeOptions()

        # 性能优化参数
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # 缓存设置
        if use_cache == 1:
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-cache")
        else:
            options.add_argument("--disk-cache-size=104857600")

        # 获取chromedriver路径
        chromedriver_path = get_chromedriver_path()

        # 启动浏览器服务
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)  # 设置页面加载超时60秒

        # 开始计时
        start_time = time.time()
        print(f"{Fore.GREEN}[+] 开始计时...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] 正在加载: {url}{Style.RESET_ALL}")

        # 实时显示计时器
        timer_stop = False

        def display_timer():
            while not timer_stop:
                elapsed_time = time.time() - start_time
                print(
                    f"{Fore.YELLOW}已加载时间: {elapsed_time:.2f} 秒{Style.RESET_ALL}", end="\r")
                time.sleep(0.1)
            print()

        timer_thread = threading.Thread(target=display_timer, daemon=True)
        timer_thread.start()

        # 访问网页
        driver.get(url)

        # 等待页面完全加载
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )

        # 结束计时
        end_time = time.time()
        timer_stop = True
        timer_thread.join()

        load_time = end_time - start_time
        print(
            f"{Fore.GREEN}[+] 页面加载完成，总时间: {load_time:.2f} 秒{Style.RESET_ALL}")

        # 保持浏览器打开5秒让用户查看
        print(f"{Fore.CYAN}[+] 浏览器窗口将保持5秒供查看...{Style.RESET_ALL}")
        time.sleep(5)

        return load_time

    except Exception as e:
        print(f"{Fore.RED}[错误] 加载网站时出错: {str(e)}{Style.RESET_ALL}")
        return -1

    finally:
        if driver:
            driver.quit()


def main():
    """主程序"""
    try:
        # 显示欢迎信息
        print(
            f"{Fore.YELLOW}[+] 欢迎使用网站加载计时器 (外置chromedriver版){Style.RESET_ALL}")
        print(
            f"{Fore.BLUE}[+] 请确保chromedriver.exe位于程序目录下的chromedriver-win64文件夹中{Style.RESET_ALL}")
        print(
            f"{Fore.BLUE}[+] 作者: Mete0r | 博客: {Fore.GREEN}https://www.xscnet.cn{Style.RESET_ALL}")

        # 获取用户输入
        url = input(f"{Fore.CYAN}[+] 请输入待检测网站的网址: {Style.RESET_ALL}").strip()
        if not url:
            raise ValueError("网址不能为空")

        # 自动添加协议
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        # 缓存选项
        use_cache = int(input(f"""{Fore.CYAN}
请选择缓存模式:
1. 不使用本地缓存(第一次加载较慢)
2. 使用本地缓存(需要两次加载)
[+] 请输入选项数字(1/2): {Style.RESET_ALL}"""))

        if use_cache not in (1, 2):
            raise ValueError("请输入1或2")

        # 预热加载（如果选择使用缓存）
        if use_cache == 2:
            print(f"{Fore.MAGENTA}[+] 正在进行预热加载（不计时）...{Style.RESET_ALL}")
            if load_website(url, use_cache=1) == -1:
                raise RuntimeError("预热加载失败")

        # 正式加载并计时
        print(f"{Fore.MAGENTA}[+] 开始正式加载并计时...{Style.RESET_ALL}")
        load_time = load_website(url, use_cache)

        if load_time > 0:
            print(
                f"{Fore.GREEN}[+] 最终加载时间: {load_time:.2f} 秒{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] 未能成功测量加载时间{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[错误] {str(e)}{Style.RESET_ALL}")

    finally:
        print(f"{Fore.YELLOW}[+] 检测完成，感谢使用！{Style.RESET_ALL}")
        input("按任意键退出...")


if __name__ == "__main__":
    main()
