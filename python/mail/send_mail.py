#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText


class Sender:
    def __init__(self, sender, smtp_server, port, password, timeout=10):
        self.sender = sender
        self.smtp_server = smtp_server
        self.port = port
        self.password = password
        self.timeout = timeout
        self.mail = smtplib.SMTP_SSL(host=self.smtp_server, port=self.port, timeout=self.timeout)
        self.mail.login(self.sender, self.password)


    def send(self, subject, content, receiver):
        # 构造邮件内容
        msg = MIMEText(content, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = receiver
        # 发送邮件
        receiver = receiver.split(",")
        self.mail.sendmail(self.sender, receiver, msg.as_string())
        self.mail.quit()
        print("发送成功!")


if __name__ == "__main__":
    receiver = "wufeiqun@xxx.com, wufeiqun@yyy.com" # 邮件接收者是以逗号分隔的字符串
    # 邮件内容是HTML文本
    content = """
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="https://www.python.org">你好</a> you wanted.
        </p>
      </body>
    </html>
    """
    s = Sender("xxx@xxx.com", "smtp.xxx.com", 465, "xxx") # 发送者的登录信息配置
    s.send("测试邮件", content, receiver) # 邮件内容和标题的配置

