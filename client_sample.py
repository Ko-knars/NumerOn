import socket
import select
import threading

host = "127.0.0.1"
port = 50019
bufsize = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_msg(sock):
    while True:
        msg = input()
        try:
            sock.send(msg.encode())
        except:
            print("Connection closed")
            break
         
    

def receive_msg(sock):
    while True:
        try:
            r_ready_sockets,w_ready_sockets,e_ready_sockets = select.select([sock],[],[], 0.5)
            if r_ready_sockets:
                recev_msg = sock.recv(bufsize).decode()
                if recev_msg == '':
                    print("Connection closed by server.")
                    break
                print(recev_msg)
        except:
            print("Connection closed")
            break


try:
    sock.connect((host,port))    
except Exception as e:
    print(e)


receive_thrd = threading.Thread(target = receive_msg, args = (sock,))
send_thrd = threading.Thread(target = send_msg, args = (sock,))
receive_thrd.start()
send_thrd.start()

receive_thrd.join()
send_thrd.join()
sock.close()
