import socket
import os
#import myCustom
import threading


server_addr = '127.0.0.1', 5555
th=[];

sema = threading.Semaphore(3)

# Create a socket with port and host bindings
def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("start sock server")
    try:
        s.bind(server_addr)
    except socket.error as msg:
        print(msg)
    return s


# Establish connection with a client
def setupConnection(s):
    s.listen(1) 
    conn, addr = s.accept()
    return conn


# Get input from user
def GET():
    reply = input("Reply: ")
    return reply


def sendFile(filename, conn):
    f = open(filename, 'rb')
    line = f.read(1024)
    while line:
        conn.send(line)
        line = f.read(1024)
    f.close()


# Loop that sends & receives data
def dataTransfer(conn, s, mode):
    while True:
    # Send a File over the network
        try:
            data = conn.recv(4);
            # 최초 4바이트는 전송할 데이터의 크기
            length = int.from_bytes(data, "little")
            #데이터 분할하여 받기
            tmpByteData=b''
            while True:
                 tmpData = conn.recv(1024)
                 tmpByteData += tmpData
                 if len(tmpByteData) == length :
                     break
            jsonData = tmpByteData.decode('utf-8')
            sema.acquire()
            #filePath = myCustom.makeFile(jsonData)
            file_path = "./test.json"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(jsonData, file)
            sema.release()
            sendFile(filePath, conn)
            os.remove(filePath)
            break
        except:
            break
    conn.close()


sock = setupServer()
while True:
    try:
        connection = setupConnection(sock)
    except:
        break
    client = threading.Thread(target=dataTransfer, args=(connection, sock, "SEND"))
    client.start()
    th.append(client);
    for t in th[:]:
        if not t.is_alive():
            th.remove(t)
