import socket

def start_client():
    """启动TCP客户端并与服务器通信"""
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 建立连接
    s.connect(('127.0.0.1', 9999))
    
    # 接收并打印欢迎消息
    welcome_message = s.recv(1024).decode('utf-8')
    print(welcome_message)

    # 定义要发送的数据
    names = [b'Michael', b'Tracy', b'Sarah']
    for name in names:
        # 发送数据
        s.send(name)
        # 接收并打印响应
        response = s.recv(1024).decode('utf-8')
        print(response)
    
    # 发送退出命令
    s.send(b'exit')
    s.close()

if __name__ == '__main__':
    start_client()
