from email_handler import make_email, send_email
from config import save_config
import shutil

title = """
______         _  _          _   _  _  _     _               
|  _  \       (_)| |        | | | |(_)| |   (_)              
| | | |  __ _  _ | | _   _  | |_| | _ | | __ _  _ __    __ _ 
| | | | / _` || || || | | | |  _  || || |/ /| || '_ \  / _` |
| |/ / | (_| || || || |_| | | | | || ||   < | || | | || (_| |
|___/   \__,_||_||_| \__, | \_| |_/|_||_|\_\|_||_| |_| \__, |
                      __/ |                             __/ |
                     |___/                             |___/ 
"""

options = "1: 이메일 전송\n" \
        "2: 이메일 정보 입력\n" \
        "3: 데이터 삭제\n" \
        "4: 프로그램 종료"

def run_client():
    while True:
        print(title)
        print(options)
        opt = input("> ")
        print()
        try:
            if int(opt)==1:
                print("이메일을 전송합니다.")
                subject, body, attach = make_email()
                send_email(subject, body, attach)
            elif int(opt)==2:
                print("사용할 Gmail 계정을 입력하세요.")
                account = input("> ")
                if not account.endswith('@gmail'):
                    account += '@gmail'
                print("Gmail 계정의 2차 패스워드를 입력하세요.")
                pwd = input("> ")
                print("전송 받을 이메일 주소를 입력하세요.")
                receiver = input("> ")
                save_config("email", "sender", account)
                save_config("email", "receiver", receiver)
                save_config("email", "username", account)
                save_config("email", "password", pwd)
            elif int(opt)==3:
                try:
                    shutil.rmtree("log")
                    print("로그데이터가 삭제 되었습니다.")
                except OSError as e:
                    print("삭제할 로그데이터가 없습니다.")    
                continue
            elif int(opt)==4:
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 입력해주세요")    
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run_client()