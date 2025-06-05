from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(filename='D:\chromedriver\chromedriver130\login_network\login_network.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def login():
    # 创建 Chrome 配置选项
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略 SSL 证书错误
    chrome_options.add_argument('--allow-insecure-localhost')   # 允许不安全的本地连接
    # 手动指定 ChromeDriver 的路径
    chrome_driver_path = 'D:\chromedriver\chromedriver130\chromedriver-win64\chromedriver.exe'  # 替换为实际路径
    # 创建服务对象
    service = Service(chrome_driver_path)
    # 创建 WebDriver 实例
    driver = webdriver.Chrome(service=service,options=chrome_options)
    # 打开网页
    driver.get('https://auth.solidleisure.com/ac_portal/20240528094321/pc.html?template=20240528094321&tabs=pwd&dual_stack=0&vlanid=249&url=https://www.gstatic.com%2Fgenerate_204')  # 替换为你要访问的 URL
    # 输入用户名
    try:
        username = driver.find_element(By.ID,'password_name')
        username.send_keys('cesar')
        password = driver.find_element(By.ID,'password_pwd')
        password.send_keys('QWERqwer-123')
        login_button = driver.find_element(By.ID,'password_submitBtn')
        login_button.click()
        logging.info("点击登录按钮成功")
    except Exception as e:
        print("发生异常",e)

    finally:
        time.sleep(5)  # 等待 5 秒
        driver.quit()
        logging.info("浏览器已关闭")

def main():
    login()
     
main()

