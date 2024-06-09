import socket
import threading

def start_server():
    """啟動TCP伺服器"""
    # 創建一個TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 綁定伺服器到所有可用的接口（'0.0.0.0'）和端口5002
    server_socket.bind(('0.0.0.0', 5002))
    # 開始監聽傳入的連接，最大連接數為5
    server_socket.listen(5)
    print('伺服器已啟動，等待連接...')

    while True:
        # 接受一個新的連接
        client_socket, addr = server_socket.accept()
        print(f"連接來自: {addr}")
        # 為每個新連接啟動一個新的線程來處理客戶端
        threading.Thread(target=user_face, args=(client_socket,)).start()

def user_face(client_socket):
    """處理客戶端連接"""
    try:
        # 接收來自客戶端的數據，最大接收1024字節
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            # 將接收到的數據按逗號分割並轉換為整數列表
            values = list(map(int, data.split(',')))
            # 迭代接收到的每個數值並打印出來
            for value in values:
                print(f"接收到的數值: {value}")
    finally:
        # 關閉客戶端socket
        client_socket.close()
