import socket

def send_message(message):
    """發送訊息到TCP伺服器"""
    # 創建一個TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 連接到伺服器（IP地址'127.0.0.1'，端口5002）
    client_socket.connect(('127.0.0.1', 5002))
    # 發送訊息
    client_socket.sendall(message.encode('utf-8'))
    # 關閉socket
    client_socket.close()

# 發送訊息 '1' 到伺服器
send_message('1')
