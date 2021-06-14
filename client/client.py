import socket
from _thread import *
import threading
from tkinter import *
from time import sleep

flag_out, flag_send = False, False

def send(sock):
    global flag_send, flag_out
    while True:
        if flag_send:
            msg = (txt_msg.get(1.0,"end").rstrip())
            sock.send((en_name.get()+'|'+msg).encode())
            txt_msg.delete(1.0, "end")
            flag_send = False
        else:
            if flag_out:
                sock.close()
                exit()
            sleep(0.1)

def chater_list_del():
    chater_list['state'] = 'normal'
    chater_list.delete(1.0, "end")
    chater_list['state'] = 'disabled'
def recv(sock):
    while True:
        try:
            data = str(sock.recv(1024).decode())
            if(data[0:6] == '[접속인원]'):
                chater_list_del()
                data=data.replace("[접속인원]","")
                data=data.split('|')
                for d in data:
                    chater_list['state'] = 'normal'
                    chater_list.insert("end", d + '\n')
                    chater_list['state'] = 'disabled'
            elif(data[0:8]=='[아이디 중복]'):
                print('중복')
                raise NameError('중복')
            elif (data[0:6] == '[kick]'):
                raise ConnectionAbortedError('강퇴')
            elif (data[0:8] == '[시스템 추방]'):
                sock.send(('').encode())
                chat_log['state'] = 'normal'
                chat_log.insert("end", data+'\n')
                chat_log['state'] = 'disabled'
            else:
                chat_log['state'] = 'normal'
                chat_log.insert("end",str(data+'\n'))
                chat_log['state'] = 'disabled'
        except ConnectionAbortedError as e:
            print(e)
            chat_log['state'] = 'normal'
            chat_log.insert("end", '[시스템] 접속을 종료합니다.\n')
            chat_log['state'] = 'disabled'
            try_logout()
            sock.close()
            exit()
        except NameError as e:
            chat_log['state'] = 'normal'
            chat_log.insert("end", '[시스템] 아이디가 중복되었습니다..\n')
            chat_log['state'] = 'disabled'
            try_logout()
            sock.close()
            exit()
def login():
    host = en_ip.get()
    port = int(en_port.get())
    try:
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_sock.connect((host, port))
        c_sock.send(("id," + "|" + en_name.get()).encode())
        threading.Thread(target=send, args=(c_sock,)).start()
        threading.Thread(target=recv, args=(c_sock,)).start()
        exit()
    except Exception as e:
        chat_log['state'] = 'normal'
        chat_log.insert("end", '[시스템] 접속을 실패 했습니다.\n')
        chat_log['state'] = 'disabled'
        try_logout()



def try_login():
    global flag_out
    start_new_thread(login,())
    btn_login['state'] = 'disabled'
    btn_logout['state'] = 'active'
    en_ip['state'] = 'readonly'
    en_port['state'] = 'readonly'
    en_name['state'] = 'readonly'
    flag_out = False

def try_logout():
    global flag_out
    btn_login['state'] = 'active'
    btn_logout['state'] = 'disabled'
    en_ip['state'] = 'normal'
    en_port['state'] = 'normal'
    en_name['state'] = 'normal'
    flag_out = True
    chater_list_del()

def set_flag_send(event):
    global flag_send
    flag_send = True


### GUI

win = Tk()
win.geometry('580x450')
win.title('클라이언트')
win.resizable(False, False)

Label(win, text = '서버 IP : ').place(x=20, y=20)
Label(win, text = '포트 : ').place(x=190, y=20)
Label(win, text = '이름 : ').place(x=270, y=20)
Label(win, text = '접속중').place(x=475, y=60)
en_ip = Entry(win, width=14)
en_ip.place(x=83, y=21)
en_ip.insert(0,'127.0.0.1')
en_port = Entry(win, width=5)
en_port.place(x = 230, y=21)
en_port.insert(0,'9190')
en_name = Entry(win, width=9)
en_name.place(x = 310, y=21)
en_name.insert(0,'name')
btn_login = Button(win,text='로그인', command=try_login)
btn_login.place(x=390, y=18)
btn_logout = Button(win,text='로그아웃',state = 'disabled', command = try_logout)
btn_logout.place(x=440, y=18)


chat_frame = Frame(win)
chater_frame = Frame(win)
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side='right',fill='y')
scrollbar2 = Scrollbar(chater_frame)
scrollbar2.pack(side='right',fill='y')
chat_log = Text(chat_frame, width = 62, height = 24, state = 'disabled', yscrollcommand = scrollbar.set)
chat_log.pack(side='left')
chater_list = Text(chater_frame, width = 12, height = 22, state = 'disabled', yscrollcommand = scrollbar.set)
chater_list.pack(side='left')
scrollbar['command'] = chat_log.yview
chat_frame.place(x=20, y=60)
chater_frame.place(x=475, y=80)
txt_msg = Text(win, width = 55, height = 4)
txt_msg.place(x=20,y = 390)
btn_send = Button(win, text = 'Send', command = lambda: set_flag_send(None))
btn_send.place(x=430, y=405)
txt_msg.bind("<Return>",set_flag_send)

win.mainloop()