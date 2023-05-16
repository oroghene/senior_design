import socket
# import pickle # serialization and deserialization

HEADER = 64
PORT = 5050
# SERVER = "192.168.1.152"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send('Hello World')
input()
send('Casamigos')
input()
send('For my amigos')
input()
send('It\'s gone')
send(DISCONNECT_MESSAGE)