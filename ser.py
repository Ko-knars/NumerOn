import socket
import select
def send_to(sock, msg):
    try:
        sock.send(msg.encode())
        return True
    except:
        sock.close()
        return False

def broadcast(socklist, msg):
      for sock in socklist:
          if not send_to(sock,msg):
              sock_list.remove(sock)

number1 = []
number2 = []

            
host = '127.0.0.1'
port = 50001
backlog = 10
bufsize = 4096

#サーバーソケットの作成
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket is created")

try:
    server_sock.bind((host, port))
    print("socket bind")
    #同時に処理できる未処理の接続の最大数を指定
    server_sock.listen(backlog)
    print("socket listen")
    #sock_list：サーバーソケットとすべてのクライアントソケットを格納
    #sock_list（リスト）にサーバーソケットを格納
    sock_list = [server_sock]
    #クライアントのソケットをボートで管理するために、辞書でソケットを保存する
    client_sock_table = {}
    while True:
        r_ready_sockets, w_ready_sockets, e_ready_sockets = select.select(sock_list, [], [])
        for sock in r_ready_sockets:
            if sock == server_sock:
                conn, address = sock.accept()
                #sock_list（リスト）にクライアントソケットを格納
                sock_list.append(conn)
                #ボートをキーとしてソケットを保存する
                client_sock_table[address[1]] = conn
                #誰かからの接続があったことを全員に通知する
                sock_list.remove(server_sock)
                broadcast(sock_list,"ボート" + str(address[1]) + "")
                sock_list.append(server_sock)
                print(str(address) + "is connected")
            else:
                try:
                    b_msg = sock.recv(bufsize)
                    msg = b_msg.decode('utf-8')
                    if len(msg) == 0:
                        sock.close()
                        sock_list.remove(sock)
                    else:
                        sender_port = None
                        for key, val in client_sock_table.items():
                            if val == sock:
                                sender_port = key
                                break
                        if sender_port is not None:
                            sock_list.remove(server_sock)
                            #全員に受信したメッセージをbroadcast
                            broadcast(sock_list, str(sender_port) + ":" + msg)
                            sock_list.append(server_sock)
                except:
                    sock.close()
                    sock_list.remove(sock)
                    sock_list.remove(server_sock)
                    broadcast(sock_list, "someone disconnect")
                    sock_list.append(server_sock)

except Exception as e:
    print("Exception!")
    print(e)
    server_sock.close()