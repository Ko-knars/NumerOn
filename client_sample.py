import socket
import select
import threading

host = "127.0.0.1"
port = 50028
bufsize = 4096
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

         
def receive_msg(sock):
    while True:
        try:
            r_ready_sockets,w_ready_sockets,e_ready_sockets = select.select([sock],[],[], 0.5)
            if r_ready_sockets:
                recev_msg = sock.recv(bufsize).decode()
                if recev_msg == '':
                    print("Connection closed by server.")
                    break
                text_box.insert(tk.END, recev_msg + "\n")
        except:
            print("Connection closed")
            break


try:
    sock.connect((host,port))    
except Exception as e:
    print(e)




import tkinter as tk
import tkinter.font as font

root = tk.Tk()
root.title('NumerOn')


my_font = font.Font(family='Helvetica', size=20, weight='bold')


labels = [tk.Label(root, text='', width=2, height=1, bg='white', font=my_font) for _ in range(3)]
for i, label in enumerate(labels):
    label.grid(row=0, column=i, padx=5, pady=5)
    
text_box = tk.Text(root, width=20, height=20)
text_box.grid(row=1, column=3, rowspan=4, padx=5, pady=5)

def click(number):
    for label in labels:
        if label.cget('text') == '':
            label.config(text=str(number))
            break

def clear():
    for label in reversed(labels):
        if label.cget('text') != '':
            label.config(text='')
            break

def send():
    if all(label.cget('text') != '' for label in labels):
        number = ''.join(label.cget('text') for label in labels)
        try:
            sock.send(number.encode())
        except:
            print("Connection closed")
        for label in labels:
            label.config(text='')


button_texts = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['0', 'Clear', 'Call']
]
for i, row in enumerate(button_texts):
    for j, text in enumerate(row):
        if text.isdigit():
            button = tk.Button(root, text=text, command=lambda number=text: click(number), font=my_font, width=5, height=2)
        else:
            button = tk.Button(root, text=text, command=clear if text == 'Clear' else send, font=my_font, width=5, height=2)
        button.grid(row=i+1, column=j, sticky='nsew', padx=5, pady=5)


for i in range(3):
    root.grid_columnconfigure(i, weight=1)
for i in range(5):
    root.grid_rowconfigure(i, weight=1)

receive_thrd = threading.Thread(target = receive_msg, args = (sock,))
receive_thrd.start()
root.mainloop()
