import socket

def send_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5002))  # IP 和端口號應該與 Unity 伺服器匹配
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()

send_message('1')