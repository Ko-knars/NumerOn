import socket
import select
import threading

host = "127.0.0.1"
port = 50008
bufsize = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_msg(sock):
    while True:
        msg = input()
        sock.send(msg.encode())
    

def receive_msg(sock):
    while True:
        r_ready_sockets,w_ready_sockets,e_ready_sockets = select.select([sock],[],[])
        try:
            recev_msg = sock.recv(bufsize).decode()
            print(recev_msg)
        except:
            break
        #finally:
            #sock.close()
            #receive_msg("サーバとの接続が切断されました．")


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
