# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import subprocess
import psutil
import time

def is_chrome_running():
    try:
        response = requests.get("http://127.0.0.1:9222/json")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False

def start_chrome():
    #chrome.exe --remote-debugging-port=9222 --user-data-dir="H:\work\selenum" --incognito #手动打开这个 
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"D:\selenum"
    command = [chrome_path, f"--remote-debugging-port=9222", f"--user-data-dir={user_data_dir}", "--incognito"]
    subprocess.Popen(command)

def kill_chrome_processes():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            proc.terminate()
            proc.wait()

# 检查 Chrome 是否在调试模式下运行
if not is_chrome_running():
    print("Chrome 没有在调试模式下运行，正在启动...")
    start_chrome()
    # 等待几秒钟让 Chrome 完全启动
    time.sleep(3)
    
chrome_options=Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
service = Service(executable_path=r'D:\chromedriver\chromedriver-win64\chromedriver-win64\chromedriver.exe')

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("浏览器已成功打开并连接到调试地址。")
except Exception as e:
    print(f"浏览器未能打开。错误信息: {e}")



try:
    #driver.get("https://auth.solidleisure.com:444/ac_portal/proxy.html?template=20240528094321&tabs=pwd&dual_stack=0&vlanid=249&url=https://solidleisure.awsapps.com%2Fstart%2F#/saml/default/Jumpserver/ins-aafdad643ee897f7")
    #driver.get("https://auth.solidleisure.com/ac_portal/20240528094321/pc.html?template=20240528094321&tabs=freeauth&dual_stack=0&vlanid=249&url=https://solidleisure.awsapps.com/start")
    driver.get("https://auth.solidleisure.com/ac_portal/20240528094321/pc.html?template=20240528094321&tabs=pwd&dual_stack=0&vlanid=249&url=https://www.gstatic.com%2Fgenerate_204")
    print("OK")
    driver.find_element(by=By.ID, value='password_name').send_keys('cesar')
    driver.find_element(by=By.ID, value='password_pwd').send_keys('solid@2024!')
    driver.find_element(by=By.ID, value='rememberPwd').click()
    driver.find_element(by=By.ID, value='password_disclaimer').click()
    driver.find_element(by=By.ID, value='password_submitBtn').click()

    # driver.find_element(by=By.ID, value='freeauth_disclaimer').click()
    # time.sleep(1)
    # driver.find_element(by=By.ID, value='freeauth_submitBtn').click()
    # 等待一段时间以确保页面跳转完成
    time.sleep(5)  # 根据页面的响应时间调整

    print("用户名、密码已输入，复选框已勾选。")
    
finally:
    # 确保在操作完成后关闭浏览器
    try:
        driver.quit()
        print("浏览器将要关闭。")
    except Exception as e:
        print(f"关闭浏览器时出错: {e}")
    # 强制终止任何剩余的 Chrome 进程
    kill_chrome_processes()        