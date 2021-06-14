import socket
from tkinter import *
from _thread import *

c_sockList = []
s_sock = None
c_sockNameList = []

def s_thread(c_sock, addr):
    global chat_log
    chat_log['state'] = 'normal'
    chat_log.insert("end", '접속 :' + addr[0] + ':' + str(addr[1]) + '\n')
    chat_log['state'] = 'disabled'
    while True:
        try:
            data = c_sock.recv(1024)
            if(data==''):
                continue
            data=str(data.decode()).split('|')
            if data[0] == 'id,':
                for c in c_sockNameList:
                    if(c==data[1]):
                        print('중복')
                        raise NameError('중복')

                c_sockNameList.append(data[1])
                chater_list['state'] = 'normal'
                chater_list.insert("end",data[1] + '\n')
                chater_list['state'] = 'disabled'
                for c in c_sockList:
                    msg = '[접속인원]'
                    for Name in c_sockNameList:
                        msg = msg + Name + '|'
                    c.sendall(msg.encode())
                    c.sendall(('[시스템] ' + data[1] + ' 님이 접속하였습니다.').encode())
            else:
                for c in c_sockList:
                    c.sendall((data[0] + ' : ' + data[1]).encode())
                chat_log['state'] = 'normal'
                chat_log.insert("end",
                                '받은 데이터 ' + addr[0] + ' : ' + str(addr[1]) + ' :: ' + data[1] + '\n')
                chat_log['state'] = 'disabled'
        except ConnectionResetError as e:
            c_sockList.remove(c_sock)
            c_sockNameList.remove(data[1])
            chater_list_del()
            for c in c_sockList:
                c.sendall(('[시스템] ' + data[1] + ' 님이 나갔습니다.').encode())
                msg = '[접속인원]'
                for Name in c_sockNameList:
                    msg = msg + Name + '|'
                    chater_list['state'] = 'normal'
                    chater_list.insert("end", Name + '\n')
                    chater_list['state'] = 'disabled'
                c.sendall(msg.encode())
            chat_log['state'] = 'normal'
            chat_log.insert("end", '접속 종료 ' + addr[0] + ':' + str(addr[1]) + '\n')
            chat_log['state'] = 'disabled'
            break
        except NameError as e:
            c_sockList.remove(c_sock)
            print('중복')
            c_sock.sendall(('[아이디 중복]').encode())
            chat_log['state'] = 'normal'
            chat_log.insert("end", '아이디 중복 종료 ' + addr[0] + ':' + str(addr[1]) + '\n')
            chat_log['state'] = 'disabled'
            c_sock.close()
            break
    c_sock.close()
def chater_list_del():
    chater_list['state'] = 'normal'
    chater_list.delete(1.0, "end")
    chater_list['state'] = 'disabled'
def s_open():
    host = en_ip.get();
    port = int(en_port.get())
    start_new_thread(s_make, (host, port))
    btn_open['state'] = 'disabled'
    en_ip['state'] = 'readonly'
    en_port['state'] = 'readonly'
    btn_close['state'] = 'active'
    btn_kick['state'] = 'active'
    en_kick['state'] = 'normal'

def s_close():
    global s_sock
    btn_open['state'] = 'active'
    en_ip['state'] = 'normal'
    en_port['state'] = 'normal'
    btn_close['state'] = 'disabled'
    btn_kick['state'] = 'disabled'
    en_kick['state'] = 'readonly'
    s_sock.close()
    chater_list_del()
def s_make(host, port):
    try:
        global s_sock
        s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_sock.bind((host, port))
        s_sock.listen()
        chat_log['state'] = 'normal'
        chat_log.insert("end", '서버 시작\n')
        chat_log['state'] = 'disabled'
        while True:
            client_socket, addr = s_sock.accept()
            c_sockList.append(client_socket)
            start_new_thread(s_thread, (c_sockList[-1], addr))
    except Exception as e:
        chat_log['state'] = 'normal'
        chat_log.insert("end", '{}\n'.format(e))
        chat_log.insert("end", '서버 중지\n')
        chat_log['state'] = 'disabled'
        s_close()
    finally:
        s_sock.close()

def kick():
    name = en_kick.get()
    try:
        c_sockList[c_sockNameList.index(name)].sendall(('[kick]').encode())
        del c_sockList[c_sockNameList.index(name)]
        c_sockNameList.remove(name)
        chater_list_del()
        for c in c_sockList:
            c.sendall(('[시스템 추방] ' + name + ' 님이 추방되었습니다.').encode())
            msg = '[접속인원]'
            for Name in c_sockNameList:
                msg = msg + Name + '|'
            c.sendall(msg.encode())
        chat_log['state'] = 'normal'
        chat_log.insert("end", '추방 '+name + '\n')
        chat_log['state'] = 'disabled'
        chater_list_del()
        for Name in c_sockNameList:
            chater_list['state'] = 'normal'
            chater_list.insert("end", Name + '\n')
            chater_list['state'] = 'disabled'
    except Exception as e:
        print(e)

### GUI

win = Tk()
win.geometry('760x450')
win.title('서버')
win.resizable(False, False)

Label(win, text = '서버 IP : ').place(x=20, y=20)
Label(win, text = '포트 : ').place(x=190, y=20)
Label(win, text = '접속중').place(x=475, y=60)
en_ip = Entry(win, width=14)
en_ip.place(x=83, y=21)
en_ip.insert(0,'127.0.0.1')

en_port = Entry(win, width=5, text = '9190')
en_port.place(x = 240, y=21)
en_port.insert(0,'9190')
btn_open = Button(win,text='서버 실행', command=s_open)
btn_open.place(x=310, y=18)
btn_close = Button(win,text='서버 닫기',command=s_close, state='disabled')
btn_close.place(x=400, y = 18)
en_kick = Entry(win, width=14, state='readonly')
en_kick.place(x=480, y = 18)
btn_kick = Button(win,text='강퇴', command=kick, state='disabled')
btn_kick.place(x=585, y = 18)

chat_frame = Frame(win)
chater_frame = Frame(win)
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side='right',fill='y')
scrollbar2 = Scrollbar(chater_frame)
scrollbar2.pack(side='right',fill='y')
chat_log = Text(chat_frame, width=62, height=28, state='disabled', spacing2=2)
chat_log.pack(side='left')
chater_list = Text(chater_frame, width = 35, height = 26, state = 'disabled', yscrollcommand = scrollbar.set)
chater_list.pack(side='left')
chat_frame.place(x=20, y=60)
chater_frame.place(x=475, y=80)
win.mainloop()