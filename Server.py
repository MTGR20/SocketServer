import socket

soc = socket.socket()
host = "" #IPv4
port = 8000
soc.bind((host, port))
soc.listen(5)

while True:
    print("Ready to connect")
    conn, addr = soc.accept()
    print("Got connection from",addr)
    length_of_message = int.from_bytes(conn.recv(2), byteorder='big')
    msg = conn.recv(length_of_message).decode("UTF-8")
    print('받은 메세지: ' + msg)
    print(length_of_message)

    message_to_send = "Bye".encode("UTF-8")
    conn.send(len(message_to_send).to_bytes(2, byteorder='big'))
    conn.send(message_to_send)

    '''
    # Note the corrected indentation below
    if "Hello"in msg:
        message_to_send = "Bye".encode("UTF-8")
        conn.send(len(message_to_send).to_bytes(2, byteorder='big'))
        conn.send(message_to_send)
    else:
        print("no message")
    '''
