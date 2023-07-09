import socket
import select
import time

def send_to(sock,msg):
    try:
        sock.send(msg.encode())
        return True
    except:
        sock.close()
        return False

def broadcast(sock_list, msg):
    for sock in sock_list:
        if not send_to(sock,msg):
            sock_list.remove(sock)

def game(player,prediction):
    eats = 0
    bites = 0

    for i in range(digit):
        prediction_num = prediction[i]
        if player[i] == prediction_num:
            eats = eats + 1
        
        if any(prediction_num  in player[j] for j in range(digit)):
            bites = bites + 1

    return str(eats) + "EAT" + str(bites-eats) + "BITE"


player1_num_list = []
player2_num_list = []
digit = 3


host = "127.0.0.1"
port = 50019
backlog = 1
bufsize = 4096

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket is created")

try:
    server_sock.bind((host,port))
    print("socket bind")
    server_sock.listen(backlog)
    print("socket listen")
    sock_list = []
    client_sock_table = {}
    
    while True:
        conn, address = server_sock.accept()
        if len(sock_list) < 2:
            sock_list.append(conn)
            client_sock_table[address[1]] = conn
            broadcast(sock_list, "ポート" + str(address[1]) + "")
            print(str(address) + "is connected")
            if len(sock_list) == 2:
                break
        else:
            print("connection refuse")
            conn.close()

    try:
        broadcast(sock_list, "ゲームを開始します")
        time.sleep(1)
        broadcast(sock_list, "三桁の数値を入力してください")
        player1_num = sock_list[0].recv(bufsize).decode('utf-8')
        player1_num_list = list(player1_num)
        broadcast([sock_list[0]], "player1の数値:" + str(player1_num))
        player2_num = sock_list[1].recv(bufsize).decode('utf-8')
        player2_num_list = list(player2_num)
        broadcast([sock_list[1]], "player2の数値:" + str(player2_num))
        player = 0
        
        while True:
            player = player + 1
            if player % 2 == 1:
                broadcast([sock_list[0]], "予測値を入力してください")
                input_prediction = sock_list[0].recv(bufsize).decode('utf-8')
                ans = game(player2_num_list, list(input_prediction))
                broadcast(sock_list, "player1の予測値:" + str(input_prediction))
                time.sleep(0.5)
                broadcast(sock_list, ans)
                time.sleep(0.5)
                if ans == "3EAT0BITE":
                    broadcast(sock_list, "player1の勝利です")
                    time.sleep(1)
                    break

            elif player % 2 == 0:
                broadcast([sock_list[1]], "予測値を入力してください")
                input_prediction = sock_list[1].recv(bufsize).decode('utf-8')
                ans = game(player1_num_list, list(input_prediction))
                broadcast(sock_list, "player2の予測値:" + str(input_prediction))
                time.sleep(0.5)
                broadcast(sock_list, ans)
                time.sleep(0.5)
                if ans == "3EAT0BITE":
                    broadcast(sock_list, "player2の勝利です")
                    time.sleep(1)
                    break
        sock_list[0].close()
        sock_list[1].close()
        server_sock.close()
    except:
        print("ゲーム中に予期せぬエラーが発生しました。")
        sock_list[0].close()
        sock_list[1].close()
        server_sock.close()

except Exception as e:
    print("Exception!")
    print(e)
    server_sock.close()

