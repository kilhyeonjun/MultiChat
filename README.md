# MultiChat
python Thread기반 멀티 채팅

## 개요
멀티 스레드 기반 TCP IP 소켓프로그래밍의 프로젝트를 곰곰히 생각해 보다가
게임아니면 챗봇인거 같아서 Python으로 제작해 보았습니다.

## 목적
멀티 스레드를 이용하여 서버에 여러 클라이언트가 다중으로 접속이 가능하게 구현을 하였고 이를 통해 
여러 클라이언트가 하나의 서버에서 서로 소통을 할 수 있게 되었습니다.

## 설계 및 기능

### server.py

def s_open():
서버 실행 버튼 클릭시 사용자에게 입력 받은 server ip와 port번호를 인자값으로 s_make 함수에 스레드 할당

def s_make(host, port):
입력 받은 인자값으로 서버 소켓 할당후 무한루프문을 통해 클라이언트 소켓 받아와 리스트에 넣고 s_thread 함수에 스레드 할당

def s_thread(c_sock, addr):
무한루프문을 통해 데이터 계속 수신 수신한 데이터 별로 모든 클라이언트에게 데이터 전송(클라이언트 접속/종료, 채팅, 참여중인 클라이언트 정보, 아이디 중복)

def s_close():
서버 닫기 버튼 클릭시
소켓 종료

def kick():
강퇴버튼 클릭시 en_kick엔트리에 닉네임 값을 받아와 해당 클라이언트에게 kick메세지 전송후 클라이언트 삭제

### client.py

def try_login():
로그인버튼 클릭시 login 함수에 스레드 할당

def login():
사용자에게 입력 받은 server ip와 port번호를 인자값으로 소켓 할당후 커넥트에 성공하면 send, recv 함수에 해당 소켓을 인자값으로 스레드 할당

def send(sock):
무한루프문을 통해 데이터 입력시 데이터 보냄.
로그아웃 했을 경우 해당 소켓 종료후 쓰레드 종료

def recv(sock):
무한루프문을 통해 데이터 계속 수신.
각 수신한 데이터 별로 (클라이언트 접속/종료, 채팅, 참여중인 클라이언트 정보, 아이디 중복) 수행

def try_logout():
로그아웃 버튼 클릭시 실행

def set_flag_send(event):
 enter키 이벤트 리스너
 데이터 송신 boolean값 True로 변경

## 차이점
각 클라이언트에서 닉네임 할당이 가능하고 상시적으로 접속중인 정보를 보여줌
서버에서 닉네임으로 클라이언트 강퇴가 가능함

## 실행화면

### 서버 GUI
<img width="" height="" src="./image/서버 처음.png"></img>
### 서버 실행
<img width="" height="" src="./image/서버 실행.png"></img>
### 클라이언트 GUI
<img width="" height="" src="./image/클라이언트 처음.png"></img>
### 클라이언트 접속
<img width="" height="" src="./image/클라이언트 접속.png"></img>
### 클라이언트 닉네임 중복 접속
<img width="" height="" src="./image/클라이언트 중복 접속.png"></img>
<img width="" height="" src="./image/서버 아이디 중복.png"></img>
### 채팅
<img width="" height="" src="./image/채팅.PNG"></img>
<img width="" height="" src="./image/서버 채팅 로그.png"></img>
### 강퇴
<img width="" height="" src="./image/서버 강퇴1.png"></img>
<img width="" height="" src="./image/서버 강퇴2.png"></img>
<img width="" height="" src="./image/클라이언트 추방.PNG"></img>
### 접속 종료
<img width="" height="" src="./image/클라이언트 종료.PNG"></img>
<img width="" height="" src="./image/서버 클라이언트 종료.png"></img>
