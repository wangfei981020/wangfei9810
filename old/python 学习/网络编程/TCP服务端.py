import socket
import threading
import time

def tcplink(sock, addr):
    """处理与客户端的连接"""
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')

    while True:
        data = sock.recv(1024)
        if not data:
            break  # 如果没有数据，退出循环

        # 解码并处理数据
        message = data.decode('utf-8')
        if message == 'exit':
            break
        
        response = f'Hello, {message}!'
        sock.send(response.encode('utf-8'))
    
    sock.close()
    print('Connection from %s:%s closed.' % addr)

def start_server():
    """启动TCP服务器"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print('Waiting for connection...')

    while True:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

if __name__ == '__main__':
    start_server()