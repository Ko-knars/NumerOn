import tkinter as tk
import socket, select
import threading

def send_msg(ev=None):
    if len(entered_txt.get()) <= 0:
        return
    #if entered_txt.get().isspace():
        #return
    sock.send(entered_txt.get().encode())
    #sock.send(er.encode())
    etr.delete(0, tk.END)
 
    
def receive_msg(msg):
    if text_w is None:
        return
    text_w.config(state=tk.NORMAL)
    text_w.insert(tk.END, msg + "\n")
    text_w.config(state=tk.DISABLED)
    text_w.see(tk.END)

#サーバから送られてきたメッセージをストックする．
def stock_msg(msg):
    stocked_msg.append(msg)
    
#ストックされたメッセージに対してreceive_msgを呼び出す．
def check_msg():
    while len(stocked_msg) > 0:
        receive_msg(stocked_msg.pop(0))
    #after(time,func)
    #funcの実行（呼び出し）をtime[ミリ秒]ごとに行う
    text_w.after(200, check_msg)

#サーバーから送信されたメッセージをストックする．
def listen(host, port, sock, bufsize=4096):
    try:
        sock.connect((host,port))
        while True:
            r_ready_sockets,w_ready_sockets,e_ready_sockets = select.select([sock],[],[])
            try:
                recev_msg = sock.recv(bufsize).decode()
                
            except:
                break
            #直近receive_msgを呼び出すのではなく、stock_msgを呼び出してメッセージをストックしておく
            stock_msg(recev_msg)
            
    except Exception as e:
        print(e)
    finally:
        sock.close()
        receive_msg("サーバとの接続が切断されました．")

# GUIの構築 -----
root = tk.Tk(None)
root.title("サンプルチャット")

frame = tk.Frame(master=root, width=480, height=320)

label1 = tk.Label(master=frame, text="サンプルチャット", font=('メイリオ', '12'), bg="#cccccc")
label1.place(relx=0, rely=0, relwidth=1.0, relheight=0.1)

#複数行テキスト
text_w = tk.Text(master=frame, state=tk.DISABLED, font=('メイリオ', '10'), bg="white")
text_w.place(relx=0.05, rely=0.1, relwidth=0.85, relheight=0.7)

#スクロールバー
sb_y = tk.Scrollbar(master=frame, orient=tk.VERTICAL, command=text_w.yview)
sb_y.place(relx=0.90, rely=0.1, relwidth=0.05, relheight=0.7)
text_w.config(yscrollcommand=sb_y.set)

#入力された文字列を扱うための文字列変数オブジェクト
entered_txt = tk.StringVar()
#er = "と発言しました"
#1行編集テキスト
etr = tk.Entry(master=frame, width = 30, textvariable = entered_txt)
etr.bind('<Return>', send_msg)
etr.place(relx = 0.05,rely = 0.85, relwidth = 0.65, relheight = 0.1)

#ボタン
bt = tk.Button(master = frame, text ="発言", bg = "skyblue", command = send_msg)
bt.place(relx = 0.75,rely = 0.85, relwidth = 0.20, relheight = 0.1)

frame.pack()

# メッセージ通信の開始 -----
host = '127.0.0.1'
port = 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#送られてきたメッセージをストックするためのリスト
stocked_msg = []

#ストックされたメッセージを定期的に処理するcheck_msgを呼び出す
check_msg()

#サーバから送信されたメッセージを持つ処理を別のスレッドで制御する
#threading.Threadのインスタンスを生成する
#targetで指定したlistenをスレッドで処理する

thrd = threading.Thread(target = listen, args = (host, port, sock))
thrd.start()
    
    
#GUIの表示
root.mainloop()