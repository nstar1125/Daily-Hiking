import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import load_config
from report_generator import export_report

def make_email():
    export_report()
    cur_date_name = datetime.today().strftime("%Y년 %m월 %d일")
    cur_date = datetime.today().strftime("%Y-%m-%d")
    subject=f"{cur_date_name}의 리포트가 도착했습니다. 📈"
    report_path = f"log/reports/{cur_date}_정기리포트.pdf"
    content = "오늘의 정기리포트입니다!"
    return subject, content, report_path

def send_email(subject, body, attachment_path=None):
    email_config = load_config("email")
    msg = MIMEMultipart()
    msg['From'] = email_config['sender']
    msg['To'] = email_config['receiver']
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name='정기리포트.pdf')
            part['Content-Disposition'] = f'attachment; filename={attachment_path}'
            msg.attach(part)
    
    try:
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"정기리포트가 {email_config['receiver']}로 전송 되었습니다. ({cur_time})")
    except:
        print("이메일 전송에 실패했습니다. 이메일 정보가 맞는지 확인해주세요.")

if __name__ == "__main__":
    subject, body, attach = make_email()
    send_email(subject, body, attach)